"""
Button components for the OSA Remote Control application.
"""

from dash import html
import dash_bootstrap_components as dbc

def create_button(text, id=None, color="primary", outline=False, size=None, className="me-2", disabled=False, icon=None):
    """
    Create a button component.
    
    Args:
        text (str): Button text
        id (str): ID of the button
        color (str): Button color (primary, secondary, success, danger, warning, info, light, dark)
        outline (bool): Whether the button has an outline style
        size (str): Button size (sm, md, lg)
        className (str): Additional CSS classes
        disabled (bool): Whether the button is disabled
        icon (str): Bootstrap icon class
        
    Returns:
        dbc.Button: Button component
    """
    content = text
    if icon:
        content = [html.I(className=f"bi bi-{icon} me-2"), text]
    
    return dbc.Button(
        content,
        id=id,
        color=color,
        outline=outline,
        size=size,
        className=className,
        disabled=disabled
    )

def create_primary_button(text, id=None, outline=False, size=None, className="me-2", disabled=False, icon=None):
    """
    Create a primary button component.
    
    Args:
        text (str): Button text
        id (str): ID of the button
        outline (bool): Whether the button has an outline style
        size (str): Button size (sm, md, lg)
        className (str): Additional CSS classes
        disabled (bool): Whether the button is disabled
        icon (str): Bootstrap icon class
        
    Returns:
        dbc.Button: Primary button component
    """
    return create_button(
        text,
        id=id,
        color="primary",
        outline=outline,
        size=size,
        className=className,
        disabled=disabled,
        icon=icon
    )

def create_success_button(text, id=None, outline=False, size=None, className="me-2", disabled=False, icon=None):
    """
    Create a success button component.
    
    Args:
        text (str): Button text
        id (str): ID of the button
        outline (bool): Whether the button has an outline style
        size (str): Button size (sm, md, lg)
        className (str): Additional CSS classes
        disabled (bool): Whether the button is disabled
        icon (str): Bootstrap icon class
        
    Returns:
        dbc.Button: Success button component
    """
    return create_button(
        text,
        id=id,
        color="success",
        outline=outline,
        size=size,
        className=className,
        disabled=disabled,
        icon=icon
    )

def create_danger_button(text, id=None, outline=False, size=None, className="me-2", disabled=False, icon=None):
    """
    Create a danger button component.
    
    Args:
        text (str): Button text
        id (str): ID of the button
        outline (bool): Whether the button has an outline style
        size (str): Button size (sm, md, lg)
        className (str): Additional CSS classes
        disabled (bool): Whether the button is disabled
        icon (str): Bootstrap icon class
        
    Returns:
        dbc.Button: Danger button component
    """
    return create_button(
        text,
        id=id,
        color="danger",
        outline=outline,
        size=size,
        className=className,
        disabled=disabled,
        icon=icon
    )

def create_button_group(buttons, id=None, size=None, className=""):
    """
    Create a button group component.
    
    Args:
        buttons (list): List of button components
        id (str): ID of the button group
        size (str): Button size (sm, md, lg)
        className (str): Additional CSS classes
        
    Returns:
        dbc.ButtonGroup: Button group component
    """
    return dbc.ButtonGroup(
        buttons,
        id=id,
        size=size,
        className=className
    )