#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget

from .device import Device
from .ui.ui_layout import Ui_Form


class LayoutForm(QWidget, Ui_Form):

    def __init__(self, ems: Device, parent=None, **kws):
        super(self.__class__, self).__init__()
        self.parent = parent

        self.setupUi(self)
        self.setWindowTitle("Device Schematic Layout")

        self._post_init(ems)

    def _post_init(self, ems):
        self.device_name_lbl.setText(ems.name)
        self.length_lineEdit.setText(str(ems.length))
        self.length1_lineEdit.setText(str(ems.length1))
        self.length2_lineEdit.setText(str(ems.length2))
        self.gap_lineEdit.setText(str(ems.gap))
        self.slit_width_lineEdit.setText(str(ems.slit_width))
        self.slit_thickness_lineEdit.setText(str(ems.slit_thickness))

#    def keyPressEvent(self, e):
#        if e.key() == Qt.Key_Escape:
#            self.close()
#        else:
#            QDialog.keyPressEvent(self, e)
