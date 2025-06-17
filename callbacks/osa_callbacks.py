"""
This module contains callbacks for OSA connection and data acquisition.
"""

from dash import Input, Output, State, callback, no_update
from utils.osa_connection import AQ6370D
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
import time

@callback(
    Output("connection-test-store", "data"),
    Output("test-connection-button", "disabled"),
    Output("connection-test-spinner", "spinner_style"),
    Input("test-connection-button", "n_clicks"),
    State("osa-ip-address", "value"),
    State("osa-port", "value"),
    prevent_initial_call=True
)
def start_connection_test(n_clicks, ip_address, port):
    """
    Start the connection test process.

    Args:
        n_clicks (int): Number of times the button has been clicked
        ip_address (str): IP address of the OSA device
        port (int): Port number for the OSA device

    Returns:
        tuple: Connection test parameters, button disabled state, spinner style
    """
    if not n_clicks:
        return no_update, no_update, no_update

    if not ip_address:
        return None, False, {"display": "none"}

    # Store the connection test parameters
    port = int(port) if port else 10001
    test_params = {
        "ip_address": ip_address,
        "port": port,
        "timestamp": time.time()
    }

    # Show spinner and disable button during connection test
    # This will be returned immediately to the UI
    return test_params, True, {"display": "inline-block"}

@callback(
    Output("status-message", "children"),
    Output("status-message", "color"),
    Output("test-connection-button", "disabled", allow_duplicate=True),
    Output("connection-test-spinner", "spinner_style", allow_duplicate=True),
    Input("connection-test-store", "data"),
    prevent_initial_call=True
)
def perform_connection_test(test_params):
    """
    Perform the actual connection test.

    Args:
        test_params (dict): Connection test parameters

    Returns:
        tuple: Status message, color, button disabled state, spinner style
    """
    if not test_params:
        return "Por favor, ingrese una dirección IP válida.", "warning", False, {"display": "none"}

    try:
        ip_address = test_params["ip_address"]
        port = test_params["port"]

        osa = AQ6370D(ip_address, port)
        success, message = osa.test_connection()

        if success:
            return message, "success", False, {"display": "none"}
        else:
            return message, "danger", False, {"display": "none"}
    except Exception as e:
        return f"Error al probar la conexión: {str(e)}", "danger", False, {"display": "none"}

