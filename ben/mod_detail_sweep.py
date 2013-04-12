import SRS830
import IPS120
import T344
import readconfigfile as pyfile

#from freq_sweep_functions import *

import threading
import time
import string

from pylab import *

debug_mode = False

using_magnet=True


SAMPLE_CURRENT = 0.1
COIL_VOLTAGE = 1.0


GAIN = 1
I_MEAS = 1e-3

NUM_SAMPLES = 3
NUM_DC_POINTS = 10
NUM_POINTS = 10
MEAS_TIME = 10
REST_TIME = 30
OFFSETS = [-0.005, 0.005]
PHASES = [0, 180]
FIELD_SET = arange(5.18, 5.03, -0.005)

FIELD_SWEEP_RATE = 0.010
GPIB_2_CONNECTED = True
GPIB_3_CONNECTED = True
F1 = 95
F3 = 200


if GPIB_2_CONNECTED:
    #instrumentation setup
    lockins = [SRS830.SRS830('GPIB::8', debug_mode),SRS830.SRS830('GPIB::10', debug_mode),SRS830.SRS830('GPIB::7', debug_mode)]

    # tuple: lockin #, channel, subplot for display
    data_channels = ([0,1,1, array([])], [0,2,2, array([])], [1,1,3, array([])],
                 [1,2,4, array([])], [2,1,5, array([])],[2,2,6, array([])])
elif GPIB_3_CONNECTED:
    #instrumentation setup
    lockins = [SRS830.SRS830('GPIB::8', debug_mode),SRS830.SRS830('GPIB::7', debug_mode)]

    # tuple: lockin #, channel, subplot for display
    data_channels = ([0,1,1, array([])], [0,2,2, array([])], [0,5,3, array([])],
                 [0,7,4, array([])], [1,1,5, array([])],[1,2,6, array([])])
else:
   #instrumentation setup
    lockins = [SRS830.SRS830('GPIB::8', debug_mode)]

    # tuple: lockin #, channel, subplot for display
    data_channels = ([0,1,1, array([])], [0,2,2, array([])], [0,5,3, array([])],
                 [0,7,4, array([])], [0,6,5, array([])],[0,8,6, array([])])
    
    
    
#lakeshore = LS370.LS370('dev12')
f_src = T344.T344('COM1', debug_mode)

if using_magnet==True:
    magnet = IPS120.IPS120('GPIB0::3', debug_mode)
    magnet.unlock()
    magnet.hold()
    magnet.set_field_sweep_rate(FIELD_SWEEP_RATE)


#open file, write header
out_file = pyfile.open_data_file()
t_start = time.time()
out_file.write('#T_start = ' + str(t_start) + '\n')
out_file.write('#NUM_POINTS = ' + str(NUM_POINTS) + '\n')
out_file.write('#NUM_SAMPLES = ' + str(NUM_SAMPLES) + '\n')
out_file.write('#NUM_DC_POINTS = ' + str(NUM_DC_POINTS) + '\n')
out_file.write('#I_MEAS = ' + str(I_MEAS) + '\n')
out_file.write('#Delta_R_scale = 1.0\n')
out_file.write('#GAIN = ' + str(GAIN) + '\n')
out_file.write('#CAL = 1.0\n')
out_file.write('#CAL_ERR = 0.0\n')

out_file.write('time field F1 F2 F3 PHASE OFFSET COIL_CURRENT SAMPLE_CURRENT X1 Y1 X2 Y2 X3 Y3\n')


def auto_scale_y(data):
    span = max(data.max() - data.min(), 0.1 * data.min())
    return (data.min() - span *0.05), (data.max() + span*0.05)



def set_frequencies (f_1, f_3, phase):

    #must use raw
    f_raw_1 = int(67.10887 * f_1)
    f_raw_3 = int(67.10887 * f_3)
        
    if f_1 < f_3:        
        f_raw_2 = f_raw_3 - f_raw_1
    else:
        f_raw_2 = f_raw_3 + f_raw_1
        
    f_src.set_freq_raw(0, f_raw_1)
    f_src.set_freq_raw(1, f_raw_2)        
    f_src.set_freq_raw(2, f_raw_3)
    f_src.set_freq_raw(3, f_raw_3)
    
    f_src.set_phase(3, phase)
    f_src.sync()
    return [f_1, f_raw_2/67.10887, f_3] 


def set_amplitudes (coil_drive, coil_offset):
    f_src.set_amp(0, 5)
    f_src.set_amp(1, 1)        
    f_src.set_amp(2, 1)
    f_src.set_amp(3, coil_drive)
    f_src.set_DC(3, coil_offset)


