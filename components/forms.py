"""
Form components for the OSA Remote Control application.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc

def create_input_field(id, label, placeholder=None, value=None, type="text", width=12):
    """
    Create an input field with a label.

    Args:
        id (str): ID of the input field
        label (str): Label text
        placeholder (str): Placeholder text
        value: Initial value
        type (str): Input type (text, number, etc.)
        width (int): Column width (1-12)

    Returns:
        dbc.Col: Column containing the input field
    """
    return dbc.Col(
        [
            html.Label(label),
            dbc.Input(
                id=id,
                type=type,
                placeholder=placeholder,
                value=value
            )
        ],
        width=width
    )

def create_dropdown_field(id, label, options, value=None, width=12):
    """
    Create a dropdown field with a label.

    Args:
        id (str): ID of the dropdown field
        label (str): Label text
        options (list): List of options
        value: Initial value
        width (int): Column width (1-12)

    Returns:
        dbc.Col: Column containing the dropdown field
    """
    return dbc.Col(
        [
            html.Label(label),
            dcc.Dropdown(
                id=id,
                options=options,
                value=value
            )
        ],
        width=width
    )

def create_range_input(id_prefix, label, start_value=None, end_value=None, start_placeholder="Inicio", end_placeholder="Fin"):
    """
    Create a range input with two fields (start and end).

    Args:
        id_prefix (str): Prefix for the input field IDs
        label (str): Label text
        start_value: Initial value for the start field
        end_value: Initial value for the end field
        start_placeholder (str): Placeholder text for the start field
        end_placeholder (str): Placeholder text for the end field

    Returns:
        dbc.Col: Column containing the range input
    """
    return dbc.Col(
        [
            html.Label(label),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Input(
                            id=f"{id_prefix}-start",
                            type="number",
                            placeholder=start_placeholder,
                            value=start_value
                        ),
                        width=6
                    ),
                    dbc.Col(
                        dbc.Input(
                            id=f"{id_prefix}-end",
                            type="number",
                            placeholder=end_placeholder,
                            value=end_value
                        ),
                        width=6
                    )
                ]
            )
        ],
        width=12
    )

def create_form_card(title, children, id=None):
    """
    Create a card containing form elements.

    Args:
        title (str): Card title
        children (list): List of form elements
        id (str): ID of the card

    Returns:
        dbc.Card: Card containing form elements
    """
    # Only include id in kwargs if it's not None
    kwargs = {}
    if id is not None:
        kwargs['id'] = id

    return dbc.Card(
        [
            dbc.CardHeader(title),
            dbc.CardBody(children)
        ],
        **kwargs
    )
