#!/usr/bin/env python  
import visa 
import string, os, sys, time  

class HP4263B:  
    def __init__(self, name, debug_mode=False):  
        self.debug_mode = debug_mode
        if self.debug_mode == False:
            self.inst = visa.instrument(name) 
        else:
            self.inst = None
            
    def trigger(self):  
        if self.debug_mode == False:
            self.inst.write(':TRIG:IMM')

    def read_data(self):  
        if self.debug_mode == False:
            string_data = self.inst.ask(':FETC?')
            list_data = string.split(string_data, ',')
            return float(list_data[2])
        else:
            return 123.4
                
    def set_trigger_bus(self):
        if self.debug_mode == False:
            self.inst.write (':TRIG:SOUR BUS')
  
    def set_comparator(self, state):
        if self.debug_mode == False:
            if state==True:         
                self.inst.write(':CALC1:LIM:STAT ON')
                self.inst.write(':CALC2:LIM:STAT ON')
            else:
                self.inst.write(':CALC1:LIM:STAT OFF')
                self.inst.write(':CALC2:LIM:STAT OFF')

    def read(self):
        if self.debug_mode == False:
            return self.inst.read()
        else:
            return 123
    
    def ask (self, stri):
        if self.debug_mode == False:
            return self.inst.ask(stri)
        else:
            return 123
    def write(self, stri):
        if self.debug_mode == False:
            return self.inst.write(stri)

    def close(self):
        if self.debug_mode == False:
            self.inst.close()  

    def raw_to_mK(self,raw_value):
        return -4.36894/(-raw_value*1000+2.93629)
        
    #if run as own program  
    #if (__name__ == '__main__'):  
      
     #   lockin = device('dev9')  
     #   lockin.set_ref_internal  # no averaging
     #   lockin.close()  
