# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_post_snp.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(494, 314)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 5, 3, 1, 1)
        self.note_textEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.note_textEdit.setStyleSheet("QPlainTextEdit {\n"
                                         "    color: rgb(0, 123, 255);\n"
                                         "}")
        self.note_textEdit.setObjectName("note_textEdit")
        self.gridLayout.addWidget(self.note_textEdit, 4, 0, 1, 4)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setStyleSheet("QLabel {\n"
                                   "    border-top: 0px solid gray;\n"
                                   "    border-bottom: 1px solid gray;\n"
                                   "    padding: 2px 0px 5px 0px;\n"
                                   "}")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 4)
        self.tags_hbox = QtWidgets.QHBoxLayout()
        self.tags_hbox.setObjectName("tags_hbox")
        self.gridLayout.addLayout(self.tags_hbox, 1, 0, 1, 2)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.selected_tags = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.selected_tags.sizePolicy().hasHeightForWidth())
        self.selected_tags.setSizePolicy(sizePolicy)
        self.selected_tags.setText("")
        self.selected_tags.setObjectName("selected_tags")
        self.gridLayout.addWidget(self.selected_tags, 1, 2, 1, 2)

        self.retranslateUi(Dialog)
        self.pushButton.clicked.connect(Dialog.on_click_ok)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "OK"))
        self.note_textEdit.setPlaceholderText(
            _translate("Dialog", "Input note ..."))
        self.label_3.setText(
            _translate(
                "Dialog",
                "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Finalize a New Snapshot</span></p></body></html>"
            ))
        self.label.setText(_translate("Dialog", "Note"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
