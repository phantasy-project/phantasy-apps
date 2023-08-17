#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tempfile
from functools import partial
import toml
import os
import shutil

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QSpacerItem

from phantasy_ui import get_open_directory
from phantasy_ui import get_open_filename
from phantasy_ui import get_save_filename
from phantasy_ui import select_font
from phantasy_ui import delayed_exec

from .utils import COLUMN_NAMES
from .ui.ui_preferences import Ui_Dialog

from .conf import reset_app_config, init_user_config


def _read_data_in_tmp_file(data: str):
    with tempfile.NamedTemporaryFile("w", delete=False, suffix='.toml') as f1:
        f1.write(data)
    QDesktopServices.openUrl(QUrl(f1.name))
    delayed_exec(lambda: os.unlink(f1.name), 10000)

_DATA_MODE_MAP = {
    'Model/Snapshot': 'model',
    'Live/Control': 'live'
}

class PreferencesDialog(QDialog, Ui_Dialog):

    pref_changed = pyqtSignal()
    visibility_changed = pyqtSignal(int, bool)

    # font
    font_changed = pyqtSignal(QFont)

    # data uri changed
    data_uri_changed = pyqtSignal('QString')

    def __init__(self, preference_dict: dict, parent):
        super(self.__class__, self).__init__()
        self.parent = parent

        # point to original one in parent
        # all changes reflect in parent
        self.pref_dict = preference_dict

        # UI
        self.setupUi(self)
        self.setWindowTitle("Preferences")

        #
        self._post_init()

    def _post_init(self):
        # field init mode
        mode = self.pref_dict['SETTINGS']['FIELD_INIT_MODE']
        self.model_rbtn.setChecked(mode == 'model')
        self.live_rbtn.setChecked(mode == 'live')
        for o in (self.model_rbtn, self.live_rbtn):
            o.toggled.emit(o.isChecked())

        # t_wait in second
        t_wait = self.pref_dict['SETTINGS']['T_WAIT']
        self.apply_delt_dsbox.setValue(t_wait)
        self.apply_delt_dsbox.valueChanged.connect(self.on_apply_delt_changed)

        # init snapshot
        skip_none = self.pref_dict['SETTINGS']['SKIP_NONE']
        self.skip_none_chkbox.setChecked(skip_none)
        self.init_snp_btn.clicked.connect(self.parent.on_init_lattice_settings)
        self.skip_none_chkbox.toggled.connect(self.on_toggle_skip_none)

        # tolerance
        tol = self.pref_dict['SETTINGS']['TOLERANCE']
        self.tol_dsbox.setValue(tol)
        self.tol_dsbox.valueChanged.connect(self.on_tol_changed)

        # ndigits
        ndigit = self.pref_dict['SETTINGS']['PRECISION']
        self.ndigit_sbox.setValue(ndigit)
        self.ndigit_sbox.valueChanged.connect(self.on_ndigit_changed)

        # data source type
        dsrc_mode = self.pref_dict['DATA_SOURCE']['TYPE']
        self.dsrc_mode_cbb.setEnabled(False)
        self.dsrc_mode_cbb.setCurrentText(dsrc_mode)
        self.dsrc_mode_cbb.currentTextChanged.connect(self.on_dsrc_mode_changed)
        self.dsrc_mode_cbb.currentTextChanged.emit(self.dsrc_mode_cbb.currentText())

        # data source uri
        dsrc_uri = self.pref_dict['DATA_SOURCE']['URI']
        self.set_uri(dsrc_uri, dsrc_mode)

        # machine state
        msconf_path = self.pref_dict['MACH_STATE']['CONFIG_PATH']
        self.msconf_path_lineEdit.setText(msconf_path)
        msconf_daq_rate = self.pref_dict['MACH_STATE']['DAQ_RATE']
        self.msconf_rate_cbb.setCurrentText(str(msconf_daq_rate))
        msconf_daq_nshot = self.pref_dict['MACH_STATE']['DAQ_NSHOT']
        self.msconf_nshot_cbb.setCurrentText(str(msconf_daq_nshot))
        self.msconf_open_btn.clicked.connect(self.on_read_ms_config)
        self.msconf_nshot_cbb.currentTextChanged.connect(self.on_daq_nshot_changed)
        self.msconf_rate_cbb.currentTextChanged.connect(self.on_daq_rate_changed)

        # column visibility
        hidden_col_idx_list = self.pref_dict['_HIDDEN_COLUMNS_IDX']
        tv = self.parent._tv
        layout = self.col_visibility_gbox
        for idx, name in enumerate(COLUMN_NAMES):
            btn = QPushButton(name, self)
            btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            btn.setCheckable(True)
            btn.setChecked(idx in hidden_col_idx_list)
            btn.toggled.connect(partial(self.on_toggle_visibility, idx))
            i = idx // 4
            j = idx - 4 * i
            layout.addWidget(btn, i, j)

        # reset app config
        self.reset_app_config_btn.clicked.connect(self.on_reset_app_config)
        self.reset_app_config_btn.setVisible(False)

        # read app config
        self.view_app_config_btn.clicked.connect(self.on_read_app_config)
        # app config path
        self.appconf_path_lineEdit.setText(self.pref_dict['_FILEPATH'])

        # export app config (with all runtime changes through Preferences dialog)
        self.export_app_config_btn.clicked.connect(self.on_export_app_config)

        # font
        self.font_changed.connect(self.on_font_changed)
        font = self.pref_dict['_FONT']
        self.font_changed.emit(font)

    def set_uri(self, path: str, dsrc_mode: str):
        if not os.access(os.path.abspath(os.path.expanduser(path)), os.W_OK):
            return
        if dsrc_mode == 'database':
            self.dbpath_lbl.setText(path)
        else:
            self.wdir_lbl.setText(path)
        if self.pref_dict['DATA_SOURCE']['URI'] != path:
            self.pref_dict['DATA_SOURCE']['URI'] = path
            self.data_uri_changed.emit(path)

    @pyqtSlot()
    def on_reset_app_config(self):
        """Reset app config with the package distributed one.
        """
        r = QMessageBox.question(self, "Reset App Configuration File",
                "Are you sure to reset app configurations?",
                QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.No:
            return
        reset_app_config() # reset the config file to ~/.phantasy/settings_manager.toml

    @pyqtSlot()
    def on_read_app_config(self):
        """Edit app configurations if possible.
        """
        with open(self.pref_dict['_FILEPATH'], "r") as f0:
            data = f0.read()
        _read_data_in_tmp_file(data)

    @pyqtSlot()
    def on_export_app_config(self):
        """Export app configurations to a file.
        """
        filepath, ext = get_save_filename(self,
                    type_filter='Config File (*.toml);;Other Files (*.*)',
                    cdir=os.path.expanduser("~"))
        if filepath is None:
            return
        with open(filepath, "w") as fp:
            pref_dict_copy = self.pref_dict.copy()
            [pref_dict_copy.pop(k) for k in self.pref_dict.keys() if k.startswith("_")]
            toml.dump(pref_dict_copy, fp)

    @pyqtSlot()
    def on_read_ms_config(self):
        with open(self.pref_dict['MACH_STATE']['CONFIG_PATH'], "r") as f0:
            data = f0.read()
        _read_data_in_tmp_file(data)

    @pyqtSlot(bool)
    def on_toggle_visibility(self, idx, f):
        """Toggle the visibility of the *idx*-th column, if *f* is True,
        hide, otherwise show.
        """
        self.visibility_changed.emit(idx, f)
        if f: # hidden
            self.pref_dict['_HIDDEN_COLUMNS_IDX'].append(idx)
            self.pref_dict['SETTINGS']['HIDDEN_COLUMNS'].append(COLUMN_NAMES[idx])
        else: # shown
            self.pref_dict['_HIDDEN_COLUMNS_IDX'].remove(idx)
            self.pref_dict['SETTINGS']['HIDDEN_COLUMNS'].remove(COLUMN_NAMES[idx])

    @pyqtSlot(bool)
    def on_toggle_mode(self, f):
        if f:
            self.mode = _DATA_MODE_MAP[self.sender().text()]
            self.pref_dict['SETTINGS']['FIELD_INIT_MODE'] = self.mode

    @pyqtSlot(float)
    def on_tol_changed(self, tol: float):
        """Tolerance is changed.
        """
        # change tolerance via PVs.
        pass

    @pyqtSlot(int)
    def on_ndigit_changed(self, n: int):
        """Float Precision is changed.
        """
        self.pref_dict['SETTINGS']['PRECISION'] = n

    @pyqtSlot()
    def on_click_ok(self):
        self.pref_changed.emit()
        self.close()
        self.setResult(QDialog.Accepted)

    @pyqtSlot('QString')
    def on_daq_nshot_changed(self, s: str):
        """DAQ nshot is changed.
        """
        self.pref_dict['MACH_STATE']['DAQ_NSHOT'] = int(s)

    @pyqtSlot('QString')
    def on_daq_rate_changed(self, s: str):
        """DAQ rate is changed.
        """
        self.pref_dict['MACH_STATE']['DAQ_RATE'] = int(s)

    @pyqtSlot()
    def on_select_font(self):
        """Update font.
        """
        font, ok = select_font(self, self.font)
        if ok:
            self.font_changed.emit(font)

    @pyqtSlot(QFont)
    def on_font_changed(self, font):
        self.font = font
        self.font_sample_lbl.setText('{},{}pt'.format(font.family(),
                                                      font.pointSize()))
        self.font_sample_lbl.setFont(font)

    @pyqtSlot('QString')
    def on_dsrc_mode_changed(self, s):
        objs_file = (self.wdir_title_lbl, self.wdir_lbl, self.wdir_btn)
        objs_db = (self.dbpath_title_lbl, self.dbpath_lbl, self.dbpath_btn)
        [o.setVisible(s=='database') for o in objs_db]
        [o.setVisible(s!='database') for o in objs_file]

    @pyqtSlot()
    def on_choose_wdir(self):
        """Select working directory.
        """
        d = get_open_directory(self)
        self.set_uri(d, 'file')

    @pyqtSlot()
    def on_choose_dbfile(self):
        """Select the db file.
        """
        filepath, ext = get_open_filename(self, type_filter='SQLite File (*.db);;Other Files (*.*)')
        if filepath is None:
            return
        self.set_uri(filepath, 'database')

    @pyqtSlot(bool)
    def on_toggle_skip_none(self, is_skip_none: bool):
        """If skip the non-reachable device settings or not.
        """
        self.pref_dict['SETTINGS']['SKIP_NONE'] = is_skip_none

    @pyqtSlot(float)
    def on_apply_delt_changed(self, t: float):
        """Delta t in seconds for settings apply.
        """
        self.pref_dict['SETTINGS']['T_WAIT'] = t

