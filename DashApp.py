import dash
from dash import dcc, html, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import os
from metodos import *

app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    dbc.icons.BOOTSTRAP,
])

filenames_refs = [f for f in os.listdir("./ref_data") if f.endswith('.dpt')]

filenames_meas = [f for f in os.listdir("./OSA_data") if f.endswith('.csv')]

app.layout = html.Div([
    html.Div([

        dbc.Row([
            dbc.Col([
                html.H1("Espectroscopia Por Reflexion difusa")
            ], width=12, className='text-center', style={'textAlign': 'center'}),
        ], justify='center', align='center', style={'padding': '2em'}),

        dbc.Row([

            dbc.Col([
                html.Label("Ref Filename"),
                dcc.Dropdown(
                    id='ref_dropdown',
                    options=[{'label': f, 'value': f} for f in filenames_refs],
                    value=filenames_refs[0] if filenames_refs else None,
                    clearable=False,
                )
            ], width=3, style={'display': 'block'}),
            dbc.Col([
                dcc.Graph(id='reflectancia_refs')  # Placeholder for the plot
            ], width=6),

            dbc.Col([
                html.Spacer()
            ], width=3),
        ]),

        dbc.Row([
            dbc.Col([
                html.Label("Measures"),
                dcc.Dropdown(
                    id='meas_dropdown',
                    options=[{'label': f, 'value': f} for f in filenames_meas],
                    value=filenames_meas[0] if filenames_meas else None,
                    clearable=False,
                )
            ], width=3, style={'display': 'block'}),

            dbc.Col([
                dcc.Graph(id='g1')  # Placeholder for the plot
            ], width=6),


        ])




    ])
])

@callback(
    Output('reflectancia_refs', 'figure'),
    Output('g1', 'figure'),
    Input('ref_dropdown', 'value'),
    Input('meas_dropdown', 'value'),
)
def update_graph(ref_fname, meas_fname):
    df = load_dpt_file(f"./ref_data/{ref_fname}")
    df = process_dpt_dataframe(df)
    fig1 = create_figure(df)

    dfm = load_dpt_file(f"./OSA_data/{meas_fname}")
    fig2 = create_figure(dfm)

    return fig1, fig2  # Retornamos directamente el objeto fig

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8050, debug=True)
