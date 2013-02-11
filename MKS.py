import time
import serial
#!/usr/bin/env python  
import string, os, sys, time  
import io
      
class MKS_gauge:  
    def __init__(self, port='/dev/ttyUSB0', debug=False):  
        self.debug = debug
        if not debug:
            self.ser = serial.Serial(
                port,
                baudrate=9600,
                parity=serial.PARITY_EVEN,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.SEVENBITS,
                timeout=1 )
            #self.sio = io.TextIOWrapper(io.BufferedRWPair(self.ser,self.ser))
            self.sio = self.ser
  
    def get_pressure(self, chan):
        if not self.debug:
            if chan==1:
                self.write('@6011?')
            elif chan==2:
                self.write('@6012?')
            else:
                return None        
            return self.sio.read(13)
        else:
            return 1.23e-3
            
    def write(self, stri):
        if not self.debug:     
            self.sio.write(stri + '\r\n')            

    def readline(self):
        if not self.debug:     
            return self.sio.readline()
    
    def read2(self):
         if not self.debug:     
             sio = self.sio
             time.sleep(0.1)
             out=''
             while sio.inWaiting() > 0:
                 out += sio.read(1)
             return (out)

    #initialization should open it already    
    def reopen(self):
         if not self.debug:
             self.ser.open()
        
    def close(self):  
         if not self.debug:
             self.sio.close() 
