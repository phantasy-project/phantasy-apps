# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_app_pref.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(525, 258)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(4, 8, 4, 4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.formLayout = QtWidgets.QFormLayout(self.tab)
        self.formLayout.setContentsMargins(6, 6, 6, 6)
        self.formLayout.setSpacing(4)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit_url = QtWidgets.QLineEdit(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_url.sizePolicy().hasHeightForWidth())
        self.lineEdit_url.setSizePolicy(sizePolicy)
        self.lineEdit_url.setObjectName("lineEdit_url")
        self.horizontalLayout_2.addWidget(self.lineEdit_url)
        self.lineEdit_port = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_port.setObjectName("lineEdit_port")
        self.horizontalLayout_2.addWidget(self.lineEdit_port)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.comboBox = QtWidgets.QComboBox(self.tab)
        self.comboBox.setEnabled(True)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.srv_ctrl_btn = QtWidgets.QPushButton(self.tab)
        self.srv_ctrl_btn.setObjectName("srv_ctrl_btn")
        self.horizontalLayout.addWidget(self.srv_ctrl_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.srv_db_reset_btn = QtWidgets.QPushButton(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.srv_db_reset_btn.sizePolicy().hasHeightForWidth())
        self.srv_db_reset_btn.setSizePolicy(sizePolicy)
        self.srv_db_reset_btn.setObjectName("srv_db_reset_btn")
        self.horizontalLayout_3.addWidget(self.srv_db_reset_btn)
        self.srv_db_empty_btn = QtWidgets.QPushButton(self.tab)
        self.srv_db_empty_btn.setObjectName("srv_db_empty_btn")
        self.horizontalLayout_3.addWidget(self.srv_db_empty_btn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.formLayout.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_2.setContentsMargins(6, 6, 6, 6)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pageZoom_lbl = QtWidgets.QLabel(self.tab_2)
        self.pageZoom_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.pageZoom_lbl.setObjectName("pageZoom_lbl")
        self.gridLayout_2.addWidget(self.pageZoom_lbl, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.pageZoom_slider = QtWidgets.QSlider(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pageZoom_slider.sizePolicy().hasHeightForWidth())
        self.pageZoom_slider.setSizePolicy(sizePolicy)
        self.pageZoom_slider.setMinimum(50)
        self.pageZoom_slider.setMaximum(200)
        self.pageZoom_slider.setSingleStep(5)
        self.pageZoom_slider.setPageStep(20)
        self.pageZoom_slider.setProperty("value", 100)
        self.pageZoom_slider.setSliderPosition(100)
        self.pageZoom_slider.setOrientation(QtCore.Qt.Horizontal)
        self.pageZoom_slider.setInvertedAppearance(False)
        self.pageZoom_slider.setInvertedControls(False)
        self.pageZoom_slider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.pageZoom_slider.setTickInterval(10)
        self.pageZoom_slider.setObjectName("pageZoom_slider")
        self.gridLayout_2.addWidget(self.pageZoom_slider, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem2, 2, 1, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.tab_3)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.get_all_srv_status_btn = QtWidgets.QPushButton(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.get_all_srv_status_btn.sizePolicy().hasHeightForWidth())
        self.get_all_srv_status_btn.setSizePolicy(sizePolicy)
        self.get_all_srv_status_btn.setObjectName("get_all_srv_status_btn")
        self.horizontalLayout_4.addWidget(self.get_all_srv_status_btn)
        self.clean_all_srv_btn = QtWidgets.QPushButton(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clean_all_srv_btn.sizePolicy().hasHeightForWidth())
        self.clean_all_srv_btn.setSizePolicy(sizePolicy)
        self.clean_all_srv_btn.setObjectName("clean_all_srv_btn")
        self.horizontalLayout_4.addWidget(self.clean_all_srv_btn)
        self.popup_browser_btn = QtWidgets.QPushButton(self.tab_3)
        self.popup_browser_btn.setObjectName("popup_browser_btn")
        self.horizontalLayout_4.addWidget(self.popup_browser_btn)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.textEdit_srv_info = QtWidgets.QTextEdit(self.tab_3)
        self.textEdit_srv_info.setStyleSheet("QTextEdit {\n"
"    color: rgb(0, 0, 255);\n"
"}")
        self.textEdit_srv_info.setReadOnly(True)
        self.textEdit_srv_info.setObjectName("textEdit_srv_info")
        self.gridLayout.addWidget(self.textEdit_srv_info, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.btn_box = QtWidgets.QDialogButtonBox(Dialog)
        self.btn_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.btn_box.setObjectName("btn_box")
        self.verticalLayout.addWidget(self.btn_box)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Base URL"))
        self.lineEdit_url.setToolTip(_translate("Dialog", "<html><head/><body><p>URL</p></body></html>"))
        self.lineEdit_url.setText(_translate("Dialog", "http://127.0.0.1"))
        self.lineEdit_port.setToolTip(_translate("Dialog", "<html><head/><body><p>Port</p></body></html>"))
        self.lineEdit_port.setText(_translate("Dialog", "5000"))
        self.label_2.setText(_translate("Dialog", "API Version"))
        self.comboBox.setCurrentText(_translate("Dialog", "v1.0"))
        self.comboBox.setItemText(0, _translate("Dialog", "v1.0"))
        self.label_4.setText(_translate("Dialog", "Service Status"))
        self.srv_ctrl_btn.setText(_translate("Dialog", "START"))
        self.label_5.setText(_translate("Dialog", "Database"))
        self.srv_db_reset_btn.setToolTip(_translate("Dialog", "Reset with default database."))
        self.srv_db_reset_btn.setText(_translate("Dialog", "Reset to Default"))
        self.srv_db_empty_btn.setToolTip(_translate("Dialog", "Reset with an empty database."))
        self.srv_db_empty_btn.setText(_translate("Dialog", "Empty"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Unicorn WebApp"))
        self.pageZoom_lbl.setText(_translate("Dialog", "100 %"))
        self.label_3.setText(_translate("Dialog", "Page Zoom"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Style"))
        self.label_6.setText(_translate("Dialog", "Alive Services"))
        self.get_all_srv_status_btn.setToolTip(_translate("Dialog", "<html><head/><body><p>Get the list of all alive services.</p></body></html>"))
        self.get_all_srv_status_btn.setText(_translate("Dialog", "Update"))
        self.clean_all_srv_btn.setToolTip(_translate("Dialog", "<html><head/><body><p>Terminate all other alive services.</p></body></html>"))
        self.clean_all_srv_btn.setText(_translate("Dialog", "Clean Up"))
        self.popup_browser_btn.setToolTip(_translate("Dialog", "<html><head/><body><p>Access &amp; control UNICORN in the web browser</p></body></html>"))
        self.popup_browser_btn.setText(_translate("Dialog", "Start with Browser"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "Advance"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
