# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\GitHub\pythonsample\pyqt5case\tableViewWnd.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_tableViewDlg(object):
    def setupUi(self, tableViewDlg):
        tableViewDlg.setObjectName("tableViewDlg")
        tableViewDlg.resize(781, 624)
        self.buttonBox = QtWidgets.QDialogButtonBox(tableViewDlg)
        self.buttonBox.setGeometry(QtCore.QRect(420, 570, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.tableViewWnd = QtWidgets.QTableWidget(tableViewDlg)
        self.tableViewWnd.setGeometry(QtCore.QRect(10, 10, 761, 381))
        self.tableViewWnd.setObjectName("tableViewWnd")
        self.tableViewWnd.setColumnCount(4)
        self.tableViewWnd.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableViewWnd.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableViewWnd.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableViewWnd.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableViewWnd.setHorizontalHeaderItem(3, item)

        self.retranslateUi(tableViewDlg)
        self.buttonBox.accepted.connect(tableViewDlg.accept)
        self.buttonBox.rejected.connect(tableViewDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(tableViewDlg)

    def retranslateUi(self, tableViewDlg):
        _translate = QtCore.QCoreApplication.translate
        tableViewDlg.setWindowTitle(_translate("tableViewDlg", "Dialog"))
        item = self.tableViewWnd.horizontalHeaderItem(0)
        item.setText(_translate("tableViewDlg", "Partition"))
        item = self.tableViewWnd.horizontalHeaderItem(1)
        item.setText(_translate("tableViewDlg", "New Column"))
        item = self.tableViewWnd.horizontalHeaderItem(2)
        item.setText(_translate("tableViewDlg", "Size"))
        item = self.tableViewWnd.horizontalHeaderItem(3)
        item.setText(_translate("tableViewDlg", "FilePath"))
