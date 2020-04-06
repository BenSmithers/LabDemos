# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lab_gui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.frew_lbl = QtWidgets.QLabel(self.centralwidget)
        self.frew_lbl.setObjectName("frew_lbl")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.frew_lbl)
        self.freq_spin = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.freq_spin.setMinimum(20.0)
        self.freq_spin.setMaximum(20000.0)
        self.freq_spin.setSingleStep(10.0)
        self.freq_spin.setObjectName("freq_spin")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.freq_spin)
        self.fixed_check = QtWidgets.QCheckBox(self.centralwidget)
        self.fixed_check.setText("")
        self.fixed_check.setObjectName("fixed_check")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.fixed_check)
        self.fixed_end_lbl = QtWidgets.QLabel(self.centralwidget)
        self.fixed_end_lbl.setObjectName("fixed_end_lbl")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.fixed_end_lbl)
        self.enabled_q = QtWidgets.QLabel(self.centralwidget)
        self.enabled_q.setObjectName("enabled_q")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.enabled_q)
        self.enabled_chk = QtWidgets.QCheckBox(self.centralwidget)
        self.enabled_chk.setText("")
        self.enabled_chk.setObjectName("enabled_chk")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.enabled_chk)
        self.horizontalLayout.addLayout(self.formLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.frew_lbl.setText(_translate("MainWindow", "Driving f"))
        self.fixed_end_lbl.setText(_translate("MainWindow", "Fixed End"))
        self.enabled_q.setText(_translate("MainWindow", "Enabled?"))

