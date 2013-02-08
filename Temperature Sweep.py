# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 16:17:59 2012
Program for Binxin
@author: Bram!
"""

import SRS830
import lakeshore332
import time

t_start = time.time()
points = 1000000
timestep = 1 #(s)
step = 0
lockin = SRS830.device('GPIB1::8')
#lockin2 = SRS830.device('GPIB::17')
temp = lakeshore332.device('GPIB1::12')
#Write the filename here
filename = 'D:\\MANIP\\DATA\\Binxin\\RT_VTI.dat'

out_file = open (filename, 'w')
out_file.write('X-Value\t Y-Value\t Temperature\t Time \n') 
print 'X-Value\t Y-Value\t Temperature\t Time'

def read():
    t = time.time() - t_start
    t = float(t)
    x_value = lockin.read_input(1)
    x = float(x_value)
    y_value = lockin.read_input(2)
    y = float(y_value)
    # gate = gate
    temperature = float(temp.read('b'))
    return [x, y, temperature, t]

for i in range(points):
    data = read()
    print "%r \t %r \t %r \t %f" % (data[0], data[1], data[2], data[3])
    out_file.write("%r \t %r \t %r \t %f\n" % (data[0], data[1], data[2], data[3]))
    step = step+1
    #Wait until the enxt timestep
    while (time.time()-t_start)<step:
        wait=1
        
print ('Measurement Complete!')
        
        
            