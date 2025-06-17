import dash
import dash_bootstrap_components as dbc

# Import reusable components
from components.cards import create_info_card

# Register the page as the home page
dash.register_page(__name__, path='/', name='Inicio', order=0, icon='house')

# Layout for the home page
layout = dash.html.Div([
    dbc.Row([
        dbc.Col([
            dash.html.H2("Bienvenido a OSA Remote Control", className="display-4"),
            dash.html.Hr(),
            dash.html.P(
                "Esta aplicación permite controlar y analizar datos del Analizador de Espectro Óptico (OSA).",
                className="lead",
            ),
            dash.html.Div([
                dash.html.P("Utilice el panel de navegación a la izquierda para acceder a las diferentes funcionalidades:"),
                dash.html.Ul([
                    dash.html.Li([
                        dash.html.Strong("Adquisición de datos: "),
                        "Configure y controle el OSA para adquirir nuevos datos de espectro óptico."
                    ]),
                    dash.html.Li([
                        dash.html.Strong("Pre Procesamiento y visualización: "),
                        "Visualice y procese los datos adquiridos previamente."
                    ]),
                ]),
            ]),
            dash.html.Br(),
            create_info_card(
                title="Instrucciones de uso",
                content=[
                    dash.html.P("Para comenzar:"),
                    dash.html.Ol([
                        dash.html.Li("Seleccione una opción del menú de navegación"),
                        dash.html.Li("Configure los parámetros según sea necesario"),
                        dash.html.Li("Visualice y analice los resultados"),
                    ]),
                    dash.html.P("Puede ocultar el panel de navegación haciendo clic en el botón en la parte inferior del panel."),
                ],
                icon="info-circle",
                color="light"
            ),
        ], width={"size": 10, "offset": 1}),
    ]),
])
