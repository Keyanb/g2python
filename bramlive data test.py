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
import keithley2400
import LS332

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
        
        self.ax.set_title('Conductance Plot')
        self.ax.set_xlabel('Gate Voltage (V)')
        self.ax.set_ylabel('Conductance (2e^2/h)')
        
        self.connect(self.datataker, SIGNAL("data(PyQt_PyObject)"), self.updateData)
        path = self.selectFile()
        self.datataker.path = path
        self.datataker.setup()
        self.datataker.start()
        
    def updateData(self, data_set):
        print data_set
        self.xdata.append(data_set[0])
        self.y1data.append(data_set[4])
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
        path = 'C:\\Users\\keyan\\Documents\\Data\\' + date + '\\'
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
        
        self.VTI_instr()
                
        self.data_file = open (self.path,'w')
        self.headers = ['Gate Voltage', 'x-Value', 'y-Value', 'x-Value-2', 'y-Value-2', 'Temperature', 'Conductance']
        self.dataPoint = []
        
        print "Initialization Complete"
        
    def run(self):
        '''
        This is where the control logic of the program goes. Loops, parameter
        changes and if statements should be located here.
        '''
        
        print "Acquiring Data..."
        
        stepTime = 0.5
        max_gate = -2
        stepsize = 0.005
        windowlower = -1.5
        windowupper = -2.0
        windowstep = 0.005
        gateVoltage = 0.0
        
        while gateVoltage > max_gate:
            
            self.gate.set_voltage(gateVoltage)
            self.ReadData(gateVoltage)
        
            if (gateVoltage <= windowlower and gateVoltage >= windowupper):
                gateVoltage = gateVoltage - windowstep
            else:
                gateVoltage = gateVoltage - stepsize  
                
            time.sleep(stepTime)
        
        while gateVoltage < 0:
            
            self.gate.set_voltage(gateVoltage)
            self.ReadData(gateVoltage)
        
            if (gateVoltage <= windowlower and gateVoltage >= windowupper):
                gateVoltage = gateVoltage + windowstep
            else:
                gateVoltage = gateVoltage + stepsize  
                
            time.sleep(stepTime)
        
        self.gate.set_voltage(0)
        
        
    def ReadData(self,voltage):
        '''
        This function reads the data, sends it to the GUI and writes it to the 
        file. The data should be sent with the x-value as the first number
        and all the dependent variables following. Make sure to include all
        the data you want (such as the calculated conductance)
        '''
        # Read the various Values
        xValue1 = float(self.lockin1.read_input(1))
        xValue2 = float(self.lockin2.read_input(1))
        yValue1 = float(self.lockin1.read_input(2))
        yValue2 = float(self.lockin2.read_input(1))
        
        temp = float(self.temp.read('C'))
        gateVoltage = voltage
        conductance = twopointcond(xValue1)
        
        # Compile values into a list
        self.dataPoint = [gateVoltage, xValue1, yValue1, xValue2, yValue2, temp, conductance]
        
        # Convert to a string for writing to file
        stri = str(self.dataPoint)
        
        # Send signal to GUI
        self.emit(SIGNAL("data(PyQt_PyObject)"), self.dataPoint)
        
        # Save data to dat_file
        self.data_file.write(stri+'\n')
        
    def measurementRecord(self):
        '''
        This function is intended to save all the parameters and notes
        associated with the measurement. Values such as the lockin settings,
        time, date and equipment.
        '''
    def VTI_instr(self):
        print "Initializing Instruments..."
        self.lockin1 = SRS830.SRS830('GPIB1::14')
        self.lockin2 = SRS830.SRS830('GPIB1::8')
        self.gate = keithley2400.device('GPIB1::24')
        self.temp = LS332.device('GPIB1::12')
        
    def He3_instr(self):
        print "Initializing Instruments..."
        self.lockin1 = SRS830.SRS830('GPIB0::8')
        self.lockin2 = SRS830.SRS830('GPIB0::16')
        self.gate = DAC488.device('GPIB0::10')
        self.gate.set_range(1,3)
        self.temp = LS340.device('GPIB0::12')
        
        
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = WireSweep()
    form.show()
    app.exec_()
