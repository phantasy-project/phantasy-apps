# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_query_tips.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1143, 819)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.textBrowser.setHtml(
            _translate(
                "Form",
                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:\'Cantarell\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Input filter string with the format of <span style=\" font-weight:600;\">keyword=pattern</span>.  <span style=\" font-style:italic;\">Pattern</span> applies Unix wildcard rules. <span style=\" font-style:italic;\">Keyword</span> is case insensitive, if <span style=\" font-style:italic;\">keyword</span> is not given, <span style=\" font-style:italic;\">device</span> is used. Valid keywords are: <span style=\" font-style:italic;\">device</span>, <span style=\" font-style:italic;\">field</span>, <span style=\" font-style:italic;\">type</span>, <span style=\" font-style:italic;\">pos</span>, <span style=\" font-style:italic;\">x0</span>, <span style=\" font-style:italic;\">x1</span>, <span style=\" font-style:italic;\">x2</span>, <span style=\" font-style:italic;\">dx01</span>, <span style=\" font-style:italic;\">dx02</span>, <span style=\" font-style:italic;\">dx12</span>, <span style=\" font-style:italic;\">tolerance</span>, <span style=\" font-style:italic;\">writable</span>.</p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">For <span style=\" font-style:italic;\">Setpoint</span> column, the keyword <span style=\" font-style:italic;\">x0</span> is used, the same rule applies to <span style=\" font-style:italic;\">x1</span>, <span style=\" font-style:italic;\">x2</span>, <span style=\" font-style:italic;\">dx01</span>, <span style=\" font-style:italic;\">dx02</span>, <span style=\" font-style:italic;\">dx12</span>, where <span style=\" font-style:italic;\">dxij</span> is <span style=\" font-style:italic;\">Δ(xi, xj)</span> as shown in the headers.</p>\n"
                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Press <span style=\" font-style:italic;\">Enter</span> to activate the filter, <span style=\" font-style:italic;\">Esc</span> to clear the filter.</p>\n"
                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">General wildcard rules: </span></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1. * is to match any char or digit.</p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2. ? is to match one char or digit, pure \'\' is to interpret as *.</p>\n"
                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Filter examples:</span></p>\n"
                "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1. *: match all device names, which is equivalent of device=*.</p>\n"
                "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2. *LEBT*: match device name which has string \'LEBT\'.</p>\n"
                "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3. type=\'CAV\': match all devices of type \'CAV\'.</p>\n"
                "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">4. type=\'*COR\': match all devices of type \'HCOR\' and \'VCOR\'.</p>\n"
                "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">5. dx12=0.00*: match the diff between readback and setpoint of 0.00xx...</p>\n"
                "<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Number Columns:</span></p>\n"
                "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">For the columns where values are numbers, value range or single value filter is supported:</p>\n"
                "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">6. pos=(1,) matches all the position value equal or greater than 1.0.</p>\n"
                "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">7. x1=(-1, 2) matches current readback value is in [-1, 2] range.</p>\n"
                "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">8. dx12=0.1 matches the discrenpacy between the live readback and setpoint is 0.1.</p></body></html>"
            ))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
