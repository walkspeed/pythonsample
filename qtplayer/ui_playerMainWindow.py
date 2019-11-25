# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\GitHub\pythonsample\qtplayer\playerMainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(603, 470)
        self.playframe = QtWidgets.QFrame(Dialog)
        self.playframe.setGeometry(QtCore.QRect(10, 10, 581, 341))
        self.playframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.playframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.playframe.setObjectName("playframe")
        self.playSlider = QtWidgets.QSlider(Dialog)
        self.playSlider.setGeometry(QtCore.QRect(10, 360, 581, 22))
        self.playSlider.setOrientation(QtCore.Qt.Horizontal)
        self.playSlider.setObjectName("playSlider")
        self.pbOpen = QtWidgets.QPushButton(Dialog)
        self.pbOpen.setGeometry(QtCore.QRect(10, 410, 93, 28))
        self.pbOpen.setObjectName("pbOpen")
        self.pbPlay = QtWidgets.QPushButton(Dialog)
        self.pbPlay.setGeometry(QtCore.QRect(130, 410, 93, 28))
        self.pbPlay.setObjectName("pbPlay")
        self.pbPause = QtWidgets.QPushButton(Dialog)
        self.pbPause.setGeometry(QtCore.QRect(250, 410, 93, 28))
        self.pbPause.setObjectName("pbPause")
        self.pbStop = QtWidgets.QPushButton(Dialog)
        self.pbStop.setGeometry(QtCore.QRect(360, 410, 93, 28))
        self.pbStop.setObjectName("pbStop")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pbOpen.setText(_translate("Dialog", "load"))
        self.pbPlay.setText(_translate("Dialog", "play"))
        self.pbPause.setText(_translate("Dialog", "pause"))
        self.pbStop.setText(_translate("Dialog", "stop"))
