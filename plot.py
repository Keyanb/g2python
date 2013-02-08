# -*- coding: utf-8 -*-
"""
Created on Wed Sep 05 14:30:55 2012


"""
from matplotlib import *
from pylab import *


class basicplot:
    
    def __init__(self):
        ion()
        self.fig = figure()
        self.ax = self.fig.add_subplot(111)
        self.x = []
        self.y = []
        self.fig.canvas.draw()
        
    def setTitle(self,title):
        self.fig.canvas.set_window_title(title)
        self.fig.canvas.draw()
        
    def addPoint(self,x_value,y_value):
        self.x.append(x_value)
        self.y.append(y_value)
        self.ax.plot(self.x,self.y)
        self.fig.canvas.draw()
        
        
        