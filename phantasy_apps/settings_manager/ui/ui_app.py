# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_app.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 975)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.gridLayout.setObjectName("gridLayout")
        self.expand_all_btn = QtWidgets.QToolButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/sm-icons/expand.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/sm-icons/collapse.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.expand_all_btn.setIcon(icon)
        self.expand_all_btn.setIconSize(QtCore.QSize(24, 24))
        self.expand_all_btn.setCheckable(True)
        self.expand_all_btn.setAutoRaise(True)
        self.expand_all_btn.setObjectName("expand_all_btn")
        self.gridLayout.addWidget(self.expand_all_btn, 0, 0, 1, 1)
        self.select_all_btn = QtWidgets.QToolButton(self.centralwidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/sm-icons/select-all.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.select_all_btn.setIcon(icon1)
        self.select_all_btn.setIconSize(QtCore.QSize(24, 24))
        self.select_all_btn.setAutoRaise(True)
        self.select_all_btn.setObjectName("select_all_btn")
        self.gridLayout.addWidget(self.select_all_btn, 0, 1, 1, 1)
        self.invert_selection_btn = QtWidgets.QToolButton(self.centralwidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/sm-icons/invert-selection.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.invert_selection_btn.setIcon(icon2)
        self.invert_selection_btn.setIconSize(QtCore.QSize(24, 24))
        self.invert_selection_btn.setAutoRaise(True)
        self.invert_selection_btn.setObjectName("invert_selection_btn")
        self.gridLayout.addWidget(self.invert_selection_btn, 0, 2, 1, 1)
        self.reset_set_status_btn = QtWidgets.QToolButton(self.centralwidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/sm-icons/clear.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reset_set_status_btn.setIcon(icon3)
        self.reset_set_status_btn.setIconSize(QtCore.QSize(24, 24))
        self.reset_set_status_btn.setAutoRaise(True)
        self.reset_set_status_btn.setObjectName("reset_set_status_btn")
        self.gridLayout.addWidget(self.reset_set_status_btn, 0, 3, 1, 1)
        self.delete_btn = QtWidgets.QToolButton(self.centralwidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/sm-icons/delete.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_btn.setIcon(icon4)
        self.delete_btn.setIconSize(QtCore.QSize(24, 24))
        self.delete_btn.setAutoRaise(True)
        self.delete_btn.setObjectName("delete_btn")
        self.gridLayout.addWidget(self.delete_btn, 0, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(300, 30,
                                           QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 5, 1, 1)
        self.filter_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.filter_lineEdit.sizePolicy().hasHeightForWidth())
        self.filter_lineEdit.setSizePolicy(sizePolicy)
        self.filter_lineEdit.setText("")
        self.filter_lineEdit.setObjectName("filter_lineEdit")
        self.gridLayout.addWidget(self.filter_lineEdit, 0, 6, 1, 2)
        self.filter_btn = QtWidgets.QToolButton(self.centralwidget)
        self.filter_btn.setStyleSheet(
            "QToolButton {\n"
            "    border-image: url(:/sm-icons/search.svg);\n"
            "    width: 24px;\n"
            "    height: 24px;\n"
            "    background-repeat: no-repeat;\n"
            "}\n"
            "QToolButton::hover {\n"
            "    border-image: url(:/sm-icons/search-on.svg);\n"
            "    background-repeat: no-repeat;\n"
            "}\n"
            "QToolButton::checked {\n"
            "    border-image: url(:/sm-icons/search-on.svg);\n"
            "    background-repeat: no-repeat;\n"
            "}\n"
            "QToolButton::unchecked {\n"
            "    border-image: url(:/sm-icons/search.svg);\n"
            "    background-repeat: no-repeat;\n"
            "}")
        self.filter_btn.setText("")
        self.filter_btn.setCheckable(True)
        self.filter_btn.setObjectName("filter_btn")
        self.gridLayout.addWidget(self.filter_btn, 0, 8, 1, 1)
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/sm-icons/help.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton.setIcon(icon5)
        self.toolButton.setIconSize(QtCore.QSize(24, 24))
        self.toolButton.setAutoRaise(True)
        self.toolButton.setObjectName("toolButton")
        self.gridLayout.addWidget(self.toolButton, 0, 9, 1, 1)
        self.total_show_number_lbl = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
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
        self.gridLayout.addWidget(self.total_show_number_lbl, 0, 10, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 11, 1, 1)
        self.grow_fontsize_btn = QtWidgets.QToolButton(self.centralwidget)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/sm-icons/increase-font.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.grow_fontsize_btn.setIcon(icon6)
        self.grow_fontsize_btn.setAutoRaise(True)
        self.grow_fontsize_btn.setObjectName("grow_fontsize_btn")
        self.gridLayout.addWidget(self.grow_fontsize_btn, 1, 0, 1, 1)
        self.shrink_fontsize_btn = QtWidgets.QToolButton(self.centralwidget)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/sm-icons/decrease-font.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.shrink_fontsize_btn.setIcon(icon7)
        self.shrink_fontsize_btn.setAutoRaise(True)
        self.shrink_fontsize_btn.setObjectName("shrink_fontsize_btn")
        self.gridLayout.addWidget(self.shrink_fontsize_btn, 1, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setAlignment(QtCore.Qt.AlignRight
                                  | QtCore.Qt.AlignTrailing
                                  | QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 1, 7, 1, 3)
        self.show_all_selected_btn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.show_all_selected_btn.sizePolicy().hasHeightForWidth())
        self.show_all_selected_btn.setSizePolicy(sizePolicy)
        self.show_all_selected_btn.setCheckable(True)
        self.show_all_selected_btn.setObjectName("show_all_selected_btn")
        self.gridLayout.addWidget(self.show_all_selected_btn, 1, 10, 1, 2)
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.treeView.sizePolicy().hasHeightForWidth())
        self.treeView.setSizePolicy(sizePolicy)
        self.treeView.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeView.setObjectName("treeView")
        self.gridLayout.addWidget(self.treeView, 2, 0, 1, 12)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.reload_lattice_btn = QtWidgets.QToolButton(self.centralwidget)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/sm-icons/reload.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reload_lattice_btn.setIcon(icon8)
        self.reload_lattice_btn.setIconSize(QtCore.QSize(24, 24))
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
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/sm-icons/view-details.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.lv_view_btn.setIcon(icon9)
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
        spacerItem1 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
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
        self.update_rate_cbb.addItem("")
        self.horizontalLayout.addWidget(self.update_rate_cbb)
        self.update_ctrl_btn = QtWidgets.QToolButton(self.centralwidget)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/sm-icons/start.png"),
                         QtGui.QIcon.Active, QtGui.QIcon.Off)
        icon10.addPixmap(QtGui.QPixmap(":/sm-icons/stop.png"),
                         QtGui.QIcon.Active, QtGui.QIcon.On)
        self.update_ctrl_btn.setIcon(icon10)
        self.update_ctrl_btn.setIconSize(QtCore.QSize(24, 24))
        self.update_ctrl_btn.setCheckable(True)
        self.update_ctrl_btn.setChecked(False)
        self.update_ctrl_btn.setAutoRaise(True)
        self.update_ctrl_btn.setObjectName("update_ctrl_btn")
        self.horizontalLayout.addWidget(self.update_ctrl_btn)
        self.single_update_btn = QtWidgets.QToolButton(self.centralwidget)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/sm-icons/single.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.single_update_btn.setIcon(icon11)
        self.single_update_btn.setIconSize(QtCore.QSize(24, 24))
        self.single_update_btn.setAutoRaise(True)
        self.single_update_btn.setObjectName("single_update_btn")
        self.horizontalLayout.addWidget(self.single_update_btn)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, 0, 0, -1)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout_3.setSpacing(1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.apply_btn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.apply_btn.sizePolicy().hasHeightForWidth())
        self.apply_btn.setSizePolicy(sizePolicy)
        self.apply_btn.setFlat(False)
        self.apply_btn.setObjectName("apply_btn")
        self.horizontalLayout_3.addWidget(self.apply_btn)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_3.addWidget(self.label_8)
        self.scaling_factor_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scaling_factor_lineEdit.sizePolicy().hasHeightForWidth())
        self.scaling_factor_lineEdit.setSizePolicy(sizePolicy)
        self.scaling_factor_lineEdit.setObjectName("scaling_factor_lineEdit")
        self.horizontalLayout_3.addWidget(self.scaling_factor_lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.apply_pb = QtWidgets.QProgressBar(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.apply_pb.sizePolicy().hasHeightForWidth())
        self.apply_pb.setSizePolicy(sizePolicy)
        self.apply_pb.setMinimumSize(QtCore.QSize(0, 10))
        self.apply_pb.setMaximumSize(QtCore.QSize(16777215, 10))
        self.apply_pb.setProperty("value", 0)
        self.apply_pb.setFormat("")
        self.apply_pb.setObjectName("apply_pb")
        self.verticalLayout.addWidget(self.apply_pb)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 12)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.total_elem_number_lbl = QtWidgets.QLabel(self.centralwidget)
        self.total_elem_number_lbl.setStyleSheet("QLabel {\n"
                                                 "    color: #28A745;\n"
                                                 "}")
        self.total_elem_number_lbl.setObjectName("total_elem_number_lbl")
        self.horizontalLayout_2.addWidget(self.total_elem_number_lbl)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.total_sppv_number_lbl = QtWidgets.QLabel(self.centralwidget)
        self.total_sppv_number_lbl.setStyleSheet("QLabel {\n"
                                                 "    color: #28A745;\n"
                                                 "}")
        self.total_sppv_number_lbl.setObjectName("total_sppv_number_lbl")
        self.horizontalLayout_2.addWidget(self.total_sppv_number_lbl)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.total_rdpv_number_lbl = QtWidgets.QLabel(self.centralwidget)
        self.total_rdpv_number_lbl.setStyleSheet("QLabel {\n"
                                                 "    color: #28A745;\n"
                                                 "}")
        self.total_rdpv_number_lbl.setObjectName("total_rdpv_number_lbl")
        self.horizontalLayout_2.addWidget(self.total_rdpv_number_lbl)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_2.addWidget(self.label_9)
        self.ndigit_sbox = QtWidgets.QSpinBox(self.centralwidget)
        self.ndigit_sbox.setMaximum(20)
        self.ndigit_sbox.setProperty("value", 3)
        self.ndigit_sbox.setObjectName("ndigit_sbox")
        self.horizontalLayout_2.addWidget(self.ndigit_sbox)
        self.init_settings_chkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.init_settings_chkbox.setObjectName("init_settings_chkbox")
        self.horizontalLayout_2.addWidget(self.init_settings_chkbox)
        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 0, 1, 12)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1300, 30))
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
        self.toolBar.setAllowedAreas(QtCore.Qt.BottomToolBarArea
                                     | QtCore.Qt.TopToolBarArea)
        self.toolBar.setOrientation(QtCore.Qt.Horizontal)
        self.toolBar.setIconSize(QtCore.QSize(36, 36))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.snp_dock = QtWidgets.QDockWidget(MainWindow)
        self.snp_dock.setFloating(False)
        self.snp_dock.setFeatures(
            QtWidgets.QDockWidget.DockWidgetFloatable
            | QtWidgets.QDockWidget.DockWidgetMovable
            | QtWidgets.QDockWidget.DockWidgetVerticalTitleBar)
        self.snp_dock.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea
                                      | QtCore.Qt.TopDockWidgetArea)
        self.snp_dock.setObjectName("snp_dock")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout_3.setContentsMargins(6, 6, 6, 6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.snp_treeView = QtWidgets.QTreeView(self.dockWidgetContents)
        self.snp_treeView.setDragDropMode(
            QtWidgets.QAbstractItemView.NoDragDrop)
        self.snp_treeView.setIndentation(10)
        self.snp_treeView.setRootIsDecorated(True)
        self.snp_treeView.setSortingEnabled(False)
        self.snp_treeView.setAnimated(True)
        self.snp_treeView.setObjectName("snp_treeView")
        self.gridLayout_3.addWidget(self.snp_treeView, 3, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_5 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.wdir_lineEdit = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.wdir_lineEdit.setReadOnly(True)
        self.wdir_lineEdit.setObjectName("wdir_lineEdit")
        self.horizontalLayout_4.addWidget(self.wdir_lineEdit)
        self.label_10 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_4.addWidget(self.label_10)
        self.total_snp_lbl = QtWidgets.QLabel(self.dockWidgetContents)
        self.total_snp_lbl.setStyleSheet("QLabel {\n"
                                         "    font-weight: bold;\n"
                                         "    color: rgb(0, 0, 255);\n"
                                         "}")
        self.total_snp_lbl.setObjectName("total_snp_lbl")
        self.horizontalLayout_4.addWidget(self.total_snp_lbl)
        self.gridLayout_3.addLayout(self.horizontalLayout_4, 2, 0, 1, 1)
        self.snp_dock.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.snp_dock)
        self.action_About = QtWidgets.QAction(MainWindow)
        self.action_About.setObjectName("action_About")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/sm-icons/exit.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionE_xit.setIcon(icon12)
        self.actionE_xit.setObjectName("actionE_xit")
        self.actionContents = QtWidgets.QAction(MainWindow)
        self.actionContents.setObjectName("actionContents")
        self.action_Save = QtWidgets.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/sm-icons/save.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Save.setIcon(icon13)
        self.action_Save.setObjectName("action_Save")
        self.actionLoad_From_Snapshot = QtWidgets.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/sm-icons/folder-open-snp.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoad_From_Snapshot.setIcon(icon14)
        self.actionLoad_From_Snapshot.setObjectName("actionLoad_From_Snapshot")
        self.actionPhysics_Fields = QtWidgets.QAction(MainWindow)
        self.actionPhysics_Fields.setCheckable(True)
        self.actionPhysics_Fields.setChecked(False)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/sm-icons/physics.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPhysics_Fields.setIcon(icon15)
        self.actionPhysics_Fields.setObjectName("actionPhysics_Fields")
        self.actionEngineering_Fields = QtWidgets.QAction(MainWindow)
        self.actionEngineering_Fields.setCheckable(True)
        self.actionEngineering_Fields.setChecked(True)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/sm-icons/engineering.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEngineering_Fields.setIcon(icon16)
        self.actionEngineering_Fields.setObjectName("actionEngineering_Fields")
        self.actionLoad_Lattice = QtWidgets.QAction(MainWindow)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(":/sm-icons/load_lattice.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoad_Lattice.setIcon(icon17)
        self.actionLoad_Lattice.setObjectName("actionLoad_Lattice")
        self.actionLoad_Settings = QtWidgets.QAction(MainWindow)
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap(":/sm-icons/open.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoad_Settings.setIcon(icon18)
        self.actionLoad_Settings.setObjectName("actionLoad_Settings")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        icon19 = QtGui.QIcon()
        icon19.addPixmap(QtGui.QPixmap(":/sm-icons/preferences.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPreferences.setIcon(icon19)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionAdd_Devices = QtWidgets.QAction(MainWindow)
        icon20 = QtGui.QIcon()
        icon20.addPixmap(QtGui.QPixmap(":/sm-icons/add.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd_Devices.setIcon(icon20)
        self.actionAdd_Devices.setObjectName("actionAdd_Devices")
        self.actionTake_Snapshot = QtWidgets.QAction(MainWindow)
        icon21 = QtGui.QIcon()
        icon21.addPixmap(QtGui.QPixmap(":/sm-icons/snapshot.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTake_Snapshot.setIcon(icon21)
        self.actionTake_Snapshot.setObjectName("actionTake_Snapshot")
        self.menu_File.addAction(self.actionLoad_From_Snapshot)
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
        self.toolBar.addAction(self.actionTake_Snapshot)
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
        self.filter_lineEdit.editingFinished.connect(
            MainWindow.on_filter_changed)
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
        self.update_ctrl_btn.toggled['bool'].connect(
            self.single_update_btn.setDisabled)
        self.single_update_btn.clicked.connect(MainWindow.on_single_update)
        self.treeView.pressed['QModelIndex'].connect(
            MainWindow.on_pressed_view)
        self.show_all_selected_btn.toggled['bool'].connect(
            MainWindow.on_toggle_all_selected)
        self.actionTake_Snapshot.triggered.connect(
            MainWindow.on_take_settings_snapshot)
        self.scaling_factor_lineEdit.returnPressed.connect(
            MainWindow.on_input_scaling_factor)
        self.init_settings_chkbox.toggled['bool'].connect(
            MainWindow.on_toggle_init_lattice_settings)
        self.ndigit_sbox.valueChanged['int'].connect(
            MainWindow.on_ndigit_valueChanged)
        self.toolButton.clicked.connect(MainWindow.on_show_query_tips)
        self.filter_btn.toggled['bool'].connect(self.filter_lineEdit.setFocus)
        self.scaling_factor_lineEdit.textChanged['QString'].connect(
            MainWindow.on_scaling_factor_changed)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.expand_all_btn, self.select_all_btn)
        MainWindow.setTabOrder(self.select_all_btn, self.invert_selection_btn)
        MainWindow.setTabOrder(self.invert_selection_btn,
                               self.reset_set_status_btn)
        MainWindow.setTabOrder(self.reset_set_status_btn, self.filter_lineEdit)
        MainWindow.setTabOrder(self.filter_lineEdit, self.treeView)
        MainWindow.setTabOrder(self.treeView, self.reload_lattice_btn)
        MainWindow.setTabOrder(self.reload_lattice_btn, self.lv_view_btn)
        MainWindow.setTabOrder(self.lv_view_btn, self.update_rate_cbb)
        MainWindow.setTabOrder(self.update_rate_cbb, self.update_ctrl_btn)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
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
        self.filter_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Search (Ctrl + F).</p></body></html>"))
        self.filter_btn.setShortcut(_translate("MainWindow", "Ctrl+F"))
        self.toolButton.setText(_translate("MainWindow", "?"))
        self.total_show_number_lbl.setToolTip(
            _translate("MainWindow", "Total filtered items."))
        self.total_show_number_lbl.setText(_translate("MainWindow", "0"))
        self.label_4.setText(_translate("MainWindow", "items"))
        self.grow_fontsize_btn.setToolTip(
            _translate(
                "MainWindow",
                "Grow font size by 1pt (Ctrl + plus, reset with Ctrl + 0)."))
        self.grow_fontsize_btn.setText(_translate("MainWindow", "..."))
        self.shrink_fontsize_btn.setToolTip(
            _translate(
                "MainWindow",
                "Shrink font size by 1pt (Ctrl + minus, reset with Ctrl + 0).")
        )
        self.shrink_fontsize_btn.setText(_translate("MainWindow", "..."))
        self.label_7.setText(_translate("MainWindow", "Filter Shortcuts"))
        self.show_all_selected_btn.setToolTip(
            _translate("MainWindow", "Show all selected items."))
        self.show_all_selected_btn.setText(
            _translate("MainWindow", "All Selected"))
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
        self.label_6.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Auto : Realtime update</p><p>1-5 : Update every 0.2 to 1 second</p></body></html>"
            ))
        self.label_6.setText(_translate("MainWindow", "Update Rate"))
        self.update_rate_cbb.setItemText(0, _translate("MainWindow", "1.0 Hz"))
        self.update_rate_cbb.setItemText(1, _translate("MainWindow", "0.5 Hz"))
        self.update_rate_cbb.setItemText(2, _translate("MainWindow", "2.0 Hz"))
        self.update_rate_cbb.setItemText(3, _translate("MainWindow", "0.2 Hz"))
        self.update_rate_cbb.setItemText(4, _translate("MainWindow", "0.1 Hz"))
        self.update_ctrl_btn.setToolTip(
            _translate("MainWindow", "Start/stop updating values."))
        self.update_ctrl_btn.setText(_translate("MainWindow", "..."))
        self.single_update_btn.setToolTip(
            _translate("MainWindow", "Update for one time."))
        self.single_update_btn.setText(_translate("MainWindow", "..."))
        self.apply_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Only apply the settings of checked items after scaling by the defined scaling factor.</p></body></html>"
            ))
        self.apply_btn.setText(_translate("MainWindow", "Apply"))
        self.label_8.setText(
            _translate("MainWindow",
                       "<html><head/><body><p>×</p></body></html>"))
        self.scaling_factor_lineEdit.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Scaling factor, input a number e.g. 0.8, or an expression, e.g. 12 / 18, then press Enter.</p></body></html>"
            ))
        self.scaling_factor_lineEdit.setText(_translate("MainWindow", "1.0"))
        self.label.setText(_translate("MainWindow", "Total Elements"))
        self.total_elem_number_lbl.setText(_translate("MainWindow", "0"))
        self.label_2.setText(_translate("MainWindow", "Setpoint PVs"))
        self.total_sppv_number_lbl.setText(_translate("MainWindow", "0"))
        self.label_3.setText(_translate("MainWindow", "Readback PVs"))
        self.total_rdpv_number_lbl.setText(_translate("MainWindow", "0"))
        self.label_9.setText(_translate("MainWindow", "Precision number"))
        self.init_settings_chkbox.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Initialize device settings with the whole loaded lattice.</p></body></html>"
            ))
        self.init_settings_chkbox.setText(
            _translate("MainWindow", "Initialize with loaded lattice"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.snp_dock.setWindowTitle(_translate("MainWindow", "Snapshots"))
        self.label_5.setText(_translate("MainWindow", "Working Directory"))
        self.label_10.setText(_translate("MainWindow", "Total"))
        self.total_snp_lbl.setText(
            _translate("MainWindow",
                       "<html><head/><body><p>0</p></body></html>"))
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
            _translate("MainWindow", "Load lattice."))
        self.actionLoad_Lattice.setShortcut(
            _translate("MainWindow", "Ctrl+Shift+L"))
        self.actionLoad_Settings.setText(
            _translate("MainWindow", "Load Settings"))
        self.actionLoad_Settings.setToolTip(
            _translate("MainWindow",
                       "Load settings from a file, or drag and drop in."))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences"))
        self.actionPreferences.setToolTip(
            _translate("MainWindow", "Preferences."))
        self.actionAdd_Devices.setText(_translate("MainWindow", "Add Devices"))
        self.actionAdd_Devices.setToolTip(
            _translate("MainWindow", "Add more devices."))
        self.actionTake_Snapshot.setText(
            _translate("MainWindow", "Take Snapshot"))
        self.actionTake_Snapshot.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Record current device settings, make sure fetch all live settings prior to this action.</p></body></html>"
            ))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
