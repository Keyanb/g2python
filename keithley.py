# -*- coding: utf-8 -*-
"""
Created on Wed May 16 16:22:26 2012
Keithley 2400
@author: Bram
"""

#!/usr/bin/env python  
from visa import *  
import string, os, sys, time  
      
class device:  
    def __init__(self, name):  
        self.name = instrument(name)
        k2400 = self.name
        print k2400.ask('*IDN?')
        # Should Read KEITHLEY INSTRUMENTS INC., MODEL nnnn, xxxxxxx, yyyyy/zzzzz /a/d
        
    def reset(self):  
        k2400 = self.name
        k2400.write('*RST')
        time.sleep(1)
        # Resets the instrument

    def operation_complete(self):
        k2400 = self.name
        k2400.write ('*OPC')
        # Returns a 1 after all the commands are complete

    def configure_measurement(self,sensor):
        #VOLT,CURR RES
        k2400 = self.name
        s = ':%s:RANG:AUTO ON' % sensor
        print(s)
        k2400.write (s)
    
    def configure_voltage_source(self):
        k2400 = self.name
        k2400.write(':SOUR:FUNC:MODE VOLT')
    
    def set_current_compliance(self,compliance):
        k2400 = self.name
        k2400.write(':SENS:CURR:PROT:LEV '+ str(compliance))

    def configure_output(self, source_mode = 'VOLT' , output_level = 0, compliance_level = 0.001):
        # source_mode: VOLT, CURR
        # output_level: in Volts or Amps
        # compliance level: in Amps or Volts
        
        if source_mode == 'CURR':
            protection = 'VOLT'
        else:
            protection = 'CURR'
            
        k2400 = self.name
        s = ':SOUR:FUNC %s;:SOUR:%s %f;:%s:PROT %r;' % (source_mode, source_mode, output_level, protection, compliance_level)
        k2400.write(s)
        
    
    def enable_output(self):
        k2400 = self.name
        k2400.write (':OUTP ON;')
        
    def disable_output(self):
        k2400 = self.name
        k2400.write (':OUTP OFF;')        
        
    def set_voltage(self, voltage):
        k2400 = self.name
        s = ':SOUR:FUNC VOLT;:SOUR:VOLT %f;:CURR:PROT 5E-5;' % voltage
        k2400.write (s)
    
    def configure_multipoint(self,sample_count=1,trigger_count=1,output_mode='FIX'):
        k2400 = self.name
        s = ':ARM:COUN %d;:TRIG:COUN %d;:SOUR:VOLT:MODE %s;:SOUR:CURR:MODE %s;' % (sample_count,trigger_count,output_mode,output_mode)
        k2400.write(s)
        
    def configure_trigger(self,arming_source='IMM',timer_setting=0.01,trigger_source='IMM',trigger_delay=0.0):
        # arming source: IMM,BUS,TIM,MAN,TLIN,NST,PST,BST  
            # Immediate Arming
            # Software Trigger Signal
            # Timer (set with <B>Timer Setting</B>)
            # Manual (pressing the TRIG button on the instrument)
            # Rising SOT Pulse
            # Falling SOT Pulse
            # Any SOT Pulse
        # trigger source: IMM,TLIN
        # timer setting: interval of time to wait before arming the trigger
        # trigger delay: the time to wait after the trigger has been
        k2400 = self.name
        s = ':ARM:SOUR %s;:ARM:TIM %f;:TRIG:SOUR %s;:TRIG:DEL %f;' % (arming_source,timer_setting,trigger_source,trigger_delay)
        k2400.write(s)
    
    def initiate(self):
        # Clears the trigger, then initiates
        k2400 = self.name
        s = ':TRIG:CLE;:INIT;'
        k2400.write(s)
        time.sleep(0.01)
        # delay to replace OPC
        
    def wait_for_OPC(self):
        k2400 = self.name
        k2400.write('*OPC;')
        
    def fetch_measurements(self):
        k2400 = self.name
        print k2400.ask(':FETC')
        
    def standard_setup(self):
        k2400 = self.name
        self.reset()
        self.configure_measurement('VOLT')
        self.configure_measurement('CURR')
        self.configure_measurement('RES')
        self.configure_output('VOLT',0,0.00005)
        self.enable_output()
        
    def close(self):
        k2400 = self.name
        self.disable_output()
        k2400.write('*RST')
        k2400.write('*CLS')
        k2400.write(':*SRE 0')

