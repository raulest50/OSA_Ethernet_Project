import dash
from dash import callback, Input, Output
import dash_bootstrap_components as dbc
import os
from utils.data_processing import load_dpt_file, process_dpt_dataframe, create_figure

# Import reusable components
from components.forms import create_input_field, create_dropdown_field, create_range_input, create_form_card
from components.buttons import create_primary_button, create_success_button
from components.graphs import create_graph_component
from components.alerts import create_info_alert

# Register the page
dash.register_page(__name__, path='/adquisicion-datos', name='Adquisición de datos', order=1, icon='cloud-download')

# Layout for the data acquisition page
layout = dash.html.Div([
    dbc.Row([
        dbc.Col([
            dash.html.H2("Adquisición de datos"),
            dash.html.Hr(),
            dash.html.P("Esta página permite la adquisición de datos del OSA."),

            # Add controls for OSA data acquisition
            create_form_card(
                title="Configuración del OSA",
                children=[
                    dbc.Row([
                        create_range_input(
                            id_prefix="wavelength",
                            label="Rango de longitud de onda (nm)",
                            start_value=1500,
                            end_value=1600
                        )
                    ]),
                    dash.html.Br(),
                    dbc.Row([
                        create_input_field(
                            id="resolution",
                            label="Resolución (nm)",
                            placeholder="Resolución",
                            value=0.1,
                            type="number",
                            width=6
                        ),
                        create_dropdown_field(
                            id="sensitivity",
                            label="Sensibilidad",
                            options=[
                                {"label": "ALTA 1", "value": "HIGH1"},
                                {"label": "ALTA 2", "value": "HIGH2"},
                                {"label": "ALTA 3", "value": "HIGH3"},
                                {"label": "NORMAL", "value": "NORMAL"},
                            ],
                            value="NORMAL",
                            width=6
                        )
                    ]),
                    dash.html.Br(),
                    dash.html.Div([
                        create_primary_button("Adquirir datos", id="acquire-button", icon="cloud-download"),
                        create_success_button("Guardar datos", id="save-button", disabled=True, icon="save")
                    ])
                ]
            ),

            dash.html.Br(),

            # Status and messages
            create_info_alert(
                "Esperando acción...",
                id="status-message"
            )
        ], width=4),

        dbc.Col([
            # Graph to display acquired data
            create_graph_component(id="osa-graph", height="80vh")
        ], width=8),
    ]),
])

# Callbacks will be added later for actual functionality
@callback(
    Output("status-message", "children"),
    Output("status-message", "color"),
    Input("acquire-button", "n_clicks"),
    prevent_initial_call=True
)
def update_status(n_clicks):
    if n_clicks:
        return "Esta es una simulación. En una implementación real, aquí se conectaría con el OSA.", "warning"
    return "Esperando acción...", "info"
