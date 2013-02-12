# -*- coding: utf-8 -*-
"""
DAC488 Testing Program
Since there have been extensive problems with the DAC,
this program has been created for the purpose of testing
the basic DAC functions. It can also be used as an example
for DAC functionality.
"""
import DAC488
import time

# Initialize the DAC
gate = DAC488.device('GPIB0::10')
time.sleep(3)

# Next we need to set the range of the port
# The first number is the port, the second the setting code
time.sleep(3)
gate.set_range(1,3)

# Port 1 is set to 5V bipolar

for i in range(0,5):
    gate.set_voltage(1,i)
    time.sleep(1)
    
# You should observe the gate sweep from 0-4 volts
print "finished test"