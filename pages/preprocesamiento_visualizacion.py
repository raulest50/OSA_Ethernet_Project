import dash
from dash import html, dcc, callback, Input, Output, State, clientside_callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import json

# Import reusable components
from components.alerts import create_info_alert, create_error_alert
from components.buttons import create_primary_button, create_success_button, create_button
from components.forms import create_form_card
from components.graphs import create_graph_component

# Register the page
dash.register_page(__name__, path='/preprocesamiento-visualizacion', name='Pre Procesamiento y visualización', order=2, icon='graph-up')

# Layout for the preprocessing and visualization page
layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H2("Pre Procesamiento y visualización"),
            html.Hr(),
            html.P("Esta página permite cargar, visualizar y normalizar datos de espectros guardados en formato CSV."),

            # Card for file loading and options
            create_form_card(
                title="Cargar y Procesar Datos",
                children=[
                    dbc.Row([
                        dbc.Col([
                            # File selection button
                            create_primary_button(
                                "Cargar CSV", 
                                id="load-csv-button", 
                                icon="file-earmark-text",
                                className="w-100 mb-3"
                            ),

                            # Display selected file name
                            html.Div(id="selected-file-info", className="mb-3"),

                            # Normalization option
                            dbc.Checkbox(
                                id="normalize-data-checkbox",
                                label="Normalizar datos",
                                value=False,
                                className="mb-3"
                            ),

                            # Status message
                            html.Div(id="csv-load-status")
                        ])
                    ])
                ]
            ),

            # Hidden div for file picker setup
            html.Div(id="file-picker-setup", style={"display": "none"}),

        ], width=4),

        dbc.Col([
            # Graph to display loaded data
            dbc.Spinner(
                id="loading-csv-data",
                color="primary",
                type="border",
                fullscreen=False,
                children=[
                    create_graph_component(id="csv-graph", height="80vh")
                ]
            ),
        ], width=8),
    ]),

    # Store for holding loaded CSV data
    dcc.Store(id="csv-data-store"),
])

# Initialize file picker setup when the page loads
clientside_callback(
    """
    function() {
        // Create hidden file input if it doesn't exist
        if (!document.getElementById('hidden-file-input')) {
            const input = document.createElement('input');
            input.type = 'file';
            input.id = 'hidden-file-input';
            input.accept = '.csv';
            input.style.display = 'none';
            document.body.appendChild(input);
        }
        return true;
    }
    """,
    Output("file-picker-setup", "children"),
    Input("file-picker-setup", "id"),
    prevent_initial_call=False
)

# Add client-side callback for file selection
clientside_callback(
    """
    window.dash_clientside.file_selector.openFilePicker
    """,
    Output("csv-data-store", "data"),
    Input("load-csv-button", "n_clicks"),
    prevent_initial_call=True
)

# Callback to update the file info display
@callback(
    Output("selected-file-info", "children"),
    Input("csv-data-store", "data")
)
def update_file_info(data):
    if not data:
        return "No se ha seleccionado ningún archivo"

    return [
        html.Strong("Archivo seleccionado: "),
        html.Span(data.get("name", "Desconocido"))
    ]

# Callback to process and display the CSV data
@callback(
    Output("csv-graph", "figure"),
    Output("csv-load-status", "children"),
    Input("csv-data-store", "data"),
    Input("normalize-data-checkbox", "value")
)
def update_graph(data, normalize):
    if not data or not data.get("content"):
        # Return empty figure if no data
        fig = go.Figure()
        fig.update_layout(
            title="No hay datos para mostrar",
            xaxis_title="Longitud de onda (nm)",
            yaxis_title="Intensidad (u.a.)",
            template="plotly_white"
        )
        return fig, ""

    try:
        # Load CSV data
        from utils.data_processing import load_csv_file, normalize_data

        # Parse CSV content
        df = load_csv_file(data["content"])

        # Apply normalization if requested
        if normalize:
            df = normalize_data(df)
            title_suffix = " (Normalizado)"
        else:
            title_suffix = ""

        # Create figure
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['wavelength'],
            y=df['intensity'],
            mode='lines',
            name='Espectro',
            line=dict(color='blue', width=2)
        ))

        # Update layout
        fig.update_layout(
            title=f"Espectro cargado desde {data['name']}{title_suffix}",
            xaxis_title="Longitud de onda (nm)",
            yaxis_title="Intensidad (u.a.)",
            template="plotly_white",
            margin=dict(l=50, r=50, t=80, b=50),
            height=600,
            hovermode="closest",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        # Add grid lines
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

        return fig, create_info_alert("Datos cargados correctamente")

    except Exception as e:
        # Create error figure
        error_fig = go.Figure()
        error_fig.add_annotation(
            text=f"Error al procesar datos: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14, color="red")
        )
        error_fig.update_layout(
            xaxis_title="Longitud de onda (nm)",
            yaxis_title="Intensidad (u.a.)",
            template="plotly_white"
        )

        return error_fig, create_error_alert(f"Error al procesar datos: {str(e)}")
