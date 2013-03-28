# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 11:41:32 2013

@author: keyan
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import visa
from conductance_calculator import *
from math import *

import LS340, LS332, LS370, SRS830, DAC488, keithley2400
import time, os, errno
import numpy

class DataTaker(QThread):
    def __init__(self, parent=None):
        super(DataTaker, self).__init__(parent)
        self.path = None
        self.debug = False
        self.instr = 'VTI'
        self.meas = 'Bode Plot'
        
    def run(self):
        print "Acquiring Data..."
        self.setup()
        
        measurement = {'Bode Plot': self.bodePlot,
                       'Wire Conductance':self.wireCond,
                       'Temperature Sweep':self.tempSweep,
                       'Four Wire':self.fourWire}
                       
        measurement[self.meas]()
        
    def setup(self):
        '''
        This is the setup function which intializes the instruments and values
        which will be read. Opens data file.
        '''
        print "Initializing Instruments..."
        
        self.instrumentSelect()
        
        self.stop = False
        
        time.sleep(1)
        
        print "Initialization Complete"
        
    def bodePlot(self):
        '''
        This is where the control logic of the program goes. Loops, parameter
        changes and if statements should be located here.
        '''
        self.data_file = open (self.path,'w')
        self.headers = ['Frequency(hz)', 'x-Value', 'y-Value', 'Amplitude(dB)', 'Phase(deg)']
        self.emit(SIGNAL("list(PyQt_PyObject)"), self.headers)
        
        stri = self.list2tabdel(self.headers)
        self.data_file.write(stri)
        
        frequencies = numpy.logspace(1,5,100)
        n = len(frequencies)
        self.lockin1.set_freq(frequencies[0])
        
        print 'Starting in...'
        self.printCountdown(3)
        # wait for things to stabilize

        self.ro = self.lockin1.read_input(3)
        
        for i in range(0,n-1):
            if self.stop == True:
                break
            self.lockin1.set_freq(frequencies[i])
            time.sleep(1)
            self.ReadFreqData(frequencies[i])
            
        self.data_file.close()
        
    def ReadFreqData(self,ctrlVar):
        '''
        This function reads the data, sends it to the GUI and writes it to the 
        file. The data should be sent with the x-value as the first number
        and all the dependent variables following. Make sure to include all
        the data you want (such as the calculated conductance)
        '''
        # The control variable which will be written as the first column        
        freq = ctrlVar
        
        # Read the various Values
        xValue = float(self.lockin1.read_input(1))
        yValue = float(self.lockin1.read_input(2))
        rValue = float(self.lockin1.read_input(3))
        phase = float(self.lockin1.read_input(4)) 
        amp = self.amplitudeDB(rValue)
        
        # Compile values into a list
        dataPoint = [freq, xValue, yValue, amp, phase]
        
        # Convert to a string for writing to file
        stri = self.list2tabdel(dataPoint)
        self.data_file.write(stri)
        
        # Create a dictionary for the data point and send signal to GUI    
        dataDict = dict(zip(self.headers,dataPoint))
        self.emit(SIGNAL("data(PyQt_PyObject)"), dataDict)
        
    def wireCond(self):
        print 'Measuring Wire Conductance'
        self.data_file = open (self.path,'w')
        self.headers = ['Gate(V)', 'x-Value', 'y-Value', 'r-Value-1', 'Theta-Value-1', 'x-Value-2', 'y-Value-2', 'r-Value-2', 'Theta-Value-2', 'Conductance(2e^2/h)']
        self.emit(SIGNAL("list(PyQt_PyObject)"), self.headers)
        
        stri = self.list2tabdel(self.headers)
        self.data_file.write(stri)
        
        stepTime = .5
        max_gate = -2
        stepsize = 0.002
        windowlower = -1.6
        windowupper = -2.2
        windowstep = 0.0005
        gateVoltage = 0.0
        
        while gateVoltage > max_gate:
            if self.stop == True:
                break
            
            self.gate.set_voltage(gateVoltage)
            self.readCondData(gateVoltage)
        
            if (gateVoltage <= windowlower and gateVoltage >= windowupper):
                gateVoltage = gateVoltage - windowstep
            else:
                gateVoltage = gateVoltage - stepsize  
                
            time.sleep(stepTime)
        
        while gateVoltage < 0:
            if self.stop == True:
                break
            
            self.gate.set_voltage(gateVoltage)
            self.readCondData(gateVoltage)
        
            if (gateVoltage <= windowlower and gateVoltage >= windowupper):
                gateVoltage = gateVoltage + windowstep
            else:
                gateVoltage = gateVoltage + stepsize  
                
            time.sleep(stepTime)
            
        # Loop to slowly reduce gate
        
        if self.stop == True:        
            while gateVoltage < 0:
                gateVoltage += 0.001
                self.gate.set_voltage(gateVoltage)
                # 0.1 delay corresponds to 1:40 per volt (assuming 0.001 step)
                time.sleep(0.2)
                
        self.gate.set_voltage(0)
        print "Measurement Complete"
        self.data_file.close()
        
    def readCondData(self,ctrlVar):
        '''
        This function reads the data, sends it to the GUI and writes it to the 
        file. The data should be sent with the x-value as the first number
        and all the dependent variables following. Make sure to include all
        the data you want (such as the calculated conductance)
        '''
        # Read the various Values
        xValue1 = float(self.lockin1.read_input(1))
        xValue2 = float(self.lockin2.read_input(1))
        yValue1 = float(self.lockin1.read_input(2))
        yValue2 = float(self.lockin2.read_input(2))
        rValue1 = float(self.lockin1.read_input(3))
        rValue2 = float(self.lockin2.read_input(3))
        thetaValue1 = float(self.lockin1.read_input(4))
        thetaValue2 = float(self.lockin2.read_input(4))
        
        #temp = float(self.temp.read(9))
        gateVoltage = ctrlVar
        conductance = twopointcond(xValue1,50.5)
        
        # Compile values into a list
        dataPoint = [gateVoltage, xValue1, yValue1, rValue1, thetaValue1, xValue2, yValue2, rValue2, thetaValue2,conductance]
        
        # Convert to a string for writing to file
        stri = self.list2tabdel(dataPoint)
        self.data_file.write(stri)
        
        # Create a dictionary for the data point and send signal to GUI    
        dataDict = dict(zip(self.headers,dataPoint))
        self.emit(SIGNAL("data(PyQt_PyObject)"), dataDict)
        
    def fourWire(self):
                
        self.headers = ['Gate(V)', 'x-Value', 'y-Value',  'x-Value-2', 'y-Value-2', 'Temperature (K)', 'Conductance(2e^2/h)']
        self.emit(SIGNAL("list(PyQt_PyObject)"), self.headers)
        
        headerString = self.list2tabdel(self.headers)
        
        
        stepTime = 0.5
        max_gate = -2
        stepsize = 0.005
        windowlower = -1.5
        windowupper = -2.0
        windowstep = 0.005
        gateVoltage = 0.0
        DACoput = 0
        
        for wire in ['Wire1','Wire2','Wire3','Wire4']:
            self.data_file = open (self.path+wire+'.dat','w')
            self.data_file.write(headerString)
            DACoput += 1
            
            while gateVoltage > max_gate:
                if self.stop == True:
                    break
                
                self.gate.set_voltage(gateVoltage,DACoput)
                self.readCondData(gateVoltage)
            
                if (gateVoltage <= windowlower and gateVoltage >= windowupper):
                    gateVoltage = gateVoltage - windowstep
                else:
                    gateVoltage = gateVoltage - stepsize  
                    
                time.sleep(stepTime)
            
            while gateVoltage < 0:
                if self.stop == True:
                    break
                
                self.gate.set_voltage(gateVoltage,DACoput)
                self.readCondData(gateVoltage)
            
                if (gateVoltage <= windowlower and gateVoltage >= windowupper):
                    gateVoltage = gateVoltage + windowstep
                else:
                    gateVoltage = gateVoltage + stepsize  
                    
                time.sleep(stepTime)
                
            # Loop to slowly reduce gate
            
            if self.stop == True:        
                while gateVoltage < 0:
                    gateVoltage += 0.001
                    self.gate.setvoltage(gateVoltage,DACoput)
                    # 0.1 delay corresponds to 1:40 per volt (assuming 0.001 step)
                    time.wait(0.2)
                    
            self.gate.set_voltage(0,DACoput)
            
            self.data_file.close()
            self.emit(SIGNAL("clear(PyQt_PyObject)"))
            print 'Finished ' + wire
        
        
    def tempSweep(self):
        '''
        This script just monitors the instruments, generally for a temperature
        sweep, but it could be adapted to othe purposes fairly easily
        '''
        self.data_file = open (self.path,'w')
        self.headers = ['Temperature-A (K)', 'Temperature-B (K)','x-Value', 'y-Value',  'x-Value-2', 'y-Value-2','Time(s)']
        self.emit(SIGNAL("list(PyQt_PyObject)"), self.headers)
        
        stri = self.list2tabdel(self.headers)
        self.data_file.write(stri)
        
        self.t_start = time.time()
        timestep = 1 #(s)
        temperatures = [self.temp.read('a'),self.temp.read('b')]
        
        while temperatures[1]>1.8:
            temperatures = self.readTempData()
            step = step+1
            #Wait until the enxt timestep
            while (time.time()-t_start)<step:
                wait=1
                
    
    def readTempData(self):
        t = float(time.time() - self.t_start)
        xValue1 = float(self.lockin1.read_input(1))
        xValue2 = float(self.lockin2.read_input(1))
        yValue1 = float(self.lockin1.read_input(2))
        yValue2 = float(self.lockin2.read_input(1))
        # gate = gate
        temperatureA = float(self.temp.read('a'))
        temperatureB = float(self.temp.read('b'))
        dataPoint = [temperatureA, temperatureB, xValue1, yValue1, xValue2, yValue2, t]
        
        # Convert to a string for writing to file
        stri = self.list2tabdel(dataPoint)
        self.data_file.write(stri)
        
        # Create a dictionary for the data point and send signal to GUI    
        dataDict = dict(zip(self.headers,dataPoint))
        self.emit(SIGNAL("data(PyQt_PyObject)"), dataDict)
        
        # return temperatures since they are the control variables
        return [temperatureA,temperatureB]
        
    def measurementRecord(self):
        '''
        This function is intended to save all the parameters and notes
        associated with the measurement. Values such as the lockin settings,
        time, date and equipment.
        '''
        self.measurement_record = open (self.path+'_record.dat','w')
                
        
    def instrumentSelect(self):
        
        instrDict = {
        'VTI' : self.VTI_instr,
        'He3' : self.He3_instr,
        'Dilution' : self.dil_instr,
        'Custom' : self.custom_instr,
        'Debug': self.debug_instr
        }
        print 'Selecting Instruments'     
        
        instrDict[self.instr](self.debug)
                
    def VTI_instr(self,debug=False):
        print "Initializing VTI Instruments..."
        self.lockin1 = SRS830.SRS830('GPIB1::14',debug)
        self.lockin2 = SRS830.SRS830('GPIB1::8',debug)
        self.gate = DAC488.DAC488('GPIB0::10',debug)
        self.gate.set_range(4,1) # up to 10V
        self.gate.set_range(4,2) # up to 10V 
        self.gate.set_range(4,3) # up to 10V 
        self.gate.set_range(4,4) # up to 10V 
        self.temp = LS332.LS332('GPIB1::12',debug)
        
    def He3_instr(self,debug=False):
        print "Initializing He3 Instruments..."
        self.lockin1 = SRS830.SRS830('GPIB0::8',debug)
        self.lockin2 = SRS830.SRS830('GPIB0::16',debug)
        self.gate = DAC488.DAC488('GPIB0::10',debug)
        self.gate.set_range(4,1) # up to 10V 
        self.temp = LS340.LS340('GPIB0::12',debug)
    
    def dil_instr(self,debug=False):
        '''
        Dilution Fridge Instruments
        '''
        print "Initializing Dil Instruments..."
        self.lockin1 = SRS830.SRS830('GPIB0::8',debug)
        self.lockin2 = SRS830.SRS830('GPIB0::10',debug)
        self.gate = keithley2400.device('GPIB0::24',debug)
        #self.temp = LS370.LS370('GPIB0::12',debug)
        
    def custom_instr(self,debug=False):
        '''
        Custom Instrument Setup
        '''
    def debug_instr(self,debug=True):
        '''
        debug 
        '''
        debug = True
        
        print "Initializing Debug Instruments..."
        self.lockin1 = SRS830.SRS830('GPIB1::14',debug)
        self.lockin2 = SRS830.SRS830('GPIB1::8',debug)
        self.gate = keithley2400.device('GPIB1::24',debug)
        self.gate.enable_output()
        self.temp = LS332.LS332('GPIB1::12',debug)
        
    def amplitudeDB(self,r):
        amp = 20*log10(r/self.ro)
        return amp
    
    def list2tabdel(self,values):
        stri = ''
        for i in values:
            stri = stri + str(i) +'\t'
        stri = stri + '\n'
        return stri
        
    def printCountdown(self,seconds):
        for s in range(seconds):
            print seconds-s
            time.sleep(1)
            
    def safeStop(self):
        self.stop = True
   
        print "Safely shutting down instruments..."