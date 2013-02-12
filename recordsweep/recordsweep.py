# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 13:18:32 2012

@author: Benjamin Schmidt
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import ui_recordsweep
import LS370, HP4263B, MKS
import time
import threading
import chart_recorder as cr
import numpy as np
import SRS830
import IPS120
import readconfigfile
import string
from pylab import *

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class RecordSweepWindow(QMainWindow, ui_recordsweep.Ui_RecordSweepWindow):
    def __init__(self, parent=None):
        super(RecordSweepWindow, self).__init__()
        self.setupUi(self)

        self.lock = QReadWriteLock()         
        self.datataker = DataTaker(self.lock, self)  

        self.ax = self.mplwidget.axes
        self.fig = self.mplwidget.figure
        self.line = []
        
        #for idx, chan in enumerate(self.data_channels):
        #    tline, = self.ax.plot(0, 0, '.-')
        #    self.line.append(tline)          
            
        self.ax.tick_params(axis='x', labelsize=8)
        self.ax.tick_params(axis='y', labelsize=8)
        self.fig.canvas.draw()          

                     
                     
    @pyqtSignature("")
    def on_startStopButton_clicked(self):
        if self.datataker.isStopped():      
            self.datataker.initialize()            
            self.datataker.start()
            
            self.startStopButton.setText("Stop")
            print ("data taker started")             
        else:
            self.datataker.stop()
            self.startStopButton.setText("Start")
            print ("data taker stopped") 


class DataTaker(QThread):
    MEAS_TIME = 3      
    DEBUG = True       
    USING_MAGNET = True 
    
    def __init__(self, lock, parent=None):
        super(DataTaker, self).__init__(parent)
        self.lock = lock
        self.stopped = True
        self.mutex = QMutex()
        self.path = None
        self.completed = False

    def initialize(self, ):
        self.stopped = True
        self.completed = False     
        self.t_start = time.time()
        #instrumentation setup - store instrument objects in a dictionary by address
        self.instruments = {}
        self.instruments['GPIB::8'] = SRS830.SRS830('GPIB::8', debug=self.DEBUG)
        
        # tuple: lockin #, channel, subplot for display
        self.data_channels = []
        
        self.data_channels.append(['TIME', lambda: time.time() - self.t_start, []])
        if self.USING_MAGNET==True:
            self.magnet = IPS120.IPS120('GPIB::26', debug=self.DEBUG)
            self.data_channels.append(['FIELD', lambda:self.magnet.read_field(), []])
        self.data_channels.append(['X', lambda: self.instruments['GPIB::8'].read_input(1), []])
        self.data_channels.append(['Y', lambda: self.instruments['GPIB::8'].read_input(2), []])
             
        #open file, write header
        out_file = readconfigfile.open_data_file()

        out_file.write('Starting time: ' + str(self.t_start) + '\n')
        for chan in self.data_channels:        
            out_file.write(chan[0] + ", ")
        out_file.write('\n')
        

        
    def run(self):
        self.stopped = False
        self.main_loop()
        print ("yay")
        self.stop()
        self.emit(SIGNAL("finished(bool)"), self.completed)        
        
    
    def stop(self):
        try:
            self.mutex.lock()
            self.stopped = True
        finally:
            self.mutex.unlock()

    def isStopped(self):
        try:
            self.mutex.lock()
            return self.stopped
        finally:
            self.mutex.unlock()    
    
    def main_loop(self):
        print ("entered main loop")
        t_start = time.time()
        while self.isStopped() == False:
            stri = ""
            
            for chan in self.data_channels:
                stri = stri + "\t" + str(chan[1]())
            #out_file.write(stri)
            print stri
            
            time.sleep(self.MEAS_TIME)
            

    def clean_up(self):
        out_file.close()

        for inst in self.instruments:
            inst.close()
        
        if using_magnet==True:
            self.magnet.close()        
        
    def auto_scale_y(self,data):
        span = max(data.max() - data.min(), 0.1 * data.min())
        return (data.min() - span *0.05), (data.max() + span*0.05)
    
    def read_data(self, t_start, using_magnet):
        output_line = ""
        t_current= time.time() - t_start
    
        if using_magnet==True:
            current_field = self.magnet.read_field()
            output_line = output_line + "%.5f"%current_field
            self.fields = append(self.fields, current_field)
            
        #read 3 lock-ins
        for idx, chan in enumerate(self.data_channels):
            if chan[1] <5:
                dat = self.instruments[chan[0]].read_input(chan[1])
            else:
                dat = self.instruments[chan[0]].read_aux(chan[1]-4)
            
            output_line = output_line + ', %.6e'%dat
            
            chan[3] = append(chan[3],dat)
                     
            self.line[idx].set_data(arange(chan[3].size), chan[3])
    
            y1, y2 = self.auto_scale_y(chan[3])
            self.ax.set_ylim(ymin = y1, ymax = y2)
            self.ax.set_xlim(xmin=0, xmax = chan[3].size-1)
        self.fig.canvas.draw()
                     
        #output_line = output_line + str(lakeshore.read_channel(9))    
    
        return output_line

             
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = RecordSweepWindow()
    #form.connect(form, SIGNAL("found"), found)
    #form.connect(form, SIGNAL("notfound"), nomore)
    #form.plot([0,1,2,3,4], [0,1,2,3,])
    form.show()
    app.exec_()
