# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nexusget.ui'
#
# Created: Thu Mar 20 14:10:53 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(345, 437)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.username = QtGui.QLineEdit(self.centralwidget)
        self.username.setObjectName("username")
        self.gridLayout.addWidget(self.username, 4, 0, 1, 1)
        self.filenumbers = QtGui.QLineEdit(self.centralwidget)
        self.filenumbers.setObjectName("filenumbers")
        self.gridLayout.addWidget(self.filenumbers, 2, 0, 1, 1)
        self.getfiles = QtGui.QPushButton(self.centralwidget)
        self.getfiles.setObjectName("getfiles")
        self.gridLayout.addWidget(self.getfiles, 8, 0, 1, 1)
        self.password = QtGui.QLineEdit(self.centralwidget)
        self.password.setObjectName("password")
        self.gridLayout.addWidget(self.password, 5, 0, 1, 1)
        self.setdirectory = QtGui.QPushButton(self.centralwidget)
        self.setdirectory.setObjectName("setdirectory")
        self.gridLayout.addWidget(self.setdirectory, 7, 0, 1, 1)
        self.animal = QtGui.QComboBox(self.centralwidget)
        self.animal.setObjectName("animal")
        self.gridLayout.addWidget(self.animal, 1, 0, 1, 1)
        self.checkBox = QtGui.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 3, 0, 1, 1)
        self.directory = QtGui.QLineEdit(self.centralwidget)
        self.directory.setEnabled(False)
        self.directory.setObjectName("directory")
        self.gridLayout.addWidget(self.directory, 6, 0, 1, 1)
        self.history = QtGui.QPlainTextEdit(self.centralwidget)
        self.history.setObjectName("history")
        self.gridLayout.addWidget(self.history, 9, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 345, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.animal, self.filenumbers)
        MainWindow.setTabOrder(self.filenumbers, self.checkBox)
        MainWindow.setTabOrder(self.checkBox, self.username)
        MainWindow.setTabOrder(self.username, self.password)
        MainWindow.setTabOrder(self.password, self.directory)
        MainWindow.setTabOrder(self.directory, self.setdirectory)
        MainWindow.setTabOrder(self.setdirectory, self.getfiles)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "NeXus Get", None, QtGui.QApplication.UnicodeUTF8))
        self.username.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "Username", None, QtGui.QApplication.UnicodeUTF8))
        self.filenumbers.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "List of NX numbers, e.g. 123, 124, 130-140", None, QtGui.QApplication.UnicodeUTF8))
        self.getfiles.setText(QtGui.QApplication.translate("MainWindow", "Get files", None, QtGui.QApplication.UnicodeUTF8))
        self.password.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.setdirectory.setText(QtGui.QApplication.translate("MainWindow", "Set directory", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("MainWindow", "Get Event Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.directory.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "directory", None, QtGui.QApplication.UnicodeUTF8))

