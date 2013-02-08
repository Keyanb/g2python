# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 12:41:25 2012

@author: bram
"""
import time
import SRS830
import DAC488
import lakeshore332
import os, errno
import plot
import keithley

stepTime = 0.3
max_gate = -2.2
stepsize = 0.001
windowlower = -1.5
windowupper = -2.0
windowstep = 0.0001
gateVoltage = 0.0


sample = 'VA150ALD2'
wire = 'III'
notes = '.............'
date = time.strftime('%d-%m-%y',time.localtime())

# Initialize the devices

lockin1 = SRS830.device('GPIB0::8')
lockin2 = SRS830.device('GPIB0::16')
#gate = DAC488.device('GPIB::10')
gate = keithley.device('GPIB0::24')
temp = lakeshore332.device('GPIB0::12')

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else: raise

path = 'C:\\Users\\bram\\Documents\\Data\\' + date + '\\' + sample +'\\' + wire + '\\'

if os.path.isfile(path+'rampup.dat'):
    print 'Warning! File already exists'
    path = path + 'I'
    
mkdir_p(path)

dat_file = open (path + 'rampup.dat', 'w')
meas_file = open (path + 'measurement.txt','w')
gate.reset()
gate.configure_output('VOLT',gateVoltage,0.00005)
gate.enable_output()

t_start = time.time()

print "Window %f to %f" % (windowlower, windowupper)

print("Temp(K) \t Time(s) \t Gate(V) \t X-Value(V)\t X-Value-2\n")
dat_file.write("Temp(K) \t Time(s) \t Gate(V) \t X-Value(V)\t X-Value-2\n")

#plot1 = plot.basicplot()

# Sweep Up Gate
while gateVoltage > max_gate:       
    
    # Set the new Gate Voltage
    gate.configure_output('VOLT',gateVoltage,0.00005)
    
    # Wait
    time.sleep(stepTime)
    
    currTemp = float(temp.read('c'))
    xValue1 = lockin1.read_input(1)
    yValue1 = lockin1.read_input(2)
    xValue2 = lockin2.read_input(1)
    yValue2 = lockin2.read_input(2)
    currTime = (time.time()-t_start)/60
    
    #plot1.addPoint(gateVoltage,xValue1)
    
    # Write the values to file
    print "%f \t %f \t %f \t %r \t %r" % (currTemp, currTime, gateVoltage, xValue1, yValue1, xValue2, yValue2)
    dat_file.write("%f \t %f \t %f \t %r \t %r \n" % (currTemp, currTime, gateVoltage, xValue1, yValue1, xValue2, yValue2))
    
    if (gateVoltage <= windowlower and gateVoltage >= windowupper):
        gateVoltage = gateVoltage - windowstep
    else:
            gateVoltage = gateVoltage - stepsize   
            
    
    ## Sweep Down Gate
while gateVoltage <= 0:            
     # Set the new Gate Voltage
    gate.configure_output('VOLT',gateVoltage,0.00005)
    
    # Wait
    time.sleep(stepTime)
    
    currTemp = float(temp.read('c'))
    xValue1 = lockin1.read_input(1)
    xValue2 = lockin2.read_input(1)
    currTime = (time.time()-t_start)/60
    
    # Write the values to file
    print "%f \t %f \t %f \t %r \t %r" % (currTemp, currTime, gateVoltage, xValue1, xValue2)
    dat_file.write("%f \t %f \t %f \t %r \t %r \n" % (currTemp, currTime, gateVoltage, xValue1, xValue2))
        
    if (gateVoltage <= windowlower and gateVoltage >= windowupper):
        gateVoltage = gateVoltage + windowstep
    else:
            gateVoltage = gateVoltage + stepsize  