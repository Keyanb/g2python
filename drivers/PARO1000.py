# -*- coding: utf-8 -*-
"""
Created on Wed May 08 13:31:59 2013
Paroscientific Digiquartz Pressure sensor 1000 Driver
@author: Bram
"""
from visa import *
import string, os, sys, time, random
      
class PARO1000:  
    def __init__(self, name, debug=False): 
        self.debug = debug
        if self.debug == False:
            self.name = instrument(name, term_chars = '\r\n')
            paro = self.name
            print paro.ask('*0100MN')
            

    def read(self):
        if self.debug == False:
            paro = self.name
            pressureResult = paro.ask('*0100P3')
            return float(pressureResult[5:]) #remove the first 5 characters
        else:
            return random.random()
            
    def close(self):   
        if self.debug == False:
            self.paro.close()