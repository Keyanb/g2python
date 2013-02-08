# -*- coding: utf-8 -*-
"""
Created on Tue Dec 04 12:06:32 2012
Quick Filter Test 
@author: bram
"""

import SRS830
import time
import numpy
import matplotlib
from pylab import *


stepTime = 5
stepsize = 0.001
freq = numpy.logspace(0,5,100)
n = len(freq)
lockin = SRS830.device('GPIB1::14')
lockin.set_freq(freq[0])

# Plotter
#ion()
#fig = figure()
#fig.canvas.set_window_title("Frequency Sweep")
#ax = fig.add_subplot (111)

dat_file = open ("C:\\Users\\keyan\\Documents\\Data\\Filter\\nitrogen.dat", 'w')
dat_file.write("Frequency(hz) \t X(V) \t Y(V) \n")
print("Frequency(hz) \t X(V) \t Y(V) \n")

x = []
y = []

for i in range(0,n-1):
    lockin.set_freq(freq[i])
    time.sleep(10)
    x.append(lockin.read_input(1))
    y.append(lockin.read_input(2))
    line = "%f \t %s \t %s \n" % (freq[i],x[i],y[i])
    
    print(line)
    dat_file.write(line)
    
print ("Sweep Finished")
    
    
    
