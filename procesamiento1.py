import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
source = pd.read_csv("./OSA_Data/source_lin_plate_smallband1_hi3.csv")  # Replace with your file path
data1 = pd.read_csv("./OSA_Data/muestra_lin_smallband1_hi3.csv")  # Replace with your file path

def load_dpt_file(file_path):
    data = pd.read_csv(file_path, header=None, sep=',')
    data.columns = ['Wavelength', 'Intensity']
    return data

def plot_data(data):
    plt.plot(data['Wavelength (nm)'], data['Intensity'])
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Intensity")
    plt.title("Light Spectrum")
    plt.show()

def plot_2data(data1, data2):
    plt.plot(data1['Wavelength (nm)'], data1['Intensity'], color='blue', label='Datos 1')
    plt.plot(data2['Wavelength (nm)'], data2['Intensity'], color='red', label='Datos 2')
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Intensity")
    plt.title("Light Spectrum")
    plt.legend()
    plt.show()


def normalize_signal_db(data):
    normalized_data = data.copy()
    max_intensity = normalized_data['Intensity'].max()
    #normalized_data['Intensity'] = normalized_data['Intensity']*-1
    normalized_data['Intensity'] = normalized_data['Intensity'] / max_intensity
    normalized_data['Intensity'] = 1-normalized_data['Intensity']
    return normalized_data

def normalize_signal_lin(data):
    normalized_data = data.copy()
    max_intensity = normalized_data['Intensity'].max()
    normalized_data['Intensity'] = normalized_data['Intensity'] / max_intensity
    return normalized_data

sn = normalize_signal_lin(source)
dn = normalize_signal_lin(data1)

#plot_2data(sn, dn)

absorption = source.copy()
absorption['Intensity'] = sn['Intensity'] / dn['Intensity']

#absorption_nn = source.copy()
#absorption_nn['Intensity'] = source['Intensity'] / data1['Intensity']

plot_2data(sn, absorption)

