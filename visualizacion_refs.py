
import pandas as pd
import matplotlib.pyplot as plt

def load_dpt_file(file_path):
    data = pd.read_csv(file_path, header=None, sep=',')
    data.columns = ['Wavelength', 'Intensity']
    return data


def process_dpt_dataframe(df):
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
    return df[['Wavelength_nm', 'Absorbance', 'Reflectance']]

data = load_dpt_file("./ref_data/PAR_05.0.dpt")
data = process_dpt_dataframe(data)

plt.plot(data['Wavelength_nm'], data['Reflectance'])
plt.xlabel("Wavelength (nm)")
plt.ylabel("Intensity")
plt.title("Espectro Reflectancia")
plt.show()


