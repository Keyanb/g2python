# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 22:51:37 2013
Conductance Plot
@author: bram
"""

import matplotlib.pyplot as plt
from brams_plot_functions import *
import csv
import numpy as np
import time
from scipy.signal import lfilter, lfilter_zi, filtfilt, butter

#(x,y) = readConductanceData('/home/bram/Ubuntu One/Thesis/Data/13-03-29/VA150InSn1-III-ContactaX-WT-23mK-3.dat')
(x,y) = readConductanceData('D:\\MANIP\\DATA\\13-04-15\\VA150InSn1-Wire V-23mK-2.dat')
ny = np.array(y)
ny = ny - 0.1
plt.plot(x,ny,'-ro',markersize=3.0)
plt.title('Wire Conductance at 23mK')
plt.xlabel('Gate Voltage (V)')
plt.ylabel('Conductance (2e^2/h')
plt.grid('on')
plt.yticks(range(20))
plt.show()