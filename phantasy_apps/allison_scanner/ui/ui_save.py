# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_save.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(741, 424)
        Dialog.setStyleSheet(
            "QLineEdit {\n"
            "    border: 0.5px solid gray;\n"
            "    padding: 1 5px;\n"
            "    border-radius: 3px;\n"
            "}\n"
            "\n"
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
            "}")
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.dirpath_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.dirpath_lineEdit.setReadOnly(True)
        self.dirpath_lineEdit.setObjectName("dirpath_lineEdit")
        self.gridLayout.addWidget(self.dirpath_lineEdit, 2, 2, 1, 3)
        self.cancel_btn = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cancel_btn.sizePolicy().hasHeightForWidth())
        self.cancel_btn.setSizePolicy(sizePolicy)
        self.cancel_btn.setAutoDefault(False)
        self.cancel_btn.setObjectName("cancel_btn")
        self.gridLayout.addWidget(self.cancel_btn, 5, 4, 1, 1)
        self.save_btn = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.save_btn.sizePolicy().hasHeightForWidth())
        self.save_btn.setSizePolicy(sizePolicy)
        self.save_btn.setAutoDefault(False)
        self.save_btn.setObjectName("save_btn")
        self.gridLayout.addWidget(self.save_btn, 5, 5, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 5, 1, 1, 3)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                   | QtCore.Qt.AlignVCenter)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setContentsMargins(4, 10, 4, 4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.note_plainTextEdit = QtWidgets.QPlainTextEdit(self.groupBox)
        self.note_plainTextEdit.setObjectName("note_plainTextEdit")
        self.gridLayout_2.addWidget(self.note_plainTextEdit, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 4, 1, 1, 5)
        self.filepath_lineEdit = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.filepath_lineEdit.sizePolicy().hasHeightForWidth())
        self.filepath_lineEdit.setSizePolicy(sizePolicy)
        self.filepath_lineEdit.setObjectName("filepath_lineEdit")
        self.gridLayout.addWidget(self.filepath_lineEdit, 3, 2, 1, 3)
        self.locate_dirpath_btn = QtWidgets.QPushButton(Dialog)
        self.locate_dirpath_btn.setObjectName("locate_dirpath_btn")
        self.gridLayout.addWidget(self.locate_dirpath_btn, 2, 5, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 5, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 4)
        self.save_image_chkbox = QtWidgets.QCheckBox(Dialog)
        self.save_image_chkbox.setCheckable(True)
        self.save_image_chkbox.setChecked(True)
        self.save_image_chkbox.setObjectName("save_image_chkbox")
        self.gridLayout.addWidget(self.save_image_chkbox, 0, 5, 1, 1)

        self.retranslateUi(Dialog)
        self.cancel_btn.clicked.connect(Dialog.reject)  # type: ignore
        self.save_btn.clicked.connect(Dialog.on_save_data)  # type: ignore
        self.pushButton.clicked.connect(
            Dialog.auto_fill_filepath)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.cancel_btn.setText(_translate("Dialog", "Cancel"))
        self.save_btn.setText(_translate("Dialog", "Save"))
        self.groupBox.setTitle(_translate("Dialog", "Note"))
        self.note_plainTextEdit.setToolTip(
            _translate("Dialog", "Input additional note for saved data file."))
        self.locate_dirpath_btn.setText(_translate("Dialog", "Locate"))
        self.label_3.setText(_translate("Dialog", "Root Directory"))
        self.label.setText(_translate("Dialog", "Filepath"))
        self.pushButton.setToolTip(
            _translate("Dialog", "Generate filename by timestamp."))
        self.pushButton.setText(_translate("Dialog", "Auto"))
        self.label_2.setText(
            _translate("Dialog", "Save the data and image to the files."))
        self.save_image_chkbox.setText(_translate("Dialog", "Image"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
