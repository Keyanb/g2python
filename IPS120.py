#!/usr/bin/env python  

import visa  
      
class IPS120:  
    def __init__(self, name, debug=False, read_only = False):
        self.debug = debug
        self.read_only = control
        
        if self.debug == False:
            self.ips = visa.instrument(name, term_chars = CR)
            if self.read_only == False:
                self.set_extended()
            
            print (self.read_status())

    def unlock (self):      
        return self.ips.ask('@0C3\r')

    def set_field_sweep_rate(self, rate):
        if rate <= 0.20 and rate >0:        
            return self.ips.ask('@0T%.4f\r' % rate)
        else:
            return "set rate too fast"
            
    def set_point_field(self, val):
        if val >=-9 and val <=9:
            return self.ips.ask('@0J%.4f\r'%val)
        
    def hold(self):
        return self.ips.ask('@0A0\r')

    def goto_set(self):
        return self.ips.ask('@0A1\r')

    def goto_zero(self):
        return self.ips.ask('@0A2\r')
                                   
    def read_param (self, param):
        return self.ips.ask ('@0R' + str(param) + '\r')  
        
    def read_field (self):
        return self.ips.ask ('@0R7\r')  

    def read_status (self):
        return self.ips.ask ('@0X\r')  

    def set_extended (self):
        return self.ips.ask ('@0Q4\r')

    def close(self):  
        if self.debug == False:
            self.ips.close()  


    #if run as own program  
    #if (__name__ == '__main__'):  
      