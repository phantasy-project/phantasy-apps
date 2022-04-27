# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_app.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1474, 1086)
        MainWindow.setStyleSheet("QLineEdit {\n"
                                 "    padding: 2px 2px 2px 10px;\n"
                                 "}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.beam_power_tab = QtWidgets.QWidget()
        self.beam_power_tab.setObjectName("beam_power_tab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.beam_power_tab)
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_4.setSpacing(4)
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
        self.gridLayout_2.setContentsMargins(4, 12, 4, 4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 6, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 5, 0, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.groupBox)
        self.label_22.setObjectName("label_22")
        self.gridLayout_2.addWidget(self.label_22, 7, 0, 1, 1)
        self.rep_rate_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.rep_rate_lineEdit.setObjectName("rep_rate_lineEdit")
        self.gridLayout_2.addWidget(self.rep_rate_lineEdit, 1, 1, 1, 1)
        self.pulse_length_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.pulse_length_lineEdit.setObjectName("pulse_length_lineEdit")
        self.gridLayout_2.addWidget(self.pulse_length_lineEdit, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)
        self.peak_current_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.peak_current_lineEdit.setObjectName("peak_current_lineEdit")
        self.gridLayout_2.addWidget(self.peak_current_lineEdit, 3, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.sync_btn = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sync_btn.sizePolicy().hasHeightForWidth())
        self.sync_btn.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/calc-app/refresh.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sync_btn.setIcon(icon)
        self.sync_btn.setObjectName("sync_btn")
        self.horizontalLayout_2.addWidget(self.sync_btn)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 8, 0, 1, 1)
        self.ion_mass_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.ion_mass_lineEdit.setObjectName("ion_mass_lineEdit")
        self.gridLayout_2.addWidget(self.ion_mass_lineEdit, 4, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.ion_charge_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.ion_charge_lineEdit.setObjectName("ion_charge_lineEdit")
        self.gridLayout_2.addWidget(self.ion_charge_lineEdit, 5, 1, 1, 1)
        self.duty_cycle_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.duty_cycle_lineEdit.setEnabled(False)
        self.duty_cycle_lineEdit.setReadOnly(True)
        self.duty_cycle_lineEdit.setObjectName("duty_cycle_lineEdit")
        self.gridLayout_2.addWidget(self.duty_cycle_lineEdit, 2, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 4, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 11, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.beam_energy_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.beam_energy_lineEdit.setObjectName("beam_energy_lineEdit")
        self.gridLayout_2.addWidget(self.beam_energy_lineEdit, 6, 1, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.beamSpeciesDisplayWidget = BeamSpeciesDisplayWidget(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.beamSpeciesDisplayWidget.sizePolicy().hasHeightForWidth())
        self.beamSpeciesDisplayWidget.setSizePolicy(sizePolicy)
        self.beamSpeciesDisplayWidget.setObjectName("beamSpeciesDisplayWidget")
        self.horizontalLayout_3.addWidget(self.beamSpeciesDisplayWidget)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 7, 1, 2, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.splitter)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setContentsMargins(4, 12, 4, 4)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.beam_power_lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.beam_power_lineEdit.setFont(font)
        self.beam_power_lineEdit.setReadOnly(True)
        self.beam_power_lineEdit.setObjectName("beam_power_lineEdit")
        self.gridLayout_3.addWidget(self.beam_power_lineEdit, 1, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem3, 4, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 1, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.splitter_2)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setContentsMargins(4, 12, 4, 4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
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
        self.matplotlibcurveWidget.setFigureAutoScale(True)
        self.matplotlibcurveWidget.setProperty("figureTightLayout", False)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.matplotlibcurveWidget.setFigureXYlabelFont(font)
        font = QtGui.QFont()
        font.setFamily("sans-serif")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.matplotlibcurveWidget.setFigureTitleFont(font)
        self.matplotlibcurveWidget.setProperty("figureDPI", 100.0)
        self.matplotlibcurveWidget.setFigureGridToggle(True)
        self.matplotlibcurveWidget.setFigureMTicksToggle(True)
        font = QtGui.QFont()
        font.setFamily("sans-serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.matplotlibcurveWidget.setFigureXYticksFont(font)
        self.matplotlibcurveWidget.setObjectName("matplotlibcurveWidget")
        self.verticalLayout.addWidget(self.matplotlibcurveWidget)
        self.gridLayout_4.addWidget(self.splitter_2, 0, 0, 1, 1)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/calc-app/flash_on.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.beam_power_tab, icon1, "")
        self.fsee_flux_tab = QtWidgets.QWidget()
        self.fsee_flux_tab.setObjectName("fsee_flux_tab")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.fsee_flux_tab)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.textBrowser = QtWidgets.QTextBrowser(self.fsee_flux_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setStyleSheet(
            "QTextBrowser {\n"
            "    background-color: rgb(239, 239, 239);\n"
            "}")
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_7.addWidget(self.textBrowser, 0, 0, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.fsee_flux_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_5.setContentsMargins(4, 12, 4, 4)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.area_w_lineEdit = QtWidgets.QLineEdit(self.groupBox_4)
        self.area_w_lineEdit.setObjectName("area_w_lineEdit")
        self.gridLayout_5.addWidget(self.area_w_lineEdit, 4, 1, 1, 1)
        self.area_lineEdit = QtWidgets.QLineEdit(self.groupBox_4)
        self.area_lineEdit.setReadOnly(True)
        self.area_lineEdit.setObjectName("area_lineEdit")
        self.gridLayout_5.addWidget(self.area_lineEdit, 4, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem4, 5, 0, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.groupBox_4)
        self.label_26.setObjectName("label_26")
        self.gridLayout_5.addWidget(self.label_26, 3, 2, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.groupBox_4)
        self.label_19.setObjectName("label_19")
        self.gridLayout_5.addWidget(self.label_19, 2, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.groupBox_4)
        self.label_16.setObjectName("label_16")
        self.gridLayout_5.addWidget(self.label_16, 3, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.groupBox_4)
        self.label_15.setObjectName("label_15")
        self.gridLayout_5.addWidget(self.label_15, 1, 0, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.groupBox_4)
        self.label_17.setObjectName("label_17")
        self.gridLayout_5.addWidget(self.label_17, 3, 1, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.groupBox_4)
        self.label_18.setObjectName("label_18")
        self.gridLayout_5.addWidget(self.label_18, 0, 0, 1, 1)
        self.charge_state_lineEdit = QtWidgets.QLineEdit(self.groupBox_4)
        self.charge_state_lineEdit.setObjectName("charge_state_lineEdit")
        self.gridLayout_5.addWidget(self.charge_state_lineEdit, 1, 2, 1, 1)
        self.area_h_lineEdit = QtWidgets.QLineEdit(self.groupBox_4)
        self.area_h_lineEdit.setObjectName("area_h_lineEdit")
        self.gridLayout_5.addWidget(self.area_h_lineEdit, 4, 2, 1, 1)
        self.k_lineEdit = QtWidgets.QLineEdit(self.groupBox_4)
        self.k_lineEdit.setObjectName("k_lineEdit")
        self.gridLayout_5.addWidget(self.k_lineEdit, 2, 2, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.fc_intensity_lineEdit = QtWidgets.QLineEdit(self.groupBox_4)
        self.fc_intensity_lineEdit.setObjectName("fc_intensity_lineEdit")
        self.horizontalLayout_4.addWidget(self.fc_intensity_lineEdit)
        self.toolButton = QtWidgets.QToolButton(self.groupBox_4)
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QtCore.QSize(30, 30))
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_4.addWidget(self.toolButton)
        self.gridLayout_5.addLayout(self.horizontalLayout_4, 0, 2, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_4, 1, 0, 1, 1)
        self.groupBox_5 = QtWidgets.QGroupBox(self.fsee_flux_tab)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_6.setContentsMargins(4, 12, 4, 4)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.beam_rate_lineEdit = QtWidgets.QLineEdit(self.groupBox_5)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.beam_rate_lineEdit.setFont(font)
        self.beam_rate_lineEdit.setText("")
        self.beam_rate_lineEdit.setReadOnly(True)
        self.beam_rate_lineEdit.setObjectName("beam_rate_lineEdit")
        self.gridLayout_6.addWidget(self.beam_rate_lineEdit, 0, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem5, 4, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox_5)
        self.label_9.setObjectName("label_9")
        self.gridLayout_6.addWidget(self.label_9, 0, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.groupBox_5)
        self.label_14.setObjectName("label_14")
        self.gridLayout_6.addWidget(self.label_14, 1, 0, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.groupBox_5)
        self.label_20.setObjectName("label_20")
        self.gridLayout_6.addWidget(self.label_20, 1, 2, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.groupBox_5)
        self.label_21.setObjectName("label_21")
        self.gridLayout_6.addWidget(self.label_21, 0, 2, 1, 1)
        self.beam_flux_lineEdit = QtWidgets.QLineEdit(self.groupBox_5)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.beam_flux_lineEdit.setFont(font)
        self.beam_flux_lineEdit.setReadOnly(True)
        self.beam_flux_lineEdit.setObjectName("beam_flux_lineEdit")
        self.gridLayout_6.addWidget(self.beam_flux_lineEdit, 1, 1, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_5, 2, 0, 1, 1)
        self.tabWidget.addTab(self.fsee_flux_tab, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1474, 32))
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
        self.tabWidget.setCurrentIndex(0)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.actionE_xit.triggered.connect(MainWindow.close)
        self.action_About.triggered.connect(MainWindow.onAbout)
        self.toolButton.clicked.connect(MainWindow.on_pull_fc2569)
        self.sync_btn.clicked.connect(MainWindow.on_sync_beam_state)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.tabWidget, self.pulse_length_lineEdit)
        MainWindow.setTabOrder(self.pulse_length_lineEdit,
                               self.rep_rate_lineEdit)
        MainWindow.setTabOrder(self.rep_rate_lineEdit,
                               self.duty_cycle_lineEdit)
        MainWindow.setTabOrder(self.duty_cycle_lineEdit,
                               self.peak_current_lineEdit)
        MainWindow.setTabOrder(self.peak_current_lineEdit,
                               self.ion_mass_lineEdit)
        MainWindow.setTabOrder(self.ion_mass_lineEdit,
                               self.ion_charge_lineEdit)
        MainWindow.setTabOrder(self.ion_charge_lineEdit,
                               self.beam_energy_lineEdit)
        MainWindow.setTabOrder(self.beam_energy_lineEdit, self.param_cbb)
        MainWindow.setTabOrder(self.param_cbb, self.from_lineEdit)
        MainWindow.setTabOrder(self.from_lineEdit, self.to_lineEdit)
        MainWindow.setTabOrder(self.to_lineEdit, self.step_lineEdit)
        MainWindow.setTabOrder(self.step_lineEdit, self.draw_btn)
        MainWindow.setTabOrder(self.draw_btn, self.beam_power_lineEdit)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Parameters"))
        self.label_7.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Beam Energy (W) [MeV/u]</p></body></html>"
            ))
        self.label_6.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Ion Charge (initial) (Q)</p></body></html>"
            ))
        self.label_22.setText(_translate("MainWindow", "Current Beam State"))
        self.rep_rate_lineEdit.setText(_translate("MainWindow", "5"))
        self.pulse_length_lineEdit.setText(_translate("MainWindow", "26"))
        self.label.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Pulse Length (&tau;) [μs]</p></body></html>"
            ))
        self.label_4.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Peak Current (I<span style=\" vertical-align:sub;\">p</span>) [eμA]</p></body></html>"
            ))
        self.peak_current_lineEdit.setText(_translate("MainWindow", "22"))
        self.sync_btn.setText(_translate("MainWindow", "Sync"))
        self.ion_mass_lineEdit.setText(_translate("MainWindow", "36"))
        self.label_3.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Duty Cycle (&eta;) [%]</p></body></html>"
            ))
        self.ion_charge_lineEdit.setText(_translate("MainWindow", "10"))
        self.duty_cycle_lineEdit.setText(_translate("MainWindow", "0.013"))
        self.label_5.setText(
            _translate("MainWindow",
                       "<html><head/><body><p>Ion Mass (A)</p></body></html>"))
        self.label_2.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Rep Rate (f) [Hz]</p></body></html>"))
        self.beam_energy_lineEdit.setText(_translate("MainWindow", "20.3"))
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
        self.textBrowser.setHtml(
            _translate(
                "MainWindow",
                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:\'Cantarell\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Calculate the beam flux to the FSEE user experiment station from the reading of Faraday cup (FS1_SEE:FC_D2569) intensity and estimated the beam charge state after passing through the spoil foil.</p>\n"
                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">See Also other apps:</p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- ETACHA4: Charge state estimation</p>\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Viola: Beam spot size estimation</p></body></html>"
            ))
        self.groupBox_4.setTitle(_translate("MainWindow", "Parameters"))
        self.area_w_lineEdit.setText(_translate("MainWindow", "7"))
        self.area_lineEdit.setText(_translate("MainWindow", "0.7"))
        self.label_26.setText(_translate("MainWindow", "height [mm]"))
        self.label_19.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Coefficient for FC reading fix (K), <span style=\" font-style:italic;\">I = I</span><span style=\" font-style:italic; vertical-align:sub;\">0</span><span style=\" font-style:italic;\">K</span></p></body></html>"
            ))
        self.label_16.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Beam Area [cm<span style=\" vertical-align:super;\">2</span>]</p></body></html>"
            ))
        self.label_15.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Charge State (<span style=\" font-style:italic;\">Q</span>)</p></body></html>"
            ))
        self.label_17.setText(_translate("MainWindow", "width [mm]"))
        self.label_18.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Faraday Cup D2569 [pA], <span style=\" font-style:italic;\">I</span></p></body></html>"
            ))
        self.charge_state_lineEdit.setText(_translate("MainWindow", "49"))
        self.area_h_lineEdit.setText(_translate("MainWindow", "10"))
        self.k_lineEdit.setText(_translate("MainWindow", "1.18"))
        self.fc_intensity_lineEdit.setText(_translate("MainWindow", "2.65"))
        self.toolButton.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Pull the FC reading from FS1_SEE:FC_D2569:AVG_RD.</p></body></html>"
            ))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.groupBox_5.setTitle(_translate("MainWindow", "Results"))
        self.label_9.setText(
            _translate("MainWindow",
                       "<html><head/><body><p>Beam Rate</p></body></html>"))
        self.label_14.setText(
            _translate("MainWindow",
                       "<html><head/><body><p>Beam Flux</p></body></html>"))
        self.label_20.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>pps/cm<span style=\" vertical-align:super;\">2</span></p></body></html>"
            ))
        self.label_21.setText(_translate("MainWindow", "pps"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.fsee_flux_tab),
                                  _translate("MainWindow", "FSEE Flux"))
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
from phantasy_ui.widgets.beam_species_displayWidget import BeamSpeciesDisplayWidget
from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
