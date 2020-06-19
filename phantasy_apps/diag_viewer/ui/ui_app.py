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
        MainWindow.resize(1300, 975)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/dv.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QProgressBar {\n"
                                 "    border: 1px solid gray;\n"
                                 "    border-radius: 5px;\n"
                                 "    height: 5px;\n"
                                 "}\n"
                                 "\n"
                                 "QProgressBar::chunk {\n"
                                 "    background-color: #05B8CC;\n"
                                 "    width: 15px;\n"
                                 "    margin: 0.5px;\n"
                                 "}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(6, 12, 6, 6)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.plot_gbox = QtWidgets.QGroupBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.plot_gbox.sizePolicy().hasHeightForWidth())
        self.plot_gbox.setSizePolicy(sizePolicy)
        self.plot_gbox.setObjectName("plot_gbox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.plot_gbox)
        self.horizontalLayout_3.setContentsMargins(4, 10, 4, 4)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.matplotlibbarWidget = MatplotlibBarWidget(self.plot_gbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.matplotlibbarWidget.sizePolicy().hasHeightForWidth())
        self.matplotlibbarWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("sans-serif")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.matplotlibbarWidget.setFigureXYlabelFont(font)
        font = QtGui.QFont()
        font.setFamily("sans-serif")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.matplotlibbarWidget.setFigureTitleFont(font)
        self.matplotlibbarWidget.setFigureGridToggle(True)
        self.matplotlibbarWidget.setFigureMTicksToggle(True)
        font = QtGui.QFont()
        font.setFamily("sans-serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.matplotlibbarWidget.setFigureXYticksFont(font)
        self.matplotlibbarWidget.setProperty("figureBarWidth", 0.8)
        self.matplotlibbarWidget.setObjectName("matplotlibbarWidget")
        self.horizontalLayout_3.addWidget(self.matplotlibbarWidget)
        self.device_gbox = QtWidgets.QGroupBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.device_gbox.sizePolicy().hasHeightForWidth())
        self.device_gbox.setSizePolicy(sizePolicy)
        self.device_gbox.setMinimumSize(QtCore.QSize(300, 0))
        self.device_gbox.setObjectName("device_gbox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.device_gbox)
        self.verticalLayout_2.setContentsMargins(4, 10, 4, 4)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.device_select_hbox = QtWidgets.QHBoxLayout()
        self.device_select_hbox.setSpacing(6)
        self.device_select_hbox.setObjectName("device_select_hbox")
        self.refresh_bpm_btn = QtWidgets.QToolButton(self.device_gbox)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/refresh.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refresh_bpm_btn.setIcon(icon1)
        self.refresh_bpm_btn.setObjectName("refresh_bpm_btn")
        self.device_select_hbox.addWidget(self.refresh_bpm_btn)
        self.select_all_elems_btn = QtWidgets.QToolButton(self.device_gbox)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/select-all.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.select_all_elems_btn.setIcon(icon2)
        self.select_all_elems_btn.setIconSize(QtCore.QSize(20, 20))
        self.select_all_elems_btn.setObjectName("select_all_elems_btn")
        self.device_select_hbox.addWidget(self.select_all_elems_btn)
        self.inverse_selection_btn = QtWidgets.QToolButton(self.device_gbox)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/invert-selection.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.inverse_selection_btn.setIcon(icon3)
        self.inverse_selection_btn.setIconSize(QtCore.QSize(20, 20))
        self.inverse_selection_btn.setObjectName("inverse_selection_btn")
        self.device_select_hbox.addWidget(self.inverse_selection_btn)
        self.field_cbb = QtWidgets.QComboBox(self.device_gbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.field_cbb.sizePolicy().hasHeightForWidth())
        self.field_cbb.setSizePolicy(sizePolicy)
        self.field_cbb.setObjectName("field_cbb")
        self.device_select_hbox.addWidget(self.field_cbb)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.device_select_hbox.addItem(spacerItem)
        self.choose_elems_btn = QtWidgets.QPushButton(self.device_gbox)
        self.choose_elems_btn.setIconSize(QtCore.QSize(20, 20))
        self.choose_elems_btn.setObjectName("choose_elems_btn")
        self.device_select_hbox.addWidget(self.choose_elems_btn)
        self.verticalLayout_2.addLayout(self.device_select_hbox)
        self.devices_treeView = QtWidgets.QTreeView(self.device_gbox)
        self.devices_treeView.setObjectName("devices_treeView")
        self.verticalLayout_2.addWidget(self.devices_treeView)
        self.verticalLayout.addWidget(self.splitter)
        self.control_gbox = QtWidgets.QGroupBox(self.centralwidget)
        self.control_gbox.setObjectName("control_gbox")
        self.gridLayout = QtWidgets.QGridLayout(self.control_gbox)
        self.gridLayout.setContentsMargins(4, 10, 4, 4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.daq_hbox = QtWidgets.QHBoxLayout()
        self.daq_hbox.setSpacing(4)
        self.daq_hbox.setObjectName("daq_hbox")
        self.label_2 = QtWidgets.QLabel(self.control_gbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.daq_hbox.addWidget(self.label_2)
        self.daqfreq_dSpinbox = QtWidgets.QDoubleSpinBox(self.control_gbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.daqfreq_dSpinbox.sizePolicy().hasHeightForWidth())
        self.daqfreq_dSpinbox.setSizePolicy(sizePolicy)
        self.daqfreq_dSpinbox.setDecimals(1)
        self.daqfreq_dSpinbox.setMinimum(0.0)
        self.daqfreq_dSpinbox.setMaximum(10.0)
        self.daqfreq_dSpinbox.setSingleStep(0.5)
        self.daqfreq_dSpinbox.setProperty("value", 1.0)
        self.daqfreq_dSpinbox.setObjectName("daqfreq_dSpinbox")
        self.daq_hbox.addWidget(self.daqfreq_dSpinbox)
        self.label = QtWidgets.QLabel(self.control_gbox)
        self.label.setObjectName("label")
        self.daq_hbox.addWidget(self.label)
        self.daq_nshot_sbox = QtWidgets.QSpinBox(self.control_gbox)
        self.daq_nshot_sbox.setSuffix("")
        self.daq_nshot_sbox.setMinimum(1)
        self.daq_nshot_sbox.setMaximum(3000)
        self.daq_nshot_sbox.setObjectName("daq_nshot_sbox")
        self.daq_hbox.addWidget(self.daq_nshot_sbox)
        self.daq_status_lbl = QtWidgets.QLabel(self.control_gbox)
        self.daq_status_lbl.setText("")
        self.daq_status_lbl.setPixmap(QtGui.QPixmap(":/icons/inactive.png"))
        self.daq_status_lbl.setObjectName("daq_status_lbl")
        self.daq_hbox.addWidget(self.daq_status_lbl)
        self.viz_cnt_lbl = QtWidgets.QLabel(self.control_gbox)
        self.viz_cnt_lbl.setObjectName("viz_cnt_lbl")
        self.daq_hbox.addWidget(self.viz_cnt_lbl)
        self.daq_pb = QtWidgets.QProgressBar(self.control_gbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.daq_pb.sizePolicy().hasHeightForWidth())
        self.daq_pb.setSizePolicy(sizePolicy)
        self.daq_pb.setProperty("value", 0)
        self.daq_pb.setAlignment(QtCore.Qt.AlignCenter)
        self.daq_pb.setObjectName("daq_pb")
        self.daq_hbox.addWidget(self.daq_pb)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.daq_hbox.addItem(spacerItem1)
        self.capture_btn = QtWidgets.QPushButton(self.control_gbox)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/single.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.capture_btn.setIcon(icon4)
        self.capture_btn.setObjectName("capture_btn")
        self.daq_hbox.addWidget(self.capture_btn)
        self.start_btn = QtWidgets.QPushButton(self.control_gbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.start_btn.sizePolicy().hasHeightForWidth())
        self.start_btn.setSizePolicy(sizePolicy)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/start.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.start_btn.setIcon(icon5)
        self.start_btn.setObjectName("start_btn")
        self.daq_hbox.addWidget(self.start_btn)
        self.stop_btn = QtWidgets.QPushButton(self.control_gbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stop_btn.sizePolicy().hasHeightForWidth())
        self.stop_btn.setSizePolicy(sizePolicy)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/stop.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.stop_btn.setIcon(icon6)
        self.stop_btn.setObjectName("stop_btn")
        self.daq_hbox.addWidget(self.stop_btn)
        self.gridLayout.addLayout(self.daq_hbox, 1, 1, 1, 2)
        self.viz_hbox = QtWidgets.QHBoxLayout()
        self.viz_hbox.setSpacing(4)
        self.viz_hbox.setObjectName("viz_hbox")
        self.label_11 = QtWidgets.QLabel(self.control_gbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setObjectName("label_11")
        self.viz_hbox.addWidget(self.label_11)
        self.id_as_x_rbtn = QtWidgets.QRadioButton(self.control_gbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.id_as_x_rbtn.sizePolicy().hasHeightForWidth())
        self.id_as_x_rbtn.setSizePolicy(sizePolicy)
        self.id_as_x_rbtn.setObjectName("id_as_x_rbtn")
        self.xaxis_data_group = QtWidgets.QButtonGroup(MainWindow)
        self.xaxis_data_group.setObjectName("xaxis_data_group")
        self.xaxis_data_group.addButton(self.id_as_x_rbtn)
        self.viz_hbox.addWidget(self.id_as_x_rbtn)
        self.pos_as_x_rbtn = QtWidgets.QRadioButton(self.control_gbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pos_as_x_rbtn.sizePolicy().hasHeightForWidth())
        self.pos_as_x_rbtn.setSizePolicy(sizePolicy)
        self.pos_as_x_rbtn.setObjectName("pos_as_x_rbtn")
        self.xaxis_data_group.addButton(self.pos_as_x_rbtn)
        self.viz_hbox.addWidget(self.pos_as_x_rbtn)
        self.line_4 = QtWidgets.QFrame(self.control_gbox)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.viz_hbox.addWidget(self.line_4)
        self.show_dnum_rbtn = QtWidgets.QRadioButton(self.control_gbox)
        self.show_dnum_rbtn.setObjectName("show_dnum_rbtn")
        self.xticklbls_group = QtWidgets.QButtonGroup(MainWindow)
        self.xticklbls_group.setObjectName("xticklbls_group")
        self.xticklbls_group.addButton(self.show_dnum_rbtn)
        self.viz_hbox.addWidget(self.show_dnum_rbtn)
        self.show_dname_rbtn = QtWidgets.QRadioButton(self.control_gbox)
        self.show_dname_rbtn.setObjectName("show_dname_rbtn")
        self.xticklbls_group.addButton(self.show_dname_rbtn)
        self.viz_hbox.addWidget(self.show_dname_rbtn)
        self.annote_height_chkbox = QtWidgets.QCheckBox(self.control_gbox)
        self.annote_height_chkbox.setObjectName("annote_height_chkbox")
        self.viz_hbox.addWidget(self.annote_height_chkbox)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.viz_hbox.addItem(spacerItem2)
        self.gridLayout.addLayout(self.viz_hbox, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.control_gbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignRight
                                  | QtCore.Qt.AlignTrailing
                                  | QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.control_gbox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignRight
                                  | QtCore.Qt.AlignTrailing
                                  | QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)
        self.reset_figure_btn = QtWidgets.QPushButton(self.control_gbox)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/load.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.reset_figure_btn.setIcon(icon7)
        self.reset_figure_btn.setObjectName("reset_figure_btn")
        self.gridLayout.addWidget(self.reset_figure_btn, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.control_gbox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1300, 27))
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
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        self.actionE_xit.setObjectName("actionE_xit")
        self.action_About = QtWidgets.QAction(MainWindow)
        self.action_About.setObjectName("action_About")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionLoad_Lattice = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/load_lattice.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoad_Lattice.setIcon(icon8)
        self.actionLoad_Lattice.setObjectName("actionLoad_Lattice")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/save.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.actionSave.setIcon(icon9)
        self.actionSave.setObjectName("actionSave")
        self.menu_File.addSeparator()
        self.menu_Help.addAction(self.action_About)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.toolBar.addAction(self.actionLoad_Lattice)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionE_xit)

        self.retranslateUi(MainWindow)
        self.action_About.triggered.connect(MainWindow.onAbout)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.actionE_xit.triggered.connect(MainWindow.close)
        self.id_as_x_rbtn.toggled['bool'].connect(
            MainWindow.on_apply_id_as_xdata)
        self.pos_as_x_rbtn.toggled['bool'].connect(
            MainWindow.on_apply_pos_as_xdata)
        self.start_btn.clicked.connect(MainWindow.on_daq_start)
        self.stop_btn.clicked.connect(MainWindow.on_daq_stop)
        self.reset_figure_btn.clicked.connect(MainWindow.on_init_dataviz)
        self.annote_height_chkbox.toggled['bool'].connect(
            MainWindow.on_annote_height)
        self.actionLoad_Lattice.triggered.connect(
            MainWindow.onLoadLatticeAction)
        self.capture_btn.clicked.connect(MainWindow.on_single_viz_update)
        self.actionSave.triggered.connect(MainWindow.on_save_data)
        self.show_dnum_rbtn.toggled['bool'].connect(MainWindow.on_show_dnum)
        self.show_dname_rbtn.toggled['bool'].connect(MainWindow.on_show_dname)
        self.refresh_bpm_btn.clicked.connect(MainWindow.on_refresh_model)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.plot_gbox.setTitle(_translate("MainWindow", "Data Visualization"))
        self.device_gbox.setTitle(_translate("MainWindow", "Devices"))
        self.refresh_bpm_btn.setToolTip(
            _translate("MainWindow", "Refresh BPMs selection."))
        self.refresh_bpm_btn.setText(_translate("MainWindow", "..."))
        self.select_all_elems_btn.setToolTip(
            _translate("MainWindow",
                       "<html><head/><body><p>Select All</p></body></html>"))
        self.select_all_elems_btn.setText(
            _translate("MainWindow", "Select All"))
        self.inverse_selection_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Inverse Current Selection</p></body></html>"
            ))
        self.inverse_selection_btn.setText(
            _translate("MainWindow", "Inverse Selection"))
        self.choose_elems_btn.setText(_translate("MainWindow", "Choose"))
        self.control_gbox.setTitle(_translate("MainWindow", "Control Panel"))
        self.label_2.setText(_translate("MainWindow", "Frequency"))
        self.daqfreq_dSpinbox.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Total number of shot captured in one second.</p></body></html>"
            ))
        self.daqfreq_dSpinbox.setSuffix(_translate("MainWindow", " Hz"))
        self.label.setText(_translate("MainWindow", "Shot Number"))
        self.daq_nshot_sbox.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Total shot number in one DAQ iteration.</p></body></html>"
            ))
        self.viz_cnt_lbl.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Completed DAQ iterations.</p></body></html>"
            ))
        self.viz_cnt_lbl.setText(_translate("MainWindow", "0"))
        self.capture_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Do single DAQ.</p></body></html>"))
        self.capture_btn.setText(_translate("MainWindow", "Capture"))
        self.start_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Do DAQ untile Stop button is pushed.</p></body></html>"
            ))
        self.start_btn.setText(_translate("MainWindow", "Start"))
        self.stop_btn.setToolTip(
            _translate("MainWindow",
                       "<html><head/><body><p>Stop DAQ.</p></body></html>"))
        self.stop_btn.setText(_translate("MainWindow", "Stop"))
        self.label_11.setText(_translate("MainWindow", "X-Axis"))
        self.id_as_x_rbtn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Apply device sequece order as x data.</p></body></html>"
            ))
        self.id_as_x_rbtn.setText(_translate("MainWindow", "ID"))
        self.pos_as_x_rbtn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Apply device longitudinal position as x data.</p></body></html>"
            ))
        self.pos_as_x_rbtn.setText(_translate("MainWindow", "Position"))
        self.show_dnum_rbtn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Show device D-numbers as xticks.</p></body></html>"
            ))
        self.show_dnum_rbtn.setText(_translate("MainWindow", "D####"))
        self.show_dname_rbtn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Show device names as xticks.</p></body></html>"
            ))
        self.show_dname_rbtn.setText(_translate("MainWindow", "Device Name"))
        self.annote_height_chkbox.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Show bar height values as annotations.</p></body></html>"
            ))
        self.annote_height_chkbox.setText(
            _translate("MainWindow", "Height Annotation"))
        self.label_5.setText(_translate("MainWindow", "DataViz"))
        self.label_6.setText(_translate("MainWindow", "DAQ"))
        self.reset_figure_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Reset figure is always required after changing any configuration, before Capture/Start.</p></body></html>"
            ))
        self.reset_figure_btn.setText(_translate("MainWindow", "Reset"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionE_xit.setText(_translate("MainWindow", "E&xit"))
        self.actionE_xit.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.action_About.setText(_translate("MainWindow", "&About"))
        self.action_About.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))
        self.actionLoad_Lattice.setText(
            _translate("MainWindow", "Load Lattice"))
        self.actionLoad_Lattice.setShortcut(
            _translate("MainWindow", "Ctrl+Shift+L"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))


from mpl4qt.widgets.mplbarwidget import MatplotlibBarWidget
from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
