# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design/langdetect.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LangDetectDialog(object):
    def setupUi(self, LangDetectDialog):
        LangDetectDialog.setObjectName("LangDetectDialog")
        LangDetectDialog.resize(400, 378)
        self.langList = QtWidgets.QListWidget(LangDetectDialog)
        self.langList.setGeometry(QtCore.QRect(10, 70, 381, 231))
        self.langList.setObjectName("langList")
        self.cancelBtn = QtWidgets.QPushButton(LangDetectDialog)
        self.cancelBtn.setGeometry(QtCore.QRect(110, 320, 99, 27))
        self.cancelBtn.setObjectName("cancelBtn")
        self.okBtn = QtWidgets.QPushButton(LangDetectDialog)
        self.okBtn.setGeometry(QtCore.QRect(210, 320, 99, 27))
        self.okBtn.setObjectName("okBtn")
        self.label = QtWidgets.QLabel(LangDetectDialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 381, 61))
        self.label.setObjectName("label")

        self.retranslateUi(LangDetectDialog)
        QtCore.QMetaObject.connectSlotsByName(LangDetectDialog)

    def retranslateUi(self, LangDetectDialog):
        _translate = QtCore.QCoreApplication.translate
        LangDetectDialog.setWindowTitle(_translate("LangDetectDialog", "Language Confirmation"))
        self.cancelBtn.setText(_translate("LangDetectDialog", "Cancel"))
        self.okBtn.setText(_translate("LangDetectDialog", "OK"))
        self.label.setText(_translate("LangDetectDialog", "<html><head/><body><p align=\"center\">Check if the languages below are correct </p><p align=\"center\">for the corresponding contents</p></body></html>"))

