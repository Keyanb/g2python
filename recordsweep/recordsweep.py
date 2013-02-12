# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 13:18:32 2012

@author: Benjamin Schmidt
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import ui_recordsweep
import LS370, HP4263B, MKS
import time
import threading
import chart_recorder as cr
import numpy as np
import SRS830
import IPS120
import readconfigfile
import string
from pylab import *

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class RecordSweepWindow(QMainWindow, ui_recordsweep.Ui_RecordSweepWindow):
    def __init__(self, parent=None):
        super(RecordSweepWindow, self).__init__()
        self.setupUi(self)
        
        #self.connect(self.alarmCheckBox, SIGNAL("stateChanged(int)"), self.changeAlarm)       
        #self.connect (self.htrRangeComboBox, SIGNAL("currentIndexChanged(int)"), self.set_htr_range)
        #self.connect (self.htrOutputLineEdit, SIGNAL ("editingFinished()"), self.set_htr_output)

        self.running = False
        self.T = threading.Thread(target=self.main_loop)
        self.T.daemon = True
        #self.ALARM_ON = self.alarmCheckBox.isChecked()

        #self.debug = config_file_reader.get_debug_setting()
        #self.msg = config_file_reader.get_msg_info()      

    def main_loop(self):
        
        using_magnet = True
        MEAS_TIME = 3
        DEBUG = True

        #instrumentation setup
        self.instruments = {}
        self.instruments['GPIB::8'] = SRS830.SRS830('GPIB::8', debug=DEBUG)
        
        # tuple: lockin #, channel, subplot for display
        self.data_channels = (['GPIB::8',1,1, array([])], ['GPIB::8',2,2, array([])])
        
 
        
        if using_magnet==True:
            self.magnet = IPS120.IPS120('GPIB::26', debug=DEBUG)
            self.fields= array([])
            
        #open file, write header
        out_file = readconfigfile.open_data_file()
        t_start = time.time()
        out_file.write('Starting time: ' + str(t_start) + '\n')
        out_file.write('time, field, X1, Y1, X2, Y2, X3, Y3\n')
        
        self.ax = self.mplwidget.axes
        self.fig = self.mplwidget.figure
        self.line = []
        
        for idx, chan in enumerate(self.data_channels):
            tline, = self.ax.plot(0, 0, '.-')
            self.line.append(tline)          
            
        self.ax.tick_params(axis='x', labelsize=8)
        self.ax.tick_params(axis='y', labelsize=8)

        self.fig.canvas.draw()   
        
        running = True
        t_start = time.time()
        while running == True:
            t_str = "%.1f, "%(time.time() - t_start)
            s2 = self.read_data(t_start, using_magnet)
            output_string = t_str + s2 + "\n"
            out_file.write(output_string)
            print output_string
            time.sleep(MEAS_TIME)
            
        out_file.close()

        for inst in self.instruments:
            inst.close()
        
        if using_magnet==True:
            self.magnet.close()

    def auto_scale_y(self,data):
        span = max(data.max() - data.min(), 0.1 * data.min())
        return (data.min() - span *0.05), (data.max() + span*0.05)
    
    def read_data(self, t_start, using_magnet):
        output_line = ""
        t_current= time.time() - t_start
    
        if using_magnet==True:
            current_field = self.magnet.read_field()
            output_line = output_line + "%.5f"%current_field
            self.fields = append(self.fields, current_field)
            
        #read 3 lock-ins
        for idx, chan in enumerate(self.data_channels):
            if chan[1] <5:
                dat = self.instruments[chan[0]].read_input(chan[1])
            else:
                dat = self.instruments[chan[0]].read_aux(chan[1]-4)
            
            output_line = output_line + ', %.6e'%dat
            
            chan[3] = append(chan[3],dat)
                     
            self.line[idx].set_data(arange(chan[3].size), chan[3])
    
            y1, y2 = self.auto_scale_y(chan[3])
            self.ax.set_ylim(ymin = y1, ymax = y2)
            self.ax.set_xlim(xmin=0, xmax = chan[3].size-1)
        self.fig.canvas.draw()
                     
        #output_line = output_line + str(lakeshore.read_channel(9))    
    
        return output_line
        
    @pyqtSignature("")
    def on_startStopButton_clicked(self):
        if self.running == True:
            self.running = False
            self.startStopButton.setText("Start")
        else:
            if not self.T.isAlive():            
                self.T.start()
            self.running = True
            self.startStopButton.setText("Stop")           
        print ("Click!") 
             
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = RecordSweepWindow()
    #form.connect(form, SIGNAL("found"), found)
    #form.connect(form, SIGNAL("notfound"), nomore)
    #form.plot([0,1,2,3,4], [0,1,2,3,])
    form.show()
    app.exec_()
