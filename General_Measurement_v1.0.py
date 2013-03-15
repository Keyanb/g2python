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
from math import *
from collections import defaultdict

import LS340
import LS332
import time, os, errno
import threading
import numpy
import SRS830
import DAC488
import keithley2400

from pylab import *



class WireSweep(QMainWindow, bramplot.Ui_MainWindow):
    def __init__(self, parent=None):
        super(WireSweep, self).__init__()
        self.setupUi(self)
        self.datataker = DataTaker(self)
    
        # Setting up first plot
        self.ax = self.mplwidget.axes
        self.fig = self.mplwidget.figure
        self.ax.tick_params(axis='x', labelsize=8)
        self.ax.tick_params(axis='y', labelsize=8)
        self.line, = self.ax.plot([],[])
        #self.ax.lines = line
        
        # Setting up second plot
        self.ax2 = self.mplwidget_2.axesR
        self.fig2 = self.mplwidget_2.figure
        self.ax2.tick_params(axis='x', labelsize=8)
        self.ax2.tick_params(axis='y', labelsize=8)
        self.line2, = self.ax2.plot([],[])
        #self.ax.lines = line
        
        # Slots
        self.connect(self.datataker, SIGNAL("list(PyQt_PyObject)"), self.listHeaders)
        self.connect(self.datataker, SIGNAL("dataD(PyQt_PyObject)"), self.updateDataD)
        self.connect(self.xlist1, SIGNAL('activated(QString)'), self.updatePlotD)
        self.connect(self.xlist2, SIGNAL('activated(QString)'), self.updatePlotD)
        self.connect(self.ylist1, SIGNAL('activated(QString)'), self.updatePlotD)
        self.connect(self.ylist2, SIGNAL('activated(QString)'), self.updatePlotD)
        
        # Get the computer name
        
        self.computer = os.environ['COMPUTERNAME']
        print self.computer
        
#        self.timer = QTimer(self)
#        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.updatePlotD)
        
    @pyqtSignature("")
    def on_startButton_clicked(self):
        path = self.selectFile()
        
        # Read the radiobuttons
        
        instr_buttons = [self.vtiButton,self.he3Button,self.dilutionButton,self.customButton,self.debugButton]
        instr_configs = ['VTI','He3','Dilution','Custom','Debug']
        
        for button in instr_buttons:
            state = button.isChecked()
            if state == True:
                i = instr_buttons.index(button)
                instr = instr_configs[i]
                
        meas_buttons = [self.bodeplot,self.quantumwire,self.tempsweep]
        meas_configs = ['Bode Plot','Wire Conductance','Temperature Sweep']
        
        for button in meas_buttons:
            state = button.isChecked()
            if state == True:
                meas = meas_configs[meas_buttons.index(button)]
                
        self.ax.set_title(meas)
        self.ax2.set_title(meas)
                
        self.datataker.instr = instr
        self.datataker.meas = meas
        # Clear the comboboxes
        self.xlist1.clear()
        self.xlist2.clear()
        self.ylist1.clear()
        self.ylist2.clear()
        
        
        self.datataker.path = path
        self.datataker.start()
        
