import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__)
import polars as pl
from nc_scratchers import NCScratcherData


def string_odds(expr):
    return (
        pl
        .when(~expr.is_infinite())
        .then(expr.map_elements(lambda x: f'1 in {int(x):,}'))
        .otherwise(pl.lit('0'))
    )


def layout(game_id=None, **other_unknown_query_strings):

    n = NCScratcherData()
    game_id = int(game_id)
    out = n.get_game_detail(game_id)
    scrape_time = out['scrape_time'].item(0)

    game_title = n.game_id_dict.get(game_id)
    game_link = n.link_dict.get(game_id)
    df = out.with_columns(
        pl.col('new_odds').pipe(string_odds),
        pl.col('odds_at_start_computed').pipe(string_odds),
    )

    return html.Div(
        [
            dcc.Link(
                'Back to Summary', href=dash.page_registry['pages.home']['relative_path']
            ),
            html.Hr(),
            dcc.Markdown(
                f"""### Details for [{game_title}](https://nclottery.com/{game_link}); ID = {game_id}"""
            ),
            dbc.Table.from_enhanced_dataframe(
                df.to_pandas()[
                    [
                        'value',
                        'winners_at_start',
                        'winners_remaining',
                        'fraction_unclaimed',
                        'expectation_score',
                        'new_odds',
                        'odds_at_start_computed',
                    ]
                ],
                striped=True,
            ),
            dcc.Markdown(f'Data last scraped on {scrape_time}'),
        ],
        style={'width': '80%', 'margin': 'auto'},
    )
