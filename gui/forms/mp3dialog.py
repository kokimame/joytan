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
        Mp3Dialog.resize(472, 408)
        self.ttsCombo = QtWidgets.QComboBox(Mp3Dialog)
        self.ttsCombo.setGeometry(QtCore.QRect(40, 10, 85, 27))
        self.ttsCombo.setObjectName("ttsCombo")
        self.ttsCombo.addItem("")
        self.ttsCombo.addItem("")
        self.label = QtWidgets.QLabel(Mp3Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 31, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Mp3Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 101, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Mp3Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 190, 91, 17))
        self.label_3.setObjectName("label_3")
        self.bgmAddBtn = QtWidgets.QPushButton(Mp3Dialog)
        self.bgmAddBtn.setGeometry(QtCore.QRect(340, 330, 81, 27))
        self.bgmAddBtn.setObjectName("bgmAddBtn")
        self.label_4 = QtWidgets.QLabel(Mp3Dialog)
        self.label_4.setGeometry(QtCore.QRect(160, 170, 171, 20))
        self.label_4.setObjectName("label_4")
        self.sfxTable = QtWidgets.QTableWidget(Mp3Dialog)
        self.sfxTable.setGeometry(QtCore.QRect(10, 70, 451, 91))
        self.sfxTable.setObjectName("sfxTable")
        self.sfxTable.setColumnCount(0)
        self.sfxTable.setRowCount(0)
        self.wordSpin = QtWidgets.QSpinBox(Mp3Dialog)
        self.wordSpin.setGeometry(QtCore.QRect(300, 10, 41, 27))
        self.wordSpin.setMinimum(1)
        self.wordSpin.setProperty("value", 3)
        self.wordSpin.setObjectName("wordSpin")
        self.label_5 = QtWidgets.QLabel(Mp3Dialog)
        self.label_5.setGeometry(QtCore.QRect(210, 10, 91, 31))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Mp3Dialog)
        self.label_6.setGeometry(QtCore.QRect(350, 10, 41, 31))
        self.label_6.setObjectName("label_6")
        self.cancelBtn = QtWidgets.QPushButton(Mp3Dialog)
        self.cancelBtn.setGeometry(QtCore.QRect(140, 370, 99, 27))
        self.cancelBtn.setObjectName("cancelBtn")
        self.createBtn = QtWidgets.QPushButton(Mp3Dialog)
        self.createBtn.setGeometry(QtCore.QRect(260, 370, 99, 27))
        self.createBtn.setCheckable(False)
        self.createBtn.setAutoDefault(False)
        self.createBtn.setDefault(True)
        self.createBtn.setObjectName("createBtn")
        self.bgmList = QtWidgets.QListWidget(Mp3Dialog)
        self.bgmList.setGeometry(QtCore.QRect(10, 210, 451, 111))
        self.bgmList.setObjectName("bgmList")

        self.retranslateUi(Mp3Dialog)
        QtCore.QMetaObject.connectSlotsByName(Mp3Dialog)

    def retranslateUi(self, Mp3Dialog):
        _translate = QtCore.QCoreApplication.translate
        Mp3Dialog.setWindowTitle(_translate("Mp3Dialog", "Audio Setting"))
        self.ttsCombo.setItemText(0, _translate("Mp3Dialog", "say"))
        self.ttsCombo.setItemText(1, _translate("Mp3Dialog", "espeak"))
        self.label.setText(_translate("Mp3Dialog", "TTS"))
        self.label_2.setText(_translate("Mp3Dialog", "Sound effects"))
        self.label_3.setText(_translate("Mp3Dialog", "BGM Loop"))
        self.bgmAddBtn.setText(_translate("Mp3Dialog", "Add Song"))
        self.label_4.setText(_translate("Mp3Dialog", ">>> Preview Coming <<<"))
        self.label_5.setText(_translate("Mp3Dialog", "Repeat word"))
        self.label_6.setText(_translate("Mp3Dialog", "times"))
        self.cancelBtn.setText(_translate("Mp3Dialog", "Cancel"))
        self.createBtn.setText(_translate("Mp3Dialog", "Create MP3"))

