import dash
from dash import html, dcc, clientside_callback, callback, Input, Output, State
import dash_bootstrap_components as dbc
import os
from utils.data_processing import load_dpt_file, process_dpt_dataframe, create_figure

# Import reusable components
from components.forms import create_input_field, create_dropdown_field, create_range_input, create_form_card
from components.buttons import create_primary_button, create_success_button, create_button
from components.graphs import create_graph_component
from components.alerts import create_info_alert

# Import callbacks (this ensures they are registered)
from callbacks.osa_callbacks import test_osa_connection, acquire_osa_data, save_osa_data

# Register the page
dash.register_page(__name__, path='/adquisicion-datos', name='Adquisición de datos', order=1, icon='cloud-download')

# Layout for the data acquisition page
layout = dash.html.Div([
    dbc.Row([
        dbc.Col([
            dash.html.H2("Adquisición de datos"),
            dash.html.Hr(),
            dash.html.P("Esta página permite la adquisición de datos del OSA."),

            # Add connection settings for OSA
            create_form_card(
                title="Conexión al OSA",
                children=[
                    dbc.Row([
                        create_input_field(
                            id="osa-ip-address",
                            label="Dirección IP del OSA",
                            placeholder="Ej. 192.168.1.100",
                            value="168.176.118.22",  # Valor predeterminado
                            type="text",
                            width=8
                        ),
                        create_input_field(
                            id="osa-port",
                            label="Puerto",
                            placeholder="Puerto",
                            value=10001,
                            type="number",
                            width=4
                        )
                    ]),
                    dash.html.Br(),
                    dash.html.Div([
                        create_button("Probar conexión", id="test-connection-button", color="info", icon="ethernet")
                    ])
                ],
                id="connection-settings-card"
            ),

            dash.html.Br(),

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

                    # Toggle button for advanced options
                    dash.html.Div([
                        dash.html.Button(
                            [
                                dash.html.I(className="bi bi-gear me-2"),
                                "Opciones avanzadas"
                            ],
                            id="toggle-advanced-options",
                            className="btn btn-outline-secondary btn-sm mt-3 mb-3"
                        )
                    ]),

                    # Advanced options section (initially hidden)
                    dash.html.Div([
                        dbc.Row([
                            create_dropdown_field(
                                id="sweep-mode",
                                label="Modo de barrido",
                                options=[
                                    {"label": "Continuo", "value": "CONTINUOUS"},
                                    {"label": "Único", "value": "SINGLE"},
                                    {"label": "Repetir", "value": "REPEAT"},
                                ],
                                value="SINGLE",
                                width=6
                            ),
                            create_dropdown_field(
                                id="sweep-speed",
                                label="Velocidad de barrido",
                                options=[
                                    {"label": "1x", "value": "1x"},
                                    {"label": "2x", "value": "2x"},
                                    {"label": "5x", "value": "5x"},
                                    {"label": "10x", "value": "10x"},
                                    {"label": "20x", "value": "20x"},
                                ],
                                value="2x",
                                width=6
                            )
                        ]),
                        dash.html.Br(),
                        dbc.Row([
                            create_input_field(
                                id="averaging-times",
                                label="Número de promedios",
                                placeholder="Promedios",
                                value=1,
                                type="number",
                                width=6
                            ),
                            create_dropdown_field(
                                id="sampling-points",
                                label="Puntos de muestreo",
                                options=[
                                    {"label": "Auto", "value": "AUTO"},
                                    {"label": "501", "value": "501"},
                                    {"label": "1001", "value": "1001"},
                                    {"label": "2001", "value": "2001"},
                                    {"label": "5001", "value": "5001"},
                                ],
                                value="AUTO",
                                width=6
                            )
                        ])
                    ], id="advanced-options-content", style={"display": "none"}),

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
            # Loading component for data acquisition
            dbc.Spinner(
                id="loading-acquisition",
                color="primary",
                type="border",
                fullscreen=False,
                children=[]
            ),

            # Graph to display acquired data
            create_graph_component(id="osa-graph", height="80vh")
        ], width=8),
    ]),

    # Store for holding acquired data
    dcc.Store(id="acquired-data-store")
])

# Register client-side callbacks after layout is defined
clientside_callback(
    """
    window.dash_clientside.clientside.update_acquire_button_state
    """,
    Output("acquire-button", "disabled"),
    Input("osa-ip-address", "value"),
    Input("wavelength-start", "value"),
    Input("wavelength-end", "value"),
    Input("resolution", "value"),
)

clientside_callback(
    """
    window.dash_clientside.clientside.toggle_form_section
    """,
    Output("advanced-options-content", "style"),
    Input("toggle-advanced-options", "n_clicks"),
    State("advanced-options-content", "style"),
)
