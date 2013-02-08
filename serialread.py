# -*- coding: utf-8 -*-
"""
Created on Wed Aug 01 13:06:18 2012

@author: bram
"""

import serial

class device:
    def __init__(self,name):
        self.name = serial.Serial(2,115200)
        arudino = self.name
        
    def getTemp(self):
        arduino = self.name
        arduino.writeline('temp?')
        tempA = arudino.readline()
        tempB = arduino.readline()
        tempC = arudino.readline()
        print tempA + tempB + tempC