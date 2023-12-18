# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_snpdiff.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1204, 1578)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.title_lbl = QtWidgets.QLabel(Form)
        self.title_lbl.setStyleSheet("QLabel {    \n"
                                     "    border-top: 0px solid gray;\n"
                                     "    border-bottom: 3px solid gray;\n"
                                     "    padding-bottom: 6px;\n"
                                     "}")
        self.title_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.title_lbl.setObjectName("title_lbl")
        self.gridLayout.addWidget(self.title_lbl, 0, 0, 1, 2)
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.frame = QtWidgets.QFrame(self.splitter)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame.setStyleSheet("QFrame#frame {\n"
                                 "    border-top: 0px solid gray;\n"
                                 "    border-bottom: 3px solid gray;\n"
                                 "}")
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_4.setContentsMargins(0, 5, 0, 5)
        self.horizontalLayout_4.setSpacing(5)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.snp_one_gbox = QtWidgets.QGridLayout()
        self.snp_one_gbox.setContentsMargins(-1, 0, -1, -1)
        self.snp_one_gbox.setSpacing(5)
        self.snp_one_gbox.setObjectName("snp_one_gbox")
        self.note_one_vbox = QtWidgets.QVBoxLayout()
        self.note_one_vbox.setContentsMargins(-1, 0, -1, -1)
        self.note_one_vbox.setSpacing(0)
        self.note_one_vbox.setObjectName("note_one_vbox")
        self.note_one_title_lbl = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.note_one_title_lbl.sizePolicy().hasHeightForWidth())
        self.note_one_title_lbl.setSizePolicy(sizePolicy)
        self.note_one_title_lbl.setStyleSheet("QLabel {\n"
                                              "    font-family: monospace;\n"
                                              "    font-size: 8pt;\n"
                                              "    color: #888A85;\n"
                                              "}")
        self.note_one_title_lbl.setObjectName("note_one_title_lbl")
        self.note_one_vbox.addWidget(self.note_one_title_lbl)
        self.snp_one_note_plainTextEdit = QtWidgets.QPlainTextEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.snp_one_note_plainTextEdit.sizePolicy().hasHeightForWidth())
        self.snp_one_note_plainTextEdit.setSizePolicy(sizePolicy)
        self.snp_one_note_plainTextEdit.setReadOnly(True)
        self.snp_one_note_plainTextEdit.setObjectName(
            "snp_one_note_plainTextEdit")
        self.note_one_vbox.addWidget(self.snp_one_note_plainTextEdit)
        self.snp_one_gbox.addLayout(self.note_one_vbox, 4, 0, 1, 2)
        self.snp_one_title_lbl = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.snp_one_title_lbl.sizePolicy().hasHeightForWidth())
        self.snp_one_title_lbl.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("monospace")
        font.setPointSize(9)
        self.snp_one_title_lbl.setFont(font)
        self.snp_one_title_lbl.setStyleSheet("QLabel {\n"
                                             "    font-family: monospace;\n"
                                             "    font-size: 9pt;\n"
                                             "    color: #888A85;\n"
                                             "}")
        self.snp_one_title_lbl.setObjectName("snp_one_title_lbl")
        self.snp_one_gbox.addWidget(self.snp_one_title_lbl, 0, 0, 1, 2)
        self.snp_one_name_lbl = QtWidgets.QLabel(self.frame)
        self.snp_one_name_lbl.setStyleSheet("QLabel {\n"
                                            "    font-family: monospace;\n"
                                            "}")
        self.snp_one_name_lbl.setObjectName("snp_one_name_lbl")
        self.snp_one_gbox.addWidget(self.snp_one_name_lbl, 3, 0, 1, 1)
        self.snp_one_jump_btn = QtWidgets.QToolButton(self.frame)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/sm-icons/jump.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.snp_one_jump_btn.setIcon(icon)
        self.snp_one_jump_btn.setIconSize(QtCore.QSize(32, 32))
        self.snp_one_jump_btn.setAutoRaise(True)
        self.snp_one_jump_btn.setObjectName("snp_one_jump_btn")
        self.snp_one_gbox.addWidget(self.snp_one_jump_btn, 3, 1, 1, 1)
        self.snp_one_hbox = QtWidgets.QHBoxLayout()
        self.snp_one_hbox.setContentsMargins(-1, 0, 0, -1)
        self.snp_one_hbox.setSpacing(5)
        self.snp_one_hbox.setObjectName("snp_one_hbox")
        self.tag_one_vbox = QtWidgets.QVBoxLayout()
        self.tag_one_vbox.setContentsMargins(0, -1, -1, -1)
        self.tag_one_vbox.setSpacing(0)
        self.tag_one_vbox.setObjectName("tag_one_vbox")
        self.tag_one_title_lbl = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tag_one_title_lbl.sizePolicy().hasHeightForWidth())
        self.tag_one_title_lbl.setSizePolicy(sizePolicy)
        self.tag_one_title_lbl.setStyleSheet("QLabel {\n"
                                             "    font-family: monospace;\n"
                                             "    font-size: 8pt;\n"
                                             "    color: #888A85;\n"
                                             "}")
        self.tag_one_title_lbl.setObjectName("tag_one_title_lbl")
        self.tag_one_vbox.addWidget(self.tag_one_title_lbl)
        self.snp_one_tag_area = QtWidgets.QScrollArea(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.snp_one_tag_area.sizePolicy().hasHeightForWidth())
        self.snp_one_tag_area.setSizePolicy(sizePolicy)
        self.snp_one_tag_area.setWidgetResizable(True)
        self.snp_one_tag_area.setObjectName("snp_one_tag_area")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 453, 143))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.snp_one_tag_area.setWidget(self.scrollAreaWidgetContents)
        self.tag_one_vbox.addWidget(self.snp_one_tag_area)
        self.snp_one_hbox.addLayout(self.tag_one_vbox)
        self.ion_one_vbox = QtWidgets.QVBoxLayout()
        self.ion_one_vbox.setContentsMargins(-1, -1, 0, -1)
        self.ion_one_vbox.setSpacing(0)
        self.ion_one_vbox.setObjectName("ion_one_vbox")
        self.beam_one_title_lbl = QtWidgets.QLabel(self.frame)
        self.beam_one_title_lbl.setStyleSheet("QLabel {\n"
                                              "    font-family: monospace;\n"
                                              "    font-size: 8pt;\n"
                                              "    color: #888A85;\n"
                                              "}")
        self.beam_one_title_lbl.setObjectName("beam_one_title_lbl")
        self.ion_one_vbox.addWidget(self.beam_one_title_lbl)
        self.snp_one_pix = QtWidgets.QLabel(self.frame)
        self.snp_one_pix.setMinimumSize(QtCore.QSize(96, 96))
        self.snp_one_pix.setMaximumSize(QtCore.QSize(96, 96))
        self.snp_one_pix.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.snp_one_pix.setAlignment(QtCore.Qt.AlignLeading
                                      | QtCore.Qt.AlignLeft
                                      | QtCore.Qt.AlignVCenter)
        self.snp_one_pix.setObjectName("snp_one_pix")
        self.ion_one_vbox.addWidget(self.snp_one_pix)
        self.snp_one_isrc_name_lbl = QtWidgets.QLabel(self.frame)
        self.snp_one_isrc_name_lbl.setStyleSheet(
            "QLabel {\n"
            "    font-family: monospace;\n"
            "    font-size: 9pt;\n"
            "    border: 1px solid gray;\n"
            "}")
        self.snp_one_isrc_name_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.snp_one_isrc_name_lbl.setObjectName("snp_one_isrc_name_lbl")
        self.ion_one_vbox.addWidget(self.snp_one_isrc_name_lbl)
        self.snp_one_hbox.addLayout(self.ion_one_vbox)
        self.snp_one_gbox.addLayout(self.snp_one_hbox, 1, 0, 1, 2)
        self.horizontalLayout_4.addLayout(self.snp_one_gbox)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.swap_btn = QtWidgets.QToolButton(self.frame)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/sm-icons/swap_horiz.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.swap_btn.setIcon(icon1)
        self.swap_btn.setIconSize(QtCore.QSize(36, 36))
        self.swap_btn.setObjectName("swap_btn")
        self.horizontalLayout_4.addWidget(self.swap_btn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.snp_two_gbox = QtWidgets.QGridLayout()
        self.snp_two_gbox.setContentsMargins(-1, 0, 0, -1)
        self.snp_two_gbox.setSpacing(5)
        self.snp_two_gbox.setObjectName("snp_two_gbox")
        self.snp_two_name_lbl = QtWidgets.QLabel(self.frame)
        self.snp_two_name_lbl.setStyleSheet("QLabel {\n"
                                            "    font-family: monospace;\n"
                                            "}")
        self.snp_two_name_lbl.setObjectName("snp_two_name_lbl")
        self.snp_two_gbox.addWidget(self.snp_two_name_lbl, 2, 0, 1, 2)
        self.snp_two_jump_btn = QtWidgets.QToolButton(self.frame)
        self.snp_two_jump_btn.setIcon(icon)
        self.snp_two_jump_btn.setIconSize(QtCore.QSize(32, 32))
        self.snp_two_jump_btn.setAutoRaise(True)
        self.snp_two_jump_btn.setObjectName("snp_two_jump_btn")
        self.snp_two_gbox.addWidget(self.snp_two_jump_btn, 2, 2, 1, 1)
        self.note_two_vbox = QtWidgets.QVBoxLayout()
        self.note_two_vbox.setContentsMargins(-1, 0, -1, -1)
        self.note_two_vbox.setSpacing(0)
        self.note_two_vbox.setObjectName("note_two_vbox")
        self.note_two_title_lbl = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.note_two_title_lbl.sizePolicy().hasHeightForWidth())
        self.note_two_title_lbl.setSizePolicy(sizePolicy)
        self.note_two_title_lbl.setStyleSheet("QLabel {\n"
                                              "    font-family: monospace;\n"
                                              "    font-size: 8pt;\n"
                                              "    color: #888A85;\n"
                                              "}")
        self.note_two_title_lbl.setObjectName("note_two_title_lbl")
        self.note_two_vbox.addWidget(self.note_two_title_lbl)
        self.snp_two_note_plainTextEdit = QtWidgets.QPlainTextEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.snp_two_note_plainTextEdit.sizePolicy().hasHeightForWidth())
        self.snp_two_note_plainTextEdit.setSizePolicy(sizePolicy)
        self.snp_two_note_plainTextEdit.setReadOnly(True)
        self.snp_two_note_plainTextEdit.setObjectName(
            "snp_two_note_plainTextEdit")
        self.note_two_vbox.addWidget(self.snp_two_note_plainTextEdit)
        self.snp_two_gbox.addLayout(self.note_two_vbox, 3, 0, 1, 3)
        self.snp_two_hbox = QtWidgets.QHBoxLayout()
        self.snp_two_hbox.setContentsMargins(-1, 0, 0, -1)
        self.snp_two_hbox.setSpacing(5)
        self.snp_two_hbox.setObjectName("snp_two_hbox")
        self.tag_two_vbox = QtWidgets.QVBoxLayout()
        self.tag_two_vbox.setContentsMargins(0, -1, 0, -1)
        self.tag_two_vbox.setSpacing(0)
        self.tag_two_vbox.setObjectName("tag_two_vbox")
        self.tag_two_title_lbl = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tag_two_title_lbl.sizePolicy().hasHeightForWidth())
        self.tag_two_title_lbl.setSizePolicy(sizePolicy)
        self.tag_two_title_lbl.setStyleSheet("QLabel {\n"
                                             "    font-family: monospace;\n"
                                             "    font-size: 8pt;\n"
                                             "    color: #888A85;\n"
                                             "}")
        self.tag_two_title_lbl.setObjectName("tag_two_title_lbl")
        self.tag_two_vbox.addWidget(self.tag_two_title_lbl)
        self.snp_two_tag_area = QtWidgets.QScrollArea(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.snp_two_tag_area.sizePolicy().hasHeightForWidth())
        self.snp_two_tag_area.setSizePolicy(sizePolicy)
        self.snp_two_tag_area.setWidgetResizable(True)
        self.snp_two_tag_area.setObjectName("snp_two_tag_area")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(
            QtCore.QRect(0, 0, 453, 143))
        self.scrollAreaWidgetContents_2.setObjectName(
            "scrollAreaWidgetContents_2")
        self.snp_two_tag_area.setWidget(self.scrollAreaWidgetContents_2)
        self.tag_two_vbox.addWidget(self.snp_two_tag_area)
        self.snp_two_hbox.addLayout(self.tag_two_vbox)
        self.ion_two_vbox = QtWidgets.QVBoxLayout()
        self.ion_two_vbox.setContentsMargins(-1, -1, 0, -1)
        self.ion_two_vbox.setSpacing(0)
        self.ion_two_vbox.setObjectName("ion_two_vbox")
        self.beam_two_title_lbl = QtWidgets.QLabel(self.frame)
        self.beam_two_title_lbl.setStyleSheet("QLabel {\n"
                                              "    font-family: monospace;\n"
                                              "    font-size: 8pt;\n"
                                              "    color: #888A85;\n"
                                              "}")
        self.beam_two_title_lbl.setObjectName("beam_two_title_lbl")
        self.ion_two_vbox.addWidget(self.beam_two_title_lbl)
        self.snp_two_pix = QtWidgets.QLabel(self.frame)
        self.snp_two_pix.setMinimumSize(QtCore.QSize(96, 96))
        self.snp_two_pix.setMaximumSize(QtCore.QSize(96, 96))
        self.snp_two_pix.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.snp_two_pix.setObjectName("snp_two_pix")
        self.ion_two_vbox.addWidget(self.snp_two_pix)
        self.snp_two_isrc_name_lbl = QtWidgets.QLabel(self.frame)
        self.snp_two_isrc_name_lbl.setStyleSheet(
            "QLabel {\n"
            "    font-family: monospace;\n"
            "    font-size: 9pt;\n"
            "    border: 1px solid gray;\n"
            "}")
        self.snp_two_isrc_name_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.snp_two_isrc_name_lbl.setObjectName("snp_two_isrc_name_lbl")
        self.ion_two_vbox.addWidget(self.snp_two_isrc_name_lbl)
        self.snp_two_hbox.addLayout(self.ion_two_vbox)
        self.snp_two_gbox.addLayout(self.snp_two_hbox, 1, 0, 1, 3)
        self.snp_two_title_lbl = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.snp_two_title_lbl.sizePolicy().hasHeightForWidth())
        self.snp_two_title_lbl.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("monospace")
        font.setPointSize(9)
        self.snp_two_title_lbl.setFont(font)
        self.snp_two_title_lbl.setStyleSheet("QLabel {\n"
                                             "    font-family: monospace;\n"
                                             "    font-size: 9pt;\n"
                                             "    color: #888A85;\n"
                                             "}")
        self.snp_two_title_lbl.setObjectName("snp_two_title_lbl")
        self.snp_two_gbox.addWidget(self.snp_two_title_lbl, 0, 0, 1, 3)
        self.horizontalLayout_4.addLayout(self.snp_two_gbox)
        self.snpdiffView = QtWidgets.QTableView(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.snpdiffView.sizePolicy().hasHeightForWidth())
        self.snpdiffView.setSizePolicy(sizePolicy)
        self.snpdiffView.setStyleSheet(
            "QHeaderView {\n"
            "    font-weight: bold;\n"
            "}\n"
            "QTableView {\n"
            "    font-family: monospace;\n"
            "    show-decoration-selected: 1;\n"
            "}\n"
            "QTableView::item {\n"
            "    border: 1px solid #D9D9D9;\n"
            "    border-top-color: transparent;\n"
            "    border-bottom-color: transparent;\n"
            "}\n"
            "QTableView::item:hover {\n"
            "    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);\n"
            "    border: 1px solid #bfcde4;\n"
            "}\n"
            "QTableView::item:selected {\n"
            "    border: 1px solid #567DBC;\n"
            "    background-color: #D3D7CF;\n"
            "}\n"
            "QTableView::item:selected:active{\n"
            "    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);\n"
            "}\n"
            "\n"
            "")
        self.snpdiffView.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.snpdiffView.setAlternatingRowColors(True)
        self.snpdiffView.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.snpdiffView.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.snpdiffView.setObjectName("snpdiffView")
        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 2)
        self.diff_gbox = QtWidgets.QGroupBox(Form)
        self.diff_gbox.setObjectName("diff_gbox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.diff_gbox)
        self.gridLayout_2.setContentsMargins(6, 12, 6, 6)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.absdiff_lineEdit = QtWidgets.QLineEdit(self.diff_gbox)
        self.absdiff_lineEdit.setObjectName("absdiff_lineEdit")
        self.gridLayout_2.addWidget(self.absdiff_lineEdit, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.diff_gbox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 1, 1, 1)
        self.enable_absdiff_rbtn = QtWidgets.QRadioButton(self.diff_gbox)
        self.enable_absdiff_rbtn.setObjectName("enable_absdiff_rbtn")
        self.diff_level_rgrp = QtWidgets.QButtonGroup(Form)
        self.diff_level_rgrp.setObjectName("diff_level_rgrp")
        self.diff_level_rgrp.addButton(self.enable_absdiff_rbtn)
        self.gridLayout_2.addWidget(self.enable_absdiff_rbtn, 1, 0, 1, 1)
        self.reldiff_sbox = QtWidgets.QDoubleSpinBox(self.diff_gbox)
        self.reldiff_sbox.setMinimum(0.0)
        self.reldiff_sbox.setSingleStep(0.1)
        self.reldiff_sbox.setProperty("value", 0.0)
        self.reldiff_sbox.setObjectName("reldiff_sbox")
        self.gridLayout_2.addWidget(self.reldiff_sbox, 2, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.diff_gbox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 1, 1, 1)
        self.enable_reldiff_rbtn = QtWidgets.QRadioButton(self.diff_gbox)
        self.enable_reldiff_rbtn.setObjectName("enable_reldiff_rbtn")
        self.diff_level_rgrp.addButton(self.enable_reldiff_rbtn)
        self.gridLayout_2.addWidget(self.enable_reldiff_rbtn, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.diff_gbox, 2, 0, 1, 1)
        self.filter_gbox = QtWidgets.QGroupBox(Form)
        self.filter_gbox.setObjectName("filter_gbox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.filter_gbox)
        self.gridLayout_3.setContentsMargins(6, 12, 6, 6)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.show_outrange_rbtn = QtWidgets.QRadioButton(self.filter_gbox)
        self.show_outrange_rbtn.setObjectName("show_outrange_rbtn")
        self.show_opt_rgrp = QtWidgets.QButtonGroup(Form)
        self.show_opt_rgrp.setObjectName("show_opt_rgrp")
        self.show_opt_rgrp.addButton(self.show_outrange_rbtn)
        self.gridLayout_3.addWidget(self.show_outrange_rbtn, 0, 0, 1, 1)
        self.show_inrange_rbtn = QtWidgets.QRadioButton(self.filter_gbox)
        self.show_inrange_rbtn.setObjectName("show_inrange_rbtn")
        self.show_opt_rgrp.addButton(self.show_inrange_rbtn)
        self.gridLayout_3.addWidget(self.show_inrange_rbtn, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.filter_gbox, 2, 1, 1, 1)
        self.cmd_hbox = QtWidgets.QHBoxLayout()
        self.cmd_hbox.setContentsMargins(0, 0, -1, -1)
        self.cmd_hbox.setSpacing(6)
        self.cmd_hbox.setObjectName("cmd_hbox")
        self.read_csv_btn = QtWidgets.QPushButton(Form)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/sm-icons/csv.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.read_csv_btn.setIcon(icon2)
        self.read_csv_btn.setIconSize(QtCore.QSize(48, 48))
        self.read_csv_btn.setObjectName("read_csv_btn")
        self.cmd_hbox.addWidget(self.read_csv_btn)
        self.screenshot_btn = QtWidgets.QPushButton(Form)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/sm-icons/capture.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.screenshot_btn.setIcon(icon3)
        self.screenshot_btn.setIconSize(QtCore.QSize(48, 48))
        self.screenshot_btn.setObjectName("screenshot_btn")
        self.cmd_hbox.addWidget(self.screenshot_btn)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.cmd_hbox.addItem(spacerItem2)
        self.exit_btn = QtWidgets.QPushButton(Form)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/sm-icons/exit.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exit_btn.setIcon(icon4)
        self.exit_btn.setIconSize(QtCore.QSize(48, 48))
        self.exit_btn.setObjectName("exit_btn")
        self.cmd_hbox.addWidget(self.exit_btn)
        self.gridLayout.addLayout(self.cmd_hbox, 3, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.title_lbl.setText(
            _translate("Form", "<h2>Compare Two Snapshots</h2>"))
        self.note_one_title_lbl.setText(_translate("Form", "Note"))
        self.snp_one_title_lbl.setText(_translate("Form", "Snapshot 1"))
        self.snp_one_name_lbl.setText(
            _translate("Form", "2023-12-13T01:49:41 - 86Kr36(19+)"))
        self.snp_one_jump_btn.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Locate in the main database.</p></body></html>"
            ))
        self.snp_one_jump_btn.setText(_translate("Form", "..."))
        self.tag_one_title_lbl.setText(_translate("Form", "Tags"))
        self.beam_one_title_lbl.setText(_translate("Form", "Beam"))
        self.snp_one_pix.setText(_translate("Form", "Kr"))
        self.snp_one_isrc_name_lbl.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Ion source in use</p></body></html>"))
        self.snp_one_isrc_name_lbl.setText(_translate("Form", "isrc"))
        self.swap_btn.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Swap: Snapshot 1 to 2, 2 to 1.</p></body></html>"
            ))
        self.swap_btn.setText(_translate("Form", "..."))
        self.snp_two_name_lbl.setText(
            _translate("Form", "2023-12-13T01:49:41 - 86Kr36(19+)"))
        self.snp_two_jump_btn.setText(_translate("Form", "..."))
        self.note_two_title_lbl.setText(_translate("Form", "Note"))
        self.tag_two_title_lbl.setText(_translate("Form", "Tags"))
        self.beam_two_title_lbl.setText(_translate("Form", "Beam"))
        self.snp_two_pix.setText(_translate("Form", "Kr"))
        self.snp_two_isrc_name_lbl.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Ion source in use</p></body></html>"))
        self.snp_two_isrc_name_lbl.setText(_translate("Form", "isrc"))
        self.snp_two_title_lbl.setText(_translate("Form", "Snapshot 2"))
        self.diff_gbox.setTitle(_translate("Form", "Discrenpancy Level"))
        self.absdiff_lineEdit.setText(_translate("Form", "0"))
        self.label_3.setText(
            _translate(
                "Form",
                "<html><head/><body><p>|x<span style=\" vertical-align:sub;\">0</span>-y<span style=\" vertical-align:sub;\">0</span>|</p></body></html>"
            ))
        self.enable_absdiff_rbtn.setText(_translate("Form",
                                                    "By absolute diff"))
        self.reldiff_sbox.setSuffix(_translate("Form", " %"))
        self.label_2.setText(
            _translate(
                "Form",
                "<html><head/><body><p>|(x<span style=\" vertical-align:sub;\">0</span>-y<span style=\" vertical-align:sub;\">0</span>)/y<span style=\" vertical-align:sub;\">0</span>|</p></body></html>"
            ))
        self.enable_reldiff_rbtn.setText(_translate("Form",
                                                    "By relative diff"))
        self.filter_gbox.setTitle(_translate("Form", "Filters"))
        self.show_outrange_rbtn.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Show items beyond defined discrenpancy level.</p></body></html>"
            ))
        self.show_outrange_rbtn.setText(
            _translate("Form",
                       "Beyond diff range: Settings are \"Different\""))
        self.show_inrange_rbtn.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Show items within defined discrenpancy level.</p></body></html>"
            ))
        self.show_inrange_rbtn.setText(
            _translate("Form", "Within diff range: Settings are \"Same\""))
        self.read_csv_btn.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Read the data in the spreadsheet app.</p></body></html>"
            ))
        self.read_csv_btn.setText(_translate("Form", "Read"))
        self.screenshot_btn.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Capture screenshot to a file and for paste anywhere.</p></body></html>"
            ))
        self.screenshot_btn.setText(_translate("Form", "Capture"))
        self.exit_btn.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Exit the snapshot diff window.</p></body></html>"
            ))
        self.exit_btn.setText(_translate("Form", "Exit"))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())