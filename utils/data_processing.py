"""
Data processing utilities for the OSA Remote Control application.
"""

import pandas as pd
import plotly.express as px

def load_dpt_file(file_path):
    """
    Load data from a DPT file.
    
    Args:
        file_path (str): Path to the DPT file
        
    Returns:
        pandas.DataFrame: DataFrame with Wavelength and Intensity columns
    """
    data = pd.read_csv(file_path, header=None, sep=',')
    data.columns = ['Wavelength', 'Intensity']
    return data


def process_dpt_dataframe(df):
    """
    Process a DataFrame containing DPT data.
    
    Args:
        df (pandas.DataFrame): DataFrame with Wavelength and Intensity columns
        
    Returns:
        pandas.DataFrame: Processed DataFrame with Wavelength_nm, Reflectance, and Absorbance columns
    """
    # Step 1: Convert Wavelength from cm^-1 to nanometers
    df['Wavelength_nm'] = 1e7 / df['Wavelength']

    # Step 2: Take only data up to 2500 nanometers
    df = df[df['Wavelength_nm'] <= 2500].copy()

    # Step 3: Normalize Intensity with respect to its maximum value
    max_intensity = df['Intensity'].max()
    df['Absorbance'] = df['Intensity'] / max_intensity

    # Step 4: Compute Reflectance as 1 - Normalized_Intensity
    df['Reflectance'] = 1 - df['Absorbance']

    # Return the processed DataFrame with the new columns
    return df[['Wavelength_nm', 'Reflectance', 'Absorbance']]


def create_figure(df):
    """
    Create a Plotly figure from a DataFrame.
    
    Args:
        df (pandas.DataFrame): DataFrame with data to plot
        
    Returns:
        plotly.graph_objects.Figure: Plotly figure
    """
    # Create the Plotly figure
    fig = px.line(
        df,
        x=df.columns[0],
        y=df.columns[1],
        title="Reference Spectrum",
    )

    fig.update_layout(
        xaxis_title="Wavelength",
        yaxis_title="Reflectance"
    )
    # Return the figure to be displayed in the graph
    return fig