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
        self.label_72.setAlignment(QtCore.Qt.AlignRight
                                   | QtCore.Qt.AlignTrailing
                                   | QtCore.Qt.AlignVCenter)
        self.label_72.setObjectName("label_72")
        self.gridLayout.addWidget(self.label_72, 0, 0, 1, 1)
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
        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing
                                | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.apply_delt_dsbox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.apply_delt_dsbox.setDecimals(3)
        self.apply_delt_dsbox.setMaximum(5.0)
        self.apply_delt_dsbox.setSingleStep(0.05)
        self.apply_delt_dsbox.setProperty("value", 0.05)
        self.apply_delt_dsbox.setObjectName("apply_delt_dsbox")
        self.gridLayout.addWidget(self.apply_delt_dsbox, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40,
                                           QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
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
        self.gridLayout.addLayout(self.horizontalLayout_12, 3, 0, 1, 2)
        self.gridLayout_9.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.ok_btn.clicked.connect(Dialog.on_click_ok)
        self.cancel_btn.clicked.connect(Dialog.reject)
        self.live_rbtn.toggled['bool'].connect(Dialog.on_toggle_mode)
        self.model_rbtn.toggled['bool'].connect(Dialog.on_toggle_mode)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "Preferences"))
        self.label_72.setText(
            _translate("Dialog", "Initial Current Field Set Value Mode"))
        self.model_rbtn.setText(_translate("Dialog", "Model"))
        self.live_rbtn.setText(_translate("Dialog", "Live"))
        self.label.setText(
            _translate("Dialog", "Time Interval Between Batch Settings Apply"))
        self.apply_delt_dsbox.setSuffix(_translate("Dialog", " second"))
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
