#!/usr/bin/env python  
from visa import *
import string, os, sys, time  
      
class device:  
    def __init__(self, name):  
        self.name = instrument(name)  
        srs = self.name 
      
    def set_ref_internal(self):  
        srs = self.name  
        srs.write('FMOD 1')
        
    def set_ref_external(self):  
        srs = self.name 
        srs.write('FMOD 0')

    def set_phase(self, shift):
        srs = self.name 
        srs.write ('PHAS ' + str(shift))
        
    def set_amplitude(self, amplitude):
        srs = self.name
        srs.write('SLVL' + str(amplitude))
        
    def get_amplitude(self):
        srs = self.name
        return srs.ask('SLVL?')

    def set_freq(self, freq):
        srs = self.name
        srs.write ('FREQ ' + str(freq))

    def get_freq(self):
        srs = self.name 
        return srs.ask ('FREQ?')
    
    def set_harm(self, harm):
        srs = self.name 
        srs.write ('HARM ' + str(harm))

    def set_ref_out(self, voltage):
        srs = self.name 
        srs.write ('SLVL ' + str(voltage))
        
    def get_ref_out(self, voltage):
        srs = self.name 
        srs.write ('SLVL?')
        return self.read()        
                    
    def read_aux (self, num):
        srs = self.name 
        srs.write ('OAUX? ' + str(num))
        return float(self.read())
    
    def read_input (self, num):
        srs = self.name 
        return  srs.ask ('OUTP? ' + str(num))

    def close(self):  
        self.srs.close()  


    #if run as own program  
    #if (__name__ == '__main__'):  
      
     #   lockin = device('dev9')  
     #   lockin.set_ref_internal  # no averaging
     #   lockin.close()  
