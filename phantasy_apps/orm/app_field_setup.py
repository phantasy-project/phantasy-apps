#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .ui.ui_field_setup import Ui_Dialog


class FieldSetDialog(QDialog, Ui_Dialog):

    def __init__(self, parent=None, fields=None, **kws):
        super(self.__class__, self).__init__()
        self.parent = parent
        self._fields = fields

        self.setupUi(self)
        self.setWindowTitle("Monitor Fields Configuration")

        self._init_fields(fields)

    @pyqtSlot()
    def on_click_ok(self):
        self.close()
        self.setResult(QDialog.Accepted)

    @pyqtSlot()
    def on_click_cancel(self):
        self.close()
        self.setResult(QDialog.Rejected)

    def _init_fields(self, fields):
        print("initial fields: ", fields)
        self.xfield_cbb.addItems(fields)
        self.yfield_cbb.addItems(fields)
        if 'X' in fields:  # BPM
            self.xfield_cbb.setCurrentText("X")
            self.yfield_cbb.setCurrentText("Y")
        else:  # PM, or others
            self.xfield_cbb.setCurrentText("XCEN")
            self.yfield_cbb.setCurrentText("YCEN")
