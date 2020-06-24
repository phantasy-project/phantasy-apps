# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_app.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 975)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/app.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(
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
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_5.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout_5.setSpacing(4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.h_splitter = QtWidgets.QSplitter(self.centralwidget)
        self.h_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.h_splitter.setObjectName("h_splitter")
        self.v_splitter_1 = QtWidgets.QSplitter(self.h_splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(7)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.v_splitter_1.sizePolicy().hasHeightForWidth())
        self.v_splitter_1.setSizePolicy(sizePolicy)
        self.v_splitter_1.setOrientation(QtCore.Qt.Vertical)
        self.v_splitter_1.setObjectName("v_splitter_1")
        self.figctrl_groupBox = QtWidgets.QGroupBox(self.v_splitter_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.figctrl_groupBox.sizePolicy().hasHeightForWidth())
        self.figctrl_groupBox.setSizePolicy(sizePolicy)
        self.figctrl_groupBox.setObjectName("figctrl_groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.figctrl_groupBox)
        self.verticalLayout.setContentsMargins(2, 8, 2, 2)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.grid_btn = QtWidgets.QPushButton(self.figctrl_groupBox)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/grid.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.grid_btn.setIcon(icon1)
        self.grid_btn.setCheckable(True)
        self.grid_btn.setObjectName("grid_btn")
        self.horizontalLayout_2.addWidget(self.grid_btn)
        self.legend_btn = QtWidgets.QPushButton(self.figctrl_groupBox)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/label.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.legend_btn.setIcon(icon2)
        self.legend_btn.setCheckable(True)
        self.legend_btn.setObjectName("legend_btn")
        self.horizontalLayout_2.addWidget(self.legend_btn)
        self.autoscale_btn = QtWidgets.QPushButton(self.figctrl_groupBox)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/autoscale.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.autoscale_btn.setIcon(icon3)
        self.autoscale_btn.setCheckable(True)
        self.autoscale_btn.setObjectName("autoscale_btn")
        self.horizontalLayout_2.addWidget(self.autoscale_btn)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.figctrl_groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.xmin_lineEdit = QtWidgets.QLineEdit(self.figctrl_groupBox)
        self.xmin_lineEdit.setObjectName("xmin_lineEdit")
        self.horizontalLayout.addWidget(self.xmin_lineEdit)
        self.xmax_lineEdit = QtWidgets.QLineEdit(self.figctrl_groupBox)
        self.xmax_lineEdit.setObjectName("xmax_lineEdit")
        self.horizontalLayout.addWidget(self.xmax_lineEdit)
        self.line_3 = QtWidgets.QFrame(self.figctrl_groupBox)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout.addWidget(self.line_3)
        self.label_7 = QtWidgets.QLabel(self.figctrl_groupBox)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout.addWidget(self.label_7)
        self.ymin_lineEdit = QtWidgets.QLineEdit(self.figctrl_groupBox)
        self.ymin_lineEdit.setObjectName("ymin_lineEdit")
        self.horizontalLayout.addWidget(self.ymin_lineEdit)
        self.ymax_lineEdit = QtWidgets.QLineEdit(self.figctrl_groupBox)
        self.ymax_lineEdit.setObjectName("ymax_lineEdit")
        self.horizontalLayout.addWidget(self.ymax_lineEdit)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.splitter = QtWidgets.QSplitter(self.figctrl_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(True)
        self.splitter.setObjectName("splitter")
        self.matplotlibcurveWidget = MatplotlibCurveWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(6)
        sizePolicy.setHeightForWidth(
            self.matplotlibcurveWidget.sizePolicy().hasHeightForWidth())
        self.matplotlibcurveWidget.setSizePolicy(sizePolicy)
        self.matplotlibcurveWidget.setProperty("figureTightLayout", False)
        self.matplotlibcurveWidget.setFigureXlabel("")
        self.matplotlibcurveWidget.setFigureTitle("")
        font = QtGui.QFont()
        font.setFamily("sans-serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.matplotlibcurveWidget.setFigureXYlabelFont(font)
        font = QtGui.QFont()
        font.setFamily("sans-serif")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.matplotlibcurveWidget.setFigureTitleFont(font)
        font = QtGui.QFont()
        font.setFamily("sans-serif")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.matplotlibcurveWidget.setFigureXYticksFont(font)
        self.matplotlibcurveWidget.setObjectName("matplotlibcurveWidget")
        self.bpms_magplot = MatplotlibCurveWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.bpms_magplot.sizePolicy().hasHeightForWidth())
        self.bpms_magplot.setSizePolicy(sizePolicy)
        self.bpms_magplot.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.bpms_magplot.setProperty("figureToolbarToggle", False)
        self.bpms_magplot.setObjectName("bpms_magplot")
        self.verticalLayout.addWidget(self.splitter)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_14 = QtWidgets.QLabel(self.figctrl_groupBox)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_3.addWidget(self.label_14)
        self.line_5 = QtWidgets.QFrame(self.figctrl_groupBox)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.horizontalLayout_3.addWidget(self.line_5)
        self.label_3 = QtWidgets.QLabel(self.figctrl_groupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.show_ref_x_btn = QtWidgets.QToolButton(self.figctrl_groupBox)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/show.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.show_ref_x_btn.setIcon(icon4)
        self.show_ref_x_btn.setCheckable(True)
        self.show_ref_x_btn.setChecked(True)
        self.show_ref_x_btn.setAutoRaise(True)
        self.show_ref_x_btn.setObjectName("show_ref_x_btn")
        self.horizontalLayout_3.addWidget(self.show_ref_x_btn)
        self.label_15 = QtWidgets.QLabel(self.figctrl_groupBox)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_3.addWidget(self.label_15)
        self.show_ref_y_btn = QtWidgets.QToolButton(self.figctrl_groupBox)
        self.show_ref_y_btn.setToolTip("")
        self.show_ref_y_btn.setIcon(icon4)
        self.show_ref_y_btn.setCheckable(True)
        self.show_ref_y_btn.setChecked(True)
        self.show_ref_y_btn.setAutoRaise(True)
        self.show_ref_y_btn.setObjectName("show_ref_y_btn")
        self.horizontalLayout_3.addWidget(self.show_ref_y_btn)
        self.line_6 = QtWidgets.QFrame(self.figctrl_groupBox)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.horizontalLayout_3.addWidget(self.line_6)
        self.last_one_rbtn = QtWidgets.QRadioButton(self.figctrl_groupBox)
        self.last_one_rbtn.setObjectName("last_one_rbtn")
        self.horizontalLayout_3.addWidget(self.last_one_rbtn)
        self.last_five_rbtn = QtWidgets.QRadioButton(self.figctrl_groupBox)
        self.last_five_rbtn.setObjectName("last_five_rbtn")
        self.horizontalLayout_3.addWidget(self.last_five_rbtn)
        self.line_4 = QtWidgets.QFrame(self.figctrl_groupBox)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout_3.addWidget(self.line_4)
        self.update_refline_chkbox = QtWidgets.QCheckBox(self.figctrl_groupBox)
        self.update_refline_chkbox.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/update.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.update_refline_chkbox.setIcon(icon5)
        self.update_refline_chkbox.setObjectName("update_refline_chkbox")
        self.horizontalLayout_3.addWidget(self.update_refline_chkbox)
        self.save_traj_btn = QtWidgets.QToolButton(self.figctrl_groupBox)
        self.save_traj_btn.setEnabled(False)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/save.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.save_traj_btn.setIcon(icon6)
        self.save_traj_btn.setAutoRaise(True)
        self.save_traj_btn.setObjectName("save_traj_btn")
        self.horizontalLayout_3.addWidget(self.save_traj_btn)
        self.load_traj_btn = QtWidgets.QToolButton(self.figctrl_groupBox)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/open.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.load_traj_btn.setIcon(icon7)
        self.load_traj_btn.setAutoRaise(True)
        self.load_traj_btn.setObjectName("load_traj_btn")
        self.horizontalLayout_3.addWidget(self.load_traj_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.show_bpm_mag_btn = QtWidgets.QToolButton(self.figctrl_groupBox)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/intensity.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.show_bpm_mag_btn.setIcon(icon8)
        self.show_bpm_mag_btn.setCheckable(True)
        self.show_bpm_mag_btn.setAutoRaise(True)
        self.show_bpm_mag_btn.setObjectName("show_bpm_mag_btn")
        self.horizontalLayout_3.addWidget(self.show_bpm_mag_btn)
        self.toolButton = QtWidgets.QToolButton(self.figctrl_groupBox)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/dv.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.toolButton.setIcon(icon9)
        self.toolButton.setAutoRaise(True)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_3.addWidget(self.toolButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.daqctrl_groupBox = QtWidgets.QGroupBox(self.v_splitter_1)
        self.daqctrl_groupBox.setAlignment(QtCore.Qt.AlignLeading
                                           | QtCore.Qt.AlignLeft
                                           | QtCore.Qt.AlignVCenter)
        self.daqctrl_groupBox.setObjectName("daqctrl_groupBox")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.daqctrl_groupBox)
        self.gridLayout_6.setContentsMargins(2, 8, 2, 2)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.monitors_hbox = QtWidgets.QHBoxLayout()
        self.monitors_hbox.setSpacing(4)
        self.monitors_hbox.setObjectName("monitors_hbox")
        self.label_8 = QtWidgets.QLabel(self.daqctrl_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setObjectName("label_8")
        self.monitors_hbox.addWidget(self.label_8)
        self.line = QtWidgets.QFrame(self.daqctrl_groupBox)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.monitors_hbox.addWidget(self.line)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.use_all_bpms_rbtn = QtWidgets.QRadioButton(self.daqctrl_groupBox)
        self.use_all_bpms_rbtn.setObjectName("use_all_bpms_rbtn")
        self.buttonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.use_all_bpms_rbtn)
        self.gridLayout_5.addWidget(self.use_all_bpms_rbtn, 0, 1, 1, 1)
        self.bpm_unit_millimeter_rbtn = QtWidgets.QRadioButton(
            self.daqctrl_groupBox)
        self.bpm_unit_millimeter_rbtn.setObjectName("bpm_unit_millimeter_rbtn")
        self.buttonGroup_2 = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup_2.setObjectName("buttonGroup_2")
        self.buttonGroup_2.addButton(self.bpm_unit_millimeter_rbtn)
        self.gridLayout_5.addWidget(self.bpm_unit_millimeter_rbtn, 1, 2, 1, 1)
        self.use_selected_bpms_rbtn = QtWidgets.QRadioButton(
            self.daqctrl_groupBox)
        self.use_selected_bpms_rbtn.setObjectName("use_selected_bpms_rbtn")
        self.buttonGroup.addButton(self.use_selected_bpms_rbtn)
        self.gridLayout_5.addWidget(self.use_selected_bpms_rbtn, 0, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.daqctrl_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setObjectName("label_9")
        self.gridLayout_5.addWidget(self.label_9, 0, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.daqctrl_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setObjectName("label_10")
        self.gridLayout_5.addWidget(self.label_10, 1, 0, 1, 1)
        self.bpm_unit_meter_rbtn = QtWidgets.QRadioButton(
            self.daqctrl_groupBox)
        self.bpm_unit_meter_rbtn.setObjectName("bpm_unit_meter_rbtn")
        self.buttonGroup_2.addButton(self.bpm_unit_meter_rbtn)
        self.gridLayout_5.addWidget(self.bpm_unit_meter_rbtn, 1, 1, 1, 1)
        self.field1_cbb = QtWidgets.QComboBox(self.daqctrl_groupBox)
        self.field1_cbb.setObjectName("field1_cbb")
        self.gridLayout_5.addWidget(self.field1_cbb, 0, 4, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.daqctrl_groupBox)
        self.label_12.setObjectName("label_12")
        self.gridLayout_5.addWidget(self.label_12, 0, 3, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.daqctrl_groupBox)
        self.label_13.setObjectName("label_13")
        self.gridLayout_5.addWidget(self.label_13, 1, 3, 1, 1)
        self.field2_cbb = QtWidgets.QComboBox(self.daqctrl_groupBox)
        self.field2_cbb.setObjectName("field2_cbb")
        self.gridLayout_5.addWidget(self.field2_cbb, 1, 4, 1, 1)
        self.monitors_hbox.addLayout(self.gridLayout_5)
        self.gridLayout_6.addLayout(self.monitors_hbox, 0, 0, 1, 1)
        self.daq_hbox = QtWidgets.QHBoxLayout()
        self.daq_hbox.setSpacing(4)
        self.daq_hbox.setObjectName("daq_hbox")
        self.label_11 = QtWidgets.QLabel(self.daqctrl_groupBox)
        self.label_11.setObjectName("label_11")
        self.daq_hbox.addWidget(self.label_11)
        self.line_2 = QtWidgets.QFrame(self.daqctrl_groupBox)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.daq_hbox.addWidget(self.line_2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.daqctrl_groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.daqctrl_groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.start_btn = QtWidgets.QPushButton(self.daqctrl_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.start_btn.sizePolicy().hasHeightForWidth())
        self.start_btn.setSizePolicy(sizePolicy)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/start.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.start_btn.setIcon(icon10)
        self.start_btn.setIconSize(QtCore.QSize(20, 20))
        self.start_btn.setObjectName("start_btn")
        self.gridLayout.addWidget(self.start_btn, 1, 1, 1, 1)
        self.stop_btn = QtWidgets.QPushButton(self.daqctrl_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stop_btn.sizePolicy().hasHeightForWidth())
        self.stop_btn.setSizePolicy(sizePolicy)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icons/stop.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.stop_btn.setIcon(icon11)
        self.stop_btn.setIconSize(QtCore.QSize(20, 20))
        self.stop_btn.setObjectName("stop_btn")
        self.gridLayout.addWidget(self.stop_btn, 1, 2, 1, 1)
        self.freq_dSpinbox = QtWidgets.QDoubleSpinBox(self.daqctrl_groupBox)
        self.freq_dSpinbox.setDecimals(1)
        self.freq_dSpinbox.setMinimum(0.0)
        self.freq_dSpinbox.setMaximum(10.0)
        self.freq_dSpinbox.setSingleStep(0.5)
        self.freq_dSpinbox.setProperty("value", 1.0)
        self.freq_dSpinbox.setObjectName("freq_dSpinbox")
        self.gridLayout.addWidget(self.freq_dSpinbox, 0, 1, 1, 2)
        self.daq_hbox.addLayout(self.gridLayout)
        self.gridLayout_6.addLayout(self.daq_hbox, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(75, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem1, 0, 1, 1, 1)
        self.v_splitter_2 = QtWidgets.QSplitter(self.h_splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.v_splitter_2.sizePolicy().hasHeightForWidth())
        self.v_splitter_2.setSizePolicy(sizePolicy)
        self.v_splitter_2.setMinimumSize(QtCore.QSize(350, 0))
        self.v_splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.v_splitter_2.setObjectName("v_splitter_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.v_splitter_2)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_4.setContentsMargins(2, 8, 2, 2)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(4)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_7.addWidget(self.label_4)
        self.select_all_bpms_btn = QtWidgets.QToolButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.select_all_bpms_btn.sizePolicy().hasHeightForWidth())
        self.select_all_bpms_btn.setSizePolicy(sizePolicy)
        self.select_all_bpms_btn.setText("")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/icons/select-all.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.select_all_bpms_btn.setIcon(icon12)
        self.select_all_bpms_btn.setObjectName("select_all_bpms_btn")
        self.horizontalLayout_7.addWidget(self.select_all_bpms_btn)
        self.inverse_bpm_selection_btn = QtWidgets.QToolButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.inverse_bpm_selection_btn.sizePolicy().hasHeightForWidth())
        self.inverse_bpm_selection_btn.setSizePolicy(sizePolicy)
        self.inverse_bpm_selection_btn.setText("")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/icons/invert-selection.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.inverse_bpm_selection_btn.setIcon(icon13)
        self.inverse_bpm_selection_btn.setObjectName(
            "inverse_bpm_selection_btn")
        self.horizontalLayout_7.addWidget(self.inverse_bpm_selection_btn)
        self.select_bpms_btn = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.select_bpms_btn.sizePolicy().hasHeightForWidth())
        self.select_bpms_btn.setSizePolicy(sizePolicy)
        self.select_bpms_btn.setObjectName("select_bpms_btn")
        self.horizontalLayout_7.addWidget(self.select_bpms_btn)
        self.gridLayout_4.addLayout(self.horizontalLayout_7, 0, 0, 1, 1)
        self.bpms_treeView = QtWidgets.QTreeView(self.groupBox_3)
        self.bpms_treeView.setObjectName("bpms_treeView")
        self.gridLayout_4.addWidget(self.bpms_treeView, 1, 0, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.v_splitter_2)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_3.setContentsMargins(2, 8, 2, 2)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setSpacing(4)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_6 = QtWidgets.QLabel(self.groupBox_4)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_8.addWidget(self.label_6)
        self.select_all_cors_btn = QtWidgets.QToolButton(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.select_all_cors_btn.sizePolicy().hasHeightForWidth())
        self.select_all_cors_btn.setSizePolicy(sizePolicy)
        self.select_all_cors_btn.setText("")
        self.select_all_cors_btn.setIcon(icon12)
        self.select_all_cors_btn.setObjectName("select_all_cors_btn")
        self.horizontalLayout_8.addWidget(self.select_all_cors_btn)
        self.inverse_cor_selection_btn = QtWidgets.QToolButton(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.inverse_cor_selection_btn.sizePolicy().hasHeightForWidth())
        self.inverse_cor_selection_btn.setSizePolicy(sizePolicy)
        self.inverse_cor_selection_btn.setText("")
        self.inverse_cor_selection_btn.setIcon(icon13)
        self.inverse_cor_selection_btn.setObjectName(
            "inverse_cor_selection_btn")
        self.horizontalLayout_8.addWidget(self.inverse_cor_selection_btn)
        self.select_cors_btn = QtWidgets.QPushButton(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.select_cors_btn.sizePolicy().hasHeightForWidth())
        self.select_cors_btn.setSizePolicy(sizePolicy)
        self.select_cors_btn.setObjectName("select_cors_btn")
        self.horizontalLayout_8.addWidget(self.select_cors_btn)
        self.gridLayout_3.addLayout(self.horizontalLayout_8, 0, 0, 1, 1)
        self.cors_treeView = QtWidgets.QTreeView(self.groupBox_4)
        self.cors_treeView.setObjectName("cors_treeView")
        self.gridLayout_3.addWidget(self.cors_treeView, 1, 0, 1, 1)
        self.horizontalLayout_5.addWidget(self.h_splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1300, 23))
        self.menubar.setObjectName("menubar")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/icons/exit.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.actionE_xit.setIcon(icon14)
        self.actionE_xit.setObjectName("actionE_xit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/icons/info.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon15)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/icons/qt.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.actionAbout_Qt.setIcon(icon16)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionContents = QtWidgets.QAction(MainWindow)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(":/icons/help.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.actionContents.setIcon(icon17)
        self.actionContents.setObjectName("actionContents")
        self.actionORM = QtWidgets.QAction(MainWindow)
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap(":/icons/matrix.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionORM.setIcon(icon18)
        self.actionORM.setObjectName("actionORM")
        self.actionLoad_Lattice = QtWidgets.QAction(MainWindow)
        icon19 = QtGui.QIcon()
        icon19.addPixmap(QtGui.QPixmap(":/icons/load_lattice.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoad_Lattice.setIcon(icon19)
        self.actionLoad_Lattice.setObjectName("actionLoad_Lattice")
        self.actionShaded_As_Selection = QtWidgets.QAction(MainWindow)
        icon20 = QtGui.QIcon()
        icon20.addPixmap(QtGui.QPixmap(":/icons/shade_as_selection.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionShaded_As_Selection.setIcon(icon20)
        self.actionShaded_As_Selection.setObjectName(
            "actionShaded_As_Selection")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setIcon(icon6)
        self.actionSave.setObjectName("actionSave")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setIcon(icon7)
        self.actionOpen.setObjectName("actionOpen")
        self.menu_Help.addAction(self.actionContents)
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menubar.addAction(self.menu_Help.menuAction())
        self.toolBar.addAction(self.actionLoad_Lattice)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionORM)
        self.toolBar.addAction(self.actionShaded_As_Selection)
        self.toolBar.addAction(self.actionE_xit)

        self.retranslateUi(MainWindow)
        self.actionAbout.triggered.connect(MainWindow.onAbout)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.actionE_xit.triggered.connect(MainWindow.close)
        self.actionContents.triggered.connect(MainWindow.onHelp)
        self.actionORM.triggered.connect(MainWindow.on_launch_orm)
        self.actionLoad_Lattice.triggered.connect(
            MainWindow.onLoadLatticeAction)
        self.grid_btn.toggled['bool'].connect(
            self.matplotlibcurveWidget.setFigureGridToggle)
        self.legend_btn.toggled['bool'].connect(
            self.matplotlibcurveWidget.setLegendToggle)
        self.autoscale_btn.toggled['bool'].connect(
            self.matplotlibcurveWidget.setFigureAutoScale)
        self.autoscale_btn.toggled['bool'].connect(MainWindow.on_auto_xyscale)
        self.field1_cbb.currentTextChanged['QString'].connect(
            MainWindow.on_field1_updated)
        self.field2_cbb.currentTextChanged['QString'].connect(
            MainWindow.on_field2_updated)
        self.matplotlibcurveWidget.gridOnUpdated['bool'].connect(
            self.grid_btn.setChecked)
        self.matplotlibcurveWidget.legendOnUpdated['bool'].connect(
            self.legend_btn.setChecked)
        self.matplotlibcurveWidget.autoScaleOnUpdated['bool'].connect(
            self.autoscale_btn.setChecked)
        self.save_traj_btn.clicked.connect(MainWindow.on_save_trajectory)
        self.load_traj_btn.clicked.connect(MainWindow.on_load_trajectory)
        self.update_refline_chkbox.toggled['bool'].connect(
            self.save_traj_btn.setDisabled)
        self.show_ref_x_btn.toggled['bool'].connect(MainWindow.on_show_ref_x)
        self.show_bpm_mag_btn.toggled['bool'].connect(
            self.bpms_magplot.setVisible)
        self.actionShaded_As_Selection.triggered.connect(
            MainWindow.onShadedAsSelection)
        self.show_ref_y_btn.toggled['bool'].connect(MainWindow.on_show_ref_y)
        self.toolButton.clicked.connect(MainWindow.on_open_dv)
        self.actionSave.triggered.connect(MainWindow.on_save)
        self.actionOpen.triggered.connect(MainWindow.on_open)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.figctrl_groupBox.setTitle(
            _translate("MainWindow", "Data Visualization"))
        self.grid_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Show/hide grid</p></body></html>"))
        self.grid_btn.setText(_translate("MainWindow", "Grid"))
        self.legend_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Show/hide legend</p></body></html>"))
        self.legend_btn.setText(_translate("MainWindow", "Legend"))
        self.autoscale_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Autoset XY scale</p></body></html>"))
        self.autoscale_btn.setText(_translate("MainWindow", "Scale"))
        self.label.setText(_translate("MainWindow", "X-Limit"))
        self.label_7.setText(_translate("MainWindow", "Y-Limit"))
        self.label_14.setText(_translate("MainWindow", "Reference Trajectory"))
        self.label_3.setText(_translate("MainWindow", "X"))
        self.show_ref_x_btn.setText(_translate("MainWindow", "..."))
        self.label_15.setText(_translate("MainWindow", "Y"))
        self.show_ref_y_btn.setText(_translate("MainWindow", "..."))
        self.last_one_rbtn.setToolTip(
            _translate("MainWindow", "Average last one (1) shot."))
        self.last_one_rbtn.setText(_translate("MainWindow", "1"))
        self.last_five_rbtn.setToolTip(
            _translate("MainWindow", "Average last five (5) shots."))
        self.last_five_rbtn.setText(_translate("MainWindow", "5"))
        self.update_refline_chkbox.setToolTip(
            _translate("MainWindow",
                       "Check/uncheck to update/freeze reference X&Y."))
        self.save_traj_btn.setToolTip(
            _translate("MainWindow", "Save reference trajectory into a file."))
        self.save_traj_btn.setText(_translate("MainWindow", "Save"))
        self.load_traj_btn.setToolTip(
            _translate("MainWindow", "Load reference trajectory from a file."))
        self.load_traj_btn.setText(_translate("MainWindow", "Load"))
        self.show_bpm_mag_btn.setToolTip(
            _translate("MainWindow", "Show/hide BPM intensities"))
        self.show_bpm_mag_btn.setText(_translate("MainWindow", "Show MAG"))
        self.toolButton.setToolTip(
            _translate("MainWindow",
                       "View BPM intensity in \'Device Viewer\'."))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.daqctrl_groupBox.setTitle(
            _translate("MainWindow", "Controls Panel"))
        self.label_8.setText(_translate("MainWindow", "Monitors"))
        self.use_all_bpms_rbtn.setText(_translate("MainWindow", "Use All"))
        self.bpm_unit_millimeter_rbtn.setText(
            _translate("MainWindow", "Millimeter"))
        self.use_selected_bpms_rbtn.setText(
            _translate("MainWindow", "Use Selected"))
        self.label_9.setText(_translate("MainWindow", "Monitoring"))
        self.label_10.setText(_translate("MainWindow", "Measurement Unit"))
        self.bpm_unit_meter_rbtn.setText(_translate("MainWindow", "Meter"))
        self.field1_cbb.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Field to monitor, show as 1<span style=\" vertical-align:super;\">st</span> Line</p></body></html>"
            ))
        self.label_12.setText(_translate("MainWindow", "Field-1"))
        self.label_13.setText(_translate("MainWindow", "Field-2"))
        self.field2_cbb.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Field to monitor, show as 2<span style=\" vertical-align:super;\">nd</span> Line</p></body></html>"
            ))
        self.label_11.setText(_translate("MainWindow", "DAQ"))
        self.label_2.setText(_translate("MainWindow", "Frequency"))
        self.label_5.setText(_translate("MainWindow", "Action"))
        self.start_btn.setToolTip(
            _translate("MainWindow", "Start DAQ (Ctrl+R)."))
        self.start_btn.setText(_translate("MainWindow", "Start"))
        self.start_btn.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.stop_btn.setToolTip(
            _translate("MainWindow", "Stop DAQ (Ctrl+period)."))
        self.stop_btn.setText(_translate("MainWindow", "Stop"))
        self.stop_btn.setShortcut(_translate("MainWindow", "Ctrl+."))
        self.freq_dSpinbox.setSuffix(_translate("MainWindow", " Hz"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Monitors"))
        self.label_4.setText(_translate("MainWindow", "Monitors (BPMs)"))
        self.select_all_bpms_btn.setToolTip(
            _translate("MainWindow",
                       "<html><head/><body><p>Select All</p></body></html>"))
        self.inverse_bpm_selection_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Inverse Current Selection</p></body></html>"
            ))
        self.select_bpms_btn.setText(_translate("MainWindow", "Choose"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Correctors"))
        self.label_6.setText(_translate("MainWindow", "Correctors"))
        self.select_all_cors_btn.setToolTip(
            _translate("MainWindow",
                       "<html><head/><body><p>Select All</p></body></html>"))
        self.inverse_cor_selection_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Inverse Current Selection</p></body></html>"
            ))
        self.select_cors_btn.setText(_translate("MainWindow", "Choose"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionE_xit.setText(_translate("MainWindow", "E&xit"))
        self.actionE_xit.setToolTip(
            _translate("MainWindow", "Exit this application (Ctrl+W)."))
        self.actionE_xit.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))
        self.actionContents.setText(_translate("MainWindow", "Contents"))
        self.actionContents.setShortcut(_translate("MainWindow", "F1"))
        self.actionORM.setText(
            _translate("MainWindow", "Trajectory Response Matrix"))
        self.actionORM.setToolTip(
            _translate(
                "MainWindow",
                "Launch the app for trajectory response matrix measure and apply (Ctrl+Shift+M)."
            ))
        self.actionORM.setShortcut(_translate("MainWindow", "Ctrl+Shift+M"))
        self.actionLoad_Lattice.setText(
            _translate("MainWindow", "Load Lattice"))
        self.actionLoad_Lattice.setToolTip(
            _translate("MainWindow", "Load lattice (Ctrl+Shift+L)."))
        self.actionLoad_Lattice.setShortcut(
            _translate("MainWindow", "Ctrl+Shift+L"))
        self.actionShaded_As_Selection.setText(
            _translate("MainWindow", "Shaded As Selection"))
        self.actionShaded_As_Selection.setToolTip(
            _translate(
                "MainWindow",
                "Auto-select devices in the shaded area (Alt+Shift+S)."))
        self.actionShaded_As_Selection.setShortcut(
            _translate("MainWindow", "Alt+Shift+S"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))


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
