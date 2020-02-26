# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_app.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 1200)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.beam_power_tab = QtWidgets.QWidget()
        self.beam_power_tab.setObjectName("beam_power_tab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.beam_power_tab)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.splitter_2 = QtWidgets.QSplitter(self.beam_power_tab)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.groupBox = QtWidgets.QGroupBox(self.splitter)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)
        self.duty_cycle_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.duty_cycle_lineEdit.setObjectName("duty_cycle_lineEdit")
        self.gridLayout_2.addWidget(self.duty_cycle_lineEdit, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.peak_current_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.peak_current_lineEdit.setObjectName("peak_current_lineEdit")
        self.gridLayout_2.addWidget(self.peak_current_lineEdit, 3, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 6, 0, 1, 1)
        self.ion_mass_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.ion_mass_lineEdit.setObjectName("ion_mass_lineEdit")
        self.gridLayout_2.addWidget(self.ion_mass_lineEdit, 4, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.pulse_length_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.pulse_length_lineEdit.setObjectName("pulse_length_lineEdit")
        self.gridLayout_2.addWidget(self.pulse_length_lineEdit, 0, 1, 1, 1)
        self.beam_energy_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.beam_energy_lineEdit.setObjectName("beam_energy_lineEdit")
        self.gridLayout_2.addWidget(self.beam_energy_lineEdit, 6, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 4, 0, 1, 1)
        self.rep_rate_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.rep_rate_lineEdit.setObjectName("rep_rate_lineEdit")
        self.gridLayout_2.addWidget(self.rep_rate_lineEdit, 1, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 5, 0, 1, 1)
        self.ion_charge_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.ion_charge_lineEdit.setObjectName("ion_charge_lineEdit")
        self.gridLayout_2.addWidget(self.ion_charge_lineEdit, 5, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40,
                                           QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 7, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.splitter)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.beam_power_lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.beam_power_lineEdit.setReadOnly(True)
        self.beam_power_lineEdit.setObjectName("beam_power_lineEdit")
        self.gridLayout_3.addWidget(self.beam_power_lineEdit, 0, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 1, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.splitter_2)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_13 = QtWidgets.QLabel(self.groupBox_3)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout.addWidget(self.label_13)
        self.param_cbb = QtWidgets.QComboBox(self.groupBox_3)
        self.param_cbb.setObjectName("param_cbb")
        self.horizontalLayout.addWidget(self.param_cbb)
        self.label_10 = QtWidgets.QLabel(self.groupBox_3)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout.addWidget(self.label_10)
        self.from_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.from_lineEdit.setObjectName("from_lineEdit")
        self.horizontalLayout.addWidget(self.from_lineEdit)
        self.label_11 = QtWidgets.QLabel(self.groupBox_3)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout.addWidget(self.label_11)
        self.to_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.to_lineEdit.setObjectName("to_lineEdit")
        self.horizontalLayout.addWidget(self.to_lineEdit)
        self.label_12 = QtWidgets.QLabel(self.groupBox_3)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout.addWidget(self.label_12)
        self.step_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.step_lineEdit.setObjectName("step_lineEdit")
        self.horizontalLayout.addWidget(self.step_lineEdit)
        self.draw_btn = QtWidgets.QPushButton(self.groupBox_3)
        self.draw_btn.setObjectName("draw_btn")
        self.horizontalLayout.addWidget(self.draw_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.matplotlibcurveWidget = MatplotlibCurveWidget(self.groupBox_3)
        self.matplotlibcurveWidget.setProperty("figureTightLayout", False)
        self.matplotlibcurveWidget.setFigureGridToggle(True)
        self.matplotlibcurveWidget.setFigureAutoScale(True)
        self.matplotlibcurveWidget.setObjectName("matplotlibcurveWidget")
        self.verticalLayout.addWidget(self.matplotlibcurveWidget)
        self.gridLayout_4.addWidget(self.splitter_2, 0, 0, 1, 1)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/calc-app/flash_on.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.beam_power_tab, icon, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1600, 31))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.action_About = QtWidgets.QAction(MainWindow)
        self.action_About.setObjectName("action_About")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        self.actionE_xit.setObjectName("actionE_xit")
        self.actionContents = QtWidgets.QAction(MainWindow)
        self.actionContents.setObjectName("actionContents")
        self.menu_File.addAction(self.actionE_xit)
        self.menu_Help.addAction(self.actionContents)
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.action_About)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.actionE_xit.triggered.connect(MainWindow.close)
        self.action_About.triggered.connect(MainWindow.onAbout)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Parameters"))
        self.label_4.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Peak Current (I<span style=\" vertical-align:sub;\">p</span>) [eμA]</p></body></html>"
            ))
        self.duty_cycle_lineEdit.setText(_translate("MainWindow", "0.013"))
        self.label_3.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Duty Cycle (D) [%]</p></body></html>"))
        self.peak_current_lineEdit.setText(_translate("MainWindow", "22"))
        self.label_7.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Beam Energy (W) [MeV/u]</p></body></html>"
            ))
        self.ion_mass_lineEdit.setText(_translate("MainWindow", "36"))
        self.label_2.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Rep Rate (f) [Hz]</p></body></html>"))
        self.pulse_length_lineEdit.setText(_translate("MainWindow", "26"))
        self.beam_energy_lineEdit.setText(_translate("MainWindow", "20.3"))
        self.label_5.setText(
            _translate("MainWindow",
                       "<html><head/><body><p>Ion Mass (A)</p></body></html>"))
        self.rep_rate_lineEdit.setText(_translate("MainWindow", "5"))
        self.label_6.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Ion Charge (Q)</p></body></html>"))
        self.ion_charge_lineEdit.setText(_translate("MainWindow", "10"))
        self.label.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Pulse Length (&tau;) [μs]</p></body></html>"
            ))
        self.groupBox_2.setTitle(_translate("MainWindow", "Results"))
        self.beam_power_lineEdit.setText(_translate("MainWindow", "0.209009"))
        self.label_8.setText(_translate("MainWindow", "Beam Power (P) [Watt]"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Trend"))
        self.label_13.setText(_translate("MainWindow", "Change"))
        self.label_10.setText(_translate("MainWindow", "From"))
        self.label_11.setText(_translate("MainWindow", "To"))
        self.label_12.setText(_translate("MainWindow", "by step of"))
        self.draw_btn.setText(_translate("MainWindow", "Draw"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.beam_power_tab),
                                  _translate("MainWindow", "Beam Power"))
        self.tabWidget.setTabToolTip(
            self.tabWidget.indexOf(self.beam_power_tab),
            _translate("MainWindow", "Beam power."))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.action_About.setText(_translate("MainWindow", "&About"))
        self.action_About.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))
        self.actionE_xit.setText(_translate("MainWindow", "E&xit"))
        self.actionE_xit.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionContents.setText(_translate("MainWindow", "Contents"))
        self.actionContents.setShortcut(_translate("MainWindow", "F1"))


from mpl4qt.widgets.mplcurvewidget import MatplotlibCurveWidget
from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
