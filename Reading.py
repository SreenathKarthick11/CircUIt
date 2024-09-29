import pyvisa as visa
import csv
import numpy as np

vdata=[] # voltage
tdata=[] # time
vtdata=[vdata]
vtdata_h = ['Voltage','Time']
# Connect to the oscilloscope
rm = visa.ResourceManager()
list1 = rm.list_resources()
print(list1)
osresource=input("Enter the address of scope :")
oscilloscope = rm.open_resource(osresource)  # Adjust the address as per your instrument
oscilloscope.chunk_size = 1024*1024
oscilloscope.timeout=30000
# Specify the file path
csv_file_path = 'vtdata.csv'

# Set up the oscilloscope
oscilloscope.write(":STOP")  # Stop the oscilloscope acquisition
oscilloscope.write(":WAV:FORM ASCII")  # Set waveform format to ASCII

# Set up the oscilloscope
oscilloscope.write(":AUT")  # Reset the oscilloscope to default settings
oscilloscope.write(":TIMebase:MODE MAIN")  # Set the timebase mode to MAIN
# Query and print instantaneous voltage and current readings
oscilloscope.write(":WAV:SOUR CHAN1")
oscilloscope.write(':WAVeform:FORMat ASCII') # Query waveform data for channel 1
data = oscilloscope.query('WAV:DATA?')  # Read raw waveform data
# Process the waveform data as per your oscilloscope format (ASCII, binary, etc.)
# Example: Assuming ASCII format with comma-separated values
print(type(data))
# waveform_values = []

for num_str in data.split(','):
    try:
        num = float(num_str)
        vdata.append(num)
    except ValueError:
        print(f"Could not convert '{num_str}' to float. Skipping.")
        continue

print("Instantaneous voltage readings:", vdata)
# vdata.append(waveform_values)

oscilloscope.write('TIMEBASE:RANGE?')
horizontal_scale = float(oscilloscope.read())

# numpoints is the total number oo points 
num_points=len(vdata)
print(num_points)
tdata =np.linspace(0,horizontal_scale,num_points)
vtdata.append(tdata)
print(tdata)
print(len(tdata))
# Transpose the data to convert it into column-wise format


with open(csv_file_path, 'w', newline='') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)
    
    # Write transposed data to the CSV file
    csv_writer.writerow(vtdata_h)
    # csv_writer.writerows(vtdata_transposed)
    for i in range(len(vdata)):
        csv_writer.writerow([vdata[i],tdata[i]])

vdata=[]
tdata=[]

# Repeat the process for current readings if applicable

# Close connection to the oscilloscope
oscilloscope.close()