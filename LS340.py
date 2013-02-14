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
        lak340 = self.name
        print lak340.ask('*IDN?')
    
    def read(self, input):
        lak340 = self.name
        return lak340.ask('SRDG?'+str(input))