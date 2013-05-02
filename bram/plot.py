# -*- coding: utf-8 -*-
"""
Created on Mon Apr 01 11:18:48 2013

@author: gervais
"""

import matplotlib.pyplot as plt
import csv
import numpy as np
from scipy.signal import lfilter, lfilter_zi, filtfilt, butter

#filename = 'C:\\Users\\Shared\\Data\\2013\\Sweep\\sweep_13B2_0426.001'
filename = 'D:\\MANIP\\DATA\\13-04-26\\VA150InSn1-Wire III-CurrentXT-VoltageWa.dat'

data = np.loadtxt(filename,skiprows=1)
        

plt.hold(True)
plt.figure(1)
plt.grid()

#comp = np.abs(data[:,4] + 1j * data[:,5])

plt.plot(data[:,0],data[:,10],'-o',markersize=3)

plt.title('Hall Effect')
plt.xlabel('Field(T)')
plt.ylabel('Voltage(V)')

plt.show()