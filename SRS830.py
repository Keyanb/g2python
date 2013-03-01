#!/usr/bin/env python  
from visa import *
import string, os, sys, time, random  
      
class SRS830:  
    def __init__(self, name, debug = False):  
        self.name = name
        self.debug = debug
        
        if self.debug == False:
            self.srs = instrument(name)        
            print self.srs.ask('*IDN?')
            
    def set_scale(self, scale):
        if self.debug == False:
            self.srs.write('SENS ' + str(scale))
            
    def set_ref_internal(self):  
        if self.debug == False:
            self.srs.write('FMOD 1')
        
    def set_ref_external(self):  
        if self.debug == False:
            self.srs.write('FMOD 0')

    def set_phase(self, shift):
        if self.debug == False:        
            self.srs.write ('PHAS ' + str(shift))
     
    def set_amplitude(self, amplitude):
        if self.debug == False:        
            srs = self.name
            srs.write('SLVL' + str(amplitude))
        
    def get_amplitude(self):
        if self.debug == False:
            srs = self.name
            return srs.ask('SLVL?')

    def set_freq(self, freq):
        if self.debug == False:
            self.srs.write ('FREQ ' + str(freq))

    def get_freq(self):
        if self.debug == False:
            self.srs.write ('FREQ?')
            return self.srs.read() 
   
    def set_harm(self, harm):
        if self.debug == False:
            self.srs.write ('HARM ' + str(harm))

    def set_ref_out(self, voltage):
        if self.debug == False:
            self.srs.write ('SLVL ' + str(voltage))
        
    def get_ref_out(self, voltage):
        if self.debug == False:
            self.srs.write ('SLVL?')
            return self.srs.read()        
        else:
            return 1.234
               
    def read_aux (self, num):
        if self.debug == False:
            self.srs.write ('OAUX? ' + str(num))
            return float(self.srs.read())
        else:
            return 1.234     
    
    def set_aux_out(self, chan, volts):
        if self.debug == False:        
            self.srs.write ('AUXV ' + str(chan) + ", " + str(volts))       
    
    def read_input (self, num):
        if self.debug == False:
            self.srs.write ('OUTP? ' + str(num))
            return float(self.srs.read())    
        else:
            return 1.23e-4 * random.random()

    def close(self):  
        self.srs.close()  


    #if run as own program  
    #if (__name__ == '__main__'):  
      
     #   lockin = device('dev9')  
     #   lockin.set_ref_internal  # no averaging
     #   lockin.close()  
