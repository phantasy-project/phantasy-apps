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
        Form.resize(1137, 802)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(
            _translate(
                "Form",
                "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600; color:#0000ff;\">Search Tips</span></p></body></html>"
            ))
        self.textEdit.setHtml(
            _translate(
                "Form",
                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:\'Cantarell\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Input filter string with the format of </span><span style=\" font-size:14pt; font-weight:600;\">keyword=pattern</span><span style=\" font-size:14pt;\">, different filtering conditions can be combined with </span><span style=\" font-size:14pt; font-weight:600;\">and </span><span style=\" font-size:14pt;\">logic. </span><span style=\" font-size:14pt; font-style:italic;\">Pattern</span><span style=\" font-size:14pt;\"> applies Unix wildcard rules. By default </span><span style=\" font-size:14pt; font-style:italic;\">Pattern</span><span style=\" font-size:14pt;\"> prefixed and suffixed with \'*\' unless \'Strict\' option is checked. </span><span style=\" font-size:14pt; font-style:italic;\">Keyword</span><span style=\" font-size:14pt;\"> is case insensitive, if </span><span style=\" font-size:14pt; font-style:italic;\">keyword</span><span style=\" font-size:14pt;\"> is not given, </span><span style=\" font-size:14pt; font-style:italic;\">device</span><span style=\" font-size:14pt;\"> will be used. Valid keywords are: </span><span style=\" font-size:14pt; font-style:italic;\">device</span><span style=\" font-size:14pt;\">, </span><span style=\" font-size:14pt; font-style:italic;\">field</span><span style=\" font-size:14pt;\">, </span><span style=\" font-size:14pt; font-style:italic;\">type</span><span style=\" font-size:14pt;\">, </span><span style=\" font-size:14pt; font-style:italic;\">pos</span><span style=\" font-size:14pt;\">, </span><span style=\" font-size:14pt; font-style:italic;\">x0</span><span style=\" font-size:14pt;\">, </span><span style=\" font-size:14pt; font-style:italic;\">x1</span><span style=\" font-size:14pt;\">, </span><span style=\" font-size:14pt; font-style:italic;\">x2</span><span style=\" font-size:14pt;\">, </span><span style=\" font-size:14pt; font-style:italic;\">dx01</span><span style=\" font-size:14pt;\">, </span><span style=\" font-size:14pt; font-style:italic;\">dx02</span><span style=\" font-size:14pt;\">, </span><span style=\" font-size:14pt; font-style:italic;\">dx12</span><span style=\" font-size:14pt;\">, </span><span style=\" font-size:14pt; font-style:italic;\">x2/x0</span><span style=\" font-size:14pt;\">, </span><span style=\" font-size:14pt; font-style:italic;\">tolerance</span><span style=\" font-size:14pt;\">, </span><span style=\" font-size:14pt; font-style:italic;\">writable</span><span style=\" font-size:14pt;\">.</span></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">For </span><span style=\" font-size:14pt; font-style:italic;\">Setpoint</span><span style=\" font-size:14pt;\"> column, the keyword </span><span style=\" font-size:14pt; font-style:italic;\">x0</span><span style=\" font-size:14pt;\"> is used, the same rule applies to </span><span style=\" font-size:14pt; font-style:italic;\">x1</span><span style=\" font-size:14pt;\">, </span><span style=\" font-size:14pt; font-style:italic;\">x2</span><span style=\" font-size:14pt;\">, </span><span style=\" font-size:14pt; font-style:italic;\">dx01</span><span style=\" font-size:14pt;\">, </span><span style=\" font-size:14pt; font-style:italic;\">dx02</span><span style=\" font-size:14pt;\">, </span><span style=\" font-size:14pt; font-style:italic;\">dx12</span><span style=\" font-size:14pt;\">, where </span><span style=\" font-size:14pt; font-style:italic;\">dxij</span><span style=\" font-size:14pt;\"> is </span><span style=\" font-size:14pt; font-style:italic;\">Δ(xi, xj)</span><span style=\" font-size:14pt;\"> as shown in the headers.</span></p>\n"
                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Press </span><span style=\" font-size:14pt; font-weight:600;\">Enter</span><span style=\" font-size:14pt;\"> to activate the filter, </span><span style=\" font-size:14pt; font-weight:600;\">Esc</span><span style=\" font-size:14pt;\"> to clear the filter.</span></p>\n"
                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600;\">General wildcard rules: </span></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">1. * is to match any char or digit.</span></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">2. ? is to match one char or digit, pure \'\' is to interpret as *.</span></p>\n"
                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600;\">Contains test:</span></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">The contains test with </span><span style=\" font-size:14pt; font-weight:600;\">in</span><span style=\" font-size:14pt;\"> is supported, when the </span><span style=\" font-size:14pt; font-style:italic;\">pattern</span><span style=\" font-size:14pt;\"> starts with </span><span style=\" font-size:14pt; font-style:italic;\">in</span><span style=\" font-size:14pt;\"> followed by a list/tuple. The value of key will be tested if it is in the defined list/tuple, no wildcard is supported for the tuple/list members, e.g.</span></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">1. pos=(10,) and field=in (\'I\', \'AMP\') match all the devices after longitudinal location &gt;= 10 m, and field name is \'I\' or \'AMP\' (please quote the field names).</span></p>\n"
                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600;\">Filter examples:</span></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">1. *: match all device names, which is equivalent of device=*.</span></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">2. *LEBT*: match device name which has string \'LEBT\', or simply input LEBT.</span></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">3. type=\'CAV\': match all devices of type \'CAV\' when \'Strict\' option enabled, otherwise also match CAV1, 1CAV, etc.</span></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">4. type=\'*COR\': match all devices of type \'HCOR\' and \'VCOR\'.</span></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">5. dx12=0.00*: match the diff between readback and setpoint of 0.00xx...</span></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">6. device=*LS1* and type=*COR and pos=(20, ): match all devices, which device name has string \'LS1\', device type is HCOR or VCOR, located after 20 m, note: LS1 and COR do the same filter set.</span></p>\n"
                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600;\">Number Columns:</span></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">For the columns where values are numbers, value range or single value filter is supported:</span></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">1. pos=(1,) matches all the position value equal or greater than 1.0.</span></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">2. x1=(-1, 2) matches current readback value is in [-1, 2] range.</span></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">3. dx12=0.1 matches the discrenpacy between the live readback and setpoint is 0.1.</span></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">4. x2/x0=(0.1,) matches the ratio of x2/x0 greater than 0.1.</span></p></body></html>"
            ))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
