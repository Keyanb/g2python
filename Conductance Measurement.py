# -*- coding: utf-8 -*-
"""
Created on Tue May 15 16:39:11 2012

@author: Bram
"""

# Use this command to compile interface pyuic4 -x plotter.ui -o plotter.py
import sys
import matplotlib
import measurement
import time
import threading
from pylab import *
from plotter import Ui_MainWindow
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
from PyQt4 import QtCore

class MyForm(QMainWindow,Ui_MainWindow):
        def __init__(self, parent=None):
                #build parent user interface
               QMainWindow.__init__(self, parent)
               self.setupUi(self)
               self.connect(self.goButton, SIGNAL('clicked()'),self.go)
               self.connect(self.quit, SIGNAL('clicked()'),self.closeProgram)
               
        def go(self):
            print "Starting Measurement..."
            threading.Thread(target=self.do_start, name="_gen_").start()
            
        def do_start(self):

            delay = self.delay.value()
            max_gate = self.maxGate.value()
            stepsize = self.stepSize.value()
            gate_voltage = 0
            windowlower = self.windowlower.value()
            windowupper = self.windowupper.value()
            windowstep = self.windowstep.value()
            
            ax = self.mplwidget.figure.add_subplot(111)
            print "Window %f to %f" % (windowlower, windowupper)
            print "Step Size: %f" % stepsize
            out_file = open ('test.txt', 'w')
            print 'Gate\t Conductance\t X-Value\t Temperature\t Time'
            out_file.write('Gate\t Conductance\t X-Value\t Temperature\t Time \n') 
            x = []
            y = []
            # Sweep Up Gate
            while gate_voltage > max_gate:       
                measurement.setNextGate(gate_voltage)
                time.sleep(delay)
                data = measurement.read(gate_voltage)
                x.append(gate_voltage)
                y.append(data[1])
                print "%f \t %f \t %r \t %f \t %f" % (data[0], data[1], data[2], data[3], data[4])
                out_file.write("%f \t %f \t %r \t %f \t %f \n" % (data[0], data[1], data[2], data[3],data[4]))
                self.mplwidget.axes.plot(x,y)
                self.gate_display.display(gate_voltage)
                self.conductance.display(data[1])
                self.time.display(data[4])
                self.temp.display(data[3])
                self.mplwidget.draw()
                self.show()
                
                if (gate_voltage <= windowlower and gate_voltage >= windowupper):
                    gate_voltage = gate_voltage - windowstep
                else:
                    gate_voltage = gate_voltage - stepsize   
                
        
            ## Sweep Down Gate
            while gate_voltage <= 0:            
                measurement.setNextGate(gate_voltage)
                time.sleep(delay)
                data = measurement.read(gate_voltage)
                x.append(gate_voltage)
                y.append(data[1])
                print "%f \t %f \t %r \t %f \t %f" % (data[0], data[1], data[2], data[3], data[4])
                out_file.write("%f \t %f \t %r \t %f \t %f \n" % (data[0], data[1], data[2], data[3],data[4])) 
                self.mplwidget.axes.plot(x,y)
                self.gate_display.display(gate_voltage)
                self.conductance.display(data[1])
                self.time.display(data[4])
                self.temp.display(data[3])
                self.mplwidget.draw()
                self.show()
                
                if (gate_voltage <= windowlower and gate_voltage >= windowupper):
                    gate_voltage = gate_voltage + windowstep
                else:
                    gate_voltage = gate_voltage + stepsize  
                
        def closeProgram(self):
            qApp.exit(0)
        
            
if __name__ == "__main__":
        #This function means this was run directly, not called from another python file.
        app = QApplication(sys.argv)
        myapp = MyForm()
        myapp.show()
        sys.exit(app.exec_())
    