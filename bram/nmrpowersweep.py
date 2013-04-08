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

#files = [
#'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-29\\VA150InSn1-III-ContactaX-WT-23mK-NMR.dat-10.0.dat-20.0.dat',
#'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-29\\VA150InSn1-III-ContactaX-WT-23mK-NMR.dat-10.0.dat-19.0.dat',
#'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-29\\VA150InSn1-III-ContactaX-WT-23mK-NMR.dat-10.0.dat-18.0.dat',
#'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-29\\VA150InSn1-III-ContactaX-WT-23mK-NMR.dat-10.0.dat-17.0.dat',
#'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-29\\VA150InSn1-III-ContactaX-WT-23mK-NMR.dat-10.0.dat-16.0.dat',
#'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-29\\VA150InSn1-III-ContactaX-WT-23mK-NMR.dat-10.0.dat-15.0.dat',
#'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-29\\VA150InSn1-III-ContactaX-WT-23mK-NMR.dat-10.0.dat-14.0.dat',
#'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-29\\VA150InSn1-III-ContactaX-WT-23mK-NMR.dat-10.0.dat-13.0.dat',
#'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-29\\VA150InSn1-III-ContactaX-WT-23mK-NMR.dat-10.0.dat-12.0.dat',
#'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-29\\VA150InSn1-III-ContactaX-WT-23mK-NMR.dat-10.0.dat-11.0.dat',
#'\\\\leod.physics.mcgill.ca\\Gervais\\data\\data dilution fridge\\Qwire\\data\\13-03-29\\VA150InSn1-III-ContactaX-WT-23mK-NMR.dat-10.0.dat-10.0.dat',
#]

files = [
'/home/bram/Documents/Data/13-03-29/VA150InSn1-III-ContactaX-WT-23mK-NMR.dat-10.0.dat-20.0.dat',
'/home/bram/Documents/Data/13-03-29/VA150InSn1-III-ContactaX-WT-23mK-NMR.dat-10.0.dat-19.0.dat',
'/home/bram/Documents/Data/13-03-29/VA150InSn1-III-ContactaX-WT-23mK-NMR.dat-10.0.dat-18.0.dat',
'/home/bram/Documents/Data/13-03-29/VA150InSn1-III-ContactaX-WT-23mK-NMR.dat-10.0.dat-17.0.dat',
'/home/bram/Documents/Data/13-03-29/VA150InSn1-III-ContactaX-WT-23mK-NMR.dat-10.0.dat-16.0.dat',
'/home/bram/Documents/Data/13-03-29/VA150InSn1-III-ContactaX-WT-23mK-NMR.dat-10.0.dat-15.0.dat',
'/home/bram/Documents/Data/13-03-29/VA150InSn1-III-ContactaX-WT-23mK-NMR.dat-10.0.dat-14.0.dat',
'/home/bram/Documents/Data/13-03-29/VA150InSn1-III-ContactaX-WT-23mK-NMR.dat-10.0.dat-13.0.dat',
'/home/bram/Documents/Data/13-03-29/VA150InSn1-III-ContactaX-WT-23mK-NMR.dat-10.0.dat-12.0.dat',
'/home/bram/Documents/Data/13-03-29/VA150InSn1-III-ContactaX-WT-23mK-NMR.dat-10.0.dat-11.0.dat',
'/home/bram/Documents/Data/13-03-29/VA150InSn1-III-ContactaX-WT-23mK-NMR.dat-10.0.dat-10.0.dat',
]

dB = ['-20.0dB','-19.0dB','-18.0dB','-17.0dB','-16.0dB','-15.0dB','-14.0dB','-13.0dB','-12.0dB','-11.0dB','-10.0dB']
freq20,freq19,freq18,freq17,freq16,freq15,freq14,freq13,freq12,freq11,freq10 = ([] for i in range(11))
cond20,cond19,cond18,cond17,cond16,cond15,cond14,cond13,cond12,cond11,cond10 = ([] for i in range(11))
x = [freq20,freq19,freq18,freq17,freq16,freq15,freq14,freq13,freq12,freq11,freq10]
y = [cond20,cond19,cond18,cond17,cond16,cond15,cond14,cond13,cond12,cond11,cond10]

for data,xvar,yvar in zip(files,x,y):
    reader = csv.reader(open(data),delimiter = '\t',)
    header = reader.next()
    for row in reader:   
        try:
            yvar.append(float(row[10]))
            xvar.append(float(row[0]))
        except:
            print 'Bad Row'

fig = plt.figure(1)
ax = plt.subplot(111)
for freq,cond in zip(x,y):
    ax.plot(freq,cond)
plt.title('NMR Power Sweep')
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
plt.legend(dB,bbox_to_anchor=(1.15, 1.0))
plt.xlabel(header[0])
plt.ylabel(header[10])

#ax.annotate("Possible Feature?",
#            xy=(42080000, 1.27), xycoords='data',
#            xytext=(42150000, 1.2), textcoords='data',
#            arrowprops=dict(arrowstyle="fancy",
#                            connectionstyle="arc3,rad=-0.3"),
#            )
            

plt.show()
