#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import partial
import os
import shutil

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QSpacerItem

from phantasy_ui import get_open_directory
from phantasy_apps.utils import find_dconf

from .utils import COLUMN_NAMES
from .ui.ui_preferences import Ui_Dialog

DEFAULT_FIELD_INIT_MODE = 'model'
DEFAULT_INIT_SETTINGS = False
DEFAULT_T_WAIT = 0.05
DEFAULT_TOLERANCE = 0.10
DEFAULT_CONFIG_SYNC_TIME_INTERVAL = 10  # second
DEFAULT_N_DIGITS = 3
DEFAULT_CONFIG_PATH = "~/.phantasy-apps/settings-manager"

DEFAULT_PREF = {
    'field_init_mode': DEFAULT_FIELD_INIT_MODE,
    'init_settings': DEFAULT_INIT_SETTINGS,
    't_wait': DEFAULT_T_WAIT,
    'tolerance': DEFAULT_TOLERANCE,
    'dt_confsync': DEFAULT_CONFIG_SYNC_TIME_INTERVAL,
    'ndigit': DEFAULT_N_DIGITS,
    'config_path': os.path.abspath(os.path.expanduser(DEFAULT_CONFIG_PATH)),
}


class PreferencesDialog(QDialog, Ui_Dialog):

    pref_changed = pyqtSignal(dict)
    visibility_changed = pyqtSignal(int, bool)

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

        # colvis
        tv = self.parent._tv
        layout = self.col_visibility_gbox
        for idx, name in enumerate(COLUMN_NAMES):
            btn = QPushButton(name, self)
            btn.setCheckable(True)
            btn.setChecked(tv.isColumnHidden(idx))
            btn.toggled.connect(partial(self.on_toggle_visibility, idx))
            i = idx // 4
            j = idx - 4 * i
            layout.addWidget(btn, i, j)
        layout.addItem(QSpacerItem(20, 20,
                       QSizePolicy.Preferred, QSizePolicy.Expanding))

        # config path
        config_path = self.pref_dict['config_path']
        self.update_config_paths(config_path)
        self.change_config_path_btn.clicked.connect(self.on_change_confpath)

        # reset config
        self.reset_config_btn.clicked.connect(self.on_reset_config)
        # purge config
        self.purge_config_btn.clicked.connect(self.on_purge_config)

    @pyqtSlot()
    def on_reset_config(self):
        """Reset config data with package distributed.
        """
        r = QMessageBox.question(self, "Reset Configuration Files",
                "Are you sure to reset all the configuration files?",
                QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.No:
            return

        default_ts_path = find_dconf("settings_manager", "tolerance.json")
        default_ms_path = find_dconf("settings_manager", "settings.json")
        default_elem_path = find_dconf("settings_manager", "elements.json")
        current_config_path = self.config_path_lineEdit.text()
        ts_path = os.path.join(current_config_path, 'tolerance.json')
        ms_path = os.path.join(current_config_path, 'settings.json')
        elem_path = os.path.join(current_config_path, 'elements.json')

        for default_path, path in zip(
                (default_ts_path, default_ms_path, default_elem_path),
                (ts_path, ms_path, elem_path)):
            shutil.copy2(default_path, path)

    @pyqtSlot()
    def on_purge_config(self):
        """Purge config data.
        """
        r = QMessageBox.question(self, "Purge Configuration Files",
                "Are you sure to clean up all the configuration files?",
                QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.No:
            return

        current_config_path = self.config_path_lineEdit.text()
        ts_path = os.path.join(current_config_path, 'tolerance.json')
        ms_path = os.path.join(current_config_path, 'settings.json')
        elem_path = os.path.join(current_config_path, 'elements.json')
        for path in (ts_path, ms_path, elem_path):
            with open(path, 'w'): pass

    def update_config_paths(self, root_config_path):
        config_path = root_config_path
        ts_confpath = os.path.join(config_path, 'tolerance.json')
        ms_confpath = os.path.join(config_path, 'settings.json')
        elem_confpath = os.path.join(config_path, 'elements.json')
        self.config_path_lineEdit.setText(config_path)
        layout = self.config_btns_hbox
        for i in reversed(range(layout.count())):
            w = layout.itemAt(i)
            try:
                w.widget().setParent(None)
            except:
                layout.removeItem(w)
        for p in (ts_confpath, ms_confpath, elem_confpath):
            btn = QPushButton(os.path.basename(p), self)
            btn.setToolTip(p)
            btn.clicked.connect(partial(self.on_open_filepath, p))
            layout.addWidget(btn)
        layout.addItem(QSpacerItem(20, 20,
                       QSizePolicy.Expanding, QSizePolicy.Preferred))

    @pyqtSlot()
    def on_open_filepath(self, path):
        QDesktopServices.openUrl(QUrl(path))

    @pyqtSlot()
    def on_change_confpath(self):
        d = get_open_directory(self)
        if not os.access(d, os.W_OK):
            return
        self.update_config_paths(d)

    @pyqtSlot(bool)
    def on_toggle_visibility(self, idx, f):
        """Toggle the visibility of the *idx*-th column, if *f* is True,
        hide, otherwise show.
        """
        self.visibility_changed.emit(idx, f)

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
                'init_settings': self.init_settings_chkbox.isChecked(),
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
