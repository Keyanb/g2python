# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 16:30:18 2012
Driver for N5700 series power supply
@author: bram
"""

from visa import *
import string, os, sys, time  

class device:  
    def __init__(self, name):  
        self.name = instrument(name)
        n5700 = self.name
        print n5700.ask('IDN?')
    
    def setVoltage(self, input):
        n5700 = self.name
        n5700.write('VOLT'+str(input))
        
    def setCurrent(self, input):
        n5700 = self.name
        n5700.write('CURR'+str(input))
        
    def setOverVoltage(self,input):
        n5700 = self.name
        n5700.write('VOLT:PROT:LEV'+str(input))
        
    def setOverCurrent(self,input):
        n5700 = self.name
        n5700.write('CURR:PROT:LEV'+str(input))
        
    def outputOn(self):
        n5700 = self.name
        n5700.write('OUTP ON')
        time.sleep(0.01)
        return n5700.ask('*OPC')
        
    def measureVoltage(self):
        n5700 = self.name
        return n5700.ask('Meas:Volt?')
        
    def checkError(self):
        n5700 = self.name
        return n5700.ask('Syst:err?')