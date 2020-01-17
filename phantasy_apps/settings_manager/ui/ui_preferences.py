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
        Dialog.resize(836, 484)
        self.gridLayout_9 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_72 = QtWidgets.QLabel(self.groupBox)
        self.label_72.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                   | QtCore.Qt.AlignVCenter)
        self.label_72.setObjectName("label_72")
        self.gridLayout.addWidget(self.label_72, 1, 0, 1, 1)
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
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40,
                                           QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
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
        self.gridLayout.addLayout(self.horizontalLayout_12, 4, 0, 1, 2)
        self.apply_delt_dsbox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.apply_delt_dsbox.setDecimals(3)
        self.apply_delt_dsbox.setMaximum(5.0)
        self.apply_delt_dsbox.setSingleStep(0.05)
        self.apply_delt_dsbox.setProperty("value", 0.05)
        self.apply_delt_dsbox.setObjectName("apply_delt_dsbox")
        self.gridLayout.addWidget(self.apply_delt_dsbox, 2, 1, 1, 1)
        self.init_settings_chkbox = QtWidgets.QCheckBox(self.groupBox)
        self.init_settings_chkbox.setObjectName("init_settings_chkbox")
        self.gridLayout.addWidget(self.init_settings_chkbox, 0, 0, 1, 2)
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
        self.label_72.setText(
            _translate("Dialog", "Initial current field set value mode"))
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
        self.label.setText(
            _translate("Dialog", "Settling time between batch settings apply"))
        self.cancel_btn.setText(_translate("Dialog", "Cancel"))
        self.ok_btn.setText(_translate("Dialog", "OK"))
        self.apply_delt_dsbox.setSuffix(_translate("Dialog", " second"))
        self.init_settings_chkbox.setToolTip(
            _translate(
                "Dialog",
                "<html><head/><body><p>If this option is enabled, settings will be listed after loading lattice.</p></body></html>"
            ))
        self.init_settings_chkbox.setText(
            _translate(
                "Dialog",
                "Initialize device settings with the whole loaded lattice"))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
