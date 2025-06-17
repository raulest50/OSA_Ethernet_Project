"""
Alert components for the OSA Remote Control application.
"""

from dash import html
import dash_bootstrap_components as dbc

def create_alert(message, color="info", dismissable=False, icon=None, id=None, is_open=True):
    """
    Create an alert component.

    Args:
        message (str or list): Alert message
        color (str): Alert color (primary, secondary, success, danger, warning, info, light, dark)
        dismissable (bool): Whether the alert can be dismissed
        icon (str): Bootstrap icon class
        id (str): ID of the alert
        is_open (bool): Whether the alert is initially open

    Returns:
        dbc.Alert: Alert component
    """
    content = message
    if icon:
        if isinstance(message, list):
            content = [html.I(className=f"bi bi-{icon} me-2")] + message
        else:
            content = [html.I(className=f"bi bi-{icon} me-2"), message]

    # Create kwargs dictionary for Alert properties
    alert_kwargs = {
        "color": color,
        "dismissable": dismissable,
        "is_open": is_open
    }

    # Only add id if it's not None
    if id is not None:
        alert_kwargs["id"] = id

    return dbc.Alert(
        content,
        **alert_kwargs
    )

def create_info_alert(message, id=None, dismissable=False, is_open=True):
    """
    Create an info alert component.

    Args:
        message (str or list): Alert message
        id (str): ID of the alert
        dismissable (bool): Whether the alert can be dismissed
        is_open (bool): Whether the alert is initially open

    Returns:
        dbc.Alert: Info alert component
    """
    return create_alert(
        message,
        color="info",
        dismissable=dismissable,
        icon="info-circle-fill",
        id=id,
        is_open=is_open
    )

def create_success_alert(message, id=None, dismissable=False, is_open=True):
    """
    Create a success alert component.

    Args:
        message (str or list): Alert message
        id (str): ID of the alert
        dismissable (bool): Whether the alert can be dismissed
        is_open (bool): Whether the alert is initially open

    Returns:
        dbc.Alert: Success alert component
    """
    return create_alert(
        message,
        color="success",
        dismissable=dismissable,
        icon="check-circle-fill",
        id=id,
        is_open=is_open
    )

def create_warning_alert(message, id=None, dismissable=False, is_open=True):
    """
    Create a warning alert component.

    Args:
        message (str or list): Alert message
        id (str): ID of the alert
        dismissable (bool): Whether the alert can be dismissed
        is_open (bool): Whether the alert is initially open

    Returns:
        dbc.Alert: Warning alert component
    """
    return create_alert(
        message,
        color="warning",
        dismissable=dismissable,
        icon="exclamation-triangle-fill",
        id=id,
        is_open=is_open
    )

def create_error_alert(message, id=None, dismissable=False, is_open=True):
    """
    Create an error alert component.

    Args:
        message (str or list): Alert message
        id (str): ID of the alert
        dismissable (bool): Whether the alert can be dismissed
        is_open (bool): Whether the alert is initially open

    Returns:
        dbc.Alert: Error alert component
    """
    return create_alert(
        message,
        color="danger",
        dismissable=dismissable,
        icon="x-circle-fill",
        id=id,
        is_open=is_open
    )