@callback(
    Output("status-message", "children", allow_duplicate=True),
    Output("status-message", "color", allow_duplicate=True),
    Output("osa-graph", "figure"),
    Output("loading-acquisition", "children"),
    Output("save-button", "disabled"),
    Output("acquired-data-store", "data"),
    Input("acquire-button", "n_clicks"),
    State("osa-ip-address", "value"),
    State("osa-port", "value"),
    State("wavelength-start", "value"),
    State("wavelength-end", "value"),
    State("resolution", "value"),
    State("sensitivity", "value"),
    State("sweep-mode", "value"),
    State("sweep-speed", "value"),
    State("averaging-times", "value"),
    State("sampling-points", "value"),
    prevent_initial_call=True
)
def acquire_osa_data(n_clicks, ip_address, port, wavelength_start, wavelength_end, resolution, sensitivity, 
                     sweep_mode, sweep_speed, averaging_times, sampling_points):
    """
    Acquire data from the OSA device.

    Args:
        n_clicks (int): Number of times the button has been clicked
        ip_address (str): IP address of the OSA device
        port (int): Port number for the OSA device
        wavelength_start (float): Start wavelength in nm
        wavelength_end (float): End wavelength in nm
        resolution (float): Resolution in nm
        sensitivity (str): Sensitivity setting
        sweep_mode (str): Sweep mode (CONTINUOUS, SINGLE, REPEAT)
        sweep_speed (str): Sweep speed (1x, 2x, 5x, 10x, 20x)
        averaging_times (int): Number of averaging times
        sampling_points (str): Number of sampling points or AUTO

    Returns:
        tuple: Status message, color, figure, loading children, save button disabled state, acquired data
    """
    if not n_clicks:
        return no_update, no_update, no_update, no_update, no_update, no_update

    if not ip_address:
        return "Por favor, ingrese una dirección IP válida.", "warning", no_update, "", True, no_update

    if not wavelength_start or not wavelength_end or not resolution:
        return "Por favor, complete todos los campos de configuración.", "warning", no_update, "", True, no_update

    try:
        # This is a simulation for now
        # In a real implementation, we would connect to the OSA and acquire data

        # Simulate data acquisition delay
        time.sleep(1)

        # Create simulated data
        wavelengths = np.linspace(wavelength_start, wavelength_end, 1000)
        # Create a simulated spectrum with a peak
        peak_position = (wavelength_start + wavelength_end) / 2
        peak_width = (wavelength_end - wavelength_start) / 20
        intensities = np.exp(-((wavelengths - peak_position) ** 2) / (2 * peak_width ** 2))

        # Create the figure
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=wavelengths,
            y=intensities,
            mode='lines',
            name='Espectro'
        ))
        fig.update_layout(
            title=f"Espectro adquirido ({sensitivity}, {resolution} nm)",
            xaxis_title="Longitud de onda (nm)",
            yaxis_title="Intensidad (u.a.)",
            template="plotly_white"
        )

        # Create a dictionary with the acquired data for storage
        acquired_data = {
            "wavelengths": wavelengths.tolist(),
            "intensities": intensities.tolist(),
            "metadata": {
                "wavelength_start": wavelength_start,
                "wavelength_end": wavelength_end,
                "resolution": resolution,
                "sensitivity": sensitivity,
                "sweep_mode": sweep_mode,
                "sweep_speed": sweep_speed,
                "averaging_times": averaging_times,
                "sampling_points": sampling_points,
                "timestamp": time.time(),
            }
        }

        return (
            "Datos adquiridos correctamente (simulación).", 
            "success", 
            fig, 
            "", 
            False,  # Enable save button
            acquired_data  # Store the acquired data
        )
    except Exception as e:
        return f"Error al adquirir datos: {str(e)}", "danger", no_update, "", True, no_update

@callback(
    Output("status-message", "children", allow_duplicate=True),
    Output("status-message", "color", allow_duplicate=True),
    Input("save-button", "n_clicks"),
    State("acquired-data-store", "data"),
    prevent_initial_call=True
)
def save_osa_data(n_clicks, acquired_data):
    """
    Save the acquired OSA data.

    Args:
        n_clicks (int): Number of times the button has been clicked
        acquired_data (dict): Dictionary containing the acquired data

    Returns:
        tuple: Status message and color
    """
    if not n_clicks:
        return no_update, no_update

    if not acquired_data:
        return "No hay datos para guardar. Por favor, adquiera datos primero.", "warning"

    try:
        # This is a simulation for now
        # In a real implementation, we would save the data to a file
        time.sleep(0.5)

        # Create a timestamp for the filename
        import datetime
        timestamp = datetime.datetime.fromtimestamp(
            acquired_data["metadata"]["timestamp"]
        ).strftime("%Y%m%d_%H%M%S")

        # Create a filename with metadata
        sensitivity = acquired_data["metadata"]["sensitivity"]
        resolution = acquired_data["metadata"]["resolution"]
        filename = f"osa_data_{sensitivity}_{resolution}nm_{timestamp}.csv"

        # In a real implementation, we would save the data to a file
        # For now, just simulate the save operation
        # import pandas as pd
        # import os
        # 
        # # Create a DataFrame with the data
        # df = pd.DataFrame({
        #     "wavelength": acquired_data["wavelengths"],
        #     "intensity": acquired_data["intensities"]
        # })
        # 
        # # Create the directory if it doesn't exist
        # os.makedirs("data", exist_ok=True)
        # 
        # # Save the DataFrame to a CSV file
        # df.to_csv(os.path.join("data", filename), index=False)

        return f"Datos guardados correctamente como '{filename}' (simulación).", "success"
    except Exception as e:
        return f"Error al guardar datos: {str(e)}", "danger"
