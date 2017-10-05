# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design/main.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(522, 636)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.dlcButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.dlcButton.setGeometry(QtCore.QRect(10, 520, 211, 41))
        self.dlcButton.setObjectName("dlcButton")
        self.mp3Button = QtWidgets.QPushButton(self.centralwidget)
        self.mp3Button.setGeometry(QtCore.QRect(380, 530, 99, 27))
        self.mp3Button.setObjectName("mp3Button")
        self.pdfButton = QtWidgets.QPushButton(self.centralwidget)
        self.pdfButton.setGeometry(QtCore.QRect(380, 560, 99, 27))
        self.pdfButton.setObjectName("pdfButton")
        self.frameList = QtWidgets.QListWidget(self.centralwidget)
        self.frameList.setGeometry(QtCore.QRect(10, 10, 501, 511))
        self.frameList.setObjectName("frameList")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 522, 25))
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.actionUndo = QtWidgets.QAction(MainWindow)
        self.actionUndo.setObjectName("actionUndo")
        self.actionImport = QtWidgets.QAction(MainWindow)
        self.actionImport.setObjectName("actionImport")
        self.action_Exit = QtWidgets.QAction(MainWindow)
        self.action_Exit.setObjectName("action_Exit")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionExtract = QtWidgets.QAction(MainWindow)
        self.actionExtract.setObjectName("actionExtract")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.menuFile.addAction(self.actionExtract)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionPreferences)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Bavl"))
        self.dlcButton.setText(_translate("MainWindow", "Get DLC via Online Dictionary"))
        self.mp3Button.setText(_translate("MainWindow", "Get MP3"))
        self.pdfButton.setText(_translate("MainWindow", "Get PDF"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuEdit.setTitle(_translate("MainWindow", "&Edit"))
        self.menuTools.setTitle(_translate("MainWindow", "&Tools"))
        self.menuHelp.setTitle(_translate("MainWindow", "&Help"))
        self.actionUndo.setText(_translate("MainWindow", "&Undo"))
        self.actionImport.setText(_translate("MainWindow", "&Import..."))
        self.action_Exit.setText(_translate("MainWindow", "&Exit"))
        self.actionExit.setText(_translate("MainWindow", "&Exit"))
        self.actionExtract.setText(_translate("MainWindow", "Extract..."))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences"))

