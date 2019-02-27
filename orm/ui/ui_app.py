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
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/work.png"), QtGui.QIcon.Normal,
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
            "}\n"
            "\n"
            "QProgressBar {\n"
            "    border: 1px solid gray;\n"
            "    border-radius: 10px;\n"
            "    text-align: center;\n"
            "}\n"
            "\n"
            "QProgressBar::chunk {\n"
            "    background-color: #05B8CC;\n"
            "    width: 20px;\n"
            "    margin: 0.5px;\n"
            "}")
        MainWindow.setIconSize(QtCore.QSize(36, 36))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.hsplitter = QtWidgets.QSplitter(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.hsplitter.sizePolicy().hasHeightForWidth())
        self.hsplitter.setSizePolicy(sizePolicy)
        self.hsplitter.setOrientation(QtCore.Qt.Horizontal)
        self.hsplitter.setObjectName("hsplitter")
        self.elem_models = QtWidgets.QWidget(self.hsplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.elem_models.sizePolicy().hasHeightForWidth())
        self.elem_models.setSizePolicy(sizePolicy)
        self.elem_models.setMinimumSize(QtCore.QSize(450, 0))
        self.elem_models.setObjectName("elem_models")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.elem_models)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_10 = QtWidgets.QLabel(self.elem_models)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_11.addWidget(self.label_10)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem)
        self.refresh_models_btn = QtWidgets.QPushButton(self.elem_models)
        self.refresh_models_btn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/refresh.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.refresh_models_btn.setIcon(icon1)
        self.refresh_models_btn.setIconSize(QtCore.QSize(24, 24))
        self.refresh_models_btn.setObjectName("refresh_models_btn")
        self.horizontalLayout_11.addWidget(self.refresh_models_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_11)
        self.line = QtWidgets.QFrame(self.elem_models)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.splitter = QtWidgets.QSplitter(self.elem_models)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.bpm_vbox = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.bpm_vbox.setContentsMargins(0, 0, 0, 0)
        self.bpm_vbox.setObjectName("bpm_vbox")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setSpacing(6)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.select_all_bpms_btn = QtWidgets.QToolButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.select_all_bpms_btn.sizePolicy().hasHeightForWidth())
        self.select_all_bpms_btn.setSizePolicy(sizePolicy)
        self.select_all_bpms_btn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/select-all.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.select_all_bpms_btn.setIcon(icon2)
        self.select_all_bpms_btn.setObjectName("select_all_bpms_btn")
        self.horizontalLayout_9.addWidget(self.select_all_bpms_btn)
        self.inverse_bpm_selection_btn = QtWidgets.QToolButton(
            self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.inverse_bpm_selection_btn.sizePolicy().hasHeightForWidth())
        self.inverse_bpm_selection_btn.setSizePolicy(sizePolicy)
        self.inverse_bpm_selection_btn.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(":/icons/invert-selection.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.inverse_bpm_selection_btn.setIcon(icon3)
        self.inverse_bpm_selection_btn.setObjectName(
            "inverse_bpm_selection_btn")
        self.horizontalLayout_9.addWidget(self.inverse_bpm_selection_btn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem1)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_9.addWidget(self.label_6)
        self.monitor_fields_cbb = QtWidgets.QComboBox(self.layoutWidget)
        self.monitor_fields_cbb.setObjectName("monitor_fields_cbb")
        self.monitor_fields_cbb.addItem("")
        self.monitor_fields_cbb.addItem("")
        self.monitor_fields_cbb.addItem("")
        self.horizontalLayout_9.addWidget(self.monitor_fields_cbb)
        self.nelem_selected_bpms_lineEdit = QtWidgets.QLineEdit(
            self.layoutWidget)
        self.nelem_selected_bpms_lineEdit.setReadOnly(True)
        self.nelem_selected_bpms_lineEdit.setObjectName(
            "nelem_selected_bpms_lineEdit")
        self.horizontalLayout_9.addWidget(self.nelem_selected_bpms_lineEdit)
        self.bpm_vbox.addLayout(self.horizontalLayout_9)
        self.monitors_gbox = QtWidgets.QGroupBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.monitors_gbox.sizePolicy().hasHeightForWidth())
        self.monitors_gbox.setSizePolicy(sizePolicy)
        self.monitors_gbox.setObjectName("monitors_gbox")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.monitors_gbox)
        self.horizontalLayout_6.setContentsMargins(4, 8, 4, 4)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.bpms_treeView = QtWidgets.QTreeView(self.monitors_gbox)
        self.bpms_treeView.setObjectName("bpms_treeView")
        self.horizontalLayout_6.addWidget(self.bpms_treeView)
        self.bpm_vbox.addWidget(self.monitors_gbox)
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.cor_vbox = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.cor_vbox.setContentsMargins(0, 0, 0, 0)
        self.cor_vbox.setObjectName("cor_vbox")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setSpacing(6)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.select_all_cors_btn = QtWidgets.QToolButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.select_all_cors_btn.sizePolicy().hasHeightForWidth())
        self.select_all_cors_btn.setSizePolicy(sizePolicy)
        self.select_all_cors_btn.setText("")
        self.select_all_cors_btn.setIcon(icon2)
        self.select_all_cors_btn.setObjectName("select_all_cors_btn")
        self.horizontalLayout_10.addWidget(self.select_all_cors_btn)
        self.inverse_cor_selection_btn = QtWidgets.QToolButton(
            self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.inverse_cor_selection_btn.sizePolicy().hasHeightForWidth())
        self.inverse_cor_selection_btn.setSizePolicy(sizePolicy)
        self.inverse_cor_selection_btn.setText("")
        self.inverse_cor_selection_btn.setIcon(icon3)
        self.inverse_cor_selection_btn.setObjectName(
            "inverse_cor_selection_btn")
        self.horizontalLayout_10.addWidget(self.inverse_cor_selection_btn)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem2)
        self.label_17 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_10.addWidget(self.label_17)
        self.corrector_fields_cbb = QtWidgets.QComboBox(self.layoutWidget1)
        self.corrector_fields_cbb.setObjectName("corrector_fields_cbb")
        self.corrector_fields_cbb.addItem("")
        self.corrector_fields_cbb.addItem("")
        self.horizontalLayout_10.addWidget(self.corrector_fields_cbb)
        self.nelem_selected_cors_lineEdit = QtWidgets.QLineEdit(
            self.layoutWidget1)
        self.nelem_selected_cors_lineEdit.setReadOnly(True)
        self.nelem_selected_cors_lineEdit.setObjectName(
            "nelem_selected_cors_lineEdit")
        self.horizontalLayout_10.addWidget(self.nelem_selected_cors_lineEdit)
        self.cor_vbox.addLayout(self.horizontalLayout_10)
        self.cors_gbox = QtWidgets.QGroupBox(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cors_gbox.sizePolicy().hasHeightForWidth())
        self.cors_gbox.setSizePolicy(sizePolicy)
        self.cors_gbox.setObjectName("cors_gbox")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.cors_gbox)
        self.horizontalLayout_4.setContentsMargins(4, 8, 4, 4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.cors_treeView = QtWidgets.QTreeView(self.cors_gbox)
        self.cors_treeView.setObjectName("cors_treeView")
        self.horizontalLayout_4.addWidget(self.cors_treeView)
        self.cor_vbox.addWidget(self.cors_gbox)
        self.verticalLayout.addWidget(self.splitter)
        self.operations_toolBox = QtWidgets.QToolBox(self.hsplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.operations_toolBox.sizePolicy().hasHeightForWidth())
        self.operations_toolBox.setSizePolicy(sizePolicy)
        self.operations_toolBox.setStyleSheet(
            "QToolBox{\n"
            "     icon-size: 30px;\n"
            "}\n"
            "\n"
            "QToolBox QScrollArea > QWidget > QWidget\n"
            "{\n"
            "    border: 2px solid gray;\n"
            "    border-radius: 5px;\n"
            "}\n"
            "\n"
            "QToolBox::tab {\n"
            "\n"
            "    background-color: #BABDB6;\n"
            "    /*border: 2px solid gray;*/\n"
            "    border-radius: 5px;\n"
            "    color: black;\n"
            "}\n"
            "\n"
            "QToolBox::tab:selected { \n"
            "    font: italic;\n"
            "    color: blue;\n"
            "}")
        self.operations_toolBox.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.operations_toolBox.setFrameShadow(QtWidgets.QFrame.Plain)
        self.operations_toolBox.setObjectName("operations_toolBox")
        self.orm_measurement = QtWidgets.QWidget()
        self.orm_measurement.setGeometry(QtCore.QRect(0, 0, 1118, 809))
        self.orm_measurement.setObjectName("orm_measurement")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.orm_measurement)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(793, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.orm_measurement)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_16 = QtWidgets.QLabel(self.orm_measurement)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout.addWidget(self.label_16)
        self.alter_start_lineEdit = QtWidgets.QLineEdit(self.orm_measurement)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.alter_start_lineEdit.sizePolicy().hasHeightForWidth())
        self.alter_start_lineEdit.setSizePolicy(sizePolicy)
        self.alter_start_lineEdit.setObjectName("alter_start_lineEdit")
        self.horizontalLayout.addWidget(self.alter_start_lineEdit)
        self.label_4 = QtWidgets.QLabel(self.orm_measurement)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.alter_stop_lineEdit = QtWidgets.QLineEdit(self.orm_measurement)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.alter_stop_lineEdit.sizePolicy().hasHeightForWidth())
        self.alter_stop_lineEdit.setSizePolicy(sizePolicy)
        self.alter_stop_lineEdit.setObjectName("alter_stop_lineEdit")
        self.horizontalLayout.addWidget(self.alter_stop_lineEdit)
        self.label_5 = QtWidgets.QLabel(self.orm_measurement)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.alter_steps_lineEdit = QtWidgets.QLineEdit(self.orm_measurement)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.alter_steps_lineEdit.sizePolicy().hasHeightForWidth())
        self.alter_steps_lineEdit.setSizePolicy(sizePolicy)
        self.alter_steps_lineEdit.setObjectName("alter_steps_lineEdit")
        self.horizontalLayout.addWidget(self.alter_steps_lineEdit)
        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 1, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.orm_measurement)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.measure_pb = QtWidgets.QProgressBar(self.orm_measurement)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.measure_pb.sizePolicy().hasHeightForWidth())
        self.measure_pb.setSizePolicy(sizePolicy)
        self.measure_pb.setProperty("value", 24)
        self.measure_pb.setObjectName("measure_pb")
        self.horizontalLayout_7.addWidget(self.measure_pb)
        spacerItem4 = QtWidgets.QSpacerItem(10, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem4)
        self.stop_measure_btn = QtWidgets.QPushButton(self.orm_measurement)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap(":/icons/stop.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.stop_measure_btn.setIcon(icon4)
        self.stop_measure_btn.setIconSize(QtCore.QSize(24, 24))
        self.stop_measure_btn.setObjectName("stop_measure_btn")
        self.horizontalLayout_7.addWidget(self.stop_measure_btn)
        self.run_btn = QtWidgets.QPushButton(self.orm_measurement)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.run_btn.sizePolicy().hasHeightForWidth())
        self.run_btn.setSizePolicy(sizePolicy)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap(":/icons/run.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.run_btn.setIcon(icon5)
        self.run_btn.setIconSize(QtCore.QSize(24, 24))
        self.run_btn.setObjectName("run_btn")
        self.horizontalLayout_7.addWidget(self.run_btn)
        self.gridLayout_2.addLayout(self.horizontalLayout_7, 6, 0, 1, 3)
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.wait_time_dspinbox = QtWidgets.QDoubleSpinBox(
            self.orm_measurement)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.wait_time_dspinbox.sizePolicy().hasHeightForWidth())
        self.wait_time_dspinbox.setSizePolicy(sizePolicy)
        self.wait_time_dspinbox.setDecimals(1)
        self.wait_time_dspinbox.setMaximum(60.0)
        self.wait_time_dspinbox.setSingleStep(0.5)
        self.wait_time_dspinbox.setProperty("value", 1.0)
        self.wait_time_dspinbox.setObjectName("wait_time_dspinbox")
        self.horizontalLayout_19.addWidget(self.wait_time_dspinbox)
        self.label_15 = QtWidgets.QLabel(self.orm_measurement)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_19.addWidget(self.label_15)
        self.gridLayout_2.addLayout(self.horizontalLayout_19, 1, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.orm_measurement)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.n_digits_measure_spinBox = QtWidgets.QSpinBox(
            self.orm_measurement)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.n_digits_measure_spinBox.sizePolicy().hasHeightForWidth())
        self.n_digits_measure_spinBox.setSizePolicy(sizePolicy)
        self.n_digits_measure_spinBox.setMaximum(10)
        self.n_digits_measure_spinBox.setProperty("value", 2)
        self.n_digits_measure_spinBox.setObjectName("n_digits_measure_spinBox")
        self.horizontalLayout_20.addWidget(self.n_digits_measure_spinBox)
        self.label_21 = QtWidgets.QLabel(self.orm_measurement)
        self.label_21.setStyleSheet("QLabel {\n"
                                    "    color: gray;\n"
                                    "    font-style: italic;\n"
                                    "}")
        self.label_21.setAlignment(QtCore.Qt.AlignCenter)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_20.addWidget(self.label_21)
        self.gridLayout_2.addLayout(self.horizontalLayout_20, 3, 1, 1, 2)
        self.operation_mode_cbb = QtWidgets.QComboBox(self.orm_measurement)
        self.operation_mode_cbb.setEnabled(False)
        self.operation_mode_cbb.setObjectName("operation_mode_cbb")
        self.operation_mode_cbb.addItem("")
        self.operation_mode_cbb.addItem("")
        self.gridLayout_2.addWidget(self.operation_mode_cbb, 0, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.update_eta_btn = QtWidgets.QToolButton(self.orm_measurement)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(":/icons/update.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.update_eta_btn.setIcon(icon6)
        self.update_eta_btn.setIconSize(QtCore.QSize(24, 24))
        self.update_eta_btn.setAutoRaise(True)
        self.update_eta_btn.setObjectName("update_eta_btn")
        self.horizontalLayout_2.addWidget(self.update_eta_btn)
        self.label_18 = QtWidgets.QLabel(self.orm_measurement)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_2.addWidget(self.label_18)
        self.eta_lbl = QtWidgets.QLabel(self.orm_measurement)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.eta_lbl.sizePolicy().hasHeightForWidth())
        self.eta_lbl.setSizePolicy(sizePolicy)
        self.eta_lbl.setStyleSheet("QLabel {\n"
                                   "    font-family: monospace;\n"
                                   "}")
        self.eta_lbl.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                  | QtCore.Qt.AlignVCenter)
        self.eta_lbl.setObjectName("eta_lbl")
        self.horizontalLayout_2.addWidget(self.eta_lbl)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.label_19 = QtWidgets.QLabel(self.orm_measurement)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_2.addWidget(self.label_19)
        self.eta_timer_lbl = QtWidgets.QLabel(self.orm_measurement)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.eta_timer_lbl.sizePolicy().hasHeightForWidth())
        self.eta_timer_lbl.setSizePolicy(sizePolicy)
        self.eta_timer_lbl.setStyleSheet("QLabel {\n"
                                         "    color: blue;\n"
                                         "    font-family: monospace;\n"
                                         "}")
        self.eta_timer_lbl.setAlignment(QtCore.Qt.AlignRight
                                        | QtCore.Qt.AlignTrailing
                                        | QtCore.Qt.AlignVCenter)
        self.eta_timer_lbl.setObjectName("eta_timer_lbl")
        self.horizontalLayout_2.addWidget(self.eta_timer_lbl)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 5, 0, 1, 3)
        self.label_20 = QtWidgets.QLabel(self.orm_measurement)
        self.label_20.setObjectName("label_20")
        self.gridLayout_2.addWidget(self.label_20, 3, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem6, 4, 0, 1, 1)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(
            QtGui.QPixmap(":/icons/measure.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.operations_toolBox.addItem(self.orm_measurement, icon7, "")
        self.orm_apply = QtWidgets.QWidget()
        self.orm_apply.setGeometry(QtCore.QRect(0, 0, 1118, 809))
        self.orm_apply.setObjectName("orm_apply")
        self.gridLayout = QtWidgets.QGridLayout(self.orm_apply)
        self.gridLayout.setObjectName("gridLayout")
        self.cached_settings_hbox = QtWidgets.QHBoxLayout()
        self.cached_settings_hbox.setContentsMargins(-1, 0, -1, -1)
        self.cached_settings_hbox.setObjectName("cached_settings_hbox")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.cached_settings_hbox.addItem(spacerItem7)
        self.undo_apply_btn = QtWidgets.QToolButton(self.orm_apply)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(
            QtGui.QPixmap(":/icons/undo.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.undo_apply_btn.setIcon(icon8)
        self.undo_apply_btn.setIconSize(QtCore.QSize(30, 30))
        self.undo_apply_btn.setAutoRaise(True)
        self.undo_apply_btn.setObjectName("undo_apply_btn")
        self.cached_settings_hbox.addWidget(self.undo_apply_btn)
        self.redo_apply_btn = QtWidgets.QToolButton(self.orm_apply)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(
            QtGui.QPixmap(":/icons/redo.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.redo_apply_btn.setIcon(icon9)
        self.redo_apply_btn.setIconSize(QtCore.QSize(30, 30))
        self.redo_apply_btn.setAutoRaise(True)
        self.redo_apply_btn.setObjectName("redo_apply_btn")
        self.cached_settings_hbox.addWidget(self.redo_apply_btn)
        self.reset_cached_settings_btn = QtWidgets.QToolButton(self.orm_apply)
        self.reset_cached_settings_btn.setIcon(icon6)
        self.reset_cached_settings_btn.setIconSize(QtCore.QSize(30, 30))
        self.reset_cached_settings_btn.setAutoRaise(True)
        self.reset_cached_settings_btn.setObjectName(
            "reset_cached_settings_btn")
        self.cached_settings_hbox.addWidget(self.reset_cached_settings_btn)
        self.view_cached_settings_btn = QtWidgets.QToolButton(self.orm_apply)
        self.view_cached_settings_btn.setObjectName("view_cached_settings_btn")
        self.cached_settings_hbox.addWidget(self.view_cached_settings_btn)
        self.gridLayout.addLayout(self.cached_settings_hbox, 6, 0, 1, 2)
        self.label_11 = QtWidgets.QLabel(self.orm_apply)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 0, 0, 1, 1)
        self.cor_niter_spinbox = QtWidgets.QSpinBox(self.orm_apply)
        self.cor_niter_spinbox.setMinimum(1)
        self.cor_niter_spinbox.setMaximum(20)
        self.cor_niter_spinbox.setObjectName("cor_niter_spinbox")
        self.gridLayout.addWidget(self.cor_niter_spinbox, 2, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.orm_apply)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 3, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.orm_apply)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.orm_apply)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 1)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_12 = QtWidgets.QLabel(self.orm_apply)
        self.label_12.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_13.addWidget(self.label_12)
        self.lower_limit_lineEdit = QtWidgets.QLineEdit(self.orm_apply)
        self.lower_limit_lineEdit.setEnabled(False)
        self.lower_limit_lineEdit.setObjectName("lower_limit_lineEdit")
        self.horizontalLayout_13.addWidget(self.lower_limit_lineEdit)
        self.label_13 = QtWidgets.QLabel(self.orm_apply)
        self.label_13.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_13.addWidget(self.label_13)
        self.upper_limit_lineEdit = QtWidgets.QLineEdit(self.orm_apply)
        self.upper_limit_lineEdit.setEnabled(False)
        self.upper_limit_lineEdit.setObjectName("upper_limit_lineEdit")
        self.horizontalLayout_13.addWidget(self.upper_limit_lineEdit)
        spacerItem8 = QtWidgets.QSpacerItem(5, 20,
                                            QtWidgets.QSizePolicy.Preferred,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem8)
        self.enable_limit_change_chkbox = QtWidgets.QCheckBox(self.orm_apply)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.enable_limit_change_chkbox.sizePolicy().hasHeightForWidth())
        self.enable_limit_change_chkbox.setSizePolicy(sizePolicy)
        self.enable_limit_change_chkbox.setObjectName(
            "enable_limit_change_chkbox")
        self.horizontalLayout_13.addWidget(self.enable_limit_change_chkbox)
        self.gridLayout.addLayout(self.horizontalLayout_13, 0, 1, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.orm_apply)
        self.label_22.setObjectName("label_22")
        self.gridLayout.addWidget(self.label_22, 4, 0, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.cor_apply_pb = QtWidgets.QProgressBar(self.orm_apply)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cor_apply_pb.sizePolicy().hasHeightForWidth())
        self.cor_apply_pb.setSizePolicy(sizePolicy)
        self.cor_apply_pb.setProperty("value", 24)
        self.cor_apply_pb.setObjectName("cor_apply_pb")
        self.horizontalLayout_8.addWidget(self.cor_apply_pb)
        spacerItem9 = QtWidgets.QSpacerItem(10, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem9)
        self.stop_apply_btn = QtWidgets.QPushButton(self.orm_apply)
        self.stop_apply_btn.setIcon(icon4)
        self.stop_apply_btn.setIconSize(QtCore.QSize(24, 24))
        self.stop_apply_btn.setObjectName("stop_apply_btn")
        self.horizontalLayout_8.addWidget(self.stop_apply_btn)
        self.cor_eva_btn = QtWidgets.QPushButton(self.orm_apply)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(
            QtGui.QPixmap(":/icons/evaluate.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.cor_eva_btn.setIcon(icon10)
        self.cor_eva_btn.setIconSize(QtCore.QSize(20, 20))
        self.cor_eva_btn.setObjectName("cor_eva_btn")
        self.horizontalLayout_8.addWidget(self.cor_eva_btn)
        self.cor_apply_btn = QtWidgets.QPushButton(self.orm_apply)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cor_apply_btn.sizePolicy().hasHeightForWidth())
        self.cor_apply_btn.setSizePolicy(sizePolicy)
        self.cor_apply_btn.setIcon(icon5)
        self.cor_apply_btn.setIconSize(QtCore.QSize(24, 24))
        self.cor_apply_btn.setObjectName("cor_apply_btn")
        self.horizontalLayout_8.addWidget(self.cor_apply_btn)
        self.gridLayout.addLayout(self.horizontalLayout_8, 7, 0, 1, 2)
        self.cor_damping_fac_dspinbox = QtWidgets.QDoubleSpinBox(
            self.orm_apply)
        self.cor_damping_fac_dspinbox.setMinimum(-1.0)
        self.cor_damping_fac_dspinbox.setMaximum(1.0)
        self.cor_damping_fac_dspinbox.setSingleStep(0.05)
        self.cor_damping_fac_dspinbox.setProperty("value", 0.5)
        self.cor_damping_fac_dspinbox.setObjectName("cor_damping_fac_dspinbox")
        self.gridLayout.addWidget(self.cor_damping_fac_dspinbox, 1, 1, 1, 1)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.cor_wait_time_dspinbox = QtWidgets.QDoubleSpinBox(self.orm_apply)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cor_wait_time_dspinbox.sizePolicy().hasHeightForWidth())
        self.cor_wait_time_dspinbox.setSizePolicy(sizePolicy)
        self.cor_wait_time_dspinbox.setDecimals(1)
        self.cor_wait_time_dspinbox.setMaximum(60.0)
        self.cor_wait_time_dspinbox.setSingleStep(0.5)
        self.cor_wait_time_dspinbox.setProperty("value", 1.0)
        self.cor_wait_time_dspinbox.setObjectName("cor_wait_time_dspinbox")
        self.horizontalLayout_16.addWidget(self.cor_wait_time_dspinbox)
        self.label_14 = QtWidgets.QLabel(self.orm_apply)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_16.addWidget(self.label_14)
        self.gridLayout.addLayout(self.horizontalLayout_16, 3, 1, 1, 1)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.n_digits_apply_spinBox = QtWidgets.QSpinBox(self.orm_apply)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.n_digits_apply_spinBox.sizePolicy().hasHeightForWidth())
        self.n_digits_apply_spinBox.setSizePolicy(sizePolicy)
        self.n_digits_apply_spinBox.setMaximum(10)
        self.n_digits_apply_spinBox.setProperty("value", 2)
        self.n_digits_apply_spinBox.setObjectName("n_digits_apply_spinBox")
        self.horizontalLayout_15.addWidget(self.n_digits_apply_spinBox)
        self.label_23 = QtWidgets.QLabel(self.orm_apply)
        self.label_23.setStyleSheet("QLabel {\n"
                                    "    color: gray;\n"
                                    "    font-style: italic;\n"
                                    "}")
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_15.addWidget(self.label_23)
        self.gridLayout.addLayout(self.horizontalLayout_15, 4, 1, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40,
                                             QtWidgets.QSizePolicy.Minimum,
                                             QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem10, 5, 0, 1, 1)
        self.operations_toolBox.addItem(self.orm_apply, icon, "")
        self.log_gbox = QtWidgets.QGroupBox(self.splitter_2)
        self.log_gbox.setMinimumSize(QtCore.QSize(0, 100))
        self.log_gbox.setObjectName("log_gbox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.log_gbox)
        self.gridLayout_3.setContentsMargins(4, 8, 4, 4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.log_textEdit = QtWidgets.QTextEdit(self.log_gbox)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.log_textEdit.setFont(font)
        self.log_textEdit.setReadOnly(True)
        self.log_textEdit.setObjectName("log_textEdit")
        self.gridLayout_3.addWidget(self.log_textEdit, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.splitter_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1600, 34))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menu_Settings = QtWidgets.QMenu(self.menubar)
        self.menu_Settings.setObjectName("menu_Settings")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.load_settings = QtWidgets.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(
            QtGui.QPixmap(":/icons/open.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.load_settings.setIcon(icon11)
        self.load_settings.setObjectName("load_settings")
        self.save_settings = QtWidgets.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(
            QtGui.QPixmap(":/icons/save.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.save_settings.setIcon(icon12)
        self.save_settings.setObjectName("save_settings")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(
            QtGui.QPixmap(":/icons/info.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon13)
        self.actionAbout.setObjectName("actionAbout")
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(
            QtGui.QPixmap(":/icons/exit.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionE_xit.setIcon(icon14)
        self.actionE_xit.setObjectName("actionE_xit")
        self.actionContents = QtWidgets.QAction(MainWindow)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(
            QtGui.QPixmap(":/icons/help.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionContents.setIcon(icon15)
        self.actionContents.setObjectName("actionContents")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(
            QtGui.QPixmap(":/icons/qt.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.actionAbout_Qt.setIcon(icon16)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setIcon(icon12)
        self.actionSave.setObjectName("actionSave")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setIcon(icon11)
        self.actionOpen.setObjectName("actionOpen")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionE_xit)
        self.menu_Settings.addAction(self.save_settings)
        self.menu_Settings.addAction(self.load_settings)
        self.menu_Help.addAction(self.actionContents)
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_Settings.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        self.actionAbout.triggered.connect(MainWindow.onAbout)
        self.actionE_xit.triggered.connect(MainWindow.close)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.run_btn.clicked.connect(MainWindow.on_measure_orm)
        self.cor_apply_btn.clicked.connect(MainWindow.on_apply_orm)
        self.actionOpen.triggered.connect(MainWindow.on_open_orm)
        self.actionSave.triggered.connect(MainWindow.on_save_orm)
        self.enable_limit_change_chkbox.toggled['bool'].connect(
            self.label_13.setEnabled)
        self.enable_limit_change_chkbox.toggled['bool'].connect(
            self.label_12.setEnabled)
        self.stop_apply_btn.clicked.connect(MainWindow.on_stop_apply_orm)
        self.stop_measure_btn.clicked.connect(MainWindow.on_stop_measure_orm)
        self.enable_limit_change_chkbox.toggled['bool'].connect(
            self.lower_limit_lineEdit.setEnabled)
        self.enable_limit_change_chkbox.toggled['bool'].connect(
            self.upper_limit_lineEdit.setEnabled)
        self.cor_eva_btn.clicked.connect(
            MainWindow.on_evaluate_settings_from_orm)
        self.undo_apply_btn.clicked.connect(MainWindow.on_undo_apply_orm)
        self.redo_apply_btn.clicked.connect(MainWindow.on_redo_apply_orm)
        self.view_cached_settings_btn.clicked.connect(
            MainWindow.on_show_cached_settings)
        self.reset_cached_settings_btn.clicked.connect(
            MainWindow.on_reset_cached_settings)
        self.save_settings.triggered.connect(MainWindow.on_save_settings)
        self.load_settings.triggered.connect(MainWindow.on_load_settings)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_10.setText(_translate("MainWindow", "Refresh"))
        self.refresh_models_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Refresh the elements</p></body></html>")
        )
        self.select_all_bpms_btn.setToolTip(
            _translate("MainWindow",
                       "<html><head/><body><p>Select All</p></body></html>"))
        self.inverse_bpm_selection_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Inverse Current Selection</p></body></html>"
            ))
        self.label_6.setText(_translate("MainWindow", "Field"))
        self.monitor_fields_cbb.setItemText(0, _translate("MainWindow", "X&Y"))
        self.monitor_fields_cbb.setItemText(1, _translate("MainWindow", "X"))
        self.monitor_fields_cbb.setItemText(2, _translate("MainWindow", "Y"))
        self.nelem_selected_bpms_lineEdit.setText(
            _translate("MainWindow", "0"))
        self.monitors_gbox.setTitle(_translate("MainWindow", "Monitors"))
        self.select_all_cors_btn.setToolTip(
            _translate("MainWindow",
                       "<html><head/><body><p>Select All</p></body></html>"))
        self.inverse_cor_selection_btn.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Inverse Current Selection</p></body></html>"
            ))
        self.label_17.setText(_translate("MainWindow", "Field"))
        self.corrector_fields_cbb.setItemText(0, _translate("MainWindow", "I"))
        self.corrector_fields_cbb.setItemText(1, _translate(
            "MainWindow", "ANG"))
        self.nelem_selected_cors_lineEdit.setText(
            _translate("MainWindow", "0"))
        self.cors_gbox.setTitle(_translate("MainWindow", "Correctors"))
        self.label.setText(_translate("MainWindow", "Operation Mode"))
        self.label_16.setText(_translate("MainWindow", "From"))
        self.alter_start_lineEdit.setText(_translate("MainWindow", "-0.003"))
        self.label_4.setText(_translate("MainWindow", "To"))
        self.alter_stop_lineEdit.setText(_translate("MainWindow", "0.003"))
        self.label_5.setText(_translate("MainWindow", "N"))
        self.alter_steps_lineEdit.setText(_translate("MainWindow", "5"))
        self.label_3.setText(_translate("MainWindow", "Alter Range"))
        self.stop_measure_btn.setToolTip(
            _translate("MainWindow", "Stop ORM measurement"))
        self.stop_measure_btn.setText(_translate("MainWindow", "Stop"))
        self.run_btn.setToolTip(
            _translate("MainWindow", "Start ORM measurement"))
        self.run_btn.setText(_translate("MainWindow", "Measure"))
        self.label_15.setText(_translate("MainWindow", "Second"))
        self.label_2.setText(_translate("MainWindow", "Additional Wait Time"))
        self.label_21.setText(
            _translate(
                "MainWindow",
                "e.g. for the case of 2, the original float 0.123 will be applied as 0.12."
            ))
        self.operation_mode_cbb.setItemText(0, _translate(
            "MainWindow", "Live"))
        self.operation_mode_cbb.setItemText(1, _translate(
            "MainWindow", "Model"))
        self.update_eta_btn.setText(_translate("MainWindow", "Update"))
        self.label_18.setText(_translate("MainWindow", "Estimated Time"))
        self.eta_lbl.setText(_translate("MainWindow", "00:00:00"))
        self.label_19.setText(_translate("MainWindow", "Running"))
        self.eta_timer_lbl.setText(_translate("MainWindow", "00:00:00"))
        self.label_20.setText(_translate("MainWindow", "Float Precision"))
        self.operations_toolBox.setItemText(
            self.operations_toolBox.indexOf(self.orm_measurement),
            _translate("MainWindow",
                       "Central Trajectory Response Measurement"))
        self.undo_apply_btn.setToolTip(
            _translate("MainWindow", "Backward corrector settings"))
        self.undo_apply_btn.setText(_translate("MainWindow", "Undo"))
        self.redo_apply_btn.setToolTip(
            _translate("MainWindow", "Forward corrector settings"))
        self.redo_apply_btn.setText(_translate("MainWindow", "Undo"))
        self.reset_cached_settings_btn.setToolTip(
            _translate("MainWindow", "Reset corrector settings cache"))
        self.reset_cached_settings_btn.setText(
            _translate("MainWindow", "Reset"))
        self.view_cached_settings_btn.setToolTip(
            _translate("MainWindow", "Show cached corrector settings"))
        self.view_cached_settings_btn.setText(_translate("MainWindow", "View"))
        self.label_11.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Settings limit for the correctors</p></body></html>"
            ))
        self.label_11.setText(_translate("MainWindow", "Settings Limit"))
        self.label_9.setText(_translate("MainWindow", "Additional Wait Time"))
        self.label_8.setText(_translate("MainWindow", "Iteration"))
        self.label_7.setText(_translate("MainWindow", "Damping Factor"))
        self.label_12.setText(_translate("MainWindow", "From"))
        self.lower_limit_lineEdit.setText(_translate("MainWindow", "-5.0"))
        self.label_13.setText(_translate("MainWindow", "To"))
        self.upper_limit_lineEdit.setText(_translate("MainWindow", "5.0"))
        self.enable_limit_change_chkbox.setText(
            _translate("MainWindow", "Change Limit"))
        self.label_22.setText(_translate("MainWindow", "Float Precision"))
        self.stop_apply_btn.setToolTip(
            _translate("MainWindow", "Stop applying settings to correctors"))
        self.stop_apply_btn.setText(_translate("MainWindow", "Stop"))
        self.cor_eva_btn.setToolTip(
            _translate("MainWindow",
                       "Evaluate the new settings for correctors"))
        self.cor_eva_btn.setText(_translate("MainWindow", "Evaluate"))
        self.cor_apply_btn.setToolTip(
            _translate("MainWindow",
                       "Apply the concured new settings to correctors"))
        self.cor_apply_btn.setText(_translate("MainWindow", "Apply"))
        self.label_14.setText(_translate("MainWindow", "Second"))
        self.label_23.setText(
            _translate(
                "MainWindow",
                "e.g. for the case of 2, the original float 0.123 will be applied as 0.12."
            ))
        self.operations_toolBox.setItemText(
            self.operations_toolBox.indexOf(self.orm_apply),
            _translate("MainWindow", "Central Trajectory Correction"))
        self.log_gbox.setTitle(_translate("MainWindow", "Log"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menu_Settings.setTitle(_translate("MainWindow", "Settings"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.load_settings.setText(_translate("MainWindow", "Load"))
        self.load_settings.setShortcut(
            _translate("MainWindow", "Ctrl+Shift+L"))
        self.save_settings.setText(_translate("MainWindow", "Save"))
        self.save_settings.setIconText(_translate("MainWindow", "Measure ORM"))
        self.save_settings.setShortcut(
            _translate("MainWindow", "Ctrl+Shift+S"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionE_xit.setText(_translate("MainWindow", "E&xit"))
        self.actionE_xit.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionContents.setText(_translate("MainWindow", "Contents"))
        self.actionContents.setShortcut(_translate("MainWindow", "F1"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
