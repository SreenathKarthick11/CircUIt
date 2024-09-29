import pyvisa as visa
import csv
import numpy as np
import matplotlib.pyplot as plt

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
fgresource=input("Enter address of Function Generator :")
inst_sig = rm.open_resource(fgresource)  # Open the instrument

def Reading():
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
    # print(type(data))
    # waveform_values = []

    for num_str in data.split(','):
        try:
            num = float(num_str)
            vdata.append(num)
        except ValueError:
            print(f"Could not convert '{num_str}' to float. Skipping.")
            continue


    oscilloscope.write('TIMEBASE:RANGE?')
    horizontal_scale = float(oscilloscope.read())

    # numpoints is the total number oo points 
    num_points=len(vdata)

    tdata =np.linspace(0,horizontal_scale,num_points)
    vtdata.append(tdata)

    # Transpose the data to convert it into column-wise format


    with open(csv_file_path, 'w', newline='') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)
        
        # Write transposed data to the CSV file
        csv_writer.writerow(vtdata_h)
        # csv_writer.writerows(vtdata_transposed)
        for i in range(len(vdata)):
            csv_writer.writerow([vdata[i],tdata[i]])

# Repeat the process for current readings if applicable

def ac_analysis():
    Vin=int(input("Enter the Input Voltage :"))
    # Set up the oscilloscope
    oscilloscope.write(":STOP")  # Stop the oscilloscope acquisition
    oscilloscope.write(":WAV:FORM ASCII")  # Set waveform format to ASCII

    # Set up the oscilloscope
    oscilloscope.write(":AUT")  # Reset the oscilloscope to default settings
    oscilloscope.write(":TIMebase:MODE MAIN")  # Set the timebase mode to MAIN
    # Query and print instantaneous voltage and current readings
    # Configure the oscilloscope for AC analysis
    oscilloscope.write("ACQUIRE:TYPE AVERAGE")   # Set acquisition type to average
    oscilloscope.write("CHAN1:COUPLING AC")      # Set channel 1 coupling to AC
    oscilloscope.write("CHAN1:SCALE 1")          # Set channel 1 voltage scale to 1 V/div
    oscilloscope.write("TRIG:SOURCE IMM")        # Set trigger source to immediate
    oscilloscope.write("TRIG:LEVEL 0.5")         # Set trigger level to 0.5 V
    oscilloscope.write(":WAV:SOUR CHAN1")
    oscilloscope.write(':WAVeform:FORMat ASCII') # Query waveform data for channel 1
    data = oscilloscope.query('WAV:DATA?')  # Read raw waveform data
    # Process the waveform data as per your oscilloscope format (ASCII, binary, etc.)
    # Example: Assuming ASCII format with comma-separated values
    print(type(data))
    # waveform_values = []

    for num_str in data.split(','):
        try:
            num = float(num_str)/Vin
            vdata.append(num)
        except ValueError:
            print(f"Could not convert '{num_str}' to float. Skipping.")
            continue

    
    # vdata.append(waveform_values)
    # Set up frequency sweep parameters
    ac_start_freq = int(input("Enter the Start Frequency in Hz :"))  # Start frequency (Hz)
    ac_stop_freq = int(input("Enter the Stop Frequency in Hz :"))  # Stop frequency (Hz)
    num_points = len(vdata)  # Number of points in the sweep # should be equal to vdata

    # Perform frequency sweep and capture Bode plot data
    frequency = np.logspace(np.log10(ac_start_freq), np.log10(ac_stop_freq), num_points)

    phase = []
    # for freq in frequency:
    #     oscilloscope.write(f"FUNC:FREQ {freq}")  # Set function generator frequency
    #     # Acquire waveform and process data to extract magnitude and phase
    #     # This step depends on your oscilloscope's specific commands and capabilities
    #     # You may need to use SCPI commands to fetch waveform data and analyze it
    #     # Alternatively, some oscilloscopes have built-in functions for Bode plot measurements
    #     # Consult your oscilloscope's programming manual for details

    # Display the Bode plot
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.semilogx(frequency, vdata)
    # plt.plot(frequency, vdata)
    plt.xlabel('frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.title('Bode Plot - Magnitude')

    # plt.subplot(2, 1, 2)
    # plt.semilogx(frequency, phase)
    # plt.xlabel('frequency (Hz)')
    # plt.ylabel('Phase (degrees)')
    # plt.title('Bode Plot - Phase')

    plt.tight_layout()
    plt.show()

def dc_analysis():
        # Configure the oscilloscope for AC analysis
    oscilloscope.write("ACQUIRE:TYPE AVERAGE")   # Set acquisition type to average
    oscilloscope.write("CHAN1:COUPLING DC")      # Set channel 1 coupling to DC
    oscilloscope.write("CHAN1:SCALE 1")          # Set channel 1 voltage scale to 1 V/div
    oscilloscope.write("TRIG:SOURCE IMM")        # Set trigger source to immediate
    oscilloscope.write("TRIG:LEVEL 0.5")         # Set trigger level to 0.5 V

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


    # Set up voltage sweep parameters
    start_sweep_volt = int(input("Enter start voltage :"))  # Start voltage   # plot against voltage
    stop_sweep_volt = int(input("Enter Stop voltage :"))   # Stop Voltage
    num_points = len(vdata) # Number of points in the sweep should be equal to len(vdata)

    # Perform voltage sweep and capture Bode plot data
    sweep_voltage = np.logspace(np.log10(start_sweep_volt), np.log10(stop_sweep_volt), num_points)
    # print(sweep_voltage)
    
    plt.plot(sweep_voltage, vdata)
    plt.xlabel('sweep voltage (V)')
    plt.ylabel(' Voltage ')
    plt.title(' DC Analysis ')


    plt.tight_layout()
    plt.show()

def ploting():

    csv_file_path = 'vtdata.csv'
    data = []
    with open(csv_file_path,'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            data.append(row)

    # Assuming the first row contains the column headers and the rest are data
    headers = data[0]
    data = data[1:]

    # Extract data columns
    x_values = [float(row[0]) for row in data]  # Assuming the first column is x-values
    y_values = [float(row[1]) for row in data]  # Assuming the second column is y-values

    # Plot the graph
    plt.plot(y_values, x_values)
    plt.xlabel("Time")  # Set x-axis label
    plt.ylabel("Voltage")  # Set y-axis label
    plt.title("Voltage vs Time")  # Set plot title
    plt.grid(True)  # Show grid
    plt.show()
# Close connection to the oscilloscope

# Calling Functions:
    
# Reading()
ploting()
# ac_analysis()
# dc_analysis()

oscilloscope.close()