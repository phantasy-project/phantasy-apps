# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_plot_all.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1356, 851)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.matplotliberrorbarWidget = MatplotlibErrorbarWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.matplotliberrorbarWidget.sizePolicy().hasHeightForWidth())
        self.matplotliberrorbarWidget.setSizePolicy(sizePolicy)
        self.matplotliberrorbarWidget.setFigureAutoScale(True)
        font = QtGui.QFont()
        font.setFamily("sans-serif")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.matplotliberrorbarWidget.setFigureXYlabelFont(font)
        font = QtGui.QFont()
        font.setFamily("sans-serif")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.matplotliberrorbarWidget.setFigureTitleFont(font)
        self.matplotliberrorbarWidget.setFigureGridToggle(True)
        self.matplotliberrorbarWidget.setProperty("figureLegendToggle", False)
        font = QtGui.QFont()
        font.setFamily("sans-serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.matplotliberrorbarWidget.setFigureXYticksFont(font)
        self.matplotliberrorbarWidget.setObjectName("matplotliberrorbarWidget")
        self.groupBox = QtWidgets.QGroupBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.option_area = QtWidgets.QScrollArea(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.option_area.sizePolicy().hasHeightForWidth())
        self.option_area.setSizePolicy(sizePolicy)
        self.option_area.setWidgetResizable(True)
        self.option_area.setObjectName("option_area")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 891, 777))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.option_area.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.option_area)
        self.verticalLayout_2.addWidget(self.splitter)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Curves"))


from mpl4qt.widgets.mplerrorbarwidget import MatplotlibErrorbarWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
