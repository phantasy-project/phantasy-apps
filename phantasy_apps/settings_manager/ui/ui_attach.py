# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_attach.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1200, 800)
        Dialog.setStyleSheet(
            "QCheckBox::indicator {\n"
            "    width: 16px;\n"
            "    height: 16px;\n"
            "}\n"
            "QCheckBox::indicator::unchecked {\n"
            "    image: url(:/sm-icons/uncheck-square.png);\n"
            "}\n"
            "QCheckBox::indicator::checked {\n"
            "    image: url(:/sm-icons/check-square-fill.png);\n"
            "}\n"
            "QAbstractItemView::indicator::unchecked {\n"
            "    image: url(:/sm-icons/uncheck-square.png);\n"
            "}\n"
            "QAbstractItemView::indicator::checked {\n"
            "    image: url(:/sm-icons/check-square-fill.png);\n"
            "}")
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setContentsMargins(6, 8, 6, 6)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.nitem_lbl = QtWidgets.QLabel(Dialog)
        self.nitem_lbl.setStyleSheet("QLabel {\n"
                                     "    color: #007BFF;\n"
                                     "    font-family: monospace;\n"
                                     "}")
        self.nitem_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.nitem_lbl.setObjectName("nitem_lbl")
        self.horizontalLayout_4.addWidget(self.nitem_lbl)
        self.show_checked_btn = QtWidgets.QToolButton(Dialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/sm-icons/check-square-fill.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.show_checked_btn.setIcon(icon)
        self.show_checked_btn.setIconSize(QtCore.QSize(36, 36))
        self.show_checked_btn.setAutoRaise(True)
        self.show_checked_btn.setObjectName("show_checked_btn")
        self.horizontalLayout_4.addWidget(self.show_checked_btn)
        self.show_all_btn = QtWidgets.QToolButton(Dialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/sm-icons/all.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.show_all_btn.setIcon(icon1)
        self.show_all_btn.setIconSize(QtCore.QSize(36, 36))
        self.show_all_btn.setAutoRaise(True)
        self.show_all_btn.setObjectName("show_all_btn")
        self.horizontalLayout_4.addWidget(self.show_all_btn)
        self.gridLayout.addLayout(self.horizontalLayout_4, 4, 3, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.uri_type_cbb = QtWidgets.QComboBox(Dialog)
        self.uri_type_cbb.setIconSize(QtCore.QSize(32, 32))
        self.uri_type_cbb.setObjectName("uri_type_cbb")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/sm-icons/file.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.uri_type_cbb.addItem(icon2, "")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/sm-icons/hyperlink.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.uri_type_cbb.addItem(icon3, "")
        self.horizontalLayout_3.addWidget(self.uri_type_cbb)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.uri_name_lbl = QtWidgets.QLabel(Dialog)
        self.uri_name_lbl.setObjectName("uri_name_lbl")
        self.horizontalLayout_3.addWidget(self.uri_name_lbl)
        self.uri_name_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.uri_name_lineEdit.setObjectName("uri_name_lineEdit")
        self.horizontalLayout_3.addWidget(self.uri_name_lineEdit)
        self.gridLayout.addLayout(self.horizontalLayout_3, 3, 0, 1, 2)
        self.uri_path_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.uri_path_lineEdit.setReadOnly(False)
        self.uri_path_lineEdit.setObjectName("uri_path_lineEdit")
        self.gridLayout.addWidget(self.uri_path_lineEdit, 2, 1, 1, 1)
        self.attach_view = QtWidgets.QTableView(Dialog)
        self.attach_view.setStyleSheet(
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
        self.attach_view.setAlternatingRowColors(True)
        self.attach_view.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.attach_view.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.attach_view.setObjectName("attach_view")
        self.attach_view.horizontalHeader().setVisible(True)
        self.attach_view.horizontalHeader().setSortIndicatorShown(False)
        self.attach_view.horizontalHeader().setStretchLastSection(False)
        self.attach_view.verticalHeader().setVisible(True)
        self.gridLayout.addWidget(self.attach_view, 5, 0, 1, 4)
        self.browse_btn = QtWidgets.QPushButton(Dialog)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/sm-icons/browse.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.browse_btn.setIcon(icon4)
        self.browse_btn.setIconSize(QtCore.QSize(32, 32))
        self.browse_btn.setObjectName("browse_btn")
        self.gridLayout.addWidget(self.browse_btn, 2, 3, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.search_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.search_lineEdit.setObjectName("search_lineEdit")
        self.horizontalLayout_2.addWidget(self.search_lineEdit)
        self.search_btn = QtWidgets.QPushButton(Dialog)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/sm-icons/search.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search_btn.setIcon(icon5)
        self.search_btn.setIconSize(QtCore.QSize(32, 32))
        self.search_btn.setObjectName("search_btn")
        self.horizontalLayout_2.addWidget(self.search_btn)
        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 0, 1, 2)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_6 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("monospace")
        font.setPointSize(8)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("QLabel {\n"
                                   "    font-family: monospace;\n"
                                   "    font-size: 8pt;\n"
                                   "    color: #888A85;\n"
                                   "}")
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.snp_name_lbl = QtWidgets.QLabel(Dialog)
        self.snp_name_lbl.setStyleSheet("QLabel {\n"
                                        "    color: #1E88E5;\n"
                                        "    font-family: monospace;\n"
                                        "    font-weight: bold;\n"
                                        "    border-top: 0px solid gray;\n"
                                        "    border-bottom: 3px solid gray;\n"
                                        "}")
        self.snp_name_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.snp_name_lbl.setObjectName("snp_name_lbl")
        self.verticalLayout.addWidget(self.snp_name_lbl)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.upload_btn = QtWidgets.QPushButton(Dialog)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/sm-icons/expand.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.upload_btn.setIcon(icon6)
        self.upload_btn.setIconSize(QtCore.QSize(32, 32))
        self.upload_btn.setObjectName("upload_btn")
        self.horizontalLayout.addWidget(self.upload_btn)
        self.attach_after_upload_chkbox = QtWidgets.QCheckBox(Dialog)
        self.attach_after_upload_chkbox.setText("")
        self.attach_after_upload_chkbox.setObjectName(
            "attach_after_upload_chkbox")
        self.horizontalLayout.addWidget(self.attach_after_upload_chkbox)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 3, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.uri_path_lineEdit, self.browse_btn)
        Dialog.setTabOrder(self.browse_btn, self.uri_type_cbb)
        Dialog.setTabOrder(self.uri_type_cbb, self.uri_name_lineEdit)
        Dialog.setTabOrder(self.uri_name_lineEdit, self.search_lineEdit)
        Dialog.setTabOrder(self.search_lineEdit, self.search_btn)
        Dialog.setTabOrder(self.search_btn, self.show_checked_btn)
        Dialog.setTabOrder(self.show_checked_btn, self.show_all_btn)
        Dialog.setTabOrder(self.show_all_btn, self.attach_view)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.nitem_lbl.setToolTip(
            _translate(
                "Dialog",
                "<html><head/><body><p>The total number of listed attachments after applying filters.</p></body></html>"
            ))
        self.nitem_lbl.setText(_translate("Dialog", "0"))
        self.show_checked_btn.setToolTip(
            _translate(
                "Dialog",
                "<html><head/><body><p>Click to show only checked (attached) items.</p></body></html>"
            ))
        self.show_checked_btn.setText(_translate("Dialog", "Checked"))
        self.show_all_btn.setToolTip(
            _translate(
                "Dialog",
                "<html><head/><body><p>Click to show the attachment inventory.</p></body></html>"
            ))
        self.show_all_btn.setText(_translate("Dialog", "..."))
        self.label_2.setText(_translate("Dialog", "URI Type"))
        self.uri_type_cbb.setItemText(0, _translate("Dialog", "File"))
        self.uri_type_cbb.setItemText(1, _translate("Dialog", "URL"))
        self.uri_name_lbl.setText(_translate("Dialog", "Destination FilePath"))
        self.browse_btn.setText(_translate("Dialog", "Browse"))
        self.label_5.setText(
            _translate("Dialog", "Search the inventory to attach"))
        self.search_btn.setText(_translate("Dialog", "Search"))
        self.label.setText(_translate("Dialog", "Source FilePath"))
        self.label_6.setText(_translate("Dialog", "Snapshot"))
        self.snp_name_lbl.setText(_translate("Dialog", "ABC - 123Ar45(67+)"))
        self.upload_btn.setText(_translate("Dialog", "Upload"))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
