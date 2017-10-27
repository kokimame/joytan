# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design/textdialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TextDialog(object):
    def setupUi(self, TextDialog):
        TextDialog.setObjectName("TextDialog")
        TextDialog.resize(400, 300)
        self.createBtn = QtWidgets.QPushButton(TextDialog)
        self.createBtn.setGeometry(QtCore.QRect(160, 110, 99, 27))
        self.createBtn.setObjectName("createBtn")

        self.retranslateUi(TextDialog)
        QtCore.QMetaObject.connectSlotsByName(TextDialog)

    def retranslateUi(self, TextDialog):
        _translate = QtCore.QCoreApplication.translate
        TextDialog.setWindowTitle(_translate("TextDialog", "Text Setting"))
        self.createBtn.setText(_translate("TextDialog", "OK"))

