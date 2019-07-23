# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_plot_region.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1700, 1000)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.intensity_plot = MatplotlibImageWidget(self.splitter)
        self.intensity_plot.setProperty("figureToolbarToggle", True)
        self.intensity_plot.setProperty("reseverColorMap", False)
        self.intensity_plot.setAutoColorLimit(True)
        self.intensity_plot.setObjectName("intensity_plot")
        self.classification_plot = MatplotlibImageWidget(self.splitter)
        self.classification_plot.setProperty("figureToolbarToggle", True)
        self.classification_plot.setObjectName("classification_plot")
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.auto_boundary_chkbox = QtWidgets.QCheckBox(Form)
        self.auto_boundary_chkbox.setChecked(True)
        self.auto_boundary_chkbox.setObjectName("auto_boundary_chkbox")
        self.gridLayout.addWidget(self.auto_boundary_chkbox, 1, 0, 1, 1)

        self.retranslateUi(Form)
        self.auto_boundary_chkbox.toggled['bool'].connect(
            Form.on_auto_boundary)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.intensity_plot.setFigureAspectRatio(_translate("Form", "auto"))
        self.intensity_plot.setFigureXlabel(
            _translate("Form", "$x\\,\\mathrm{[mm]}$"))
        self.intensity_plot.setFigureYlabel(
            _translate("Form", "$x\'\\,\\mathrm{[mrad]}$"))
        self.intensity_plot.setFigureTitle(
            _translate("Form", "Intensity Distribution"))
        self.intensity_plot.setColorMap(_translate("Form", "jet"))
        self.classification_plot.setFigureAspectRatio(
            _translate("Form", "auto"))
        self.classification_plot.setFigureXlabel(
            _translate("Form", "$x\\,\\mathrm{[mm]}$"))
        self.classification_plot.setFigureYlabel(
            _translate("Form", "$x\'\\,\\mathrm{[mrad]}$"))
        self.classification_plot.setFigureTitle(
            _translate("Form", "Signal/Noise Classification"))
        self.classification_plot.setColorMap(_translate("Form", "tab20c"))
        self.auto_boundary_chkbox.setText(
            _translate("Form", "Auto draw boundary of noise/signal"))


from mpl4qt.widgets.mplimagewidget import MatplotlibImageWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
