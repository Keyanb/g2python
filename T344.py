import time
import serial
#!/usr/bin/env python  
import string, os, sys, time  
      
class T344:  
    def __init__(self, name):  
        self.ser = serial.Serial(
        port='COM1',
        baudrate=38400,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
        )
        ser = self.ser
        ser.isOpen()
        # send the character to the device
        # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
        self.write(' ')
        out = ''
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        while ser.inWaiting() > 0:
            out += ser.read(1)
        if out != '':
            print ">>" + out 

    def get_status(self):
        self.write('ST')
        return self.readline()

    def sync(self):
        self.write('SYNC')
        return self.readline()

    def set_freq(self, chan, val):
        self.write(str(chan) + 'FREQ ' + str(val))
        return self.readline()

    def set_freq_raw(self, chan, val):
        self.write(str(chan) + 'RAW ' + str(val))
        return self.readline()

    def set_amp(self, chan, val):
        self.write(str(chan) + 'AMP ' + str(val))
        return self.readline()

    def set_phase(self, chan, val):
        self.write(str(chan) + 'PHASE ' + str(val))
        return self.readline()

    def set_DC(self, chan, val):
        self.write(str(chan) + 'DC ' + str(val))
        return self.readline()  
    
    def write(self, stri):
        ser = self.ser
        ser.write(stri + '\r\n')            

    def readline(self):
        ser = self.ser
        return ser.readline()
    
    def read2(self):
        ser = self.ser
        time.sleep(0.1)
        out=''
        while ser.inWaiting() > 0:
            out += ser.read(1)
        return (out)

    #initialization should open it already    
    def reopen(self):
        self.ser.open()
        
    def close(self):  
        self.ser.close() 