#        time.sleep(1)
#        self.timer.start(100)
        
    @pyqtSignature("")
    def on_stopButton_clicked(self):
        '''
        If the stop button is pressed, the 
        '''
        self.datataker.safeStop()
    
    def listHeaders(self, headers):
        '''
        Activated when the headers signal is sent. Headers should arrive in a
        list. The drop-down select boxes will be populated
        with the two types of variables.
        '''
        print "Getting Variable List..."
        
        varlist = QStringList(headers)
        self.headers = headers
        
        # Legacy Code for separate x and y variables
        # xlist = QStringList(ctrlVariables)
        # ylist = QStringList(measVariables)
        
        self.xlist1.addItems(varlist)
        self.xlist2.addItems(varlist)
        
        self.ylist1.addItems(varlist)
        self.ylist2.addItems(varlist)
        
        # by default, we are going to plot the second and third variables
        # against the first
        self.ylist1.setCurrentIndex(1)
        self.ylist2.setCurrentIndex(2)
        
        self.data = defaultdict(list)
        for v in self.headers:
            self.data[v] = []
        
    def updateData(self, data_set):
        '''
        Updates data using manually set data variables. Easy to understand
        but less flexible than the dict methods.
        '''
        stri = str(data_set).strip('[]')
        print stri
        self.freqData.append(data_set[0])
        self.ampData.append(data_set[3])
        self.phaseData.append(data_set[4])
        self.updatePlot()
        
    def updateDataD(self, data_set):
        for v in self.headers:
            self.data[v].append(data_set[v])
        self.updatePlotD()
            
    def updatePlotD(self):
        '''
        Updates the plots using the dict data methods. More advanced than the
        updatePlot method, but harder to understand.
        '''
        # Update plot 1
        self.ax.set_autoscalex_on(True)
        var = str(self.xlist1.currentText())
        xdata = self.data[var]
        self.ax.set_xlabel(var)
        var = str(self.ylist1.currentText())
        ydata = self.data[var]
        self.ax.set_ylabel(var)
        
        self.line.set_data(xdata,ydata)
        self.mplwidget.rescale_and_draw()

#       self.ax.relim()
#       self.ax.autoscale_view()  
#       self.fig.canvas.draw()
        
        # Update Plot 2
        var = str(self.xlist2.currentText())
        xdata = self.data[var]
        self.ax2.set_xlabel(var)
        var = str(self.ylist2.currentText())
        ydata = self.data[var]
        self.ax2.set_ylabel(var)
        
        self.line2.set_data(xdata,ydata)
        self.ax2.relim()
        self.ax2.autoscale_view()                      
        self.fig2.canvas.draw()
        
        
    def updatePlot(self):
        # update plot 1
        self.line.set_data(self.freqData,self.ampData)
        self.ax.relim()
        self.ax.autoscale_view()    
        self.fig.canvas.draw()
        
        # update plot 2
        self.line2.set_data(self.freqData,self.phaseData)
        self.ax2.relim()
        self.ax2.autoscale_view()                      
        self.fig2.canvas.draw()
        
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
        path = 'C:\\Users\\keyan\\Documents\\Data\\' + date + '\\'
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
        
        if self.computer == '293-PCZ156':
            path = 'C:\\Users\\keyan\\Documents\\Data\\' + date + '\\'
        else:
            path = 'C:\\Users\\bram\\Documents\\Data\\' + date + '\\'
            
            
        mkdir_p(path)
        folderPath = QFileDialog.getExistingDirectory(self,'Choose Data Folder',path)
        
        return folderPath
        
        
        
