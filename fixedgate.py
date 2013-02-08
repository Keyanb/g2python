# -*- coding: utf-8 -*-
"""
Created on Wed Sep 05 15:58:48 2012

@author: bram
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 11:08:03 2012
Program for Bias Cooling
This program will ramp to set gate voltage and vary the bias at that voltage
Changelog:
    - Created 7/19/2012
    -
@author: Brraaaam
"""

import time
import matplotlib
import SRS830
import DAC488
import lakeshore332
import winsound
import datetime
import os, errno

# Program Parameters

gateSet = -2.0
gateVoltage = -0.0
biasSet = 5.0
biasVoltage = 0.0 
biasStep = 0.1
stepTime = 1
stepVoltage = 0.1 # 1mV steps

#Sample Info

sample = 'VA150ALD2'
wire = 'III'
notes = '.............'
date = time.strftime('%d/%m/%y',time.localtime())

# Initialize the devices

lockin1 = SRS830.device('GPIB::8')
lockin2 = SRS830.device('GPIB::16')
gate = DAC488.device('GPIB::10')
temp = lakeshore332.device('GPIB1::12')

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else: raise

path = 'C:\\Users\\bram\\Documents\\Data\\' + date + '\\' + sample +'\\' + wire + '\\'

# Make the sample directory
mkdir_p(path)

dat_file = open (path + 'rampup.dat', 'w')
meas_file = open (path + 'measurement.txt','w')
gate.set_range(1,3)
t_start = time.time()

# Measurement info is stored in a separate file than the actual values


# Sample info
s = 'Sample: %s \t Wire: %s \n' % (sample,wire)
meas_file.write(s)
print(s)
s = time.strftime('%H:%M:%S',time.localtime()) + '\t Ramping the Gate Voltage from %f to %f \n' % (gateVoltage,gateSet)
meas_file.write(s)

print(s)
print("...")
print("...")

print("Temp(K) \t Time(s) \t Gate(V) \t X-Value(V)\t X-Value-2\n")
dat_file.write("Temp(K) \t Time(s) \t Gate(V) \t X-Value(V)\t X-Value-2\n")


# Start Ramping the Gate

while gateVoltage > gateSet:
    # Set the new Gate Voltage
    gate.set_voltage(1,gateVoltage)
    
    # Wait
    time.sleep(stepTime)
    
    # Get Temperature, Voltages, Time
    currTemp = float(temp.read('b'))
    xValue1 = lockin1.read_input(1)
    xValue2 = lockin2.read_input(1)
    currTime = (time.time()-t_start)/60
    
    # Write the values to file
    print "%f \t %f \t %f \t %r \t %r" % (currTemp, currTime, gateVoltage, xValue1, xValue2)
    dat_file.write("%f \t %f \t %f \t %r \t %r \n" % (currTemp, currTime, gateVoltage, xValue1, xValue2))
    
    # Increment the gate voltage
    gateVoltage = gateVoltage + stepVoltage
    
    

s = time.strftime('%H:%M:%S',time.localtime()) + '\t Finished Ramping. Gate Voltage: %f /n' % gateVoltage
print(s)
meas_file.write(s)

# Close the ramp up file
dat_file.close()

# Open a new data file

dat_file = open (path + 'static_gate.dat')

# Alert that ramp is finished
Freq = 2500 # Set Frequency To 2500 Hertz
Dur = 300 # Set Duration To 1000 ms == 1 second

winsound.Beep(Freq,Dur)

s = time.strftime('%H:%M:%S',time.localtime()) + '\t Beginning Bias Sweep \n'
print s
meas_file.write(s)

print("Temp(K) \t Time(s) \t Gate(V) \t X-Value(V)\t X-Value-2\n")
dat_file.write("Temp(K) \t Time(s) \t Gate(V) \t X-Value(V)\t X-Value-2\n")

while biasVoltage<biasSet:
     # Set the new Gate Voltage
    lockin1.set_amplitude(biasVoltage)
    
    # Wait
    time.sleep(stepTime)
    
    # Get Temperature, Voltages, Time
    currTemp = float(temp.read('b'))
    xValue1 = lockin1.read_input(1)
    xValue2 = lockin2.read_input(1)
    currTime = (time.time()-t_start)/60
    
    # Write the values to file
    print "%f \t %f \t %f \t %r \t %r" % (currTemp, currTime, biasVoltage, xValue1, xValue2)
    dat_file.write("%f \t %f \t %f \t %r \t %r \n" % (currTemp, currTime, biasVoltage, xValue1, xValue2))
    
    # Increment the gate voltage
    biasVoltage = biasVoltage + biasStep


# Close the bias sweep file

dat_file.close()

# Open a new data file

dat_file = open (path + 'rampdown.dat')

s = time.strftime('%H:%M:%S',time.localtime()) + '\t Bias Sweep Finished. Beginning ramp down \n'
print s
meas_file.write(s)


s = "Temp(K) \t Time(s) \t Gate(V) \t X-Value(V) \t X-Value-2\n"
dat_file.write(s)
    
while gateVoltage < 0:
    # Set the new Gate Voltage
    gate.set_voltage(1,gateVoltage)
    
    # Wait
    time.sleep(stepTime)
    
    # Get Temperature, Voltages, Time
    currTemp = float(temp.read('b'))
    xValue1 = lockin1.read_input(1)
    xValue2 = lockin2.read_input(1)
    currTime = (time.time()-t_start)/60
    
    # Write the values to file
    print "%f \t %f \t %f \t %r \t %r" % (currTemp, currTime, gateVoltage, xValue1, xValue2)
    dat_file.write("%f \t %f \t %f \t %r \t %r \n" % (currTemp, currTime, gateVoltage, xValue1, xValue2))
    
    # Increment the gate voltage
    gateVoltage = gateVoltage + stepVoltage
    
print("Cooldown Finished!")
print("...")
print("Ramping Voltage back to zero")

s=time.strftime('%H:%M:%S',time.localtime()) + '\t Measurement Finished \n'
print s
meas_file.write(s)

winsound.Beep(Freq,Dur)

