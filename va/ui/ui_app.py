# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_app.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(868, 391)
        MainWindow.setStyleSheet(
            "QGroupBox {\n"
            "    /*background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #E0E0E0, stop: 1 #E0E0E0);\n"
            "   */\n"
            "    border: 2px solid gray;\n"
            "    border-radius: 5px;\n"
            "    margin-top: 1.5ex; /* leave space at the top for the title */\n"
            "    margin-bottom: 0.5ex;\n"
            "}\n"
            "\n"
            "QGroupBox::title {\n"
            "    subcontrol-origin: margin;\n"
            "    subcontrol-position: top center; /* position at the top center */\n"
            "    padding: 0 3px;\n"
            "    /*background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #EDECEB, stop: 1 #FFFFFF);\n"
            "    */\n"
            "}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.config_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.config_groupBox.setObjectName("config_groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.config_groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.config_groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.mach_comboBox = QtWidgets.QComboBox(self.config_groupBox)
        self.mach_comboBox.setObjectName("mach_comboBox")
        self.mach_comboBox.addItem("")
        self.mach_comboBox.addItem("")
        self.mach_comboBox.addItem("")
        self.gridLayout.addWidget(self.mach_comboBox, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.config_groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.engine_comboBox = QtWidgets.QComboBox(self.config_groupBox)
        self.engine_comboBox.setObjectName("engine_comboBox")
        self.engine_comboBox.addItem("")
        self.engine_comboBox.addItem("")
        self.gridLayout.addWidget(self.engine_comboBox, 0, 3, 1, 1)
        self.verticalLayout.addWidget(self.config_groupBox)
        self.control_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.control_groupBox.sizePolicy().hasHeightForWidth())
        self.control_groupBox.setSizePolicy(sizePolicy)
        self.control_groupBox.setObjectName("control_groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.control_groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.run_tbtn = QtWidgets.QToolButton(self.control_groupBox)
        self.run_tbtn.setObjectName("run_tbtn")
        self.horizontalLayout_3.addWidget(self.run_tbtn)
        self.stop_tbtn = QtWidgets.QToolButton(self.control_groupBox)
        self.stop_tbtn.setObjectName("stop_tbtn")
        self.horizontalLayout_3.addWidget(self.stop_tbtn)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.va_status_label = QtWidgets.QLabel(self.control_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.va_status_label.sizePolicy().hasHeightForWidth())
        self.va_status_label.setSizePolicy(sizePolicy)
        self.va_status_label.setText("")
        self.va_status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.va_status_label.setObjectName("va_status_label")
        self.horizontalLayout_2.addWidget(self.va_status_label)
        self.label_3 = QtWidgets.QLabel(self.control_groupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.uptime_label = QtWidgets.QLabel(self.control_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.uptime_label.sizePolicy().hasHeightForWidth())
        self.uptime_label.setSizePolicy(sizePolicy)
        self.uptime_label.setStyleSheet("QLabel {\n"
                                        "    font-family: monospace;\n"
                                        "}")
        self.uptime_label.setAlignment(QtCore.Qt.AlignRight
                                       | QtCore.Qt.AlignTrailing
                                       | QtCore.Qt.AlignVCenter)
        self.uptime_label.setObjectName("uptime_label")
        self.horizontalLayout_2.addWidget(self.uptime_label)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.control_groupBox)
        self.tools_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tools_groupBox.sizePolicy().hasHeightForWidth())
        self.tools_groupBox.setSizePolicy(sizePolicy)
        self.tools_groupBox.setObjectName("tools_groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tools_groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.open_notebook_tbtn = QtWidgets.QToolButton(self.tools_groupBox)
        self.open_notebook_tbtn.setObjectName("open_notebook_tbtn")
        self.horizontalLayout.addWidget(self.open_notebook_tbtn)
        self.open_workdir_tbtn = QtWidgets.QToolButton(self.tools_groupBox)
        self.open_workdir_tbtn.setObjectName("open_workdir_tbtn")
        self.horizontalLayout.addWidget(self.open_workdir_tbtn)
        self.view_log_tbtn = QtWidgets.QToolButton(self.tools_groupBox)
        self.view_log_tbtn.setObjectName("view_log_tbtn")
        self.horizontalLayout.addWidget(self.view_log_tbtn)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addWidget(self.tools_groupBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 868, 30))
        self.menubar.setObjectName("menubar")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionContents = QtWidgets.QAction(MainWindow)
        self.actionContents.setObjectName("actionContents")
        self.menu_Help.addAction(self.actionContents)
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        self.actionAbout.triggered.connect(MainWindow.onAbout)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.run_tbtn.clicked.connect(MainWindow.on_run_va)
        self.stop_tbtn.clicked.connect(MainWindow.on_stop_va)
        self.mach_comboBox.currentTextChanged['QString'].connect(
            MainWindow.on_machine_changed)
        self.engine_comboBox.currentTextChanged['QString'].connect(
            MainWindow.on_engine_changed)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.mach_comboBox, self.engine_comboBox)
        MainWindow.setTabOrder(self.engine_comboBox, self.run_tbtn)
        MainWindow.setTabOrder(self.run_tbtn, self.open_notebook_tbtn)
        MainWindow.setTabOrder(self.open_notebook_tbtn, self.open_workdir_tbtn)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.config_groupBox.setTitle(
            _translate("MainWindow", "Configuration"))
        self.label.setText(_translate("MainWindow", "Accelerator"))
        self.mach_comboBox.setItemText(0, _translate("MainWindow", "LEBT"))
        self.mach_comboBox.setItemText(1, _translate("MainWindow", "MEBT"))
        self.mach_comboBox.setItemText(2, _translate("MainWindow",
                                                     "VA_LS1FS1"))
        self.label_2.setText(_translate("MainWindow", "Model Engine"))
        self.engine_comboBox.setItemText(0, _translate("MainWindow", "FLAME"))
        self.engine_comboBox.setItemText(1, _translate("MainWindow", "IMPACT"))
        self.control_groupBox.setTitle(_translate("MainWindow", "Control"))
        self.run_tbtn.setText(_translate("MainWindow", "RUN"))
        self.stop_tbtn.setText(_translate("MainWindow", "STOP"))
        self.label_3.setText(_translate("MainWindow", "Uptime"))
        self.uptime_label.setText(_translate("MainWindow", "00:00:00"))
        self.tools_groupBox.setTitle(_translate("MainWindow", "Tools"))
        self.open_notebook_tbtn.setText(_translate("MainWindow", "Notebook"))
        self.open_workdir_tbtn.setText(_translate("MainWindow", "Work Dir"))
        self.view_log_tbtn.setText(_translate("MainWindow", "View Log"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))
        self.actionContents.setText(_translate("MainWindow", "Contents"))
        self.actionContents.setShortcut(_translate("MainWindow", "F1"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
