# -*- coding: utf-8 -*-
"""
Created on Tue May 22 09:51:19 2012
Driver for DAC488
@author: Bram
"""

from visa import *  
import string, os, sys, time, threading
      
class DAC488:  
    def __init__(self, name, debug = False):
        self.debug = debug
        if self.debug == False:
            self.name = instrument(name)
            self.currentVoltage = 0
            self.name.write('*RX')
            time.sleep(2)

        
    def set_range(self,vrange,port=1):
        if self.debug == False:
            dac488 = self.name
            dac488.write('P'+str(port)+'X')
            dac488.write('R'+str(vrange)+'X')
            # vrange does not mean the literal voltage range!!!
            # 1,2,3,4 correspond to 1V, 2V, 5V, 10V bipolar
        
    def set_voltage(self,voltage,port=1):
        if self.debug == False:
            dac488 = self.name
            self.currentVoltage = voltage
            dac488.write("P" + str(port))
            dac488.write("V" + str(voltage))
            dac488.write("X")
        
    def error_query(self):
        if self.debug == False:
            dac488 = self.name
            return dac488.ask('E?X')
        
    def reset(self):
        if self.debug == False:
            dac488 = self.name
            dac488.write('DCL')
                
        
        