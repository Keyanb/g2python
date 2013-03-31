# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 16:46:03 2013

Live data collector
This program is responsible for the collection of all the data and feeding it
into the GUI. It runs in a separate thread.

@author: keyan
To Do:
    - Multiple Lines
    - Zoom
    - Paramater Dialog
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui, QtSvg
import bramplot
import visa
from conductance_calculator import *
from math import *
from collections import defaultdict

import time, os, errno
import threading
import numpy
from bramDataTaker import DataTaker


from pylab import *



class WireSweep(QMainWindow, bramplot.Ui_MainWindow):
    def __init__(self, parent=None):
        super(WireSweep, self).__init__()
        self.setWindowTitle('Measurement')
        self.setupUi(self)
        self.datataker = DataTaker(self)
    
        # Setting up first plot
        self.ax = self.mplwidget.axes
        self.fig = self.mplwidget.figure
        self.ax.tick_params(axis='x', labelsize=8)
        self.ax.tick_params(axis='y', labelsize=8)
        self.line, = self.ax.plot([],[],'-o', markersize = 2)
        #self.ax.lines = line
        
        # Setting up second plot
        self.ax2 = self.mplwidget_2.axes
        self.fig2 = self.mplwidget_2.figure
        self.ax2.tick_params(axis='x', labelsize=8)
        self.ax2.tick_params(axis='y', labelsize=8)
        self.line2, = self.ax2.plot([],[],'-o',color = 'red', markersize = 2)
        #self.ax.lines = line
        
        # Slots
        self.connect(self.datataker, SIGNAL("list(PyQt_PyObject)"), self.listHeaders)
        self.connect(self.datataker, SIGNAL("data(PyQt_PyObject)"), self.updateData)
        self.connect(self.datataker, SIGNAL("clear()"), self.clearData)
        self.connect(self.xlist1, SIGNAL('activated(QString)'), self.updatePlot)
        self.connect(self.xlist2, SIGNAL('activated(QString)'), self.updatePlot)
        self.connect(self.ylist1, SIGNAL('activated(QString)'), self.updatePlot)
        self.connect(self.ylist2, SIGNAL('activated(QString)'), self.updatePlot)
        self.connect(self.rescaleButton, SIGNAL('on_rescaleButton_clicked()'), self.rescale)
        
        self.computerDetect()

#        self.timer = QTimer(self)
#        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.updatePlotD)
        
    @pyqtSignature("")
    def on_startButton_clicked(self):
        
        
        # Read the radiobuttons
        
        instr_buttons = [self.vtiButton,self.he3Button,self.dilutionButton,self.customButton,self.debugButton]
        instr_configs = ['VTI','He3','Dilution','Custom','Debug']
        
        for button in instr_buttons:
            state = button.isChecked()
            if state == True:
                i = instr_buttons.index(button)
                instr = instr_configs[i]
                
        meas_buttons = [self.bodeplot,self.quantumwire,self.tempsweep,self.custom]
        meas_configs = ['Bode Plot','Wire Conductance','Temperature Sweep','Custom']
        
        for button in meas_buttons:
            state = button.isChecked()
            if state == True:
                meas = meas_configs[meas_buttons.index(button)]
             
        if meas == 'Four Wire':
            path = self.selectFolder()
        else:
            path = self.selectFile()
                
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
    def updatePlot(self):
        '''
        Updates the plots using the dict data methods. More advanced than the
        updatePlot method, but harder to understand.
        '''
        # Update plot 1
        var = str(self.xlist1.currentText())
        xdata = self.data[var]
        self.ax.set_xlabel(var)
        var = str(self.ylist1.currentText())
        ydata = self.data[var]
        self.ax.set_ylabel(var)
        
        self.line.set_data(xdata,ydata)

        self.ax.relim()
        self.ax.autoscale_view()  
        self.fig.canvas.draw()
        
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
        
    def rescale(self):
        self.ax.set_autoscalex_on(True)
        self.ax.set_autoscaley_on(True)
        self.mplwidget.rescale_and_draw()
        self.ax2.set_autoscalex_on(True)
        self.ax2.set_autoscaley_on(True)
        self.mplwidget_2.rescale_and_draw()
    
    def clearData(self):
        self.data = defaultdict(list)
        for v in self.headers:
            self.data[v] = []        
            
    def computerDetect(self):
        '''
        This function is responsible for setting the various computer specific
        program parameters.
        - Choosing the correct path for data to be saved in
        - Auto select the relevant instrument configuration
        - 
        
        The current setup of computer is:
            - Diltion Fridge: LONGICORNE
            - VTI Desktop: 293-PCZ156
            - Laptop: PCZ169
        '''        
        # Get the computer name
        computer = os.environ['COMPUTERNAME']
        print computer


        
        if computer == 'LONGICORNE':
            self.dilutionButton.setChecked(True)
            self.dataPath = 'D:\\MANIP\\DATA\\'
        elif computer == '293-PCZ156':
            self.vtiButton.setChecked(True)
            self.dataPath = 'C:\\Users\\keyan\\Documents\\Data\\'
        elif computer == 'PCZ156':
            self.he3Button.setChecked(True)
            self.dataPath == 'C:\\Users\\bram\\Documents\\Data\\'
        else:
            self.dataPath = 'C:\\'
        
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
                
        date = time.strftime('%y-%m-%d',time.localtime())
        
        path = self.dataPath + date + '\\'


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
                
        date = time.strftime('%y-%m-%d',time.localtime())
        
        path = self.dataPath + date + '\\'
            
        mkdir_p(path)
        folderPath = QFileDialog.getExistingDirectory(self,'Choose Data Folder',path)
        
        return folderPath
    
    def parameterDialog(self):
        '''
        Want to Make a dialog which has the measurement specific paramters
        '''
        
        
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = WireSweep()
    form.show()
    app.exec_()
