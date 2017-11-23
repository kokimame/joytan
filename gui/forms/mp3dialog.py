# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design/mp3dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Mp3Dialog(object):
    def setupUi(self, Mp3Dialog):
        Mp3Dialog.setObjectName("Mp3Dialog")
        Mp3Dialog.resize(507, 653)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Mp3Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(Mp3Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.settingBtn = QtWidgets.QPushButton(Mp3Dialog)
        self.settingBtn.setObjectName("settingBtn")
        self.horizontalLayout_2.addWidget(self.settingBtn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_5 = QtWidgets.QLabel(Mp3Dialog)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.wordSpin = QtWidgets.QSpinBox(Mp3Dialog)
        self.wordSpin.setMinimum(1)
        self.wordSpin.setProperty("value", 3)
        self.wordSpin.setObjectName("wordSpin")
        self.horizontalLayout_4.addWidget(self.wordSpin)
        self.label_6 = QtWidgets.QLabel(Mp3Dialog)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.horizontalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.lrcCheck = QtWidgets.QCheckBox(Mp3Dialog)
        self.lrcCheck.setChecked(True)
        self.lrcCheck.setObjectName("lrcCheck")
        self.verticalLayout.addWidget(self.lrcCheck)
        self.gstaticCheck = QtWidgets.QCheckBox(Mp3Dialog)
        self.gstaticCheck.setChecked(False)
        self.gstaticCheck.setObjectName("gstaticCheck")
        self.verticalLayout.addWidget(self.gstaticCheck)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(Mp3Dialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.sfxList = QtWidgets.QListWidget(Mp3Dialog)
        self.sfxList.setObjectName("sfxList")
        self.verticalLayout_3.addWidget(self.sfxList)
        self.label_4 = QtWidgets.QLabel(Mp3Dialog)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.label_3 = QtWidgets.QLabel(Mp3Dialog)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.bgmList = QtWidgets.QListWidget(Mp3Dialog)
        self.bgmList.setObjectName("bgmList")
        self.verticalLayout_3.addWidget(self.bgmList)
        self.line = QtWidgets.QFrame(Mp3Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_7 = QtWidgets.QLabel(Mp3Dialog)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout.addWidget(self.label_7)
        self.pgMsg = QtWidgets.QLabel(Mp3Dialog)
        self.pgMsg.setText("")
        self.pgMsg.setObjectName("pgMsg")
        self.horizontalLayout.addWidget(self.pgMsg)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.progressBar = QtWidgets.QProgressBar(Mp3Dialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_3.addWidget(self.progressBar)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.cancelBtn = QtWidgets.QPushButton(Mp3Dialog)
        self.cancelBtn.setObjectName("cancelBtn")
        self.horizontalLayout_5.addWidget(self.cancelBtn)
        self.createBtn = QtWidgets.QPushButton(Mp3Dialog)
        self.createBtn.setCheckable(False)
        self.createBtn.setAutoDefault(False)
        self.createBtn.setDefault(True)
        self.createBtn.setObjectName("createBtn")
        self.horizontalLayout_5.addWidget(self.createBtn)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Mp3Dialog)
        QtCore.QMetaObject.connectSlotsByName(Mp3Dialog)

    def retranslateUi(self, Mp3Dialog):
        _translate = QtCore.QCoreApplication.translate
        Mp3Dialog.setWindowTitle(_translate("Mp3Dialog", "Audio Setting"))
        self.label.setText(_translate("Mp3Dialog", "TTS"))
        self.settingBtn.setText(_translate("Mp3Dialog", "Setting"))
        self.label_5.setText(_translate("Mp3Dialog", "Repeat word"))
        self.label_6.setText(_translate("Mp3Dialog", "times"))
        self.lrcCheck.setText(_translate("Mp3Dialog", "Create Lyrics file"))
        self.gstaticCheck.setText(_translate("Mp3Dialog", "Download nice pronunciation for English words if possible"))
        self.label_2.setText(_translate("Mp3Dialog", "Sound effects"))
        self.label_4.setText(_translate("Mp3Dialog", ">>> Preview Coming <<<"))
        self.label_3.setText(_translate("Mp3Dialog", "BGM Loop"))
        self.label_7.setText(_translate("Mp3Dialog", "Progress:"))
        self.cancelBtn.setText(_translate("Mp3Dialog", "Cancel"))
        self.createBtn.setText(_translate("Mp3Dialog", "Start"))

