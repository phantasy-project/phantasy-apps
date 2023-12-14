#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .ui.ui_settings_view import Ui_Dialog
from .utils import SettingsModel


class SettingsView(QDialog, Ui_Dialog):

    def __init__(self, data, parent=None, **kws):
        super(self.__class__, self).__init__()
        self.parent = parent
        self.data = data

        self.setupUi(self)
        self.setWindowTitle("Saved Scan Settings")
        self.v = self.treeView

        model = SettingsModel(self.v, self.data, **kws)
        model.view_size.connect(self.on_resize)
        model.set_model()

    def on_resize(self, w: int, h: int):
        rect = self.geometry()
        w0, h0 = rect.width(), rect.height()
        if h0 < h:
            h = h0
        else:
            h += 150
        self.resize(int(w * 1.05), int(h * 1.05))

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        else:
            QDialog.keyPressEvent(self, e)
