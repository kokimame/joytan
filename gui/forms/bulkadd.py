# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bulkadd.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BulkaddDialog(object):
    def setupUi(self, BulkaddDialog):
        BulkaddDialog.setObjectName("BulkaddDialog")
        BulkaddDialog.resize(400, 296)
        self.buttonBox = QtWidgets.QDialogButtonBox(BulkaddDialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.lineEdit = QtWidgets.QLineEdit(BulkaddDialog)
        self.lineEdit.setGeometry(QtCore.QRect(30, 210, 331, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(BulkaddDialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 381, 191))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        self.retranslateUi(BulkaddDialog)
        self.buttonBox.accepted.connect(BulkaddDialog.accept)
        self.buttonBox.rejected.connect(BulkaddDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(BulkaddDialog)

    def retranslateUi(self, BulkaddDialog):
        _translate = QtCore.QCoreApplication.translate
        BulkaddDialog.setWindowTitle(_translate("BulkaddDialog", "Bulk Add"))
        self.label.setText(_translate("BulkaddDialog", "Input a string to quickly build the audio entries: \n"
" a=atop \n"
" 1~9=def-1~def-9 \n"
" e1~e9=ex-1~ex-9\n"
" r=rest\n"
" i=index\n"
" e.g. \"11a2r\"=twice def-1, once atop, once def-2, rest"))
