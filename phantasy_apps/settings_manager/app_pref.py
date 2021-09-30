#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import partial
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
from phantasy_ui import select_font

from .utils import COLUMN_NAMES
from .utils import reset_config
from .ui.ui_preferences import Ui_Dialog

from .conf import APP_CONF, APP_CONF_PATH
from .conf import N_SNP_MAX, NPROC, MS_CONF_PATH, MS_ENABLED
from .conf import DATA_SOURCE_MODE, DB_ENGINE, DATA_URI
from .conf import reset_app_config


class PreferencesDialog(QDialog, Ui_Dialog):

    pref_changed = pyqtSignal(dict)
    visibility_changed = pyqtSignal(int, bool)

    # config, ts, ms, elem pv
    config_changed = pyqtSignal()

    # font
    font_changed = pyqtSignal(QFont)

    # bool
    init_settings_changed = pyqtSignal(bool)

    # data uri changed
    data_uri_changed = pyqtSignal('QString')

    def __init__(self, parent=None, preference_dict=None):
        super(self.__class__, self).__init__()
        self.parent = parent

        self.pref_dict = APP_CONF if preference_dict is None else preference_dict

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

        # init_settings bool
        init_settings = self.pref_dict['SETTINGS']['INIT_SETTINGS']
        self.init_settings_chkbox.setChecked(init_settings)

        # tolerance
        tol = self.pref_dict['SETTINGS']['TOLERANCE']
        self.tol_dsbox.setValue(tol)

        # ndigits
        ndigit = self.pref_dict['SETTINGS']['PRECISION']
        self.ndigit_sbox.setValue(ndigit)

        # data source type
        dsrc_mode = self.pref_dict['DATA_SOURCE']['TYPE']
        self.dsrc_mode_cbb.setCurrentText(dsrc_mode)
        self.dsrc_mode_cbb.currentTextChanged.connect(self.on_dsrc_mode_changed)
        self.dsrc_mode_cbb.currentTextChanged.emit(self.dsrc_mode_cbb.currentText())

        # data source uri
        dsrc_uri = self.pref_dict['DATA_SOURCE']['URI']
        self.set_uri(dsrc_uri, dsrc_mode)

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

        # config path
        config_path = self.pref_dict['SETTINGS']['SUPPORT_CONFIG_PATH']
        self.update_config_paths(config_path)
        self.change_config_path_btn.clicked.connect(self.on_change_confpath)

        # reset support config
        self.reset_config_btn.clicked.connect(self.on_reset_config)
        # purge support config
        self.purge_config_btn.clicked.connect(self.on_purge_config)

        # reset app config
        self.reset_app_config_btn.clicked.connect(self.on_reset_app_config)
        # edit app config
        self.edit_app_config_btn.clicked.connect(self.on_edit_app_config)

        # font
        self.font_changed.connect(self.on_font_changed)
        font = self.pref_dict['font']
        self.font_changed.emit(font)

    def set_uri(self, path, dsrc_mode):
        if not os.access(os.path.abspath(os.path.expanduser(path)), os.W_OK):
            return
        if dsrc_mode == 'DB':
            self.dbpath_lineEdit.setText(path)
        else:
            self.wdir_lineEdit.setText(path)
        self.data_uri_changed.emit(path)

    @pyqtSlot()
    def on_reset_app_config(self):
        """Reset app config with package distributed one.
        """
        r = QMessageBox.question(self, "Reset App Configuration File",
                "Are you sure to reset app configurations?",
                QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.No:
            return
        reset_app_config()

    @pyqtSlot()
    def on_edit_app_config(self):
        """Edit app configurations if possible.
        """
        QDesktopServices.openUrl(QUrl(APP_CONF_PATH))

    @pyqtSlot()
    def on_reset_config(self):
        """Reset config data with package distributed ones.
        """
        r = QMessageBox.question(self, "Reset Configuration Files",
                "Are you sure to reset all the configuration files?",
                QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.No:
            return

        current_config_path = self.config_path_lineEdit.text()
        reset_config(current_config_path)

        self.config_changed.emit()

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

        self.config_changed.emit()

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
        return {
                'SETTINGS':
                    {'FIELD_INIT_MODE': self.mode,
                     'T_WAIT': self.apply_delt_dsbox.value(),
                     'INIT_SETTINGS': self.init_settings_chkbox.isChecked(),
                     'TOLERANCE': self.tol_dsbox.value(),
                     'PRECISION': self.ndigit_sbox.value(),
                     }
                }

    @pyqtSlot(bool)
    def on_init_settings(self, f):
        """If toggled, initialize settings view with the whole loaded
        lattice, otherwise the user should add elements into view.
        """
        self.init_settings = f
        self.init_settings_changed.emit(f)

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
        objs_file = (self.wdir_lbl, self.wdir_lineEdit, self.wdir_btn)
        objs_db = (self.dbpath_lbl, self.dbpath_lineEdit, self.dbpath_btn)
        [o.setVisible(s=='DB') for o in objs_db]
        [o.setVisible(s!='DB') for o in objs_file]

    @pyqtSlot()
    def on_choose_wdir(self):
        """Select working directory.
        """
        d = get_open_directory(self)
        self.set_uri(d, 'FILE')

    @pyqtSlot()
    def on_choose_dbfile(self):
        """Select the db file.
        """
        filepath, ext = get_open_filename(self, type_filter='SQLite File (*.db);;Other Files (*.*)')
        if filepath is None:
            return
        self.set_uri(filepath, 'DB')
