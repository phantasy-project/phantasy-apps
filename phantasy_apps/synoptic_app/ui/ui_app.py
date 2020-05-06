# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_app.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(6, 12, 6, 6)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.settling_time_dsbox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.settling_time_dsbox.setDecimals(1)
        self.settling_time_dsbox.setMinimum(0.2)
        self.settling_time_dsbox.setProperty("value", 1.0)
        self.settling_time_dsbox.setObjectName("settling_time_dsbox")
        self.horizontalLayout_2.addWidget(self.settling_time_dsbox)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.start_data_agent_btn = QtWidgets.QPushButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/sn-app/icons/start.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.start_data_agent_btn.setIcon(icon)
        self.start_data_agent_btn.setObjectName("start_data_agent_btn")
        self.horizontalLayout_2.addWidget(self.start_data_agent_btn)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.vbox.setObjectName("vbox")
        self.gridLayout.addLayout(self.vbox, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.current_pointed_device_lineEdit = QtWidgets.QLineEdit(
            self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.current_pointed_device_lineEdit.setFont(font)
        self.current_pointed_device_lineEdit.setObjectName(
            "current_pointed_device_lineEdit")
        self.horizontalLayout.addWidget(self.current_pointed_device_lineEdit)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 27))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_About = QtWidgets.QAction(MainWindow)
        self.action_About.setObjectName("action_About")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        self.actionE_xit.setObjectName("actionE_xit")
        self.actionContents = QtWidgets.QAction(MainWindow)
        self.actionContents.setObjectName("actionContents")
        self.action_Open = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/sn-app/icons/open.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Open.setIcon(icon1)
        self.action_Open.setObjectName("action_Open")
        self.action_zoom_in = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/sn-app/icons/zoom_in.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_zoom_in.setIcon(icon2)
        self.action_zoom_in.setObjectName("action_zoom_in")
        self.action_zoom_out = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/sn-app/icons/zoom_out.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_zoom_out.setIcon(icon3)
        self.action_zoom_out.setObjectName("action_zoom_out")
        self.action_zoom_reset = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/sn-app/icons/zoom_reset.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_zoom_reset.setIcon(icon4)
        self.action_zoom_reset.setObjectName("action_zoom_reset")
        self.action_zoom_page_fit = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/sn-app/icons/zoom_page-fit.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_zoom_page_fit.setIcon(icon5)
        self.action_zoom_page_fit.setObjectName("action_zoom_page_fit")
        self.actionLoad_Lattice = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/sn-app/icons/load_lattice.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoad_Lattice.setIcon(icon6)
        self.actionLoad_Lattice.setObjectName("actionLoad_Lattice")
        self.menu_File.addSeparator()
        self.menu_Help.addAction(self.actionContents)
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.action_About)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.toolBar.addAction(self.action_Open)
        self.toolBar.addAction(self.actionLoad_Lattice)
        self.toolBar.addAction(self.action_zoom_in)
        self.toolBar.addAction(self.action_zoom_out)
        self.toolBar.addAction(self.action_zoom_reset)
        self.toolBar.addAction(self.action_zoom_page_fit)
        self.toolBar.addAction(self.actionE_xit)

        self.retranslateUi(MainWindow)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.actionE_xit.triggered.connect(MainWindow.close)
        self.action_About.triggered.connect(MainWindow.onAbout)
        self.action_Open.triggered.connect(MainWindow.on_open_file)
        self.action_zoom_in.triggered.connect(MainWindow.on_zoom_in_view)
        self.action_zoom_out.triggered.connect(MainWindow.on_zoom_out_view)
        self.action_zoom_reset.triggered.connect(MainWindow.on_zoom_set_view)
        self.action_zoom_page_fit.triggered.connect(
            MainWindow.on_zoom_fit_page_view)
        self.start_data_agent_btn.clicked.connect(
            MainWindow.on_click_start_btn)
        self.actionLoad_Lattice.triggered.connect(MainWindow.on_load_lattice)
        self.settling_time_dsbox.valueChanged['double'].connect(
            MainWindow.on_settling_time_changed)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Update data every"))
        self.label_3.setText(_translate("MainWindow", "second(s)"))
        self.start_data_agent_btn.setText(_translate("MainWindow", "START"))
        self.label.setText(_translate("MainWindow", "Pointed Device"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action_About.setText(_translate("MainWindow", "&About"))
        self.action_About.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))
        self.actionE_xit.setText(_translate("MainWindow", "E&xit"))
        self.actionE_xit.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionContents.setText(_translate("MainWindow", "Contents"))
        self.actionContents.setShortcut(_translate("MainWindow", "F1"))
        self.action_Open.setText(_translate("MainWindow", "&Open"))
        self.action_zoom_in.setText(_translate("MainWindow", "zoom_in"))
        self.action_zoom_in.setIconText(_translate("MainWindow", "Zoom In"))
        self.action_zoom_in.setToolTip(
            _translate("MainWindow", "Enlarge the view."))
        self.action_zoom_out.setText(_translate("MainWindow", "zoom_out"))
        self.action_zoom_out.setIconText(_translate("MainWindow", "Zom Out"))
        self.action_zoom_out.setToolTip(
            _translate("MainWindow", "Shrink the view."))
        self.action_zoom_reset.setText(_translate("MainWindow", "zoom_reset"))
        self.action_zoom_reset.setIconText(
            _translate("MainWindow", "Reset View"))
        self.action_zoom_reset.setToolTip(
            _translate("MainWindow", "Reset the view."))
        self.action_zoom_page_fit.setText(
            _translate("MainWindow", "zoom_page_fit"))
        self.action_zoom_page_fit.setIconText(
            _translate("MainWindow", "Fit Page"))
        self.action_zoom_page_fit.setToolTip(
            _translate("MainWindow", "Page fit the view."))
        self.actionLoad_Lattice.setText(
            _translate("MainWindow", "Load Lattice"))
        self.actionLoad_Lattice.setToolTip(
            _translate("MainWindow", "Load lattice."))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
