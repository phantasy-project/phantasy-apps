# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_device_selection.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(835, 354)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pv_input_gbox = QtWidgets.QGridLayout()
        self.pv_input_gbox.setObjectName("pv_input_gbox")
        self.pv_lbl = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pv_lbl.sizePolicy().hasHeightForWidth())
        self.pv_lbl.setSizePolicy(sizePolicy)
        self.pv_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing
                                 | QtCore.Qt.AlignVCenter)
        self.pv_lbl.setObjectName("pv_lbl")
        self.pv_input_gbox.addWidget(self.pv_lbl, 0, 0, 1, 1)
        self.pv_lineEdit = QtWidgets.QLineEdit(Form)
        self.pv_lineEdit.setObjectName("pv_lineEdit")
        self.pv_input_gbox.addWidget(self.pv_lineEdit, 0, 1, 1, 1)
        self.add_btn = QtWidgets.QToolButton(Form)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/dv/add.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.add_btn.setIcon(icon)
        self.add_btn.setIconSize(QtCore.QSize(24, 24))
        self.add_btn.setObjectName("add_btn")
        self.pv_input_gbox.addWidget(self.add_btn, 0, 2, 1, 1)
        self.del_btn = QtWidgets.QToolButton(Form)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/dv/remove.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.del_btn.setIcon(icon1)
        self.del_btn.setIconSize(QtCore.QSize(24, 24))
        self.del_btn.setObjectName("del_btn")
        self.pv_input_gbox.addWidget(self.del_btn, 0, 3, 1, 1)
        self.verticalLayout.addLayout(self.pv_input_gbox)
        self.pv_textEdit = QtWidgets.QTextEdit(Form)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.pv_textEdit.setFont(font)
        self.pv_textEdit.setReadOnly(True)
        self.pv_textEdit.setObjectName("pv_textEdit")
        self.verticalLayout.addWidget(self.pv_textEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.pv_cnt_lbl = QtWidgets.QLabel(Form)
        self.pv_cnt_lbl.setText("")
        self.pv_cnt_lbl.setObjectName("pv_cnt_lbl")
        self.horizontalLayout.addWidget(self.pv_cnt_lbl)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.exit_btn = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.exit_btn.sizePolicy().hasHeightForWidth())
        self.exit_btn.setSizePolicy(sizePolicy)
        self.exit_btn.setAutoDefault(True)
        self.exit_btn.setObjectName("exit_btn")
        self.horizontalLayout.addWidget(self.exit_btn)
        self.apply_btn = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.apply_btn.sizePolicy().hasHeightForWidth())
        self.apply_btn.setSizePolicy(sizePolicy)
        self.apply_btn.setAutoDefault(True)
        self.apply_btn.setObjectName("apply_btn")
        self.horizontalLayout.addWidget(self.apply_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pv_lbl.setBuddy(self.pv_lineEdit)

        self.retranslateUi(Form)
        self.pv_textEdit.textChanged.connect(Form.on_pvlist_changed)
        self.exit_btn.clicked.connect(Form.on_exit)
        self.apply_btn.clicked.connect(Form.on_apply)
        self.pv_textEdit.selectionChanged.connect(Form.on_selection_changed)
        self.pv_lineEdit.returnPressed.connect(self.add_btn.click)
        self.add_btn.clicked.connect(Form.on_add_pv)
        self.del_btn.clicked.connect(Form.on_del_pv)
        self.pushButton.clicked.connect(Form.on_clear_all_pv)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pv_lbl.setText(_translate("Form", "Process Variable"))
        self.pv_lineEdit.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Press Enter after input</p></body></html>"
            ))
        self.add_btn.setText(_translate("Form", "..."))
        self.del_btn.setText(_translate("Form", "..."))
        self.label.setText(_translate("Form", "Total PVs:"))
        self.pushButton.setText(_translate("Form", "Clear All PVs"))
        self.exit_btn.setText(_translate("Form", "Exit"))
        self.apply_btn.setText(_translate("Form", "Apply"))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
