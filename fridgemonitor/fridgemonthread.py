# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 17:42:35 2013

@author: Ben
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import LS370
import HP4263B
import MKS
import time


class FridgeMonThread(QThread):    
    def __init__(self, lock, parent=None):
        super(FridgeMonThread, self).__init__(parent)
        self.lock = lock
        self.stopped = True
        self.completed = False

    def initialize(self, debug):
        self.debug = debug
        self.active_channels = [1,2,3,4,5,9]
        
        self.lakeshore = LS370.LS370('GPIB::12', self.debug)
        self.CMN = HP4263B.HP4263B('GPIB::17', self.debug)
        self.pirani = MKS.MKS_gauge('COM3', self.debug) #'/dev/ttyUSB0'
        
        self.TIME_STEP = 10

    def run(self):
        self.stopped = False
        self.main_loop()
        self.stop()
        self.emit(SIGNAL("finished(bool)"), self.completed)        
        
    
    def stop(self):
        self.stopped = True

    def isStopped(self):
        return self.stopped
        
    def main_loop(self):
        while self.isStopped() == False:         
            self.CMN.trigger()
            
            for chan in self.active_channels:
                self.lakeshore.scanner_to_channel(chan)
                time.sleep(self.TIME_STEP)
                dat = self.lakeshore.read_channel(chan)
                
                self.emit(SIGNAL("data(PyQt_PyObject)"), ['LS370', chan, dat])                 
                
                while self.isStopped() == True:
                    break
            
            CMN_temp = self.CMN.read_data()
            self.emit(SIGNAL("data(PyQt_PyObject)"), ['CMN', 0, dat])


    def clean_up(self):
        pass
