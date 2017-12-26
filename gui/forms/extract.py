# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design/extract.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ExtractDialog(object):
    def setupUi(self, ExtractDialog):
        ExtractDialog.setObjectName("ExtractDialog")
        ExtractDialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(ExtractDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(ExtractDialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.nameLbl = QtWidgets.QLineEdit(ExtractDialog)
        self.nameLbl.setReadOnly(True)
        self.nameLbl.setObjectName("nameLbl")
        self.horizontalLayout_3.addWidget(self.nameLbl)
        self.fileBtn = QtWidgets.QToolButton(ExtractDialog)
        self.fileBtn.setObjectName("fileBtn")
        self.horizontalLayout_3.addWidget(self.fileBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.line = QtWidgets.QFrame(ExtractDialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.overCheck = QtWidgets.QCheckBox(ExtractDialog)
        self.overCheck.setChecked(True)
        self.overCheck.setObjectName("overCheck")
        self.verticalLayout.addWidget(self.overCheck)
        self.label = QtWidgets.QLabel(ExtractDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.keyList = QtWidgets.QListWidget(ExtractDialog)
        self.keyList.setObjectName("keyList")
        self.horizontalLayout_2.addWidget(self.keyList)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.cancelBtn = QtWidgets.QPushButton(ExtractDialog)
        self.cancelBtn.setObjectName("cancelBtn")
        self.horizontalLayout.addWidget(self.cancelBtn)
        self.okBtn = QtWidgets.QPushButton(ExtractDialog)
        self.okBtn.setAutoDefault(False)
        self.okBtn.setDefault(True)
        self.okBtn.setObjectName("okBtn")
        self.horizontalLayout.addWidget(self.okBtn)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ExtractDialog)
        QtCore.QMetaObject.connectSlotsByName(ExtractDialog)

    def retranslateUi(self, ExtractDialog):
        _translate = QtCore.QCoreApplication.translate
        ExtractDialog.setWindowTitle(_translate("ExtractDialog", "Extract setting"))
        self.label_2.setText(_translate("ExtractDialog", "Select Wordlist file:"))
        self.fileBtn.setText(_translate("ExtractDialog", "..."))
        self.overCheck.setText(_translate("ExtractDialog", "Overwrite exisiting Entry"))
        self.label.setText(_translate("ExtractDialog", "Extract to:"))
        self.cancelBtn.setText(_translate("ExtractDialog", "Cancel"))
        self.okBtn.setText(_translate("ExtractDialog", "OK"))

