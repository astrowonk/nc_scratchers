import polars as pl
import pandas as pd
import re
import datetime
from sqlalchemy import create_engine
from helpers import print_to_slack
import traceback
import sqlite3
from great_tables import GT
import requests
from io import StringIO
from bs4 import BeautifulSoup
import json
from config import PROXIES


class NCScratcherScraper:
    URL = 'https://nclottery.com/scratch-off-prizes-remaining'
    summary_df: pl.DataFrame = None
    detail_df: pl.DataFrame = None
    game_id_dict: dict = None

    def __init__(self):
        self.page_request = requests.get(self.URL, proxies=PROXIES)
        self.soup = BeautifulSoup(self.page_request.content, 'html.parser')
        self.scrape_tables()
        self.engine = create_engine('sqlite:///nc_database.db')

    def scrape_url_dict(self):
        self.link_dict = {}
        all_th = self.soup.find_all('th', class_='ticketdetails')
        for item in all_th:
            href = item.find('span', class_='gamename').find('a').get('href')
            number_text = item.find('span', class_='gamenumber').text
            game_num = re.search(r'(\d+)', number_text)[0]
            self.link_dict[game_num] = href
        self.game_id_dict = (
            self.summary_df
            .group_by('game')
            .agg(pl.col('game_number').first())
            .to_pandas()
            .set_index('game_number')['game']
            .to_dict()
        )
        self.game_id_dict = {int(k): val for k, val in self.game_id_dict.items()}

    def scrape_tables(self):
        self.tables = pd.read_html(StringIO(self.page_request.content.decode('UTF-8')))
        self.scrape_time = datetime.datetime.now()

    @staticmethod
    def process_cleaned(cleaned):
        calibration_data = (
            cleaned
            .with_columns(variance=1 / pl.col('winners_at_start').sqrt())
            .filter(pl.col('variance').lt(0.005))
            .sort('value', descending=True)
            .with_columns(fraction=pl.col('winners_remaining') / pl.col('winners_at_start'))
            .head(1)['fraction', 'value']
        )
        calibration_ratio = calibration_data.item(0, 0)
        calibration_value = calibration_data.item(0, 1)

        # The calibration ratio is the highest prize where 1/ sqrt(n) > .005. Cheap prices like $1 ones often go unclaimed.
        # So this gives the best estimate of how many tickets have been sold.

        return (
            cleaned
            .with_columns(
                total_tickets=(pl.col('odds_scraped') * pl.col('winners_at_start'))
                .round()
                .cast(pl.Int32)
            )
            .with_columns(mode_total=pl.col('total_tickets').mode().first())
            .with_columns(
                odds_at_start_computed=pl.col('mode_total') / pl.col('winners_at_start')
            )
            .with_columns(
                new_odds=pl
                .when(pl.col('value').gt(calibration_value))
                .then((pl.col('mode_total') * calibration_ratio) / pl.col('winners_remaining'))
                .otherwise(pl.col('odds_at_start_computed'))
            )
            .with_columns(
                original_expectation_value=(pl.col('value') / pl.col('value').min())
                / pl.col('odds_at_start_computed'),
                expectation_score=pl.col('odds_at_start_computed') / pl.col('new_odds'),
                current_expectation_value=(pl.col('value') / pl.col('value').min())
                / pl.col('new_odds'),
                fraction_unclaimed=pl.col('winners_remaining') / pl.col('winners_at_start'),
            )
        )

    @staticmethod
    def clean_df(df: pd.DataFrame):
        title = df.columns[0][0]
        df.columns = ['value', 'odds_scraped', 'winners_at_start', 'winners_remaining']
        dfpl = pl.from_pandas(df)
        return title, dfpl.with_columns(
            pl.col('value').str.replace_all(r'[^0-9]', '').str.to_integer()
        ).drop_nulls()

    def process_one_df(self, n: int):
        title, cleaned = self.tables[n].pipe(self.clean_df)
        num_res = re.findall(r'Game Number: (\d+)', title)
        just_title = title.split('Game')[0]
        game_number = None
        if num_res:
            game_number = int(num_res[0])
        final = self.process_cleaned(cleaned).with_columns(
            game_number=game_number, title=pl.lit(just_title)
        )
        cost = final.select(pl.col('value').min()).item(0, 0)
        summary = (
            final
            .select(['current_expectation_value', 'original_expectation_value'])
            .sum()
            .with_columns(game=pl.lit(just_title), cost=cost, game_number=game_number)
        )
        return summary, final

    def fix_time(self, _df: pl.DataFrame):
        return _df.with_columns(scrape_time=self.scrape_time).with_columns(
            pl.col('scrape_time').dt.cast_time_unit('ms')
        )

    @staticmethod
    def fix_dtypes(_df):
        return _df.with_columns(
            pl.col(['winners_at_start', 'winners_remaining']).cast(pl.Int32)
        )

    def run(self):
        summary_list = []
        all_data_list = []
        for n in range(len(self.tables)):
            summary, final = self.process_one_df(n)
            summary_list.append(summary)
            all_data_list.append(final)
        self.summary_df = pl.concat(summary_list).pipe(self.fix_time)
        self.detail_df = pl.concat(all_data_list).pipe(self.fix_time).pipe(self.fix_dtypes)
        self.scrape_url_dict()

    def upload_all(self):
        rows_summary = self.upload(self.summary_df, 'summary')
        rows_details = self.upload(self.detail_df, 'details')
        return rows_details, rows_summary

    def upload(self, df: pl.DataFrame, table_name: str):
        df.write_database(
            table_name=table_name, connection=self.engine, if_table_exists='append'
        )

    def write_json(self):
        with open('game_link_info.json', 'w') as f:
            json.dump(
                {'link_dict': self.link_dict, 'game_id_dict': self.game_id_dict},
                fp=f,
                indent=4,
            )


