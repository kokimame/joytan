# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design/translate.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TranslateDialog(object):
    def setupUi(self, TranslateDialog):
        TranslateDialog.setObjectName("TranslateDialog")
        TranslateDialog.resize(400, 300)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(TranslateDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.onlyCheck = QtWidgets.QCheckBox(TranslateDialog)
        self.onlyCheck.setObjectName("onlyCheck")
        self.verticalLayout_2.addWidget(self.onlyCheck)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_2 = QtWidgets.QLabel(TranslateDialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_5.addWidget(self.label_2)
        self.keyList = QtWidgets.QListWidget(TranslateDialog)
        self.keyList.setObjectName("keyList")
        self.verticalLayout_5.addWidget(self.keyList)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(TranslateDialog)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.langCombo = QtWidgets.QComboBox(TranslateDialog)
        self.langCombo.setObjectName("langCombo")
        self.horizontalLayout_2.addWidget(self.langCombo)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(TranslateDialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.pgMsg = QtWidgets.QLabel(TranslateDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pgMsg.sizePolicy().hasHeightForWidth())
        self.pgMsg.setSizePolicy(sizePolicy)
        self.pgMsg.setText("")
        self.pgMsg.setObjectName("pgMsg")
        self.horizontalLayout_3.addWidget(self.pgMsg)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.progressBar = QtWidgets.QProgressBar(TranslateDialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.cancelBtn = QtWidgets.QPushButton(TranslateDialog)
        self.cancelBtn.setObjectName("cancelBtn")
        self.horizontalLayout_4.addWidget(self.cancelBtn)
        self.startBtn = QtWidgets.QPushButton(TranslateDialog)
        self.startBtn.setDefault(True)
        self.startBtn.setObjectName("startBtn")
        self.horizontalLayout_4.addWidget(self.startBtn)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.retranslateUi(TranslateDialog)
        QtCore.QMetaObject.connectSlotsByName(TranslateDialog)

    def retranslateUi(self, TranslateDialog):
        _translate = QtCore.QCoreApplication.translate
        TranslateDialog.setWindowTitle(_translate("TranslateDialog", "Translation Setting"))
        self.onlyCheck.setText(_translate("TranslateDialog", "Translate only selected entries"))
        self.label_2.setText(_translate("TranslateDialog", "Translate text of"))
        self.label_4.setText(_translate("TranslateDialog", "Translate to"))
        self.label_3.setText(_translate("TranslateDialog", "Progress:"))
        self.cancelBtn.setText(_translate("TranslateDialog", "Stop"))
        self.startBtn.setText(_translate("TranslateDialog", "Translate"))

