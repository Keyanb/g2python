# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 22:46:03 2013

@author: bram
"""
import matplotlib.pyplot as plt
import csv
import numpy as np
import time
from scipy.signal import lfilter, lfilter_zi, filtfilt, butter

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