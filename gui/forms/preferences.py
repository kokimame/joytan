# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design/preferences.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Preferences(object):
    def setupUi(self, Preferences):
        Preferences.setObjectName("Preferences")
        Preferences.resize(872, 537)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Preferences)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(Preferences)
        self.tabWidget.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.tabWidget.setToolTip("")
        self.tabWidget.setObjectName("tabWidget")
        self.tabGeneral = QtWidgets.QWidget()
        self.tabGeneral.setObjectName("tabGeneral")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tabGeneral)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_4 = QtWidgets.QLabel(self.tabGeneral)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.titleEdit = QtWidgets.QLineEdit(self.tabGeneral)
        self.titleEdit.setObjectName("titleEdit")
        self.horizontalLayout_6.addWidget(self.titleEdit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.tabGeneral)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.dpwSpin = QtWidgets.QSpinBox(self.tabGeneral)
        self.dpwSpin.setMinimum(1)
        self.dpwSpin.setMaximum(99)
        self.dpwSpin.setProperty("value", 1)
        self.dpwSpin.setObjectName("dpwSpin")
        self.horizontalLayout_3.addWidget(self.dpwSpin)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.tabGeneral)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.epdSpin = QtWidgets.QSpinBox(self.tabGeneral)
        self.epdSpin.setMinimum(0)
        self.epdSpin.setMaximum(99)
        self.epdSpin.setProperty("value", 0)
        self.epdSpin.setObjectName("epdSpin")
        self.horizontalLayout_4.addWidget(self.epdSpin)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.line = QtWidgets.QFrame(self.tabGeneral)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.sfxEdit = QtWidgets.QLineEdit(self.tabGeneral)
        self.sfxEdit.setObjectName("sfxEdit")
        self.gridLayout.addWidget(self.sfxEdit, 2, 1, 1, 1)
        self.bgmEdit = QtWidgets.QLineEdit(self.tabGeneral)
        self.bgmEdit.setObjectName("bgmEdit")
        self.gridLayout.addWidget(self.bgmEdit, 3, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.tabGeneral)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)
        self.workingEdit = QtWidgets.QLineEdit(self.tabGeneral)
        self.workingEdit.setObjectName("workingEdit")
        self.gridLayout.addWidget(self.workingEdit, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.tabGeneral)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.wordEdit = QtWidgets.QLineEdit(self.tabGeneral)
        self.wordEdit.setObjectName("wordEdit")
        self.gridLayout.addWidget(self.wordEdit, 4, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.tabGeneral)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.tabGeneral)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 4, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.tabWidget.addTab(self.tabGeneral, "")
        self.tabAtts = QtWidgets.QWidget()
        self.tabAtts.setObjectName("tabAtts")
        self.tabWidget.addTab(self.tabAtts, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem4)
        self.cancelBtn = QtWidgets.QPushButton(Preferences)
        self.cancelBtn.setStyleSheet("")
        self.cancelBtn.setObjectName("cancelBtn")
        self.horizontalLayout_11.addWidget(self.cancelBtn)
        self.applyBtn = QtWidgets.QPushButton(Preferences)
        self.applyBtn.setObjectName("applyBtn")
        self.horizontalLayout_11.addWidget(self.applyBtn)
        self.okBtn = QtWidgets.QPushButton(Preferences)
        self.okBtn.setAutoDefault(False)
        self.okBtn.setDefault(True)
        self.okBtn.setObjectName("okBtn")
        self.horizontalLayout_11.addWidget(self.okBtn)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_11)

        self.retranslateUi(Preferences)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Preferences)

    def retranslateUi(self, Preferences):
        _translate = QtCore.QCoreApplication.translate
        Preferences.setWindowTitle(_translate("Preferences", "Preferences"))
        self.label_4.setText(_translate("Preferences", "Title"))
        self.label.setText(_translate("Preferences", "Definition per Entry"))
        self.label_2.setText(_translate("Preferences", "Example per Definition"))
        self.label_6.setText(_translate("Preferences", "BGM Directory"))
        self.label_5.setText(_translate("Preferences", "SFX Directory"))
        self.label_3.setText(_translate("Preferences", "Working Directory"))
        self.label_7.setText(_translate("Preferences", "Wordlist Directory"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabGeneral), _translate("Preferences", "General"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAtts), _translate("Preferences", "Text-to-Speech"))
        self.cancelBtn.setText(_translate("Preferences", "Cancel"))
        self.applyBtn.setText(_translate("Preferences", "Apply"))
        self.okBtn.setText(_translate("Preferences", "OK"))

