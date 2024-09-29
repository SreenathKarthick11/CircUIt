import pyvisa as visa
import time

# Define lists for various parameters
functionlist = ['FUNC:SHAP SIN', 'FUNC:SHAP SQU', 'FUNC:SHAP TRI', 'FUNC:SHAP RAMP', 'FUNC:SHAP PULS']
frequencyModelist = ['FIX ', 'SWE ']
voltUnitlist = [' VPK', ' VPP', ' VRMS', ' VAMPL', ' mVPK', ' mVPP', ' mVRMS', ' mVAMPL']
offsetvoltUnitlist = ['mV', 'V']
frequencyUnitlist = ["Hz", "kHz"]

# Function to set the signal source (SOUR1 or SOUR2)
def set_source(source):
    global S
    if source == 1:
        S = 'SOUR1:'
    elif source == 2:
        S = 'SOUR2:'

# Function to set the frequency
def set_frequency(inst_sig, frequency, frequencymode, frequencyunit):
    inst_sig.write(S + "FREQ:" + frequencyModelist[frequencymode - 1] + str(frequency) + frequencyUnitlist[frequencyunit - 1])

# Function to set the waveform
def set_waveform(inst_sig, waveform):
    inst_sig.write(S + functionlist[waveform - 1])

# Function to set the voltage and offset voltage
def set_voltage(inst_sig, voltage, offsetvoltage, offsetvoltunit, vunit):
    inst_sig.write(S + "VOLT:LEV:IMM:AMPL " + str(voltage) + voltUnitlist[vunit - 1])
    inst_sig.write(S + "VOLT:LEV:IMM:OFFset " + str(offsetvoltage) + offsetvoltUnitlist[offsetvoltunit - 1])

# Initialize PyVISA resource manager
rm = visa.ResourceManager()

list1 = rm.list_resources()
print(list1)
resource=input("Enter address of Function Generator :")
print(resource)  
inst_sig = rm.open_resource(resource)  # Open the instrument
if inst_sig == rm.open_resource(resource):
    print("Hello")
# Signal Generator setup
inst_sig.timeout = 10000
string = inst_sig.query("*IDN?")
inst_sig.write('*RST')

# Take user inputs
source = int(input("Enter Source 1 or 2: "))
frequency = float(input("Enter frequency in Hz: "))
frequencymode = int(input("Enter Frequency Mode FIXED=1 or SWEEP=2: "))
frequencyunit = int(input("Enter 1=Hz 2=KHz: "))
waveform = int(input("Enter waveform (1=SIN, 2=SQUARE, 3=TRIANGLE, 4=RAMP, 5=PULSE): "))
voltage = float(input("Enter voltage level in volts: "))
offsetvoltage = float(input("Enter offset voltage level in volts: "))
offsetvoltunit = int(input("Enter 1=mV or 2=V: "))
vunit = int(input("1=VPK, 2=VPP, 3=VRMS, 4=VAMPL, 5=mVPK, 6=mVPP, 7=mVRMS, 8=mVAMPL: "))

# Setting up of function generator
set_source(source)
set_frequency(inst_sig, frequency, frequencymode, frequencyunit)
set_waveform(inst_sig, waveform)
set_voltage(inst_sig, voltage, offsetvoltage, offsetvoltunit, vunit)

# Turn Off and Close
inst_sig.write("OUTP1:STAT OFF")
inst_sig.close()

# Close resource manager
rm.close()
