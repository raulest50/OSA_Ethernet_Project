import dash
import dash_bootstrap_components as dbc

# Import reusable components
from components.alerts import create_info_alert

# Register the page
dash.register_page(__name__, path='/preprocesamiento-visualizacion', name='Pre Procesamiento y visualización', order=2, icon='graph-up')

# Layout for the preprocessing and visualization page - empty as requested
layout = dash.html.Div([
    dbc.Row([
        dbc.Col([
            dash.html.H2("Pre Procesamiento y visualización"),
            dash.html.Hr(),
            dash.html.P("Esta página está actualmente vacía."),

            # Empty content message
            create_info_alert(
                "Esta sección está en desarrollo."
            )
        ], width={"size": 10, "offset": 1}),
    ]),
])
