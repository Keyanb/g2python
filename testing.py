# -*- coding: utf-8 -*-
"""
Created on Wed Dec 05 11:30:01 2012

@author: keyan
"""
from dasplot import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time



x = [0,1,2,3,4,5,6]
y = [6,5,3,5,6,7,5]


app = QApplication(sys.argv)
myapp = graph()
myapp.show()
app.exec_()

time.sleep(3)
print "Calling update"
myapp.plotdata(x,y)
print "Called Update"
time.sleep(3)

y = [3,2,1,3,2,4,3]

myapp.plotdata(x,y)