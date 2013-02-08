# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 16:44:54 2012
Script to measure conductance with magnet
@author: bram
"""

# Import instrument drivers
import lakeshore332, DAC488, SRS830, n5700

# Import other libraries
import string, os, sys, time, winsound, matplotlib
import tkFileDialog

# Initialize the Instruments

lockin = SRS830.device('GPIB1::8')
bias = DAC488.device('GPIB1::10')
temp = lakeshore332.device('GPIB1::12')
pwr = n5700.device('GPIB1::??')

# Set up required for the DAC
bias.set_range(1,3)

filename = tkFileDialog.asksaveasfilename()
print filename  # test

t_start = time.time()

out_file = open (filename, 'w')
