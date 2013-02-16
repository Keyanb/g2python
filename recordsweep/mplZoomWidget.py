# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 11:25:22 2013

@author: Ben
"""

from PyQt4 import QtCore, QtGui
from matplotlibwidget import MatplotlibWidget

class MatplotlibZoomWidget(MatplotlibWidget):

    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == QtCore.Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()
            self.__mousePressX = event.x()
            self.__mousePressY = event.y()
            self.__startingXLim = self.axes.get_xlim()
            self.__startingYLim = self.axes.get_ylim()
            self.__xScale = -(self.__startingXLim[1] - self.__startingXLim[0])/self.width()
            self.__yScale = (self.__startingYLim[1] - self.__startingYLim[0])/self.height()
            
        self.emit(QtCore.SIGNAL("mousePressed(PyQt_PyObject)"), [self.__mousePressX, self.__mousePressY]) 
        super(MatplotlibZoomWidget, self).mousePressEvent(event)

        
    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.axes.set_xlim(self.__startingXLim + self.__xScale * (event.x() - self.__mousePressX))
            self.axes.set_ylim(self.__startingYLim + self.__yScale * (event.y() - self.__mousePressY)) 
            self.figure.canvas.draw()

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
        
        xlim = self.axes.get_xlim()
        ylim = self.axes.get_ylim()

        self.axes.set_xlim(X - zoom * (X - xlim[0]), X - zoom * (X - xlim[1]))
        self.axes.set_ylim(Y - zoom * (Y - ylim[0]), Y - zoom * (Y - ylim[1]))
   
        self.figure.canvas.draw()    
        super(MatplotlibZoomWidget, self).wheelEvent(event)
 