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
        Dialog.resize(573, 379)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.tags_area = QtWidgets.QScrollArea(Dialog)
        self.tags_area.setWidgetResizable(True)
        self.tags_area.setObjectName("tags_area")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 563, 89))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.tags_area.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.tags_area, 3, 0, 1, 3)
        self.note_textEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.note_textEdit.setStyleSheet("QPlainTextEdit {\n"
                                         "    color: rgb(0, 123, 255);\n"
                                         "}")
        self.note_textEdit.setObjectName("note_textEdit")
        self.gridLayout.addWidget(self.note_textEdit, 5, 0, 1, 3)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setStyleSheet("QLabel {\n"
                                   "    border-top: 0px solid gray;\n"
                                   "    border-bottom: 1px solid gray;\n"
                                   "    padding: 2px 0px 5px 0px;\n"
                                   "}")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 3)
        self.selected_tags = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.selected_tags.sizePolicy().hasHeightForWidth())
        self.selected_tags.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setItalic(True)
        self.selected_tags.setFont(font)
        self.selected_tags.setText("")
        self.selected_tags.setObjectName("selected_tags")
        self.gridLayout.addWidget(self.selected_tags, 2, 1, 1, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.gridLayout.addLayout(self.horizontalLayout, 6, 0, 1, 3)

        self.retranslateUi(Dialog)
        self.pushButton.clicked.connect(Dialog.on_click_ok)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Note"))
        self.note_textEdit.setPlaceholderText(
            _translate("Dialog", "Input note ..."))
        self.label_2.setText(_translate("Dialog", "Tags"))
        self.label_3.setText(
            _translate(
                "Dialog",
                "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Finalize a New Snapshot</span></p></body></html>"
            ))
        self.pushButton.setText(_translate("Dialog", "OK"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
