# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design/lookup.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LookupDialog(object):
    def setupUi(self, LookupDialog):
        LookupDialog.setObjectName("LookupDialog")
        LookupDialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(LookupDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.onlyCheck = QtWidgets.QCheckBox(LookupDialog)
        self.onlyCheck.setObjectName("onlyCheck")
        self.verticalLayout.addWidget(self.onlyCheck)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(LookupDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.sourceCombo = QtWidgets.QComboBox(LookupDialog)
        self.sourceCombo.setObjectName("sourceCombo")
        self.horizontalLayout.addWidget(self.sourceCombo)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(LookupDialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.label_2 = QtWidgets.QLabel(LookupDialog)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(LookupDialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.pgMsg = QtWidgets.QLabel(LookupDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pgMsg.sizePolicy().hasHeightForWidth())
        self.pgMsg.setSizePolicy(sizePolicy)
        self.pgMsg.setText("")
        self.pgMsg.setObjectName("pgMsg")
        self.horizontalLayout_3.addWidget(self.pgMsg)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.progressBar = QtWidgets.QProgressBar(LookupDialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.cancelBtn = QtWidgets.QPushButton(LookupDialog)
        self.cancelBtn.setObjectName("cancelBtn")
        self.horizontalLayout_4.addWidget(self.cancelBtn)
        self.startBtn = QtWidgets.QPushButton(LookupDialog)
        self.startBtn.setDefault(True)
        self.startBtn.setObjectName("startBtn")
        self.horizontalLayout_4.addWidget(self.startBtn)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(LookupDialog)
        QtCore.QMetaObject.connectSlotsByName(LookupDialog)

    def retranslateUi(self, LookupDialog):
        _translate = QtCore.QCoreApplication.translate
        LookupDialog.setWindowTitle(_translate("LookupDialog", "Lookup Setting"))
        self.onlyCheck.setText(_translate("LookupDialog", "Look-up only selected entries"))
        self.label.setText(_translate("LookupDialog", "Online Dictionary"))
        self.label_2.setText(_translate("LookupDialog", "<html><head/><body><p><span style=\" font-style:italic;\">Joytan looks up dictionaries for word meaning and example. You have to fill the word to get information in \'</span><span style=\" font-weight:600; font-style:italic;\">atop</span><span style=\" font-style:italic;\">\' section, which locates on the top of Entry Editors. And Joytan overwrites \'</span><span style=\" font-weight:600; font-style:italic;\">def-x\'</span><span style=\" font-style:italic;\"> and \'</span><span style=\" font-weight:600; font-style:italic;\">ex-x-x</span><span style=\" font-style:italic;\">\' text with the downloaded dictionary contents in respect.</span></p></body></html>"))
        self.label_3.setText(_translate("LookupDialog", "Progress:"))
        self.cancelBtn.setText(_translate("LookupDialog", "Stop"))
        self.startBtn.setText(_translate("LookupDialog", "Start"))

