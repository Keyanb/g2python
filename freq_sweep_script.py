import SRS830
import IPS120
#import LS370
import T344

from freq_sweep_functions import *

import threading
import time
import string

import matplotlib
from pylab import *

using_magnet=True
COIL_VOLTAGE = 1.4
NUM_SAMPLES = 5
NUM_POINTS = 10
MEAS_TIME = 10
REST_TIME = 30
OFFSETS = [-2, 2]
PHASES = [0, 180]
FIELD_SET = arange(0.5, 0.52, 0.002)

#instrumentation setup
lockins = [SRS830.device('dev9'),SRS830.device('dev8'),SRS830.device('dev2')]

# tuple: lockin #, channel, subplot for display
data_channels = ([0,1,1, array([])], [0,2,2, array([])], [1,1,3, array([])],
                 [1,2,4, array([])], [2,1,5, array([])],[2,2,6, array([])])

#lakeshore = LS370.LS370('dev12')
f_src = T344.T344('COM1')

if using_magnet==True:
    magnet  = IPS120.IPS120('dev3')
    magnet.unlock()
    magnet.hold()
    magnet.set_field_sweep_rate(0.001)


#open file, write header
out_file = open ('3-11-10-2A_12B1_0515_test1.txt', 'w')
t_start = time.time()
out_file.write('Starting time: ' + str(t_start) + '\n')
out_file.write('time, field, F1, F2, F3, X1, Y1, X2, Y2, X3, Y3, LS9, CMN\n')


ion()
fig = figure()
fig.canvas.set_window_title("Data taking program")
ax = fig.add_subplot (421)
ax = fig.add_subplot (422)
ax = fig.add_subplot (423)
ax = fig.add_subplot (424)
ax = fig.add_subplot (425)
ax = fig.add_subplot (426)

line = []
ax = []

def auto_scale_y(data):
    span = max(data.max() - data.min(), 0.1 * data.min())
    return (data.min() - span *0.05), (data.max() + span*0.05)



def set_frequencies (f_1, f_3, phase):
    if f_1 < f_3:
        #must use raw
        f_raw_1 = int(67.10887 * f_1)
        f_raw_3 = int(67.10887 * f_3)
        f_raw_2 = f_raw_3 - f_raw_1

        f_src.set_freq_raw(0, f_raw_1)
        f_src.set_freq_raw(1, f_raw_2)        
        f_src.set_freq_raw(2, f_raw_3)
        f_src.set_freq_raw(3, f_raw_3)
        
        f_src.set_phase(3, phase)
        f_src.sync()
        return [f_1, f_raw_2/67.10887, f_3] 
    else:
        return "frequency 1 too large"

def set_amplitudes (coil_drive, coil_offset):
    f_src.set_amp(0, 1)
    f_src.set_amp(1, 1)        
    f_src.set_amp(2, 1)
    f_src.set_amp(3, coil_drive)
    f_src.set_DC(3, coil_offset)


def read_data():
    output_line = ""
    t_current= time.time() - t_start

    #read 3 lock-ins
    for idx, li in enumerate(data_channels):

        dat = lockins[li[0]].read_input(li[1])
        output_line = output_line + '%.2e, '%dat
        li[3] = append(li[3],dat)
                 
        line[idx].set_data(arange(li[3].size), li[3])

        y1, y2 = auto_scale_y(li[3])
        ax[idx].set_ylim(ymin = y1, ymax = y2)
        #ax[idx].plot(times, chan[1]/1000., 'o')
        ax[idx].set_xlim(xmin=0, xmax = li[3].size-1)
    fig.canvas.draw()
                 
    #output_line = output_line + str(lakeshore.read_channel(9))    

    return output_line

def make_settings_string(field,f_1,f_2,f_3,phase, offset):
    stri = "%.4f, %.1f, %.1f, %.1f, %.1f,%.3f,"%(field,f_1,f_2,f_3,phase,offset)
    return stri


print "setting frequencies \n"
[f_1, f_2, f_3] = set_frequencies(425, 875, 0)
print "setting Amplitudes \n"
set_amplitudes(1.4, 0)

print 'Enter "x" to leave the application.'

running = True
def main_loop_core(field):
    for sample in range(NUM_SAMPLES):
        for offset in OFFSETS:
            f_src.set_DC(3, offset)
            for phase in PHASES:
                f_src.set_phase(3, phase)
                f_src.sync()
                for point in range(NUM_POINTS):
                    time.sleep(MEAS_TIME)
                    t_str = "%.1f"%(time.time() - t_start)
                    s1 = make_settings_string(field, f_1, f_2, f_3, phase, offset)
                    s2= read_data() + '\r\n'
                    out_file.write(t_str +", " + s1 + ", " + s2)
                    print (s2)

                    if running==False:
                        print "terminated"
                        return True, times_arr
    return False
                
def main_loop():
    for idx, chan in enumerate(data_channels):
        ax.append(subplot(3,2, chan[2]))
        tline, = ax[idx].plot(0, 0, '.-')
        ax[idx].tick_params(axis='x', labelsize=8)
        ax[idx].tick_params(axis='y', labelsize=8)
        line.append(tline)
    fig.canvas.draw()    

    for field in FIELD_SET:
        magnet.set_point_field(field)
        magnet.goto_set()

        condition = True
        print ("Ramping field...")
        while condition :
            actual_field = string.rsplit(magnet.read_param(7), "+")[1]
            actual_field = string.rstrip(actual_field, chars='.')
            actual_field = float(actual_field)

            set_field = string.rsplit(magnet.read_param(8), "+")[1]
            set_field = string.rstrip(set_field, chars='.')
            set_field = float(set_field)
            
            condition = abs (actual_field - set_field) > 0.00001
            
            if running ==False:
                return "terminated"
            time.sleep(1)
        print ("Thermalizing at new field.\n")
        time.sleep(REST_TIME)    
        print ("Starting data acquisition.\n")
        #run the rest of the layers of the loop
        stopped =  main_loop_core(field)
        if stopped:
            return "terminated"
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

out_file.close()

for li in lockins:
    li.close()

if using_magnet==True:
    magnet.close()
#lakeshore.close()
f_src.close()
