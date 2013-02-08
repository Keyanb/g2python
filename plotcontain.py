# -*- coding: utf-8 -*-
"""
Created on Wed Dec 05 10:40:42 2012
This program should create a simple qt plot which data cna be pushed to
@author: keyan
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import matplot
import sys

class graph(matplot.Ui_MainWindow,QMainWindow):
    def __init__(self,parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.axes = self.mplwidget.figure.add_subplot(111)
        
    def plotdata(self,xdata,ydata):
        ax = self.axes
        self.mplwidget.axes.plot(xdata,ydata)
        self.mplwidget.draw()
        self.show()
        
        
app = QApplication(sys.argv)
myapp = graph()
myapp.show()
app.exec_()