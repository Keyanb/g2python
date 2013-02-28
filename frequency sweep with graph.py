# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 16:46:03 2013

Live data collector
This program is responsible for the collection of all the data and feeding it
into the GUI. It runs in a separate thread.

@author: keyan
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui, QtSvg
import bramplot
import visa
from conductance_calculator import *

import LS340
import time, os, errno
import threading
import numpy
import SRS830
import DAC488

from pylab import *



class WireSweep(QMainWindow, bramplot.Ui_MainWindow):
    def __init__(self, parent=None):
        super(WireSweep, self).__init__()
        self.setupUi(self)
        self.datataker = DataTaker(self)
        
        self.xdata = []
        self.y1data = []
        self.data_array = array([])
        
        self.ax = self.mplwidget.axes
        self.fig = self.mplwidget.figure
        self.ax.tick_params(axis='x', labelsize=8)
        self.ax.tick_params(axis='y', labelsize=8)
        self.fig.canvas.draw()
        self.line, = self.ax.plot([],[])
        #self.ax.lines = line
        
        self.ax.set_title('Frequency Response')
        self.ax.set_xlabel('Frequency(hz)')
        self.ax.set_ylabel('Voltage(V)')
        
        self.connect(self.datataker, SIGNAL("data(PyQt_PyObject)"), self.updateData)
        path = self.selectFile()
        self.datataker.path = path
        self.datataker.setup()
        self.datataker.start()
        
    def updateData(self, data_set):
        print data_set
        self.xdata.append(data_set[0])
        self.y1data.append(data_set[1])
        self.updatePlot()
        
    def updatePlot(self):
        self.line.set_data(self.xdata,self.y1data)
        self.ax.relim()
        self.ax.autoscale_view()                      
        self.fig.canvas.draw()
        
        
    def selectFile(self):
        
        '''
        This function creates a folder in our Data folder with the current date
        then opens a file dialog to choose our data file name. It returns this
        name as a string
        '''
        
        def mkdir_p(path):
            try:
                os.makedirs(path)
            except OSError as exc:
                if exc.errno == errno.EEXIST:
                    pass
                else: raise
                
        date = time.strftime('%d-%m-%y',time.localtime())
        path = 'C:\\Users\\bram\\Documents\\Data\\' + date + '\\'
        mkdir_p(path)
        filePath = QFileDialog.getSaveFileName(None,'Choose Data File',path)
        
        return filePath
        
    def selectFolder(self):
        
        '''
        This function is identical to selectFile, but chooses a folder rather
        than a data file. This is useful if you want to more than one datafile
        from a given measurement.
        '''
        
        def mkdir_p(path):
            try:
                os.makedirs(path)
            except OSError as exc:
                if exc.errno == errno.EEXIST:
                    pass
                else: raise
                
        date = time.strftime('%d-%m-%y',time.localtime())
        path = 'C:\\Users\\bram\\Documents\\Data\\' + date + '\\'
        mkdir_p(path)
        folderPath = QFileDialog.getExistingDirectory(self,'Choose Data Folder',path)
        
        return folderPath
        
        
class DataTaker(QThread):
    def __init__(self, parent=None):
        super(DataTaker, self).__init__(parent)
        self.path = None
        
    def setup(self):
        '''
        This is the setup function which intializes the instruments and values
        which will be read. Opens data file.
        '''
        print "Initializing Instruments..."
        self.lockin = SRS830.SRS830('GPIB1::14')
        # self.lockin2 = SRS830.SRS830('GPIB0::16')
        # self.gate = DAC488.device('GPIB0::10')
        # self.gate.set_range(1,3)
        # self.temp = LS340.device('GPIB0::12')
        
                
        self.data_file = open (self.path,'w')
        self.headers = ['Frequency', 'x-Value', 'y-Value']
        stri = ''
        for i in self.headers:
            stri = stri + str(i) +'\t'
        stri = stri + '\n'
        self.data_file.write(stri)
        self.dataPoint = []
        
        print "Initialization Complete"
        
    def run(self):
        '''
        This is where the control logic of the program goes. Loops, parameter
        changes and if statements should be located here.
        '''
        
        print "Acquiring Data..."
        
        frequencies = numpy.logspace(1,5,100)
        n = len(frequencies)
        self.lockin.set_freq(frequencies[0])
       
        for i in range(0,n-1):
           self.lockin.set_freq(frequencies[i])
           time.sleep(5)
           self.ReadData(frequencies[i])
           
        print "Measurement Complete!"
        
        
    def ReadData(self,freq):
        '''
        This function reads the data, sends it to the GUI and writes it to the 
        file. The data should be sent with the x-value as the first number
        and all the dependent variables following. Make sure to include all
        the data you want (such as the calculated conductance)
        '''
        # Read the various Values
        xValue = float(self.lockin.read_input(1))
        yValue = float(self.lockin.read_input(2))
        
        # Compile values into a list
        self.dataPoint = [freq, xValue, yValue]
        
        # Convert to a string for writing to file
        #stri = str(self.dataPoint).strip('[]')
        stri = ''
        for i in self.dataPoint:
            stri = stri + str(i) +'\t'
        
        stri = stri + '\n'
        # Send signal to GUI
        self.emit(SIGNAL("data(PyQt_PyObject)"), self.dataPoint)
        
        # Save data to dat_file
        self.data_file.write(stri)
        
    def measurementRecord(self):
        '''
        This function is intended to save all the parameters and notes
        associated with the measurement. Values such as the lockin settings,
        time, date and equipment.
        '''
        
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = WireSweep()
    form.show()
    app.exec_()
