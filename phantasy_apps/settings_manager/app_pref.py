#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .ui.ui_preferences import Ui_Dialog

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog


class PreferencesDialog(QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__()
        self.parent = parent

        # UI
        self.setupUi(self)
        self.setWindowTitle("Preferences")

        #
        self._post_init()

    def _post_init(self):
        self.live_rbtn.setChecked(True)
        self.live_rbtn.toggled.emit(True)

    @pyqtSlot(bool)
    def on_toggle_mode(self, f):
        if f:
            self.mode = self.sender().text().lower()
