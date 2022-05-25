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
        MainWindow.resize(2045, 1434)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/sm-icons/logo.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QProgressBar {\n"
                                 "    border: 1px solid gray;\n"
                                 "    border-radius: 1px;\n"
                                 "    text-align: center;\n"
                                 "}\n"
                                 "\n"
                                 "QProgressBar::chunk {\n"
                                 "    background-color: #05B8CC;\n"
                                 "    width: 10px;\n"
                                 "    margin: 0.5px;\n"
                                 "}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.settingsView = QtWidgets.QTreeView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.settingsView.sizePolicy().hasHeightForWidth())
        self.settingsView.setSizePolicy(sizePolicy)
        self.settingsView.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        self.settingsView.setUniformRowHeights(True)
        self.settingsView.setObjectName("settingsView")
        self.gridLayout.addWidget(self.settingsView, 3, 1, 1, 16)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.grow_fontsize_btn = QtWidgets.QToolButton(self.centralwidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/sm-icons/increase-font.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.grow_fontsize_btn.setIcon(icon1)
        self.grow_fontsize_btn.setIconSize(QtCore.QSize(30, 30))
        self.grow_fontsize_btn.setAutoRaise(True)
        self.grow_fontsize_btn.setObjectName("grow_fontsize_btn")
        self.horizontalLayout_9.addWidget(self.grow_fontsize_btn)
        self.shrink_fontsize_btn = QtWidgets.QToolButton(self.centralwidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/sm-icons/decrease-font.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.shrink_fontsize_btn.setIcon(icon2)
        self.shrink_fontsize_btn.setIconSize(QtCore.QSize(30, 30))
        self.shrink_fontsize_btn.setAutoRaise(True)
        self.shrink_fontsize_btn.setObjectName("shrink_fontsize_btn")
        self.horizontalLayout_9.addWidget(self.shrink_fontsize_btn)
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/sm-icons/resize-horizontal.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton.setIcon(icon3)
        self.toolButton.setIconSize(QtCore.QSize(30, 30))
        self.toolButton.setAutoRaise(True)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_9.addWidget(self.toolButton)
        self.delete_btn = QtWidgets.QToolButton(self.centralwidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/sm-icons/delete.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_btn.setIcon(icon4)
        self.delete_btn.setIconSize(QtCore.QSize(30, 30))
        self.delete_btn.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.delete_btn.setAutoRaise(True)
        self.delete_btn.setObjectName("delete_btn")
        self.horizontalLayout_9.addWidget(self.delete_btn)
        spacerItem = QtWidgets.QSpacerItem(600, 30,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem)
        self.filter_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.filter_lineEdit.sizePolicy().hasHeightForWidth())
        self.filter_lineEdit.setSizePolicy(sizePolicy)
        self.filter_lineEdit.setText("")
        self.filter_lineEdit.setObjectName("filter_lineEdit")
        self.horizontalLayout_9.addWidget(self.filter_lineEdit)
        self.filters_hbox = QtWidgets.QHBoxLayout()
        self.filters_hbox.setObjectName("filters_hbox")
        self.horizontalLayout_9.addLayout(self.filters_hbox)
        self.filter_btn = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.filter_btn.sizePolicy().hasHeightForWidth())
        self.filter_btn.setSizePolicy(sizePolicy)
        self.filter_btn.setStyleSheet(
            "QToolButton {\n"
            "    border-image: url(:/sm-icons/search.svg);\n"
            "    width: 24px;\n"
            "    height: 24px;\n"
            "    background-repeat: no-repeat;\n"
            "}\n"
            "QToolButton::hover {\n"
            "    border-image: url(:/sm-icons/search-hover.svg);\n"
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
        self.filter_btn.setIconSize(QtCore.QSize(30, 30))
        self.filter_btn.setCheckable(True)
        self.filter_btn.setObjectName("filter_btn")
        self.horizontalLayout_9.addWidget(self.filter_btn)
        self.filter_tip_btn = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.filter_tip_btn.sizePolicy().hasHeightForWidth())
        self.filter_tip_btn.setSizePolicy(sizePolicy)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/sm-icons/help.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.filter_tip_btn.setIcon(icon5)
        self.filter_tip_btn.setIconSize(QtCore.QSize(30, 30))
        self.filter_tip_btn.setAutoRaise(True)
        self.filter_tip_btn.setObjectName("filter_tip_btn")
        self.horizontalLayout_9.addWidget(self.filter_tip_btn)
        self.total_show_number_lbl = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.total_show_number_lbl.sizePolicy().hasHeightForWidth())
        self.total_show_number_lbl.setSizePolicy(sizePolicy)
        self.total_show_number_lbl.setMinimumSize(QtCore.QSize(80, 0))
        self.total_show_number_lbl.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setFamily("Monospace")
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.total_show_number_lbl.setFont(font)
        self.total_show_number_lbl.setStyleSheet(
            "QLabel {\n"
            "    font: bold 1.5em;\n"
            "    color: rgb(0, 170, 127);\n"
            "    padding: 1px 10px 0px 10px;\n"
            "}")
        self.total_show_number_lbl.setAlignment(QtCore.Qt.AlignRight
                                                | QtCore.Qt.AlignTrailing
                                                | QtCore.Qt.AlignVCenter)
        self.total_show_number_lbl.setObjectName("total_show_number_lbl")
        self.horizontalLayout_9.addWidget(self.total_show_number_lbl)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setAlignment(QtCore.Qt.AlignRight
                                  | QtCore.Qt.AlignTrailing
                                  | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_9.addWidget(self.label_4)
        self.gridLayout.addLayout(self.horizontalLayout_9, 0, 1, 1, 16)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.show_sts_btn = QtWidgets.QToolButton(self.centralwidget)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/sm-icons/right-arrow.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon6.addPixmap(QtGui.QPixmap(":/sm-icons/left-arrow.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.show_sts_btn.setIcon(icon6)
        self.show_sts_btn.setIconSize(QtCore.QSize(24, 24))
        self.show_sts_btn.setCheckable(True)
        self.show_sts_btn.setChecked(True)
        self.show_sts_btn.setAutoRaise(True)
        self.show_sts_btn.setObjectName("show_sts_btn")
        self.horizontalLayout_2.addWidget(self.show_sts_btn)
        self.total_elem_number_title_lbl = QtWidgets.QLabel(self.centralwidget)
        self.total_elem_number_title_lbl.setObjectName(
            "total_elem_number_title_lbl")
        self.horizontalLayout_2.addWidget(self.total_elem_number_title_lbl)
        self.total_elem_number_lbl = QtWidgets.QLabel(self.centralwidget)
        self.total_elem_number_lbl.setStyleSheet(
            "QLabel {\n"
            "    font-family: monospace;\n"
            "    color: #28A745;\n"
            "}")
        self.total_elem_number_lbl.setObjectName("total_elem_number_lbl")
        self.horizontalLayout_2.addWidget(self.total_elem_number_lbl)
        self.total_field_number_title_lbl = QtWidgets.QLabel(
            self.centralwidget)
        self.total_field_number_title_lbl.setObjectName(
            "total_field_number_title_lbl")
        self.horizontalLayout_2.addWidget(self.total_field_number_title_lbl)
        self.total_field_number_lbl = QtWidgets.QLabel(self.centralwidget)
        self.total_field_number_lbl.setStyleSheet(
            "QLabel {\n"
            "    font-family: monospace;\n"
            "    color: #28A745;\n"
            "}")
        self.total_field_number_lbl.setObjectName("total_field_number_lbl")
        self.horizontalLayout_2.addWidget(self.total_field_number_lbl)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.snp_ms_chkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.snp_ms_chkbox.setObjectName("snp_ms_chkbox")
        self.horizontalLayout_2.addWidget(self.snp_ms_chkbox)
        self.wysiwyc_chkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.wysiwyc_chkbox.setObjectName("wysiwyc_chkbox")
        self.horizontalLayout_2.addWidget(self.wysiwyc_chkbox)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout_2.addWidget(self.line_4)
        self.auto_ndigit_chkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.auto_ndigit_chkbox.setEnabled(True)
        self.auto_ndigit_chkbox.setObjectName("auto_ndigit_chkbox")
        self.horizontalLayout_2.addWidget(self.auto_ndigit_chkbox)
        self.ndigit_lbl = QtWidgets.QLabel(self.centralwidget)
        self.ndigit_lbl.setObjectName("ndigit_lbl")
        self.horizontalLayout_2.addWidget(self.ndigit_lbl)
        self.ndigit_sbox = QtWidgets.QSpinBox(self.centralwidget)
        self.ndigit_sbox.setMaximum(20)
        self.ndigit_sbox.setProperty("value", 3)
        self.ndigit_sbox.setObjectName("ndigit_sbox")
        self.horizontalLayout_2.addWidget(self.ndigit_sbox)
        self.show_init_settings_btn = QtWidgets.QToolButton(self.centralwidget)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/sm-icons/down-arrow.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon7.addPixmap(QtGui.QPixmap(":/sm-icons/up-arrow.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.show_init_settings_btn.setIcon(icon7)
        self.show_init_settings_btn.setIconSize(QtCore.QSize(24, 24))
        self.show_init_settings_btn.setCheckable(True)
        self.show_init_settings_btn.setChecked(True)
        self.show_init_settings_btn.setAutoRaise(True)
        self.show_init_settings_btn.setObjectName("show_init_settings_btn")
        self.horizontalLayout_2.addWidget(self.show_init_settings_btn)
        self.gridLayout.addLayout(self.horizontalLayout_2, 5, 1, 1, 16)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.select_all_btn = QtWidgets.QToolButton(self.centralwidget)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/sm-icons/select-all.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.select_all_btn.setIcon(icon8)
        self.select_all_btn.setIconSize(QtCore.QSize(30, 30))
        self.select_all_btn.setToolButtonStyle(
            QtCore.Qt.ToolButtonTextBesideIcon)
        self.select_all_btn.setAutoRaise(True)
        self.select_all_btn.setObjectName("select_all_btn")
        self.horizontalLayout_12.addWidget(self.select_all_btn)
        self.deselect_all_btn = QtWidgets.QToolButton(self.centralwidget)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/sm-icons/uncheck.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deselect_all_btn.setIcon(icon9)
        self.deselect_all_btn.setIconSize(QtCore.QSize(30, 30))
        self.deselect_all_btn.setToolButtonStyle(
            QtCore.Qt.ToolButtonTextBesideIcon)
        self.deselect_all_btn.setAutoRaise(True)
        self.deselect_all_btn.setObjectName("deselect_all_btn")
        self.horizontalLayout_12.addWidget(self.deselect_all_btn)
        self.invert_selection_btn = QtWidgets.QToolButton(self.centralwidget)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/sm-icons/invert-selection.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.invert_selection_btn.setIcon(icon10)
        self.invert_selection_btn.setIconSize(QtCore.QSize(30, 30))
        self.invert_selection_btn.setToolButtonStyle(
            QtCore.Qt.ToolButtonTextBesideIcon)
        self.invert_selection_btn.setAutoRaise(True)
        self.invert_selection_btn.setObjectName("invert_selection_btn")
        self.horizontalLayout_12.addWidget(self.invert_selection_btn)
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.horizontalLayout_12.addWidget(self.line_5)
        self.n_all_checked_items_lbl = QtWidgets.QLabel(self.centralwidget)
        self.n_all_checked_items_lbl.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setFamily("Monospace")
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.n_all_checked_items_lbl.setFont(font)
        self.n_all_checked_items_lbl.setStyleSheet(
            "QLabel {\n"
            "    font: bold 1.5em;\n"
            "    color: rgb(0, 0, 255);\n"
            "    padding: 1px 10px 0px 10px;\n"
            "}")
        self.n_all_checked_items_lbl.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.n_all_checked_items_lbl.setFrameShadow(QtWidgets.QFrame.Plain)
        self.n_all_checked_items_lbl.setLineWidth(1)
        self.n_all_checked_items_lbl.setAlignment(QtCore.Qt.AlignRight
                                                  | QtCore.Qt.AlignTrailing
                                                  | QtCore.Qt.AlignVCenter)
        self.n_all_checked_items_lbl.setObjectName("n_all_checked_items_lbl")
        self.horizontalLayout_12.addWidget(self.n_all_checked_items_lbl)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_12.addWidget(self.label)
        self.gridLayout.addLayout(self.horizontalLayout_12, 1, 1, 1, 1)
        self.filter_hbox = QtWidgets.QHBoxLayout()
        self.filter_hbox.setContentsMargins(-1, 0, -1, -1)
        self.filter_hbox.setSpacing(6)
        self.filter_hbox.setObjectName("filter_hbox")
        self.stripper_filter_hbox = QtWidgets.QHBoxLayout()
        self.stripper_filter_hbox.setSpacing(1)
        self.stripper_filter_hbox.setObjectName("stripper_filter_hbox")
        self.pos1_filter_btn = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pos1_filter_btn.sizePolicy().hasHeightForWidth())
        self.pos1_filter_btn.setSizePolicy(sizePolicy)
        self.pos1_filter_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.pos1_filter_btn.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/sm-icons/arrow_backward.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pos1_filter_btn.setIcon(icon11)
        self.pos1_filter_btn.setIconSize(QtCore.QSize(30, 30))
        self.pos1_filter_btn.setCheckable(True)
        self.pos1_filter_btn.setChecked(True)
        self.pos1_filter_btn.setAutoRaise(True)
        self.pos1_filter_btn.setObjectName("pos1_filter_btn")
        self.stripper_filter_hbox.addWidget(self.pos1_filter_btn)
        self.pos_filter_btn = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pos_filter_btn.sizePolicy().hasHeightForWidth())
        self.pos_filter_btn.setSizePolicy(sizePolicy)
        self.pos_filter_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.pos_filter_btn.setIconSize(QtCore.QSize(30, 30))
        self.pos_filter_btn.setCheckable(False)
        self.pos_filter_btn.setAutoRaise(False)
        self.pos_filter_btn.setObjectName("pos_filter_btn")
        self.stripper_filter_hbox.addWidget(self.pos_filter_btn)
        self.pos_dspin = QtWidgets.QDoubleSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pos_dspin.sizePolicy().hasHeightForWidth())
        self.pos_dspin.setSizePolicy(sizePolicy)
        self.pos_dspin.setMaximum(1000.0)
        self.pos_dspin.setProperty("value", 223.74)
        self.pos_dspin.setObjectName("pos_dspin")
        self.stripper_filter_hbox.addWidget(self.pos_dspin)
        self.pos2_filter_btn = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pos2_filter_btn.sizePolicy().hasHeightForWidth())
        self.pos2_filter_btn.setSizePolicy(sizePolicy)
        self.pos2_filter_btn.setMinimumSize(QtCore.QSize(0, 0))
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/sm-icons/arrow_forward.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pos2_filter_btn.setIcon(icon12)
        self.pos2_filter_btn.setIconSize(QtCore.QSize(30, 30))
        self.pos2_filter_btn.setCheckable(True)
        self.pos2_filter_btn.setChecked(True)
        self.pos2_filter_btn.setAutoRaise(True)
        self.pos2_filter_btn.setObjectName("pos2_filter_btn")
        self.stripper_filter_hbox.addWidget(self.pos2_filter_btn)
        self.filter_hbox.addLayout(self.stripper_filter_hbox)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.filter_hbox.addWidget(self.line_3)
        self.show_disconnected_btn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.show_disconnected_btn.sizePolicy().hasHeightForWidth())
        self.show_disconnected_btn.setSizePolicy(sizePolicy)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/sm-icons/fail.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.show_disconnected_btn.setIcon(icon13)
        self.show_disconnected_btn.setIconSize(QtCore.QSize(30, 30))
        self.show_disconnected_btn.setCheckable(True)
        self.show_disconnected_btn.setObjectName("show_disconnected_btn")
        self.filter_hbox.addWidget(self.show_disconnected_btn)
        self.show_warning_dx02_btn = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.show_warning_dx02_btn.sizePolicy().hasHeightForWidth())
        self.show_warning_dx02_btn.setSizePolicy(sizePolicy)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/sm-icons/dx02_warning.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.show_warning_dx02_btn.setIcon(icon14)
        self.show_warning_dx02_btn.setIconSize(QtCore.QSize(80, 30))
        self.show_warning_dx02_btn.setCheckable(True)
        self.show_warning_dx02_btn.setObjectName("show_warning_dx02_btn")
        self.filter_hbox.addWidget(self.show_warning_dx02_btn)
        self.show_warning_dx12_btn = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.show_warning_dx12_btn.sizePolicy().hasHeightForWidth())
        self.show_warning_dx12_btn.setSizePolicy(sizePolicy)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/sm-icons/dx12_warning.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.show_warning_dx12_btn.setIcon(icon15)
        self.show_warning_dx12_btn.setIconSize(QtCore.QSize(80, 30))
        self.show_warning_dx12_btn.setCheckable(True)
        self.show_warning_dx12_btn.setObjectName("show_warning_dx12_btn")
        self.filter_hbox.addWidget(self.show_warning_dx12_btn)
        self.show_diff_x0ref_btn = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.show_diff_x0ref_btn.sizePolicy().hasHeightForWidth())
        self.show_diff_x0ref_btn.setSizePolicy(sizePolicy)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/sm-icons/dx0ref_warning.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.show_diff_x0ref_btn.setIcon(icon16)
        self.show_diff_x0ref_btn.setIconSize(QtCore.QSize(80, 30))
        self.show_diff_x0ref_btn.setCheckable(True)
        self.show_diff_x0ref_btn.setObjectName("show_diff_x0ref_btn")
        self.filter_hbox.addWidget(self.show_diff_x0ref_btn)
        self.show_diff_x2ref_btn = QtWidgets.QToolButton(self.centralwidget)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(":/sm-icons/dx2ref_warning.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.show_diff_x2ref_btn.setIcon(icon17)
        self.show_diff_x2ref_btn.setIconSize(QtCore.QSize(80, 30))
        self.show_diff_x2ref_btn.setCheckable(True)
        self.show_diff_x2ref_btn.setObjectName("show_diff_x2ref_btn")
        self.filter_hbox.addWidget(self.show_diff_x2ref_btn)
        self.show_state_diff_btn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.show_state_diff_btn.sizePolicy().hasHeightForWidth())
        self.show_state_diff_btn.setSizePolicy(sizePolicy)
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap(":/sm-icons/red-green.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.show_state_diff_btn.setIcon(icon18)
        self.show_state_diff_btn.setIconSize(QtCore.QSize(30, 30))
        self.show_state_diff_btn.setCheckable(True)
        self.show_state_diff_btn.setObjectName("show_state_diff_btn")
        self.filter_hbox.addWidget(self.show_state_diff_btn)
        self.show_all_selected_btn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.show_all_selected_btn.sizePolicy().hasHeightForWidth())
        self.show_all_selected_btn.setSizePolicy(sizePolicy)
        icon19 = QtGui.QIcon()
        icon19.addPixmap(QtGui.QPixmap(":/sm-icons/checked.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.show_all_selected_btn.setIcon(icon19)
        self.show_all_selected_btn.setIconSize(QtCore.QSize(24, 30))
        self.show_all_selected_btn.setCheckable(True)
        self.show_all_selected_btn.setObjectName("show_all_selected_btn")
        self.filter_hbox.addWidget(self.show_all_selected_btn)
        self.filter_ctrls_hbox = QtWidgets.QHBoxLayout()
        self.filter_ctrls_hbox.setObjectName("filter_ctrls_hbox")
        self.filter_hbox.addLayout(self.filter_ctrls_hbox)
        self.gridLayout.addLayout(self.filter_hbox, 1, 16, 1, 1)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.init_settings_lbl = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.init_settings_lbl.sizePolicy().hasHeightForWidth())
        self.init_settings_lbl.setSizePolicy(sizePolicy)
        self.init_settings_lbl.setObjectName("init_settings_lbl")
        self.horizontalLayout_11.addWidget(self.init_settings_lbl)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem2)
        self.init_settings_chkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.init_settings_chkbox.setObjectName("init_settings_chkbox")
        self.horizontalLayout_11.addWidget(self.init_settings_chkbox)
        self.skip_none_chkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.skip_none_chkbox.setObjectName("skip_none_chkbox")
        self.horizontalLayout_11.addWidget(self.skip_none_chkbox)
        self.gridLayout.addLayout(self.horizontalLayout_11, 6, 1, 1, 16)
        self.strict_wildcard_chkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.strict_wildcard_chkbox.setObjectName("strict_wildcard_chkbox")
        self.gridLayout.addWidget(self.strict_wildcard_chkbox, 1, 15, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.reload_lattice_btn = QtWidgets.QToolButton(self.centralwidget)
        icon20 = QtGui.QIcon()
        icon20.addPixmap(QtGui.QPixmap(":/sm-icons/reload.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reload_lattice_btn.setIcon(icon20)
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
        icon21 = QtGui.QIcon()
        icon21.addPixmap(QtGui.QPixmap(":/sm-icons/view-details.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.lv_view_btn.setIcon(icon21)
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
        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.horizontalLayout.addWidget(self.line_6)
        self.show_refset_ctrls_btn = QtWidgets.QToolButton(self.centralwidget)
        self.show_refset_ctrls_btn.setIcon(icon6)
        self.show_refset_ctrls_btn.setIconSize(QtCore.QSize(24, 24))
        self.show_refset_ctrls_btn.setCheckable(True)
        self.show_refset_ctrls_btn.setChecked(True)
        self.show_refset_ctrls_btn.setAutoRaise(True)
        self.show_refset_ctrls_btn.setObjectName("show_refset_ctrls_btn")
        self.horizontalLayout.addWidget(self.show_refset_ctrls_btn)
        self.refset_ctrl_hbox = QtWidgets.QHBoxLayout()
        self.refset_ctrl_hbox.setContentsMargins(0, 0, -1, 0)
        self.refset_ctrl_hbox.setSpacing(2)
        self.refset_ctrl_hbox.setObjectName("refset_ctrl_hbox")
        self.ref_datasrc_cbb = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ref_datasrc_cbb.sizePolicy().hasHeightForWidth())
        self.ref_datasrc_cbb.setSizePolicy(sizePolicy)
        self.ref_datasrc_cbb.setObjectName("ref_datasrc_cbb")
        self.ref_datasrc_cbb.addItem("")
        self.ref_datasrc_cbb.addItem("")
        self.refset_ctrl_hbox.addWidget(self.ref_datasrc_cbb)
        self.refset_ctrl_vbox = QtWidgets.QVBoxLayout()
        self.refset_ctrl_vbox.setContentsMargins(0, 0, -1, -1)
        self.refset_ctrl_vbox.setSpacing(1)
        self.refset_ctrl_vbox.setObjectName("refset_ctrl_vbox")
        self.update_ref_btn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.update_ref_btn.sizePolicy().hasHeightForWidth())
        self.update_ref_btn.setSizePolicy(sizePolicy)
        self.update_ref_btn.setObjectName("update_ref_btn")
        self.refset_ctrl_vbox.addWidget(self.update_ref_btn)
        self.refset_pb = QtWidgets.QProgressBar(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.refset_pb.sizePolicy().hasHeightForWidth())
        self.refset_pb.setSizePolicy(sizePolicy)
        self.refset_pb.setMinimumSize(QtCore.QSize(0, 10))
        self.refset_pb.setMaximumSize(QtCore.QSize(16777215, 10))
        self.refset_pb.setProperty("value", 0)
        self.refset_pb.setFormat("")
        self.refset_pb.setObjectName("refset_pb")
        self.refset_ctrl_vbox.addWidget(self.refset_pb)
        self.refset_ctrl_hbox.addLayout(self.refset_ctrl_vbox)
        self.horizontalLayout.addLayout(self.refset_ctrl_hbox)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
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
        self.update_rate_cbb.addItem("")
        self.horizontalLayout.addWidget(self.update_rate_cbb)
        self.update_ctrl_btn = QtWidgets.QToolButton(self.centralwidget)
        icon22 = QtGui.QIcon()
        icon22.addPixmap(QtGui.QPixmap(":/sm-icons/start.png"),
                         QtGui.QIcon.Active, QtGui.QIcon.Off)
        icon22.addPixmap(QtGui.QPixmap(":/sm-icons/stop.png"),
                         QtGui.QIcon.Active, QtGui.QIcon.On)
        self.update_ctrl_btn.setIcon(icon22)
        self.update_ctrl_btn.setIconSize(QtCore.QSize(32, 32))
        self.update_ctrl_btn.setCheckable(True)
        self.update_ctrl_btn.setChecked(False)
        self.update_ctrl_btn.setAutoRaise(True)
        self.update_ctrl_btn.setObjectName("update_ctrl_btn")
        self.horizontalLayout.addWidget(self.update_ctrl_btn)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_3.setSpacing(1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.single_update_btn = QtWidgets.QToolButton(self.centralwidget)
        icon23 = QtGui.QIcon()
        icon23.addPixmap(QtGui.QPixmap(":/sm-icons/single.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.single_update_btn.setIcon(icon23)
        self.single_update_btn.setIconSize(QtCore.QSize(32, 32))
        self.single_update_btn.setToolButtonStyle(
            QtCore.Qt.ToolButtonTextBesideIcon)
        self.single_update_btn.setAutoRaise(True)
        self.single_update_btn.setObjectName("single_update_btn")
        self.verticalLayout_3.addWidget(self.single_update_btn)
        self.refresh_pb = QtWidgets.QProgressBar(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.refresh_pb.sizePolicy().hasHeightForWidth())
        self.refresh_pb.setSizePolicy(sizePolicy)
        self.refresh_pb.setMinimumSize(QtCore.QSize(0, 10))
        self.refresh_pb.setMaximumSize(QtCore.QSize(16777215, 10))
        self.refresh_pb.setProperty("value", 0)
        self.refresh_pb.setFormat("")
        self.refresh_pb.setObjectName("refresh_pb")
        self.verticalLayout_3.addWidget(self.refresh_pb)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.apply_btn.sizePolicy().hasHeightForWidth())
        self.apply_btn.setSizePolicy(sizePolicy)
        self.apply_btn.setFlat(False)
        self.apply_btn.setObjectName("apply_btn")
        self.horizontalLayout_3.addWidget(self.apply_btn)
        self.scale_op_cbb = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scale_op_cbb.sizePolicy().hasHeightForWidth())
        self.scale_op_cbb.setSizePolicy(sizePolicy)
        self.scale_op_cbb.setIconSize(QtCore.QSize(24, 24))
        self.scale_op_cbb.setDuplicatesEnabled(False)
        self.scale_op_cbb.setFrame(False)
        self.scale_op_cbb.setObjectName("scale_op_cbb")
        icon24 = QtGui.QIcon()
        icon24.addPixmap(QtGui.QPixmap(":/sm-icons/multi.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.scale_op_cbb.addItem(icon24, "")
        self.scale_op_cbb.setItemText(0, "")
        icon25 = QtGui.QIcon()
        icon25.addPixmap(QtGui.QPixmap(":/sm-icons/plus.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.scale_op_cbb.addItem(icon25, "")
        self.scale_op_cbb.setItemText(1, "")
        self.horizontalLayout_3.addWidget(self.scale_op_cbb)
        self.scaling_factor_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scaling_factor_lineEdit.sizePolicy().hasHeightForWidth())
        self.scaling_factor_lineEdit.setSizePolicy(sizePolicy)
        self.scaling_factor_lineEdit.setStyleSheet(
            "QLineEdit {\n"
            "    color: blue;\n"
            "    padding: 0 0 0 0.5em;\n"
            "}")
        self.scaling_factor_lineEdit.setObjectName("scaling_factor_lineEdit")
        self.horizontalLayout_3.addWidget(self.scaling_factor_lineEdit)
        self.auto_sf_btn = QtWidgets.QToolButton(self.centralwidget)
        icon26 = QtGui.QIcon()
        icon26.addPixmap(QtGui.QPixmap(":/sm-icons/calc-sf.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.auto_sf_btn.setIcon(icon26)
        self.auto_sf_btn.setIconSize(QtCore.QSize(32, 32))
        self.auto_sf_btn.setCheckable(True)
        self.auto_sf_btn.setChecked(True)
        self.auto_sf_btn.setAutoRaise(True)
        self.auto_sf_btn.setObjectName("auto_sf_btn")
        self.horizontalLayout_3.addWidget(self.auto_sf_btn)
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
        self.gridLayout.addLayout(self.horizontalLayout, 4, 1, 1, 16)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 2045, 32))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menu_View = QtWidgets.QMenu(self.menubar)
        self.menu_View.setObjectName("menu_View")
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
        self.snp_dock = DockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.snp_dock.sizePolicy().hasHeightForWidth())
        self.snp_dock.setSizePolicy(sizePolicy)
        self.snp_dock.setWindowIcon(icon)
        self.snp_dock.setStyleSheet("QDockWidget {\n"
                                    "    font-weight: bold;\n"
                                    "}\n"
                                    "\n"
                                    "QDockWidget::title {\n"
                                    "    text-align: left;\n"
                                    "    background: lightblue;\n"
                                    "    padding-left: 15px;\n"
                                    "}")
        self.snp_dock.setFloating(False)
        self.snp_dock.setFeatures(
            QtWidgets.QDockWidget.DockWidgetClosable
            | QtWidgets.QDockWidget.DockWidgetFloatable
            | QtWidgets.QDockWidget.DockWidgetVerticalTitleBar)
        self.snp_dock.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.snp_dock.setObjectName("snp_dock")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout_3.setContentsMargins(6, 6, 6, 6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_12 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_8.addWidget(self.label_12)
        self.select_none_tags_btn = QtWidgets.QPushButton(
            self.dockWidgetContents)
        self.select_none_tags_btn.setObjectName("select_none_tags_btn")
        self.horizontalLayout_8.addWidget(self.select_none_tags_btn)
        self.select_all_tags_btn = QtWidgets.QPushButton(
            self.dockWidgetContents)
        self.select_all_tags_btn.setObjectName("select_all_tags_btn")
        self.horizontalLayout_8.addWidget(self.select_all_tags_btn)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem4)
        self.label_13 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_8.addWidget(self.label_13)
        self.select_none_ions_btn = QtWidgets.QPushButton(
            self.dockWidgetContents)
        self.select_none_ions_btn.setObjectName("select_none_ions_btn")
        self.horizontalLayout_8.addWidget(self.select_none_ions_btn)
        self.select_all_ions_btn = QtWidgets.QPushButton(
            self.dockWidgetContents)
        self.select_all_ions_btn.setObjectName("select_all_ions_btn")
        self.horizontalLayout_8.addWidget(self.select_all_ions_btn)
        self.gridLayout_3.addLayout(self.horizontalLayout_8, 4, 0, 1, 1)
        self.snp_treeView = QtWidgets.QTreeView(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.snp_treeView.sizePolicy().hasHeightForWidth())
        self.snp_treeView.setSizePolicy(sizePolicy)
        self.snp_treeView.setDragDropMode(
            QtWidgets.QAbstractItemView.NoDragDrop)
        self.snp_treeView.setIndentation(10)
        self.snp_treeView.setRootIsDecorated(True)
        self.snp_treeView.setUniformRowHeights(True)
        self.snp_treeView.setSortingEnabled(False)
        self.snp_treeView.setAnimated(True)
        self.snp_treeView.setObjectName("snp_treeView")
        self.gridLayout_3.addWidget(self.snp_treeView, 6, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.current_snp_lbl = QtWidgets.QLabel(self.dockWidgetContents)
        self.current_snp_lbl.setObjectName("current_snp_lbl")
        self.horizontalLayout_6.addWidget(self.current_snp_lbl)
        self.current_snp_lineEdit = QtWidgets.QLineEdit(
            self.dockWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.current_snp_lineEdit.setFont(font)
        self.current_snp_lineEdit.setReadOnly(True)
        self.current_snp_lineEdit.setObjectName("current_snp_lineEdit")
        self.horizontalLayout_6.addWidget(self.current_snp_lineEdit)
        self.gridLayout_3.addLayout(self.horizontalLayout_6, 7, 0, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(-1, 0, 0, -1)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.tag_filter_area = QtWidgets.QScrollArea(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tag_filter_area.sizePolicy().hasHeightForWidth())
        self.tag_filter_area.setSizePolicy(sizePolicy)
        self.tag_filter_area.setStyleSheet("QScrollArea {\n"
                                           "    border: none;\n"
                                           "}")
        self.tag_filter_area.setWidgetResizable(True)
        self.tag_filter_area.setObjectName("tag_filter_area")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1994, 89))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.tag_filter_area.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_7.addWidget(self.tag_filter_area)
        self.snp_filter_hbox = QtWidgets.QHBoxLayout()
        self.snp_filter_hbox.setContentsMargins(0, 0, -1, -1)
        self.snp_filter_hbox.setObjectName("snp_filter_hbox")
        self.horizontalLayout_7.addLayout(self.snp_filter_hbox)
        self.gridLayout_3.addLayout(self.horizontalLayout_7, 3, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.snp_expand_btn = QtWidgets.QToolButton(self.dockWidgetContents)
        icon27 = QtGui.QIcon()
        icon27.addPixmap(QtGui.QPixmap(":/sm-icons/expand.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon27.addPixmap(QtGui.QPixmap(":/sm-icons/collapse.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.snp_expand_btn.setIcon(icon27)
        self.snp_expand_btn.setIconSize(QtCore.QSize(24, 24))
        self.snp_expand_btn.setCheckable(True)
        self.snp_expand_btn.setAutoRaise(True)
        self.snp_expand_btn.setObjectName("snp_expand_btn")
        self.horizontalLayout_4.addWidget(self.snp_expand_btn)
        self.label_5 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.data_uri_lineEdit = QtWidgets.QLineEdit(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.data_uri_lineEdit.sizePolicy().hasHeightForWidth())
        self.data_uri_lineEdit.setSizePolicy(sizePolicy)
        self.data_uri_lineEdit.setReadOnly(True)
        self.data_uri_lineEdit.setObjectName("data_uri_lineEdit")
        self.horizontalLayout_4.addWidget(self.data_uri_lineEdit)
        self.snp_new_lbl = QtWidgets.QLabel(self.dockWidgetContents)
        self.snp_new_lbl.setObjectName("snp_new_lbl")
        self.horizontalLayout_4.addWidget(self.snp_new_lbl)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.snp_refresh_btn = QtWidgets.QToolButton(self.dockWidgetContents)
        icon28 = QtGui.QIcon()
        icon28.addPixmap(QtGui.QPixmap(":/sm-icons/refresh.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.snp_refresh_btn.setIcon(icon28)
        self.snp_refresh_btn.setIconSize(QtCore.QSize(24, 24))
        self.snp_refresh_btn.setAutoRaise(True)
        self.snp_refresh_btn.setObjectName("snp_refresh_btn")
        self.horizontalLayout_4.addWidget(self.snp_refresh_btn)
        self.nsnp_btn = QtWidgets.QPushButton(self.dockWidgetContents)
        self.nsnp_btn.setObjectName("nsnp_btn")
        self.horizontalLayout_4.addWidget(self.nsnp_btn)
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
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.filter_date_chkbox = QtWidgets.QCheckBox(self.dockWidgetContents)
        self.filter_date_chkbox.setObjectName("filter_date_chkbox")
        self.horizontalLayout_10.addWidget(self.filter_date_chkbox)
        self.dateEdit1 = QtWidgets.QDateEdit(self.dockWidgetContents)
        self.dateEdit1.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.dateEdit1.sizePolicy().hasHeightForWidth())
        self.dateEdit1.setSizePolicy(sizePolicy)
        self.dateEdit1.setReadOnly(True)
        self.dateEdit1.setCalendarPopup(False)
        self.dateEdit1.setObjectName("dateEdit1")
        self.horizontalLayout_10.addWidget(self.dateEdit1)
        self.label_7 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_10.addWidget(self.label_7)
        self.dateEdit2 = QtWidgets.QDateEdit(self.dockWidgetContents)
        self.dateEdit2.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.dateEdit2.sizePolicy().hasHeightForWidth())
        self.dateEdit2.setSizePolicy(sizePolicy)
        self.dateEdit2.setReadOnly(True)
        self.dateEdit2.setCalendarPopup(False)
        self.dateEdit2.setObjectName("dateEdit2")
        self.horizontalLayout_10.addWidget(self.dateEdit2)
        self.toolButton_2 = QtWidgets.QToolButton(self.dockWidgetContents)
        self.toolButton_2.setObjectName("toolButton_2")
        self.horizontalLayout_10.addWidget(self.toolButton_2)
        spacerItem6 = QtWidgets.QSpacerItem(100, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem6)
        self.filter_note_chkbox = QtWidgets.QCheckBox(self.dockWidgetContents)
        self.filter_note_chkbox.setObjectName("filter_note_chkbox")
        self.horizontalLayout_10.addWidget(self.filter_note_chkbox)
        self.snp_note_filter_lineEdit = QtWidgets.QLineEdit(
            self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.snp_note_filter_lineEdit.sizePolicy().hasHeightForWidth())
        self.snp_note_filter_lineEdit.setSizePolicy(sizePolicy)
        self.snp_note_filter_lineEdit.setObjectName("snp_note_filter_lineEdit")
        self.horizontalLayout_10.addWidget(self.snp_note_filter_lineEdit)
        self.gridLayout_3.addLayout(self.horizontalLayout_10, 5, 0, 1, 1)
        self.snp_dock.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.snp_dock)
        self.log_dock = DockWidget(MainWindow)
        self.log_dock.setMinimumSize(QtCore.QSize(697, 152))
        self.log_dock.setStyleSheet("QDockWidget {\n"
                                    "    font-weight: normal;\n"
                                    "}\n"
                                    "\n"
                                    "QDockWidget::title {\n"
                                    "    text-align: left;\n"
                                    "    background: pink;\n"
                                    "    padding-left: 15px;\n"
                                    "}")
        self.log_dock.setFeatures(
            QtWidgets.QDockWidget.DockWidgetClosable
            | QtWidgets.QDockWidget.DockWidgetFloatable
            | QtWidgets.QDockWidget.DockWidgetVerticalTitleBar)
        self.log_dock.setObjectName("log_dock")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(
            self.dockWidgetContents_2)
        self.verticalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.findtext_lbl = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.findtext_lbl.setObjectName("findtext_lbl")
        self.horizontalLayout_5.addWidget(self.findtext_lbl)
        self.findtext_lineEdit = QtWidgets.QLineEdit(self.dockWidgetContents_2)
        self.findtext_lineEdit.setObjectName("findtext_lineEdit")
        self.horizontalLayout_5.addWidget(self.findtext_lineEdit)
        self.label_11 = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_5.addWidget(self.label_11)
        self.setlog_count_lbl = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.setlog_count_lbl.setObjectName("setlog_count_lbl")
        self.horizontalLayout_5.addWidget(self.setlog_count_lbl)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem7)
        self.open_log_btn = QtWidgets.QPushButton(self.dockWidgetContents_2)
        self.open_log_btn.setObjectName("open_log_btn")
        self.horizontalLayout_5.addWidget(self.open_log_btn)
        self.clear_log_btn = QtWidgets.QToolButton(self.dockWidgetContents_2)
        self.clear_log_btn.setObjectName("clear_log_btn")
        self.horizontalLayout_5.addWidget(self.clear_log_btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.log_textEdit = QtWidgets.QTextEdit(self.dockWidgetContents_2)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.log_textEdit.setFont(font)
        self.log_textEdit.setUndoRedoEnabled(False)
        self.log_textEdit.setReadOnly(True)
        self.log_textEdit.setObjectName("log_textEdit")
        self.verticalLayout_2.addWidget(self.log_textEdit)
        self.log_dock.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.log_dock)
        self.action_About = QtWidgets.QAction(MainWindow)
        self.action_About.setObjectName("action_About")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        icon29 = QtGui.QIcon()
        icon29.addPixmap(QtGui.QPixmap(":/sm-icons/exit.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionE_xit.setIcon(icon29)
        self.actionE_xit.setObjectName("actionE_xit")
        self.actionContents = QtWidgets.QAction(MainWindow)
        self.actionContents.setObjectName("actionContents")
        self.action_Save = QtWidgets.QAction(MainWindow)
        icon30 = QtGui.QIcon()
        icon30.addPixmap(QtGui.QPixmap(":/sm-icons/save.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Save.setIcon(icon30)
        self.action_Save.setObjectName("action_Save")
        self.actionLoad_From_Snapshot = QtWidgets.QAction(MainWindow)
        icon31 = QtGui.QIcon()
        icon31.addPixmap(QtGui.QPixmap(":/sm-icons/folder-open-snp.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoad_From_Snapshot.setIcon(icon31)
        self.actionLoad_From_Snapshot.setObjectName("actionLoad_From_Snapshot")
        self.actionPhysics_Fields = QtWidgets.QAction(MainWindow)
        self.actionPhysics_Fields.setCheckable(True)
        self.actionPhysics_Fields.setChecked(False)
        icon32 = QtGui.QIcon()
        icon32.addPixmap(QtGui.QPixmap(":/sm-icons/physics.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPhysics_Fields.setIcon(icon32)
        self.actionPhysics_Fields.setObjectName("actionPhysics_Fields")
        self.actionEngineering_Fields = QtWidgets.QAction(MainWindow)
        self.actionEngineering_Fields.setCheckable(True)
        self.actionEngineering_Fields.setChecked(True)
        icon33 = QtGui.QIcon()
        icon33.addPixmap(QtGui.QPixmap(":/sm-icons/engineering.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEngineering_Fields.setIcon(icon33)
        self.actionEngineering_Fields.setObjectName("actionEngineering_Fields")
        self.actionLoad_Lattice = QtWidgets.QAction(MainWindow)
        icon34 = QtGui.QIcon()
        icon34.addPixmap(QtGui.QPixmap(":/sm-icons/load_lattice.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoad_Lattice.setIcon(icon34)
        self.actionLoad_Lattice.setObjectName("actionLoad_Lattice")
        self.actionLoad_Settings = QtWidgets.QAction(MainWindow)
        icon35 = QtGui.QIcon()
        icon35.addPixmap(QtGui.QPixmap(":/sm-icons/open.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoad_Settings.setIcon(icon35)
        self.actionLoad_Settings.setObjectName("actionLoad_Settings")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        icon36 = QtGui.QIcon()
        icon36.addPixmap(QtGui.QPixmap(":/sm-icons/preferences.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPreferences.setIcon(icon36)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionAdd_Devices = QtWidgets.QAction(MainWindow)
        icon37 = QtGui.QIcon()
        icon37.addPixmap(QtGui.QPixmap(":/sm-icons/add.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd_Devices.setIcon(icon37)
        self.actionAdd_Devices.setObjectName("actionAdd_Devices")
        self.actionTake_Snapshot = QtWidgets.QAction(MainWindow)
        icon38 = QtGui.QIcon()
        icon38.addPixmap(QtGui.QPixmap(":/sm-icons/snapshot.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTake_Snapshot.setIcon(icon38)
        self.actionTake_Snapshot.setObjectName("actionTake_Snapshot")
        self.actionFix_Corrector_Names = QtWidgets.QAction(MainWindow)
        self.actionFix_Corrector_Names.setObjectName(
            "actionFix_Corrector_Names")
        self.actionShow_Device_Settings_Log = QtWidgets.QAction(MainWindow)
        self.actionShow_Device_Settings_Log.setCheckable(True)
        self.actionShow_Device_Settings_Log.setChecked(True)
        self.actionShow_Device_Settings_Log.setObjectName(
            "actionShow_Device_Settings_Log")
        self.actionSnapshots = QtWidgets.QAction(MainWindow)
        self.actionSnapshots.setCheckable(True)
        self.actionSnapshots.setChecked(True)
        self.actionSnapshots.setObjectName("actionSnapshots")
        self.actionCapture_machstate = QtWidgets.QAction(MainWindow)
        icon39 = QtGui.QIcon()
        icon39.addPixmap(QtGui.QPixmap(":/sm-icons/machstate.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCapture_machstate.setIcon(icon39)
        self.actionCapture_machstate.setObjectName("actionCapture_machstate")
        self.actionManage_Database = QtWidgets.QAction(MainWindow)
        icon40 = QtGui.QIcon()
        icon40.addPixmap(QtGui.QPixmap(":/sm-icons/db.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionManage_Database.setIcon(icon40)
        self.actionManage_Database.setObjectName("actionManage_Database")
        self.menu_File.addAction(self.actionLoad_From_Snapshot)
        self.menu_Help.addAction(self.actionContents)
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.action_About)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menuTools.addAction(self.actionFix_Corrector_Names)
        self.menuTools.addAction(self.actionManage_Database)
        self.menu_View.addAction(self.actionShow_Device_Settings_Log)
        self.menu_View.addAction(self.actionSnapshots)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menu_View.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.toolBar.addAction(self.actionLoad_Lattice)
        self.toolBar.addAction(self.actionAdd_Devices)
        self.toolBar.addAction(self.actionTake_Snapshot)
        self.toolBar.addAction(self.actionCapture_machstate)
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
        self.actionPhysics_Fields.toggled['bool'].connect(
            MainWindow.on_toggle_phyfields)
        self.actionEngineering_Fields.toggled['bool'].connect(
            MainWindow.on_toggle_engfields)
        self.actionLoad_Lattice.triggered.connect(MainWindow.on_load_lattice)
        self.filter_lineEdit.editingFinished.connect(
            MainWindow.on_filter_changed)
        self.actionPreferences.triggered.connect(
            MainWindow.on_launch_preferences)
        self.reload_lattice_btn.clicked.connect(MainWindow.on_reload_lattice)
        self.update_ctrl_btn.toggled['bool'].connect(
            self.update_rate_cbb.setDisabled)
        self.update_rate_cbb.currentIndexChanged['int'].connect(
            MainWindow.on_update_rate)
        self.update_ctrl_btn.toggled['bool'].connect(
            MainWindow.on_toggle_update_btn)
        self.actionAdd_Devices.triggered.connect(MainWindow.on_add_devices)
        self.delete_btn.clicked.connect(MainWindow.on_remove_selected_settings)
        self.update_ctrl_btn.toggled['bool'].connect(
            self.single_update_btn.setDisabled)
        self.single_update_btn.clicked.connect(MainWindow.on_single_update)
        self.show_all_selected_btn.toggled['bool'].connect(
            MainWindow.on_toggle_all_selected)
        self.scaling_factor_lineEdit.returnPressed.connect(
            MainWindow.on_input_scaling_factor)
        self.init_settings_chkbox.toggled['bool'].connect(
            MainWindow.on_toggle_init_lattice_settings)
        self.ndigit_sbox.valueChanged['int'].connect(
            MainWindow.on_ndigit_valueChanged)
        self.filter_tip_btn.clicked.connect(MainWindow.on_show_query_tips)
        self.filter_btn.toggled['bool'].connect(self.filter_lineEdit.setFocus)
        self.scaling_factor_lineEdit.textChanged['QString'].connect(
            MainWindow.on_scaling_factor_changed)
        self.actionFix_Corrector_Names.triggered.connect(
            MainWindow.onFixCorNames)
        self.snp_expand_btn.toggled['bool'].connect(
            MainWindow.on_snp_expand_collapse)
        self.actionContents.triggered.connect(MainWindow.on_help)
        self.actionShow_Device_Settings_Log.toggled['bool'].connect(
            MainWindow.on_enable_logdock)
        self.findtext_lineEdit.returnPressed.connect(
            MainWindow.on_find_text_in_setlog)
        self.open_log_btn.clicked.connect(MainWindow.on_open_texteditor)
        self.log_textEdit.textChanged.connect(MainWindow.on_setlog_changed)
        self.clear_log_btn.clicked.connect(self.log_textEdit.clear)
        self.snp_refresh_btn.clicked.connect(MainWindow.on_refresh_snp)
        self.snp_treeView.clicked['QModelIndex'].connect(
            MainWindow.on_click_snpview)
        self.snp_dock.topLevelChanged['bool'].connect(
            MainWindow.on_snpdock_top_level_changed)
        self.auto_ndigit_chkbox.toggled['bool'].connect(
            self.ndigit_lbl.setDisabled)
        self.auto_ndigit_chkbox.toggled['bool'].connect(
            MainWindow.on_auto_ndigit)
        self.show_sts_btn.toggled['bool'].connect(
            self.total_elem_number_title_lbl.setVisible)
        self.show_sts_btn.toggled['bool'].connect(
            self.total_elem_number_lbl.setVisible)
        self.show_sts_btn.toggled['bool'].connect(
            self.total_field_number_title_lbl.setVisible)
        self.show_sts_btn.toggled['bool'].connect(
            self.total_field_number_lbl.setVisible)
        self.show_warning_dx12_btn.toggled['bool'].connect(
            MainWindow.on_show_warning_dx12)
        self.show_warning_dx02_btn.toggled['bool'].connect(
            MainWindow.on_show_warning_dx02)
        self.settingsView.pressed['QModelIndex'].connect(
            MainWindow.on_pressed_view)
        self.settingsView.clicked['QModelIndex'].connect(
            MainWindow.on_click_view)
        self.settingsView.doubleClicked['QModelIndex'].connect(
            MainWindow.on_dblclicked_view)
        self.strict_wildcard_chkbox.toggled['bool'].connect(
            MainWindow.on_toggle_strict_wildcard)
        self.snp_treeView.doubleClicked['QModelIndex'].connect(
            MainWindow.on_dblclicked_snp)
        self.actionSnapshots.toggled['bool'].connect(
            MainWindow.on_enable_snpdock)
        self.toolButton.clicked.connect(MainWindow.on_auto_column_width)
        self.dateEdit1.dateChanged['QDate'].connect(
            MainWindow.on_snp_filter_date_range_updated)
        self.dateEdit2.dateChanged['QDate'].connect(
            MainWindow.on_snp_filter_date_range_updated)
        self.filter_date_chkbox.toggled['bool'].connect(
            MainWindow.on_toggle_snp_filter_date_range)
        self.filter_note_chkbox.toggled['bool'].connect(
            MainWindow.on_toggle_snp_filter_note)
        self.snp_note_filter_lineEdit.editingFinished.connect(
            MainWindow.on_snp_filter_note_updated)
        self.toolButton_2.clicked.connect(MainWindow.on_select_daterange)
        self.nsnp_btn.clicked.connect(MainWindow.on_update_nsnp)
        self.actionManage_Database.triggered.connect(MainWindow.onManageDB)
        self.show_init_settings_btn.toggled['bool'].connect(
            self.skip_none_chkbox.setVisible)
        self.show_init_settings_btn.toggled['bool'].connect(
            self.init_settings_chkbox.setVisible)
        self.show_init_settings_btn.toggled['bool'].connect(
            self.init_settings_lbl.setVisible)
        self.show_disconnected_btn.toggled['bool'].connect(
            MainWindow.on_show_disconnected_items)
        self.wysiwyc_chkbox.toggled['bool'].connect(
            MainWindow.on_toggle_wysiwyc)
        self.show_state_diff_btn.toggled['bool'].connect(
            MainWindow.on_show_state_diff_items)
        self.update_ref_btn.clicked.connect(MainWindow.on_update_ref_values)
        self.show_diff_x0ref_btn.toggled['bool'].connect(
            MainWindow.on_show_warning_dx0ref)
        self.show_diff_x2ref_btn.toggled['bool'].connect(
            MainWindow.on_show_warning_dx2ref)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.settingsView, self.reload_lattice_btn)
        MainWindow.setTabOrder(self.reload_lattice_btn, self.lv_view_btn)
        MainWindow.setTabOrder(self.lv_view_btn, self.update_rate_cbb)
        MainWindow.setTabOrder(self.update_rate_cbb, self.update_ctrl_btn)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
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
        self.toolButton.setToolTip(
            _translate("MainWindow", "Auto adjust column width."))
        self.toolButton.setText(_translate("MainWindow", "Auto Width"))
        self.delete_btn.setToolTip(
            _translate("MainWindow", "Delete selected items."))
        self.delete_btn.setText(_translate("MainWindow", "Delete"))
        self.filter_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Search (Ctrl + F).</p></body></html>"))
        self.filter_btn.setShortcut(_translate("MainWindow", "Ctrl+F"))
        self.filter_tip_btn.setText(_translate("MainWindow", "?"))
        self.total_show_number_lbl.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Total number of items in current page.</p></body></html>"
            ))
        self.total_show_number_lbl.setText(_translate("MainWindow", "0"))
        self.label_4.setText(_translate("MainWindow", "Items"))
        self.show_sts_btn.setText(_translate("MainWindow", "..."))
        self.total_elem_number_title_lbl.setText(
            _translate("MainWindow", "Total Elements"))
        self.total_elem_number_lbl.setText(_translate("MainWindow", "0"))
        self.total_field_number_title_lbl.setText(
            _translate("MainWindow", "Fields"))
        self.total_field_number_lbl.setText(_translate("MainWindow", "0"))
        self.snp_ms_chkbox.setText(
            _translate("MainWindow", "Take Snapshot with Machine State"))
        self.wysiwyc_chkbox.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>If checked, take the snapshot in the way of \'What You See Is What You Capture\'.</p></body></html>"
            ))
        self.wysiwyc_chkbox.setText(_translate("MainWindow", "WYSIWYC"))
        self.auto_ndigit_chkbox.setToolTip(
            _translate("MainWindow",
                       "Change data presenting format to \'{n}g\'."))
        self.auto_ndigit_chkbox.setText(_translate("MainWindow", "Auto"))
        self.ndigit_lbl.setText(_translate("MainWindow", "Precision number"))
        self.show_init_settings_btn.setText(_translate("MainWindow", "..."))
        self.select_all_btn.setToolTip(
            _translate("MainWindow", "Check all in current page."))
        self.select_all_btn.setText(_translate("MainWindow", "Check All"))
        self.deselect_all_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Uncheck all in current page.</p></body></html>"
            ))
        self.deselect_all_btn.setText(_translate("MainWindow", "Uncheck All"))
        self.invert_selection_btn.setToolTip(
            _translate("MainWindow", "Invert checkstate of current page."))
        self.invert_selection_btn.setText(
            _translate("MainWindow", "Invert Checkstate"))
        self.n_all_checked_items_lbl.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Total number of all checked items.</p></body></html>"
            ))
        self.n_all_checked_items_lbl.setText(_translate("MainWindow", "0"))
        self.label.setText(_translate("MainWindow", "Checked Items"))
        self.pos_filter_btn.setToolTip(
            _translate(
                "MainWindow",
                "Reset the reference value of pos filter with stripper position."
            ))
        self.pos_filter_btn.setText(_translate("MainWindow", "Stripper"))
        self.pos_dspin.setToolTip(
            _translate(
                "MainWindow",
                "Click left and right arrow buttons to filter devices with longitudinal position (logical OR applies)."
            ))
        self.pos_dspin.setSuffix(_translate("MainWindow", " m"))
        self.pos2_filter_btn.setText(_translate("MainWindow", "..."))
        self.show_disconnected_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Show all disconnected items.</p></body></html>"
            ))
        self.show_disconnected_btn.setText(
            _translate("MainWindow", "Disconnected"))
        self.show_warning_dx02_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Show x<span style=\" vertical-align:sub;\">0 </span>!= x<span style=\" vertical-align:sub;\">2</span>, up to number of precision.</p></body></html>"
            ))
        self.show_warning_dx02_btn.setText(_translate("MainWindow", "dx02"))
        self.show_warning_dx12_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Show Δ(x<span style=\" vertical-align:sub;\">1</span>, x<span style=\" vertical-align:sub;\">2</span>) &gt; tolerance.</p></body></html>"
            ))
        self.show_warning_dx12_btn.setText(_translate("MainWindow", "dx12"))
        self.show_diff_x0ref_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Show x<span style=\" vertical-align:sub;\">0 </span>!= x<span style=\" vertical-align:sub;\">ref</span>, up to number of precision.</p></body></html>"
            ))
        self.show_diff_x0ref_btn.setText(_translate("MainWindow", "dx0ref"))
        self.show_diff_x2ref_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Show x<span style=\" vertical-align:sub;\">2 </span>!= x<span style=\" vertical-align:sub;\">ref</span>, up to number of precision.</p></body></html>"
            ))
        self.show_diff_x2ref_btn.setText(_translate("MainWindow", "dx2ref"))
        self.show_state_diff_btn.setToolTip(
            _translate(
                "MainWindow",
                "Show all devices with different state and last state."))
        self.show_state_diff_btn.setText(_translate("MainWindow",
                                                    "State Diff"))
        self.show_all_selected_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Show all checked items.</p></body></html>"
            ))
        self.show_all_selected_btn.setText(_translate("MainWindow", "Checked"))
        self.init_settings_lbl.setText(
            _translate("MainWindow",
                       "Initialize settings table from loaded lattice"))
        self.init_settings_chkbox.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Initialize device settings with the whole loaded lattice, check to generate the settings table.</p></body></html>"
            ))
        self.init_settings_chkbox.setText(
            _translate("MainWindow", "Initialize with loaded lattice"))
        self.skip_none_chkbox.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Skip devices that are not reachable (when initializing with loaded lattice).</p></body></html>"
            ))
        self.skip_none_chkbox.setText(
            _translate("MainWindow", "Skip Non-reachable Devices"))
        self.strict_wildcard_chkbox.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>When checked, apply wildcard matching with input filter string as-is.</p></body></html>"
            ))
        self.strict_wildcard_chkbox.setText(
            _translate("MainWindow", "Strict Wildcard"))
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
        self.show_refset_ctrls_btn.setText(_translate("MainWindow", "..."))
        self.ref_datasrc_cbb.setItemText(
            0, _translate("MainWindow", "Use Saved Setpoint (x0)"))
        self.ref_datasrc_cbb.setItemText(
            1, _translate("MainWindow", "Use Live Setpoint (x2)"))
        self.update_ref_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Update reference set with x<span style=\" vertical-align:sub;\">0</span>, works for checked rows.</p></body></html>"
            ))
        self.update_ref_btn.setText(
            _translate("MainWindow", "Update Reference"))
        self.label_6.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Auto : Realtime update</p><p>1-5 : Update every 0.2 to 1 second</p></body></html>"
            ))
        self.label_6.setText(_translate("MainWindow", "Update Rate"))
        self.update_rate_cbb.setItemText(0, _translate("MainWindow", "1.0 Hz"))
        self.update_rate_cbb.setItemText(1, _translate("MainWindow", "2.0 Hz"))
        self.update_rate_cbb.setItemText(2, _translate("MainWindow", "5.0 Hz"))
        self.update_rate_cbb.setItemText(3, _translate("MainWindow", "0.5 Hz"))
        self.update_rate_cbb.setItemText(4, _translate("MainWindow", "0.2 Hz"))
        self.update_rate_cbb.setItemText(5, _translate("MainWindow", "0.1 Hz"))
        self.update_ctrl_btn.setToolTip(
            _translate("MainWindow", "Start/stop updating values (Ctrl+F5)."))
        self.update_ctrl_btn.setText(_translate("MainWindow", "..."))
        self.update_ctrl_btn.setShortcut(_translate("MainWindow", "Ctrl+F5"))
        self.single_update_btn.setToolTip(
            _translate("MainWindow", "Update for one time (F5)."))
        self.single_update_btn.setText(_translate("MainWindow",
                                                  "Refresh Data"))
        self.single_update_btn.setShortcut(_translate("MainWindow", "F5"))
        self.apply_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Only apply the settings of checked items after scaling by the defined scaling factor.</p></body></html>"
            ))
        self.apply_btn.setText(_translate("MainWindow", "Apply"))
        self.scale_op_cbb.setToolTip(
            _translate("MainWindow",
                       "Select the arithmetical operation for scaling."))
        self.scaling_factor_lineEdit.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Scaling factor, input a number e.g. 0.8, or an expression, e.g. 12 / 18, then press Enter.</p></body></html>"
            ))
        self.scaling_factor_lineEdit.setText(_translate("MainWindow", "1.0"))
        self.auto_sf_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Check to enable auto fill the scaling factor.</p></body></html>"
            ))
        self.auto_sf_btn.setText(_translate("MainWindow", "..."))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menu_View.setTitle(_translate("MainWindow", "&View"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.snp_dock.setWindowTitle(_translate("MainWindow", "Snapshots"))
        self.label_12.setText(_translate("MainWindow", "Select Tags:"))
        self.select_none_tags_btn.setText(_translate("MainWindow", "None"))
        self.select_all_tags_btn.setText(_translate("MainWindow", "All"))
        self.label_13.setText(_translate("MainWindow", "Select Ions:"))
        self.select_none_ions_btn.setText(_translate("MainWindow", "None"))
        self.select_all_ions_btn.setText(_translate("MainWindow", "All"))
        self.current_snp_lbl.setText(
            _translate("MainWindow", "Current Snapshot"))
        self.snp_expand_btn.setToolTip(
            _translate("MainWindow", "Click to expand all."))
        self.snp_expand_btn.setText(_translate("MainWindow", "..."))
        self.label_5.setText(_translate("MainWindow", "Working Directory"))
        self.snp_new_lbl.setToolTip(
            _translate(
                "MainWindow",
                "Snapshot files have been updated in the last 1 minute."))
        self.snp_new_lbl.setText(_translate("MainWindow", "snp_sts"))
        self.snp_refresh_btn.setToolTip(
            _translate("MainWindow", "Refresh snapshots."))
        self.snp_refresh_btn.setText(_translate("MainWindow", "..."))
        self.nsnp_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Click to update the total number of snapshots to display, press refresh button to update snapshot list.</p></body></html>"
            ))
        self.nsnp_btn.setText(_translate("MainWindow", "N-SNP"))
        self.label_10.setText(_translate("MainWindow", "Total"))
        self.total_snp_lbl.setText(
            _translate("MainWindow",
                       "<html><head/><body><p>0</p></body></html>"))
        self.filter_date_chkbox.setText(
            _translate("MainWindow", "Filter  between"))
        self.dateEdit1.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd"))
        self.label_7.setText(_translate("MainWindow", "and"))
        self.dateEdit2.setDisplayFormat(_translate("MainWindow", "yyyy-MM-dd"))
        self.toolButton_2.setText(_translate("MainWindow", "..."))
        self.filter_note_chkbox.setText(_translate("MainWindow",
                                                   "Filter Note"))
        self.snp_note_filter_lineEdit.setToolTip(
            _translate("MainWindow", "Ignore cases, loose wildcard match."))
        self.log_dock.setWindowTitle(_translate("MainWindow", "Setting Logs"))
        self.findtext_lbl.setText(_translate("MainWindow", "Find Text"))
        self.label_11.setText(_translate("MainWindow", "Total log entries:"))
        self.setlog_count_lbl.setText(_translate("MainWindow", "0"))
        self.open_log_btn.setText(
            _translate("MainWindow", "Open in Text Editor"))
        self.clear_log_btn.setText(_translate("MainWindow", "Clear All"))
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
                "<html><head/><body><p>Record current device settings, fetch all live settings prior to this action.</p></body></html>"
            ))
        self.actionFix_Corrector_Names.setText(
            _translate("MainWindow", "Fix Corrector Names"))
        self.actionShow_Device_Settings_Log.setText(
            _translate("MainWindow", "Settings Log"))
        self.actionSnapshots.setText(_translate("MainWindow", "Snapshots"))
        self.actionCapture_machstate.setText(
            _translate("MainWindow", "Capture Machine State"))
        self.actionCapture_machstate.setIconText(
            _translate("MainWindow", "Capture Machine State"))
        self.actionCapture_machstate.setToolTip(
            _translate("MainWindow",
                       "Capture additional data as machine state."))
        self.actionManage_Database.setText(
            _translate("MainWindow", "Manage Database"))


from phantasy_ui.widgets import DockWidget
from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
