# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_layout.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1074, 605)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.drawing_vbox = QtWidgets.QVBoxLayout()
        self.drawing_vbox.setContentsMargins(0, 0, -1, -1)
        self.drawing_vbox.setSpacing(6)
        self.drawing_vbox.setObjectName("drawing_vbox")
        self.geometry_widget = QtWidgets.QWidget(Form)
        self.geometry_widget.setObjectName("geometry_widget")
        self.geometry_gbox = QtWidgets.QGridLayout(self.geometry_widget)
        self.geometry_gbox.setContentsMargins(10, 10, 10, 10)
        self.geometry_gbox.setSpacing(8)
        self.geometry_gbox.setObjectName("geometry_gbox")
        self.label_12 = QtWidgets.QLabel(self.geometry_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.geometry_gbox.addWidget(self.label_12, 1, 6, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.geometry_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        font.setItalic(False)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.geometry_gbox.addWidget(self.label_7, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.geometry_widget)
        self.label_3.setAlignment(QtCore.Qt.AlignRight
                                  | QtCore.Qt.AlignTrailing
                                  | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.geometry_gbox.addWidget(self.label_3, 2, 1, 1, 1)
        self.gap_lineEdit = QtWidgets.QLineEdit(self.geometry_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.gap_lineEdit.sizePolicy().hasHeightForWidth())
        self.gap_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.gap_lineEdit.setFont(font)
        self.gap_lineEdit.setReadOnly(True)
        self.gap_lineEdit.setObjectName("gap_lineEdit")
        self.geometry_gbox.addWidget(self.gap_lineEdit, 2, 3, 1, 1)
        self.length_lineEdit = QtWidgets.QLineEdit(self.geometry_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.length_lineEdit.sizePolicy().hasHeightForWidth())
        self.length_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.length_lineEdit.setFont(font)
        self.length_lineEdit.setReadOnly(True)
        self.length_lineEdit.setObjectName("length_lineEdit")
        self.geometry_gbox.addWidget(self.length_lineEdit, 1, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.geometry_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.geometry_gbox.addWidget(self.label_4, 2, 2, 1, 1)
        self.length2_lineEdit = QtWidgets.QLineEdit(self.geometry_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.length2_lineEdit.sizePolicy().hasHeightForWidth())
        self.length2_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.length2_lineEdit.setFont(font)
        self.length2_lineEdit.setReadOnly(True)
        self.length2_lineEdit.setObjectName("length2_lineEdit")
        self.geometry_gbox.addWidget(self.length2_lineEdit, 1, 7, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.geometry_widget)
        self.label_2.setAlignment(QtCore.Qt.AlignRight
                                  | QtCore.Qt.AlignTrailing
                                  | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.geometry_gbox.addWidget(self.label_2, 1, 1, 1, 1)
        self.length1_lineEdit = QtWidgets.QLineEdit(self.geometry_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.length1_lineEdit.sizePolicy().hasHeightForWidth())
        self.length1_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.length1_lineEdit.setFont(font)
        self.length1_lineEdit.setReadOnly(True)
        self.length1_lineEdit.setObjectName("length1_lineEdit")
        self.geometry_gbox.addWidget(self.length1_lineEdit, 1, 5, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.geometry_widget)
        self.label_5.setAlignment(QtCore.Qt.AlignRight
                                  | QtCore.Qt.AlignTrailing
                                  | QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.geometry_gbox.addWidget(self.label_5, 3, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.geometry_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.geometry_gbox.addWidget(self.label_13, 1, 4, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_6 = QtWidgets.QLabel(self.geometry_widget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.slit_thickness_lineEdit = QtWidgets.QLineEdit(
            self.geometry_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.slit_thickness_lineEdit.sizePolicy().hasHeightForWidth())
        self.slit_thickness_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.slit_thickness_lineEdit.setFont(font)
        self.slit_thickness_lineEdit.setReadOnly(True)
        self.slit_thickness_lineEdit.setObjectName("slit_thickness_lineEdit")
        self.horizontalLayout.addWidget(self.slit_thickness_lineEdit)
        self.geometry_gbox.addLayout(self.horizontalLayout, 3, 2, 1, 2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_28 = QtWidgets.QLabel(self.geometry_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        self.label_28.setFont(font)
        self.label_28.setObjectName("label_28")
        self.horizontalLayout_2.addWidget(self.label_28)
        self.slit_width_lineEdit = QtWidgets.QLineEdit(self.geometry_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.slit_width_lineEdit.sizePolicy().hasHeightForWidth())
        self.slit_width_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.slit_width_lineEdit.setFont(font)
        self.slit_width_lineEdit.setReadOnly(True)
        self.slit_width_lineEdit.setObjectName("slit_width_lineEdit")
        self.horizontalLayout_2.addWidget(self.slit_width_lineEdit)
        self.geometry_gbox.addLayout(self.horizontalLayout_2, 3, 4, 1, 4)
        self.drawing_vbox.addWidget(self.geometry_widget)
        self.as_drawing = QtWidgets.QLabel(Form)
        self.as_drawing.setText("")
        self.as_drawing.setPixmap(
            QtGui.QPixmap(":/icons/as_schematic_100dpi.png"))
        self.as_drawing.setObjectName("as_drawing")
        self.drawing_vbox.addWidget(self.as_drawing)
        self.gridLayout.addLayout(self.drawing_vbox, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.device_name_lbl = QtWidgets.QLabel(Form)
        self.device_name_lbl.setStyleSheet(
            "QLabel {\n"
            "    font-weight: bold;\n"
            "    background-color: rgb(215, 253, 255);\n"
            "    color: rgb(0, 85, 255)\n"
            "}")
        self.device_name_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.device_name_lbl.setObjectName("device_name_lbl")
        self.gridLayout.addWidget(self.device_name_lbl, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_12.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Length [mm], (<span style=\" font-style:italic;\">l</span><span style=\" font-style:italic; vertical-align:sub;\">2</span>)</p></body></html>"
            ))
        self.label_12.setText(
            _translate(
                "Form",
                "<html><head/><body><p><span style=\" font-style:italic;\">l</span><span style=\" vertical-align:sub;\">2</span></p></body></html>"
            ))
        self.label_7.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Length [mm], (<span style=\" font-style:italic;\">l</span>)</p></body></html>"
            ))
        self.label_7.setText(
            _translate(
                "Form",
                "<html><head/><body><p><span style=\" font-style:italic;\">l</span></p></body></html>"
            ))
        self.label_3.setText(
            _translate(
                "Form",
                "<html><head/><body><p><span style=\" text-decoration: underline;\">Gap [mm]</span></p></body></html>"
            ))
        self.gap_lineEdit.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Gap [mm], (<span style=\" font-style:italic;\">g</span>)</p></body></html>"
            ))
        self.length_lineEdit.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Length [mm], (<span style=\" font-style:italic;\">l</span>)</p></body></html>"
            ))
        self.label_4.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Gap [mm], (<span style=\" font-style:italic;\">g</span>)</p></body></html>"
            ))
        self.label_4.setText(
            _translate(
                "Form",
                "<html><head/><body><p><span style=\" font-style:italic;\">g</span></p></body></html>"
            ))
        self.length2_lineEdit.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Length [mm], (<span style=\" font-style:italic;\">l</span><span style=\" font-style:italic; vertical-align:sub;\">2</span>)</p></body></html>"
            ))
        self.label_2.setText(
            _translate(
                "Form",
                "<html><head/><body><p><span style=\" text-decoration: underline;\">Lengths [mm]</span></p></body></html>"
            ))
        self.length1_lineEdit.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Length [mm], (<span style=\" font-style:italic;\">l</span><span style=\" font-style:italic; vertical-align:sub;\">1</span>)</p></body></html>"
            ))
        self.label_5.setText(
            _translate(
                "Form",
                "<html><head/><body><p><span style=\" text-decoration: underline;\">Slit [mm]</span></p></body></html>"
            ))
        self.label_13.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Length [mm], (<span style=\" font-style:italic;\">l</span><span style=\" font-style:italic; vertical-align:sub;\">1</span>)</p></body></html>"
            ))
        self.label_13.setText(
            _translate(
                "Form",
                "<html><head/><body><p><span style=\" font-style:italic;\">l</span><span style=\" vertical-align:sub;\">1</span></p></body></html>"
            ))
        self.label_6.setText(
            _translate(
                "Form",
                "<html><head/><body><p>Thickness (<span style=\" font-style:italic;\">d</span>)</p></body></html>"
            ))
        self.slit_thickness_lineEdit.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Slit thickness [mm], (<span style=\" font-style:italic;\">d</span>)</p></body></html>"
            ))
        self.label_28.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Slit thickness [mm], (<span style=\" font-style:italic;\">d</span>)</p></body></html>"
            ))
        self.label_28.setText(
            _translate(
                "Form",
                "<html><head/><body><p>Width (<span style=\" font-style:italic;\">s</span>)</p></body></html>"
            ))
        self.slit_width_lineEdit.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Slit width [mm], (<span style=\" font-style:italic;\">s</span>)</p></body></html>"
            ))
        self.as_drawing.setToolTip(
            _translate(
                "Form",
                "<html><head/><body><p>Lengths in mm: <span style=\" font-style:italic;\">l, l</span><span style=\" vertical-align:sub;\">1</span>, <span style=\" font-style:italic;\">l</span><span style=\" font-style:italic; vertical-align:sub;\">2</span><span style=\" font-style:italic;\">;</span></p><p>Gap in mm: <span style=\" font-style:italic;\">g</span>;</p><p>Slit thickness in mm: <span style=\" font-style:italic;\">d</span>;</p><p>Slit width in mm: <span style=\" font-style:italic;\">s</span>.</p></body></html>"
            ))
        self.label.setText(
            _translate(
                "Form",
                "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Allison Scanner Device Schematic Layout</span></p></body></html>"
            ))
        self.device_name_lbl.setText(_translate("Form", "Device Name"))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())