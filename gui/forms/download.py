# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design/download.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DownloadDialog(object):
    def setupUi(self, DownloadDialog):
        DownloadDialog.setObjectName("DownloadDialog")
        DownloadDialog.resize(400, 300)
        self.cancelBtn = QtWidgets.QPushButton(DownloadDialog)
        self.cancelBtn.setGeometry(QtCore.QRect(100, 180, 99, 27))
        self.cancelBtn.setObjectName("cancelBtn")
        self.startBtn = QtWidgets.QPushButton(DownloadDialog)
        self.startBtn.setGeometry(QtCore.QRect(220, 180, 99, 27))
        self.startBtn.setObjectName("startBtn")
        self.horizontalLayoutWidget = QtWidgets.QWidget(DownloadDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(70, 40, 271, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.sourceCombo = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.sourceCombo.setObjectName("sourceCombo")
        self.horizontalLayout.addWidget(self.sourceCombo)

        self.retranslateUi(DownloadDialog)
        QtCore.QMetaObject.connectSlotsByName(DownloadDialog)

    def retranslateUi(self, DownloadDialog):
        _translate = QtCore.QCoreApplication.translate
        DownloadDialog.setWindowTitle(_translate("DownloadDialog", "Download Setting"))
        self.cancelBtn.setText(_translate("DownloadDialog", "Cancel"))
        self.startBtn.setText(_translate("DownloadDialog", "Start"))
        self.label.setText(_translate("DownloadDialog", "Online sources"))

