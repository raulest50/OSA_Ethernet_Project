import dash
from dash import html, dcc, clientside_callback, callback, Input, Output, State
import dash_bootstrap_components as dbc
import os
import datetime
import time
from utils.data_processing import load_dpt_file, process_dpt_dataframe, create_figure

# Import reusable components
from components.forms import create_input_field, create_dropdown_field, create_range_input, create_form_card
from components.buttons import create_primary_button, create_success_button, create_button
from components.graphs import create_graph_component
from components.alerts import create_info_alert

# Import callbacks (this ensures they are registered)
from callbacks.osa_callbacks import start_connection_test, perform_connection_test, acquire_osa_data, save_osa_data

# Add new callbacks for the save modal
@callback(
    Output("save-modal", "is_open"),
    Output("save-filename-input", "value"),
    Input("save-button", "n_clicks"),
    Input("cancel-save-button", "n_clicks"),
    Input("confirm-save-button", "n_clicks"),
    State("save-modal", "is_open"),
    State("acquired-data-store", "data"),
    prevent_initial_call=True
)
def toggle_save_modal(save_clicks, cancel_clicks, confirm_clicks, is_open, acquired_data):
    """
    Toggle the save modal and populate the filename input.

    Args:
        save_clicks (int): Number of times the save button has been clicked
        cancel_clicks (int): Number of times the cancel button has been clicked
        confirm_clicks (int): Number of times the confirm button has been clicked
        is_open (bool): Whether the modal is currently open
        acquired_data (dict): Dictionary containing the acquired data

    Returns:
        tuple: Modal open state and filename
    """
    ctx = dash.callback_context
    if not ctx.triggered:
        return is_open, ""

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "save-button" and save_clicks:
        # Generate filename based on acquired data
        if acquired_data:
            sensitivity = acquired_data["metadata"]["sensitivity"]
            wavelength_start = acquired_data["metadata"]["wavelength_start"]
            wavelength_end = acquired_data["metadata"]["wavelength_end"]
            timestamp = datetime.datetime.fromtimestamp(
                acquired_data["metadata"]["timestamp"]
            ).strftime("%Y%m%d_%H%M%S")

            filename = f"osa_data_{sensitivity}_{wavelength_start}-{wavelength_end}nm_{timestamp}"
            return True, filename
        return True, ""

    elif button_id in ["cancel-save-button", "confirm-save-button"]:
        return False, ""

    return is_open, ""

@callback(
    Output("save-file-path-store", "data"),
    Input("confirm-save-button", "n_clicks"),
    State("save-directory-input", "value"),
    State("save-filename-input", "value"),
    prevent_initial_call=True
)
def store_save_path(n_clicks, directory, filename):
    """
    Store the save path when the confirm button is clicked.

    Args:
        n_clicks (int): Number of times the confirm button has been clicked
        directory (str): Directory path
        filename (str): Filename

    Returns:
        dict: Save path data
    """
    if not n_clicks or not directory or not filename:
        return None

    return {
        "directory": directory,
        "filename": filename,
        "timestamp": time.time()
    }

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
                        dbc.Spinner(
                            id="connection-test-spinner",
                            color="info",
                            size="sm",
                            type="border",
                            fullscreen=False,
                            children=[],
                            spinner_style={"display": "none"}
                        ),
                        create_button("Probar conexión", id="test-connection-button", color="info", icon="ethernet")
                    ], className="d-flex align-items-center gap-2")
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
                        create_dropdown_field(
                            id="sensitivity",
                            label="Sensibilidad",
                            options=[
                                {"label": "MID", "value": "MID"},
                                {"label": "NORMAL", "value": "NORMAL"},
                                {"label": "ALTA 1", "value": "HIGH1"},
                                {"label": "ALTA 2", "value": "HIGH2"},
                                {"label": "ALTA 3", "value": "HIGH3"},
                            ],
                            value="HIGH3",
                            width=12
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
            # Graph to display acquired data with loading spinner
            dbc.Spinner(
                id="loading-acquisition",
                color="primary",
                type="border",
                fullscreen=False,
                children=[
                    create_graph_component(id="osa-graph", height="80vh")
                ]
            ),
        ], width=8),
    ]),

    # Store for holding acquired data
    dcc.Store(id="acquired-data-store"),

    # Store for connection test state
    dcc.Store(id="connection-test-store"),

    # Store for save file path
    dcc.Store(id="save-file-path-store"),

    # Modal for saving data
    dbc.Modal(
        [
            dbc.ModalHeader("Guardar datos"),
            dbc.ModalBody([
                html.P("Seleccione la ubicación donde desea guardar el archivo:"),
                dbc.Input(
                    id="save-directory-input",
                    type="text",
                    placeholder="Ruta del directorio",
                    value="data"
                ),
                html.Br(),
                html.P("Nombre del archivo:"),
                dbc.Input(
                    id="save-filename-input",
                    type="text",
                    placeholder="Nombre del archivo (sin extensión)",
                    disabled=True
                ),
                html.Small("El nombre del archivo se genera automáticamente con los parámetros de adquisición.", className="text-muted")
            ]),
            dbc.ModalFooter([
                dbc.Button("Cancelar", id="cancel-save-button", className="me-2", color="secondary"),
                dbc.Button("Guardar", id="confirm-save-button", color="success")
            ]),
        ],
        id="save-modal",
        is_open=False,
    )
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
)
