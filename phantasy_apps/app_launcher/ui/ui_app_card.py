# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_app_card.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AppForm(object):
    def setupUi(self, AppForm):
        AppForm.setObjectName("AppForm")
        AppForm.resize(226, 333)
        AppForm.setStyleSheet("QWidget#AppForm {\n"
                              "    border: 2px solid rgb(200,200,200);\n"
                              "}\n"
                              "QWidget#AppForm:hover:!pressed {\n"
                              "    border: 2px solid rgb(138, 138, 138);\n"
                              "}")
        self.verticalLayout = QtWidgets.QVBoxLayout(AppForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.app_ver_lbl = QtWidgets.QLabel(AppForm)
        self.app_ver_lbl.setObjectName("app_ver_lbl")
        self.horizontalLayout.addWidget(self.app_ver_lbl)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.fav_btn = QtWidgets.QToolButton(AppForm)
        self.fav_btn.setStyleSheet(
            "QToolButton {\n"
            "    border-image: url(\":/icons/fav-off.svg\");\n"
            "    width: 32px;\n"
            "    height: 32px;\n"
            "    background-repeat: no-repeat;\n"
            "}\n"
            "QToolButton::hover {\n"
            "    border-image: url(:/icons/fav-off-hover.svg);\n"
            "    background-repeat: no-repeat;\n"
            "}\n"
            "QToolButton::checked {\n"
            "    border-image: url(:/icons/fav-on.svg);\n"
            "    background-repeat: no-repeat;\n"
            "}\n"
            "QToolButton::unchecked {\n"
            "    border-image: url(:/icons/fav-off.svg);\n"
            "    background-repeat: no-repeat;\n"
            "}")
        self.fav_btn.setText("")
        self.fav_btn.setCheckable(True)
        self.fav_btn.setChecked(False)
        self.fav_btn.setObjectName("fav_btn")
        self.horizontalLayout.addWidget(self.fav_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.app_btn = QtWidgets.QToolButton(AppForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.app_btn.sizePolicy().hasHeightForWidth())
        self.app_btn.setSizePolicy(sizePolicy)
        self.app_btn.setMinimumSize(QtCore.QSize(128, 128))
        self.app_btn.setMaximumSize(QtCore.QSize(128, 128))
        self.app_btn.setBaseSize(QtCore.QSize(128, 128))
        self.app_btn.setStyleSheet("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/app-icons/app-icons/default.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.app_btn.setIcon(icon)
        self.app_btn.setIconSize(QtCore.QSize(64, 64))
        self.app_btn.setAutoRaise(True)
        self.app_btn.setObjectName("app_btn")
        self.horizontalLayout_2.addWidget(self.app_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.app_name_lbl = QtWidgets.QLabel(AppForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.app_name_lbl.sizePolicy().hasHeightForWidth())
        self.app_name_lbl.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.app_name_lbl.setFont(font)
        self.app_name_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.app_name_lbl.setObjectName("app_name_lbl")
        self.verticalLayout.addWidget(self.app_name_lbl)
        self.app_group_lbl = QtWidgets.QLabel(AppForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.app_group_lbl.sizePolicy().hasHeightForWidth())
        self.app_group_lbl.setSizePolicy(sizePolicy)
        self.app_group_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.app_group_lbl.setObjectName("app_group_lbl")
        self.verticalLayout.addWidget(self.app_group_lbl)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.info_btn = QtWidgets.QToolButton(AppForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.info_btn.sizePolicy().hasHeightForWidth())
        self.info_btn.setSizePolicy(sizePolicy)
        self.info_btn.setStyleSheet(
            "QToolButton {\n"
            "    border-image: url(:/icons/arrow_down-thin-off.png);\n"
            "    width: 64px;\n"
            "    height: 27px;\n"
            "    background-repeat: no-repeat;\n"
            "}\n"
            "QToolButton::hover {\n"
            "    border-image: url(:/icons/arrow_down-thin-on.png);\n"
            "    background-repeat: no-repeat;\n"
            "}\n"
            "QToolButton::checked {\n"
            "    border-image: url(:/icons/arrow_down-thin-on.png);\n"
            "    background-repeat: no-repeat;\n"
            "}\n"
            "QToolButton::unchecked {\n"
            "    border-image: url(:/icons/arrow_down-thin-on.png);\n"
            "    background-repeat: no-repeat;\n"
            "}")
        self.info_btn.setText("")
        self.info_btn.setCheckable(True)
        self.info_btn.setAutoRaise(False)
        self.info_btn.setObjectName("info_btn")
        self.horizontalLayout_3.addWidget(self.info_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(AppForm)
        self.fav_btn.toggled['bool'].connect(AppForm.on_toggle_fav)
        self.info_btn.toggled['bool'].connect(AppForm.on_toggle_info)
        QtCore.QMetaObject.connectSlotsByName(AppForm)

    def retranslateUi(self, AppForm):
        _translate = QtCore.QCoreApplication.translate
        AppForm.setWindowTitle(_translate("AppForm", "Form"))
        self.app_ver_lbl.setText(_translate("AppForm", "v1.0"))
        self.app_btn.setText(_translate("AppForm", "APP ICON"))
        self.app_name_lbl.setText(_translate("AppForm", "APP NAME"))
        self.app_group_lbl.setText(_translate("AppForm",
                                              "App Main Group Name"))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AppForm = QtWidgets.QWidget()
    ui = Ui_AppForm()
    ui.setupUi(AppForm)
    AppForm.show()
    sys.exit(app.exec_())
