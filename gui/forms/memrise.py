# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design/memrise.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MemriseDialog(object):
    def setupUi(self, MemriseDialog):
        MemriseDialog.setObjectName("MemriseDialog")
        MemriseDialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(MemriseDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(MemriseDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.urlEdit = QtWidgets.QLineEdit(MemriseDialog)
        self.urlEdit.setObjectName("urlEdit")
        self.horizontalLayout.addWidget(self.urlEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_2 = QtWidgets.QLabel(MemriseDialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.line = QtWidgets.QFrame(MemriseDialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(MemriseDialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.pgMsg = QtWidgets.QLabel(MemriseDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pgMsg.sizePolicy().hasHeightForWidth())
        self.pgMsg.setSizePolicy(sizePolicy)
        self.pgMsg.setText("")
        self.pgMsg.setObjectName("pgMsg")
        self.horizontalLayout_3.addWidget(self.pgMsg)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.progressBar = QtWidgets.QProgressBar(MemriseDialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.stopBtn = QtWidgets.QPushButton(MemriseDialog)
        self.stopBtn.setObjectName("stopBtn")
        self.horizontalLayout_4.addWidget(self.stopBtn)
        self.dlBtn = QtWidgets.QPushButton(MemriseDialog)
        self.dlBtn.setDefault(True)
        self.dlBtn.setObjectName("dlBtn")
        self.horizontalLayout_4.addWidget(self.dlBtn)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(MemriseDialog)
        QtCore.QMetaObject.connectSlotsByName(MemriseDialog)

    def retranslateUi(self, MemriseDialog):
        _translate = QtCore.QCoreApplication.translate
        MemriseDialog.setWindowTitle(_translate("MemriseDialog", "Download Memrise"))
        self.label.setText(_translate("MemriseDialog", "URL"))
        self.label_2.setText(_translate("MemriseDialog", "<html><head/><body><p>Paste an URL of Memrise level, <b>not a course</b>, to <br>download entries.</p></body></html>"))
        self.label_3.setText(_translate("MemriseDialog", "Progress:"))
        self.stopBtn.setText(_translate("MemriseDialog", "Stop"))
        self.dlBtn.setText(_translate("MemriseDialog", "Download"))

