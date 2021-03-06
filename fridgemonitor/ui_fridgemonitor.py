# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fridgemonitor.ui'
#
# Created: Thu Mar 28 19:27:20 2013
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_FridgeMonitorWindow(object):
    def setupUi(self, FridgeMonitorWindow):
        FridgeMonitorWindow.setObjectName(_fromUtf8("FridgeMonitorWindow"))
        FridgeMonitorWindow.resize(1249, 714)
        FridgeMonitorWindow.setWindowTitle(QtGui.QApplication.translate("FridgeMonitorWindow", "Thermometry", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(FridgeMonitorWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.mplwidget = MatplotlibWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.mplwidget.setFont(font)
        self.mplwidget.setObjectName(_fromUtf8("mplwidget"))
        self.horizontalLayout_4.addWidget(self.mplwidget)
        self.frame = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.fileNameLabel = QtGui.QLabel(self.frame)
        self.fileNameLabel.setText(QtGui.QApplication.translate("FridgeMonitorWindow", "File:", None, QtGui.QApplication.UnicodeUTF8))
        self.fileNameLabel.setObjectName(_fromUtf8("fileNameLabel"))
        self.horizontalLayout.addWidget(self.fileNameLabel)
        self.fileNameLineEdit = QtGui.QLineEdit(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileNameLineEdit.sizePolicy().hasHeightForWidth())
        self.fileNameLineEdit.setSizePolicy(sizePolicy)
        self.fileNameLineEdit.setObjectName(_fromUtf8("fileNameLineEdit"))
        self.horizontalLayout.addWidget(self.fileNameLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.startStopButton = QtGui.QPushButton(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startStopButton.sizePolicy().hasHeightForWidth())
        self.startStopButton.setSizePolicy(sizePolicy)
        self.startStopButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.startStopButton.setText(QtGui.QApplication.translate("FridgeMonitorWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.startStopButton.setObjectName(_fromUtf8("startStopButton"))
        self.verticalLayout.addWidget(self.startStopButton)
        self.alarmCheckBox = QtGui.QCheckBox(self.frame)
        self.alarmCheckBox.setText(QtGui.QApplication.translate("FridgeMonitorWindow", "Send text messages", None, QtGui.QApplication.UnicodeUTF8))
        self.alarmCheckBox.setObjectName(_fromUtf8("alarmCheckBox"))
        self.verticalLayout.addWidget(self.alarmCheckBox)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.htrOutputLabel = QtGui.QLabel(self.frame)
        self.htrOutputLabel.setText(QtGui.QApplication.translate("FridgeMonitorWindow", "Heater output:", None, QtGui.QApplication.UnicodeUTF8))
        self.htrOutputLabel.setObjectName(_fromUtf8("htrOutputLabel"))
        self.horizontalLayout_3.addWidget(self.htrOutputLabel)
        self.htrOutputLineEdit = QtGui.QLineEdit(self.frame)
        self.htrOutputLineEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.htrOutputLineEdit.setObjectName(_fromUtf8("htrOutputLineEdit"))
        self.horizontalLayout_3.addWidget(self.htrOutputLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.htrRangeLabel = QtGui.QLabel(self.frame)
        self.htrRangeLabel.setText(QtGui.QApplication.translate("FridgeMonitorWindow", "Heater Range:", None, QtGui.QApplication.UnicodeUTF8))
        self.htrRangeLabel.setObjectName(_fromUtf8("htrRangeLabel"))
        self.horizontalLayout_2.addWidget(self.htrRangeLabel)
        self.htrRangeComboBox = QtGui.QComboBox(self.frame)
        self.htrRangeComboBox.setObjectName(_fromUtf8("htrRangeComboBox"))
        self.htrRangeComboBox.addItem(_fromUtf8(""))
        self.htrRangeComboBox.setItemText(0, QtGui.QApplication.translate("FridgeMonitorWindow", "OFF", None, QtGui.QApplication.UnicodeUTF8))
        self.htrRangeComboBox.addItem(_fromUtf8(""))
        self.htrRangeComboBox.setItemText(1, QtGui.QApplication.translate("FridgeMonitorWindow", "31.6 uA", None, QtGui.QApplication.UnicodeUTF8))
        self.htrRangeComboBox.addItem(_fromUtf8(""))
        self.htrRangeComboBox.setItemText(2, QtGui.QApplication.translate("FridgeMonitorWindow", "100 uA", None, QtGui.QApplication.UnicodeUTF8))
        self.htrRangeComboBox.addItem(_fromUtf8(""))
        self.htrRangeComboBox.setItemText(3, QtGui.QApplication.translate("FridgeMonitorWindow", "316 uA", None, QtGui.QApplication.UnicodeUTF8))
        self.htrRangeComboBox.addItem(_fromUtf8(""))
        self.htrRangeComboBox.setItemText(4, QtGui.QApplication.translate("FridgeMonitorWindow", "1.00 mA", None, QtGui.QApplication.UnicodeUTF8))
        self.htrRangeComboBox.addItem(_fromUtf8(""))
        self.htrRangeComboBox.setItemText(5, QtGui.QApplication.translate("FridgeMonitorWindow", "3.16 mA", None, QtGui.QApplication.UnicodeUTF8))
        self.htrRangeComboBox.addItem(_fromUtf8(""))
        self.htrRangeComboBox.setItemText(6, QtGui.QApplication.translate("FridgeMonitorWindow", "10.0 mA", None, QtGui.QApplication.UnicodeUTF8))
        self.htrRangeComboBox.addItem(_fromUtf8(""))
        self.htrRangeComboBox.setItemText(7, QtGui.QApplication.translate("FridgeMonitorWindow", "31.6 mA", None, QtGui.QApplication.UnicodeUTF8))
        self.htrRangeComboBox.addItem(_fromUtf8(""))
        self.htrRangeComboBox.setItemText(8, QtGui.QApplication.translate("FridgeMonitorWindow", "100 mA", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontalLayout_2.addWidget(self.htrRangeComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtGui.QSpacerItem(20, 496, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_4.addWidget(self.frame)
        FridgeMonitorWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(FridgeMonitorWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1249, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        FridgeMonitorWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(FridgeMonitorWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        FridgeMonitorWindow.setStatusBar(self.statusbar)

        self.retranslateUi(FridgeMonitorWindow)
        QtCore.QMetaObject.connectSlotsByName(FridgeMonitorWindow)

    def retranslateUi(self, FridgeMonitorWindow):
        pass

from matplotlibwidget import MatplotlibWidget
