# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design/copydialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CopyDialog(object):
    def setupUi(self, CopyDialog):
        CopyDialog.setObjectName("CopyDialog")
        CopyDialog.resize(400, 140)
        self.verticalLayout = QtWidgets.QVBoxLayout(CopyDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(CopyDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.fromBox = QtWidgets.QComboBox(CopyDialog)
        self.fromBox.setObjectName("fromBox")
        self.horizontalLayout.addWidget(self.fromBox)
        self.label_2 = QtWidgets.QLabel(CopyDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.toBox = QtWidgets.QComboBox(CopyDialog)
        self.toBox.setObjectName("toBox")
        self.horizontalLayout.addWidget(self.toBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.cancelBtn = QtWidgets.QPushButton(CopyDialog)
        self.cancelBtn.setObjectName("cancelBtn")
        self.horizontalLayout_2.addWidget(self.cancelBtn)
        self.copyBtn = QtWidgets.QPushButton(CopyDialog)
        self.copyBtn.setObjectName("copyBtn")
        self.horizontalLayout_2.addWidget(self.copyBtn)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(CopyDialog)
        QtCore.QMetaObject.connectSlotsByName(CopyDialog)

    def retranslateUi(self, CopyDialog):
        _translate = QtCore.QCoreApplication.translate
        CopyDialog.setWindowTitle(_translate("CopyDialog", "Smart Copy"))
        self.label.setText(_translate("CopyDialog", "Copy contents in"))
        self.label_2.setText(_translate("CopyDialog", "to"))
        self.cancelBtn.setText(_translate("CopyDialog", "Cancel"))
        self.copyBtn.setText(_translate("CopyDialog", "Copy"))

