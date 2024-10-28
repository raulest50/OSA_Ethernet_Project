import pandas as pd
import matplotlib.pyplot as plt

def load_dpt_file(file_path):
    data = pd.read_csv(file_path, header=None, sep=',')
    data.columns = ['Wavelength', 'Intensity']
    return data

# Load the CSV file
#data = pd.read_csv("./OSA_Data/source_lin_plate1.csv")  # Replace with your file path
data = load_dpt_file("./ref_data/PAR_26.0.dpt")

# Assuming columns are 'Wavelength' and 'Intensity'
plt.plot(data['Wavelength'], data['Intensity'])
plt.xlabel("Wavelength")
plt.ylabel("Intensity")
plt.title("Light Spectrum")
plt.show()
