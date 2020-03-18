# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_ormviz.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1024, 768)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setContentsMargins(6, 12, 6, 6)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.matplotlibimageWidget = MatplotlibImageWidget(Dialog)
        self.matplotlibimageWidget.setProperty("figureTightLayout", True)
        self.matplotlibimageWidget.setProperty("reseverColorMap", False)
        self.matplotlibimageWidget.setColorBarToggle(True)
        self.matplotlibimageWidget.setAutoColorLimit(True)
        self.matplotlibimageWidget.setObjectName("matplotlibimageWidget")
        self.gridLayout.addWidget(self.matplotlibimageWidget, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.matplotlibimageWidget.setColorMap(_translate("Dialog", "prism"))
        self.matplotlibimageWidget.setColorBarOrientation(
            _translate("Dialog", "horizontal"))


from mpl4qt.widgets.mplimagewidget import MatplotlibImageWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
