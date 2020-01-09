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
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_72 = QtWidgets.QLabel(self.groupBox)
        self.label_72.setObjectName("label_72")
        self.horizontalLayout_13.addWidget(self.label_72)
        self.model_rbtn = QtWidgets.QRadioButton(self.groupBox)
        self.model_rbtn.setChecked(False)
        self.model_rbtn.setObjectName("model_rbtn")
        self.field_init_mode = QtWidgets.QButtonGroup(Dialog)
        self.field_init_mode.setObjectName("field_init_mode")
        self.field_init_mode.addButton(self.model_rbtn)
        self.horizontalLayout_13.addWidget(self.model_rbtn)
        self.live_rbtn = QtWidgets.QRadioButton(self.groupBox)
        self.live_rbtn.setChecked(True)
        self.live_rbtn.setObjectName("live_rbtn")
        self.field_init_mode.addButton(self.live_rbtn)
        self.horizontalLayout_13.addWidget(self.live_rbtn)
        self.verticalLayout.addLayout(self.horizontalLayout_13)
        spacerItem = QtWidgets.QSpacerItem(20, 40,
                                           QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem1)
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_12.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_12.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_12)
        self.gridLayout_9.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.pushButton_2.clicked.connect(Dialog.accept)
        self.pushButton.clicked.connect(Dialog.reject)
        self.model_rbtn.toggled['bool'].connect(Dialog.on_toggle_mode)
        self.live_rbtn.toggled['bool'].connect(Dialog.on_toggle_mode)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "GroupBox"))
        self.label_72.setText(
            _translate("Dialog", "Initial Current Field Set Value Mode"))
        self.model_rbtn.setText(_translate("Dialog", "Model"))
        self.live_rbtn.setText(_translate("Dialog", "Live"))
        self.pushButton.setText(_translate("Dialog", "Cancel"))
        self.pushButton_2.setText(_translate("Dialog", "OK"))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
