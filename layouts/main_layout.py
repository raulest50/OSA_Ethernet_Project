"""
This module contains the main layout components for the Dash application.
"""

import dash
from dash import html, dcc, page_container
import dash_bootstrap_components as dbc

# Define the sidebar
def create_sidebar():
    """
    Create the sidebar component with navigation links.
    
    Returns:
        html.Div: The sidebar component
    """
    return html.Div(
        [
            html.Div(
                [
                    html.H2("Navegación", className="display-6"),
                    html.Hr(),
                    html.P("Seleccione una página:", className="lead"),
                    dbc.Nav(
                        [
                            dbc.NavLink(
                                [
                                    html.I(className=f"bi bi-{page['icon'] if 'icon' in page else 'gear'} me-2"),
                                    page["name"],
                                ],
                                href=page["path"],
                                active="exact",
                            )
                            for page in dash.page_registry.values()
                        ],
                        vertical=True,
                        pills=True,
                    ),
                ],
                className="sidebar-content",
            ),
            html.Div(
                html.Button(
                    html.I(className="bi bi-chevron-left", id="sidebar-toggle-icon"),
                    id="sidebar-toggle",
                    className="sidebar-toggle-btn",
                ),
                className="sidebar-toggle-container",
            ),
        ],
        id="sidebar",
        className="sidebar",
    )

# Define the header with logo
def create_header():
    """
    Create the header component with title and logo.
    
    Returns:
        html.Div: The header component
    """
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.H1("OSA Remote Control", className="app-title"),
                        width={"size": 8, "order": 1},
                    ),
                    dbc.Col(
                        html.Img(
                            src="/assets/logo_final.svg",
                            height="200px",
                            className="logo"
                        ),
                        width={"size": 4, "order": 2},
                        className="d-flex justify-content-end align-items-center",
                    ),
                ],
                className="header-row",
            ),
            html.Hr(),
        ],
        className="header",
    )

# Define the main layout
def create_layout():
    """
    Create the main layout for the application.
    
    Returns:
        html.Div: The main layout
    """
    sidebar = create_sidebar()
    header = create_header()
    
    return html.Div(
        [
            # Store for sidebar state
            dcc.Store(id="sidebar-state", data={"collapsed": False}),

            # Sidebar
            sidebar,

            # Main content area
            html.Div(
                [
                    # Header
                    header,

                    # Page content
                    page_container,
                ],
                id="content",
                className="content",
            ),
        ],
        className="app-container",
    )