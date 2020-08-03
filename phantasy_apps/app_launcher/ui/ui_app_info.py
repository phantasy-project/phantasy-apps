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
        InfoForm.resize(968, 260)
        InfoForm.setStyleSheet("QWidget#InfoForm {\n"
                               "    border: 2px solid #04B13B;\n"
                               "}")
        self.gridLayout_2 = QtWidgets.QGridLayout(InfoForm)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.widget = QtWidgets.QWidget(InfoForm)
        self.widget.setStyleSheet("QWidget {\n"
                                  "    background-color: rgb(4, 177, 59);\n"
                                  "}")
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.app_name = QtWidgets.QLabel(self.widget)
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
        self.app_main_group = QtWidgets.QLabel(self.widget)
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
        self.gridLayout_2.addWidget(self.widget, 0, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(InfoForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(InfoForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 1, 1, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.open_btn = QtWidgets.QToolButton(InfoForm)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/run.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.open_btn.setIcon(icon)
        self.open_btn.setIconSize(QtCore.QSize(32, 32))
        self.open_btn.setAutoRaise(True)
        self.open_btn.setObjectName("open_btn")
        self.gridLayout.addWidget(self.open_btn, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(InfoForm)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 1, 1, 1)
        self.open_in_terminal_btn = QtWidgets.QToolButton(InfoForm)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/console.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.open_in_terminal_btn.setIcon(icon1)
        self.open_in_terminal_btn.setIconSize(QtCore.QSize(32, 32))
        self.open_in_terminal_btn.setCheckable(False)
        self.open_in_terminal_btn.setAutoRaise(True)
        self.open_in_terminal_btn.setObjectName("open_in_terminal_btn")
        self.gridLayout.addWidget(self.open_in_terminal_btn, 1, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(InfoForm)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 1, 1, 1)
        self.fav_btn = QtWidgets.QToolButton(InfoForm)
        self.fav_btn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/fav-off-action.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(":/icons/fav-on-action.png"),
                        QtGui.QIcon.Active, QtGui.QIcon.On)
        icon2.addPixmap(QtGui.QPixmap(":/icons/fav-on-action.png"),
                        QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.fav_btn.setIcon(icon2)
        self.fav_btn.setIconSize(QtCore.QSize(32, 32))
        self.fav_btn.setCheckable(True)
        self.fav_btn.setAutoRaise(True)
        self.fav_btn.setObjectName("fav_btn")
        self.gridLayout.addWidget(self.fav_btn, 2, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(InfoForm)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 1)
        self.desc_plainTextEdit = QtWidgets.QPlainTextEdit(InfoForm)
        self.desc_plainTextEdit.setStyleSheet("QPlainTextEdit {\n"
                                              "    font-size: 12pt;\n"
                                              "}")
        self.desc_plainTextEdit.setObjectName("desc_plainTextEdit")
        self.gridLayout_2.addWidget(self.desc_plainTextEdit, 2, 1, 1, 1)

        self.retranslateUi(InfoForm)
        self.fav_btn.toggled['bool'].connect(InfoForm.on_toggle_fav)
        self.open_btn.clicked.connect(InfoForm.on_run_app)
        self.open_in_terminal_btn.clicked.connect(
            InfoForm.on_run_app_in_terminal)
        QtCore.QMetaObject.connectSlotsByName(InfoForm)

    def retranslateUi(self, InfoForm):
        _translate = QtCore.QCoreApplication.translate
        InfoForm.setWindowTitle(_translate("InfoForm", "Form"))
        self.app_name.setText(
            _translate("InfoForm",
                       "<html><head/><body><p>App Name</p></body></html>"))
        self.app_main_group.setText(
            _translate(
                "InfoForm",
                "<html><head/><body><p><span style=\" font-size:16pt; color:#ffffff;\">App Main Group Name</span></p></body></html>"
            ))
        self.label_3.setText(
            _translate(
                "InfoForm",
                "<html><head/><body><p><span style=\" font-size:14pt;\">Actions:</span></p></body></html>"
            ))
        self.label_7.setText(
            _translate(
                "InfoForm",
                "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Descriptions:</span></p></body></html>"
            ))
        self.open_btn.setText(_translate("InfoForm", "..."))
        self.label_4.setText(_translate("InfoForm", "Open"))
        self.open_in_terminal_btn.setText(_translate("InfoForm", "..."))
        self.label_5.setText(_translate("InfoForm", "Open in Terminal"))
        self.label_6.setText(_translate("InfoForm", "Add to Favorites"))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    InfoForm = QtWidgets.QWidget()
    ui = Ui_InfoForm()
    ui.setupUi(InfoForm)
    InfoForm.show()
    sys.exit(app.exec_())
