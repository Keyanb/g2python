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

import LS370
import time
import threading
import numpy
import SRS830

from pylab import *



class WireSweep(QMainWindow, bramplot.Ui_MainWindow):
    def __init__(self, parent=None):
        super(WireSweep, self).__init__()
        self.setupUi(self)
        self.datataker = DataTaker(self)
        
        self.data = [0]
        
        self.ax = self.mplwidget.axes
        self.fig = self.mplwidget.figure
        self.ax.tick_params(axis='x', labelsize=8)
        self.ax.tick_params(axis='y', labelsize=8)
        self.fig.canvas.draw()
        self.ax.plot([],[])
        
        self.connect(self.datataker, SIGNAL("data(PyQt_PyObject)"), self.updateData)
        self.datataker.setup()
        self.datataker.start()
        
    def updateData(self, data_point):
        # stri = str(data_set).strip('[]')           
        print data_point
        self.data.append(data_point)
        self.updatePlot()
        
    def updatePlot(self):
        self.ax.plot(self.data)
        self.ax.relim()
        self.ax.autoscale_view()                      
        self.fig.canvas.draw()

        
        
class DataTaker(QThread):
    def __init__(self, parent=None):
        super(DataTaker, self).__init__(parent)
        
    def setup(self):
        self.lockin = SRS830.SRS830('GPIB0::8')
        
    def run(self):
        self.ReadData()
        
    def ReadData(self):
        for n in range(1,40):
            xValue = self.lockin.read_input(1)
            data_point = xValue         
            self.emit(SIGNAL("data(PyQt_PyObject)"), array(data_point))  
            time.sleep(1)
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = WireSweep()
    form.show()
    app.exec_()
