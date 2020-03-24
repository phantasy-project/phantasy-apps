# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_preferences.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(786, 407)
        self.gridLayout_9 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_9.setContentsMargins(6, 12, 6, 6)
        self.gridLayout_9.setSpacing(6)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")
        self.data_tab = QtWidgets.QWidget()
        self.data_tab.setObjectName("data_tab")
        self.gridLayout = QtWidgets.QGridLayout(self.data_tab)
        self.gridLayout.setContentsMargins(6, 12, 6, 6)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.label_72 = QtWidgets.QLabel(self.data_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_72.sizePolicy().hasHeightForWidth())
        self.label_72.setSizePolicy(sizePolicy)
        self.label_72.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                   | QtCore.Qt.AlignVCenter)
        self.label_72.setObjectName("label_72")
        self.gridLayout.addWidget(self.label_72, 1, 0, 1, 1)
        self.init_settings_chkbox = QtWidgets.QCheckBox(self.data_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.init_settings_chkbox.sizePolicy().hasHeightForWidth())
        self.init_settings_chkbox.setSizePolicy(sizePolicy)
        self.init_settings_chkbox.setObjectName("init_settings_chkbox")
        self.gridLayout.addWidget(self.init_settings_chkbox, 0, 0, 1, 2)
        self.apply_delt_dsbox = QtWidgets.QDoubleSpinBox(self.data_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.apply_delt_dsbox.sizePolicy().hasHeightForWidth())
        self.apply_delt_dsbox.setSizePolicy(sizePolicy)
        self.apply_delt_dsbox.setDecimals(3)
        self.apply_delt_dsbox.setMaximum(5.0)
        self.apply_delt_dsbox.setSingleStep(0.05)
        self.apply_delt_dsbox.setProperty("value", 0.05)
        self.apply_delt_dsbox.setObjectName("apply_delt_dsbox")
        self.gridLayout.addWidget(self.apply_delt_dsbox, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.data_tab)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.model_rbtn = QtWidgets.QRadioButton(self.data_tab)
        self.model_rbtn.setChecked(False)
        self.model_rbtn.setObjectName("model_rbtn")
        self.field_init_mode = QtWidgets.QButtonGroup(Dialog)
        self.field_init_mode.setObjectName("field_init_mode")
        self.field_init_mode.addButton(self.model_rbtn)
        self.horizontalLayout.addWidget(self.model_rbtn)
        self.live_rbtn = QtWidgets.QRadioButton(self.data_tab)
        self.live_rbtn.setChecked(True)
        self.live_rbtn.setObjectName("live_rbtn")
        self.field_init_mode.addButton(self.live_rbtn)
        self.horizontalLayout.addWidget(self.live_rbtn)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        self.tol_dsbox = QtWidgets.QDoubleSpinBox(self.data_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tol_dsbox.sizePolicy().hasHeightForWidth())
        self.tol_dsbox.setSizePolicy(sizePolicy)
        self.tol_dsbox.setSingleStep(0.1)
        self.tol_dsbox.setProperty("value", 0.1)
        self.tol_dsbox.setObjectName("tol_dsbox")
        self.gridLayout.addWidget(self.tol_dsbox, 3, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.data_tab)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.data_tab)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.ndigit_sbox = QtWidgets.QSpinBox(self.data_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ndigit_sbox.sizePolicy().hasHeightForWidth())
        self.ndigit_sbox.setSizePolicy(sizePolicy)
        self.ndigit_sbox.setMaximum(20)
        self.ndigit_sbox.setProperty("value", 3)
        self.ndigit_sbox.setObjectName("ndigit_sbox")
        self.gridLayout.addWidget(self.ndigit_sbox, 5, 1, 1, 1)
        self.dt_confsync_dsbox = QtWidgets.QDoubleSpinBox(self.data_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.dt_confsync_dsbox.sizePolicy().hasHeightForWidth())
        self.dt_confsync_dsbox.setSizePolicy(sizePolicy)
        self.dt_confsync_dsbox.setDecimals(1)
        self.dt_confsync_dsbox.setMinimum(1.0)
        self.dt_confsync_dsbox.setMaximum(600.0)
        self.dt_confsync_dsbox.setSingleStep(10.0)
        self.dt_confsync_dsbox.setProperty("value", 10.0)
        self.dt_confsync_dsbox.setObjectName("dt_confsync_dsbox")
        self.gridLayout.addWidget(self.dt_confsync_dsbox, 4, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.data_tab)
        self.label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40,
                                           QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 0, 1, 1)
        self.tabWidget.addTab(self.data_tab, "")
        self.view_tab = QtWidgets.QWidget()
        self.view_tab.setObjectName("view_tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.view_tab)
        self.gridLayout_2.setContentsMargins(6, 12, 6, 6)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.col_visibility_gbox = QtWidgets.QGridLayout()
        self.col_visibility_gbox.setObjectName("col_visibility_gbox")
        self.gridLayout_2.addLayout(self.col_visibility_gbox, 2, 0, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.view_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_6 = QtWidgets.QLabel(self.view_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.font_sample_lbl = QtWidgets.QLabel(self.view_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.font_sample_lbl.sizePolicy().hasHeightForWidth())
        self.font_sample_lbl.setSizePolicy(sizePolicy)
        self.font_sample_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.font_sample_lbl.setObjectName("font_sample_lbl")
        self.horizontalLayout_2.addWidget(self.font_sample_lbl)
        self.select_font_btn = QtWidgets.QPushButton(self.view_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.select_font_btn.sizePolicy().hasHeightForWidth())
        self.select_font_btn.setSizePolicy(sizePolicy)
        self.select_font_btn.setObjectName("select_font_btn")
        self.horizontalLayout_2.addWidget(self.select_font_btn)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 2)
        self.tabWidget.addTab(self.view_tab, "")
        self.config_tab = QtWidgets.QWidget()
        self.config_tab.setObjectName("config_tab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.config_tab)
        self.gridLayout_3.setContentsMargins(6, 12, 6, 6)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.change_config_path_btn = QtWidgets.QPushButton(self.config_tab)
        self.change_config_path_btn.setEnabled(False)
        self.change_config_path_btn.setObjectName("change_config_path_btn")
        self.gridLayout_3.addWidget(self.change_config_path_btn, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 2, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.config_tab)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 0, 0, 1, 1)
        self.config_path_lineEdit = QtWidgets.QLineEdit(self.config_tab)
        self.config_path_lineEdit.setReadOnly(True)
        self.config_path_lineEdit.setObjectName("config_path_lineEdit")
        self.gridLayout_3.addWidget(self.config_path_lineEdit, 0, 1, 1, 1)
        self.reset_config_btn = QtWidgets.QPushButton(self.config_tab)
        self.reset_config_btn.setObjectName("reset_config_btn")
        self.gridLayout_3.addWidget(self.reset_config_btn, 0, 3, 1, 1)
        self.purge_config_btn = QtWidgets.QPushButton(self.config_tab)
        self.purge_config_btn.setObjectName("purge_config_btn")
        self.gridLayout_3.addWidget(self.purge_config_btn, 0, 4, 1, 1)
        self.config_btns_hbox = QtWidgets.QHBoxLayout()
        self.config_btns_hbox.setContentsMargins(-1, 0, -1, -1)
        self.config_btns_hbox.setObjectName("config_btns_hbox")
        self.gridLayout_3.addLayout(self.config_btns_hbox, 1, 0, 1, 5)
        self.tabWidget.addTab(self.config_tab, "")
        self.gridLayout_9.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setSpacing(6)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem2)
        self.cancel_btn = QtWidgets.QPushButton(Dialog)
        self.cancel_btn.setObjectName("cancel_btn")
        self.horizontalLayout_12.addWidget(self.cancel_btn)
        self.ok_btn = QtWidgets.QPushButton(Dialog)
        self.ok_btn.setObjectName("ok_btn")
        self.horizontalLayout_12.addWidget(self.ok_btn)
        self.gridLayout_9.addLayout(self.horizontalLayout_12, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.ok_btn.clicked.connect(Dialog.on_click_ok)
        self.cancel_btn.clicked.connect(Dialog.reject)
        self.live_rbtn.toggled['bool'].connect(Dialog.on_toggle_mode)
        self.model_rbtn.toggled['bool'].connect(Dialog.on_toggle_mode)
        self.init_settings_chkbox.toggled['bool'].connect(
            Dialog.on_init_settings)
        self.select_font_btn.clicked.connect(Dialog.on_select_font)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.ok_btn, self.cancel_btn)
        Dialog.setTabOrder(self.cancel_btn, self.model_rbtn)
        Dialog.setTabOrder(self.model_rbtn, self.live_rbtn)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_72.setText(
            _translate("Dialog", "Initial current field set value mode"))
        self.init_settings_chkbox.setToolTip(
            _translate(
                "Dialog",
                "<html><head/><body><p>If this option is enabled, settings will be listed after loading lattice.</p></body></html>"
            ))
        self.init_settings_chkbox.setText(
            _translate(
                "Dialog",
                "Initialize device settings with the whole loaded lattice"))
        self.apply_delt_dsbox.setSuffix(_translate("Dialog", " second"))
        self.label_3.setText(
            _translate("Dialog",
                       "Time period for configuration data synchronization "))
        self.model_rbtn.setToolTip(
            _translate(
                "Dialog",
                "<html><head/><body><p>Initialize field set value from pre-defined \'model\' environment, which is maintained by \'phantasy-machines\' package.</p></body></html>"
            ))
        self.model_rbtn.setText(_translate("Dialog", "Model"))
        self.live_rbtn.setToolTip(
            _translate(
                "Dialog",
                "<html><head/><body><p>Initialize field set value by pulling the live device settings from controls network.</p></body></html>"
            ))
        self.live_rbtn.setText(_translate("Dialog", "Live"))
        self.label_4.setText(_translate("Dialog", "Float number precision"))
        self.label_2.setText(
            _translate("Dialog", "Absolute Discrepancy Tolerance"))
        self.dt_confsync_dsbox.setSuffix(_translate("Dialog", " second"))
        self.label.setText(
            _translate("Dialog", "Settling time between batch settings apply"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.data_tab),
                                  _translate("Dialog", "Data"))
        self.label_5.setText(
            _translate(
                "Dialog",
                "Check the button to hide the column of the name, uncheck to show."
            ))
        self.label_6.setText(_translate("Dialog", "Font"))
        self.font_sample_lbl.setText(_translate("Dialog", "Sample"))
        self.select_font_btn.setText(_translate("Dialog", "Select"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.view_tab),
                                  _translate("Dialog", "View"))
        self.change_config_path_btn.setText(_translate("Dialog", "Change"))
        self.label_9.setText(_translate("Dialog", "Root Path"))
        self.reset_config_btn.setText(_translate("Dialog", "Reset"))
        self.purge_config_btn.setText(_translate("Dialog", "Purge"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.config_tab),
                                  _translate("Dialog", "Configurations"))
        self.cancel_btn.setText(_translate("Dialog", "Cancel"))
        self.ok_btn.setText(_translate("Dialog", "OK"))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
