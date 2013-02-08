# -*- coding: utf-8 -*-
"""
Created on Wed Dec 05 10:40:42 2012
This program should create a simple qt plot which data cna be pushed to
@author: keyan
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import matplot
import sys, os, random, time
import Queue

from livedatafeed import LiveDataFeed

class graph(matplot.Ui_MainWindow,QMainWindow):
    def __init__(self,parent=None):
        
        super(graph, self).__init__(parent)
        self.setupUi(self)
                
        # Initialize some variables
        self.monitor_active = False
        self.x = [0]
        self.y = [0]
        
        self.livedata = LiveDataFeed()
        self.data_q = Queue.Queue
        
        # Set up the Axes
        self.axes = self.mplwidget.figure.add_subplot(111)
        self.axes.hold(False)
        
        # GUI update timer
        timer = QTimer(self)
        QObject.connect(timer, SIGNAL("timeout()"), self.update_figure)
        timer.start(1000)
        
        
    def update_figure(self):
        """ Updates the state of the window with new 
            data. The livefeed is used to find out whether new
            data was received since the last update. If not, 
            nothing is updated.
        """
         if self.livefeed.has_new_data:
            data = self.livefeed.read_data()
            self.x.append((data['gate']))
            self.y.append((data['voltage']))
            # I think this enables the 'scrolling' type data view
            # if len(self.temperature_samples) > 100:
              #  self.temperature_samples.pop(0)
              
            self.axes.plot(self.x,self.y)
            self.mplwidget.draw()
            self.show()