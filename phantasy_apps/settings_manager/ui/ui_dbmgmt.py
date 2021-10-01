# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_dbmgmt.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(738, 458)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")
        self.init_page = QtWidgets.QWidget()
        self.init_page.setObjectName("init_page")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.init_page)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(self.init_page)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.init_db_path_lineEdit = QtWidgets.QLineEdit(self.init_page)
        self.init_db_path_lineEdit.setObjectName("init_db_path_lineEdit")
        self.horizontalLayout_3.addWidget(self.init_db_path_lineEdit)
        self.init_db_path_browse_btn = QtWidgets.QPushButton(self.init_page)
        self.init_db_path_browse_btn.setObjectName("init_db_path_browse_btn")
        self.horizontalLayout_3.addWidget(self.init_db_path_browse_btn)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.init_db_btn = QtWidgets.QPushButton(self.init_page)
        self.init_db_btn.setObjectName("init_db_btn")
        self.horizontalLayout_4.addWidget(self.init_db_btn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.tabWidget.addTab(self.init_page, "")
        self.generate_page = QtWidgets.QWidget()
        self.generate_page.setObjectName("generate_page")
        self.gridLayout = QtWidgets.QGridLayout(self.generate_page)
        self.gridLayout.setObjectName("gridLayout")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.generate_page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.textBrowser_2.sizePolicy().hasHeightForWidth())
        self.textBrowser_2.setSizePolicy(sizePolicy)
        self.textBrowser_2.setStyleSheet(
            "QTextBrowser {\n"
            "    border:none;\n"
            "    background-color: rgb(239, 239, 239);\n"
            "}")
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.gridLayout.addWidget(self.textBrowser_2, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.generate_page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.choose_snpdir_btn = QtWidgets.QPushButton(self.generate_page)
        self.choose_snpdir_btn.setObjectName("choose_snpdir_btn")
        self.horizontalLayout_5.addWidget(self.choose_snpdir_btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.snpdirpath_lineEdit = QtWidgets.QLineEdit(self.generate_page)
        self.snpdirpath_lineEdit.setObjectName("snpdirpath_lineEdit")
        self.verticalLayout_2.addWidget(self.snpdirpath_lineEdit)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.generate_page)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.db_path_lineEdit = QtWidgets.QLineEdit(self.generate_page)
        self.db_path_lineEdit.setObjectName("db_path_lineEdit")
        self.horizontalLayout.addWidget(self.db_path_lineEdit)
        self.pushButton_4 = QtWidgets.QPushButton(self.generate_page)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.pushButton_3 = QtWidgets.QPushButton(self.generate_page)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem6, 4, 0, 1, 1)
        self.tabWidget.addTab(self.generate_page, "")
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.init_db_path_browse_btn.clicked.connect(
            Dialog.on_select_init_db_file)
        self.init_db_btn.clicked.connect(Dialog.on_init_db)
        self.choose_snpdir_btn.clicked.connect(Dialog.on_select_snpdir)
        self.pushButton_4.clicked.connect(Dialog.on_select_db_file)
        self.pushButton_3.clicked.connect(Dialog.on_file2db)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Initialize Database"))
        self.init_db_path_browse_btn.setText(_translate("Dialog", "Browse"))
        self.init_db_btn.setText(_translate("Dialog", "Create"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.init_page),
                                  _translate("Dialog", "Initialization"))
        self.textBrowser_2.setHtml(
            _translate(
                "Dialog",
                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:\'Cantarell\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Generate Database with Snapshot Files Captured by Settings Manager:</p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1. Input the directory path where contains all the snapshot files;</p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2. Input the path for the generated database file;</p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3. Push Generate button.</p></body></html>"
            ))
        self.label_2.setText(
            _translate("Dialog", "Folder path for snapshot files"))
        self.choose_snpdir_btn.setText(_translate("Dialog", "Browse"))
        self.label_3.setText(_translate("Dialog", "Database Path"))
        self.pushButton_4.setText(_translate("Dialog", "Browse"))
        self.pushButton_3.setText(_translate("Dialog", "Generate"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.generate_page),
                                  _translate("Dialog", "Generation"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
