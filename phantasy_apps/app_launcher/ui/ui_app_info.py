# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_app_info.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InfoForm(object):
    def setupUi(self, InfoForm):
        InfoForm.setObjectName("InfoForm")
        InfoForm.resize(1047, 290)
        InfoForm.setStyleSheet("QWidget#InfoForm {\n"
                               "    border: 2px solid #04B13B;\n"
                               "}")
        self.gridLayout_2 = QtWidgets.QGridLayout(InfoForm)
        self.gridLayout_2.setContentsMargins(2, 1, 2, 6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.desc_plainTextEdit = QtWidgets.QPlainTextEdit(InfoForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.desc_plainTextEdit.sizePolicy().hasHeightForWidth())
        self.desc_plainTextEdit.setSizePolicy(sizePolicy)
        self.desc_plainTextEdit.setStyleSheet("QPlainTextEdit {\n"
                                              "    font-size: 15pt;\n"
                                              "    font-family: monospace;\n"
                                              "    /*border: none;*/\n"
                                              "    margin-bottom: 6px;\n"
                                              "    margin-right: 6px;\n"
                                              "}")
        self.desc_plainTextEdit.setReadOnly(True)
        self.desc_plainTextEdit.setObjectName("desc_plainTextEdit")
        self.gridLayout_2.addWidget(self.desc_plainTextEdit, 4, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(InfoForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setStyleSheet("QLabel {\n"
                                   "    font-size: 14px;\n"
                                   "    font-weight: bold;\n"
                                   "}")
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 1, 1, 1, 1)
        self.headline_widget = QtWidgets.QWidget(InfoForm)
        self.headline_widget.setStyleSheet(
            "QWidget {\n"
            "    background-color: rgb(4, 177, 59);\n"
            "}")
        self.headline_widget.setObjectName("headline_widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.headline_widget)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.app_name = QtWidgets.QLabel(self.headline_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.app_name.sizePolicy().hasHeightForWidth())
        self.app_name.setSizePolicy(sizePolicy)
        self.app_name.setStyleSheet("QLabel {\n"
                                    "    margin-left: 0px;\n"
                                    "    color: white;\n"
                                    "    font-size: 20pt;\n"
                                    "    font-weight: bold;\n"
                                    "}")
        self.app_name.setObjectName("app_name")
        self.horizontalLayout.addWidget(self.app_name)
        self.app_main_group = QtWidgets.QLabel(self.headline_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.app_main_group.sizePolicy().hasHeightForWidth())
        self.app_main_group.setSizePolicy(sizePolicy)
        self.app_main_group.setStyleSheet("QLabel {\n"
                                          "    margin-left: 0px;\n"
                                          "    color: white;\n"
                                          "    font-size: 16pt;\n"
                                          "}")
        self.app_main_group.setObjectName("app_main_group")
        self.horizontalLayout.addWidget(self.app_main_group)
        self.helpdoc_btn = QtWidgets.QToolButton(self.headline_widget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/helpdoc.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.helpdoc_btn.setIcon(icon)
        self.helpdoc_btn.setIconSize(QtCore.QSize(32, 32))
        self.helpdoc_btn.setAutoRaise(True)
        self.helpdoc_btn.setObjectName("helpdoc_btn")
        self.horizontalLayout.addWidget(self.helpdoc_btn)
        self.close_btn = QtWidgets.QToolButton(self.headline_widget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/close.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.close_btn.setIcon(icon1)
        self.close_btn.setIconSize(QtCore.QSize(32, 32))
        self.close_btn.setAutoRaise(True)
        self.close_btn.setObjectName("close_btn")
        self.horizontalLayout.addWidget(self.close_btn)
        self.gridLayout_2.addWidget(self.headline_widget, 0, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(InfoForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setStyleSheet("QLabel {\n"
                                   "    font-weight: bold;\n"
                                   "    margin-left: 10px;\n"
                                   "    font-size: 14px;\n"
                                   "}")
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.contact_lbl = QtWidgets.QLabel(InfoForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.contact_lbl.sizePolicy().hasHeightForWidth())
        self.contact_lbl.setSizePolicy(sizePolicy)
        self.contact_lbl.setStyleSheet("QLabel {\n"
                                       "    margin-left: 0px;\n"
                                       "    font-size: 12px;\n"
                                       "}")
        self.contact_lbl.setObjectName("contact_lbl")
        self.horizontalLayout_2.addWidget(self.contact_lbl)
        self.contact_name_lbl = QtWidgets.QLabel(InfoForm)
        self.contact_name_lbl.setStyleSheet("QLabel {\n"
                                            "    margin-left: 10px;\n"
                                            "}")
        self.contact_name_lbl.setObjectName("contact_name_lbl")
        self.horizontalLayout_2.addWidget(self.contact_name_lbl)
        self.contact_phone_lbl = QtWidgets.QLabel(InfoForm)
        self.contact_phone_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.contact_phone_lbl.setObjectName("contact_phone_lbl")
        self.horizontalLayout_2.addWidget(self.contact_phone_lbl)
        self.contact_email_lbl = QtWidgets.QLabel(InfoForm)
        self.contact_email_lbl.setStyleSheet("QLabel {\n"
                                             "    margin-right: 6px;\n"
                                             "}")
        self.contact_email_lbl.setAlignment(QtCore.Qt.AlignRight
                                            | QtCore.Qt.AlignTrailing
                                            | QtCore.Qt.AlignVCenter)
        self.contact_email_lbl.setOpenExternalLinks(True)
        self.contact_email_lbl.setObjectName("contact_email_lbl")
        self.horizontalLayout_2.addWidget(self.contact_email_lbl)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 5, 1, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(10, 0, -1, 6)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.open_btn = QtWidgets.QToolButton(InfoForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.open_btn.sizePolicy().hasHeightForWidth())
        self.open_btn.setSizePolicy(sizePolicy)
        self.open_btn.setStyleSheet("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/run.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.open_btn.setIcon(icon2)
        self.open_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.open_btn.setAutoRaise(True)
        self.open_btn.setObjectName("open_btn")
        self.verticalLayout_2.addWidget(self.open_btn)
        self.open_in_terminal_btn = QtWidgets.QToolButton(InfoForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.open_in_terminal_btn.sizePolicy().hasHeightForWidth())
        self.open_in_terminal_btn.setSizePolicy(sizePolicy)
        self.open_in_terminal_btn.setStyleSheet("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/app-icons/app-icons/console.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.open_in_terminal_btn.setIcon(icon3)
        self.open_in_terminal_btn.setCheckable(False)
        self.open_in_terminal_btn.setToolButtonStyle(
            QtCore.Qt.ToolButtonTextBesideIcon)
        self.open_in_terminal_btn.setAutoRaise(True)
        self.open_in_terminal_btn.setObjectName("open_in_terminal_btn")
        self.verticalLayout_2.addWidget(self.open_in_terminal_btn)
        self.fav_btn = QtWidgets.QToolButton(InfoForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.fav_btn.sizePolicy().hasHeightForWidth())
        self.fav_btn.setSizePolicy(sizePolicy)
        self.fav_btn.setStyleSheet("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/fav-off-action.svg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon4.addPixmap(QtGui.QPixmap(":/icons/fav-on-action.svg"),
                        QtGui.QIcon.Active, QtGui.QIcon.On)
        self.fav_btn.setIcon(icon4)
        self.fav_btn.setCheckable(True)
        self.fav_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.fav_btn.setAutoRaise(True)
        self.fav_btn.setObjectName("fav_btn")
        self.verticalLayout_2.addWidget(self.fav_btn)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 4, 0, 1, 1)
        self.label_3.raise_()
        self.label_7.raise_()
        self.headline_widget.raise_()
        self.desc_plainTextEdit.raise_()

        self.retranslateUi(InfoForm)
        self.close_btn.clicked.connect(InfoForm.on_close)
        self.open_in_terminal_btn.clicked.connect(
            InfoForm.on_run_app_in_terminal)
        self.open_btn.clicked.connect(InfoForm.on_run_app)
        self.fav_btn.toggled['bool'].connect(InfoForm.on_toggle_fav)
        QtCore.QMetaObject.connectSlotsByName(InfoForm)

    def retranslateUi(self, InfoForm):
        _translate = QtCore.QCoreApplication.translate
        InfoForm.setWindowTitle(_translate("InfoForm", "Form"))
        self.label_7.setText(
            _translate(
                "InfoForm",
                "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Descriptions:</span></p></body></html>"
            ))
        self.app_name.setText(
            _translate("InfoForm",
                       "<html><head/><body><p>App Name</p></body></html>"))
        self.app_main_group.setText(
            _translate(
                "InfoForm",
                "<html><head/><body><p><span style=\" font-size:16pt; color:#ffffff;\">App Main Group Name</span></p></body></html>"
            ))
        self.helpdoc_btn.setText(_translate("InfoForm", "help"))
        self.close_btn.setText(_translate("InfoForm", "..."))
        self.label_3.setText(
            _translate(
                "InfoForm",
                "<html><head/><body><p><span style=\" font-size:14pt;\">Actions:</span></p></body></html>"
            ))
        self.contact_lbl.setText(
            _translate(
                "InfoForm",
                "<html><head/><body><p><span style=\" font-size:14pt;\">Contact:</span></p></body></html>"
            ))
        self.contact_name_lbl.setText(_translate("InfoForm", "name"))
        self.contact_phone_lbl.setText(_translate("InfoForm", "phone"))
        self.contact_email_lbl.setText(_translate("InfoForm", "email"))
        self.open_btn.setText(_translate("InfoForm", "Open"))
        self.open_in_terminal_btn.setText(
            _translate("InfoForm", "Open in Terminal"))
        self.fav_btn.setText(_translate("InfoForm", "Add to Favorites"))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    InfoForm = QtWidgets.QWidget()
    ui = Ui_InfoForm()
    ui.setupUi(InfoForm)
    InfoForm.show()
    sys.exit(app.exec_())