def read_data():
    output_line = ""
    t_current= time.time() - t_start

    #read 3 lock-ins
    for idx, li in enumerate(data_channels):
        if li[1] <5:
            dat = lockins[li[0]].read_input(li[1])
        else:
            dat = lockins[li[0]].read_aux(li[1]-4)
        
        output_line = output_line + ' %.6e'%dat
        li[3] = append(li[3],dat)

    return output_line

def make_settings_string(field,f_1,f_2,f_3,phase, offset, coil_voltage, sample_current):
    stri = "%.4f %.1f %.1f %.1f %.1f %.3f %.3f %.3f"%(field,f_1,f_2,f_3,phase,offset, coil_voltage, sample_current)
    return stri

def ramp_to_setpoint(field):
    magnet.set_point_field(field)
    magnet.goto_set()

    still_ramping = True
    print ("Ramping field...")
    while still_ramping:
        actual_field = string.rsplit(magnet.read_param(7), "+")[1]
        actual_field = string.rstrip(actual_field, chars='.')
        actual_field = float(actual_field)

        set_field = string.rsplit(magnet.read_param(8), "+")[1]
        set_field = string.rstrip(set_field, chars='.')
        set_field = float(set_field)
        
        still_ramping = abs (actual_field - set_field) > 0.00001
        
        if running ==False:
            return "terminated"
        time.sleep(1)    
    

print 'Enter "x" to leave the application.'

running = True
def main_loop_core(field, f_1, f_2, f_3, coil_voltage, sample_current):
    for sample in range(NUM_SAMPLES):
        offset = 0
        f_src.set_DC(3, offset)

        for phase in PHASES:
            f_src.set_phase(3, phase)
            f_src.sync()
            time.sleep(MEAS_TIME)
            for point in range(NUM_POINTS):
                time.sleep(MEAS_TIME)
                t_str = "%.1f"%(time.time() - t_start)
                s1 = make_settings_string(field, f_1, f_2, f_3, phase, offset, coil_voltage, sample_current)
                s2= read_data()
                out_file.write(t_str +" " + s1 + s2 + "\n")
                print (s2)
                if running==False:
                    print "terminated"
                    return True, times_arr
                    

    phase = 0
    f_src.set_phase(3, phase)
    for offset in OFFSETS:
        ramp_to_setpoint(field + offset)
        time.sleep(MEAS_TIME*2)
        for point in range(NUM_DC_POINTS):   
            time.sleep(MEAS_TIME)
            t_str = "%.1f"%(time.time() - t_start)
            s1 = make_settings_string(field, f_1, f_2, f_3, phase, offset, coil_voltage, sample_current)             
            s2 = read_data()
            out_file.write(t_str +" " + s1 + s2 + "\n")
            print (s2)
            if running==False:
                print "terminated"
                return True, times_arr    
            
    
                    
    return False
                
def main_loop():
    if using_magnet==True:
        print "setting Amplitudes \n"
        set_amplitudes(COIL_VOLTAGE, 0)
        f_src.set_DC(3, 0)
        lockins[0].set_ref_out(SAMPLE_CURRENT)
        
        print "setting frequencies \n"
        [f_1, f_2, f_3] = set_frequencies(F1, F3, 0)

        
        for field in FIELD_SET:
            ramp_to_setpoint(field)

            print ("Thermalizing at new field.\n")
            time.sleep(REST_TIME)    
            print ("Starting data acquisition.\n")
            #run the rest of the layers of the loop
            stopped =  main_loop_core(field, f_1, f_2, f_3, COIL_VOLTAGE, SAMPLE_CURRENT)
            if stopped:
                return "terminated"
    else:
        #using_magnet = False means it's a frequency sweep
        #for coil_voltage in COIL_VOLTAGE_SET:
        #for F3 in FREQ3_SET:
        for i in range (100):
            #F1 = F3/2.0 - 2.5
            print "setting Amplitudes \n"
            set_amplitudes(COIL_VOLTAGE, 0)
            f_src.set_DC(3, 0)
            [f_1, f_2, f_3] = set_frequencies(F1, F3, 0)
            
            print "setting measurement current"
            lockins[0].set_ref_out(SAMPLE_CURRENT)
            
            time.sleep(REST_TIME)  
            stopped =  main_loop_core(0, f_1, f_2, f_3, COIL_VOLTAGE, SAMPLE_CURRENT)
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
