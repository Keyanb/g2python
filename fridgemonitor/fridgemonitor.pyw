
# Changes to make:
# Switch to QThread
# Switch to 6 subplots in one figure
# add print function
# add button to set heater


from PyQt4.QtCore import *
from PyQt4.QtGui import *


import ui_fridgemonitor
import LS370
import HP4263B
import MKS
import time
import textmsg
import chart_recorder as cr
import pyfile as config_file_reader
import numpy as np
import matplotlib.pyplot as plt
import fridgemonthread

class FridgeMonitorWindow(QMainWindow, ui_fridgemonitor.Ui_FridgeMonitorWindow):

    def __init__(self, parent=None):
        super(FridgeMonitorWindow, self).__init__()
        self.setupUi(self)
        self.connect(self.alarmCheckBox, SIGNAL("stateChanged(int)"), self.change_alarm)       
        self.connect (self.htrRangeComboBox, SIGNAL("currentIndexChanged(int)"), self.set_htr_range)
        self.connect (self.htrOutputLineEdit, SIGNAL ("editingFinished()"), self.set_htr_output)

        self.mutex = QMutex()         
        self.dataThread = fridgemonthread.FridgeMonThread(self.mutex, self)  
        self.connect(self.dataThread, SIGNAL("data(PyQt_PyObject)"),
                     self.handle_data)

        self.ALARM_ON = self.alarmCheckBox.isChecked()
        self.MIN_1K_POT = 1700
        self.MAX_1K_POT = 2000
        self.t_warning = 0
        self.warning1_sent=False
        self.warning2_sent=False
        
        self.debug = config_file_reader.get_debug_setting()
        self.msg = config_file_reader.get_msg_info()

        self.htr_val = 0
        self.htr_range = 0
        self.htr_changed = False

        
        self.channels = {}
        self.chan_dict = {'title': 0, 'subplot': 1}
        
        self.channels['LS_1'] = {'title':'1K pot', 'subplot':1}
        self.channels['LS_2'] = {'title':'Still', 'subplot':3}
        self.channels['LS_3'] = {'title':'ICP', 'subplot':5}
        self.channels['LS_4'] = {'title':'MC', 'subplot':7}
        self.channels['LS_5'] = {'title':'Mats', 'subplot':2}
        self.channels['LS_9'] = {'title':'RuO 2k', 'subplot':4}
        self.channels['CMN'] = {'title':'CMN', 'subplot':6}
        #self.channels[8] = ["", 8]
        self.setup_plot()
        
    def setup_plot(self):
        self.mplwidget.figure.clear()
        
        for idx in self.channels:
            chan = self.channels[idx]
            chan['axes'] = self.mplwidget.figure.add_subplot(4, 2, chan['subplot'])
            chan['line'], = chan['axes'].plot(0,0)
            
            chan['axes'].set_ylabel (chan['title'])
            chan['axes'].tick_params(axis='x', labelsize=8)
            chan['axes'].tick_params(axis='y', labelsize=8)  
        self.mplwidget.figure.subplots_adjust(left = 0.05, right = 0.95, top = 0.95)           
           
    def handle_data(self, data):
        name,data = data
        print name, data
        line = self.channels[name]['line']
        axes = self.channels[name]['axes']
        line.set_xdata(np.append(line.get_xdata(), time.time()))
        line.set_ydata(np.append(line.get_ydata(), data))

        axes.relim()
        axes.autoscale_view()    
        self.mplwidget.figure.canvas.draw()  
        
        if name == 'LS_1':
            self.check_alarm(data)                
        
        
    def change_alarm(self):
        self.ALARM_ON = self.alarmCheckBox.isChecked()
        print self.ALARM_ON
    
    def set_htr_range(self):
        self.htr_range = self.htrRangeComboBox.currentIndex()
        self.htr_changed = True
        
    
    def set_htr_output(self):
        try:
            val = float(self.htrOutputLineEdit.text())
            if val < 0:
                self.htrOutputLineEdit.setText("0.0")
                val = 0
            if val > 100:
                self.htrOutputLineEdit.setText("100.0")
                val = 100.0
            self.htr_val = val
            self.htr_changed = True   
        except ValueError:
            self.htrOutputLineEdit.setText(str(self.htr_val))
        
        
    def CMN_calc(self,raw_value):
        return -4.36894/(-raw_value*1000+2.93629)

    def check_alarm(self, dat):
        if dat > self.MAX_1K_POT and self.warning1_sent == False:
            self.msg['BODY'] = "1K pot is too cold: %.3f"%dat
            textmsg.send_txt(self.msg)
            self.warning1_sent=True
            self.t_warning = self.t_current
        elif dat < self.MIN_1K_POT and self.warning2_sent == False:
            self.msg['BODY'] = "1K pot is too warm: %.3f"%dat
            textmsg.send_txt(self.msg)
            self.warning2_sent=True
            self.t_warning = self.t_current
        elif self.t_current - self.t_warning > 900: #resend warning up to every 15 minutes
            self.warning1_sent=False
            self.warning2_sent=False        
                    
    def main_loop(self):
     
        CMN_cr = cr.cr(8,"CMN", '.-b')
        
        active_channels = ([[1,cr.cr(1,'1K pot')],[2,cr.cr(3, 'Still','.-g')],
                        [3,cr.cr(5, 'ICP','.-r')], [4,cr.cr(7, 'MC','.-k')],
                        [5,cr.cr(2, 'Mats','.-c')],[9,cr.cr(4, 'Cold Plate','.-m')]])
        
        out_file, out_file_name = config_file_reader.open_therm_file()
        self.fileNameLineEdit.setText(out_file_name)

        t_start = time.time()
        out_file.write("#T_start = " + str(t_start))
        #out_file.write("
        TIME_STEP = 10

        for chan in active_channels:
            #ax = chan[1].learn_axes(fig,4,2)
            if chan[1].subplot_num == 1:    
                ax = self.mplwidget.axes
                fig = self.mplwidget.figure
            elif chan[1].subplot_num == 2:    
                ax = self.mplwidget_2.axes
                fig = self.mplwidget_2.figure 
            elif chan[1].subplot_num == 3:    
                ax = self.mplwidget_3.axes
                fig = self.mplwidget_3.figure 
            elif chan[1].subplot_num == 4:    
                ax = self.mplwidget_4.axes
                fig = self.mplwidget_4.figure 
            elif chan[1].subplot_num == 5:    
                ax = self.mplwidget_5.axes
                fig = self.mplwidget_5.figure 
            elif chan[1].subplot_num == 6:    
                ax = self.mplwidget_6.axes
                fig = self.mplwidget_6.figure 
            elif chan[1].subplot_num == 7:    
                ax = self.mplwidget_7.axes
                fig = self.mplwidget_7.figure 
            elif chan[1].subplot_num == 8:    
                ax = self.mplwidget_8.axes
                fig = self.mplwidget_8.figure     
                
            chan[1].set_axes(fig, ax)
            
            ax.tick_params(axis='x', labelsize=8)
            ax.tick_params(axis='y', labelsize=8)
            fig.subplots_adjust(left = 0.15, right = 0.99)
            #ax.set_ylabel ("test")
            fig.canvas.draw()
            
        #ax = CMN_cr.learn_axes(fig,4,2)
        ax = self.mplwidget_6.axes
        fig = self.mplwidget_6.figure 
        CMN_cr.set_axes(fig, ax)
        
        ax.tick_params(axis='x', labelsize=8)
        ax.tick_params(axis='y', labelsize=8)                
        
        warning1_sent=False
        warning2_sent=False
        t_warning = 0
        
        times = np.array([])
    
    
        while (self.running):
            t_current = time.time() - t_start
            
            times = np.append(times,t_current)
            stri = "%.1f, "%(t_current)
            
            CMN.trigger()
            
            for idx, chan in enumerate(active_channels):
                lakeshore.scanner_to_channel(chan[0])
                time.sleep(TIME_STEP)
                dat = lakeshore.read_channel(chan[0])
                stri += "%.3f, "%dat            
                chan[1].add_point(t_current, dat)                

                if self.htr_changed:
                    lakeshore.set_heater_range(self.htr_range)
                    lakeshore.set_heater_output(self.htr_val)                
                    self.htr_changed = False                       
                
                if self.running == False:
                    break
            
            CMN_temp = CMN.read_data()
            CMN_stri = "%.6f, %.3f"%(CMN_temp*1000, self.CMN_calc(CMN_temp))                 
            CMN_cr.add_point(t_current, self.CMN_calc(CMN_temp))
            
            stri += CMN_stri + str(self.htr_range) + ", " + str(self.htr_val) + "\n"
            
            print(stri)
            out_file.write(stri)
         
        out_file.close()
        lakeshore.close()
        pirani.close()
        
        print "finished"

    @pyqtSignature("")
    def on_startStopButton_clicked(self):

        if self.dataThread.isStopped():    
            self.t_start = time.time()           
            
            self.lakeshore = LS370.LS370('GPIB::12', self.debug)
            self.CMN = HP4263B.HP4263B('GPIB::17', self.debug)
            self.pirani = MKS.MKS_gauge('COM3', self.debug) #'/dev/ttyUSB0'
            
            self.dataThread.initialize(self.lakeshore, self.CMN, self.pirani, self.debug) 
            self.dataThread.start()
            
            self.startStopButton.setText("Stop")          
        else:
            self.dataThread.stop()
            self.lakeshore.close()
            self.CMN.close()
            self.pirani.close()
            
            self.out_file.close()
            self.startStopButton.setText("Start")   
         
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = FridgeMonitorWindow()
    #form.connect(form, SIGNAL("found"), found)
    #form.connect(form, SIGNAL("notfound"), nomore)
    #form.plot([0,1,2,3,4], [0,1,2,3,])
    form.show()
    app.exec_()

