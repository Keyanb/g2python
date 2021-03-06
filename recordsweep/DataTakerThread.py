# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 21:52:15 2013

@author: Ben
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import SRS830, IPS120, LS370, HP4263B, HP34401A, LS340, PARO1000
import readconfigfile
import time
import numpy as np

class DataTakerThread(QThread):
    MEAS_TIME = 1      
    USING_MAGNET = True 
    
    def __init__(self, lock, parent=None):
        super(DataTakerThread, self).__init__(parent)
        self.lock = lock
        self.stopped = True
        self.mutex = QMutex()
        self.completed = False
        self.DEBUG = readconfigfile.get_debug_setting()

    def initialize(self, name_list, type_list, dev_list, param_list):     
        self.stopped = True
        self.completed = False     
        self.t_start = time.time()
   
        # tuple: lockin #, channel, subplot for display
        self.data_channels = []        
        self.instruments = {}
        self.instrument_types = {}

        for name, instr_type, dev, param in zip(name_list, type_list, dev_list, param_list):
            if name:
                # add instrument to list if not there
                if not dev in self.instruments:
                    if instr_type == 'SRS830':               
                        self.instruments[dev] = SRS830.SRS830(dev, debug=self.DEBUG)
                    elif instr_type == 'HP34401A':               
                        self.instruments[dev] = HP34401A.HP34401A(dev, debug=self.DEBUG)                        
                    elif instr_type == 'IPS120':
                        self.instruments[dev] = IPS120.IPS120(dev, debug=self.DEBUG)  
                        self.instruments[dev].ips.clear()
                    elif instr_type == 'LS340':               
                        self.instruments[dev] = LS340.LS340(dev, debug=self.DEBUG)
                    elif instr_type == 'PARO1000':               
                        self.instruments[dev] = PARO1000.PARO1000(dev, debug=self.DEBUG) 
                    self.instrument_types[dev] = instr_type
                else:
                    if instr_type != self.instrument_types[dev]:
                        print ("Same GPIB port specified for different instruments! ")
                        print (dev + " " + instr_type + " " + self.instrument_types[dev])
                        instr_type = 'NONE'                        
    
                if instr_type == 'TIME':
                    command = lambda: time.time() - self.t_start
                elif instr_type == 'IPS120':
                    if param == 'FIELD':
                        command = lambda d=dev: self.instruments[d].read_field()
                elif instr_type == 'SRS830':
                    if param =='X':
                        command = lambda d=dev: self.instruments[d].read_input(1)
                    elif param =='Y':
                        command = lambda d=dev: self.instruments[d].read_input(2)
                    elif param =='R':
                        command = lambda d=dev: self.instruments[d].read_input(3)    
                    elif param =='PHASE':
                        command = lambda d=dev: self.instruments[d].read_input(4)
                    elif param =='AUX_1':
                        command = lambda d=dev: self.instruments[d].read_aux(1)
                    elif param =='AUX_2':
                        command = lambda d=dev: self.instruments[d].read_aux(2)
                    elif param =='AUX_3':
                        command = lambda d=dev: self.instruments[d].read_aux(3)
                    elif param =='AUX_4':
                        command = lambda d=dev: self.instruments[d].read_aux(4)
                        
                elif instr_type == 'HP34401A':
                    if param =='V_DC':
                        command = lambda d=dev: self.instruments[d].read_voltage_DC()
                    elif param =='V_AC':
                        command = lambda d=dev: self.instruments[d].read_voltage_AC()
                elif instr_type == 'LS340':
                    if param == 'A':
                        command = lambda d=dev: self.instruments[d].kread('A')
                    elif param =='B':
                        command = lambda d=dev: self.instruments[d].kread('B')
                    elif param =='C':
                        command = lambda d=dev: self.instruments[d].read('C')   
                    elif param =='D':
                        command = lambda d=dev: self.instruments[d].read('D')                         
                
                elif instr_type == 'PARO1000':
                    if param == 'PRESSURE':
                        command = lambda d=dev: self.instruments[d].read()
                    
                elif instr_type == 'None':
                    command = lambda: 0
            else:
                command = lambda: 0
                    
            self.data_channels.append(command)

        
    def run(self):
        self.stopped = False
        self.main_loop()
        self.stop()
        self.emit(SIGNAL("finished(bool)"), self.completed)        
        
    
    def stop(self):
        try:
            self.mutex.lock()
            self.stopped = True
        finally:
            self.mutex.unlock()

    def isStopped(self):
        try:
            self.mutex.lock()
            return self.stopped
        finally:
            self.mutex.unlock()    
    
    def main_loop(self):
        while self.isStopped() == False:
            data_set = [command() for command in self.data_channels]            
            self.emit(SIGNAL("data(PyQt_PyObject)"), np.array(data_set))              
            time.sleep(self.MEAS_TIME)            

    def clean_up(self):
        for inst in self.instruments:
            inst.close()      