# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_app_pref.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 600)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.formLayout = QtWidgets.QFormLayout(self.tab)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole,
                                  self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit_url = QtWidgets.QLineEdit(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lineEdit_url.sizePolicy().hasHeightForWidth())
        self.lineEdit_url.setSizePolicy(sizePolicy)
        self.lineEdit_url.setObjectName("lineEdit_url")
        self.horizontalLayout_2.addWidget(self.lineEdit_url)
        self.lineEdit_port = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_port.setObjectName("lineEdit_port")
        self.horizontalLayout_2.addWidget(self.lineEdit_port)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole,
                                  self.horizontalLayout_2)
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole,
                                  self.label_2)
        self.comboBox = QtWidgets.QComboBox(self.tab)
        self.comboBox.setEnabled(True)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole,
                                  self.comboBox)
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole,
                                  self.label_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole,
                                  self.horizontalLayout)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setContentsMargins(10, 10, 10, 10)
        self.formLayout_2.setSpacing(10)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole,
                                    self.label_3)
        self.pageZoom = QtWidgets.QComboBox(self.tab_2)
        self.pageZoom.setModelColumn(0)
        self.pageZoom.setObjectName("pageZoom")
        self.pageZoom.addItem("")
        self.pageZoom.addItem("")
        self.pageZoom.addItem("")
        self.pageZoom.addItem("")
        self.pageZoom.addItem("")
        self.pageZoom.addItem("")
        self.pageZoom.addItem("")
        self.pageZoom.addItem("")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole,
                                    self.pageZoom)
        self.gridLayout_2.addLayout(self.formLayout_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.btn_box = QtWidgets.QDialogButtonBox(Dialog)
        self.btn_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel |
                                        QtWidgets.QDialogButtonBox.Ok)
        self.btn_box.setObjectName("btn_box")
        self.verticalLayout.addWidget(self.btn_box)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.pageZoom.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Base URL"))
        self.lineEdit_url.setToolTip(_translate("Dialog", "URL"))
        self.lineEdit_url.setText(_translate("Dialog", "http://127.0.0.1"))
        self.lineEdit_port.setToolTip(_translate("Dialog", "Port"))
        self.lineEdit_port.setText(_translate("Dialog", "5000"))
        self.label_2.setText(_translate("Dialog", "API Version"))
        self.comboBox.setCurrentText(_translate("Dialog", "v1.0"))
        self.comboBox.setItemText(0, _translate("Dialog", "v1.0"))
        self.label_4.setText(_translate("Dialog", "Server Status"))
        self.pushButton_2.setText(_translate("Dialog", "START"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab),
            _translate("Dialog", "Unicorn WebApp"))
        self.label_3.setText(_translate("Dialog", "Page Zoom"))
        self.pageZoom.setCurrentText(_translate("Dialog", "100%"))
        self.pageZoom.setItemText(0, _translate("Dialog", "75%"))
        self.pageZoom.setItemText(1, _translate("Dialog", "80%"))
        self.pageZoom.setItemText(2, _translate("Dialog", "90%"))
        self.pageZoom.setItemText(3, _translate("Dialog", "100%"))
        self.pageZoom.setItemText(4, _translate("Dialog", "110%"))
        self.pageZoom.setItemText(5, _translate("Dialog", "125%"))
        self.pageZoom.setItemText(6, _translate("Dialog", "150%"))
        self.pageZoom.setItemText(7, _translate("Dialog", "200%"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Style"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
