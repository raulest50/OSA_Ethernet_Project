"""
Card components for the OSA Remote Control application.
"""

from dash import html
import dash_bootstrap_components as dbc

def create_info_card(title, content, icon=None, color="primary", id=None):
    """
    Create an information card with a title, content, and optional icon.

    Args:
        title (str): Card title
        content (str or list): Card content
        icon (str): Bootstrap icon class
        color (str): Card color (primary, secondary, success, danger, warning, info, light, dark)
        id (str): ID of the card

    Returns:
        dbc.Card: Information card
    """
    header = title
    if icon:
        header = [html.I(className=f"bi bi-{icon} me-2"), title]

    # Only include id in kwargs if it's not None
    kwargs = {
        'color': color,
        'className': "mb-4",
        'inverse': (color not in ["light"])
    }
    if id is not None:
        kwargs['id'] = id

    return dbc.Card(
        [
            dbc.CardHeader(header),
            dbc.CardBody(content)
        ],
        **kwargs
    )

def create_status_card(title, status, description=None, id=None):
    """
    Create a status card with a title, status, and optional description.

    Args:
        title (str): Card title
        status (str): Status text
        description (str): Description text
        id (str): ID of the card

    Returns:
        dbc.Card: Status card
    """
    content = [
        html.H4(status, className="card-title"),
    ]

    if description:
        content.append(html.P(description, className="card-text"))

    # Only include id in kwargs if it's not None
    kwargs = {
        'className': "mb-4"
    }
    if id is not None:
        kwargs['id'] = id

    return dbc.Card(
        [
            dbc.CardHeader(title),
            dbc.CardBody(content)
        ],
        **kwargs
    )

def create_action_card(title, buttons, content=None, id=None):
    """
    Create a card with action buttons.

    Args:
        title (str): Card title
        buttons (list): List of button components
        content (str or list): Card content
        id (str): ID of the card

    Returns:
        dbc.Card: Action card
    """
    card_body = []

    if content:
        if isinstance(content, list):
            card_body.extend(content)
        else:
            card_body.append(html.P(content))

    card_body.append(
        html.Div(
            buttons,
            className="d-flex gap-2 mt-3"
        )
    )

    # Only include id in kwargs if it's not None
    kwargs = {
        'className': "mb-4"
    }
    if id is not None:
        kwargs['id'] = id

    return dbc.Card(
        [
            dbc.CardHeader(title),
            dbc.CardBody(card_body)
        ],
        **kwargs
    )
