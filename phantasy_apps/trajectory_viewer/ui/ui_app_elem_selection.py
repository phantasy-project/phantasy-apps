# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_app_elem_selection.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(676, 490)
        Form.setStyleSheet(
            "QGroupBox {\n"
            "    /*background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #E0E0E0, stop: 1 #E0E0E0);\n"
            "   */\n"
            "    border: 2px solid gray;\n"
            "    border-radius: 5px;\n"
            "    margin-top: 1.5ex; /* leave space at the top for the title */\n"
            "    margin-bottom: 0.5ex;\n"
            "}\n"
            "\n"
            "QGroupBox::title {\n"
            "    subcontrol-origin: margin;\n"
            "    subcontrol-position: top center; /* position at the top center */\n"
            "    padding: 0 3px;\n"
            "    /*background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #EDECEB, stop: 1 #FFFFFF);\n"
            "    */\n"
            "}\n"
            "\n"
            "QLineEdit {\n"
            "    border: 0.5px solid gray;\n"
            "    padding: 1 5px;\n"
            "    border-radius: 3px;\n"
            "}")
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setContentsMargins(6, 6, 6, 6)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.treeView = QtWidgets.QTreeView(Form)
        self.treeView.setObjectName("treeView")
        self.gridLayout_3.addWidget(self.treeView, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.listed_nelem_lineEdit = QtWidgets.QLineEdit(Form)
        self.listed_nelem_lineEdit.setReadOnly(True)
        self.listed_nelem_lineEdit.setObjectName("listed_nelem_lineEdit")
        self.horizontalLayout.addWidget(self.listed_nelem_lineEdit)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.selected_nelem_lineEdit = QtWidgets.QLineEdit(Form)
        self.selected_nelem_lineEdit.setReadOnly(True)
        self.selected_nelem_lineEdit.setObjectName("selected_nelem_lineEdit")
        self.horizontalLayout.addWidget(self.selected_nelem_lineEdit)
        self.gridLayout_3.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.dtypes_groupBox = QtWidgets.QGroupBox(Form)
        self.dtypes_groupBox.setCheckable(False)
        self.dtypes_groupBox.setChecked(False)
        self.dtypes_groupBox.setObjectName("dtypes_groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.dtypes_groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.dtypes_gridLayout = QtWidgets.QGridLayout()
        self.dtypes_gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.dtypes_gridLayout.setObjectName("dtypes_gridLayout")
        self.toggle_all_dtypes_chkbox = QtWidgets.QCheckBox(
            self.dtypes_groupBox)
        self.toggle_all_dtypes_chkbox.setEnabled(True)
        self.toggle_all_dtypes_chkbox.setObjectName("toggle_all_dtypes_chkbox")
        self.dtypes_gridLayout.addWidget(self.toggle_all_dtypes_chkbox, 0, 0,
                                         1, 1)
        self.gridLayout.addLayout(self.dtypes_gridLayout, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.dtypes_groupBox, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.exit_btn = QtWidgets.QPushButton(Form)
        self.exit_btn.setObjectName("exit_btn")
        self.horizontalLayout_2.addWidget(self.exit_btn)
        self.apply_btn = QtWidgets.QPushButton(Form)
        self.apply_btn.setObjectName("apply_btn")
        self.horizontalLayout_2.addWidget(self.apply_btn)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 4, 0, 1, 1)

        self.retranslateUi(Form)
        self.toggle_all_dtypes_chkbox.toggled['bool'].connect(
            Form.on_toggle_all_dtypes)
        self.exit_btn.clicked.connect(Form.close)
        self.apply_btn.clicked.connect(Form.on_click_apply)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Total Listed Elements"))
        self.label_2.setText(_translate("Form", "Selected Elements"))
        self.dtypes_groupBox.setTitle(
            _translate("Form", "Filter by Device Types"))
        self.toggle_all_dtypes_chkbox.setText(_translate("Form", "All"))
        self.exit_btn.setText(_translate("Form", "Exit"))
        self.apply_btn.setText(_translate("Form", "Apply"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
