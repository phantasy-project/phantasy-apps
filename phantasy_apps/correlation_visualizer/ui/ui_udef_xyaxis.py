# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_udef_xyaxis.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1058, 622)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.title_textEdit = QtWidgets.QTextEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.title_textEdit.sizePolicy().hasHeightForWidth())
        self.title_textEdit.setSizePolicy(sizePolicy)
        self.title_textEdit.setReadOnly(True)
        self.title_textEdit.setObjectName("title_textEdit")
        self.gridLayout.addWidget(self.title_textEdit, 0, 0, 1, 1)
        self.body_textEdit = QtWidgets.QTextEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.body_textEdit.sizePolicy().hasHeightForWidth())
        self.body_textEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.body_textEdit.setFont(font)
        self.body_textEdit.setReadOnly(True)
        self.body_textEdit.setObjectName("body_textEdit")
        self.gridLayout.addWidget(self.body_textEdit, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.title_textEdit.setHtml(
            _translate(
                "Form",
                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:\'Cantarell\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Input user-defined expressions into the right text box to visualize arbitrary correlation between <span style=\" font-style:italic;\">X</span> and <span style=\" font-style:italic;\">Y</span>.</p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">X</span> and <span style=\" font-style:italic;\">Y</span> could be composed as a function with the input parameters of <span style=\" font-style:italic;\">x1</span>, <span style=\" font-style:italic;\">x2</span>, ..., <span style=\" font-style:italic;\">y1</span>, <span style=\" font-style:italic;\">y2</span>, ..., where <span style=\" font-style:italic;\">xi</span> is the (<span style=\" font-style:italic;\">i-1</span>)th parameter defined in the below X-Axis combobox, while <span style=\" font-style:italic;\">yi</span> is the (<span style=\" font-style:italic;\">i-1</span>)th parameter defined in Y-Axis combobox. For instance, X-Axis has items [XNAME-1, XNAME-2], to have X axis show the data of XNAME-1 - XNAME-2, define X = x1 - x2, input \'x1 - x2\' in the text box (without quotation marks) above of X-Axis combobox.</p></body></html>"
            ))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
