"""
Graph components for the OSA Remote Control application.
"""

import plotly.express as px
from dash import dcc, html
import dash_bootstrap_components as dbc

def create_graph_component(id="graph", figure=None, height="80vh", title=None):
    """
    Create a graph component with optional title.

    Args:
        id (str): ID of the graph component
        figure (plotly.graph_objects.Figure): Figure to display
        height (str): Height of the graph
        title (str): Title to display above the graph

    Returns:
        html.Div: Graph component
    """
    components = []

    if title:
        components.append(html.H4(title, className="graph-title"))

    # Create an empty figure if none is provided
    if figure is None:
        figure = {
            'data': [],
            'layout': {
                'title': 'No data available',
                'xaxis': {'title': 'X'},
                'yaxis': {'title': 'Y'}
            }
        }

    components.append(
        dcc.Graph(
            id=id,
            figure=figure,
            style={"height": height}
        )
    )

    return html.Div(
        components,
        className="graph-container"
    )

def create_graph_card(id="graph-card", graph_id="graph", figure=None, height="80vh", title=None):
    """
    Create a card containing a graph component.

    Args:
        id (str): ID of the card
        graph_id (str): ID of the graph component
        figure (plotly.graph_objects.Figure): Figure to display
        height (str): Height of the graph
        title (str): Title to display in the card header

    Returns:
        dbc.Card: Card containing a graph component
    """
    # Only include id in kwargs if it's not None
    kwargs = {
        'className': "graph-card"
    }
    if id is not None:
        kwargs['id'] = id

    card_components = []
    if title:
        card_components.append(dbc.CardHeader(title))
    card_components.append(
        dbc.CardBody(
            create_graph_component(
                id=graph_id,
                figure=figure,
                height=height
            )
        )
    )

    return dbc.Card(
        card_components,
        **kwargs
    )
