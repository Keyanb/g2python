# -*- coding: utf-8 -*-
"""
Created on Tue May 29 14:28:29 2012
Lakeshore 332 Driver
@author: Bram
"""
from visa import *
import string, os, sys, time  
      
class device:  
    def __init__(self, name):  
        self.name = instrument(name)
        lak332 = self.name
        print lak332.ask('*IDN?')
    
    def read(self, input):
        lak332 = self.name
        return lak332.ask('SRDG?'+str(input))