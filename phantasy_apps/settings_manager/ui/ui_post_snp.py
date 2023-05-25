# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_post_snp.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1052, 669)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setContentsMargins(6, 8, 6, 6)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.on_template_rbtn = QtWidgets.QRadioButton(Dialog)
        self.on_template_rbtn.setObjectName("on_template_rbtn")
        self.snpBaseBtnGrp = QtWidgets.QButtonGroup(Dialog)
        self.snpBaseBtnGrp.setObjectName("snpBaseBtnGrp")
        self.snpBaseBtnGrp.addButton(self.on_template_rbtn)
        self.gridLayout.addWidget(self.on_template_rbtn, 3, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.is_match_lbl = QtWidgets.QLabel(Dialog)
        self.is_match_lbl.setMinimumSize(QtCore.QSize(64, 64))
        self.is_match_lbl.setMaximumSize(QtCore.QSize(64, 64))
        self.is_match_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.is_match_lbl.setObjectName("is_match_lbl")
        self.horizontalLayout_2.addWidget(self.is_match_lbl)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 2, 3, 1)
        self.tags_area = QtWidgets.QScrollArea(Dialog)
        self.tags_area.setWidgetResizable(True)
        self.tags_area.setObjectName("tags_area")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1038, 89))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.tags_area.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.tags_area, 8, 0, 1, 4)
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 9, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setStyleSheet("QLabel {\n"
                                   "    border: 0.5px solid gray;\n"
                                   "    padding: 2px 5px 2px 5px; \n"
                                   "}")
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("QLabel {\n"
                                   "    border-top: 0px solid gray;\n"
                                   "    border-bottom: 1px solid gray;\n"
                                   "    padding: 2px 0px 5px 0px;\n"
                                   "}")
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 4)
        self.selected_tags = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.selected_tags.sizePolicy().hasHeightForWidth())
        self.selected_tags.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setItalic(False)
        self.selected_tags.setFont(font)
        self.selected_tags.setStyleSheet(
            "QLabel {\n"
            "    color: rgb(0, 123, 255);\n"
            "    background-color: rgb(233, 233, 233);\n"
            "}")
        self.selected_tags.setText("")
        self.selected_tags.setObjectName("selected_tags")
        self.gridLayout.addWidget(self.selected_tags, 7, 1, 1, 3)
        self.beamSpeciesDisplayWidget = BeamSpeciesDisplayWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.beamSpeciesDisplayWidget.sizePolicy().hasHeightForWidth())
        self.beamSpeciesDisplayWidget.setSizePolicy(sizePolicy)
        self.beamSpeciesDisplayWidget.setProperty("expanded", True)
        self.beamSpeciesDisplayWidget.setProperty(
            "allowClickingIonSourceButtons", False)
        self.beamSpeciesDisplayWidget.setObjectName("beamSpeciesDisplayWidget")
        self.gridLayout.addWidget(self.beamSpeciesDisplayWidget, 1, 3, 3, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.show_adv_ctls_btn = QtWidgets.QToolButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.show_adv_ctls_btn.sizePolicy().hasHeightForWidth())
        self.show_adv_ctls_btn.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/sm-icons/right-arrow.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/sm-icons/left-arrow.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.show_adv_ctls_btn.setIcon(icon)
        self.show_adv_ctls_btn.setIconSize(QtCore.QSize(32, 32))
        self.show_adv_ctls_btn.setCheckable(True)
        self.show_adv_ctls_btn.setChecked(True)
        self.show_adv_ctls_btn.setToolButtonStyle(
            QtCore.Qt.ToolButtonTextBesideIcon)
        self.show_adv_ctls_btn.setAutoRaise(True)
        self.show_adv_ctls_btn.setObjectName("show_adv_ctls_btn")
        self.horizontalLayout.addWidget(self.show_adv_ctls_btn)
        self.adv_frame = QtWidgets.QFrame(Dialog)
        self.adv_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.adv_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.adv_frame.setObjectName("adv_frame")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.adv_frame)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(4, -1, -1, -1)
        self.horizontalLayout_4.setSpacing(4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.snp_ms_chkbox = QtWidgets.QCheckBox(self.adv_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.snp_ms_chkbox.sizePolicy().hasHeightForWidth())
        self.snp_ms_chkbox.setSizePolicy(sizePolicy)
        self.snp_ms_chkbox.setIconSize(QtCore.QSize(32, 32))
        self.snp_ms_chkbox.setChecked(True)
        self.snp_ms_chkbox.setObjectName("snp_ms_chkbox")
        self.horizontalLayout_4.addWidget(self.snp_ms_chkbox)
        self.wysiwyc_chkbox = QtWidgets.QCheckBox(self.adv_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.wysiwyc_chkbox.sizePolicy().hasHeightForWidth())
        self.wysiwyc_chkbox.setSizePolicy(sizePolicy)
        self.wysiwyc_chkbox.setIconSize(QtCore.QSize(32, 32))
        self.wysiwyc_chkbox.setObjectName("wysiwyc_chkbox")
        self.horizontalLayout_4.addWidget(self.wysiwyc_chkbox)
        self.cast_chkbox = QtWidgets.QCheckBox(self.adv_frame)
        self.cast_chkbox.setChecked(True)
        self.cast_chkbox.setObjectName("cast_chkbox")
        self.horizontalLayout_4.addWidget(self.cast_chkbox)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.horizontalLayout.addWidget(self.adv_frame)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pb_lbl = QtWidgets.QLabel(Dialog)
        self.pb_lbl.setStyleSheet("QLabel {\n"
                                  "    font-family: monospace;\n"
                                  "}")
        self.pb_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.pb_lbl.setObjectName("pb_lbl")
        self.verticalLayout_2.addWidget(self.pb_lbl)
        self.pb = QtWidgets.QProgressBar(Dialog)
        self.pb.setMinimumSize(QtCore.QSize(145, 12))
        self.pb.setMaximumSize(QtCore.QSize(145, 12))
        self.pb.setStyleSheet("QProgressBar {\n"
                              "    border: 1px solid grayl;\n"
                              "    border-radius: 1px;\n"
                              "    text-align: center;\n"
                              "}\n"
                              "QProgressBar::chunk {\n"
                              "    background-color: #05B8CC;\n"
                              "    width: 10px;\n"
                              "    margin: 0.5px;\n"
                              "}")
        self.pb.setMaximum(0)
        self.pb.setProperty("value", -1)
        self.pb.setObjectName("pb")
        self.verticalLayout_2.addWidget(self.pb)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.exit_btn = QtWidgets.QPushButton(Dialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/sm-icons/exit.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exit_btn.setIcon(icon1)
        self.exit_btn.setIconSize(QtCore.QSize(32, 32))
        self.exit_btn.setObjectName("exit_btn")
        self.horizontalLayout.addWidget(self.exit_btn)
        self.capture_btn = QtWidgets.QPushButton(Dialog)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/sm-icons/snapshot.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.capture_btn.setIcon(icon2)
        self.capture_btn.setIconSize(QtCore.QSize(32, 32))
        self.capture_btn.setObjectName("capture_btn")
        self.horizontalLayout.addWidget(self.capture_btn)
        self.gridLayout.addLayout(self.horizontalLayout, 11, 0, 1, 4)
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setStyleSheet("QTextEdit {\n"
                                    "    color: gray;\n"
                                    "}")
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 6, 0, 1, 4)
        self.orig_template_lbl = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.orig_template_lbl.sizePolicy().hasHeightForWidth())
        self.orig_template_lbl.setSizePolicy(sizePolicy)
        self.orig_template_lbl.setStyleSheet("QLabel {\n"
                                             "    border: 0.5px solid gray;\n"
                                             "    padding: 2px 5px 2px 5px; \n"
                                             "}")
        self.orig_template_lbl.setAlignment(QtCore.Qt.AlignLeading
                                            | QtCore.Qt.AlignLeft
                                            | QtCore.Qt.AlignVCenter)
        self.orig_template_lbl.setObjectName("orig_template_lbl")
        self.gridLayout.addWidget(self.orig_template_lbl, 1, 1, 1, 1)
        self.note_textEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.note_textEdit.setStyleSheet("QPlainTextEdit {\n"
                                         "    color: rgb(0, 123, 255);\n"
                                         "}")
        self.note_textEdit.setObjectName("note_textEdit")
        self.gridLayout.addWidget(self.note_textEdit, 10, 0, 1, 4)
        self.on_loaded_rbtn = QtWidgets.QRadioButton(Dialog)
        self.on_loaded_rbtn.setChecked(True)
        self.on_loaded_rbtn.setObjectName("on_loaded_rbtn")
        self.snpBaseBtnGrp.addButton(self.on_loaded_rbtn)
        self.gridLayout.addWidget(self.on_loaded_rbtn, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 7, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 0, 0, -1)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.template_area = QtWidgets.QScrollArea(Dialog)
        self.template_area.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.template_area.sizePolicy().hasHeightForWidth())
        self.template_area.setSizePolicy(sizePolicy)
        self.template_area.setWidgetResizable(True)
        self.template_area.setObjectName("template_area")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(
            QtCore.QRect(0, 0, 774, 130))
        self.scrollAreaWidgetContents_2.setObjectName(
            "scrollAreaWidgetContents_2")
        self.template_area.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_3.addWidget(self.template_area)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, 0, -1, -1)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy)
        self.plainTextEdit.setStyleSheet("QPlainTextEdit {\n"
                                         "    background-color: #F5F5F5;\n"
                                         "}")
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.isrc_name_meta_cbb = QtWidgets.QComboBox(Dialog)
        self.isrc_name_meta_cbb.setObjectName("isrc_name_meta_cbb")
        self.isrc_name_meta_cbb.addItem("")
        self.isrc_name_meta_cbb.addItem("")
        self.isrc_name_meta_cbb.addItem("")
        self.verticalLayout.addWidget(self.isrc_name_meta_cbb)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout_3, 4, 0, 1, 4)

        self.retranslateUi(Dialog)
        self.capture_btn.clicked.connect(
            Dialog.on_click_capture)  # type: ignore
        self.exit_btn.clicked.connect(Dialog.on_click_exit)  # type: ignore
        self.on_template_rbtn.toggled['bool'].connect(
            self.template_area.setEnabled)  # type: ignore
        self.on_loaded_rbtn.toggled['bool'].connect(
            Dialog.onCheckOnLoaded)  # type: ignore
        self.on_template_rbtn.toggled['bool'].connect(
            Dialog.onCheckOnTemplate)  # type: ignore
        self.isrc_name_meta_cbb.currentTextChanged['QString'].connect(
            Dialog.onIsrcNameMetaChanged)  # type: ignore
        self.show_adv_ctls_btn.toggled['bool'].connect(
            self.adv_frame.setVisible)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.note_textEdit, self.capture_btn)
        Dialog.setTabOrder(self.capture_btn, self.exit_btn)
        Dialog.setTabOrder(self.exit_btn, self.on_loaded_rbtn)
        Dialog.setTabOrder(self.on_loaded_rbtn, self.on_template_rbtn)
        Dialog.setTabOrder(self.on_template_rbtn, self.template_area)
        Dialog.setTabOrder(self.template_area, self.plainTextEdit)
        Dialog.setTabOrder(self.plainTextEdit, self.isrc_name_meta_cbb)
        Dialog.setTabOrder(self.isrc_name_meta_cbb, self.textEdit)
        Dialog.setTabOrder(self.textEdit, self.tags_area)
        Dialog.setTabOrder(self.tags_area, self.show_adv_ctls_btn)
        Dialog.setTabOrder(self.show_adv_ctls_btn, self.snp_ms_chkbox)
        Dialog.setTabOrder(self.snp_ms_chkbox, self.wysiwyc_chkbox)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.on_template_rbtn.setText(_translate("Dialog", "On A Template"))
        self.is_match_lbl.setText(_translate("Dialog", "x"))
        self.label.setText(_translate("Dialog", "Note"))
        self.label_5.setText(_translate("Dialog", "Beam in Operations"))
        self.label_4.setText(_translate("Dialog", "Create a New Snapshot"))
        self.show_adv_ctls_btn.setToolTip(
            _translate(
                "Dialog",
                "<html><head/><body><p>Show/hide advanced controls.</p></body></html>"
            ))
        self.show_adv_ctls_btn.setText(_translate("Dialog", "Advanced"))
        self.snp_ms_chkbox.setToolTip(
            _translate(
                "Dialog",
                "<html><head/><body><p>Check to capture machine state data with device settings data.</p></body></html>"
            ))
        self.snp_ms_chkbox.setText(_translate("Dialog", "with Machine State"))
        self.wysiwyc_chkbox.setToolTip(
            _translate(
                "Dialog",
                "<html><head/><body><p>If checked, take the snapshot in the way of \'What You See Is What You Capture\'.</p></body></html>"
            ))
        self.wysiwyc_chkbox.setText(_translate("Dialog", "WYSIWYC"))
        self.cast_chkbox.setToolTip(
            _translate(
                "Dialog",
                "<html><head/><body><p>Check to cast the captured snapshot to the main interface.</p></body></html>"
            ))
        self.cast_chkbox.setText(_translate("Dialog", "Cast"))
        self.pb_lbl.setText(_translate("Dialog", "0:00:00"))
        self.exit_btn.setToolTip(
            _translate(
                "Dialog",
                "<html><head/><body><p>Click to exit the window.</p></body></html>"
            ))
        self.exit_btn.setText(_translate("Dialog", "Exit"))
        self.capture_btn.setToolTip(
            _translate(
                "Dialog",
                "<html><head/><body><p>Click to create a new snapshot.</p></body></html>"
            ))
        self.capture_btn.setText(_translate("Dialog", "Capture"))
        self.textEdit.setHtml(
            _translate(
                "Dialog",
                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:\'Cantarell\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                "<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\"\" style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This option will be enabled if the unmatched symbol <img src=\":/sm-icons/fail.png\" width=\"24\" style=\"vertical-align: middle;\" /> is showing.</li>\n"
                "<li style=\"\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">By default, the template button matches the machine operations is checked. </li>\n"
                "<li style=\"\" style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">It\'s the user\'s decision to choose other templates or re-check <span style=\" font-style:italic;\">On Currently Loaded</span> option.</li></ul></body></html>"
            ))
        self.orig_template_lbl.setToolTip(
            _translate(
                "Dialog",
                "<html><head/><body><p>The originated snapshot template.</p></body></html>"
            ))
        self.orig_template_lbl.setText(
            _translate("Dialog", "originated template"))
        self.note_textEdit.setPlaceholderText(
            _translate("Dialog", "Input note ..."))
        self.on_loaded_rbtn.setText(_translate("Dialog",
                                               "On Currently Loaded"))
        self.label_2.setText(_translate("Dialog", "Tags"))
        self.plainTextEdit.setPlainText(
            _translate("Dialog", "Fetch the ion metadata from"))
        self.isrc_name_meta_cbb.setItemText(0, _translate("Dialog", "Live"))
        self.isrc_name_meta_cbb.setItemText(1, _translate("Dialog", "Artemis"))
        self.isrc_name_meta_cbb.setItemText(2, _translate("Dialog", "HP-ECR"))


from phantasy_ui.widgets.beam_species_displayWidget import BeamSpeciesDisplayWidget
from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
