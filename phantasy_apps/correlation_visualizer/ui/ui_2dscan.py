# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_2dscan.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1132, 981)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.alter_elem_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.alter_elem_lineEdit.setGeometry(QtCore.QRect(171, 33, 386, 38))
        self.alter_elem_lineEdit.setText("")
        self.alter_elem_lineEdit.setObjectName("alter_elem_lineEdit")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(575, 80, 115, 40))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.enable_arbitary_array_chkbox = QtWidgets.QCheckBox(
            self.horizontalLayoutWidget)
        self.enable_arbitary_array_chkbox.setText("")
        self.enable_arbitary_array_chkbox.setObjectName(
            "enable_arbitary_array_chkbox")
        self.horizontalLayout_7.addWidget(self.enable_arbitary_array_chkbox)
        self.alter_array_btn = QtWidgets.QPushButton(
            self.horizontalLayoutWidget)
        self.alter_array_btn.setObjectName("alter_array_btn")
        self.horizontalLayout_7.addWidget(self.alter_array_btn)
        self.select_alter_elem_btn = QtWidgets.QPushButton(self.centralwidget)
        self.select_alter_elem_btn.setGeometry(QtCore.QRect(575, 33, 115, 38))
        self.select_alter_elem_btn.setObjectName("select_alter_elem_btn")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(354, 80, 20, 40))
        self.label_17.setObjectName("label_17")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(50, 33, 115, 38))
        self.label_15.setObjectName("label_15")
        self.upper_limit_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.upper_limit_lineEdit.setGeometry(QtCore.QRect(380, 81, 177, 38))
        self.upper_limit_lineEdit.setObjectName("upper_limit_lineEdit")
        self.lower_limit_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lower_limit_lineEdit.setGeometry(QtCore.QRect(171, 81, 177, 38))
        self.lower_limit_lineEdit.setObjectName("lower_limit_lineEdit")
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(50, 80, 115, 40))
        self.label_16.setObjectName("label_16")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1132, 32))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.alter_elem_lineEdit.setPlaceholderText(
            _translate("MainWindow", "Click \'Select\' to set element"))
        self.alter_array_btn.setText(_translate("MainWindow", "Array"))
        self.select_alter_elem_btn.setText(_translate("MainWindow", "Select"))
        self.label_17.setText(_translate("MainWindow", "To"))
        self.label_15.setText(_translate("MainWindow", "Alter Element"))
        self.label_16.setText(_translate("MainWindow", "Alter Range"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
