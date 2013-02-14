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
    MAX_CHANNELS = 6
    
    def __init__(self, parent=None):
        super(RecordSweepWindow, self).__init__()
        self.setupUi(self)
        self.customizeUi()
        
        self.lock = QReadWriteLock()         
        self.datataker = DataTaker(self.lock, self)  
        self.connect(self.datataker, SIGNAL("data(PyQt_PyObject)"),
                     self.updateData)

        # axes and figure initialization
        self.ax = self.mplwidget.axes
        self.fig = self.mplwidget.figure
        self.ax.tick_params(axis='x', labelsize=8)
        self.ax.tick_params(axis='y', labelsize=8)
        self.fig.canvas.draw()              
        
         # objects to hold line data

        #line1, = self.ax.plot(0, 1, '.r', )
        #line2, = self.ax.plot(0, 0, '-g')
        line_set = []
        for i in range (self.MAX_CHANNELS):            
            line1, = self.ax.plot(0, 1, '.r', )
            line_set.append(line1)
        
        self.ax.lines = line_set

        print self.ax.lines
        #self.lines = [DataLine(line1, 0, 2, '.'), DataLine(line2, 0, 3, '-')]
        
        self.data_array = array([])       
        self.chan_X = 0
        
    def customizeUi(self):
        
        self.radioButton_X = [] 
        
        for i in range (self.MAX_CHANNELS):                       
            self.radioButton_X.append(QRadioButton(self.groupBox_X))
            self.radioButton_X[i].setGeometry(QRect(10, 20*(i+1), 16, 16))
            self.radioButton_X[i].setText(_fromUtf8(""))
            self.radioButton_X[i].setObjectName(_fromUtf8("radioButton_" + str(i)))
            self.connect(self.radioButton_X[i], SIGNAL("toggled(bool)"), self.XRadioButtonHandler)       

        
        self.checkBox_Y = []
        
        for i in range (self.MAX_CHANNELS):          
            self.checkBox_Y.append(QCheckBox(self.groupBox_Y))
            self.checkBox_Y[i].setGeometry(QRect(10, 20 * (i+1), 16, 16))
            self.checkBox_Y[i].setText(_fromUtf8(""))
            self.checkBox_Y[i].setObjectName(_fromUtf8("checkBox_" +str(i)))  
            self.connect(self.checkBox_Y[i], SIGNAL("stateChanged(int)"), self.YCheckBoxHandler)       

    def XRadioButtonHandler(self):
        for num, box in enumerate(self.radioButton_X):
            if box.isChecked():
                self.chan_X = num
        self.updatePlot() 
        
    def YCheckBoxHandler(self):        
        for box in self.checkBox_Y:
            print box.isChecked()
        self.updatePlot()      
 
    def updateData(self, data_set):        
        if self.data_array.size == 0:
            self.data_array = data_set
            data_set.shape = [1, data_set.size]
        else:            
            self.data_array = vstack([self.data_array, data_set])
        self.updatePlot()

    def updatePlot(self): 
        for chan_Y, line in enumerate(self.ax.lines):
            if self.checkBox_Y[chan_Y].isChecked():
                line.set_data(self.data_array[:,self.chan_X], self.data_array[:, chan_Y])
            else:
                line.set_data([],[])
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()

        
    def auto_scale_y(self,data):
        span = max(data.max() - data.min(), 0.1 * data.min())
        return (data.min() - span *0.05), (data.max() + span*0.05)

                 
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

class DataLine():
    def __init__(self, line, x_chan = 0, y_chan = 1, fmt = '.'):
        self.x_chan = x_chan
        self.y_chan = y_chan
        self.fmt = fmt
        self.line = line
        

class DataTaker(QThread):
    MEAS_TIME = 1      
    USING_MAGNET = True 
    
    def __init__(self, lock, parent=None):
        super(DataTaker, self).__init__(parent)
        self.lock = lock
        self.stopped = True
        self.mutex = QMutex()
        self.path = None
        self.completed = False
        self.DEBUG = readconfigfile.get_debug_setting()

    def initialize(self, ):     
        print self.DEBUG
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
            self.magnet = IPS120.IPS120('GPIB::3', debug=self.DEBUG)
            self.data_channels.append(['FIELD', lambda:self.magnet.read_field(), []])
        self.data_channels.append(['X', lambda: self.instruments['GPIB::8'].read_input(1), []])
        self.data_channels.append(['Y', lambda: self.instruments['GPIB::8'].read_input(2), []])
             
        #open file, write header
        self.out_file = readconfigfile.open_data_file()

        self.out_file.write('Starting time: ' + str(self.t_start) + '\n')
        for chan in self.data_channels:        
            self.out_file.write(chan[0] + ", ")
        self.out_file.write('\n')
        
    def run(self):
        self.stopped = False
        self.main_loop()
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
            data_set = []
            for chan in self.data_channels:
                data_set.append(chan[1]())
            stri = str(data_set).strip('[]')
            print stri
            self.out_file.write(stri + '\n')
            self.emit(SIGNAL("data(PyQt_PyObject)"), array(data_set))              
            time.sleep(self.MEAS_TIME)            

    def clean_up(self):
        self.out_file.close()

        for inst in self.instruments:
            inst.close()
        
        if using_magnet==True:
            self.magnet.close()        

             
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = RecordSweepWindow()
    #form.connect(form, SIGNAL("found"), found)
    #form.connect(form, SIGNAL("notfound"), nomore)
    #form.plot([0,1,2,3,4], [0,1,2,3,])
    form.show()
    app.exec_()
