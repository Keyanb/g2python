# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 13:18:32 2012

@author: Benjamin Schmidt
"""

import SRS830
import IPS120

import pyfile
import threading
import time
import string
import matplotlib
from pylab import *

using_magnet = True
GPIB_2_CONNNECTED = True
MEAS_TIME = 3

if GPIB_2_CONNNECTED:
    #instrumentation setup
    lockins = [SRS830.SRS830('GPIB::8'),SRS830.SRS830('GPIB::10'),SRS830.SRS830('GPIB::7')]

    # tuple: lockin #, channel, subplot for display
    data_channels = ([0,1,1, array([])], [0,2,2, array([])], [1,1,3, array([])],
                 [1,2,4, array([])], [2,1,5, array([])],[2,2,6, array([])])
else:
    #instrumentation setup
    lockins = [SRS830.SRS830('GPIB::8'),SRS830.SRS830('GPIB::7')]

    # tuple: lockin #, channel, subplot for display
    data_channels = ([0,1,1, array([])], [0,2,2, array([])], [0,5,3, array([])],
                 [0,7,4, array([])], [1,1,5, array([])],[1,2,6, array([])])

if using_magnet==True:
    magnet = IPS120.IPS120('dev3')


#open file, write header
out_file = pyfile.open_data_file()
t_start = time.time()
out_file.write('Starting time: ' + str(t_start) + '\n')
out_file.write('time, field, X1, Y1, X2, Y2, X3, Y3\n')

ion()
fig = figure()
fig.canvas.set_window_title("Data taking program")
ax = fig.add_subplot (421)
ax = fig.add_subplot (422)
ax = fig.add_subplot (423)

line = []
ax = []

def auto_scale_y(data):
    span = max(data.max() - data.min(), 0.1 * data.min())
    return (data.min() - span *0.05), (data.max() + span*0.05)

def read_data():
    output_line = ""
    t_current= time.time() - t_start

    if using_magnet==True:
        current_field = float(magnet.read_field().lstrip('R'))
        output_line = output_line + "%.5f"%current_field #read magnet
        
    #read 3 lock-ins
    for idx, li in enumerate(data_channels):
        if li[1] <5:
            dat = lockins[li[0]].read_input(li[1])
        else:
            dat = lockins[li[0]].read_aux(li[1]-4)
        
        output_line = output_line + ', %.6e'%dat
        li[3] = append(li[3],dat)
                 
        line[idx].set_data(arange(li[3].size), li[3])

        y1, y2 = auto_scale_y(li[3])
        ax[idx].set_ylim(ymin = y1, ymax = y2)
        #ax[idx].plot(times, chan[1]/1000., 'o')
        ax[idx].set_xlim(xmin=0, xmax = li[3].size-1)
    fig.canvas.draw()
                 
    #output_line = output_line + str(lakeshore.read_channel(9))    

    return output_line

def main_loop():
    for idx, chan in enumerate(data_channels):
        ax.append(subplot(3,2, chan[2]))
        tline, = ax[idx].plot(0, 0, '.-')
        ax[idx].tick_params(axis='x', labelsize=8)
        ax[idx].tick_params(axis='y', labelsize=8)
        line.append(tline)
    fig.canvas.draw()   
    
    running = True
    while running == True:
        t_str = "%.1f, "%(time.time() - t_start)
        s2 = read_data()
        output_string = t_str + s2 + "\n"
        out_file.write(output_string)
        print output_string
        time.sleep(MEAS_TIME)
T = threading.Thread(target=main_loop)
T.start()

input=1
while 1 :
	# get keyboard input
	input = raw_input(">> ")
        # Python 3 users
        # input = input(">> ")
	if input == 'x':
                running = False
		break

out_file.close()

for li in lockins:
    li.close()

if using_magnet==True:
    magnet.close()