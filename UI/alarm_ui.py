# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'alarm_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AlarmWindow(object):
    def setupUi(self, AlarmWindow):
        AlarmWindow.setObjectName("AlarmWindow")
        AlarmWindow.resize(511, 303)
        self.tableWidget = QtWidgets.QTableWidget(AlarmWindow)
        self.tableWidget.setGeometry(QtCore.QRect(0, 50, 501, 192))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)

        self.retranslateUi(AlarmWindow)
        QtCore.QMetaObject.connectSlotsByName(AlarmWindow)

    def retranslateUi(self, AlarmWindow):
        _translate = QtCore.QCoreApplication.translate
        AlarmWindow.setWindowTitle(_translate("AlarmWindow", "Dialog"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("AlarmWindow", "ID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("AlarmWindow", "Message"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("AlarmWindow", "Level"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("AlarmWindow", "Time"))
