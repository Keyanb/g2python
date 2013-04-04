# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 13:18:32 2012

@author: Benjamin Schmidt

TODO:
    - add toolbar for plot navigation
    - more descriptive output in print 
    - disable appropriate inputs when acquisition starts
    - end thread more gracefully    
    - move instrument objects to main thread / shared?
"""

from __future__ import division
import time

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *

import numpy as np
from pylab import *

import visa

import ui_recordsweep_full as ui_recordsweep
import DataTakerThread as DTT
import readconfigfile

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
    
    UNITS = {'FIELD': 'T', 'X': 'V', 'Y': 'V', 'R': 'V', 'PHASE': 'degrees'}    
    
    def __init__(self, parent=None):
        super(RecordSweepWindow, self).__init__()
        self.setupUi(self)

        self.lock = QReadWriteLock()         
        self.datataker = DTT.DataTakerThread(self.lock, self)  
        self.connect(self.datataker, SIGNAL("data(PyQt_PyObject)"),
                     self.updateData)

        # axes and figure initialization
        
        self.fig = self.mplwidget.figure
        self.ax = self.mplwidget.axes
        self.axR = self.mplwidget.axesR

        self.fig.canvas.draw()              
        
        self.history_length = 0
        
         # objects to hold line data
        line_set_L = []
        line_set_R = []
        fmt_str = ['b','g','r','k','c','m']
        
        for i in range (self.MAX_CHANNELS):            
            line1, = self.ax.plot([], [], fmt_str[i])     
            line2, = self.axR.plot([], [], fmt_str[i])
            
            line_set_L.append(line1)
            line_set_R.append(line2)
        
        self.ax.lines = line_set_L
        self.axR.lines = line_set_R

        self.data_array = array([])
        self.chan_X = 0
        
        self.refreshInstrumentList()
        
        self.load_settings("default_settings.txt")
        self.tabWidget.setCurrentIndex(0)
        
        self.fileSaveSettingsAction = self.createAction("Save Settings", slot=self.fileSaveSettings, shortcut=QKeySequence.SaveAs,
                                        icon=None, tip="Save the current instrument settings")
        
        self.fileLoadSettingsAction = self.createAction("Load Settings", slot=self.fileLoadSettings, shortcut=QKeySequence.Open,
                                        icon=None, tip="Load instrument settings from file")               
        
        self.fileSaveFigAction = self.createAction("&Save Figure", slot=self.fileSaveFig, shortcut=QKeySequence.Save,
                                        icon=None, tip="Save the current figure")      
        
        self.filePrintAction = self.createAction("&Print Report", slot=self.filePrint, shortcut=QKeySequence.Print,
                                        icon=None, tip="Print the figure along with relevant information")                   
        
        self.plotToggleControlLAction = self.createAction("Toggle &Left Axes Control", slot=self.toggleControlL, shortcut=QKeySequence("Ctrl+L"),
                                        icon="toggleLeft", tip="Toggle whether the mouse adjusts Left axes pan and zoom", checkable=True)                   

        self.plotToggleControlRAction = self.createAction("Toggle &Right Axes Control", slot=self.toggleControlR, shortcut=QKeySequence("Ctrl+R"),
                                        icon="toggleRight", tip="Toggle whether the mouse adjusts right axes pan and zoom", checkable=True)                   

        self.plotToggleXControlAction = self.createAction("Toggle &X Axes Control", slot=self.toggleXControl, shortcut=QKeySequence("Ctrl+X"),
                                        icon="toggleX", tip="Toggle whether the mouse adjusts x axis pan and zoom", checkable=True)                   
         
                    
        self.plotAutoScaleXAction = self.createAction("Auto Scale X", slot=self.toggleAutoScaleX, shortcut=QKeySequence("Ctrl+A"),
                                        icon="toggleAutoScaleX", tip="Turn autoscale X on or off", checkable=True)                   
                    
        self.plotAutoScaleLAction = self.createAction("Auto Scale L", slot=self.toggleAutoScaleL, shortcut=QKeySequence("Ctrl+D"),
                                        icon="toggleAutoScaleL", tip="Turn autoscale Left Y on or off", checkable=True)                   

        self.plotAutoScaleRAction = self.createAction("Auto Scale R", slot=self.toggleAutoScaleR, shortcut=QKeySequence("Ctrl+E"),
                                        icon="toggleAutoScaleR", tip="Turn autoscale Right Y on or off", checkable=True)                   
                            
        
        self.fileMenu = self.menuBar().addMenu("File")  

        self.fileMenu.addAction(self.fileLoadSettingsAction)
        self.fileMenu.addAction(self.fileSaveSettingsAction)
        self.fileMenu.addAction(self.filePrintAction)       
        self.fileMenu.addAction("Refresh Instrument List", self.refreshInstrumentList)
        self.fileMenu.addAction(self.fileSaveFigAction)

        
        self.plotMenu = self.menuBar().addMenu("&Plot")
        
        self.plotMenu.addAction(self.plotToggleXControlAction)
        self.plotMenu.addAction(self.plotToggleControlLAction)
        self.plotMenu.addAction(self.plotToggleControlRAction)

        self.plotMenu.addAction(self.plotAutoScaleXAction)    
        self.plotMenu.addAction(self.plotAutoScaleLAction)  
        self.plotMenu.addAction(self.plotAutoScaleRAction)
        
        plotToolbar = self.addToolBar("Plot")
        plotToolbar.addAction(self.plotToggleXControlAction)
        plotToolbar.addAction(self.plotToggleControlLAction)
        plotToolbar.addAction(self.plotToggleControlRAction)

        plotToolbar.addAction(self.plotAutoScaleXAction)
        plotToolbar.addAction(self.plotAutoScaleLAction)
        plotToolbar.addAction(self.plotAutoScaleRAction)

    def createAction(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal="triggered()"):     
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon("./images/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action
        
        
    def refreshInstrumentList(self):
        try:
            self.AVAILABLE_PORTS = visa.get_instruments_list()
        except visa.VisaIOError as e:
            if e.error_code == -1073807343:
                print "GPIB does not seem to be connected"
            self.AVAILABLE_PORTS = ["GPIB::8", "GPIB::9", "GPIB::26"]        
    
    def toggleAutoScaleX(self):
        if self.plotAutoScaleXAction.isChecked():
            self.plotToggleXControlAction.setChecked(False)   
        else:
            self.plotToggleXControlAction.setChecked(True)    
        self.updateZoomSettings()

    def toggleAutoScaleL(self):
        if self.plotAutoScaleLAction.isChecked():
            self.plotToggleControlLAction.setChecked(False)            
        else:
            self.plotToggleControlLAction.setChecked(True)              
        self.updateZoomSettings()

    def toggleAutoScaleR(self):
        if self.plotAutoScaleRAction.isChecked():
            self.plotToggleControlRAction.setChecked(False)            
        else:       
            self.plotToggleControlRAction.setChecked(True)      
        self.updateZoomSettings()
        
    def toggleXControl(self):
        if self.plotToggleXControlAction.isChecked():
            self.plotAutoScaleXAction.setChecked(False)             
        self.updateZoomSettings()
            
    def toggleControlL(self):
        if self.plotToggleControlLAction.isChecked():
            self.plotAutoScaleLAction.setChecked(False)               
        self.updateZoomSettings()
         
    def toggleControlR(self):
        if self.plotToggleControlLAction.isChecked():
            self.plotAutoScaleRAction.setChecked(False)             
        self.updateZoomSettings()
            
    def updateZoomSettings(self):
        self.mplwidget.setActiveAxes(self.plotToggleXControlAction.isChecked(), 
                                     self.plotToggleControlLAction.isChecked(), 
                                     self.plotToggleControlRAction.isChecked())        
        self.ax.set_autoscalex_on(self.plotAutoScaleXAction.isChecked())
        self.ax.set_autoscaley_on(self.plotAutoScaleLAction.isChecked())
        self.axR.set_autoscaley_on(self.plotAutoScaleRAction.isChecked())        
        
    def fileSaveFig(self):
        fname = str(QFileDialog.getSaveFileName(self, 'Open settings file', './'))
        if fname:
            self.fig.savefig(fname)

    def fileSaveSettings(self):
        fname = str(QFileDialog.getSaveFileName(self, 'Save settings file as', './'))
        if fname:
            self.save_settings(fname)
        
    def fileLoadSettings(self):  
        fname = str(QFileDialog.getOpenFileName(self, 'Open settings file', './'))       
        if fname:
            self.load_settings(fname)

    def filePrint(self):
        printer = QPrinter()
        
        dlg = QPrintDialog(printer)
        
        if(dlg.exec_()!= QDialog.Accepted):
             return
             
        p = QPainter(printer)

        dpi = printer.resolution()
        
        # copy the current figure contents to a standard size figure
        fig2 = figure(figsize=(8,5), dpi = dpi*3)

        ax = fig2.add_subplot(1,1,1)
        for line in self.ax.lines:
            if line.get_xdata() != []:
                ax.plot (line.get_xdata(), line.get_ydata(), label= line.get_label())
        ax.set_xlim(self.ax.get_xlim())
        ax.set_ylim(self.ax.get_ylim())
        ax.set_xlabel(self.ax.get_xlabel())
        ax.set_ylabel(self.ax.get_ylabel())        
        
        # Shink current axis by 20%
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        
        # Put a legend to the right of the current axis
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        fig2.savefig("temp.png", dpi=dpi*3) #not sure why putting dpi=dpi makes it all pixelly
        
        margin_top = 0.5*dpi
        margin_left = 0.5*dpi       
        
        #matplotlib's svg rendering has a bug if the data extends beyond the plot limits
        #svg = QtSvg.QSvgRenderer("temp.svg")
        #svg.render(p, QRectF(margin_top,margin_left, 8*dpi, 5*dpi))

        p.drawImage(QRectF(margin_top,margin_left, 8*dpi, 5*dpi), QImage("temp.png", format='png'))
        p.drawText (margin_left, 600, "Data recorded to: " + self.out_file.name)
        print "about to send to printer"        
        p.end()           
           
    def load_settings(self, fname):
        settings_file = open(fname)
        
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
                        self.comboBox_Instr[idx].addItem(QIcon("not_found.png"), port)
                        self.comboBox_Instr[idx].setCurrentIndex(self.comboBox_Instr[idx].count()-1)
                        
                    self.comboBox_Param[idx].clear()
                    self.comboBox_Param[idx].addItems(self.AVAILABLE_PARAMS[instr_type])

                    param = settings[3].strip().upper()
                    if param in self.AVAILABLE_PARAMS[instr_type]:                       
                        self.comboBox_Param[idx].setCurrentIndex(self.comboBox_Param[idx].findText(param))
                       
            self.radioButton_X[idx].setChecked (settings[4].strip().upper() == "TRUE")
            self.checkBox_Y[idx].setChecked (settings[5].strip().upper() == "TRUE")
            
            idx +=1
        
        settings_file.close()

    def save_settings(self, fname):
        settings_file = open(fname, 'w')
        
        idx = 0
        for idx in range (self.MAX_CHANNELS):
            name = str(self.lineEdit_Name[idx].text())
            if name and not name.isspace(): 
                settings_file.write(self.lineEdit_Name[idx].text() +', ')
                settings_file.write(self.comboBox_Type[idx].currentText() +', ')
                settings_file.write(self.comboBox_Instr[idx].currentText() +', ')
                settings_file.write(self.comboBox_Param[idx].currentText() +', ')
                settings_file.write(str(self.radioButton_X[idx].isChecked()) +', ')
                settings_file.write(str(self.checkBox_Y[idx].isChecked()) +'\n')
        settings_file.close()
        
        
    def XRadioButtonHandler(self):
        for num, box in enumerate(self.radioButton_X):
            if box.isChecked():
                self.chan_X = num
                self.ax.set_xlabel(self.lineEdit_Name[num].text())
                
        self.updatePlot() 
        
    def YCheckBoxHandler(self):  
        for num, box in enumerate(self.checkBox_Y):
            if box.isChecked():
                name = self.lineEdit_Name[num].text()
                unit = self.UNITS[str(self.comboBox_Param[num].currentText())]
                self.ax.set_ylabel(name + " (" + unit + ")")
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
        stri = str(data_set).strip('[]\n\r') 
        stri = stri.replace('\n', '') #numpy arrays conveniently include newlines in their strings, get rid of them.

        print '>>' + stri
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

        for chan_Y, [line_L, line_R] in enumerate(zip (self.ax.lines, self.axR.lines)):
            if self.checkBox_Y[chan_Y].isChecked() and self.data_array.size > 0:
                line_L.set_data(self.data_array[first:,self.chan_X], self.data_array[first:, chan_Y] / 10**self.mplwidget.left_pow)
            else:
                line_L.set_data([],[])
                
            if self.checkBox_YR[chan_Y].isChecked() and self.data_array.size > 0:
                line_R.set_data(self.data_array[first:,self.chan_X], self.data_array[first:, chan_Y] / 10**self.mplwidget.right_pow)
            else:
                line_R.set_data([],[])
                
        self.mplwidget.rescale_and_draw()


            
             
    @pyqtSignature("")
    def on_startStopButton_clicked(self):

        if self.datataker.isStopped():    
            self.t_start = time.time()            
            #open file, write header
            self.out_file = readconfigfile.open_data_file()

            self.out_file.write('Starting time: ' + str(self.t_start) + '\n')
        
            name_list = []
            for lineEdit in self.lineEdit_Name:
                lineEdit.setReadOnly(True)
                name_list.append(str(lineEdit.text()))
            
            for name, line in zip (name_list, self.ax.lines):
                line.set_label(name)
            
            stri = str(name_list).strip('[]')           
            print stri
            self.out_file.write(stri + '\n')  
            
            type_list = [str(comboBox.currentText()) for comboBox in self.comboBox_Type]
            dev_list = [str(comboBox.currentText()) for comboBox in self.comboBox_Instr] 
            param_list = [str(comboBox.currentText()) for comboBox in self.comboBox_Param]

            self.tabWidget.setCurrentIndex(1)
            
            self.datataker.initialize(name_list, type_list, dev_list, param_list) 
            self.datataker.start()
            
            self.startStopButton.setText("Stop")          
        else:
            self.datataker.stop()
            self.out_file.close()
            self.startStopButton.setText("Start")   
        

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = RecordSweepWindow()
    form.show()
    app.exec_()
