import datetime
import sqlite3
from pathlib import Path

import dash_bootstrap_components as dbc
import plotly.express as px
import polars as pl
import dash
from dash import Input, Output, State, callback, callback_context, ALL, MATCH, html, dcc
from dash.exceptions import PreventUpdate
from nc_scratchers import NCScratcherData

import dash_dataframe_table

parent_dir = Path().absolute().stem

dash.register_page(__name__, path='/')


menu_div = html.Div([
    html.H1('NC Scratcher Explorer', style={'text-align': 'center'}),
    dbc.InputGroup([
        dbc.InputGroupText('Cost of Ticket ($0 for all)'),
        dbc.Select(
            id='cost-menu',
            options=[{'label': f'${n}', 'value': n} for n in [0, 1, 2, 3, 5, 10, 20, 30, 50]],
            value=10,
            persistence=True,
            persistence_type='local',
        ),
    ]),
])

main_content = html.Div(
    [
        menu_div,
        html.H3('Best Expectation Value Tickets'),
        html.Div(id='summary-div'),
    ],
    style={'width': '80%', 'margin': 'auto'},
)


layout = dbc.Container(
    [dbc.Row(dbc.Col(main_content))],
)


@callback(
    #  Output('pattern-div', 'children', allow_duplicate=True),
    Output('summary-div', 'children'),
    Input('cost-menu', 'value'),
    suppress_callback_exceptions=True,
    # prevent_initial_call='initial_duplicate',
)
def summary(value):
    n = NCScratcherData()
    print(value, type(value))
    out = n.get_best_games(cost=int(value), return_dataframe=True)
    print(out.shape)
    out = out.with_columns(
        game_HREF=pl.col('game_number').map_elements(
            lambda x: f'detail-page?game_id={x}', return_dtype=pl.String
        )
    )
    scrape_time = out['scrape_time'].item(0)
    return html.Div([
        dbc.Table.from_enhanced_dataframe(
            out
            .with_columns(pl.col('game_number').cast(pl.String))
            .drop(['scrape_time'])
            .to_pandas(),
            striped=True,
            # style={'width': '80%'},
        ),
        dcc.Markdown(f'Data last scraped on {scrape_time}'),
    ])
