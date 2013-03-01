# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 11:25:22 2013

@author: Ben
"""

from PyQt4 import QtCore, QtGui
from matplotlibwidget import MatplotlibWidget
import numpy as np

class MatplotlibZoomWidget(MatplotlibWidget):


    SI_prefixes = {-15: 'a', -12: 'p', -9: 'n', -6: 'u', -3: 'm', 0: '', 3: 'k', 6:'M', 9:'G'} 
    
    def __init__(self, parent=None, title='', xlabel='', ylabel='',
                 xlim=None, ylim=None, xscale='linear', yscale='linear',
                 width=4, height=3, dpi=100, hold=False):                
        super(MatplotlibZoomWidget, self).__init__(parent, title, xlabel, ylabel,
         xlim, ylim, xscale, yscale, width, height, dpi, hold)
        self.axesR = self.axes.twinx()
        self.left_pow = 0
        self.right_pow = 0
         
        self.active_axes = self.axes
        
        # Shink current axis by 20%
        #box = self.axes.get_position()
        #axes.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        
        # Put a legend to the right of the current axis
        #self.legend = self.axes.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        
    def toggle_left_axes(self):
        self.active_axes = self.axes

    def toggle_right_axes(self):
        self.active_axes = self.axesR
        print "toggled!"
    
    def check_scale(self, ax):
        ymin, ymax = ax.get_ylim()
        if max (abs(ymin), abs(ymax)) > 1000:
            return 3
        elif max (abs(ymin), abs(ymax)) < 1:
            return -3
        else:
            return 0
            
    def adjust_units(self):
        chk = self.check_scale(self.axes)
        if chk !=0:
            self.left_pow += chk
            self.axes.set_ylim(np.array(self.axes.get_ylim()) / 10 ** chk)  
            self.axes.set_ylabel ("Voltage (%sV)"%self.SI_prefixes[self.left_pow])
            self.adjust_units(self)
            
    def rescale_and_draw(self):
        self.adjust_units()
        self.axes.relim()
        self.axes.autoscale_view() 
        self.axesR.relim()
        self.axesR.autoscale_view()                      
        self.figure.canvas.draw()        
    
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.__mousePressX = event.x()
            self.__mousePressY = event.y()
            self.__startingXLim = self.active_axes.get_xlim()
            self.__startingYLim = self.active_axes.get_ylim()
            self.__xScale = -(self.__startingXLim[1] - self.__startingXLim[0])/self.width()
            self.__yScale = (self.__startingYLim[1] - self.__startingYLim[0])/self.height()
            
        self.emit(QtCore.SIGNAL("mousePressed(PyQt_PyObject)"), [self.__mousePressX, self.__mousePressY]) 
        super(MatplotlibZoomWidget, self).mousePressEvent(event)

        
    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.active_axes.set_xlim(self.__startingXLim + self.__xScale * (event.x() - self.__mousePressX))
            self.active_axes.set_ylim(self.__startingYLim + self.__yScale * (event.y() - self.__mousePressY)) 
            self.rescale_and_draw() 

        super(MatplotlibZoomWidget, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        #if self.__mousePressPos is not None:
        super(MatplotlibZoomWidget, self).mouseReleaseEvent(event)
        
    def wheelEvent(self, event):
        #zoom 10% for each "click" of scroll wheel
        zoom = 1 - event.delta()/1200.0
        
        # correct for difference in coordinate systems (note Y is top left in widget, bottom left in figure)
        inv = self.axes.transData.inverted()      
        X,Y = inv.transform((event.x(), self.height() - event.y()))      
        
        xlim = self.active_axes.get_xlim()
        ylim = self.active_axes.get_ylim()
        
        if event.buttons() == QtCore.Qt.LeftButton:
            self.active_axes.set_xlim(X - zoom * (X - xlim[0]), X - zoom * (X - xlim[1]))
        elif event.buttons() == QtCore.Qt.RightButton:    
            self.active_axes.set_ylim(Y - zoom * (Y - ylim[0]), Y - zoom * (Y - ylim[1]))
        else:
            self.active_axes.set_xlim(X - zoom * (X - xlim[0]), X - zoom * (X - xlim[1]))
            self.active_axes.set_ylim(Y - zoom * (Y - ylim[0]), Y - zoom * (Y - ylim[1]))
            
        self.rescale_and_draw()    
        super(MatplotlibZoomWidget, self).wheelEvent(event)

    def keyPressEvent(self, event):
        print ("hmmm")
        key = event.key()
        if key == QtCore.Qt.Key_Left: 
            x_min, x_max = self.active_axes.get_xlim()
            full_scale = x_max - x_min
            self.active_axes.set_xlim(xmin - 0.1*full_scale, xmax - 0.1*full_scale)
        elif key == QtCore.Qt.Key_Right:
            x_min, x_max = self.active_axes.get_xlim()
            full_scale = x_max - x_min
            self.active_axes.set_xlim(xmin + 0.1*full_scale, xmax + 0.1*full_scale)
        elif key == QtCore.Qt.Key_Up:
            y_min, y_max = self.active_axes.get_ylim()
            full_scale = y_max - y_min
            self.active_axes.set_xlim(ymin + 0.1*full_scale, ymax + 0.1*full_scale)
        elif key == QtCore.Qt.Key_Down:
            y_min, y_max = self.active_axes.get_ylim()
            full_scale = y_max - y_min
            self.active_axes.set_xlim(ymin + 0.1*full_scale, ymax + 0.1*full_scale)
        else:
            return
            
        self.rescale_and_draw() 
        
        super(MatplotlibZoomWidget, self).keyEvent(event)
        
    def focusInEvent(self, event):
        print ("focus!")
        super(MatplotlibZoomWidget, self).focusInEvent(event)    