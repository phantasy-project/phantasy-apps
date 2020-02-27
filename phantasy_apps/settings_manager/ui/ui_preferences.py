# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_preferences.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(836, 484)
        self.gridLayout_9 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout.addWidget(self.plainTextEdit, 7, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40,
                                           QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)
        self.label_72 = QtWidgets.QLabel(self.groupBox)
        self.label_72.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                   | QtCore.Qt.AlignVCenter)
        self.label_72.setObjectName("label_72")
        self.gridLayout.addWidget(self.label_72, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem1)
        self.cancel_btn = QtWidgets.QPushButton(self.groupBox)
        self.cancel_btn.setObjectName("cancel_btn")
        self.horizontalLayout_12.addWidget(self.cancel_btn)
        self.ok_btn = QtWidgets.QPushButton(self.groupBox)
        self.ok_btn.setObjectName("ok_btn")
        self.horizontalLayout_12.addWidget(self.ok_btn)
        self.gridLayout.addLayout(self.horizontalLayout_12, 9, 0, 1, 2)
        self.tol_dsbox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.tol_dsbox.setSingleStep(0.1)
        self.tol_dsbox.setProperty("value", 0.1)
        self.tol_dsbox.setObjectName("tol_dsbox")
        self.gridLayout.addWidget(self.tol_dsbox, 3, 1, 1, 1)
        self.dt_confsync_dsbox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.dt_confsync_dsbox.setDecimals(1)
        self.dt_confsync_dsbox.setMinimum(1.0)
        self.dt_confsync_dsbox.setMaximum(600.0)
        self.dt_confsync_dsbox.setSingleStep(10.0)
        self.dt_confsync_dsbox.setProperty("value", 10.0)
        self.dt_confsync_dsbox.setObjectName("dt_confsync_dsbox")
        self.gridLayout.addWidget(self.dt_confsync_dsbox, 4, 1, 1, 1)
        self.ndigit_sbox = QtWidgets.QSpinBox(self.groupBox)
        self.ndigit_sbox.setMaximum(20)
        self.ndigit_sbox.setProperty("value", 3)
        self.ndigit_sbox.setObjectName("ndigit_sbox")
        self.gridLayout.addWidget(self.ndigit_sbox, 5, 1, 1, 1)
        self.init_settings_chkbox = QtWidgets.QCheckBox(self.groupBox)
        self.init_settings_chkbox.setObjectName("init_settings_chkbox")
        self.gridLayout.addWidget(self.init_settings_chkbox, 0, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.model_rbtn = QtWidgets.QRadioButton(self.groupBox)
        self.model_rbtn.setChecked(False)
        self.model_rbtn.setObjectName("model_rbtn")
        self.field_init_mode = QtWidgets.QButtonGroup(Dialog)
        self.field_init_mode.setObjectName("field_init_mode")
        self.field_init_mode.addButton(self.model_rbtn)
        self.horizontalLayout.addWidget(self.model_rbtn)
        self.live_rbtn = QtWidgets.QRadioButton(self.groupBox)
        self.live_rbtn.setChecked(True)
        self.live_rbtn.setObjectName("live_rbtn")
        self.field_init_mode.addButton(self.live_rbtn)
        self.horizontalLayout.addWidget(self.live_rbtn)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        self.apply_delt_dsbox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.apply_delt_dsbox.setDecimals(3)
        self.apply_delt_dsbox.setMaximum(5.0)
        self.apply_delt_dsbox.setSingleStep(0.05)
        self.apply_delt_dsbox.setProperty("value", 0.05)
        self.apply_delt_dsbox.setObjectName("apply_delt_dsbox")
        self.gridLayout.addWidget(self.apply_delt_dsbox, 2, 1, 1, 1)
        self.col_visibility_gbox = QtWidgets.QGridLayout()
        self.col_visibility_gbox.setObjectName("col_visibility_gbox")
        self.gridLayout.addLayout(self.col_visibility_gbox, 7, 1, 2, 1)
        self.gridLayout_9.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.ok_btn.clicked.connect(Dialog.on_click_ok)
        self.cancel_btn.clicked.connect(Dialog.reject)
        self.live_rbtn.toggled['bool'].connect(Dialog.on_toggle_mode)
        self.model_rbtn.toggled['bool'].connect(Dialog.on_toggle_mode)
        self.init_settings_chkbox.toggled['bool'].connect(
            Dialog.on_init_settings)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.ok_btn, self.cancel_btn)
        Dialog.setTabOrder(self.cancel_btn, self.model_rbtn)
        Dialog.setTabOrder(self.model_rbtn, self.live_rbtn)
        Dialog.setTabOrder(self.live_rbtn, self.apply_delt_dsbox)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "Preferences"))
        self.plainTextEdit.setPlainText(
            _translate(
                "Dialog",
                "Check the button to hide regarding column, otherwise show the column. "
            ))
        self.label.setText(
            _translate("Dialog", "Settling time between batch settings apply"))
        self.label_3.setText(
            _translate("Dialog",
                       "Time period for configuration data synchronization "))
        self.label_5.setText(_translate("Dialog", "Show/hide columns"))
        self.label_72.setText(
            _translate("Dialog", "Initial current field set value mode"))
        self.label_2.setText(
            _translate("Dialog", "Absolute Discrepancy Tolerance"))
        self.cancel_btn.setText(_translate("Dialog", "Cancel"))
        self.ok_btn.setText(_translate("Dialog", "OK"))
        self.dt_confsync_dsbox.setSuffix(_translate("Dialog", " second"))
        self.init_settings_chkbox.setToolTip(
            _translate(
                "Dialog",
                "<html><head/><body><p>If this option is enabled, settings will be listed after loading lattice.</p></body></html>"
            ))
        self.init_settings_chkbox.setText(
            _translate(
                "Dialog",
                "Initialize device settings with the whole loaded lattice"))
        self.label_4.setText(_translate("Dialog", "Float number precision"))
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
        self.apply_delt_dsbox.setSuffix(_translate("Dialog", " second"))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
