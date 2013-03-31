# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 16:47:36 2013
Data Reader
Reads in the data from my tab delimted files
@author: bram
"""

import matplotlib.pyplot as plt
import csv
import numpy as np
from collections import defaultdict
plt.hold(True)

files = [
'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-30\\VA150InSn1-III-NMR-Gate-0.7.dat',
'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-30\\VA150InSn1-III-NMR-Gate-0.68.dat',
'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-30\\VA150InSn1-III-NMR-Gate-0.66.dat',
'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-30\\VA150InSn1-III-NMR-Gate-0.64.dat',
'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-30\\VA150InSn1-III-NMR-Gate-0.62.dat',
'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-30\\VA150InSn1-III-NMR-Gate-0.6.dat',
'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-30\\VA150InSn1-III-NMR-Gate-0.58.dat',
'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-30\\VA150InSn1-III-NMR-Gate-0.56.dat',
'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-30\\VA150InSn1-III-NMR-Gate-0.54.dat',
'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-30\\VA150InSn1-III-NMR-Gate-0.52.dat',
'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-30\\VA150InSn1-III-NMR-Gate-0.5.dat',
'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-30\\VA150InSn1-III-NMR-Gate-0.48.dat',
'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-30\\VA150InSn1-III-NMR-Gate-0.46.dat',
'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-30\\VA150InSn1-III-NMR-Gate-0.44.dat',
'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-30\\VA150InSn1-III-NMR-Gate-0.42.dat',
'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-30\\VA150InSn1-III-NMR-Gate-0.4.dat',
]

gate = ['0.7','0.68','0.66','0.64','0.62','0.6','0.58','0.56','0.54','0.52','0.5','0.48','0.46','0.44','0.42','0.4']
freq70,freq68,freq66,freq64,freq62,freq60,freq58,freq56,freq54,freq52,freq50,freq48,freq46,freq44,freq42,freq40 = ([] for i in range(16))
cond70,cond68,cond66,cond64,cond62,cond60,cond58,cond56,cond54,cond52,cond50,cond48,cond46,cond44,cond42,cond40 = ([] for i in range(16))
x = [freq70,freq68,freq66,freq64,freq62,freq60,freq58,freq56,freq54,freq52,freq50,freq48,freq46,freq44,freq42,freq40]
y = [cond70,cond68,cond66,cond64,cond62,cond60,cond58,cond56,cond54,cond52,cond50,cond48,cond46,cond44,cond42,cond40]

for data,xvar,yvar in zip(files,x,y):
    reader = csv.reader(open(data),delimiter = '\t',)
    header = reader.next()
    for row in reader:   
        try:
            yvar.append(float(row[10]))
            xvar.append(float(row[0]))
        except:
            print 'Bad Row'

plt.figure(1)
for freq,cond in zip(x,y):
    plt.plot(freq,cond)

plt.title('NMR Power Sweep')
plt.legend(gate)
plt.xlabel(header[0])
plt.ylabel(header[10])
plt.show()
