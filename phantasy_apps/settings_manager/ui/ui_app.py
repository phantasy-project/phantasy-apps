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
        MainWindow.resize(1600, 1200)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.apply_btn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.apply_btn.sizePolicy().hasHeightForWidth())
        self.apply_btn.setSizePolicy(sizePolicy)
        self.apply_btn.setObjectName("apply_btn")
        self.gridLayout.addWidget(self.apply_btn, 2, 1, 1, 1)
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setObjectName("treeView")
        self.gridLayout.addWidget(self.treeView, 1, 0, 1, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.reload_lattice_btn = QtWidgets.QToolButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/sm-icons/reload.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reload_lattice_btn.setIcon(icon)
        self.reload_lattice_btn.setAutoRaise(True)
        self.reload_lattice_btn.setObjectName("reload_lattice_btn")
        self.horizontalLayout.addWidget(self.reload_lattice_btn)
        self.lv_lbl = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lv_lbl.sizePolicy().hasHeightForWidth())
        self.lv_lbl.setSizePolicy(sizePolicy)
        self.lv_lbl.setObjectName("lv_lbl")
        self.horizontalLayout.addWidget(self.lv_lbl)
        self.lv_view_btn = QtWidgets.QToolButton(self.centralwidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/sm-icons/view-details.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.lv_view_btn.setIcon(icon1)
        self.lv_view_btn.setAutoRaise(True)
        self.lv_view_btn.setObjectName("lv_view_btn")
        self.horizontalLayout.addWidget(self.lv_view_btn)
        self.lv_mach_lbl = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lv_mach_lbl.sizePolicy().hasHeightForWidth())
        self.lv_mach_lbl.setSizePolicy(sizePolicy)
        self.lv_mach_lbl.setStyleSheet("QLabel {\n"
                                       "    color: #007BFF;\n"
                                       "}")
        self.lv_mach_lbl.setObjectName("lv_mach_lbl")
        self.horizontalLayout.addWidget(self.lv_mach_lbl)
        self.lv_segm_lbl = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lv_segm_lbl.sizePolicy().hasHeightForWidth())
        self.lv_segm_lbl.setSizePolicy(sizePolicy)
        self.lv_segm_lbl.setStyleSheet("QLabel {\n"
                                       "    color: #DC3545;\n"
                                       "}")
        self.lv_segm_lbl.setObjectName("lv_segm_lbl")
        self.horizontalLayout.addWidget(self.lv_segm_lbl)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.total_elem_number_lbl = QtWidgets.QLabel(self.centralwidget)
        self.total_elem_number_lbl.setStyleSheet("QLabel {\n"
                                                 "    color: #28A745;\n"
                                                 "}")
        self.total_elem_number_lbl.setObjectName("total_elem_number_lbl")
        self.horizontalLayout.addWidget(self.total_elem_number_lbl)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.total_sppv_number_lbl = QtWidgets.QLabel(self.centralwidget)
        self.total_sppv_number_lbl.setStyleSheet("QLabel {\n"
                                                 "    color: #28A745;\n"
                                                 "}")
        self.total_sppv_number_lbl.setObjectName("total_sppv_number_lbl")
        self.horizontalLayout.addWidget(self.total_sppv_number_lbl)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.total_rdpv_number_lbl = QtWidgets.QLabel(self.centralwidget)
        self.total_rdpv_number_lbl.setStyleSheet("QLabel {\n"
                                                 "    color: #28A745;\n"
                                                 "}")
        self.total_rdpv_number_lbl.setObjectName("total_rdpv_number_lbl")
        self.horizontalLayout.addWidget(self.total_rdpv_number_lbl)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.update_rate_cbb = QtWidgets.QComboBox(self.centralwidget)
        self.update_rate_cbb.setEnabled(True)
        self.update_rate_cbb.setObjectName("update_rate_cbb")
        self.update_rate_cbb.addItem("")
        self.update_rate_cbb.addItem("")
        self.update_rate_cbb.addItem("")
        self.update_rate_cbb.addItem("")
        self.horizontalLayout.addWidget(self.update_rate_cbb)
        self.update_ctrl_btn = QtWidgets.QToolButton(self.centralwidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/sm-icons/start.png"),
                        QtGui.QIcon.Active, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/sm-icons/stop.png"),
                        QtGui.QIcon.Active, QtGui.QIcon.On)
        self.update_ctrl_btn.setIcon(icon2)
        self.update_ctrl_btn.setCheckable(True)
        self.update_ctrl_btn.setChecked(False)
        self.update_ctrl_btn.setAutoRaise(False)
        self.update_ctrl_btn.setObjectName("update_ctrl_btn")
        self.horizontalLayout.addWidget(self.update_ctrl_btn)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.expand_all_btn = QtWidgets.QToolButton(self.centralwidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/sm-icons/expand.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon3.addPixmap(QtGui.QPixmap(":/sm-icons/collapse.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.expand_all_btn.setIcon(icon3)
        self.expand_all_btn.setCheckable(True)
        self.expand_all_btn.setAutoRaise(True)
        self.expand_all_btn.setObjectName("expand_all_btn")
        self.horizontalLayout_2.addWidget(self.expand_all_btn)
        self.select_all_btn = QtWidgets.QToolButton(self.centralwidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/sm-icons/select-all.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.select_all_btn.setIcon(icon4)
        self.select_all_btn.setAutoRaise(True)
        self.select_all_btn.setObjectName("select_all_btn")
        self.horizontalLayout_2.addWidget(self.select_all_btn)
        self.invert_selection_btn = QtWidgets.QToolButton(self.centralwidget)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/sm-icons/invert-selection.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.invert_selection_btn.setIcon(icon5)
        self.invert_selection_btn.setAutoRaise(True)
        self.invert_selection_btn.setObjectName("invert_selection_btn")
        self.horizontalLayout_2.addWidget(self.invert_selection_btn)
        self.reset_set_status_btn = QtWidgets.QToolButton(self.centralwidget)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/sm-icons/clear.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reset_set_status_btn.setIcon(icon6)
        self.reset_set_status_btn.setAutoRaise(True)
        self.reset_set_status_btn.setObjectName("reset_set_status_btn")
        self.horizontalLayout_2.addWidget(self.reset_set_status_btn)
        self.delete_btn = QtWidgets.QToolButton(self.centralwidget)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/sm-icons/delete.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_btn.setIcon(icon7)
        self.delete_btn.setAutoRaise(True)
        self.delete_btn.setObjectName("delete_btn")
        self.horizontalLayout_2.addWidget(self.delete_btn)
        spacerItem1 = QtWidgets.QSpacerItem(900, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.namefilter_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(8)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.namefilter_lineEdit.sizePolicy().hasHeightForWidth())
        self.namefilter_lineEdit.setSizePolicy(sizePolicy)
        self.namefilter_lineEdit.setText("")
        self.namefilter_lineEdit.setObjectName("namefilter_lineEdit")
        self.horizontalLayout_2.addWidget(self.namefilter_lineEdit)
        self.total_show_number_lbl = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.total_show_number_lbl.sizePolicy().hasHeightForWidth())
        self.total_show_number_lbl.setSizePolicy(sizePolicy)
        self.total_show_number_lbl.setStyleSheet("QLabel {\n"
                                                 "    color: #28A745;\n"
                                                 "    font-weight: bold;\n"
                                                 "}")
        self.total_show_number_lbl.setAlignment(QtCore.Qt.AlignRight
                                                | QtCore.Qt.AlignTrailing
                                                | QtCore.Qt.AlignVCenter)
        self.total_show_number_lbl.setObjectName("total_show_number_lbl")
        self.horizontalLayout_2.addWidget(self.total_show_number_lbl)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1600, 31))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.toolBar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.toolBar.setAutoFillBackground(False)
        self.toolBar.setStyleSheet("QToolBar {\n"
                                   "    padding: 4px;\n"
                                   "    spacing: 4px;\n"
                                   "}\n"
                                   "\n"
                                   "QToolBar::handle {\n"
                                   "    image: url(handle.png);\n"
                                   "}QToolb")
        self.toolBar.setOrientation(QtCore.Qt.Horizontal)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_About = QtWidgets.QAction(MainWindow)
        self.action_About.setObjectName("action_About")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/sm-icons/exit.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionE_xit.setIcon(icon8)
        self.actionE_xit.setObjectName("actionE_xit")
        self.actionContents = QtWidgets.QAction(MainWindow)
        self.actionContents.setObjectName("actionContents")
        self.action_Save = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/sm-icons/save.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Save.setIcon(icon9)
        self.action_Save.setObjectName("action_Save")
        self.actionLoad_From_Snapshot = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/sm-icons/folder-open-snp.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoad_From_Snapshot.setIcon(icon10)
        self.actionLoad_From_Snapshot.setObjectName("actionLoad_From_Snapshot")
        self.actionPhysics_Fields = QtWidgets.QAction(MainWindow)
        self.actionPhysics_Fields.setCheckable(True)
        self.actionPhysics_Fields.setChecked(False)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/sm-icons/physics.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPhysics_Fields.setIcon(icon11)
        self.actionPhysics_Fields.setObjectName("actionPhysics_Fields")
        self.actionEngineering_Fields = QtWidgets.QAction(MainWindow)
        self.actionEngineering_Fields.setCheckable(True)
        self.actionEngineering_Fields.setChecked(True)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/sm-icons/engineering.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEngineering_Fields.setIcon(icon12)
        self.actionEngineering_Fields.setObjectName("actionEngineering_Fields")
        self.actionLoad_Lattice = QtWidgets.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/sm-icons/load_lattice.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoad_Lattice.setIcon(icon13)
        self.actionLoad_Lattice.setObjectName("actionLoad_Lattice")
        self.actionLoad_Settings = QtWidgets.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/sm-icons/open.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoad_Settings.setIcon(icon14)
        self.actionLoad_Settings.setObjectName("actionLoad_Settings")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/sm-icons/preferences.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPreferences.setIcon(icon15)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionAdd_Devices = QtWidgets.QAction(MainWindow)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/sm-icons/add.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd_Devices.setIcon(icon16)
        self.actionAdd_Devices.setObjectName("actionAdd_Devices")
        self.menu_Help.addAction(self.actionContents)
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.action_About)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.toolBar.addAction(self.actionLoad_Lattice)
        self.toolBar.addAction(self.actionAdd_Devices)
        self.toolBar.addAction(self.action_Save)
        self.toolBar.addAction(self.actionLoad_Settings)
        self.toolBar.addAction(self.actionLoad_From_Snapshot)
        self.toolBar.addAction(self.actionPhysics_Fields)
        self.toolBar.addAction(self.actionEngineering_Fields)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPreferences)
        self.toolBar.addAction(self.actionE_xit)

        self.retranslateUi(MainWindow)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.actionE_xit.triggered.connect(MainWindow.close)
        self.action_About.triggered.connect(MainWindow.onAbout)
        self.apply_btn.clicked.connect(MainWindow.on_apply_settings)
        self.actionLoad_From_Snapshot.triggered.connect(
            MainWindow.on_load_from_snp)
        self.action_Save.triggered.connect(MainWindow.on_save)
        self.actionPhysics_Fields.toggled['bool'].connect(
            MainWindow.on_toggle_phyfields)
        self.actionEngineering_Fields.toggled['bool'].connect(
            MainWindow.on_toggle_engfields)
        self.actionLoad_Lattice.triggered.connect(MainWindow.on_load_lattice)
        self.namefilter_lineEdit.editingFinished.connect(
            MainWindow.on_namefilter_changed)
        self.actionLoad_Settings.triggered.connect(MainWindow.on_load)
        self.treeView.clicked['QModelIndex'].connect(MainWindow.on_click_view)
        self.actionPreferences.triggered.connect(
            MainWindow.on_launch_preferences)
        self.reload_lattice_btn.clicked.connect(MainWindow.on_reload_lattice)
        self.update_ctrl_btn.toggled['bool'].connect(
            self.update_rate_cbb.setDisabled)
        self.update_rate_cbb.currentIndexChanged['int'].connect(
            MainWindow.on_update_rate)
        self.update_ctrl_btn.toggled['bool'].connect(
            MainWindow.on_toggle_update_btn)
        self.reset_set_status_btn.clicked.connect(
            MainWindow.on_reset_set_status)
        self.expand_all_btn.toggled['bool'].connect(
            MainWindow.on_expand_collapse_view)
        self.actionAdd_Devices.triggered.connect(MainWindow.on_add_devices)
        self.delete_btn.clicked.connect(MainWindow.on_remove_selected_settings)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.expand_all_btn, self.select_all_btn)
        MainWindow.setTabOrder(self.select_all_btn, self.invert_selection_btn)
        MainWindow.setTabOrder(self.invert_selection_btn,
                               self.reset_set_status_btn)
        MainWindow.setTabOrder(self.reset_set_status_btn,
                               self.namefilter_lineEdit)
        MainWindow.setTabOrder(self.namefilter_lineEdit, self.treeView)
        MainWindow.setTabOrder(self.treeView, self.reload_lattice_btn)
        MainWindow.setTabOrder(self.reload_lattice_btn, self.lv_view_btn)
        MainWindow.setTabOrder(self.lv_view_btn, self.update_rate_cbb)
        MainWindow.setTabOrder(self.update_rate_cbb, self.update_ctrl_btn)
        MainWindow.setTabOrder(self.update_ctrl_btn, self.apply_btn)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.apply_btn.setText(_translate("MainWindow", "Apply"))
        self.reload_lattice_btn.setToolTip(
            _translate("MainWindow", "Reload Lattice."))
        self.reload_lattice_btn.setText(_translate("MainWindow", "..."))
        self.lv_lbl.setText(_translate("MainWindow", "Loaded Lattice"))
        self.lv_view_btn.setToolTip(
            _translate("MainWindow", "See the details of loaded lattice."))
        self.lv_view_btn.setText(_translate("MainWindow", "..."))
        self.lv_mach_lbl.setToolTip(_translate("MainWindow", "Machine name."))
        self.lv_mach_lbl.setText(_translate("MainWindow", "machine"))
        self.lv_segm_lbl.setToolTip(_translate("MainWindow", "Segment name."))
        self.lv_segm_lbl.setText(_translate("MainWindow", "segment"))
        self.label.setText(_translate("MainWindow", "Total Elements"))
        self.total_elem_number_lbl.setText(_translate("MainWindow", "0"))
        self.label_2.setText(_translate("MainWindow", "Setpoint PVs"))
        self.total_sppv_number_lbl.setText(_translate("MainWindow", "0"))
        self.label_3.setText(_translate("MainWindow", "Readback PVs"))
        self.total_rdpv_number_lbl.setText(_translate("MainWindow", "0"))
        self.label_6.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Auto : Realtime update</p><p>1-5 : Update every 0.2 to 1 second</p></body></html>"
            ))
        self.label_6.setText(_translate("MainWindow", "Update Rate"))
        self.update_rate_cbb.setItemText(0, _translate("MainWindow", "Auto"))
        self.update_rate_cbb.setItemText(1, _translate("MainWindow", "0.5 Hz"))
        self.update_rate_cbb.setItemText(2, _translate("MainWindow", "1.0 Hz"))
        self.update_rate_cbb.setItemText(3, _translate("MainWindow", "2.0 Hz"))
        self.update_ctrl_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Start/stop updating values.</p></body></html>"
            ))
        self.update_ctrl_btn.setText(_translate("MainWindow", "..."))
        self.expand_all_btn.setToolTip(
            _translate("MainWindow", "Click to expand all."))
        self.expand_all_btn.setText(_translate("MainWindow", "Expand"))
        self.select_all_btn.setToolTip(_translate("MainWindow", "Select all."))
        self.select_all_btn.setText(_translate("MainWindow", "Select All"))
        self.invert_selection_btn.setToolTip(
            _translate("MainWindow", "Invert current selections."))
        self.invert_selection_btn.setText(
            _translate("MainWindow", "Invert Selection"))
        self.reset_set_status_btn.setToolTip(
            _translate("MainWindow", "Clear status."))
        self.reset_set_status_btn.setText(
            _translate("MainWindow", "Clear Status"))
        self.delete_btn.setToolTip(
            _translate("MainWindow", "Delete selected items."))
        self.delete_btn.setText(_translate("MainWindow", "..."))
        self.label_5.setText(_translate("MainWindow", "Search"))
        self.namefilter_lineEdit.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Input Unix style search pattern by \'key = pattern\', valid keys: \'device\', \'field\', \'setpoint\', \'live_readback\', \'live_setpoint\', \'pos\', \'type\', if not defined, \'device\' is used, press Enter to activate the filter.</p><p>1. *: match all device names, which is equivalent of device=*;</p><p>2. *LEBT*: match device name which has string \'LEBT\';</p><p>3. type=\'CAV\': match all devices of type \'CAV\';</p><p>4. ? is to match one char or digit, pure \'\' is to interpret as *.<br/></p></body></html>"
            ))
        self.total_show_number_lbl.setToolTip(
            _translate("MainWindow", "Total filtered items."))
        self.total_show_number_lbl.setText(_translate("MainWindow", "0"))
        self.label_4.setText(_translate("MainWindow", "items"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action_About.setText(_translate("MainWindow", "&About"))
        self.action_About.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))
        self.actionE_xit.setText(_translate("MainWindow", "E&xit"))
        self.actionE_xit.setToolTip(
            _translate("MainWindow", "Exit application."))
        self.actionE_xit.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionContents.setText(_translate("MainWindow", "Contents"))
        self.actionContents.setShortcut(_translate("MainWindow", "F1"))
        self.action_Save.setText(_translate("MainWindow", "&Save"))
        self.action_Save.setIconText(_translate("MainWindow", "Save Settings"))
        self.action_Save.setToolTip(
            _translate("MainWindow", "Save settings into a file."))
        self.action_Save.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionLoad_From_Snapshot.setText(
            _translate("MainWindow", "Load From Snapshot"))
        self.actionLoad_From_Snapshot.setIconText(
            _translate("MainWindow", "Load Snapshot"))
        self.actionLoad_From_Snapshot.setToolTip(
            _translate("MainWindow",
                       "Load settings from a snapshot (.snp) file."))
        self.actionLoad_From_Snapshot.setShortcut(
            _translate("MainWindow", "Ctrl+L"))
        self.actionPhysics_Fields.setText(_translate("MainWindow", "Physics"))
        self.actionPhysics_Fields.setIconText(
            _translate("MainWindow", "Physics Fields"))
        self.actionPhysics_Fields.setToolTip(
            _translate("MainWindow", "Show physics fields."))
        self.actionPhysics_Fields.setShortcut(
            _translate("MainWindow", "Ctrl+Shift+P"))
        self.actionEngineering_Fields.setText(
            _translate("MainWindow", "Engineering"))
        self.actionEngineering_Fields.setIconText(
            _translate("MainWindow", "Engineering Fields"))
        self.actionEngineering_Fields.setToolTip(
            _translate("MainWindow", "Show engineering fields."))
        self.actionEngineering_Fields.setShortcut(
            _translate("MainWindow", "Ctrl+Shift+E"))
        self.actionLoad_Lattice.setText(
            _translate("MainWindow", "Load Lattice"))
        self.actionLoad_Lattice.setIconText(
            _translate("MainWindow", "Load Lattice"))
        self.actionLoad_Lattice.setToolTip(
            _translate("MainWindow", "Load Lattice."))
        self.actionLoad_Lattice.setShortcut(
            _translate("MainWindow", "Ctrl+Shift+L"))
        self.actionLoad_Settings.setText(
            _translate("MainWindow", "Load Settings"))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences"))
        self.actionPreferences.setToolTip(
            _translate("MainWindow", "Preferences."))
        self.actionAdd_Devices.setText(_translate("MainWindow", "Add Devices"))
        self.actionAdd_Devices.setToolTip(
            _translate("MainWindow", "Add Devices."))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
