# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'recordsweep.ui'
#
# Created: Tue Feb 12 11:30:46 2013
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
        RecordSweepWindow.resize(966, 600)
        RecordSweepWindow.setWindowTitle(QtGui.QApplication.translate("RecordSweepWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(RecordSweepWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.mplwidget = MatplotlibWidget(self.centralwidget)
        self.mplwidget.setGeometry(QtCore.QRect(0, 0, 691, 571))
        self.mplwidget.setObjectName(_fromUtf8("mplwidget"))
        self.startStopButton = QtGui.QPushButton(self.centralwidget)
        self.startStopButton.setGeometry(QtCore.QRect(700, 10, 75, 23))
        self.startStopButton.setText(QtGui.QApplication.translate("RecordSweepWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.startStopButton.setObjectName(_fromUtf8("startStopButton"))
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(710, 140, 181, 211))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 179, 209))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.radioButton = QtGui.QRadioButton(self.scrollAreaWidgetContents)
        self.radioButton.setGeometry(QtCore.QRect(10, 10, 82, 17))
        self.radioButton.setText(QtGui.QApplication.translate("RecordSweepWindow", "RadioButton", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        RecordSweepWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(RecordSweepWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 966, 21))
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
