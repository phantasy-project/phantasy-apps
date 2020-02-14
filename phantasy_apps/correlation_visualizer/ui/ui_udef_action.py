# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_udef_action.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1060, 800)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setContentsMargins(6, 12, 6, 6)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)
        self.save_btn = QtWidgets.QPushButton(Dialog)
        self.save_btn.setObjectName("save_btn")
        self.gridLayout.addWidget(self.save_btn, 0, 3, 1, 1)
        self.saveas_btn = QtWidgets.QPushButton(Dialog)
        self.saveas_btn.setObjectName("saveas_btn")
        self.gridLayout.addWidget(self.saveas_btn, 0, 4, 1, 1)
        self.browse_btn = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.browse_btn.sizePolicy().hasHeightForWidth())
        self.browse_btn.setSizePolicy(sizePolicy)
        self.browse_btn.setObjectName("browse_btn")
        self.gridLayout.addWidget(self.browse_btn, 0, 5, 1, 1)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit.setStyleSheet("QPlainTextEdit {\n"
                                         "    font-family: monospace;\n"
                                         "}")
        self.plainTextEdit.setPlaceholderText("")
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout.addWidget(self.plainTextEdit, 1, 0, 1, 6)
        self.label_2 = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.func_name_lineEdit = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.func_name_lineEdit.sizePolicy().hasHeightForWidth())
        self.func_name_lineEdit.setSizePolicy(sizePolicy)
        self.func_name_lineEdit.setObjectName("func_name_lineEdit")
        self.gridLayout.addWidget(self.func_name_lineEdit, 2, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 2, 1, 2)
        self.ok_btn = QtWidgets.QPushButton(Dialog)
        self.ok_btn.setObjectName("ok_btn")
        self.gridLayout.addWidget(self.ok_btn, 2, 4, 1, 1)
        self.cancel_btn = QtWidgets.QPushButton(Dialog)
        self.cancel_btn.setObjectName("cancel_btn")
        self.gridLayout.addWidget(self.cancel_btn, 2, 5, 1, 1)

        self.retranslateUi(Dialog)
        self.browse_btn.clicked.connect(Dialog.on_open_file)
        self.ok_btn.clicked.connect(Dialog.on_click_ok)
        self.cancel_btn.clicked.connect(Dialog.on_click_cancel)
        self.save_btn.clicked.connect(Dialog.on_save)
        self.saveas_btn.clicked.connect(Dialog.on_save_as)
        self.plainTextEdit.textChanged.connect(Dialog.on_text_changed)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(
            _translate(
                "Dialog",
                "Input Python code in the below area or load from a file to define the alter element action"
            ))
        self.save_btn.setText(_translate("Dialog", "Save"))
        self.saveas_btn.setText(_translate("Dialog", "Save As"))
        self.browse_btn.setText(_translate("Dialog", "Browse"))
        self.plainTextEdit.setPlainText(
            _translate(
                "Dialog",
                "\"\"\"User-defined operation to change the device(s) setting(s) before each DAQ.\n"
                "\n"
                "Here are some rules:\n"
                "1. The function name is \'f\';\n"
                "2. The first argument is the new setting for selected alter element;\n"
                "3. Available keyword arguments are:\n"
                "   - \'alter_elem\': current selected element to change;\n"
                "   - \'tolerance\': absolute discrenpancy between set and read;\n"
                "   - \'timeout\': timeout in second for \'ensure put\';\n"
                "   - \'extra_wait\': additional wait time in second after \'ensure put\'; \n"
                "\"\"\"\n"
                "from phantasy import ensure_put\n"
                "# from phantasy_ui import printlog\n"
                "                                                                               \n"
                "def f(goal, **kws):                                                                                                                                                                                           \n"
                "    # set alter element, apply ensure put                                         \n"
                "    alter_elem = kws.get(\'alter_elem\', None)                                      \n"
                "    tolerance = kws.get(\'tolerance\', 0.01)                                        \n"
                "    timeout = kws.get(\'timeout\', 0.01)                                            \n"
                "    extra_wait = kws.get(\'extra_wait\', 0.0)                                       \n"
                "    if alter_elem is None:                                                        \n"
                "        return                                                                    \n"
                "    ensure_put(alter_elem, goal=goal, tol=tolerance, timeout=timeout)          \n"
                "    # printlog(\"{} RD: {} SP: {}\".format(alter_elem.ename, alter_elem.value, goal))\n"
                "                                                                               \n"
                "    # extra wait                                                               \n"
                "    time.sleep(extra_wait)                                                     \n"
                "    # printlog(\"Additionally, waited for {} seconds.\".format(extra_wait)) "
            ))
        self.label_2.setText(_translate("Dialog", "Function Name"))
        self.func_name_lineEdit.setToolTip(
            _translate(
                "Dialog",
                "If the string is not the function name, input the correct one."
            ))
        self.ok_btn.setText(_translate("Dialog", "OK"))
        self.cancel_btn.setText(_translate("Dialog", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
