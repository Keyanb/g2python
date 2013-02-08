# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 11:08:03 2012
Program for Bias Cooling
This program will apply a large voltage to the sample gates while cooling.
Ideally, this depletes the sample meaning no unwanted charging occurs.
It will also record the temperature and conductance data.

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

# Program Parameters

rampTime = 10.0 # (minutes)
maxBias = -2.5
steps = int(rampTime*60)
biasVoltage = -0.0
stepTime = float(rampTime*60/steps)
stepVoltage = float(maxBias/steps)
timeout = 120.0 #(minutes)
timeout #(seconds)


# Initialize the devices

lockin = SRS830.device('GPIB1::8')
bias = DAC488.device('GPIB1::10')
temp = lakeshore332.device('GPIB1::12')


bias.set_range(1,3)
t_start = time.time()
out_file = open ('test.dat', 'w')

# First we need to slowly rampt to our bias voltage

print "Ramping up the Bias Voltage"
out_file.write("Sample: VA150InSn2\n Measuring with 0.05V/500k (100nA)\n")
out_file.write("Ramping up the Bias Voltage\n")

print("...")
print("...")

print("Temp(K) \t Time(s) \t Bias(V) \t X-Value(V)")
out_file.write("Temp(K) \t Time(s) \t Bias(V) \t X-Value(V) \n")

for i in range(steps+1):
    bias.set_voltage(1,biasVoltage)
    time.sleep(stepTime)
    currTemp = float(temp.read('b'))
    xValue = lockin.read_input(1)
    currTime = (time.time()-t_start)/60
    print "%f \t %f \t %f \t %r" % (currTemp, currTime, biasVoltage, xValue)
    out_file.write("%f \t %f \t %f \t %r \n" % (currTemp, currTime, biasVoltage, xValue))
    biasVoltage = biasVoltage + stepVoltage
    
print("Finished Ramping")

Freq = 2500 # Set Frequency To 2500 Hertz
Dur = 300 # Set Duration To 1000 ms == 1 second

winsound.Beep(Freq,Dur)

print("Begin Cooling Sample")

out_file.write("\n---------------------------------------------------- \n")
out_file.write("Temp(K) \t Time(s) \t Bias(V) \t X-Value(V) \n")
out_file.write("Cooling at Bias Voltage %f from Temperature %f \n" % (biasVoltage,currTemp)) 
time.sleep(30)
    
while(currTemp>2 and currTime<timeout):
    currTemp = float(temp.read('b'))
    xValue = lockin.read_input(1)
    currTime = (time.time()-t_start)/60
    print "%f \t %f \t %f \t %r" % (currTemp, currTime, biasVoltage, xValue)
    out_file.write("%f \t %f \t %f \t %r \n" % (currTemp, currTime, biasVoltage, xValue))
    
print("Cooldown Finished!")
print("...")
print("Ramping Voltage back to zero")

winsound.Beep(Freq,Dur)


out_file.write("\n---------------------------------------------------- \n")
out_file.write("Temp(K) \t Time(s) \t Bias(V) \t X-Value(V) \n")

for i in range(steps+1):
    bias.set_voltage(1,biasVoltage)
    time.sleep(stepTime)
    currTemp = float(temp.read('b'))
    xValue = lockin.read_input(1)
    currTime = (time.time()-t_start)/60
    print "%f \t %f \t %f \t %r" % (currTemp, currTime, biasVoltage, xValue)
    out_file.write("%f \t %f \t %f \t %r \n" % (currTemp, currTime, biasVoltage, xValue))
    biasVoltage = biasVoltage - stepVoltage
    
print("Finished Ramping")

winsound.Beep(Freq,Dur)