#!/usr/bin/env python  
from GPIB import *  
import string, os, sys, time  
      
class LS370:  
    def __init__(self, name):  
        self.ls = Gpib(name)  
        ls = self.ls 

    def read_channel (self, chan):
        self.write ('RDGR? ' + str(chan))      
        data = self.read()
        if data =="":
            return 0
        else:
            return float(data)
    
    def auto_scan (self):
        self.write('SCAN 1,1')

    def scanner_to_channel(self, chan):
        self.write('SCAN %d,0'%chan)

        
    #lower level commands start here
      
    def read(self,num=512):  
        ''''' Use only for text data. '''  
        ls = self.ls
        a = ls.read(num)  
        return a  
  
    def readb(self,num=512):  
        ''''' Use to read binary data. This prevents early termination 
            from a \0. '''  
        srs = self.srs  
        a = ls.readb(num)  
        return a  
      
    def write(self,stri):  
        ls = self.ls  
        ls.write(str(stri))  
      
    def close(self):  
        self.ls.close()  


    #if run as own program  
    #if (__name__ == '__main__'):  
      
     #   lockin = device('dev9')  
     #   lockin.set_ref_internal  # no averaging
     #   lockin.close()  
