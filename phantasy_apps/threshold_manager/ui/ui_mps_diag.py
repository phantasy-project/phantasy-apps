# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mps_diag.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1516, 676)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.view = QtWidgets.QTreeView(Form)
        self.view.setStyleSheet(
            "QHeaderView {\n"
            "    qproperty-defaultAlignment: AlignHCenter AlignVCenter;\n"
            "    font-weight: bold;\n"
            "}\n"
            "\n"
            "QTreeView {\n"
            "    font-family: monospace;\n"
            "    show-decoration-selected: 1;\n"
            "    alternate-background-color: #D3D7CF;\n"
            "}\n"
            "\n"
            "QTreeView::item {\n"
            "    /*color: black;*/\n"
            "    border: 1px solid #D9D9D9;\n"
            "    border-top-color: transparent;\n"
            "    border-bottom-color: transparent;\n"
            "}\n"
            "\n"
            "QTreeView::item:hover {\n"
            "    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);\n"
            "    border: 1px solid #bfcde4;\n"
            "}\n"
            "\n"
            "QTreeView::item:selected {\n"
            "    border: 1px solid #567DBC;\n"
            "    background-color: #D3D7CF;\n"
            "}\n"
            "\n"
            "QTreeView::item:selected:active{\n"
            "    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);\n"
            "}")
        self.view.setIndentation(10)
        self.view.setUniformRowHeights(True)
        self.view.setObjectName("view")
        self.gridLayout.addWidget(self.view, 2, 0, 1, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.refresh_sts_lbl = QtWidgets.QLabel(Form)
        self.refresh_sts_lbl.setText("")
        self.refresh_sts_lbl.setObjectName("refresh_sts_lbl")
        self.horizontalLayout.addWidget(self.refresh_sts_lbl)
        self.auto_width_btn = QtWidgets.QToolButton(Form)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/tm-icons/resize-horizontal.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.auto_width_btn.setIcon(icon)
        self.auto_width_btn.setIconSize(QtCore.QSize(32, 32))
        self.auto_width_btn.setAutoRaise(True)
        self.auto_width_btn.setObjectName("auto_width_btn")
        self.horizontalLayout.addWidget(self.auto_width_btn)
        self.saveas_btn = QtWidgets.QPushButton(Form)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/tm-icons/save.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveas_btn.setIcon(icon1)
        self.saveas_btn.setIconSize(QtCore.QSize(32, 32))
        self.saveas_btn.setObjectName("saveas_btn")
        self.horizontalLayout.addWidget(self.saveas_btn)
        self.reset_diff_btn = QtWidgets.QPushButton(Form)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/tm-icons/clear.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reset_diff_btn.setIcon(icon2)
        self.reset_diff_btn.setIconSize(QtCore.QSize(32, 32))
        self.reset_diff_btn.setObjectName("reset_diff_btn")
        self.horizontalLayout.addWidget(self.reset_diff_btn)
        self.diff_type_lbl = QtWidgets.QLabel(Form)
        self.diff_type_lbl.setText("")
        self.diff_type_lbl.setObjectName("diff_type_lbl")
        self.horizontalLayout.addWidget(self.diff_type_lbl)
        self.ref_datafilepath_lbl = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ref_datafilepath_lbl.sizePolicy().hasHeightForWidth())
        self.ref_datafilepath_lbl.setSizePolicy(sizePolicy)
        self.ref_datafilepath_lbl.setMinimumSize(QtCore.QSize(700, 0))
        self.ref_datafilepath_lbl.setStyleSheet("QLabel {\n"
                                                "    background: white;\n"
                                                "    border: 1px solid gray;\n"
                                                "}")
        self.ref_datafilepath_lbl.setText("")
        self.ref_datafilepath_lbl.setScaledContents(False)
        self.ref_datafilepath_lbl.setWordWrap(False)
        self.ref_datafilepath_lbl.setTextInteractionFlags(
            QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse)
        self.ref_datafilepath_lbl.setObjectName("ref_datafilepath_lbl")
        self.horizontalLayout.addWidget(self.ref_datafilepath_lbl)
        self.snp_locate_btn = QtWidgets.QToolButton(Form)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/tm-icons/locate.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.snp_locate_btn.setIcon(icon3)
        self.snp_locate_btn.setIconSize(QtCore.QSize(32, 32))
        self.snp_locate_btn.setObjectName("snp_locate_btn")
        self.horizontalLayout.addWidget(self.snp_locate_btn)
        self.diff_help_btn = QtWidgets.QToolButton(Form)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/tm-icons/new.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.diff_help_btn.setIcon(icon4)
        self.diff_help_btn.setIconSize(QtCore.QSize(32, 32))
        self.diff_help_btn.setAutoRaise(True)
        self.diff_help_btn.setObjectName("diff_help_btn")
        self.horizontalLayout.addWidget(self.diff_help_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.refresh_btn = QtWidgets.QPushButton(Form)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/tm-icons/start.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refresh_btn.setIcon(icon5)
        self.refresh_btn.setIconSize(QtCore.QSize(32, 32))
        self.refresh_btn.setCheckable(True)
        self.refresh_btn.setObjectName("refresh_btn")
        self.horizontalLayout.addWidget(self.refresh_btn)
        self.refresh_rate_dsbox = QtWidgets.QDoubleSpinBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.refresh_rate_dsbox.sizePolicy().hasHeightForWidth())
        self.refresh_rate_dsbox.setSizePolicy(sizePolicy)
        self.refresh_rate_dsbox.setDecimals(0)
        self.refresh_rate_dsbox.setMinimum(1.0)
        self.refresh_rate_dsbox.setMaximum(5.0)
        self.refresh_rate_dsbox.setProperty("value", 1.0)
        self.refresh_rate_dsbox.setObjectName("refresh_rate_dsbox")
        self.horizontalLayout.addWidget(self.refresh_rate_dsbox)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setStyleSheet("QLabel {\n"
                                 "    margin-bottom: 10px;\n"
                                 "}")
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.dtype_lbl = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.dtype_lbl.sizePolicy().hasHeightForWidth())
        self.dtype_lbl.setSizePolicy(sizePolicy)
        self.dtype_lbl.setStyleSheet("QLabel {\n"
                                     "    margin-left: 20px;\n"
                                     "    margin-bottom: 10px;\n"
                                     "}")
        self.dtype_lbl.setAlignment(QtCore.Qt.AlignLeading
                                    | QtCore.Qt.AlignLeft
                                    | QtCore.Qt.AlignVCenter)
        self.dtype_lbl.setObjectName("dtype_lbl")
        self.horizontalLayout_2.addWidget(self.dtype_lbl)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 2)

        self.retranslateUi(Form)
        self.auto_width_btn.clicked.connect(
            Form.auto_resize_columns)  # type: ignore
        self.refresh_btn.toggled['bool'].connect(
            Form.refreshData)  # type: ignore
        self.reset_diff_btn.clicked.connect(Form.clearDiff)  # type: ignore
        self.diff_help_btn.clicked.connect(Form.onHelpDiffMode)  # type: ignore
        self.saveas_btn.clicked.connect(Form.saveData)  # type: ignore
        self.snp_locate_btn.clicked.connect(Form.onLocateSnp)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.auto_width_btn.setToolTip(
            _translate("Form", "Auto adjust column width."))
        self.auto_width_btn.setText(_translate("Form", "Auto Width"))
        self.saveas_btn.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Capture the snasphot to the database.</p></body></html>"
            ))
        self.saveas_btn.setText(_translate("Form", "Save"))
        self.reset_diff_btn.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Reset comparison.</p></body></html>"))
        self.reset_diff_btn.setText(_translate("Form", "Reset-Diff"))
        self.snp_locate_btn.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Click to locate the loaded snapshot in the Snapshot Window.</p></body></html>"
            ))
        self.snp_locate_btn.setText(_translate("Form", "..."))
        self.diff_help_btn.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Click to see the details for diff mode.</p></body></html>"
            ))
        self.diff_help_btn.setText(_translate("Form", "..."))
        self.refresh_btn.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Check to active auto data refreshing, uncheck to stop.</p></body></html>"
            ))
        self.refresh_btn.setText(_translate("Form", "Refresh"))
        self.refresh_rate_dsbox.setSuffix(_translate("Form", " Hz"))
        self.label.setText(
            _translate(
                "Form",
                "<html><head/><body><p><span style=\" font-size:18pt;\">Read-Only Diagnostic MPS Threshold Configurations</span></p></body></html>"
            ))
        self.dtype_lbl.setText(
            _translate(
                "Form",
                "<html><head/><body><p><span style=\" font-size:18pt; font-weight:600; color:#0055ff;\">Device Type</span></p></body></html>"
            ))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
