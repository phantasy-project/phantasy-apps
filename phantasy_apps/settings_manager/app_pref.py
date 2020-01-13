#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .ui.ui_preferences import Ui_Dialog

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog


class PreferencesDialog(QDialog, Ui_Dialog):

    pref_changed = pyqtSignal(dict)

    def __init__(self, pref_dict, parent=None):
        super(self.__class__, self).__init__()
        self.parent = parent
        self.pref_dict = pref_dict

        # UI
        self.setupUi(self)
        self.setWindowTitle("Preferences")

        #
        self._post_init()

    def _post_init(self):
        # field init mode
        mode = self.pref_dict['field_init_mode']
        self.model_rbtn.setChecked(mode=='model')
        self.live_rbtn.setChecked(mode=='live')
        for o in (self.model_rbtn, self.live_rbtn):
            o.toggled.emit(o.isChecked())

        # t_wait in second
        t_wait = self.pref_dict['t_wait']
        self.apply_delt_dsbox.setValue(t_wait)

    @pyqtSlot(bool)
    def on_toggle_mode(self, f):
        if f:
            self.mode = self.sender().text().lower()

    @pyqtSlot()
    def on_click_ok(self):
        self.pref_changed.emit(self.get_config())
        self.close()
        self.setResult(QDialog.Accepted)

    def get_config(self):
        return {'field_init_mode': self.mode,
                't_wait': self.apply_delt_dsbox.value(),}

