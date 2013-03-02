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

        self.axes.tick_params(axis='x', labelsize=8)
        self.axes.tick_params(axis='y', labelsize=8)
        self.axesR.tick_params(axis='x', labelsize=8)
        self.axesR.tick_params(axis='y', labelsize=8)
        
        self.auto_scale_X_on = True
        self.auto_scale_L_on = True
        self.auto_scale_R_on = True
        
        self.control_X_on = True
        self.control_L_on = True
        self.control_R_on = True
        # Shink current axis by 20%
        #box = self.axes.get_position()
        #axes.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        
        # Put a legend to the right of the current axis
        #self.legend = self.axes.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        
    def setActiveAxes(self, control_X_on = True, control_L_on = True, control_R_on= True):
        self.control_X_on = control_X_on
        self.control_L_on = control_L_on
        self.control_R_on = control_R_on
        
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
            self.adjust_units()
            
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
            
            self.__startingXLim = self.axes.get_xlim()
            self.__xScale = -(self.__startingXLim[1] - self.__startingXLim[0])/self.width()
            
            self.__startingYLim_L = self.axes.get_ylim()
            self.__yScale_L = (self.__startingYLim_L[1] - self.__startingYLim_L[0])/self.height()

            self.__startingYLim_R = self.axes.get_ylim()
            self.__yScale_R = (self.__startingYLim_R[1] - self.__startingYLim_R[0])/self.height()
            
        self.emit(QtCore.SIGNAL("mousePressed(PyQt_PyObject)"), [self.__mousePressX, self.__mousePressY]) 
        super(MatplotlibZoomWidget, self).mousePressEvent(event)

        
    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if self.control_X_on:                
                self.axes.set_xlim(self.__startingXLim + self.__xScale * (event.x() - self.__mousePressX))
            if self.control_L_on:
                self.axes.set_ylim(self.__startingYLim_L + self.__yScale_L * (event.y() - self.__mousePressY))             
            if self.control_R_on:
                self.axesR.set_ylim(self.__startingYLim_R + self.__yScale_R * (event.y() - self.__mousePressY))                 
            self.rescale_and_draw()
            
        super(MatplotlibZoomWidget, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        #if self.__mousePressPos is not None:
        super(MatplotlibZoomWidget, self).mouseReleaseEvent(event)
        
    def wheelEvent(self, event):
        #zoom 10% for each "click" of scroll wheel
        zoom = 1 - event.delta()/1200.0

  
        if self.control_X_on or event.buttons() == QtCore.Qt.LeftButton:
            ax = self.axes
            inv = ax.transData.inverted()          
            X,Y = inv.transform((event.x(), self.height() - event.y())) 
            xlim = ax.get_xlim()
            ax.set_xlim(X - zoom * (X - xlim[0]), X - zoom * (X - xlim[1])) 
                            

        for ax, on in zip ([self.axes, self.axesR], [self.control_L_on, self.control_R_on]):
            if on:
                # correct for difference in coordinate systems (note Y is top left in widget, bottom left in figure)        
                inv = ax.transData.inverted()      
                X,Y = inv.transform((event.x(), self.height() - event.y()))      

                ylim = ax.get_ylim()
                
                ax.set_ylim(Y - zoom * (Y - ylim[0]), Y - zoom * (Y - ylim[1]))
                    
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