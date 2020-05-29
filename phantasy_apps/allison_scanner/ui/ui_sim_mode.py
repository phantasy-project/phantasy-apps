# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_sim_mode.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(188, 93)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setContentsMargins(1, 0, 1, 0)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.ready_lbl = QtWidgets.QLabel(self.groupBox)
        self.ready_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.ready_lbl.setObjectName("ready_lbl")
        self.gridLayout.addWidget(self.ready_lbl, 0, 1, 1, 1)
        self.stop = QtWidgets.QToolButton(self.groupBox)
        self.stop.setObjectName("stop")
        self.gridLayout.addWidget(self.stop, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.start = QtWidgets.QToolButton(self.groupBox)
        self.start.setObjectName("start")
        self.gridLayout.addWidget(self.start, 1, 0, 1, 1)
        self.refresh_btn = QtWidgets.QToolButton(self.groupBox)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/update.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.refresh_btn.setIcon(icon)
        self.refresh_btn.setObjectName("refresh_btn")
        self.gridLayout.addWidget(self.refresh_btn, 0, 2, 2, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.start.clicked.connect(Form.on_start)
        self.stop.clicked.connect(Form.on_stop)
        self.refresh_btn.clicked.connect(Form.on_refresh)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.ready_lbl.setText(_translate("Form", "Ready?"))
        self.stop.setText(_translate("Form", "STOP"))
        self.label_3.setText(_translate("Form", "IOC Status"))
        self.start.setText(_translate("Form", "START"))
        self.refresh_btn.setText(_translate("Form", "..."))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