class NCScratcherData:
    def __init__(self):
        self.con = sqlite3.connect('nc_database.db')

        with open('game_link_info.json', 'r') as f:
            out = json.load(fp=f)
        self.link_dict = out['link_dict']
        self.link_dict = {int(k): val for k, val in self.link_dict.items()}

        self.game_id_dict = out['game_id_dict']
        self.game_id_dict = {int(k): val for k, val in self.game_id_dict.items()}

    def get_game_detail(self, game_id):
        df = pl.read_database(
            query='select * from details where game_number = :game_id and scrape_time =  (SELECT MAX(scrape_time) FROM details) order by value desc  limit 15 ',
            execute_options={'parameters': {'game_id': game_id}},
            connection=self.con,
        )
        return df

    def get_game_detail_trend(self, game_id):
        df = pl.read_database(
            query='select * from details where game_number = :game_id order by scrape_time',
            execute_options={'parameters': {'game_id': game_id}},
            connection=self.con,
        )
        return df

    def get_best_games(
        self, cost: int = 0, return_dataframe: bool = False
    ) -> GT | pl.DataFrame:
        if cost == 0:
            out = pl.read_database(
                query='select * from summary where scrape_time =  (SELECT MAX(scrape_time) FROM summary) order by current_expectation_value desc  limit 25 ',
                connection=self.con,
            )
        else:
            out = pl.read_database(
                query='select * from summary  where cost = :cost and scrape_time =  (SELECT MAX(scrape_time) FROM summary) order by current_expectation_value desc limit 25 ',
                execute_options={'parameters': {'cost': cost}},
                connection=self.con,
            )
        if return_dataframe:
            return out
        return (
            out.style
            .fmt_currency([
                'current_expectation_value',
                'original_expectation_value',
                'cost',
            ])
            .fmt_datetime(['scrape_time'])
            .tab_header(title='Best Games Today', subtitle=f'')
        )


if __name__ == '__main__':
    try:
        n = NCScratcherScraper()
        print_to_slack('Running NC Scratcher')
        n.run()
        rows_details, rows_summary = n.upload_all()
        n.write_json()
        print_to_slack(
            rf'Uploaded {n.detail_df.shape[0]} rows to details and {n.summary_df.shape[0]} rows to summary.'
        )
    except Exception as e:  # ruff: ignore[blind-except]
        tb = ''.join(traceback.format_exception(e))
        print_to_slack('NC Scratcher error ', error=True)
        print_to_slack(tb, error=True)
