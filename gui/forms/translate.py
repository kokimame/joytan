# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design/translate.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TranslateDialog(object):
    def setupUi(self, TranslateDialog):
        TranslateDialog.setObjectName("TranslateDialog")
        TranslateDialog.resize(400, 300)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(TranslateDialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 151, 105))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.nameCheck = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.nameCheck.setChecked(False)
        self.nameCheck.setObjectName("nameCheck")
        self.verticalLayout.addWidget(self.nameCheck)
        self.defCheck = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.defCheck.setObjectName("defCheck")
        self.verticalLayout.addWidget(self.defCheck)
        self.exCheck = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        self.exCheck.setObjectName("exCheck")
        self.verticalLayout.addWidget(self.exCheck)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayoutWidget = QtWidgets.QWidget(TranslateDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(170, 20, 211, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.langCombo = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.langCombo.setObjectName("langCombo")
        self.horizontalLayout.addWidget(self.langCombo)
        self.startButton = QtWidgets.QPushButton(TranslateDialog)
        self.startButton.setGeometry(QtCore.QRect(160, 270, 99, 27))
        self.startButton.setDefault(True)
        self.startButton.setObjectName("startButton")
        self.progressBar = QtWidgets.QProgressBar(TranslateDialog)
        self.progressBar.setGeometry(QtCore.QRect(80, 230, 261, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label_3 = QtWidgets.QLabel(TranslateDialog)
        self.label_3.setGeometry(QtCore.QRect(30, 200, 67, 17))
        self.label_3.setObjectName("label_3")
        self.pgMsg = QtWidgets.QLabel(TranslateDialog)
        self.pgMsg.setGeometry(QtCore.QRect(100, 200, 281, 17))
        self.pgMsg.setText("")
        self.pgMsg.setObjectName("pgMsg")

        self.retranslateUi(TranslateDialog)
        QtCore.QMetaObject.connectSlotsByName(TranslateDialog)

    def retranslateUi(self, TranslateDialog):
        _translate = QtCore.QCoreApplication.translate
        TranslateDialog.setWindowTitle(_translate("TranslateDialog", "Translation Setting"))
        self.label.setText(_translate("TranslateDialog", "Translate contents in"))
        self.nameCheck.setText(_translate("TranslateDialog", "Name"))
        self.defCheck.setText(_translate("TranslateDialog", "Definition"))
        self.exCheck.setText(_translate("TranslateDialog", "Example"))
        self.label_2.setText(_translate("TranslateDialog", "Translate to"))
        self.startButton.setText(_translate("TranslateDialog", "Translate"))
        self.label_3.setText(_translate("TranslateDialog", "Progress:"))

