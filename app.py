import dash
import dash_bootstrap_components as dbc
import os

# Import refactored components
from layouts.main_layout import create_layout
from layouts.index_template import index_string

# Initialize the Dash app with multi-page support
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.BOOTSTRAP,
    ],
    use_pages=True,  # Enable multi-page support
)

# Set the app layout using the refactored layout
app.layout = create_layout()

# Set the custom HTML template
app.index_string = index_string

# Import callbacks to ensure they are registered
from callbacks import update_graphs

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8050, debug=True)
