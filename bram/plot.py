# -*- coding: utf-8 -*-
"""
Created on Mon Apr 01 11:18:48 2013

@author: gervais
"""

import matplotlib.pyplot as plt
import csv
import numpy as np
from scipy.signal import lfilter, lfilter_zi, filtfilt, butter

data = '\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-30\\VA150InSn1-III-Contacts-aX-WT-23mK-5.8T.dat'

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
        

plt.hold(True)
plt.figure(1)

plt.plot(freq,cond)

plt.title('Gate at 5.8T')
plt.xlabel('Frequency (hz)')
plt.ylabel('Conductance (2e^2/h)')

plt.show()