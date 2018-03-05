# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design/sortdialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SortDialog(object):
    def setupUi(self, SortDialog):
        SortDialog.setObjectName("SortDialog")
        SortDialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(SortDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.onlyCheck = QtWidgets.QCheckBox(SortDialog)
        self.onlyCheck.setObjectName("onlyCheck")
        self.verticalLayout.addWidget(self.onlyCheck)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(SortDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.optionBox = QtWidgets.QComboBox(SortDialog)
        self.optionBox.setObjectName("optionBox")
        self.optionBox.addItem("")
        self.optionBox.addItem("")
        self.horizontalLayout.addWidget(self.optionBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(SortDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.ewkeyBox = QtWidgets.QComboBox(SortDialog)
        self.ewkeyBox.setObjectName("ewkeyBox")
        self.horizontalLayout_2.addWidget(self.ewkeyBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(SortDialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.pgMsg = QtWidgets.QLabel(SortDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pgMsg.sizePolicy().hasHeightForWidth())
        self.pgMsg.setSizePolicy(sizePolicy)
        self.pgMsg.setText("")
        self.pgMsg.setObjectName("pgMsg")
        self.horizontalLayout_4.addWidget(self.pgMsg)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.progressBar = QtWidgets.QProgressBar(SortDialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.okBtn = QtWidgets.QPushButton(SortDialog)
        self.okBtn.setDefault(True)
        self.okBtn.setObjectName("okBtn")
        self.horizontalLayout_3.addWidget(self.okBtn)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(SortDialog)
        QtCore.QMetaObject.connectSlotsByName(SortDialog)

    def retranslateUi(self, SortDialog):
        _translate = QtCore.QCoreApplication.translate
        SortDialog.setWindowTitle(_translate("SortDialog", "Sort entries"))
        self.onlyCheck.setText(_translate("SortDialog", "Sort only selected entries"))
        self.label.setText(_translate("SortDialog", "Sort Option"))
        self.optionBox.setItemText(0, _translate("SortDialog", "Reverse"))
        self.optionBox.setItemText(1, _translate("SortDialog", "Shuffle"))
        self.label_2.setText(_translate("SortDialog", "Sort by"))
        self.label_3.setText(_translate("SortDialog", "Progress:"))
        self.okBtn.setText(_translate("SortDialog", "Sort"))

