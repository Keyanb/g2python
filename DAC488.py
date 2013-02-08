# -*- coding: utf-8 -*-
"""
Created on Tue May 22 09:51:19 2012
Driver for DAC488
@author: Bram
"""

from visa import *  
import string, os, sys, time, threading
      
class device:  
    def __init__(self, name):  
        self.name = instrument(name)
        dac488 = self.name
        dac488.write('*RX')
        time.sleep(2)
        print dac488.ask('*IDN?')
        
    def set_range(self,port,vrange):
        dac488 = self.name
        dac488.write('P'+str(port)+'X')
        dac488.write('R'+str(vrange)+'X')
        # vrange does not mean the literal voltage range!!!
        # 1,2,3,4 correspond to 1V, 2V, 5V, 10V bipolar
        
    def set_voltage(self,port,voltage):
        dac488 = self.name
        dac488.write("P" + str(port))
        dac488.write("V" + str(voltage))
        dac488.write("X")
        
    def error_query(self):
        dac488 = self.name
        return dac488.ask('E?X')
        
    def reset(self):
        dac488 = self.name
        dac488.write('DCL')
                
        
        