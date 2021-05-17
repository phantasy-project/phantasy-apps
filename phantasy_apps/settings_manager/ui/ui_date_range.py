# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_date_range.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(831, 339)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.dateTimeRangePicker = DatetimeRangePicker(Dialog)
        self.dateTimeRangePicker.setProperty("dateFrom",
                                             QtCore.QDate(2021, 5, 3))
        self.dateTimeRangePicker.setObjectName("dateTimeRangePicker")
        self.gridLayout.addWidget(self.dateTimeRangePicker, 0, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


from phantasy_ui.widgets.dateTimeRangePicker import DatetimeRangePicker

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
