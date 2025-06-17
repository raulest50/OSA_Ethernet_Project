"""
This module contains the HTML template for the Dash application.
"""

# HTML template for the Dash application
index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>OSA Remote Control</title>
        {%favicon%}
        {%css%}
        <style>
            /* App container */
            .app-container {
                display: flex;
                flex-direction: row; /* Ensure horizontal layout */
                width: 100%;
                height: 100vh;
                overflow: hidden;
            }

            /* Sidebar styles */
            .sidebar {
                width: 280px;
                height: 100vh;
                background-color: #f8f9fa;
                transition: width 0.3s ease;
                overflow-y: auto;
                position: fixed; /* Fixed position */
                left: 0; /* Ensure it's on the left */
                top: 0; /* Start from the top */
                bottom: 0; /* Extend to the bottom */
                box-shadow: 2px 0 5px rgba(0,0,0,0.1);
                z-index: 1000;
            }

            .sidebar.collapsed {
                width: 50px;
                overflow: hidden;
            }

            .sidebar-content {
                padding: 20px;
                width: 280px;
            }

            .sidebar.collapsed .sidebar-content {
                opacity: 0;
                pointer-events: none;
            }

            .sidebar-toggle-container {
                position: absolute;
                bottom: 20px;
                right: 10px;
            }

            .sidebar-toggle-btn {
                background: none;
                border: none;
                color: #007bff;
                font-size: 1.2rem;
                cursor: pointer;
            }

            /* Content area */
            .content {
                flex: 1;
                padding: 20px;
                transition: margin-left 0.3s ease;
                overflow-y: auto;
                height: 100vh;
                margin-left: 280px; /* Match sidebar width */
            }

            .content.expanded {
                margin-left: 50px;
            }

            /* Header styles */
            .header {
                margin-bottom: 20px;
            }

            .header-row {
                align-items: center;
            }

            .app-title {
                margin: 0;
                color: #343a40;
            }

            .logo {
                max-height: 200px; /* Updated from 60px to 200px */
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''