#!/usr/bin/env python  
import visa 
import string, os, sys, time  

class HP34401A:  
    def __init__(self, name, debug=False):  
        self.debug = debug
        if self.debug == False:
            self.inst = visa.instrument(name) 
        else:
            self.inst = None
            
    def read_voltage_DC(self):  
        if self.debug == False:
            string_data = self.inst.ask(':MEAS:VOLT:DC?')
            return float(string_data)
        else:
            return 123.4

    def read_voltage_AC(self):  
        if self.debug == False:
            string_data = self.inst.ask(':MEAS:VOLT:AC?')
            return float(string_data)
        else:
            return 123.4

    def read_current_DC(self):  
        if self.debug == False:
            string_data = self.inst.ask(':MEAS:CURR:DC?')
            return float(string_data)
        else:
            return 123.4

    def read_current_AC(self):  
        if self.debug == False:
            string_data = self.inst.ask(':MEAS:CURR:AC?')
            return float(string_data)
        else:
            return 123.4            
            
    def read(self):
        if self.debug == False:
            return self.inst.read()
        else:
            return 123
    
    def ask (self, stri):
        if self.debug == False:
            return self.inst.ask(stri)
        else:
            return 123
    def write(self, stri):
        if self.debug == False:
            return self.inst.write(stri)

    def close(self):
        if self.debug == False:
            self.inst.close()  

        
    #if run as own program  
    #if (__name__ == '__main__'):  
      
     #   lockin = device('dev9')  
     #   lockin.set_ref_internal  # no averaging
     #   lockin.close()  
