# -*- coding: utf-8 -*-
"""
Created on Mon Apr 01 11:18:48 2013

@author: gervais
"""

import matplotlib.pyplot as plt
import csv
import numpy as np
from scipy.signal import lfilter, lfilter_zi, filtfilt, butter

data = '\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-31\\VA150InSn1-III-NMR-Gate-0.4.dat'

freq = []
cond =[]

reader = csv.reader(open(data),delimiter = '\t',)
header = reader.next()
for row in reader:   
    try:
        cond.append(float(row[10]))
        freq.append(float(row[0]))
    except:
        print 'Bad Row'
        
x = cond
window = 'blackman'
window_len = 15
s=np.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
w=eval('np.'+window+'(window_len)')
y=np.convolve(w/w.sum(),s,mode='valid')
smoothcond = y[9:809]

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

print len(freq)
print len(y)

plt.hold(True)
plt.figure(1)

plt.plot(freq,cond, 'ro',markersize=3.0)
plt.plot(freq,y,linewidth=2)

plt.title('NMR at Gate 0.4')
plt.xlabel('Frequency (hz)')
plt.ylabel('Conductance (2e^2/h)')

plt.show()