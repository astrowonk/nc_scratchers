import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from pathlib import Path
import dash_dataframe_table

parent_dir = Path().absolute().stem

app = Dash(
    __name__,
    use_pages=True,
    url_base_pathname=f'/dash/{parent_dir}/',
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.YETI, dbc.icons.BOOTSTRAP],
)

about = open('about_nc.md', 'r').read()

tabs = dbc.Tabs(
    [
        dbc.Tab(label='Main', id='main-tab', tab_id='main-tab', children=dash.page_container),
        dbc.Tab(
            label='About',
            id='about-tab',
            children=html.Div(dcc.Markdown(about), style={'width': '80%', 'margin': 'auto'}),
        ),
    ],
    active_tab='main-tab',
)


app.layout = html.Div(tabs)


server = app.server


if __name__ == '__main__':
    app.run(debug=True)
