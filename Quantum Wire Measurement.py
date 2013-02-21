# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 12:41:25 2012

@author: bram
"""
import time
from SRS830 import *
import DAC488
import LS340
import os, errno
from conductance_calculator import twopointcond

stepTime = 0.5
max_gate = 2
stepsize = 0.005
windowlower = -1.5
windowupper = -2.0
windowstep = 0.005
gateVoltage = 0.0

overwrite_previous = True

sample = 'VA142-1'
wire = 'ALL'
notes = '.............'
date = time.strftime('%d-%m-%y',time.localtime())

# Initialize the devices

lockin1 = SRS830('GPIB0::8')
lockin2 = SRS830('GPIB0::16')
gate = DAC488.device('GPIB0::10')
# gate = keithley.device('GPIB0::24')
temp = LS340.device('GPIB0::12')

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else: raise

path = 'C:\\Users\\keyan\\Documents\\Data\\' + date + '\\' + sample +'\\' + wire + '\\'

if os.path.isfile(path+'rampup.dat'):
    print 'Warning! File already exists'
    if overwrite_previous == False:
        path = path + 'I'
    
mkdir_p(path)

dat_file = open (path + 'rampup.dat', 'w')
meas_file = open (path + 'measurement.txt','w')
# gate.reset()
# gate.configure_output('VOLT',gateVoltage,0.00005)
# gate.enable_output()

gate.set_range(1,3)
# Set the range to 5V bipolar
t_start = time.time()

print "Window %f to %f" % (windowlower, windowupper)

print("Temp(K) \t Time(s) \t Gate(V) \t X-Value(V)\t Y-Value\t X-Value-2\t Y-Value-2 \n")
dat_file.write("Temp(K) \t Time(s) \t Gate(V) \t X-Value(V)\t Y-Value\t X-Value-2\t Y-Value-2\t Conductance \n")

#plot1 = plot.basicplot()

# Sweep Up Gate
while gateVoltage > max_gate:       
    
    # Set the new Gate Voltage
    # gate.configure_output('VOLT',gateVoltage,0.00005)
    gate.set_voltage(1,gateVoltage)
    
    # Wait
    time.sleep(stepTime)
    
    currTemp = float(temp.read('c'))
    xValue1 = lockin1.read_input(1)
    yValue1 = lockin1.read_input(2)
    xValue2 = lockin2.read_input(1)
    yValue2 = lockin2.read_input(2)
    currTime = (time.time()-t_start)/60
    conductance = twopointcond(xValue1)
    
    #plot1.addPoint(gateVoltage,xValue1)
    
    # Write the values to file
    print "%f \t %f" % (gateVoltage,conductance)
    dat_file.write("%f \t %f \t %f \t %r \t %r \t %r \t %r \t %f \n" % (currTemp, currTime, gateVoltage, xValue1, yValue1, xValue2, yValue2, conductance))
    
    if (gateVoltage <= windowlower and gateVoltage >= windowupper):
        gateVoltage = gateVoltage - windowstep
    else:
            gateVoltage = gateVoltage - stepsize   
            
    
    ## Sweep Down Gate
    
dat_file = open (path + 'rampdown.dat', 'w')

while gateVoltage <= 0:            
     # Set the new Gate Voltage
    # gate.configure_output('VOLT',gateVoltage,0.00005)
    gate.set_voltage(1,gateVoltage)
    # Wait
    time.sleep(stepTime)
    
    currTemp = float(temp.read('c'))
    xValue1 = lockin1.read_input(1)
    yValue1 = lockin1.read_input(2)
    xValue2 = lockin2.read_input(1)
    yValue2 = lockin2.read_input(2)
    currTime = (time.time()-t_start)/60
    conductance = twopointcond(xValue1)
    
    # Write the values to file
    print "%f \t %f" % (gateVoltage,conductance)
    dat_file.write("%f \t %f \t %f \t %r \t %r \t %r \t %r \t %f \n" % (currTemp, currTime, gateVoltage, xValue1, yValue1, xValue2, yValue2, conductance))
        
    if (gateVoltage <= windowlower and gateVoltage >= windowupper):
        gateVoltage = gateVoltage + windowstep
    else:
            gateVoltage = gateVoltage + stepsize  
            
            
print 'Finished!'

gate.set_voltage(1,0)