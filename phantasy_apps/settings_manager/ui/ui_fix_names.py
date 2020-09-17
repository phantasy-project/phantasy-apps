# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_fix_names.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(984, 672)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.browse_btn = QtWidgets.QPushButton(Dialog)
        self.browse_btn.setEnabled(False)
        self.browse_btn.setObjectName("browse_btn")
        self.gridLayout.addWidget(self.browse_btn, 3, 3, 1, 1)
        self.export_dir_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.export_dir_lineEdit.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.export_dir_lineEdit.sizePolicy().hasHeightForWidth())
        self.export_dir_lineEdit.setSizePolicy(sizePolicy)
        self.export_dir_lineEdit.setObjectName("export_dir_lineEdit")
        self.gridLayout.addWidget(self.export_dir_lineEdit, 3, 2, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setStyleSheet("QLabel {\n" "    font-weight: bold;\n" "}")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.new_dir_chkbox = QtWidgets.QCheckBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.new_dir_chkbox.sizePolicy().hasHeightForWidth())
        self.new_dir_chkbox.setSizePolicy(sizePolicy)
        self.new_dir_chkbox.setObjectName("new_dir_chkbox")
        self.gridLayout.addWidget(self.new_dir_chkbox, 3, 0, 1, 2)
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.plainTextEdit_2.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_2.setSizePolicy(sizePolicy)
        self.plainTextEdit_2.setStyleSheet(
            "QPlainTextEdit {\n"
            "    border:none;\n"
            "    background-color: rgb(239, 239, 239);\n"
            "   font-style: italic;\n"
            "}")
        self.plainTextEdit_2.setReadOnly(True)
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.gridLayout.addWidget(self.plainTextEdit_2, 2, 0, 1, 1)
        self.open_btn = QtWidgets.QPushButton(Dialog)
        self.open_btn.setObjectName("open_btn")
        self.gridLayout.addWidget(self.open_btn, 3, 4, 1, 1)
        self.fix_btn = QtWidgets.QPushButton(Dialog)
        self.fix_btn.setObjectName("fix_btn")
        self.gridLayout.addWidget(self.fix_btn, 3, 5, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 6, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setStyleSheet(
            "QTextBrowser {\n"
            "    background-color: rgb(239, 239, 239);\n"
            "}")
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 7)
        self.csvfilelist_textEdit = QtWidgets.QTextEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.csvfilelist_textEdit.sizePolicy().hasHeightForWidth())
        self.csvfilelist_textEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.csvfilelist_textEdit.setFont(font)
        self.csvfilelist_textEdit.setReadOnly(True)
        self.csvfilelist_textEdit.setObjectName("csvfilelist_textEdit")
        self.gridLayout.addWidget(self.csvfilelist_textEdit, 1, 1, 2, 6)

        self.retranslateUi(Dialog)
        self.new_dir_chkbox.toggled['bool'].connect(
            self.export_dir_lineEdit.setEnabled)
        self.new_dir_chkbox.toggled['bool'].connect(self.browse_btn.setEnabled)
        self.new_dir_chkbox.toggled['bool'].connect(self.browse_btn.setFocus)
        self.open_btn.clicked.connect(Dialog.on_open_files)
        self.fix_btn.clicked.connect(Dialog.on_fix)
        self.pushButton.clicked.connect(Dialog.reject)
        self.browse_btn.clicked.connect(Dialog.on_set_export_dir)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.browse_btn.setText(_translate("Dialog", "Browse"))
        self.label.setText(_translate("Dialog", "CSV files to read and fix"))
        self.new_dir_chkbox.setText(
            _translate("Dialog", "Store new files to another directory"))
        self.plainTextEdit_2.setPlainText(
            _translate(
                "Dialog",
                "By default the file will be overwritten, or check the following option to put into another directory"
            ))
        self.open_btn.setText(_translate("Dialog", "Open"))
        self.fix_btn.setText(_translate("Dialog", "Fix"))
        self.pushButton.setText(_translate("Dialog", "Exit"))
        self.textBrowser.setHtml(
            _translate(
                "Dialog",
                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:\'Cantarell\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Fix the names of correctors in LS1 and LS2, which were saved before the changes of \'phantasy-machines\' (commit: 39c94e5), e.g.</p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">the name of corrector LS1_CA01:DCH1_D1132 was names LS1_CA01:DCH_D1132, after <span style=\" font-style:italic;\">Fix</span>, the new names will be used.</p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Open CSV files via <span style=\" font-style:italic;\">Open</span> button.</p></body></html>"
            ))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())