#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .ui.ui_preferences import Ui_Dialog

DEFAULT_FIELD_INIT_MODE = 'model'
DEFAULT_INIT_SETTINGS = False
DEFAULT_T_WAIT = 0.05
DEFAULT_TOLERANCE = 0.10
DEFAULT_CONFIG_SYNC_TIME_INTERVAL = 10  # second
DEFAULT_N_DIGITS = 3

DEFAULT_PREF = {
    'field_init_mode': DEFAULT_FIELD_INIT_MODE,
    'init_settings': DEFAULT_INIT_SETTINGS,
    't_wait': DEFAULT_T_WAIT,
    'tolerance': DEFAULT_TOLERANCE,
    'dt_confsync': DEFAULT_CONFIG_SYNC_TIME_INTERVAL,
    'ndigit': DEFAULT_N_DIGITS,
}


class PreferencesDialog(QDialog, Ui_Dialog):
    pref_changed = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(self.__class__, self).__init__()
        self.parent = parent
        self.pref_dict = DEFAULT_PREF

        # UI
        self.setupUi(self)
        self.setWindowTitle("Preferences")

        #
        self._post_init()

    def _post_init(self):
        # field init mode
        mode = self.pref_dict['field_init_mode']
        self.model_rbtn.setChecked(mode == 'model')
        self.live_rbtn.setChecked(mode == 'live')
        for o in (self.model_rbtn, self.live_rbtn):
            o.toggled.emit(o.isChecked())

        # t_wait in second
        t_wait = self.pref_dict['t_wait']
        self.apply_delt_dsbox.setValue(t_wait)

        # init_settings bool
        init_settings = self.pref_dict['init_settings']
        self.init_settings_chkbox.setChecked(init_settings)

        # tolerance
        tol = self.pref_dict['tolerance']
        self.tol_dsbox.setValue(tol)

        # confsync dt
        dt_confsync = self.pref_dict['dt_confsync']
        self.dt_confsync_dsbox.setValue(dt_confsync)

        # ndigits
        ndigit = self.pref_dict['ndigit']
        self.ndigit_sbox.setValue(ndigit)

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
                't_wait': self.apply_delt_dsbox.value(),
                'init_settings': self.init_settings,
                'tolerance': self.tol_dsbox.value(),
                'dt_confsync': self.dt_confsync_dsbox.value(),
                'ndigit': self.ndigit_sbox.value(),
                }

    @pyqtSlot(bool)
    def on_init_settings(self, f):
        """If toggled, initialize settings view with the whole loaded
        lattice, otherwise the user should add elements into view.
        """
        self.init_settings = f
