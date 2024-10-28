
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    dbc.icons.BOOTSTRAP,
])

app.layout = html.Div([
    html.Div([
        dbc.Row([
            dbc.Col([

            ])
        ])
    ])
])

app.run(host="0.0.0.0", port=8050, debug=True)
