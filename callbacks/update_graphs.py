"""
This module contains callbacks for updating UI elements in the application.
"""

from dash import Input, Output, State, callback

@callback(
    Output("sidebar", "className"),
    Output("content", "className"),
    Output("sidebar-toggle-icon", "className"),
    Output("sidebar-state", "data"),
    Input("sidebar-toggle", "n_clicks"),
    State("sidebar-state", "data"),
)
def toggle_sidebar(n_clicks, sidebar_state):
    """
    Toggle the sidebar between collapsed and expanded states.
    
    Args:
        n_clicks (int): Number of times the toggle button has been clicked
        sidebar_state (dict): Current state of the sidebar
        
    Returns:
        tuple: Updated sidebar class, content class, icon class, and sidebar state
    """
    if n_clicks:
        collapsed = not sidebar_state["collapsed"]
        sidebar_class = "sidebar collapsed" if collapsed else "sidebar"
        content_class = "content expanded" if collapsed else "content"
        icon_class = "bi bi-chevron-right" if collapsed else "bi bi-chevron-left"
        return sidebar_class, content_class, icon_class, {"collapsed": collapsed}

    # Default state (not collapsed)
    return "sidebar", "content", "bi bi-chevron-left", sidebar_state