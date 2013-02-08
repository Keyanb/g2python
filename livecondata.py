# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 11:53:53 2012
This program is responsible for collecting data from instruments
@author: keyan
"""

import time
import SRS830
import lakeshore332
import os, errno
import keithley
import threading

class acquiredata():

    def __init(self,data_q):
        threading.Thread.__init__(self)
        self.data_q = data_q
        
        # What does this do?
        self.alive = threading.Event()
        self.alive.set()
        
        self.stepTime = 0.3
        self.max_gate = -2.2
        self.stepsize = 0.001
        self.windowlower = -1.5
        self.windowupper = -2.0
        self.windowstep = 0.0001
        self.gateVoltage = 0.0
        self.gatecompliance = 0.00005
        
        # Initialize the devices

        self.lockin1 = SRS830.device('GPIB0::8')
        self.lockin2 = SRS830.device('GPIB0::16')
        #gate = DAC488.device('GPIB::10')
        self.gate = keithley.device('GPIB0::24')
        self.temp = lakeshore332.device('GPIB0::12')
        
        self.gate.reset()
        self.gate.configure_output('VOLT',gateVoltage,0.00005)
        self.gate.enable_output()

        t_start = time.time()


        self.setupfile("VA150ALD2","III")
        
    def setupfile(self,sample,wire):
        '''
        Sets up the file
        '''
        # sample = 'VA150ALD2'
        # wire = 'III'
        notes = '.............'
        date = time.strftime('%d-%m-%y',time.localtime())

        def mkdir_p(path):
            try:
                os.makedirs(path)
            except OSError as exc:
                if exc.errno == errno.EEXIST:
                    pass
                else: raise

        path = 'C:\\Users\\bram\\Documents\\Data\\' + date + '\\' + sample +'\\' + wire + '\\'

        if os.path.isfile(path+'rampup.dat'):
            print 'Warning! File already exists'
            path = path + 'I'
            
            mkdir_p(path)

        dat_file = open (path + 'data.dat', 'w')
        meas_file = open (path + 'measurement.txt','w')
        
    def run(self):

        # print "Window %f to %f" % (windowlower, windowupper)

        print("Temp(K) \t Time(s) \t Gate(V) \t X-Value(V)\t X-Value-2\n")
        dat_file.write("Temp(K) \t Time(s) \t Gate(V) \t X-Value(V)\t X-Value-2\n")
        delay = self.stepTime
        gateVoltage = self.gateVoltage
        # Sweep Up Gate
        while gateVoltage > max_gate:       
            
        # Set the new Gate Voltage
        self.gate.configure_output('VOLT',gateVoltage,self.compliance)
        
        # Wait
        time.sleep(delay)
        
        currTemp = float(temp.read('c'))
        xValue1 = lockin1.read_input(1)
        yValue1 = lockin1.read_input(2)
        xValue2 = lockin2.read_input(1)
        yValue2 = lockin2.read_input(2)
        currTime = (time.time()-t_start)
    
        #plot1.addPoint(gateVoltage,xValue1)
        
        # Write the values to file
        print "%f \t %f \t %f \t %r \t %r" % (currTemp, currTime, gateVoltage, xValue1, yValue1, xValue2, yValue2)
        dat_file.write("%f \t %f \t %f \t %r \t %r \n" % (currTemp, currTime, gateVoltage, xValue1, yValue1, xValue2, yValue2))
    
        if (gateVoltage <= windowlower and gateVoltage >= windowupper):
            gateVoltage = gateVoltage - windowstep
            else:
                gateVoltage = gateVoltage - stepsize   
                
    
        ## Sweep Down Gate
        while gateVoltage <= 0:            
            # Set the new Gate Voltage
            gate.configure_output('VOLT',gateVoltage,0.00005)
            
            # Wait
            time.sleep(stepTime)
            
            currTemp = float(temp.read('c'))
            xValue1 = lockin1.read_input(1)
            xValue2 = lockin2.read_input(1)
            currTime = (time.time()-t_start)/60
            
            # Write the values to file
            print "%f \t %f \t %f \t %r \t %r" % (currTemp, currTime, gateVoltage, xValue1, xValue2)
            dat_file.write("%f \t %f \t %f \t %r \t %r \n" % (currTemp, currTime, gateVoltage, xValue1, xValue2))
        
        if (gateVoltage <= windowlower and gateVoltage >= windowupper):
            gateVoltage = gateVoltage + windowstep
        else:
                gateVoltage = gateVoltage + stepsize
            
        def join(self, timeout=None):
        self.alive.clear()
        threading.Thread.join(self, timeout)