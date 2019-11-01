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
        MainWindow.resize(1920, 1440)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setContentsMargins(10, 10, 10, 10)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.v_splitter = QtWidgets.QSplitter(self.centralwidget)
        self.v_splitter.setOrientation(QtCore.Qt.Vertical)
        self.v_splitter.setObjectName("v_splitter")
        self.ctrl_gbox = QtWidgets.QGroupBox(self.v_splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.ctrl_gbox.sizePolicy().hasHeightForWidth())
        self.ctrl_gbox.setSizePolicy(sizePolicy)
        self.ctrl_gbox.setSizeIncrement(QtCore.QSize(0, 0))
        self.ctrl_gbox.setObjectName("ctrl_gbox")
        self.gridLayout = QtWidgets.QGridLayout(self.ctrl_gbox)
        self.gridLayout.setContentsMargins(8, 8, 8, 8)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.device_hbox = QtWidgets.QHBoxLayout()
        self.device_hbox.setSpacing(6)
        self.device_hbox.setObjectName("device_hbox")
        self.ems_names_cbb = QtWidgets.QComboBox(self.ctrl_gbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ems_names_cbb.sizePolicy().hasHeightForWidth())
        self.ems_names_cbb.setSizePolicy(sizePolicy)
        self.ems_names_cbb.setStyleSheet("QComboBox {\n"
                                         "    font-family: monospace;\n"
                                         "}")
        self.ems_names_cbb.setObjectName("ems_names_cbb")
        self.device_hbox.addWidget(self.ems_names_cbb)
        self.info_lbl = QtWidgets.QLabel(self.ctrl_gbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.info_lbl.sizePolicy().hasHeightForWidth())
        self.info_lbl.setSizePolicy(sizePolicy)
        self.info_lbl.setStyleSheet("")
        self.info_lbl.setScaledContents(False)
        self.info_lbl.setObjectName("info_lbl")
        self.device_hbox.addWidget(self.info_lbl)
        self.ems_detail_btn = QtWidgets.QToolButton(self.ctrl_gbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ems_detail_btn.sizePolicy().hasHeightForWidth())
        self.ems_detail_btn.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/view-details.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ems_detail_btn.setIcon(icon)
        self.ems_detail_btn.setIconSize(QtCore.QSize(20, 20))
        self.ems_detail_btn.setAutoRaise(True)
        self.ems_detail_btn.setObjectName("ems_detail_btn")
        self.device_hbox.addWidget(self.ems_detail_btn)
        self.label_14 = QtWidgets.QLabel(self.ctrl_gbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setObjectName("label_14")
        self.device_hbox.addWidget(self.label_14)
        self.ems_orientation_cbb = QtWidgets.QComboBox(self.ctrl_gbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ems_orientation_cbb.sizePolicy().hasHeightForWidth())
        self.ems_orientation_cbb.setSizePolicy(sizePolicy)
        self.ems_orientation_cbb.setStyleSheet("QComboBox {\n"
                                               "    font-family: monospace;\n"
                                               "}")
        self.ems_orientation_cbb.setObjectName("ems_orientation_cbb")
        self.ems_orientation_cbb.addItem("")
        self.ems_orientation_cbb.addItem("")
        self.device_hbox.addWidget(self.ems_orientation_cbb)
        self.status_lbl = QtWidgets.QLabel(self.ctrl_gbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.status_lbl.sizePolicy().hasHeightForWidth())
        self.status_lbl.setSizePolicy(sizePolicy)
        self.status_lbl.setText("")
        self.status_lbl.setPixmap(QtGui.QPixmap(":/icons/inactive.png"))
        self.status_lbl.setObjectName("status_lbl")
        self.device_hbox.addWidget(self.status_lbl)
        self.run_btn = QtWidgets.QPushButton(self.ctrl_gbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.run_btn.sizePolicy().hasHeightForWidth())
        self.run_btn.setSizePolicy(sizePolicy)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/run.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.run_btn.setIcon(icon1)
        self.run_btn.setIconSize(QtCore.QSize(24, 24))
        self.run_btn.setObjectName("run_btn")
        self.device_hbox.addWidget(self.run_btn)
        self.abort_btn = QtWidgets.QPushButton(self.ctrl_gbox)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/stop.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.abort_btn.setIcon(icon2)
        self.abort_btn.setObjectName("abort_btn")
        self.device_hbox.addWidget(self.abort_btn)
        self.fetch_data_btn = QtWidgets.QPushButton(self.ctrl_gbox)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/fetch.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.fetch_data_btn.setIcon(icon3)
        self.fetch_data_btn.setObjectName("fetch_data_btn")
        self.device_hbox.addWidget(self.fetch_data_btn)
        self.adv_ctrl_chkbox = QtWidgets.QCheckBox(self.ctrl_gbox)
        self.adv_ctrl_chkbox.setObjectName("adv_ctrl_chkbox")
        self.device_hbox.addWidget(self.adv_ctrl_chkbox)
        self.verticalLayout_2.addLayout(self.device_hbox)
        self.adv_ctrl_widget = QtWidgets.QWidget(self.ctrl_gbox)
        self.adv_ctrl_widget.setObjectName("adv_ctrl_widget")
        self.adv_ctrl_hbox = QtWidgets.QHBoxLayout(self.adv_ctrl_widget)
        self.adv_ctrl_hbox.setContentsMargins(0, 0, 0, 0)
        self.adv_ctrl_hbox.setSpacing(6)
        self.adv_ctrl_hbox.setObjectName("adv_ctrl_hbox")
        self.label_26 = QtWidgets.QLabel(self.adv_ctrl_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy)
        self.label_26.setObjectName("label_26")
        self.adv_ctrl_hbox.addWidget(self.label_26)
        self.bias_volt_dsbox = QtWidgets.QDoubleSpinBox(self.adv_ctrl_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.bias_volt_dsbox.sizePolicy().hasHeightForWidth())
        self.bias_volt_dsbox.setSizePolicy(sizePolicy)
        self.bias_volt_dsbox.setMinimum(-1000.0)
        self.bias_volt_dsbox.setMaximum(1000.0)
        self.bias_volt_dsbox.setProperty("value", -200.0)
        self.bias_volt_dsbox.setObjectName("bias_volt_dsbox")
        self.adv_ctrl_hbox.addWidget(self.bias_volt_dsbox)
        self.is_enabled_lbl = QtWidgets.QLabel(self.adv_ctrl_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.is_enabled_lbl.sizePolicy().hasHeightForWidth())
        self.is_enabled_lbl.setSizePolicy(sizePolicy)
        self.is_enabled_lbl.setObjectName("is_enabled_lbl")
        self.adv_ctrl_hbox.addWidget(self.is_enabled_lbl)
        self.label_25 = QtWidgets.QLabel(self.adv_ctrl_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy)
        self.label_25.setObjectName("label_25")
        self.adv_ctrl_hbox.addWidget(self.label_25)
        self.vpos_lineEdit = QtWidgets.QLineEdit(self.adv_ctrl_widget)
        self.vpos_lineEdit.setObjectName("vpos_lineEdit")
        self.adv_ctrl_hbox.addWidget(self.vpos_lineEdit)
        self.retract_btn = QtWidgets.QPushButton(self.adv_ctrl_widget)
        self.retract_btn.setIconSize(QtCore.QSize(28, 28))
        self.retract_btn.setObjectName("retract_btn")
        self.adv_ctrl_hbox.addWidget(self.retract_btn)
        self.is_outlimit_lbl = QtWidgets.QLabel(self.adv_ctrl_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.is_outlimit_lbl.sizePolicy().hasHeightForWidth())
        self.is_outlimit_lbl.setSizePolicy(sizePolicy)
        self.is_outlimit_lbl.setToolTip("")
        self.is_outlimit_lbl.setObjectName("is_outlimit_lbl")
        self.adv_ctrl_hbox.addWidget(self.is_outlimit_lbl)
        self.reset_itlk_btn = QtWidgets.QToolButton(self.adv_ctrl_widget)
        self.reset_itlk_btn.setObjectName("reset_itlk_btn")
        self.adv_ctrl_hbox.addWidget(self.reset_itlk_btn)
        self.is_itlk_lbl = QtWidgets.QLabel(self.adv_ctrl_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.is_itlk_lbl.sizePolicy().hasHeightForWidth())
        self.is_itlk_lbl.setSizePolicy(sizePolicy)
        self.is_itlk_lbl.setObjectName("is_itlk_lbl")
        self.adv_ctrl_hbox.addWidget(self.is_itlk_lbl)
        self.verticalLayout_2.addWidget(self.adv_ctrl_widget)
        self.verticalLayout_5.addLayout(self.verticalLayout_2)
        self.line = QtWidgets.QFrame(self.ctrl_gbox)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_5.addWidget(self.line)
        self.splitter = QtWidgets.QSplitter(self.ctrl_gbox)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.gridWidget = QtWidgets.QWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gridWidget.sizePolicy().hasHeightForWidth())
        self.gridWidget.setSizePolicy(sizePolicy)
        self.gridWidget.setObjectName("gridWidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gridWidget)
        self.gridLayout_4.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_4.setContentsMargins(8, 0, 0, 0)
        self.gridLayout_4.setHorizontalSpacing(10)
        self.gridLayout_4.setVerticalSpacing(12)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.fetch_config_btn = QtWidgets.QToolButton(self.gridWidget)
        self.fetch_config_btn.setIcon(icon3)
        self.fetch_config_btn.setIconSize(QtCore.QSize(28, 28))
        self.fetch_config_btn.setObjectName("fetch_config_btn")
        self.gridLayout_4.addWidget(self.fetch_config_btn, 6, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Source Han Sans CN")
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignRight
                                   | QtCore.Qt.AlignTrailing
                                   | QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName("label_16")
        self.gridLayout_4.addWidget(self.label_16, 6, 3, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Source Han Sans CN")
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignRight
                                   | QtCore.Qt.AlignTrailing
                                   | QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.gridLayout_4.addWidget(self.label_15, 5, 3, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_4.addWidget(self.line_2, 4, 3, 1, 3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(4, -1, -1, -1)
        self.horizontalLayout_5.setSpacing(8)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pos_steps_lbl = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pos_steps_lbl.sizePolicy().hasHeightForWidth())
        self.pos_steps_lbl.setSizePolicy(sizePolicy)
        self.pos_steps_lbl.setObjectName("pos_steps_lbl")
        self.horizontalLayout_5.addWidget(self.pos_steps_lbl)
        self.label_17 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_5.addWidget(self.label_17)
        self.pos_begin_dsbox = QtWidgets.QDoubleSpinBox(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pos_begin_dsbox.sizePolicy().hasHeightForWidth())
        self.pos_begin_dsbox.setSizePolicy(sizePolicy)
        self.pos_begin_dsbox.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.pos_begin_dsbox.setMinimum(-9999.0)
        self.pos_begin_dsbox.setMaximum(9999.0)
        self.pos_begin_dsbox.setObjectName("pos_begin_dsbox")
        self.horizontalLayout_5.addWidget(self.pos_begin_dsbox)
        self.label_18 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_5.addWidget(self.label_18)
        self.pos_end_dsbox = QtWidgets.QDoubleSpinBox(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pos_end_dsbox.sizePolicy().hasHeightForWidth())
        self.pos_end_dsbox.setSizePolicy(sizePolicy)
        self.pos_end_dsbox.setMinimum(-9999.0)
        self.pos_end_dsbox.setMaximum(9999.0)
        self.pos_end_dsbox.setObjectName("pos_end_dsbox")
        self.horizontalLayout_5.addWidget(self.pos_end_dsbox)
        self.label_19 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_5.addWidget(self.label_19)
        self.pos_step_dsbox = QtWidgets.QDoubleSpinBox(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pos_step_dsbox.sizePolicy().hasHeightForWidth())
        self.pos_step_dsbox.setSizePolicy(sizePolicy)
        self.pos_step_dsbox.setSuffix("")
        self.pos_step_dsbox.setMinimum(-9999.0)
        self.pos_step_dsbox.setMaximum(9999.0)
        self.pos_step_dsbox.setSingleStep(0.1)
        self.pos_step_dsbox.setObjectName("pos_step_dsbox")
        self.horizontalLayout_5.addWidget(self.pos_step_dsbox)
        self.label_5 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Serif")
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.pos_settling_time_dsbox = QtWidgets.QDoubleSpinBox(
            self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pos_settling_time_dsbox.sizePolicy().hasHeightForWidth())
        self.pos_settling_time_dsbox.setSizePolicy(sizePolicy)
        self.pos_settling_time_dsbox.setDecimals(2)
        self.pos_settling_time_dsbox.setSingleStep(0.01)
        self.pos_settling_time_dsbox.setObjectName("pos_settling_time_dsbox")
        self.horizontalLayout_5.addWidget(self.pos_settling_time_dsbox)
        self.gridLayout_4.addLayout(self.horizontalLayout_5, 5, 4, 1, 2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(4, -1, -1, -1)
        self.horizontalLayout_6.setSpacing(8)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.volt_steps_lbl = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.volt_steps_lbl.sizePolicy().hasHeightForWidth())
        self.volt_steps_lbl.setSizePolicy(sizePolicy)
        self.volt_steps_lbl.setObjectName("volt_steps_lbl")
        self.horizontalLayout_6.addWidget(self.volt_steps_lbl)
        self.label_20 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_6.addWidget(self.label_20)
        self.volt_begin_dsbox = QtWidgets.QDoubleSpinBox(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.volt_begin_dsbox.sizePolicy().hasHeightForWidth())
        self.volt_begin_dsbox.setSizePolicy(sizePolicy)
        self.volt_begin_dsbox.setMinimum(-9999.0)
        self.volt_begin_dsbox.setMaximum(9999.0)
        self.volt_begin_dsbox.setObjectName("volt_begin_dsbox")
        self.horizontalLayout_6.addWidget(self.volt_begin_dsbox)
        self.label_21 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_6.addWidget(self.label_21)
        self.volt_end_dsbox = QtWidgets.QDoubleSpinBox(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.volt_end_dsbox.sizePolicy().hasHeightForWidth())
        self.volt_end_dsbox.setSizePolicy(sizePolicy)
        self.volt_end_dsbox.setMinimum(-9999.0)
        self.volt_end_dsbox.setMaximum(9999.0)
        self.volt_end_dsbox.setObjectName("volt_end_dsbox")
        self.horizontalLayout_6.addWidget(self.volt_end_dsbox)
        self.label_22 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_6.addWidget(self.label_22)
        self.volt_step_dsbox = QtWidgets.QDoubleSpinBox(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.volt_step_dsbox.sizePolicy().hasHeightForWidth())
        self.volt_step_dsbox.setSizePolicy(sizePolicy)
        self.volt_step_dsbox.setMinimum(-9999.0)
        self.volt_step_dsbox.setMaximum(9999.0)
        self.volt_step_dsbox.setObjectName("volt_step_dsbox")
        self.horizontalLayout_6.addWidget(self.volt_step_dsbox)
        self.label_23 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Serif")
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_6.addWidget(self.label_23)
        self.volt_settling_time_dsbox = QtWidgets.QDoubleSpinBox(
            self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.volt_settling_time_dsbox.sizePolicy().hasHeightForWidth())
        self.volt_settling_time_dsbox.setSizePolicy(sizePolicy)
        self.volt_settling_time_dsbox.setDecimals(2)
        self.volt_settling_time_dsbox.setSingleStep(0.01)
        self.volt_settling_time_dsbox.setObjectName("volt_settling_time_dsbox")
        self.horizontalLayout_6.addWidget(self.volt_settling_time_dsbox)
        self.gridLayout_4.addLayout(self.horizontalLayout_6, 6, 4, 1, 2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(4, -1, -1, -1)
        self.horizontalLayout_4.setSpacing(8)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setKerning(True)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignRight
                                  | QtCore.Qt.AlignTrailing
                                  | QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.len_info_lbl = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.len_info_lbl.sizePolicy().hasHeightForWidth())
        self.len_info_lbl.setSizePolicy(sizePolicy)
        self.len_info_lbl.setObjectName("len_info_lbl")
        self.horizontalLayout_4.addWidget(self.len_info_lbl)
        self.label_7 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Serif")
        font.setItalic(False)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.length_lineEdit = QtWidgets.QLineEdit(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.length_lineEdit.sizePolicy().hasHeightForWidth())
        self.length_lineEdit.setSizePolicy(sizePolicy)
        self.length_lineEdit.setReadOnly(True)
        self.length_lineEdit.setObjectName("length_lineEdit")
        self.horizontalLayout_4.addWidget(self.length_lineEdit)
        self.label_13 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Serif")
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_4.addWidget(self.label_13)
        self.length1_lineEdit = QtWidgets.QLineEdit(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.length1_lineEdit.sizePolicy().hasHeightForWidth())
        self.length1_lineEdit.setSizePolicy(sizePolicy)
        self.length1_lineEdit.setReadOnly(True)
        self.length1_lineEdit.setObjectName("length1_lineEdit")
        self.horizontalLayout_4.addWidget(self.length1_lineEdit)
        self.label_12 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Serif")
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_4.addWidget(self.label_12)
        self.length2_lineEdit = QtWidgets.QLineEdit(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.length2_lineEdit.sizePolicy().hasHeightForWidth())
        self.length2_lineEdit.setSizePolicy(sizePolicy)
        self.length2_lineEdit.setReadOnly(True)
        self.length2_lineEdit.setObjectName("length2_lineEdit")
        self.horizontalLayout_4.addWidget(self.length2_lineEdit)
        self.gridLayout_4.addLayout(self.horizontalLayout_4, 0, 3, 1, 3)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(4, -1, -1, -1)
        self.horizontalLayout_7.setSpacing(8)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_8 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignRight
                                  | QtCore.Qt.AlignTrailing
                                  | QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_7.addWidget(self.label_8)
        self.gap_info_lbl = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gap_info_lbl.sizePolicy().hasHeightForWidth())
        self.gap_info_lbl.setSizePolicy(sizePolicy)
        self.gap_info_lbl.setObjectName("gap_info_lbl")
        self.horizontalLayout_7.addWidget(self.gap_info_lbl)
        self.label_4 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Serif")
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_7.addWidget(self.label_4)
        self.gap_lineEdit = QtWidgets.QLineEdit(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gap_lineEdit.sizePolicy().hasHeightForWidth())
        self.gap_lineEdit.setSizePolicy(sizePolicy)
        self.gap_lineEdit.setReadOnly(True)
        self.gap_lineEdit.setObjectName("gap_lineEdit")
        self.horizontalLayout_7.addWidget(self.gap_lineEdit)
        self.line_5 = QtWidgets.QFrame(self.gridWidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.horizontalLayout_7.addWidget(self.line_5)
        self.label_9 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignRight
                                  | QtCore.Qt.AlignTrailing
                                  | QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_7.addWidget(self.label_9)
        self.slit_info_lbl = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.slit_info_lbl.sizePolicy().hasHeightForWidth())
        self.slit_info_lbl.setSizePolicy(sizePolicy)
        self.slit_info_lbl.setObjectName("slit_info_lbl")
        self.horizontalLayout_7.addWidget(self.slit_info_lbl)
        self.label_10 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_7.addWidget(self.label_10)
        self.label_27 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Serif")
        self.label_27.setFont(font)
        self.label_27.setObjectName("label_27")
        self.horizontalLayout_7.addWidget(self.label_27)
        self.slit_width_lineEdit = QtWidgets.QLineEdit(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.slit_width_lineEdit.sizePolicy().hasHeightForWidth())
        self.slit_width_lineEdit.setSizePolicy(sizePolicy)
        self.slit_width_lineEdit.setReadOnly(True)
        self.slit_width_lineEdit.setObjectName("slit_width_lineEdit")
        self.horizontalLayout_7.addWidget(self.slit_width_lineEdit)
        self.label_11 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_7.addWidget(self.label_11)
        self.label_28 = QtWidgets.QLabel(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Serif")
        self.label_28.setFont(font)
        self.label_28.setObjectName("label_28")
        self.horizontalLayout_7.addWidget(self.label_28)
        self.slit_thickness_lineEdit = QtWidgets.QLineEdit(self.gridWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.slit_thickness_lineEdit.sizePolicy().hasHeightForWidth())
        self.slit_thickness_lineEdit.setSizePolicy(sizePolicy)
        self.slit_thickness_lineEdit.setReadOnly(True)
        self.slit_thickness_lineEdit.setObjectName("slit_thickness_lineEdit")
        self.horizontalLayout_7.addWidget(self.slit_thickness_lineEdit)
        self.gridLayout_4.addLayout(self.horizontalLayout_7, 2, 3, 1, 3)
        self.default_config_btn = QtWidgets.QToolButton(self.gridWidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/reset.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.default_config_btn.setIcon(icon4)
        self.default_config_btn.setIconSize(QtCore.QSize(28, 28))
        self.default_config_btn.setAutoRaise(False)
        self.default_config_btn.setObjectName("default_config_btn")
        self.gridLayout_4.addWidget(self.default_config_btn, 5, 0, 1, 1)
        self.as_drawing = QtWidgets.QLabel(self.splitter)
        self.as_drawing.setText("")
        self.as_drawing.setPixmap(QtGui.QPixmap(":/icons/as_schematic.png"))
        self.as_drawing.setAlignment(QtCore.Qt.AlignRight
                                     | QtCore.Qt.AlignTrailing
                                     | QtCore.Qt.AlignVCenter)
        self.as_drawing.setObjectName("as_drawing")
        self.verticalLayout_5.addWidget(self.splitter)
        self.gridLayout.addLayout(self.verticalLayout_5, 0, 0, 1, 1)
        self.h_splitter = QtWidgets.QSplitter(self.v_splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(
            self.h_splitter.sizePolicy().hasHeightForWidth())
        self.h_splitter.setSizePolicy(sizePolicy)
        self.h_splitter.setMinimumSize(QtCore.QSize(0, 0))
        self.h_splitter.setSizeIncrement(QtCore.QSize(0, 0))
        self.h_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.h_splitter.setObjectName("h_splitter")
        self.dataviz_gbox = QtWidgets.QGroupBox(self.h_splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(8)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.dataviz_gbox.sizePolicy().hasHeightForWidth())
        self.dataviz_gbox.setSizePolicy(sizePolicy)
        self.dataviz_gbox.setFlat(False)
        self.dataviz_gbox.setObjectName("dataviz_gbox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.dataviz_gbox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.matplotlibimageWidget = MatplotlibImageWidget(self.dataviz_gbox)
        font = QtGui.QFont()
        font.setFamily("sans-serif")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.matplotlibimageWidget.setFigureXYlabelFont(font)
        font = QtGui.QFont()
        font.setFamily("sans-serif")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.matplotlibimageWidget.setFigureTitleFont(font)
        font = QtGui.QFont()
        font.setFamily("sans-serif")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.matplotlibimageWidget.setFigureXYticksFont(font)
        self.matplotlibimageWidget.setProperty("reseverColorMap", False)
        self.matplotlibimageWidget.setColorBarToggle(False)
        self.matplotlibimageWidget.setAutoColorLimit(True)
        self.matplotlibimageWidget.setObjectName("matplotlibimageWidget")
        self.verticalLayout_4.addWidget(self.matplotlibimageWidget)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.raw_view_chkbox = QtWidgets.QCheckBox(self.dataviz_gbox)
        self.raw_view_chkbox.setObjectName("raw_view_chkbox")
        self.horizontalLayout_9.addWidget(self.raw_view_chkbox)
        self.checkBox = QtWidgets.QCheckBox(self.dataviz_gbox)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_9.addWidget(self.checkBox)
        self.set_cmap_chkbox = QtWidgets.QCheckBox(self.dataviz_gbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.set_cmap_chkbox.sizePolicy().hasHeightForWidth())
        self.set_cmap_chkbox.setSizePolicy(sizePolicy)
        self.set_cmap_chkbox.setObjectName("set_cmap_chkbox")
        self.horizontalLayout_9.addWidget(self.set_cmap_chkbox)
        self.cmap_fav_cbb = QtWidgets.QComboBox(self.dataviz_gbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cmap_fav_cbb.sizePolicy().hasHeightForWidth())
        self.cmap_fav_cbb.setSizePolicy(sizePolicy)
        self.cmap_fav_cbb.setObjectName("cmap_fav_cbb")
        self.horizontalLayout_9.addWidget(self.cmap_fav_cbb)
        self.verticalLayout_4.addLayout(self.horizontalLayout_9)
        self.analysis_gbox = QtWidgets.QGroupBox(self.h_splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.analysis_gbox.sizePolicy().hasHeightForWidth())
        self.analysis_gbox.setSizePolicy(sizePolicy)
        self.analysis_gbox.setObjectName("analysis_gbox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.analysis_gbox)
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.data_analysis_vsplitter = QtWidgets.QSplitter(self.analysis_gbox)
        self.data_analysis_vsplitter.setOrientation(QtCore.Qt.Vertical)
        self.data_analysis_vsplitter.setOpaqueResize(True)
        self.data_analysis_vsplitter.setObjectName("data_analysis_vsplitter")
        self.data_analysis_tbox = QtWidgets.QToolBox(
            self.data_analysis_vsplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.data_analysis_tbox.sizePolicy().hasHeightForWidth())
        self.data_analysis_tbox.setSizePolicy(sizePolicy)
        self.data_analysis_tbox.setStyleSheet(
            "QToolBox::tab {\n"
            "    background: lightgray;\n"
            "    border-radius: 5px;\n"
            "    color: darkgray;\n"
            "}\n"
            "\n"
            "QToolBox::tab:selected { /* italicize selected tabs */\n"
            "    font: italic;\n"
            "    color: green;\n"
            "}")
        self.data_analysis_tbox.setObjectName("data_analysis_tbox")
        self.page_beam_params = QtWidgets.QWidget()
        self.page_beam_params.setGeometry(QtCore.QRect(0, 0, 573, 493))
        self.page_beam_params.setObjectName("page_beam_params")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.page_beam_params)
        self.verticalLayout_6.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_6.setSpacing(8)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.auto_fill_beam_params_btn = QtWidgets.QPushButton(
            self.page_beam_params)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.auto_fill_beam_params_btn.sizePolicy().hasHeightForWidth())
        self.auto_fill_beam_params_btn.setSizePolicy(sizePolicy)
        self.auto_fill_beam_params_btn.setObjectName(
            "auto_fill_beam_params_btn")
        self.horizontalLayout_2.addWidget(self.auto_fill_beam_params_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout_6.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem1, 0, 1, 2, 1)
        self.ion_name_display_lbl = QtWidgets.QLabel(self.page_beam_params)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ion_name_display_lbl.sizePolicy().hasHeightForWidth())
        self.ion_name_display_lbl.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Serif")
        font.setPointSize(30)
        font.setBold(False)
        font.setWeight(50)
        self.ion_name_display_lbl.setFont(font)
        self.ion_name_display_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.ion_name_display_lbl.setObjectName("ion_name_display_lbl")
        self.gridLayout_6.addWidget(self.ion_name_display_lbl, 0, 2, 3, 1)
        spacerItem2 = QtWidgets.QSpacerItem(388, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem2, 0, 0, 1, 1)
        self.ion_mass_display_lbl = QtWidgets.QLabel(self.page_beam_params)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ion_mass_display_lbl.sizePolicy().hasHeightForWidth())
        self.ion_mass_display_lbl.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("sans")
        font.setPointSize(14)
        self.ion_mass_display_lbl.setFont(font)
        self.ion_mass_display_lbl.setAlignment(QtCore.Qt.AlignRight
                                               | QtCore.Qt.AlignTrailing
                                               | QtCore.Qt.AlignVCenter)
        self.ion_mass_display_lbl.setObjectName("ion_mass_display_lbl")
        self.gridLayout_6.addWidget(self.ion_mass_display_lbl, 2, 1, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_3.setSpacing(1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.ion_charge_display_lbl = QtWidgets.QLabel(self.page_beam_params)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.ion_charge_display_lbl.sizePolicy().hasHeightForWidth())
        self.ion_charge_display_lbl.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("sans")
        font.setPointSize(14)
        self.ion_charge_display_lbl.setFont(font)
        self.ion_charge_display_lbl.setObjectName("ion_charge_display_lbl")
        self.horizontalLayout_3.addWidget(self.ion_charge_display_lbl)
        self.label_50 = QtWidgets.QLabel(self.page_beam_params)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.label_50.sizePolicy().hasHeightForWidth())
        self.label_50.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("sans")
        font.setPointSize(14)
        self.label_50.setFont(font)
        self.label_50.setObjectName("label_50")
        self.horizontalLayout_3.addWidget(self.label_50)
        self.gridLayout_6.addLayout(self.horizontalLayout_3, 0, 3, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem3, 2, 3, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout_6)
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label_33 = QtWidgets.QLabel(self.page_beam_params)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_33.sizePolicy().hasHeightForWidth())
        self.label_33.setSizePolicy(sizePolicy)
        self.label_33.setObjectName("label_33")
        self.gridLayout_8.addWidget(self.label_33, 3, 0, 1, 1)
        self.label_34 = QtWidgets.QLabel(self.page_beam_params)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_34.sizePolicy().hasHeightForWidth())
        self.label_34.setSizePolicy(sizePolicy)
        self.label_34.setObjectName("label_34")
        self.gridLayout_8.addWidget(self.label_34, 5, 0, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.page_beam_params)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy)
        self.label_24.setObjectName("label_24")
        self.gridLayout_8.addWidget(self.label_24, 6, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.page_beam_params)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout_8.addWidget(self.label_2, 1, 0, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.voltage_lineEdit = QtWidgets.QLineEdit(self.page_beam_params)
        self.voltage_lineEdit.setObjectName("voltage_lineEdit")
        self.horizontalLayout_8.addWidget(self.voltage_lineEdit)
        self.label_36 = QtWidgets.QLabel(self.page_beam_params)
        self.label_36.setObjectName("label_36")
        self.horizontalLayout_8.addWidget(self.label_36)
        self.label_38 = QtWidgets.QLabel(self.page_beam_params)
        self.label_38.setText("")
        self.label_38.setPixmap(QtGui.QPixmap(":/icons/to.png"))
        self.label_38.setObjectName("label_38")
        self.horizontalLayout_8.addWidget(self.label_38)
        self.divergence_lineEdit = QtWidgets.QLineEdit(self.page_beam_params)
        self.divergence_lineEdit.setReadOnly(True)
        self.divergence_lineEdit.setObjectName("divergence_lineEdit")
        self.horizontalLayout_8.addWidget(self.divergence_lineEdit)
        self.label_37 = QtWidgets.QLabel(self.page_beam_params)
        self.label_37.setObjectName("label_37")
        self.horizontalLayout_8.addWidget(self.label_37)
        self.gridLayout_8.addLayout(self.horizontalLayout_8, 6, 4, 1, 1)
        self.label_32 = QtWidgets.QLabel(self.page_beam_params)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy)
        self.label_32.setObjectName("label_32")
        self.gridLayout_8.addWidget(self.label_32, 2, 0, 1, 1)
        self.charge_mass_ratio_lineEdit = QtWidgets.QLineEdit(
            self.page_beam_params)
        self.charge_mass_ratio_lineEdit.setEnabled(True)
        self.charge_mass_ratio_lineEdit.setReadOnly(True)
        self.charge_mass_ratio_lineEdit.setObjectName(
            "charge_mass_ratio_lineEdit")
        self.gridLayout_8.addWidget(self.charge_mass_ratio_lineEdit, 4, 4, 1,
                                    1)
        self.ion_mass_lineEdit = QtWidgets.QLineEdit(self.page_beam_params)
        self.ion_mass_lineEdit.setObjectName("ion_mass_lineEdit")
        self.gridLayout_8.addWidget(self.ion_mass_lineEdit, 3, 4, 1, 1)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.ion_energy_lineEdit = QtWidgets.QLineEdit(self.page_beam_params)
        self.ion_energy_lineEdit.setObjectName("ion_energy_lineEdit")
        self.horizontalLayout_13.addWidget(self.ion_energy_lineEdit)
        self.label_35 = QtWidgets.QLabel(self.page_beam_params)
        self.label_35.setObjectName("label_35")
        self.horizontalLayout_13.addWidget(self.label_35)
        self.gridLayout_8.addLayout(self.horizontalLayout_13, 5, 4, 1, 1)
        self.ion_charge_lineEdit = QtWidgets.QLineEdit(self.page_beam_params)
        self.ion_charge_lineEdit.setObjectName("ion_charge_lineEdit")
        self.gridLayout_8.addWidget(self.ion_charge_lineEdit, 2, 4, 1, 1)
        self.label_29 = QtWidgets.QLabel(self.page_beam_params)
        font = QtGui.QFont()
        font.setFamily("Serif")
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")
        self.gridLayout_8.addWidget(self.label_29, 2, 2, 1, 1)
        self.label_30 = QtWidgets.QLabel(self.page_beam_params)
        font = QtGui.QFont()
        font.setFamily("Serif")
        self.label_30.setFont(font)
        self.label_30.setObjectName("label_30")
        self.gridLayout_8.addWidget(self.label_30, 3, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.page_beam_params)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout_8.addWidget(self.label, 4, 0, 1, 1)
        self.label_31 = QtWidgets.QLabel(self.page_beam_params)
        font = QtGui.QFont()
        font.setFamily("Serif")
        self.label_31.setFont(font)
        self.label_31.setObjectName("label_31")
        self.gridLayout_8.addWidget(self.label_31, 5, 2, 1, 1)
        self.ion_name_lineEdit = QtWidgets.QLineEdit(self.page_beam_params)
        self.ion_name_lineEdit.setReadOnly(True)
        self.ion_name_lineEdit.setObjectName("ion_name_lineEdit")
        self.gridLayout_8.addWidget(self.ion_name_lineEdit, 1, 4, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout_8)
        spacerItem4 = QtWidgets.QSpacerItem(20, 94,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem4)
        self.data_analysis_tbox.addItem(self.page_beam_params, "")
        self.page_bkgd_noise = QtWidgets.QWidget()
        self.page_bkgd_noise.setGeometry(QtCore.QRect(0, 0, 573, 493))
        self.page_bkgd_noise.setObjectName("page_bkgd_noise")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.page_bkgd_noise)
        self.gridLayout_2.setContentsMargins(-1, 4, 4, 4)
        self.gridLayout_2.setSpacing(8)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_39 = QtWidgets.QLabel(self.page_bkgd_noise)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_39.sizePolicy().hasHeightForWidth())
        self.label_39.setSizePolicy(sizePolicy)
        self.label_39.setObjectName("label_39")
        self.gridLayout_2.addWidget(self.label_39, 0, 0, 1, 1)
        self.bkgd_noise_plot = MatplotlibBaseWidget(self.page_bkgd_noise)
        self.bkgd_noise_plot.setProperty("figureTightLayout", True)
        self.bkgd_noise_plot.setObjectName("bkgd_noise_plot")
        self.gridLayout_2.addWidget(self.bkgd_noise_plot, 3, 0, 1, 3)
        self.bkgd_noise_threshold_sbox = QtWidgets.QSpinBox(
            self.page_bkgd_noise)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.bkgd_noise_threshold_sbox.sizePolicy().hasHeightForWidth())
        self.bkgd_noise_threshold_sbox.setSizePolicy(sizePolicy)
        self.bkgd_noise_threshold_sbox.setProperty("value", 5)
        self.bkgd_noise_threshold_sbox.setObjectName(
            "bkgd_noise_threshold_sbox")
        self.gridLayout_2.addWidget(self.bkgd_noise_threshold_sbox, 1, 1, 1, 1)
        self.label_40 = QtWidgets.QLabel(self.page_bkgd_noise)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_40.sizePolicy().hasHeightForWidth())
        self.label_40.setSizePolicy(sizePolicy)
        self.label_40.setObjectName("label_40")
        self.gridLayout_2.addWidget(self.label_40, 1, 0, 1, 1)
        self.bkgd_noise_nelem_sbox = QtWidgets.QSpinBox(self.page_bkgd_noise)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.bkgd_noise_nelem_sbox.sizePolicy().hasHeightForWidth())
        self.bkgd_noise_nelem_sbox.setSizePolicy(sizePolicy)
        self.bkgd_noise_nelem_sbox.setProperty("value", 2)
        self.bkgd_noise_nelem_sbox.setObjectName("bkgd_noise_nelem_sbox")
        self.gridLayout_2.addWidget(self.bkgd_noise_nelem_sbox, 0, 1, 1, 1)
        self.auto_update_image_chkbox = QtWidgets.QCheckBox(
            self.page_bkgd_noise)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.auto_update_image_chkbox.sizePolicy().hasHeightForWidth())
        self.auto_update_image_chkbox.setSizePolicy(sizePolicy)
        self.auto_update_image_chkbox.setChecked(False)
        self.auto_update_image_chkbox.setObjectName("auto_update_image_chkbox")
        self.gridLayout_2.addWidget(self.auto_update_image_chkbox, 1, 2, 1, 1)
        self.data_analysis_tbox.addItem(self.page_bkgd_noise, "")
        self.page_noise_correction = QtWidgets.QWidget()
        self.page_noise_correction.setGeometry(QtCore.QRect(0, 0, 573, 493))
        self.page_noise_correction.setObjectName("page_noise_correction")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.page_noise_correction)
        self.gridLayout_7.setContentsMargins(-1, 4, 4, 4)
        self.gridLayout_7.setSpacing(8)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_3 = QtWidgets.QLabel(self.page_noise_correction)
        self.label_3.setObjectName("label_3")
        self.gridLayout_7.addWidget(self.label_3, 0, 0, 1, 1)
        self.factor_dsbox = QtWidgets.QDoubleSpinBox(
            self.page_noise_correction)
        self.factor_dsbox.setDecimals(1)
        self.factor_dsbox.setMaximum(20.0)
        self.factor_dsbox.setSingleStep(0.2)
        self.factor_dsbox.setProperty("value", 8.0)
        self.factor_dsbox.setObjectName("factor_dsbox")
        self.gridLayout_7.addWidget(self.factor_dsbox, 0, 1, 1, 1)
        self.plot_region_btn = QtWidgets.QToolButton(
            self.page_noise_correction)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.plot_region_btn.sizePolicy().hasHeightForWidth())
        self.plot_region_btn.setSizePolicy(sizePolicy)
        self.plot_region_btn.setObjectName("plot_region_btn")
        self.gridLayout_7.addWidget(self.plot_region_btn, 0, 2, 1, 1)
        self.label_49 = QtWidgets.QLabel(self.page_noise_correction)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_49.sizePolicy().hasHeightForWidth())
        self.label_49.setSizePolicy(sizePolicy)
        self.label_49.setObjectName("label_49")
        self.gridLayout_7.addWidget(self.label_49, 1, 0, 1, 1)
        self.noise_threshold_sbox = QtWidgets.QDoubleSpinBox(
            self.page_noise_correction)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.noise_threshold_sbox.sizePolicy().hasHeightForWidth())
        self.noise_threshold_sbox.setSizePolicy(sizePolicy)
        self.noise_threshold_sbox.setDecimals(1)
        self.noise_threshold_sbox.setSingleStep(0.2)
        self.noise_threshold_sbox.setProperty("value", 2.0)
        self.noise_threshold_sbox.setObjectName("noise_threshold_sbox")
        self.gridLayout_7.addWidget(self.noise_threshold_sbox, 1, 1, 1, 1)
        self.apply_noise_correction_btn = QtWidgets.QToolButton(
            self.page_noise_correction)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.apply_noise_correction_btn.sizePolicy().hasHeightForWidth())
        self.apply_noise_correction_btn.setSizePolicy(sizePolicy)
        self.apply_noise_correction_btn.setObjectName(
            "apply_noise_correction_btn")
        self.gridLayout_7.addWidget(self.apply_noise_correction_btn, 1, 2, 1,
                                    1)
        self.noise_plot = MatplotlibBaseWidget(self.page_noise_correction)
        self.noise_plot.setProperty("figureTightLayout", True)
        self.noise_plot.setObjectName("noise_plot")
        self.gridLayout_7.addWidget(self.noise_plot, 2, 0, 1, 3)
        self.data_analysis_tbox.addItem(self.page_noise_correction, "")
        self.twiss_gbox = QtWidgets.QGroupBox(self.data_analysis_vsplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.twiss_gbox.sizePolicy().hasHeightForWidth())
        self.twiss_gbox.setSizePolicy(sizePolicy)
        self.twiss_gbox.setFlat(False)
        self.twiss_gbox.setCheckable(False)
        self.twiss_gbox.setObjectName("twiss_gbox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.twiss_gbox)
        self.verticalLayout_3.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_3.setSpacing(8)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.twiss_gridLayout = QtWidgets.QGridLayout()
        self.twiss_gridLayout.setContentsMargins(0, -1, -1, -1)
        self.twiss_gridLayout.setSpacing(8)
        self.twiss_gridLayout.setObjectName("twiss_gridLayout")
        self.x_cen_lbl = QtWidgets.QLabel(self.twiss_gbox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.x_cen_lbl.setFont(font)
        self.x_cen_lbl.setObjectName("x_cen_lbl")
        self.twiss_gridLayout.addWidget(self.x_cen_lbl, 0, 0, 1, 1)
        self.x_cen_lineEdit = QtWidgets.QLineEdit(self.twiss_gbox)
        self.x_cen_lineEdit.setReadOnly(True)
        self.x_cen_lineEdit.setObjectName("x_cen_lineEdit")
        self.twiss_gridLayout.addWidget(self.x_cen_lineEdit, 0, 1, 1, 1)
        self.x_rms_lbl = QtWidgets.QLabel(self.twiss_gbox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.x_rms_lbl.setFont(font)
        self.x_rms_lbl.setObjectName("x_rms_lbl")
        self.twiss_gridLayout.addWidget(self.x_rms_lbl, 0, 2, 1, 1)
        self.x_rms_lineEdit = QtWidgets.QLineEdit(self.twiss_gbox)
        self.x_rms_lineEdit.setReadOnly(True)
        self.x_rms_lineEdit.setObjectName("x_rms_lineEdit")
        self.twiss_gridLayout.addWidget(self.x_rms_lineEdit, 0, 3, 1, 1)
        self.label_41 = QtWidgets.QLabel(self.twiss_gbox)
        self.label_41.setObjectName("label_41")
        self.twiss_gridLayout.addWidget(self.label_41, 0, 4, 1, 1)
        self.xp_cen_lbl = QtWidgets.QLabel(self.twiss_gbox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.xp_cen_lbl.setFont(font)
        self.xp_cen_lbl.setObjectName("xp_cen_lbl")
        self.twiss_gridLayout.addWidget(self.xp_cen_lbl, 1, 0, 1, 1)
        self.xp_cen_lineEdit = QtWidgets.QLineEdit(self.twiss_gbox)
        self.xp_cen_lineEdit.setReadOnly(True)
        self.xp_cen_lineEdit.setObjectName("xp_cen_lineEdit")
        self.twiss_gridLayout.addWidget(self.xp_cen_lineEdit, 1, 1, 1, 1)
        self.xp_rms_lbl = QtWidgets.QLabel(self.twiss_gbox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.xp_rms_lbl.setFont(font)
        self.xp_rms_lbl.setObjectName("xp_rms_lbl")
        self.twiss_gridLayout.addWidget(self.xp_rms_lbl, 1, 2, 1, 1)
        self.xp_rms_lineEdit = QtWidgets.QLineEdit(self.twiss_gbox)
        self.xp_rms_lineEdit.setReadOnly(True)
        self.xp_rms_lineEdit.setObjectName("xp_rms_lineEdit")
        self.twiss_gridLayout.addWidget(self.xp_rms_lineEdit, 1, 3, 1, 1)
        self.label_42 = QtWidgets.QLabel(self.twiss_gbox)
        self.label_42.setObjectName("label_42")
        self.twiss_gridLayout.addWidget(self.label_42, 1, 4, 1, 1)
        self.emit_x_lbl = QtWidgets.QLabel(self.twiss_gbox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.emit_x_lbl.setFont(font)
        self.emit_x_lbl.setObjectName("emit_x_lbl")
        self.twiss_gridLayout.addWidget(self.emit_x_lbl, 2, 0, 1, 1)
        self.emit_x_lineEdit = QtWidgets.QLineEdit(self.twiss_gbox)
        self.emit_x_lineEdit.setReadOnly(True)
        self.emit_x_lineEdit.setObjectName("emit_x_lineEdit")
        self.twiss_gridLayout.addWidget(self.emit_x_lineEdit, 2, 1, 1, 1)
        self.emitn_x_lbl = QtWidgets.QLabel(self.twiss_gbox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.emitn_x_lbl.setFont(font)
        self.emitn_x_lbl.setObjectName("emitn_x_lbl")
        self.twiss_gridLayout.addWidget(self.emitn_x_lbl, 2, 2, 1, 1)
        self.emitn_x_lineEdit = QtWidgets.QLineEdit(self.twiss_gbox)
        self.emitn_x_lineEdit.setReadOnly(True)
        self.emitn_x_lineEdit.setObjectName("emitn_x_lineEdit")
        self.twiss_gridLayout.addWidget(self.emitn_x_lineEdit, 2, 3, 1, 1)
        self.label_47 = QtWidgets.QLabel(self.twiss_gbox)
        self.label_47.setObjectName("label_47")
        self.twiss_gridLayout.addWidget(self.label_47, 2, 4, 1, 1)
        self.verticalLayout_3.addLayout(self.twiss_gridLayout)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.alpha_x_lbl = QtWidgets.QLabel(self.twiss_gbox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.alpha_x_lbl.setFont(font)
        self.alpha_x_lbl.setObjectName("alpha_x_lbl")
        self.horizontalLayout_10.addWidget(self.alpha_x_lbl)
        self.alpha_x_lineEdit = QtWidgets.QLineEdit(self.twiss_gbox)
        self.alpha_x_lineEdit.setReadOnly(True)
        self.alpha_x_lineEdit.setObjectName("alpha_x_lineEdit")
        self.horizontalLayout_10.addWidget(self.alpha_x_lineEdit)
        self.beta_x_lbl = QtWidgets.QLabel(self.twiss_gbox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.beta_x_lbl.setFont(font)
        self.beta_x_lbl.setObjectName("beta_x_lbl")
        self.horizontalLayout_10.addWidget(self.beta_x_lbl)
        self.beta_x_lineEdit = QtWidgets.QLineEdit(self.twiss_gbox)
        self.beta_x_lineEdit.setReadOnly(True)
        self.beta_x_lineEdit.setObjectName("beta_x_lineEdit")
        self.horizontalLayout_10.addWidget(self.beta_x_lineEdit)
        self.label_48 = QtWidgets.QLabel(self.twiss_gbox)
        self.label_48.setObjectName("label_48")
        self.horizontalLayout_10.addWidget(self.label_48)
        self.gamma_x_lbl = QtWidgets.QLabel(self.twiss_gbox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.gamma_x_lbl.setFont(font)
        self.gamma_x_lbl.setObjectName("gamma_x_lbl")
        self.horizontalLayout_10.addWidget(self.gamma_x_lbl)
        self.gamma_x_lineEdit = QtWidgets.QLineEdit(self.twiss_gbox)
        self.gamma_x_lineEdit.setReadOnly(True)
        self.gamma_x_lineEdit.setObjectName("gamma_x_lineEdit")
        self.horizontalLayout_10.addWidget(self.gamma_x_lineEdit)
        self.label_46 = QtWidgets.QLabel(self.twiss_gbox)
        self.label_46.setObjectName("label_46")
        self.horizontalLayout_10.addWidget(self.label_46)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.update_results_btn = QtWidgets.QToolButton(self.twiss_gbox)
        self.update_results_btn.setObjectName("update_results_btn")
        self.horizontalLayout_11.addWidget(self.update_results_btn)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem5)
        self.show_results_btn = QtWidgets.QToolButton(self.twiss_gbox)
        self.show_results_btn.setObjectName("show_results_btn")
        self.horizontalLayout_11.addWidget(self.show_results_btn)
        self.verticalLayout_3.addLayout(self.horizontalLayout_11)
        self.verticalLayout.addWidget(self.data_analysis_vsplitter)
        self.gridLayout_3.addWidget(self.v_splitter, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 35))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menuConfiguration = QtWidgets.QMenu(self.menubar)
        self.menuConfiguration.setObjectName("menuConfiguration")
        self.menu_Device = QtWidgets.QMenu(self.menubar)
        self.menu_Device.setObjectName("menu_Device")
        self.menu_Data = QtWidgets.QMenu(self.menubar)
        self.menu_Data.setObjectName("menu_Data")
        MainWindow.setMenuBar(self.menubar)
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/exit.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.actionE_xit.setIcon(icon5)
        self.actionE_xit.setObjectName("actionE_xit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/info.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon6)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/qt.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.actionAbout_Qt.setIcon(icon7)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionReload = QtWidgets.QAction(MainWindow)
        self.actionReload.setObjectName("actionReload")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionLoad_From = QtWidgets.QAction(MainWindow)
        self.actionLoad_From.setObjectName("actionLoad_From")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionLocate = QtWidgets.QAction(MainWindow)
        self.actionLocate.setObjectName("actionLocate")
        self.actionSimulation_Mode = QtWidgets.QAction(MainWindow)
        self.actionSimulation_Mode.setCheckable(True)
        self.actionSimulation_Mode.setObjectName("actionSimulation_Mode")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/open.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon8)
        self.actionOpen.setObjectName("actionOpen")
        self.actionAuto_Analysis = QtWidgets.QAction(MainWindow)
        self.actionAuto_Analysis.setCheckable(True)
        self.actionAuto_Analysis.setChecked(True)
        self.actionAuto_Analysis.setObjectName("actionAuto_Analysis")
        self.actionSaveData = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/save.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.actionSaveData.setIcon(icon9)
        self.actionSaveData.setObjectName("actionSaveData")
        self.actionRunXY = QtWidgets.QAction(MainWindow)
        self.actionRunXY.setObjectName("actionRunXY")
        self.menu_File.addAction(self.actionOpen)
        self.menu_File.addAction(self.actionSaveData)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionE_xit)
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menuConfiguration.addAction(self.actionReload)
        self.menuConfiguration.addAction(self.actionSave)
        self.menuConfiguration.addAction(self.actionLoad_From)
        self.menuConfiguration.addAction(self.actionSave_As)
        self.menuConfiguration.addSeparator()
        self.menuConfiguration.addAction(self.actionLocate)
        self.menu_Device.addAction(self.actionSimulation_Mode)
        self.menu_Device.addAction(self.actionRunXY)
        self.menu_Data.addAction(self.actionAuto_Analysis)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuConfiguration.menuAction())
        self.menubar.addAction(self.menu_Data.menuAction())
        self.menubar.addAction(self.menu_Device.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        self.data_analysis_tbox.setCurrentIndex(0)
        self.actionAbout.triggered.connect(MainWindow.onAbout)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.actionE_xit.triggered.connect(MainWindow.close)
        self.run_btn.clicked.connect(MainWindow.on_run)
        self.actionReload.triggered.connect(MainWindow.on_reload_config)
        self.actionLoad_From.triggered.connect(MainWindow.on_loadfrom_config)
        self.actionSave.triggered.connect(MainWindow.on_save_config)
        self.actionSave_As.triggered.connect(MainWindow.on_saveas_config)
        self.actionLocate.triggered.connect(MainWindow.on_locate_config)
        self.actionSimulation_Mode.toggled['bool'].connect(
            MainWindow.on_enable_simulation_mode)
        self.update_results_btn.clicked.connect(MainWindow.on_update_results)
        self.actionOpen.triggered.connect(MainWindow.on_open_data)
        self.bkgd_noise_nelem_sbox.valueChanged['int'].connect(
            MainWindow.on_update_nsampling)
        self.bkgd_noise_threshold_sbox.valueChanged['int'].connect(
            MainWindow.on_update_threshold0)
        self.checkBox.toggled['bool'].connect(
            self.matplotlibimageWidget.setColorBarToggle)
        self.raw_view_chkbox.toggled['bool'].connect(
            MainWindow.on_enable_raw_view)
        self.auto_update_image_chkbox.toggled['bool'].connect(
            MainWindow.on_enable_auto_filter_bkgd_noise)
        self.plot_region_btn.clicked.connect(MainWindow.on_plot_region)
        self.apply_noise_correction_btn.clicked.connect(
            MainWindow.on_apply_noise_correction)
        self.factor_dsbox.valueChanged['double'].connect(
            MainWindow.on_update_ellipse_size_factor)
        self.noise_threshold_sbox.valueChanged['double'].connect(
            MainWindow.on_update_noise_threshold)
        self.show_results_btn.clicked.connect(MainWindow.on_finalize_results)
        self.fetch_data_btn.clicked.connect(MainWindow.on_sync_data)
        self.actionAuto_Analysis.toggled['bool'].connect(
            MainWindow.on_enable_auto_analysis)
        self.actionSaveData.triggered.connect(MainWindow.on_save_data)
        self.abort_btn.clicked.connect(MainWindow.on_abort)
        self.auto_fill_beam_params_btn.clicked.connect(
            MainWindow.on_auto_fill_beam_params)
        self.adv_ctrl_chkbox.toggled['bool'].connect(
            MainWindow.on_enable_advctrl)
        self.actionRunXY.triggered.connect(MainWindow.onRunXnY)
        self.fetch_config_btn.clicked.connect(MainWindow.sync_config)
        self.default_config_btn.clicked.connect(
            MainWindow.on_load_default_config)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ctrl_gbox.setTitle(_translate("MainWindow", "Device"))
        self.ems_names_cbb.setToolTip(
            _translate("MainWindow", "Select Allison scanner device."))
        self.info_lbl.setText(_translate("MainWindow", "info"))
        self.ems_detail_btn.setText(_translate("MainWindow", "..."))
        self.label_14.setText(_translate("MainWindow", "Orientation"))
        self.ems_orientation_cbb.setToolTip(
            _translate("MainWindow", "Select measurement orientation."))
        self.ems_orientation_cbb.setItemText(0, _translate("MainWindow", "X"))
        self.ems_orientation_cbb.setItemText(1, _translate("MainWindow", "Y"))
        self.status_lbl.setToolTip(
            _translate("MainWindow", "Motor movement status"))
        self.run_btn.setToolTip(_translate("MainWindow", "Run device."))
        self.run_btn.setText(_translate("MainWindow", "Run"))
        self.abort_btn.setToolTip(_translate("MainWindow", "Abort running."))
        self.abort_btn.setText(_translate("MainWindow", "Abort"))
        self.fetch_data_btn.setToolTip(
            _translate("MainWindow", "Fetch measured data."))
        self.fetch_data_btn.setText(_translate("MainWindow", "Data"))
        self.adv_ctrl_chkbox.setToolTip(
            _translate("MainWindow", "Show additional configuration panel"))
        self.adv_ctrl_chkbox.setText(_translate("MainWindow", "Advanced"))
        self.label_26.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-style:italic;\">V</span><span style=\" vertical-align:sub;\">bias</span></p></body></html>"
            ))
        self.bias_volt_dsbox.setSuffix(_translate("MainWindow", " V"))
        self.is_enabled_lbl.setText(_translate("MainWindow", "is_enable?"))
        self.label_25.setText(_translate("MainWindow", "Motor Position [mm]"))
        self.retract_btn.setToolTip(
            _translate("MainWindow", "Retract device to out limit"))
        self.retract_btn.setText(_translate("MainWindow", "Retract"))
        self.is_outlimit_lbl.setText(_translate("MainWindow", "is_out?"))
        self.reset_itlk_btn.setText(_translate("MainWindow",
                                               "Reset Interlock"))
        self.is_itlk_lbl.setText(_translate("MainWindow", "is_itlk?"))
        self.fetch_config_btn.setToolTip(
            _translate("MainWindow", "Click me when I\'m RED."))
        self.fetch_config_btn.setText(_translate("MainWindow", "..."))
        self.label_16.setText(_translate("MainWindow", "Voltage [Volt]"))
        self.label_15.setText(_translate("MainWindow", "Position [mm]"))
        self.pos_steps_lbl.setText(_translate("MainWindow", "[#]"))
        self.label_17.setText(_translate("MainWindow", "Begin"))
        self.label_18.setText(_translate("MainWindow", "End"))
        self.label_19.setText(_translate("MainWindow", "Step"))
        self.label_5.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-style:italic;\">T</span><span style=\" vertical-align:sub;\">settling</span></p></body></html>"
            ))
        self.pos_settling_time_dsbox.setSuffix(_translate(
            "MainWindow", " sec"))
        self.volt_steps_lbl.setText(_translate("MainWindow", "[#]"))
        self.label_20.setText(_translate("MainWindow", "Begin"))
        self.label_21.setText(_translate("MainWindow", "End"))
        self.label_22.setText(_translate("MainWindow", "Step"))
        self.label_23.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-style:italic;\">T</span><span style=\" vertical-align:sub;\">settling</span></p></body></html>"
            ))
        self.volt_settling_time_dsbox.setSuffix(
            _translate("MainWindow", " sec"))
        self.label_6.setText(_translate("MainWindow", "Lengths [mm]"))
        self.len_info_lbl.setText(_translate("MainWindow", ">"))
        self.label_7.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-style:italic;\">l</span></p></body></html>"
            ))
        self.label_13.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-style:italic;\">l</span><span style=\" vertical-align:sub;\">1</span></p></body></html>"
            ))
        self.label_12.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-style:italic;\">l</span><span style=\" vertical-align:sub;\">2</span></p></body></html>"
            ))
        self.label_8.setText(_translate("MainWindow", "Gap [mm]"))
        self.gap_info_lbl.setText(_translate("MainWindow", ">"))
        self.label_4.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-style:italic;\">g</span></p></body></html>"
            ))
        self.label_9.setText(_translate("MainWindow", "Slit [mm]"))
        self.slit_info_lbl.setText(_translate("MainWindow", ">"))
        self.label_10.setText(
            _translate("MainWindow",
                       "<html><head/><body><p>Width</p></body></html>"))
        self.label_27.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-style:italic;\">s</span></p></body></html>"
            ))
        self.label_11.setText(
            _translate("MainWindow",
                       "<html><head/><body><p>Thickness</p></body></html>"))
        self.label_28.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-style:italic;\">d</span></p></body></html>"
            ))
        self.default_config_btn.setToolTip(
            _translate("MainWindow", "Reset to default scan configuration."))
        self.default_config_btn.setText(_translate("MainWindow", "..."))
        self.dataviz_gbox.setTitle(
            _translate("MainWindow", "Data Visualization"))
        self.matplotlibimageWidget.setFigureAspectRatio(
            _translate("MainWindow", "auto"))
        self.matplotlibimageWidget.setColorMap(_translate("MainWindow", "jet"))
        self.raw_view_chkbox.setText(_translate("MainWindow", "Raw View"))
        self.checkBox.setText(_translate("MainWindow", "Show Colorbar"))
        self.set_cmap_chkbox.setText(_translate("MainWindow", "Set Color Map"))
        self.analysis_gbox.setTitle(_translate("MainWindow", "Data Analysis"))
        self.auto_fill_beam_params_btn.setToolTip(
            _translate("MainWindow", "Fetch live beam species  infomation."))
        self.auto_fill_beam_params_btn.setText(
            _translate("MainWindow", "Auto Fill"))
        self.ion_name_display_lbl.setText(_translate("MainWindow", "Ar"))
        self.ion_mass_display_lbl.setText(_translate("MainWindow", "40"))
        self.ion_charge_display_lbl.setText(_translate("MainWindow", "9"))
        self.label_50.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" vertical-align:super;\">+</span></p></body></html>"
            ))
        self.label_33.setText(
            _translate("MainWindow",
                       "<html><head/><body><p>Ion Mass</p></body></html>"))
        self.label_34.setText(
            _translate("MainWindow",
                       "<html><head/><body><p>Ion Energy</p></body></html>"))
        self.label_24.setText(_translate("MainWindow", "Conversion"))
        self.label_2.setText(_translate("MainWindow", "Ion Name"))
        self.voltage_lineEdit.setText(_translate("MainWindow", "100"))
        self.label_36.setText(_translate("MainWindow", "V"))
        self.label_37.setText(_translate("MainWindow", "mrad"))
        self.label_32.setText(
            _translate("MainWindow",
                       "<html><head/><body><p>Ion Charge</p></body></html>"))
        self.ion_mass_lineEdit.setText(_translate("MainWindow", "39.948"))
        self.ion_energy_lineEdit.setText(_translate("MainWindow", "12000"))
        self.label_35.setText(
            _translate("MainWindow",
                       "<html><head/><body><p>eV</p></body></html>"))
        self.ion_charge_lineEdit.setText(_translate("MainWindow", "9"))
        self.label_29.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>(<span style=\" font-style:italic;\">Q</span>)</p></body></html>"
            ))
        self.label_30.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>(<span style=\" font-style:italic;\">A</span>)</p></body></html>"
            ))
        self.label.setText(_translate("MainWindow", "Q/A"))
        self.label_31.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>(<span style=\" font-style:italic;\">E</span><span style=\" vertical-align:sub;\">k</span>)</p></body></html>"
            ))
        self.data_analysis_tbox.setItemText(
            self.data_analysis_tbox.indexOf(self.page_beam_params),
            _translate("MainWindow", "Ion Species"))
        self.label_39.setText(_translate("MainWindow", "# of Sampling Points"))
        self.label_40.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Threshold by <span style=\" font-style:italic;\">σ</span></p></body></html>"
            ))
        self.auto_update_image_chkbox.setText(
            _translate("MainWindow", "Auto Update"))
        self.data_analysis_tbox.setItemText(
            self.data_analysis_tbox.indexOf(self.page_bkgd_noise),
            _translate("MainWindow", "Background Noise"))
        self.label_3.setText(_translate("MainWindow", "Ellipse Size Factor"))
        self.plot_region_btn.setText(_translate("MainWindow", "Plot"))
        self.label_49.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Noise Threshold by <span style=\" font-style:italic;\">σ</span></p></body></html>"
            ))
        self.apply_noise_correction_btn.setText(
            _translate("MainWindow", "Apply"))
        self.data_analysis_tbox.setItemText(
            self.data_analysis_tbox.indexOf(self.page_noise_correction),
            _translate("MainWindow", "Noise Correction"))
        self.twiss_gbox.setTitle(_translate("MainWindow", "Twiss Paramemters"))
        self.x_cen_lbl.setText(_translate("MainWindow", "x_cen"))
        self.x_rms_lbl.setText(_translate("MainWindow", "x_rms"))
        self.label_41.setText(_translate("MainWindow", "mm"))
        self.xp_cen_lbl.setText(_translate("MainWindow", "xp_cen"))
        self.xp_rms_lbl.setText(_translate("MainWindow", "xp_rms"))
        self.label_42.setText(_translate("MainWindow", "mrad"))
        self.emit_x_lbl.setText(_translate("MainWindow", "emit"))
        self.emitn_x_lbl.setText(_translate("MainWindow", "emit_n"))
        self.label_47.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>mm&middot;mrad</p></body></html>"))
        self.alpha_x_lbl.setText(_translate("MainWindow", "alpha"))
        self.beta_x_lbl.setText(_translate("MainWindow", "beta"))
        self.label_48.setText(
            _translate("MainWindow",
                       "<html><head/><body><p>m</p></body></html>"))
        self.gamma_x_lbl.setText(_translate("MainWindow", "gamma"))
        self.label_46.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p>m<span style=\" vertical-align:super;\">-1</span></p></body></html>"
            ))
        self.update_results_btn.setText(_translate("MainWindow", "Update"))
        self.show_results_btn.setText(
            _translate("MainWindow", "Finalize Results"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.menuConfiguration.setTitle(
            _translate("MainWindow", "&Configuration"))
        self.menu_Device.setTitle(_translate("MainWindow", "&Device"))
        self.menu_Data.setTitle(_translate("MainWindow", "&Data"))
        self.actionE_xit.setText(_translate("MainWindow", "E&xit"))
        self.actionE_xit.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))
        self.actionReload.setText(_translate("MainWindow", "Reload"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionLoad_From.setText(_translate("MainWindow", "Load From"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As"))
        self.actionLocate.setText(_translate("MainWindow", "Locate"))
        self.actionSimulation_Mode.setText(
            _translate("MainWindow", "Simulation Mode"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionAuto_Analysis.setText(
            _translate("MainWindow", "Auto Analysis"))
        self.actionSaveData.setText(_translate("MainWindow", "Save"))
        self.actionSaveData.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionRunXY.setText(_translate("MainWindow", "Run X and Y"))


from mpl4qt.widgets.mplbasewidget import MatplotlibBaseWidget
from mpl4qt.widgets.mplimagewidget import MatplotlibImageWidget
from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
