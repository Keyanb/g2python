# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'recordsweep.ui'
#
# Created: Thu Feb 14 21:23:51 2013
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RecordSweepWindow(object):
    def setupUi(self, RecordSweepWindow):
        RecordSweepWindow.setObjectName(_fromUtf8("RecordSweepWindow"))
        RecordSweepWindow.resize(1035, 600)
        RecordSweepWindow.setWindowTitle(QtGui.QApplication.translate("RecordSweepWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(RecordSweepWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.mplwidget = MatplotlibWidget(self.centralwidget)
        self.mplwidget.setGeometry(QtCore.QRect(0, 0, 641, 571))
        self.mplwidget.setObjectName(_fromUtf8("mplwidget"))
        self.startStopButton = QtGui.QPushButton(self.centralwidget)
        self.startStopButton.setGeometry(QtCore.QRect(700, 10, 75, 23))
        self.startStopButton.setText(QtGui.QApplication.translate("RecordSweepWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.startStopButton.setObjectName(_fromUtf8("startStopButton"))
        self.groupBox_Y = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_Y.setGeometry(QtCore.QRect(940, 80, 31, 191))
        self.groupBox_Y.setTitle(QtGui.QApplication.translate("RecordSweepWindow", "Y", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_Y.setObjectName(_fromUtf8("groupBox_Y"))
        self.groupBox_X = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_X.setGeometry(QtCore.QRect(910, 80, 31, 191))
        self.groupBox_X.setTitle(QtGui.QApplication.translate("RecordSweepWindow", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_X.setObjectName(_fromUtf8("groupBox_X"))
        self.groupBox_Type = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_Type.setGeometry(QtCore.QRect(730, 80, 101, 191))
        self.groupBox_Type.setTitle(QtGui.QApplication.translate("RecordSweepWindow", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_Type.setObjectName(_fromUtf8("groupBox_Type"))
        self.groupBox_Name = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_Name.setGeometry(QtCore.QRect(650, 80, 81, 191))
        self.groupBox_Name.setTitle(QtGui.QApplication.translate("RecordSweepWindow", "Channel Name", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_Name.setObjectName(_fromUtf8("groupBox_Name"))
        self.groupBox_Instr = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_Instr.setGeometry(QtCore.QRect(830, 80, 81, 191))
        self.groupBox_Instr.setTitle(QtGui.QApplication.translate("RecordSweepWindow", "Instrument", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_Instr.setObjectName(_fromUtf8("groupBox_Instr"))
        RecordSweepWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(RecordSweepWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1035, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        RecordSweepWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(RecordSweepWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        RecordSweepWindow.setStatusBar(self.statusbar)

        self.retranslateUi(RecordSweepWindow)
        QtCore.QMetaObject.connectSlotsByName(RecordSweepWindow)

    def retranslateUi(self, RecordSweepWindow):
        pass

from matplotlibwidget import MatplotlibWidget
