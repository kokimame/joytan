# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design/opendialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_OpenDialog(object):
    def setupUi(self, OpenDialog):
        OpenDialog.setObjectName("OpenDialog")
        OpenDialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(OpenDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_2 = QtWidgets.QLabel(OpenDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        self.fileLbl = QtWidgets.QLineEdit(OpenDialog)
        self.fileLbl.setFocusPolicy(QtCore.Qt.NoFocus)
        self.fileLbl.setReadOnly(True)
        self.fileLbl.setObjectName("fileLbl")
        self.horizontalLayout_5.addWidget(self.fileLbl)
        self.fileBtn = QtWidgets.QToolButton(OpenDialog)
        self.fileBtn.setObjectName("fileBtn")
        self.horizontalLayout_5.addWidget(self.fileBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(OpenDialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.pgMsg = QtWidgets.QLabel(OpenDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pgMsg.sizePolicy().hasHeightForWidth())
        self.pgMsg.setSizePolicy(sizePolicy)
        self.pgMsg.setText("")
        self.pgMsg.setObjectName("pgMsg")
        self.horizontalLayout_3.addWidget(self.pgMsg)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.progressBar = QtWidgets.QProgressBar(OpenDialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.stopBtn = QtWidgets.QPushButton(OpenDialog)
        self.stopBtn.setObjectName("stopBtn")
        self.horizontalLayout_4.addWidget(self.stopBtn)
        self.openBtn = QtWidgets.QPushButton(OpenDialog)
        self.openBtn.setDefault(True)
        self.openBtn.setObjectName("openBtn")
        self.horizontalLayout_4.addWidget(self.openBtn)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(OpenDialog)
        QtCore.QMetaObject.connectSlotsByName(OpenDialog)

    def retranslateUi(self, OpenDialog):
        _translate = QtCore.QCoreApplication.translate
        OpenDialog.setWindowTitle(_translate("OpenDialog", "Open file "))
        self.label_2.setText(_translate("OpenDialog", "Selected file:"))
        self.fileBtn.setText(_translate("OpenDialog", "..."))
        self.label_3.setText(_translate("OpenDialog", "Progress:"))
        self.stopBtn.setText(_translate("OpenDialog", "Stop"))
        self.openBtn.setText(_translate("OpenDialog", "Open"))

