import LS370
import time
import threading

#import numpy
#import scipy

import matplotlib
#matplotlib.use('GTKAgg')
#import matplotlib.pyplot as plt
from pylab import *


lakeshore = LS370.LS370('dev12')
active_channels = ([[1,array([]),1,'1K pot'],[2,array([]),3, 'Still'],
                    [3,array([]),5, 'ICP'], [4,array([]),7, 'MC'],
                    [5,array([]),2, 'Mats'],[9,array([]),4, 'Cold Plate']])

#lakeshore.auto_scan()


out_file = open ('testfile2.txt', 'a')
t_start = time.time()
TIME_STEP = 10


running = True

ion()
fig = figure()
fig.canvas.set_window_title("LS370 Monitor")
ax = fig.add_subplot (421)
ax = fig.add_subplot (422)
ax = fig.add_subplot (423)
ax = fig.add_subplot (424)
ax = fig.add_subplot (425)
ax = fig.add_subplot (426)

def auto_scale_y(data):
    span = max(data.max() - data.min(), 0.1 * data.min())
    return (data.min() - span *0.05), (data.max() + span*0.05)


def main_loop():


    times = array([])
    line = []
    ax = []
    for idx, chan in enumerate(active_channels):
        dat = lakeshore.read_channel(chan[0])
        ax.append(subplot(4,2, chan[2]))
        tline, = ax[idx].plot(0, dat/1000, '.-')
        ax[idx].tick_params(axis='x', labelsize=8)
        ax[idx].tick_params(axis='y', labelsize=8)
        ylabel(chan[3])
        line.append(tline)
    fig.canvas.draw()
    
    while (running):
        t_current= time.time() - t_start
        
        times = append(times,t_current)
        stri = "%.1f, "%(t_current)
        
        for idx, chan in enumerate(active_channels):
            lakeshore.scanner_to_channel(chan[0])
            
            time.sleep(TIME_STEP)

            dat = lakeshore.read_channel(chan[0])
            chan[1] = append(chan[1],dat)
            stri += "%.3f, "%dat
            #ax = subplot(4,2, chan[2])
            line[idx].set_data(times, chan[1]/1000.)
            y1, y2 = auto_scale_y(chan[1]/1000.)
            ax[idx].set_ylim(ymin = y1, ymax = y2)
            #ax[idx].plot(times, chan[1]/1000., 'o')
            ax[idx].set_xlim(xmin=0, xmax = t_current)
            fig.canvas.draw()
            if running == False:
                break
            
        

        stri += "0\n"
        print(stri)
        out_file.write(stri)
        



    print "finished"

    
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
fig.show()

out_file.close()
lakeshore.close()
