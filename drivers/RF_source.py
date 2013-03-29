#!/usr/bin/env python  

'''
class to talk to SCPI-compliant RF sources. Tested on Agilent E4400B
'''

import visa 

class RF_source:  
    def __init__(self, name, debug_mode=False):  
        self.debug_mode = debug_mode
        if self.debug_mode == False:
            self.inst = visa.instrument(name) 
            print self.get_ID()
            
            self.POW_MIN = self.inst.ask(':SOUR:POW? MIN')
            self.POW_MAX = self.inst.ask(':SOUR:POW? MAX')
        else:
            self.inst = None
    
    def get_ID(self):
        if self.debug_mode == False:        
            return self.inst.ask('*IDN?')
        
    def set_freq(self, freq):
        if self.debug_mode == False:
            self.inst.write(':SOUR:FREQ:CW ' + str(freq))        

    def set_power(self, power):
        if self.debug_mode == False:
            self.inst.write(':POW:LEV:IMM:AMPL ' + str(power))  

    def close(self):
        if self.debug_mode == False:
            self.inst.close()  
        
    #if run as own program  
    #if (__name__ == '__main__'):  
      
     #   lockin = device('dev9')  
     #   lockin.set_ref_internal  # no averaging
     #   lockin.close()  
