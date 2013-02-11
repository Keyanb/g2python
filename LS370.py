#!/usr/bin/env python  
import visa

import string, os, sys, time  
      
class LS370:  
    def __init__(self, name, debug=False):  
        self.debug = debug
        if debug==True:
            self.ls = None
        else:
            self.ls = visa.instrument(name)  

    def read_channel (self, chan):
        if self.debug == False:        
            self.write ('RDGR? ' + str(chan))      
            data = self.read()
            if data =="":
                return 0
            else:
                return float(data)
        else:
            return 1337.0
    
    def set_heater_range(self, htr_range):
        if self.debug == False:    
            if htr_range >= 0 and htr_range < 9:
                self.write('HTRRNG %d'%htr_range)
    
    def set_heater_output(self, percent):
        if self.debug == False:          
            if percent >= 0 and percent <= 100:
                self.write('MOUT %.3f'%percent)
    
    def auto_scan (self):
        if self.debug == False:        
            self.write('SCAN 1,1')

    def scanner_to_channel(self, chan):
        if self.debug == False:
            self.write('SCAN %d,0'%chan)

        
    #lower level commands start here
      
    def read(self):  
        if self.debug == False:
            return self.ls.read() 

    def write(self,stri):  
        if self.debug == False:
            self.ls.write(str(stri))  
      
    def close(self):  
        if self.debug == False:
            self.ls.close()  


    #if run as own program  
    #if (__name__ == '__main__'):  
      
     #   lockin = device('dev9')  
     #   lockin.set_ref_internal  # no averaging
     #   lockin.close()  
