# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 13:18:32 2012

@author: Benjamin Schmidt
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
import ui_recordsweep
import visa

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
    INSTRUMENT_TYPES = ['TIME', 'IPS120', 'SRS830']   
    
    AVAILABLE_PARAMS = {}
    AVAILABLE_PARAMS['TIME'] = []
    AVAILABLE_PARAMS[''] = []
    AVAILABLE_PARAMS['IPS120'] = ['FIELD']
    AVAILABLE_PARAMS['SRS830'] = ['X', 'Y', 'R', 'Phase', 'AUX_1', 'AUX_2', 'AUX_3', 'AUX_4']    
    
    def __init__(self, parent=None):
        super(RecordSweepWindow, self).__init__()
        self.setupUi(self)

        
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
        
        self.history_length = 0
        
         # objects to hold line data
        line_set = []
        fmt_str = ['b','g','r','k','c','m']
        
        for i in range (self.MAX_CHANNELS):            
            line1, = self.ax.plot([], [], fmt_str[i])            
            line_set.append(line1)
        
        self.ax.lines = line_set

   
        try:
            self.AVAILABLE_PORTS = visa.get_instruments_list()
        except visa.VisaIOError as e:
            if e.error_code == -1073807343:
                print "GPIB does not seem to be connected"
            self.AVAILABLE_PORTS = ["GPIB::8", "GPIB::9", "GPIB::26"]
            
        self.data_array = array([])#zeros(self.MAX_CHANNELS)
        #self.data_array.shape = [1,self.MAX_CHANNELS]
        self.chan_X = 0

        self.customizeUi()
        self.load_settings()
        
        self.statusbar.showMessage("Program loaded")
        self.plotMenu = self.menuBar().addMenu("&Plot")
        self.plotMenu.addAction("Quick Save Figure", self.savefigure)
        
    def savefigure(self):
        self.fig.savefig("test.pdf")
        
    def customizeUi(self):

        self.lineEdit_Name = []
        self.comboBox_Type = []
        self.comboBox_Instr = []
        self.comboBox_Param = []       
        self.radioButton_X = [] 
        self.checkBox_Y = []        
   
        for i in range (self.MAX_CHANNELS):   

            pos_LE = lambda x: (20 * x + 1) + 50
                    
            self.lineEdit_Name.append(QtGui.QLineEdit(self.groupBox_Name))
            self.lineEdit_Name[i].setGeometry(QtCore.QRect(10, pos_LE(i), 81, 16))
            self.lineEdit_Name[i].setText(QtGui.QApplication.translate("RecordSweepWindow", "", None, QtGui.QApplication.UnicodeUTF8))
            self.lineEdit_Name[i].setObjectName(_fromUtf8("lineEdit_Name"))
            
            self.comboBox_Type.append(QtGui.QComboBox(self.groupBox_Type))
            self.comboBox_Type[i].setGeometry(QtCore.QRect(10, 20 * (i+1), 61, 16))
            self.comboBox_Type[i].setObjectName(_fromUtf8("comboBox"))
            self.comboBox_Type[i].addItems(self.INSTRUMENT_TYPES)
            
            self.connect(self.comboBox_Type[i], SIGNAL("currentIndexChanged(int)"), self.ComboBoxTypeHandler)                  

            self.comboBox_Instr.append(QtGui.QComboBox(self.groupBox_Instr))
            self.comboBox_Instr[i].setGeometry(QtCore.QRect(10, 20 * (i+1), 61, 16))
            self.comboBox_Instr[i].setObjectName(_fromUtf8("comboBox"))
            self.comboBox_Instr[i].addItems(self.AVAILABLE_PORTS)
            
            self.comboBox_Param.append(QtGui.QComboBox(self.groupBox_Param))
            self.comboBox_Param[i].setGeometry(QtCore.QRect(10, 20 * (i+1), 61, 16))
            self.comboBox_Param[i].setObjectName(_fromUtf8("comboBox"))

            self.radioButton_X.append(QRadioButton(self.groupBox_X))
            self.radioButton_X[i].setGeometry(QRect(7, 20*(i+1), 16, 16))
            self.radioButton_X[i].setText(_fromUtf8(""))
            self.radioButton_X[i].setObjectName(_fromUtf8("radioButton_" + str(i)))
            self.connect(self.radioButton_X[i], SIGNAL("toggled(bool)"), self.XRadioButtonHandler)                          
      
            self.checkBox_Y.append(QCheckBox(self.groupBox_Y))
            self.checkBox_Y[i].setGeometry(QRect(5, 20 * (i+1), 16, 16))
            self.checkBox_Y[i].setText(_fromUtf8(""))
            self.checkBox_Y[i].setObjectName(_fromUtf8("checkBox_" +str(i)))  
            self.connect(self.checkBox_Y[i], SIGNAL("stateChanged(int)"), self.YCheckBoxHandler)       

    
    def load_settings(self):
        settings_file = open("default_settings.txt")
        
        idx = 0
        for line in settings_file:
            settings = line.split(',')
            self.lineEdit_Name[idx].setText (settings[0])
            instr_type = settings[1].strip().upper()
            
            if instr_type in self.INSTRUMENT_TYPES:                
                self.comboBox_Type[idx].setCurrentIndex(self.comboBox_Type[idx].findText(instr_type))
                
                if instr_type == "TIME":
                    self.comboBox_Instr[idx].clear()
                else:
                    port = settings[2].strip().upper()
                    if port in self.AVAILABLE_PORTS:
                        self.comboBox_Instr[idx].setCurrentIndex(self.comboBox_Instr[idx].findText(port))
                    else:
                        self.comboBox_Instr[idx].addItem(port)
                        self.comboBox_Instr[idx].setItemIcon(0, QIcon("not_found.png"))
                        
                    self.comboBox_Param[idx].clear()
                    self.comboBox_Param[idx].addItems(self.AVAILABLE_PARAMS[instr_type])

                    param = settings[3].strip().upper()
                    if param in self.AVAILABLE_PARAMS[instr_type]:
                        
                        self.comboBox_Param[idx].setCurrentIndex(self.comboBox_Param[idx].findText(param))

                        
            self.radioButton_X[idx].setChecked (settings[4].strip().upper() == "TRUE")
            self.checkBox_Y[idx].setChecked (settings[5].strip().upper() == "TRUE")
            
            idx +=1
        
        settings_file.close()
        
        
    def XRadioButtonHandler(self):
        for num, box in enumerate(self.radioButton_X):
            if box.isChecked():
                self.chan_X = num
                self.ax.set_xlabel(self.lineEdit_Name[num].text())
                
        self.updatePlot() 
        
    def YCheckBoxHandler(self):        
        self.updatePlot()      
    
    def ComboBoxTypeHandler(self):
        for typeBox, instrBox, paramBox in zip (self.comboBox_Type, self.comboBox_Instr, self.comboBox_Param):     
            if typeBox == self.sender():
                for i in range(instrBox.count() + 1):
                        instrBox.removeItem(0)
                        
                text = typeBox.currentText()
                if text == "TIME":
                    instrBox.clear()
                else:
                    instrBox.clear()
                    instrBox.addItems(self.AVAILABLE_PORTS)
                paramBox.clear()
                paramBox.addItems(self.AVAILABLE_PARAMS[str(text)])
                    
    def updateData(self, data_set): 
        stri = str(data_set).strip('[]')           
        print stri
        self.out_file.write(stri + '\n')        
        
        if self.data_array.size == 0:
            self.data_array = data_set
            data_set.shape = [1, data_set.size]
        else:            
            self.data_array = vstack([self.data_array, data_set])
        self.updatePlot()

    def updatePlot(self): 
        first = 0
        if self.history_length:
            first = max(0, self.data_array.shape[0] - self.history_length)
            
        for chan_Y, line in enumerate(self.ax.lines):
            if self.checkBox_Y[chan_Y].isChecked() and self.data_array.size > 0:
                line.set_data(self.data_array[first:,self.chan_X], self.data_array[first:, chan_Y])
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
            
            #open file, write header
            self.out_file = readconfigfile.open_data_file()
            self.out_file.write('Starting time: ' + str(self.t_start) + '\n')
        
            name_list = []
            for lineEdit in self.lineEdit_Name:
                lineEdit.setReadOnly(True)
                name_list.append(str(lineEdit.text()))
                
            stri = str(data_set).strip('[]')           
            print stri
            self.out_file.write(stri + '\n')  
            
            type_list = self.getComboBoxData(self.comboBox_Type)
            dev_list = self.getComboBoxData(self.comboBox_Instr)   
            param_list = self.getComboBoxData(self.comboBox_Param)

            self.tabWidget.setCurrentIndex(1)
            
            self.datataker.initialize(name_list, type_list, dev_list, param_list) 
            self.datataker.start()
            
            self.startStopButton.setText("Stop")          
        else:
            self.datataker.stop()
            self.out_file.close()
            self.startStopButton.setText("Start")

    def getComboBoxData(self, comboBox_List):
        stri_list = []
        for comboBox in comboBox_List:
            text = comboBox.currentText()
            stri_list.append(str(text))
            #comboBox.clear()
            #comboBox.addItem(text)
        return stri_list   

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
        self.completed = False
        self.DEBUG = readconfigfile.get_debug_setting()

    def initialize(self, name_list, type_list, dev_list, param_list):     
        self.stopped = True
        self.completed = False     
        self.t_start = time.time()
        #instrumentation setup - store instrument objects in a dictionary by address
        
        # tuple: lockin #, channel, subplot for display
        self.data_channels = []        
        self.instruments = {}
        self.instrument_types = {}

        for name, instr_type, dev, param in zip(name_list, type_list, dev_list, param_list):
            if name:
                # add instrument to list if not there
                if not dev in self.instruments:
                    if instr_type == 'SRS830':               
                        self.instruments[dev] = SRS830.SRS830(dev, debug=self.DEBUG)
                    elif instr_type == 'IPS120':
                        self.instruments[dev] = IPS120.IPS120(dev, debug=self.DEBUG)    
                    self.instrument_types[dev] = instr_type
                else:
                    if instr_type != self.instrument_types[dev]:
                        print ("Same GPIB port specified for different instruments! ")
                        print (dev + " " + instr_type + " " + self.instrument_types[dev])
                        instr_type = 'NONE'
                        
    
                if instr_type == 'TIME':
                    command = lambda: time.time() - self.t_start
                elif instr_type == 'IPS120':
                    if param == 'FIELD':
                        command = lambda d=dev: self.instruments[d].read_field()
                elif instr_type == 'SRS830':
                    if param =='X':
                        command = lambda d=dev: self.instruments[d].read_input(1)
                    elif param =='Y':
                        command = lambda d=dev: self.instruments[d].read_input(2)
                    elif param =='R':
                        command = lambda d=dev: self.instruments[d].read_input(3)    
                    elif param =='PHASE':
                        command = lambda d=dev: self.instruments[d].read_input(4)    
                     
            self.data_channels.append(command)

        
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
        while self.isStopped() == False:
            data_set = [command() for command in self.data_channels]            
            self.emit(SIGNAL("data(PyQt_PyObject)"), array(data_set))              
            time.sleep(self.MEAS_TIME)            

    def clean_up(self):
        for inst in self.instruments:
            inst.close()      

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = RecordSweepWindow()
    form.show()
    app.exec_()
