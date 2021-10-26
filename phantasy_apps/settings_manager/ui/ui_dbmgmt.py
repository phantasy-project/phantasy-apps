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
        Dialog.resize(660, 483)
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
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.textBrowser_3.sizePolicy().hasHeightForWidth())
        self.textBrowser_3.setSizePolicy(sizePolicy)
        self.textBrowser_3.setStyleSheet(
            "QTextBrowser {\n"
            "    border:none;\n"
            "    background-color: rgb(239, 239, 239);\n"
            "}")
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.gridLayout_2.addWidget(self.textBrowser_3, 0, 0, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.choose_db1_btn = QtWidgets.QPushButton(self.tab)
        self.choose_db1_btn.setObjectName("choose_db1_btn")
        self.gridLayout_2.addWidget(self.choose_db1_btn, 1, 1, 1, 1)
        self.db1_path_lineEdit = QtWidgets.QLineEdit(self.tab)
        self.db1_path_lineEdit.setObjectName("db1_path_lineEdit")
        self.gridLayout_2.addWidget(self.db1_path_lineEdit, 2, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)
        self.choose_db2_btn = QtWidgets.QPushButton(self.tab)
        self.choose_db2_btn.setObjectName("choose_db2_btn")
        self.gridLayout_2.addWidget(self.choose_db2_btn, 3, 1, 1, 1)
        self.db2_path_lineEdit = QtWidgets.QLineEdit(self.tab)
        self.db2_path_lineEdit.setObjectName("db2_path_lineEdit")
        self.gridLayout_2.addWidget(self.db2_path_lineEdit, 4, 0, 1, 2)
        self.merge_btn = QtWidgets.QPushButton(self.tab)
        self.merge_btn.setObjectName("merge_btn")
        self.gridLayout_2.addWidget(self.merge_btn, 5, 1, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.backup_btn = QtWidgets.QPushButton(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.backup_btn.sizePolicy().hasHeightForWidth())
        self.backup_btn.setSizePolicy(sizePolicy)
        self.backup_btn.setObjectName("backup_btn")
        self.gridLayout_3.addWidget(self.backup_btn, 3, 1, 1, 1)
        self.textBrowser_4 = QtWidgets.QTextBrowser(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.textBrowser_4.sizePolicy().hasHeightForWidth())
        self.textBrowser_4.setSizePolicy(sizePolicy)
        self.textBrowser_4.setStyleSheet(
            "QTextBrowser {\n"
            "    border:none;\n"
            "    background-color: rgb(239, 239, 239);\n"
            "}")
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.gridLayout_3.addWidget(self.textBrowser_4, 0, 0, 1, 2)
        self.backdb_path_lineEdit = QtWidgets.QLineEdit(self.tab_2)
        self.backdb_path_lineEdit.setObjectName("backdb_path_lineEdit")
        self.gridLayout_3.addWidget(self.backdb_path_lineEdit, 2, 0, 1, 2)
        self.choose_backdb_btn = QtWidgets.QPushButton(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.choose_backdb_btn.sizePolicy().hasHeightForWidth())
        self.choose_backdb_btn.setSizePolicy(sizePolicy)
        self.choose_backdb_btn.setObjectName("choose_backdb_btn")
        self.gridLayout_3.addWidget(self.choose_backdb_btn, 1, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.tab_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 1, 0, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem7, 4, 1, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.choose_snpdir_btn.clicked.connect(Dialog.on_select_snpdir)
        self.pushButton_4.clicked.connect(Dialog.on_select_db_file)
        self.init_db_path_browse_btn.clicked.connect(
            Dialog.on_select_init_db_file)
        self.init_db_btn.clicked.connect(Dialog.on_init_db)
        self.pushButton_3.clicked.connect(Dialog.on_file2db)
        self.choose_db1_btn.clicked.connect(Dialog.on_select_db1_path)
        self.choose_db2_btn.clicked.connect(Dialog.on_select_db2_path)
        self.merge_btn.clicked.connect(Dialog.on_merge)
        self.choose_backdb_btn.clicked.connect(Dialog.on_select_backdb_path)
        self.backup_btn.clicked.connect(Dialog.on_back_up)
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
        self.textBrowser_3.setHtml(
            _translate(
                "Dialog",
                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:\'Cantarell\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Merge database 1 to database 2:</p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1. Select the path for database 1;</p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2. Select the path for database 2;</p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3. Push Merge button, check database 2 for merged data.</p></body></html>"
            ))
        self.label_5.setText(
            _translate("Dialog", "Database 1: Contains the data to merge"))
        self.choose_db1_btn.setText(_translate("Dialog", "Browse"))
        self.label_4.setText(
            _translate(
                "Dialog",
                "Database 2: Target database for  the new data merging into"))
        self.choose_db2_btn.setText(_translate("Dialog", "Browse"))
        self.merge_btn.setText(_translate("Dialog", "Merge"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab),
                                  _translate("Dialog", "Merge"))
        self.backup_btn.setText(_translate("Dialog", "Back up"))
        self.textBrowser_4.setHtml(
            _translate(
                "Dialog",
                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:\'Cantarell\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Back up the database that is current working with.</p></body></html>"
            ))
        self.choose_backdb_btn.setText(_translate("Dialog", "Browse"))
        self.label_6.setText(
            _translate("Dialog", "Select the path for backup database"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2),
                                  _translate("Dialog", "Backup"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
