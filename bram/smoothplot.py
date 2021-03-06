# -*- coding: utf-8 -*-
"""
Created on Mon Apr 01 11:18:48 2013

@author: gervais

"""

import matplotlib.pyplot as plt
import csv
import numpy as np
import time
from scipy.signal import lfilter, lfilter_zi, filtfilt, butter

plt.close('all')
def readConductanceData(filepath):
    freq = []
    cond =[]
    reader = csv.reader(open(filepath),delimiter = '\t',)
    reader.next()
    
    for row in reader:   
        try:
            cond.append(float(row[10]))
            freq.append(float(row[0]))
        except:
            print 'Bad Row'
            
    return (freq,cond)

def smoothData(xn):
    xn = cond
    # Create an order 3 lowpass butterworth filter.
    b, a = butter(3, 0.05)
    
    # Apply the filter to xn.  Use lfilter_zi to choose the initial condition
    # of the filter.
    zi = lfilter_zi(b, a)
    z, _ = lfilter(b, a, xn, zi=zi*xn[0])
    
    # Apply the filter again, to have a result filtered at an order
    # the same as filtfilt.
    z2, _ = lfilter(b, a, z, zi=zi*z[0])
    
    # Use filtfilt to apply the filter.
    y = filtfilt(b, a, xn)
    return y
plt.hold(True)

gate = ['-0.4','-0.41','-0.42','-0.43','-0.44','-0.46','-0.48','-0.5','-0.52','-0.54','-0.56','-0.58','-0.6','-0.62','-0.64','-0.66','-0.68','-0.7']
data = ['/home/bram/Ubuntu One/Thesis/Data/NMR-Gate Sweep/Va150InSn1-III-NMR-Gate' + v + '.dat' for v in gate]

for i, (path,v) in enumerate(zip(data,gate)):
    (freq,cond) = readConductanceData(path)
    smoothCond = smoothData(cond)
    x = np.array(freq)
    y = np.array(cond)
    
#    avg = np.average(y)
#    
#    y = y/avg - float(i)/70
#      
    plt.figure(i+1)
    plt.subplot(111)
    plt.plot(x,y,'-ro',markersize=3.0)
    plt.plot(freq,smoothCond,linewidth=2.0)
    
    plt.title('NMR at Gate '+v)
    plt.xlabel('Frequency (hz)')
    plt.ylabel('Conductance (A.U)')
    #plt.legend(gate)
    plt.draw()
    
plt.show()