# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design/preferences.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_preferences(object):
    def setupUi(self, preferences):
        preferences.setObjectName("preferences")
        preferences.resize(461, 453)
        self.tabWidget = QtWidgets.QTabWidget(preferences)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 441, 391))
        self.tabWidget.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.tabWidget.setToolTip("")
        self.tabWidget.setObjectName("tabWidget")
        self.tabGeneral = QtWidgets.QWidget()
        self.tabGeneral.setObjectName("tabGeneral")
        self.tabWidget.addTab(self.tabGeneral, "")
        self.tabMP3 = QtWidgets.QWidget()
        self.tabMP3.setObjectName("tabMP3")
        self.tabWidget.addTab(self.tabMP3, "")
        self.tabPDF = QtWidgets.QWidget()
        self.tabPDF.setObjectName("tabPDF")
        self.tabWidget.addTab(self.tabPDF, "")
        self.buttonBox = QtWidgets.QDialogButtonBox(preferences)
        self.buttonBox.setGeometry(QtCore.QRect(9, 410, 441, 32))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.Help)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(preferences)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(preferences)

    def retranslateUi(self, preferences):
        _translate = QtCore.QCoreApplication.translate
        preferences.setWindowTitle(_translate("preferences", "Preferences"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabGeneral), _translate("preferences", "General"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMP3), _translate("preferences", "MP3"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabPDF), _translate("preferences", "PDF"))

