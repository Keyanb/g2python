#!/usr/bin/env python  

import visa  
      
class IPS120:  
    def __init__(self, name, debug=False, read_only = False):
        self.debug = debug

        self.read_only = read_only
        
        if self.debug == False:
            self.ips = visa.instrument(name, term_chars = visa.CR)

            if self.read_only == False:
                self.set_extended()
            
            print (self.read_status())

    def unlock (self):
        if self.debug == False:
            return self.ips.ask('@0C3\r')

    def set_field_sweep_rate(self, rate):
        if self.debug == False:        
            if rate <= 0.20 and rate >0:        
                return self.ips.ask('@0T%.4f\r' % rate)
            else:
                return "set rate too fast"
                
    def set_point_field(self, val):
        if self.debug == False:      
            if val >=-9 and val <=9:
                return self.ips.ask('@0J%.4f\r'%val)
            
    def hold(self):
        if self.debug == False:      
            return self.ips.ask('@0A0\r')

    def goto_set(self):
        if self.debug == False:      
            return self.ips.ask('@0A1\r')

    def goto_zero(self):
        if self.debug == False:      
            return self.ips.ask('@0A2\r')
                                   
    def read_param (self, param):
        if self.debug == False:      
            return self.ips.ask ('@0R' + str(param) + '\r')  
        
    def read_field (self):
        if self.debug == False:      
            return float(self.ips.ask('@0R7\r').lstrip('R')) 
        else:
            return 0

    def read_status (self):
        if self.debug == False:      
            return self.ips.ask ('@0X\r')  

    def set_extended (self):
        if self.debug == False:      
            return self.ips.write ('@0Q4\r')

    def close(self):   
        if self.debug == False:
            self.ips.close()  


    #if run as own program  
    #if (__name__ == '__main__'):  
      