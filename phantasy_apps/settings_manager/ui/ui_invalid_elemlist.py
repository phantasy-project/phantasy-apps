# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_invalid_elemlist.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1034, 705)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setStyleSheet("QLabel {\n"
                                 "    font-size: 20pt;\n"
                                 "    background-color: rgb(255, 170, 0);\n"
                                 "    padding: 10 5 10 5;\n"
                                 "    border-radius: 4px;\n"
                                 "}")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.treeView = QtWidgets.QTreeView(Dialog)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(
            _translate(
                "Dialog",
                "Warning: The following devices are no longer existing!"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
