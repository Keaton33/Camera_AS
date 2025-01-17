# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SettingWindow(object):
    def setupUi(self, SettingWindow):
        SettingWindow.setObjectName("SettingWindow")
        SettingWindow.resize(404, 299)
        self.verticalLayout = QtWidgets.QVBoxLayout(SettingWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_12 = QtWidgets.QLabel(SettingWindow)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_4.addWidget(self.label_12)
        self.lineEdit_hb_dimension_vertical = QtWidgets.QLineEdit(SettingWindow)
        self.lineEdit_hb_dimension_vertical.setObjectName("lineEdit_hb_dimension_vertical")
        self.horizontalLayout_4.addWidget(self.lineEdit_hb_dimension_vertical)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 4, 0, 1, 1)
        self.pushButton_configure = QtWidgets.QPushButton(SettingWindow)
        self.pushButton_configure.setObjectName("pushButton_configure")
        self.gridLayout_2.addWidget(self.pushButton_configure, 5, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_Kp = QtWidgets.QLineEdit(SettingWindow)
        self.lineEdit_Kp.setObjectName("lineEdit_Kp")
        self.horizontalLayout.addWidget(self.lineEdit_Kp)
        self.lineEdit_Ki = QtWidgets.QLineEdit(SettingWindow)
        self.lineEdit_Ki.setObjectName("lineEdit_Ki")
        self.horizontalLayout.addWidget(self.lineEdit_Ki)
        self.lineEdit_Kd = QtWidgets.QLineEdit(SettingWindow)
        self.lineEdit_Kd.setObjectName("lineEdit_Kd")
        self.horizontalLayout.addWidget(self.lineEdit_Kd)
        self.label_9 = QtWidgets.QLabel(SettingWindow)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout.addWidget(self.label_9)
        self.lineEdit_trolley_max_speed = QtWidgets.QLineEdit(SettingWindow)
        self.lineEdit_trolley_max_speed.setObjectName("lineEdit_trolley_max_speed")
        self.horizontalLayout.addWidget(self.lineEdit_trolley_max_speed)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_xyxy_bottom = QtWidgets.QLabel(SettingWindow)
        self.label_xyxy_bottom.setObjectName("label_xyxy_bottom")
        self.gridLayout.addWidget(self.label_xyxy_bottom, 1, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(SettingWindow)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(SettingWindow)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(SettingWindow)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_hoist_height_bottom = QtWidgets.QLabel(SettingWindow)
        self.label_hoist_height_bottom.setObjectName("label_hoist_height_bottom")
        self.gridLayout.addWidget(self.label_hoist_height_bottom, 1, 1, 1, 1)
        self.label_hoist_height_top = QtWidgets.QLabel(SettingWindow)
        self.label_hoist_height_top.setObjectName("label_hoist_height_top")
        self.gridLayout.addWidget(self.label_hoist_height_top, 0, 1, 1, 1)
        self.label_xyxy_top = QtWidgets.QLabel(SettingWindow)
        self.label_xyxy_top.setObjectName("label_xyxy_top")
        self.gridLayout.addWidget(self.label_xyxy_top, 0, 3, 1, 1)
        self.pushButton_bottom = QtWidgets.QPushButton(SettingWindow)
        self.pushButton_bottom.setObjectName("pushButton_bottom")
        self.gridLayout.addWidget(self.pushButton_bottom, 1, 4, 1, 1)
        self.label = QtWidgets.QLabel(SettingWindow)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.pushButton_top = QtWidgets.QPushButton(SettingWindow)
        self.pushButton_top.setObjectName("pushButton_top")
        self.gridLayout.addWidget(self.pushButton_top, 0, 4, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_11 = QtWidgets.QLabel(SettingWindow)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_3.addWidget(self.label_11)
        self.lineEdit_hb_dimension_horizontal = QtWidgets.QLineEdit(SettingWindow)
        self.lineEdit_hb_dimension_horizontal.setObjectName("lineEdit_hb_dimension_horizontal")
        self.horizontalLayout_3.addWidget(self.lineEdit_hb_dimension_horizontal)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 3, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_integral = QtWidgets.QLabel(SettingWindow)
        self.label_integral.setObjectName("label_integral")
        self.horizontalLayout_2.addWidget(self.label_integral)
        self.label_prev_error = QtWidgets.QLabel(SettingWindow)
        self.label_prev_error.setObjectName("label_prev_error")
        self.horizontalLayout_2.addWidget(self.label_prev_error)
        self.label_10 = QtWidgets.QLabel(SettingWindow)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_2.addWidget(self.label_10)
        self.lineEdit_trolley_acc = QtWidgets.QLineEdit(SettingWindow)
        self.lineEdit_trolley_acc.setObjectName("lineEdit_trolley_acc")
        self.horizontalLayout_2.addWidget(self.lineEdit_trolley_acc)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)

        self.retranslateUi(SettingWindow)
        self.pushButton_top.clicked.connect(self.label_hoist_height_top.clear) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(SettingWindow)

    def retranslateUi(self, SettingWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingWindow.setWindowTitle(_translate("SettingWindow", "Dialog"))
        self.label_12.setText(_translate("SettingWindow", "HB Dimension Vertical:"))
        self.pushButton_configure.setText(_translate("SettingWindow", "Configure"))
        self.lineEdit_Kp.setText(_translate("SettingWindow", "1.5"))
        self.lineEdit_Ki.setText(_translate("SettingWindow", "0.001"))
        self.lineEdit_Kd.setText(_translate("SettingWindow", "0.01"))
        self.label_9.setText(_translate("SettingWindow", "Trolley Max Speed:"))
        self.label_xyxy_bottom.setText(_translate("SettingWindow", "8562.56"))
        self.label_3.setText(_translate("SettingWindow", "xyxy"))
        self.label_2.setText(_translate("SettingWindow", "xyxy:"))
        self.label_4.setText(_translate("SettingWindow", "Hoist Height"))
        self.label_hoist_height_bottom.setText(_translate("SettingWindow", "8562.56"))
        self.label_hoist_height_top.setText(_translate("SettingWindow", "8562.56"))
        self.label_xyxy_top.setText(_translate("SettingWindow", "8562.56"))
        self.pushButton_bottom.setText(_translate("SettingWindow", "Bottom"))
        self.label.setText(_translate("SettingWindow", "Hoist Height:"))
        self.pushButton_top.setText(_translate("SettingWindow", "Top"))
        self.label_11.setText(_translate("SettingWindow", "HB Dimension Horizontal:"))
        self.label_integral.setText(_translate("SettingWindow", "Integral"))
        self.label_prev_error.setText(_translate("SettingWindow", "Prev error"))
        self.label_10.setText(_translate("SettingWindow", "Trolley Acceleration:"))
