# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_snp_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(997, 600)
        Form.setStyleSheet(
            "QCheckBox::indicator {\n"
            "    width: 16px;\n"
            "    height: 16px;\n"
            "}\n"
            "QCheckBox::indicator::unchecked {\n"
            "    image: url(:/sm_icons/icons/uncheck-square.png);\n"
            "}\n"
            "QCheckBox::indicator::checked {\n"
            "    image: url(:/sm_icons/icons/check-square-fill.png);\n"
            "}\n"
            "QAbstractItemView::indicator::unchecked {\n"
            "    image: url(:/sm_icons/icons/uncheck-square.png);\n"
            "}\n"
            "QAbstractItemView::indicator::checked {\n"
            "    image: url(:/sm_icons/icons/check-square-fill.png);\n"
            "}\n"
            "\n"
            "/*Splitter*/\n"
            "QSplitter::handle {\n"
            "    height: 6px;\n"
            "    width: 6px;\n"
            "}\n"
            "QSplitter::handle:horizontal {\n"
            "    image: url(:/sm_icons/icons/separator-v.png);\n"
            "}\n"
            "QSplitter::handle:horizontal:pressed, QSplitter::handle:horizontal:hover {\n"
            "    image: url(:/sm_icons/icons/separator-v-pressed.png);\n"
            "}\n"
            "QSplitter::handle:vertical {\n"
            "    image: url(:/sm_icons/icons/separator-h.png);\n"
            "}\n"
            "QSplitter::handle:vertical:pressed, QSplitter::handle:vertical:hover {\n"
            "    image: url(:/sm_icons/icons/separator-h-pressed.png);\n"
            "}\n"
            "\n"
            "QMainWindow::separator {\n"
            "    width: 6px;\n"
            "    height: 6px;\n"
            "}\n"
            "QMainWindow::separator:horizontal {\n"
            "    image: url(:/sm_icons/icons/separator-h.png);\n"
            "}\n"
            "QMainWindow::separator:horizontal:hover, QMainWindow::separator:horizontal:pressed {\n"
            "    image: url(:/sm_icons/icons/separator-h-pressed.png);\n"
            "}\n"
            "QMainWindow::separator:vertical {\n"
            "    image: url(:/sm_icons/icons/separator-v.png);\n"
            "}\n"
            "QMainWindow::separator:vertical:hover, QMainWindow::separator:vertical:pressed {\n"
            "    image: url(:/sm_icons/icons/separator-v-pressed.png);\n"
            "}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.db_path_lineEdit = QtWidgets.QLineEdit(Form)
        self.db_path_lineEdit.setObjectName("db_path_lineEdit")
        self.horizontalLayout.addWidget(self.db_path_lineEdit)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.init_nitem_sbox = QtWidgets.QSpinBox(Form)
        self.init_nitem_sbox.setMinimum(10)
        self.init_nitem_sbox.setMaximum(500)
        self.init_nitem_sbox.setSingleStep(10)
        self.init_nitem_sbox.setProperty("value", 100)
        self.init_nitem_sbox.setObjectName("init_nitem_sbox")
        self.horizontalLayout.addWidget(self.init_nitem_sbox)
        self.fetched_nitem_lbl = QtWidgets.QLabel(Form)
        self.fetched_nitem_lbl.setObjectName("fetched_nitem_lbl")
        self.horizontalLayout.addWidget(self.fetched_nitem_lbl)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.total_nitem_lbl = QtWidgets.QLabel(Form)
        self.total_nitem_lbl.setObjectName("total_nitem_lbl")
        self.horizontalLayout.addWidget(self.total_nitem_lbl)
        self.db_open_btn = QtWidgets.QPushButton(Form)
        self.db_open_btn.setObjectName("db_open_btn")
        self.horizontalLayout.addWidget(self.db_open_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.splitter_2 = QtWidgets.QSplitter(Form)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.snp_tag_ion_frame = QtWidgets.QFrame(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.snp_tag_ion_frame.sizePolicy().hasHeightForWidth())
        self.snp_tag_ion_frame.setSizePolicy(sizePolicy)
        self.snp_tag_ion_frame.setStyleSheet(
            "QScrollArea {\n"
            "    border-top: 0px solid #B8B8B8;\n"
            "    border-bottom: 1px solid #B8B8B8;\n"
            "}")
        self.snp_tag_ion_frame.setObjectName("snp_tag_ion_frame")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.snp_tag_ion_frame)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setHorizontalSpacing(2)
        self.gridLayout_5.setVerticalSpacing(0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.splitter = QtWidgets.QSplitter(self.snp_tag_ion_frame)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.tag_filter_frame = QtWidgets.QFrame(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tag_filter_frame.sizePolicy().hasHeightForWidth())
        self.tag_filter_frame.setSizePolicy(sizePolicy)
        self.tag_filter_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tag_filter_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tag_filter_frame.setObjectName("tag_filter_frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tag_filter_frame)
        self.gridLayout_2.setContentsMargins(2, 0, 2, 2)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tag_filter_area = QtWidgets.QScrollArea(self.tag_filter_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.tag_filter_area.sizePolicy().hasHeightForWidth())
        self.tag_filter_area.setSizePolicy(sizePolicy)
        self.tag_filter_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tag_filter_area.setWidgetResizable(True)
        self.tag_filter_area.setObjectName("tag_filter_area")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 647, 89))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.tag_filter_area.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.tag_filter_area, 0, 0, 1, 6)
        self.select_invert_tags_btn = QtWidgets.QToolButton(
            self.tag_filter_frame)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/tm-icons/check-invert.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.select_invert_tags_btn.setIcon(icon)
        self.select_invert_tags_btn.setIconSize(QtCore.QSize(28, 28))
        self.select_invert_tags_btn.setAutoRaise(True)
        self.select_invert_tags_btn.setObjectName("select_invert_tags_btn")
        self.gridLayout_2.addWidget(self.select_invert_tags_btn, 1, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 4, 1, 1)
        self.select_none_tags_btn = QtWidgets.QToolButton(
            self.tag_filter_frame)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/tm-icons/check-none.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.select_none_tags_btn.setIcon(icon1)
        self.select_none_tags_btn.setIconSize(QtCore.QSize(28, 28))
        self.select_none_tags_btn.setAutoRaise(True)
        self.select_none_tags_btn.setObjectName("select_none_tags_btn")
        self.gridLayout_2.addWidget(self.select_none_tags_btn, 1, 1, 1, 1)
        self.tag_filter_nitem_lbl = QtWidgets.QLabel(self.tag_filter_frame)
        self.tag_filter_nitem_lbl.setText("")
        self.tag_filter_nitem_lbl.setObjectName("tag_filter_nitem_lbl")
        self.gridLayout_2.addWidget(self.tag_filter_nitem_lbl, 1, 5, 1, 1)
        self.select_all_tags_btn = QtWidgets.QToolButton(self.tag_filter_frame)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/tm-icons/check-all.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.select_all_tags_btn.setIcon(icon2)
        self.select_all_tags_btn.setIconSize(QtCore.QSize(28, 28))
        self.select_all_tags_btn.setAutoRaise(True)
        self.select_all_tags_btn.setObjectName("select_all_tags_btn")
        self.gridLayout_2.addWidget(self.select_all_tags_btn, 1, 3, 1, 1)
        self.ion_filter_frame = QtWidgets.QFrame(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ion_filter_frame.sizePolicy().hasHeightForWidth())
        self.ion_filter_frame.setSizePolicy(sizePolicy)
        self.ion_filter_frame.setMinimumSize(QtCore.QSize(0, 120))
        self.ion_filter_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ion_filter_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.ion_filter_frame.setObjectName("ion_filter_frame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.ion_filter_frame)
        self.gridLayout_4.setContentsMargins(2, 0, 2, 2)
        self.gridLayout_4.setSpacing(2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.select_none_ions_btn = QtWidgets.QToolButton(
            self.ion_filter_frame)
        self.select_none_ions_btn.setIcon(icon1)
        self.select_none_ions_btn.setIconSize(QtCore.QSize(28, 28))
        self.select_none_ions_btn.setAutoRaise(True)
        self.select_none_ions_btn.setObjectName("select_none_ions_btn")
        self.gridLayout_4.addWidget(self.select_none_ions_btn, 1, 1, 1, 1)
        self.select_all_ions_btn = QtWidgets.QToolButton(self.ion_filter_frame)
        self.select_all_ions_btn.setIcon(icon2)
        self.select_all_ions_btn.setIconSize(QtCore.QSize(28, 28))
        self.select_all_ions_btn.setAutoRaise(True)
        self.select_all_ions_btn.setObjectName("select_all_ions_btn")
        self.gridLayout_4.addWidget(self.select_all_ions_btn, 1, 3, 1, 1)
        self.ion_filter_area = QtWidgets.QScrollArea(self.ion_filter_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.ion_filter_area.sizePolicy().hasHeightForWidth())
        self.ion_filter_area.setSizePolicy(sizePolicy)
        self.ion_filter_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ion_filter_area.setWidgetResizable(True)
        self.ion_filter_area.setObjectName("ion_filter_area")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(
            0, 0, 320, 89))
        self.scrollAreaWidgetContents_2.setObjectName(
            "scrollAreaWidgetContents_2")
        self.ion_filter_area.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout_4.addWidget(self.ion_filter_area, 0, 0, 1, 6)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 1, 4, 1, 1)
        self.select_invert_ions_btn = QtWidgets.QToolButton(
            self.ion_filter_frame)
        self.select_invert_ions_btn.setIcon(icon)
        self.select_invert_ions_btn.setIconSize(QtCore.QSize(28, 28))
        self.select_invert_ions_btn.setAutoRaise(True)
        self.select_invert_ions_btn.setObjectName("select_invert_ions_btn")
        self.gridLayout_4.addWidget(self.select_invert_ions_btn, 1, 2, 1, 1)
        self.ion_filter_nitem_lbl = QtWidgets.QLabel(self.ion_filter_frame)
        self.ion_filter_nitem_lbl.setText("")
        self.ion_filter_nitem_lbl.setObjectName("ion_filter_nitem_lbl")
        self.gridLayout_4.addWidget(self.ion_filter_nitem_lbl, 1, 5, 1, 1)
        self.gridLayout_5.addWidget(self.splitter, 0, 0, 1, 1)
        self.snp_view_frame = QtWidgets.QFrame(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.snp_view_frame.sizePolicy().hasHeightForWidth())
        self.snp_view_frame.setSizePolicy(sizePolicy)
        self.snp_view_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.snp_view_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.snp_view_frame.setObjectName("snp_view_frame")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.snp_view_frame)
        self.gridLayout_6.setContentsMargins(2, 2, 2, 2)
        self.gridLayout_6.setSpacing(2)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.filter_note_lineEdit = QtWidgets.QLineEdit(self.snp_view_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.filter_note_lineEdit.sizePolicy().hasHeightForWidth())
        self.filter_note_lineEdit.setSizePolicy(sizePolicy)
        self.filter_note_lineEdit.setObjectName("filter_note_lineEdit")
        self.gridLayout_6.addWidget(self.filter_note_lineEdit, 0, 7, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem2, 0, 1, 1, 1)
        self.view = QtWidgets.QTreeView(self.snp_view_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.view.sizePolicy().hasHeightForWidth())
        self.view.setSizePolicy(sizePolicy)
        self.view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.view.setStyleSheet(
            "QHeaderView {\n"
            "    qproperty-defaultAlignment: AlignHCenter AlignVCenter;\n"
            "    font-weight: bold;\n"
            "}\n"
            "QTreeView {\n"
            "    font-family: monospace;\n"
            "    show-decoration-selected: 1;\n"
            "    alternate-background-color: #F7F7F7;\n"
            "}\n"
            "QTreeView::item {\n"
            "    border: 1px solid #D9D9D9;\n"
            "    border-top-color: transparent;\n"
            "    border-bottom-color: transparent;\n"
            "}\n"
            "QTreeView::item:hover {\n"
            "    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);\n"
            "    border: 1px solid #bfcde4;\n"
            "}\n"
            "QTreeView::item:selected:!has-children {\n"
            "    border: 1px solid #567DBC;\n"
            "    background-color: #D3D7CF;\n"
            "}\n"
            "QTreeView::item:selected:active:!has-children {\n"
            "    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #99C0FC, stop: 1 #7BACF9);\n"
            "}\n"
            "QTreeView::item::has-children {\n"
            "    color: #308CC6;\n"
            "}\n"
            "/*\n"
            "QTreeView::branch {\n"
            "        background: palette(base);\n"
            "}\n"
            "\n"
            "QTreeView::branch:has-siblings:!adjoins-item {\n"
            "        background: cyan;\n"
            "}\n"
            "\n"
            "QTreeView::branch:has-siblings:adjoins-item {\n"
            "        background: red;\n"
            "}\n"
            "\n"
            "QTreeView::branch:!has-children:!has-siblings:adjoins-item {\n"
            "        background: blue;\n"
            "}\n"
            "\n"
            "QTreeView::branch:closed:has-children:has-siblings {\n"
            "        background: pink;\n"
            "}\n"
            "\n"
            "QTreeView::branch:has-children:!has-siblings:closed {\n"
            "        background: gray;\n"
            "}\n"
            "\n"
            "QTreeView::branch:open:has-children:has-siblings {\n"
            "        background: magenta;\n"
            "}\n"
            "\n"
            "QTreeView::branch:open:has-children:!has-siblings {\n"
            "        background: green;\n"
            "}\n"
            "*/")
        self.view.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.view.setAlternatingRowColors(True)
        self.view.setIndentation(10)
        self.view.setRootIsDecorated(True)
        self.view.setUniformRowHeights(True)
        self.view.setSortingEnabled(False)
        self.view.setAnimated(False)
        self.view.setObjectName("view")
        self.gridLayout_6.addWidget(self.view, 3, 0, 1, 9)
        self.filter_daterange_btn = QtWidgets.QToolButton(self.snp_view_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.filter_daterange_btn.sizePolicy().hasHeightForWidth())
        self.filter_daterange_btn.setSizePolicy(sizePolicy)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/tm-icons/calendar.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.filter_daterange_btn.setIcon(icon3)
        self.filter_daterange_btn.setIconSize(QtCore.QSize(24, 24))
        self.filter_daterange_btn.setCheckable(True)
        self.filter_daterange_btn.setToolButtonStyle(
            QtCore.Qt.ToolButtonTextBesideIcon)
        self.filter_daterange_btn.setObjectName("filter_daterange_btn")
        self.gridLayout_6.addWidget(self.filter_daterange_btn, 0, 2, 1, 1)
        self.user_filter_hbox = QtWidgets.QHBoxLayout()
        self.user_filter_hbox.setSpacing(4)
        self.user_filter_hbox.setObjectName("user_filter_hbox")
        self.gridLayout_6.addLayout(self.user_filter_hbox, 0, 8, 1, 1)
        self.filter_daterange_dateEdit2 = QtWidgets.QDateEdit(
            self.snp_view_frame)
        self.filter_daterange_dateEdit2.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.filter_daterange_dateEdit2.sizePolicy().hasHeightForWidth())
        self.filter_daterange_dateEdit2.setSizePolicy(sizePolicy)
        self.filter_daterange_dateEdit2.setReadOnly(False)
        self.filter_daterange_dateEdit2.setMaximumDate(
            QtCore.QDate(2099, 12, 31))
        self.filter_daterange_dateEdit2.setMinimumDate(QtCore.QDate(
            2000, 1, 1))
        self.filter_daterange_dateEdit2.setCalendarPopup(False)
        self.filter_daterange_dateEdit2.setObjectName(
            "filter_daterange_dateEdit2")
        self.gridLayout_6.addWidget(self.filter_daterange_dateEdit2, 0, 5, 1,
                                    1)
        self.filter_daterange_dateEdit1 = QtWidgets.QDateEdit(
            self.snp_view_frame)
        self.filter_daterange_dateEdit1.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.filter_daterange_dateEdit1.sizePolicy().hasHeightForWidth())
        self.filter_daterange_dateEdit1.setSizePolicy(sizePolicy)
        self.filter_daterange_dateEdit1.setReadOnly(False)
        self.filter_daterange_dateEdit1.setMaximumDate(
            QtCore.QDate(2099, 12, 31))
        self.filter_daterange_dateEdit1.setMinimumDate(QtCore.QDate(
            2000, 1, 1))
        self.filter_daterange_dateEdit1.setCalendarPopup(False)
        self.filter_daterange_dateEdit1.setObjectName(
            "filter_daterange_dateEdit1")
        self.gridLayout_6.addWidget(self.filter_daterange_dateEdit1, 0, 3, 1,
                                    1)
        self.filter_note_btn = QtWidgets.QToolButton(self.snp_view_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.filter_note_btn.sizePolicy().hasHeightForWidth())
        self.filter_note_btn.setSizePolicy(sizePolicy)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/tm-icons/comment.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.filter_note_btn.setIcon(icon4)
        self.filter_note_btn.setIconSize(QtCore.QSize(24, 24))
        self.filter_note_btn.setCheckable(True)
        self.filter_note_btn.setChecked(False)
        self.filter_note_btn.setToolButtonStyle(
            QtCore.Qt.ToolButtonTextBesideIcon)
        self.filter_note_btn.setObjectName("filter_note_btn")
        self.gridLayout_6.addWidget(self.filter_note_btn, 0, 6, 1, 1)
        self.daterange_lbl = QtWidgets.QLabel(self.snp_view_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.daterange_lbl.sizePolicy().hasHeightForWidth())
        self.daterange_lbl.setSizePolicy(sizePolicy)
        self.daterange_lbl.setObjectName("daterange_lbl")
        self.gridLayout_6.addWidget(self.daterange_lbl, 0, 4, 1, 1)
        self.verticalLayout.addWidget(self.splitter_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "DataBase"))
        self.db_path_lineEdit.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>File path of the database.</p></body></html>"
            ))
        self.label_2.setText(_translate("Form", "Initial"))
        self.init_nitem_sbox.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Initially the number of showing items.</p></body></html>"
            ))
        self.init_nitem_sbox.setSuffix(_translate("Form", " Items"))
        self.fetched_nitem_lbl.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Total fetched items.</p></body></html>")
        )
        self.fetched_nitem_lbl.setText(_translate("Form", "0"))
        self.label_4.setText(_translate("Form", "/"))
        self.total_nitem_lbl.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Total items, with filters applied if any.</p></body></html>"
            ))
        self.total_nitem_lbl.setText(_translate("Form", "0"))
        self.db_open_btn.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Open or reload a database.</p></body></html>"
            ))
        self.db_open_btn.setText(_translate("Form", "Open"))
        self.select_invert_tags_btn.setToolTip(
            _translate("Form", "Invert the tag selection."))
        self.select_invert_tags_btn.setText(_translate("Form", "..."))
        self.select_none_tags_btn.setToolTip(
            _translate("Form", "Select none tags."))
        self.select_none_tags_btn.setText(_translate("Form", "Select None"))
        self.tag_filter_nitem_lbl.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Count of Snapshot items that match any of the checked tags.</p></body></html>"
            ))
        self.select_all_tags_btn.setToolTip(
            _translate("Form", "Select all tags."))
        self.select_all_tags_btn.setText(_translate("Form", "Select All"))
        self.select_none_ions_btn.setToolTip(
            _translate("Form", "Select none ions."))
        self.select_none_ions_btn.setText(_translate("Form", "Select None"))
        self.select_all_ions_btn.setToolTip(
            _translate("Form", "Select all ions."))
        self.select_all_ions_btn.setText(_translate("Form", "Select All"))
        self.select_invert_ions_btn.setToolTip(
            _translate("Form", "Invert the ion selections."))
        self.select_invert_ions_btn.setText(_translate("Form", "..."))
        self.ion_filter_nitem_lbl.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Count of Snapshot items that match any of the checked ions.</p></body></html>"
            ))
        self.filter_note_lineEdit.setToolTip(
            _translate("Form", "Ignore cases, loose wildcard match."))
        self.filter_daterange_btn.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Check to enable filtering on date range.</p></body></html>"
            ))
        self.filter_daterange_btn.setText(_translate("Form", "DateRange"))
        self.filter_daterange_dateEdit2.setDisplayFormat(
            _translate("Form", "yyyy-MM-dd"))
        self.filter_daterange_dateEdit1.setDisplayFormat(
            _translate("Form", "yyyy-MM-dd"))
        self.filter_note_btn.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Check to enable filtering on note string.</p></body></html>"
            ))
        self.filter_note_btn.setText(_translate("Form", "Note"))
        self.daterange_lbl.setText(_translate("Form", "To"))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