class DataTaker(QThread):
    def __init__(self, parent=None):
        super(DataTaker, self).__init__(parent)
        self.path = None
        self.debug = False
        self.instr = 'VTI'
        self.meas = 'Bode Plot'
        
    def run(self):
        print "Acquiring Data..."
        self.setup()
        
        measurement = {'Bode Plot': self.bodePlot,
                       'Wire Conductance':self.wireCond,
                       'Temperature Sweep':self.tempSweep}
                       
        measurement[self.meas]()
        
    def setup(self):
        '''
        This is the setup function which intializes the instruments and values
        which will be read. Opens data file.
        '''
        print "Initializing Instruments..."
        
        self.instrumentSelect()
        
        self.stop = False
                
        self.data_file = open (self.path,'w')
        
        time.sleep(1)
        
        print "Initialization Complete"
        
    def bodePlot(self):
        '''
        This is where the control logic of the program goes. Loops, parameter
        changes and if statements should be located here.
        '''
        self.headers = ['Frequency(hz)', 'x-Value', 'y-Value', 'Amplitude(dB)', 'Phase(deg)']
        self.emit(SIGNAL("list(PyQt_PyObject)"), self.headers)
        
        stri = self.list2tabdel(self.headers)
        self.data_file.write(stri)
        
        frequencies = numpy.logspace(1,5,100)
        n = len(frequencies)
        self.lockin1.set_freq(frequencies[0])
        
        print 'Starting in...'
        self.printCountdown(3)
        # wait for things to stabilize

        self.ro = self.lockin1.read_input(3)
        
        for i in range(0,n-1):
            if self.stop == True:
                break
            self.lockin1.set_freq(frequencies[i])
            time.sleep(1)
            self.ReadFreqData(frequencies[i])
            
        self.data_file.close()
        
    def ReadFreqData(self,ctrlVar):
        '''
        This function reads the data, sends it to the GUI and writes it to the 
        file. The data should be sent with the x-value as the first number
        and all the dependent variables following. Make sure to include all
        the data you want (such as the calculated conductance)
        '''
        # The control variable which will be written as the first column        
        freq = ctrlVar
        
        # Read the various Values
        xValue = float(self.lockin1.read_input(1))
        yValue = float(self.lockin1.read_input(2))
        rValue = float(self.lockin1.read_input(3))
        phase = float(self.lockin1.read_input(4)) 
        amp = self.amplitudeDB(rValue)
        
        # Compile values into a list
        dataPoint = [freq, xValue, yValue, amp, phase]
        
        # Convert to a string for writing to file
        stri = self.list2tabdel(dataPoint)
        self.data_file.write(stri)
        
        # Create a dictionary for the data point and send signal to GUI    
        dataDict = dict(zip(self.headers,dataPoint))
        self.emit(SIGNAL("dataD(PyQt_PyObject)"), dataDict)
        
    def wireCond(self):
        
        self.headers = ['Gate(V)', 'x-Value', 'y-Value',  'x-Value-2', 'y-Value-2', 'Temperature (K)', 'Conductance(2e^2/h)']
        self.emit(SIGNAL("list(PyQt_PyObject)"), self.headers)
        
        stri = self.list2tabdel(self.headers)
        self.data_file.write(stri)
        
        stepTime = 0.5
        max_gate = -2
        stepsize = 0.005
        windowlower = -1.5
        windowupper = -2.0
        windowstep = 0.005
        gateVoltage = 0.0
        
        while gateVoltage > max_gate:
            if self.stop == True:
                break
            
            self.gate.set_voltage(gateVoltage)
            self.readCondData(gateVoltage)
        
            if (gateVoltage <= windowlower and gateVoltage >= windowupper):
                gateVoltage = gateVoltage - windowstep
            else:
                gateVoltage = gateVoltage - stepsize  
                
            time.sleep(stepTime)
        
        while gateVoltage < 0:
            if self.stop == True:
                break
            
            self.gate.set_voltage(gateVoltage)
            self.readCondData(gateVoltage)
        
            if (gateVoltage <= windowlower and gateVoltage >= windowupper):
                gateVoltage = gateVoltage + windowstep
            else:
                gateVoltage = gateVoltage + stepsize  
                
            time.sleep(stepTime)
            
        # Loop to slowly reduce gate
        
        if self.stop == True:        
            while gateVoltage < 0:
                gateVoltage += 0.001
                self.gate.setvoltage(gateVoltage)
                # 0.1 delay corresponds to 1:40 per volt (assuming 0.001 step)
                time.wait(0.2)
                
        self.gate.set_voltage(0)
        
        self.data_file.close()
        
    def readCondData(self,ctrlVar):
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
        gateVoltage = ctrlVar
        conductance = twopointcond(xValue1)
        
        # Compile values into a list
        dataPoint = [gateVoltage, xValue1, yValue1, xValue2, yValue2, temp, conductance]
        
        # Convert to a string for writing to file
        stri = self.list2tabdel(dataPoint)
        self.data_file.write(stri)
        
        # Create a dictionary for the data point and send signal to GUI    
        dataDict = dict(zip(self.headers,dataPoint))
        self.emit(SIGNAL("dataD(PyQt_PyObject)"), dataDict)
        
        
    def tempSweep(self):
        '''
        This script just monitors the instruments, generally for a temperature
        sweep, but it could be adapted to othe purposes fairly easily
        '''
        self.headers = ['Temperature-A (K)', 'Temperature-B (K)','x-Value', 'y-Value',  'x-Value-2', 'y-Value-2','Time(s)']
        self.emit(SIGNAL("list(PyQt_PyObject)"), self.headers)
        
        stri = self.list2tabdel(self.headers)
        self.data_file.write(stri)
        
        self.t_start = time.time()
        timestep = 1 #(s)
        temperatures = [self.temp.read('a'),self.temp.read('b')]
        
        while temperatures[1]>1.8:
            temperatures = self.readTempData()
            step = step+1
            #Wait until the enxt timestep
            while (time.time()-t_start)<step:
                wait=1
                
    
    def readTempData(self):
        t = float(time.time() - self.t_start)
        xValue1 = float(self.lockin1.read_input(1))
        xValue2 = float(self.lockin2.read_input(1))
        yValue1 = float(self.lockin1.read_input(2))
        yValue2 = float(self.lockin2.read_input(1))
        # gate = gate
        temperatureA = float(self.temp.read('a'))
        temperatureB = float(self.temp.read('b'))
        dataPoint = [temperatureA, temperatureB, xValue1, yValue1, xValue2, yValue2, t]
        
        # Convert to a string for writing to file
        stri = self.list2tabdel(dataPoint)
        self.data_file.write(stri)
        
        # Create a dictionary for the data point and send signal to GUI    
        dataDict = dict(zip(self.headers,dataPoint))
        self.emit(SIGNAL("dataD(PyQt_PyObject)"), dataDict)
        
        # return temperatures since they are the control variables
        return [temperatureA,temperatureB]
        
    def measurementRecord(self):
        '''
        This function is intended to save all the parameters and notes
        associated with the measurement. Values such as the lockin settings,
        time, date and equipment.
        '''
    def instrumentSelect(self):
        
        instrDict = {
        'VTI' : self.VTI_instr,
        'He3' : self.He3_instr,
        'Dilution' : self.dil_instr,
        'Custom' : self.custom_instr,
        'Debug': self.debug_instr
        }
        print 'Selecting Instruments'     
        
        instrDict[self.instr](self.debug)
                
    def VTI_instr(self,debug=False):
        print "Initializing VTI Instruments..."
        self.lockin1 = SRS830.SRS830('GPIB1::14',debug)
        self.lockin2 = SRS830.SRS830('GPIB1::8',debug)
        self.gate = keithley2400.device('GPIB1::24',debug)
        self.temp = LS332.LS332('GPIB1::12',debug)
        
    def He3_instr(self,debug=False):
        print "Initializing He3 Instruments..."
        self.lockin1 = SRS830.SRS830('GPIB0::8',debug)
        self.lockin2 = SRS830.SRS830('GPIB0::16',debug)
        self.gate = DAC488.DAC488('GPIB0::10',debug)
        self.gate.set_range(1,3)
        self.temp = LS340.LS340('GPIB0::12',debug)
    
    def dil_instr(self,debug=False):
        '''
        Dilution Fridge Instruments
        '''
    def custom_instr(self,debug=False):
        '''
        Custom Instrument Setup
        '''
    def debug_instr(self,debug=True):
        '''
        debug 
        '''
        debug = True
        
        print "Initializing Debug Instruments..."
        self.lockin1 = SRS830.SRS830('GPIB1::14',debug)
        self.lockin2 = SRS830.SRS830('GPIB1::8',debug)
        self.gate = keithley2400.device('GPIB1::24',debug)
        self.temp = LS332.LS332('GPIB1::12',debug)
        
    def amplitudeDB(self,r):
        amp = 20*log10(r/self.ro)
        return amp
    
    def list2tabdel(self,values):
        stri = ''
        for i in values:
            stri = stri + str(i) +'\t'
        stri = stri + '\n'
        return stri
        
    def printCountdown(self,seconds):
        for s in range(seconds):
            print seconds-s
            time.sleep(1)
            
    def safeStop(self):
        self.stop = True

        print "Measurement Complete!"        
        print "Safely shutting down instruments..."
        
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = WireSweep()
    form.show()
    app.exec_()
