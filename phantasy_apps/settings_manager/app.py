#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import fnmatch
import json
import os
import pathlib
import re
import numpy as np
import pandas as pd
import tempfile
import time
import toml
from collections import OrderedDict
from datetime import datetime
from epics import caget, caput, ca, get_pv
from functools import partial
from getpass import getuser
from subprocess import Popen

from PyQt5.QtCore import (QDate, QEventLoop, QPoint, QRect, QSize, QTimer,
                          QUrl, QVariant, Qt, pyqtSignal, pyqtSlot)

from PyQt5.QtGui import (QColor, QFont, QFontDatabase, QFontMetrics, QIcon,
                         QKeySequence, QPainter, QPixmap, QGuiApplication,
                         QDesktopServices, QDoubleValidator)
from PyQt5.QtWidgets import (QCompleter, QCheckBox, QDialog, QLabel,
                             QMessageBox, QMenu, QAction, QWidgetAction,
                             QToolButton, QPushButton, QSizePolicy, QShortcut,
                             QWidget, QProgressBar, QHBoxLayout, QLineEdit,
                             QLabel)

from phantasy import (build_element, CaField, Settings)
from phantasy_ui import (BaseAppForm, delayed_exec, get_open_filename,
                         get_save_filename, printlog, milli_sleep)
from phantasy_ui.widgets import (is_item_checked, BeamSpeciesDisplayWidget,
                                 DataAcquisitionThread as DAQT,
                                 ElementSelectDialog, FlowLayout,
                                 LatticeWidget, ProbeWidget, DataTrendWidget)
from phantasy_apps.msviz.mach_state import (get_meta_conf_dict,
                                            merge_mach_conf, _build_dataframe,
                                            _daq_func)
from archappl.client import (ArchiverDataClient, ArchiverMgmtClient)

from .app_date_range import DateRangeDialog
from .app_import import ImportSNPDialog
from .app_pref import PreferencesDialog
from .app_bpmviz import BPMVizWidget
from .app_postsnp import PostSnapshotDialog
from .data import CSV_HEADER
from .data import DEFAULT_DATA_FMT
from .data import ElementPVConfig
from .data import SnapshotData
from .data import get_settings_data
from .data import make_physics_settings
from .data import read_data
from .db_utils import insert_update_data
from .db_utils import delete_data
from .ui.ui_app import Ui_MainWindow
from .ui.ui_query_tips import Ui_Form as QueryTipsForm
from .conf import read_app_config
from .utils import FMT
from .utils import ELEMT_PX_MAP
from .utils import TBTN_STY_REGULAR
from .utils import TBTN_STY_GOLDEN
from .utils import SettingsModel
from .utils import pack_settings
from .utils import str2float
from .utils import get_ratio_as_string
from .utils import VALID_FILTER_KEYS
from .utils import VALID_FILTER_KEYS_NUM
from .utils import SnapshotDataModel
from .data import DEFAULT_MACHINE, DEFAULT_SEGMENT
from .utils import ELEM_WRITE_PERM
from .utils import NUM_LENGTH
from .utils import BG_COLOR_GOLDEN_NO
from .utils import CHP_STS_TUPLE
from .utils import TGT_STS_TUPLE
from .utils import TAG_BTN_STY
# from .utils import get_pwr_sts
from .utils import PWR_STS_U_ROLE, STS_PX_MAP
from .contrib.db.db_utils import ensure_connect_db
from .config import sym2z
from .utils import SetLogMessager
from .utils import EffSetLogMsgContainer

# scaling eligible field names:
SCALABLE_FIELD_NAMES = ('I', 'V', 'AMP', 'AMP1', 'AMP2', 'AMP3', 'I_TC')
# scaling op
SCALE_OP_MAP = ('x', '+')  # simple form for {0: 'x', 1: '+'}
#
SUPPORT_FTYPES = ("xlsx", "csv", "h5")

# sb pos of stripper (carbon) [m]
STRIPPER_POS = 224.903684519998

PX_SIZE = 24
ION_ICON_SIZE = 48
DATA_SRC_MAP = {'model': 'model', 'live': 'control'}
IDX_RATE_MAP = {
    0: 1.0,  # 1 s
    1: 0.5,  # 2 s
    2: 0.2,  # 5 s
    3: 0.1,  # 10 s
    4: 0.05,  # 20 s
    5: 0.02,  # 50 s
}
FILTER_TT = """\
Filter strings 'keyword=pattern', multiple conditions could be linked with 'and', support 'in'
test. More details please click the right help button."""
TS_FMT = "%Y-%m-%dT%H:%M:%S.%f"
_, LOG_FILE = tempfile.mkstemp(datetime.now().strftime(TS_FMT),
                               "settings_manager_setlog_", "/tmp")

NOW_DT = datetime.now()
NOW_YEAR = NOW_DT.year
NOW_MONTH = NOW_DT.month
NOW_DAY = NOW_DT.day
from .conf import N_SNP_MAX

# Alarm types to control, disable/enable.
ALM_TYPE_MAP = { # [read, tune]
    'All': [True, True],
    'Read': [True, False],
    'Tune': [False, True],
}

ISRC_NAME_MAP = {'ISRC1': 'Artemis', 'ISRC2': 'HP-ECR'}

# SNP PVs
SNP_NAME_PV = "PHY:SM_SNP_LAST_NAME"
SNP_NOTE_PV = "PHY:SM_SNP_LAST_NOTE"
SNP_ION_PV = "PHY:SM_SNP_LAST_ION"
SNP_AUTHOR_PV = "PHY:SM_SNP_LAST_AUTHOR"
SNP_PUBLISHER_PV = "PHY:SM_SNP_LAST_PUBLISHER"

_CHANGELOG_FILE = os.path.join(os.path.dirname(__file__), 'CHANGELOG.pdf')
_USERGUIDE_FILE = os.path.join(os.path.dirname(__file__),
                               'docs/SettingsManager_UserGuide.pdf')

# refresh period
REFRESH_INTERVAL_MAP = {
    'Slow': 30000,  # milliseconds
    'Normal': 10000,
    'Fast': 5000,
}

DB_REFRESH_INTERVAL_MAP = {
    0: 15 * 60 * 1000,  # fast, every 15 mins
    1: 30 * 60 * 1000,  # normal, every 30 mins
    2: 60 * 60 * 1000,  # slow, every 1 hour
    3: 7 * 24 * 60 * 60 * 1000,  # slowest, every 1 week
}

# MAX lines of setting logs
MAX_LOG_LINES = 3000

REVERT_TT_REASON = """<html><head/><body><p>Revert <span style=" color:#0055ff;">{n}</span> device settings (<span style=" color:#ff007f;">{op} {ov}</span>) changed at <span style=" color:#0055ff;">{ts} </span>for <span style=" color:#aa00ff;">{reason}</span>. Original snapshot: {snapshot}.</p></body></html>"""
REVERT_TT_NO_REASON = """<html><head/><body><p>Revert <span style=" color:#0055ff;">{n}</span> device settings (<span style=" color:#ff007f;">{op} {ov}</span>) changed at <span style=" color:#0055ff;">{ts}</span>. Original snapshot: {snapshot}.</p></body></html>"""

MATCH_STY = """
QFrame#orig_template_info_frame {
    border: 1px solid #28A745;
}"""
NOT_MATCH_STY = """
QFrame#orig_template_info_frame {
    border: 1px solid #DC3545;
}"""


class SettingsManagerWindow(BaseAppForm, Ui_MainWindow):
    # settings view filter button group status (or) changed --> update
    filter_btn_group_status_changed = pyqtSignal()

    # signal: settings loaded, emit flat_settings and settings.
    settingsLoaded = pyqtSignal(QVariant, QVariant)

    # refresh rate
    rate_changed = pyqtSignal(int)

    # lattice is loaded
    lattice_loaded = pyqtSignal(QVariant)

    # the list of element list is changed --> update settings model
    element_list_changed = pyqtSignal()

    # ndigit
    ndigit_changed = pyqtSignal(int)

    # font
    font_changed = pyqtSignal(QFont)

    # bool
    init_settings_changed = pyqtSignal(bool)

    # snp saved, snpdata name, filepath
    snp_saved = pyqtSignal('QString', 'QString')

    # snp loaded, snpdata
    snp_loaded = pyqtSignal(SnapshotData)

    # snp filter (snp dock)
    snp_filters_updated = pyqtSignal()

    # refresh database
    db_refresh = pyqtSignal()

    # pull data from database
    db_pull = pyqtSignal()

    # total number of checked items (not limited to current page) changed by amount of input int
    total_number_checked_items_changed = pyqtSignal(int)

    # last refresh: data is refreshed
    last_refreshed = pyqtSignal()

    # eligible (True/False) to issue apply command
    sigApplyReady = pyqtSignal(bool)

    # set log text color
    sigSetLogColorChanged = pyqtSignal(QColor)
    sigSetLogColorReset = pyqtSignal()
    sigSetLogColorSkip = pyqtSignal()
    sigSetLogColorSet = pyqtSignal()

    # name of the originated template of the loaded snapshot is changed
    sigOrigTemplateChanged = pyqtSignal('QString')

    def __init__(self, version: str, config_file: str = None, **kws):
        # kws: title, splash
        super(SettingsManagerWindow, self).__init__()

        # splash screen
        self._splash_w = kws.get('splash', None)
        self._task_list = [
        ]  # a list of tasks (also msg str) to be done before show

        # app version
        self._version = version

        # set app properties
        self.setAppTitle("Settings Manager")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Settings Manager</h4>
            <p>This app is created to manage the physics optics settings for
            the accelerator system, current version is {}.
            </p>
            <p>Copyright (C) 2019 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)
        self.postInitUi()

        # window title/icon
        self.setWindowTitle(kws.get("title", "Settings Manager"))

        # read and init app config
        self.init_config(config_file)

        # resizing
        self.resize(self._ui_width, self._ui_height)

        # preload snapshot templates (splashing)
        self.__preload_templates(self.pref_dict.get('SNAPSHOT_TEMPLATES'))

        # config for machine state data capture
        self._mach_state_config = self.get_ms_config()

        self.__init_dsrc(self.dsrc_dict)

        # post init ui
        self.__post_init_ui()

        # preload lattice (splashing)
        self.__preload_lattice(self.pref_dict['LATTICE']['DEFAULT_MACHINE'],
                               self.pref_dict['LATTICE']['DEFAULT_SEGMENT'])

        # init AA
        self.__init_aa()

        # init CA (not in use)
        # self.__init_ca()

        # init data files, e.g. JSON files of refst, tol, almact PVs
        # {} or 'refset', 'tol', 'almact' keys of values
        self._pv_map = self.__init_datafiles()

        # init filter string buttons
        self.__init_filter_str_ctls()


    def __init_filter_str_ctls(self):
        """Create convenient buttons for load filter strings.
        """
        conf = self.pref_dict
        if conf.get('FILTER_BUTTONS', None) is not None:
            for _, v in conf['FILTER_BUTTONS'].items():
                filepath = v.get('FILEPATH', None)
                if filepath is None:
                    continue
                if not os.path.isfile(filepath):
                    continue
                _conf = toml.load(filepath)
                btn_tt = _conf['filter_config'].get('description')
                btn_name = _conf['filter_config'].get('name')
                btn = QToolButton()
                btn.setIcon(QIcon(QPixmap(":/sm-icons/filter.png")))
                btn.setIconSize(QSize(30, 30))
                btn.setText(btn_name)
                btn.setToolTip(btn_tt)
                btn.setAutoRaise(True)
                btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
                btn.clicked.connect(
                    partial(self.load_filter_from_file, filepath))
                self.filters_hbox.addWidget(btn)

        if conf.get('FILTER_GROUPS', None) is not None:
            for _, v in conf['FILTER_GROUPS'].items():
                grp_name = v.get('NAME', None)
                if grp_name is None:
                    continue
                grp_tt = v.get('DESC', grp_name)
                grp_dir = v.get('DIRPATH')
                btn = QToolButton()
                menu = QMenu()
                for f in pathlib.Path(grp_dir).glob("**/*.flt"):
                    act = QAction(QIcon(QPixmap(":/sm-icons/filter.png")),
                                  f.stem, menu)
                    act.triggered.connect(
                        partial(self.load_filter_from_file, f.as_posix()))
                    menu.addAction(act)
                btn.setMenu(menu)
                # btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
                btn.setToolTip(grp_tt)
                btn.setText(grp_name)
                btn.setPopupMode(QToolButton.MenuButtonPopup)
                btn.setIcon(QIcon(QPixmap(":/sm-icons/rocket.png")))
                btn.setIconSize(QSize(30, 30))
                btn.setAutoRaise(True)
                self.filters_hbox.addWidget(btn)

    def load_filter_from_file(self, path):
        """Set settings filter with the .flt config from *path*.
        """
        conf = toml.load(path)
        text = conf['filter_config'].get('string', '')
        wildcard_flag = conf['filter_config'].get('strict_wildcard', False)
        check_all_flag = conf['filter_config'].get('check_all_items', False)
        #
        self.filter_btn.setChecked(True)
        self.filter_lineEdit.setText(text)
        self.strict_wildcard_chkbox.setChecked(wildcard_flag)
        #
        self.filter_lineEdit.editingFinished.emit()
        if check_all_flag and self._tv.model() is not None:
            delayed_exec(lambda: self.select_all_btn.clicked.emit(), 1000)

    def __init_aa(self):
        # initialize config for Archiver Appliance
        self._aa_data_client = None
        self._aa_mgmt_client = None
        # Initialize archiver appliance client
        aa_conf = self.pref_dict.get('ARCHIVER_APPLIANCE', None)
        if aa_conf is None:
            return
        data_client_conf = aa_conf.get('DATA_CLIENT', None)
        if data_client_conf is not None:
            self._aa_data_client = ArchiverDataClient(
                data_client_conf.get('URL'))
        mgmt_client_conf = aa_conf.get('MGMT_CLIENT', None)
        if mgmt_client_conf is not None:
            self._aa_mgmt_client = ArchiverMgmtClient(
                mgmt_client_conf.get('URL'))

    def __init_ca(self):
        ca_conf = self.pref_dict.get('EPICS', None)
        if ca_conf is None:
            return
        for k, v in ca_conf.items():
            if isinstance(v, list):
                v = ' '.join(v)
            os.environ[f'EPICS_{k}'] = v
        _reset_ca()

    def __init_datafiles(self):
        # probably, should migrate to phantasy-machines sometime in the future.
        dfile_conf = self.pref_dict.get('DATA', None)
        if dfile_conf is None:
            return {}

        # REF ST PV MAP
        fpath_refset = dfile_conf.get('REFST_PVFILE', None)
        if fpath_refset is None:
            ref_st_pv_map = {}
        else:
            with open(fpath_refset, "r") as fp:
                ref_st_pv_map = {
                    k: get_pv(v)
                    for k, v in json.load(fp).items()
                }

        # TOL PV MAP
        fpath_tol = dfile_conf.get('TOL_PVFILE', None)
        if fpath_tol is None:
            tol_pv_map = {}
        else:
            with open(fpath_tol, "r") as fp:
                tol_pv_map = {k: get_pv(v) for k, v in json.load(fp).items()}

        # Device alarm switch PV MAP
        fpath_almact = dfile_conf.get('ALMACT_PVFILE', None)
        if fpath_almact is None:
            alm_act_pv_map = {}
        else:
            with open(fpath_almact, "r") as fp:
                alm_act_pv_map = {
                    k: (get_pv(v[0]), get_pv(v[1]))
                    for k, v in json.load(fp).items()
                }

        #
        return {
            'refset': ref_st_pv_map,
            'tol': tol_pv_map,
            'almact': alm_act_pv_map
        }

    def init_config(self, config_file: str = None):
        #
        # read app configurations from config_file
        # - initialize preference dialog
        # - maintain the dict of config through preference dialog
        #
        # preferences
        self.pref_dict = read_app_config(config_file)

        # UI
        self._ui_width = self.pref_dict['UI'].get('WIDTH', 1920)
        self._ui_height = self.pref_dict['UI'].get('HEIGHT', 1440)

        self.field_init_mode = self.pref_dict['SETTINGS']['FIELD_INIT_MODE']
        self.t_wait = self.pref_dict['SETTINGS']['T_WAIT']
        self.init_settings = self.pref_dict['SETTINGS']['INIT_SETTINGS']
        self.ndigit = self.pref_dict['SETTINGS']['PRECISION']

        self.fmt = '{{0:>{0}.{1}f}}'.format(NUM_LENGTH, self.ndigit)
        # for field NMR, HALL probe
        self.fmt_nmr = '{{0:>{0}.{1}f}}'.format(NUM_LENGTH, 5)

        # data source
        self.dsrc_mode = self.pref_dict['DATA_SOURCE']['TYPE']
        self.db_engine = self.pref_dict['DATA_SOURCE']['DB_ENGINE']
        self.data_uri = self.pref_dict['DATA_SOURCE']['URI']
        self.dsrc_dict = {
            'mode': self.dsrc_mode,
            'engine': self.db_engine,
            'uri': self.data_uri
        }
        #

        # font
        self.default_font, self.default_font_size = self.get_default_font_config(
        )
        self.font = self.default_font
        self.pref_dict['font'] = self.font
        self.font_changed.connect(self.on_font_changed)

        self.ndigit_changed.connect(self.on_ndigit_changed)
        # init settings boolean
        self.init_settings_changed.connect(
            self.init_settings_chkbox.setChecked)

    def __preload_templates(self, temp_conf: dict):
        # preload snapshot templates.
        if temp_conf is None:
            printlog("No snapshot templates to load!")
            return

        def _load_single(t: tuple):
            _itemp_name, _itemp_conf = t
            _isnp_data = get_snapshotdata(_itemp_conf['DB_ENTRY'],
                                          self.data_uri)
            if _isnp_data is not None:
                _isnp_data.extract_blob()
            return (_itemp_conf['NAME'], _itemp_conf['DB_TAGS'], _isnp_data)

        def _load_ready(res):
            # a list of snapshot templates, with expanded tabular data
            self.snp_template_list = res

        def _load_started():
            self._task_list.append('Loading the snapshot templates...')
            self._splash_msg_undone()

        def _load_done():
            task_name = "Loading the snapshot templates..."
            self._task_list.remove(task_name)
            self._splash_msg("Loaded the snapshot templates.")
            self._splash_msg_undone()

        self._snp_temp_loader = DAQT(daq_func=_load_single,
                                     daq_seq=temp_conf.items())
        self._snp_temp_loader.daqStarted.connect(_load_started)
        self._snp_temp_loader.resultsReady.connect(_load_ready)
        self._snp_temp_loader.daqFinished.connect(_load_done)
        self._snp_temp_loader.start()

    def get_originated_template(self):
        """Get the name of snapshot template from the currently loaded one.

        The result could be:
        - The name of a template: loaded one exactly matches that template;
        - The name of a template (subset): the loaded one is a subset of that template;
        - None: the loaded one is not originated from any templates.

        Returns
        -------
        r : tuple
            A tuple of the original snapshot template, name, tag list,
            and the loaded SnapshotData (for On Loaded option of 'Take Snapshot')
        """
        loaded_settings_name_set = set(
            self._current_snpdata.data.Name.unique())
        for _tmp_name, _tmp_tags, _tmp_snp_data in self.snp_template_list:
            _name_set = set(_tmp_snp_data.data.Name.unique())
            if _name_set == loaded_settings_name_set:
                return _tmp_name, _tmp_tags, self._current_snpdata
            elif loaded_settings_name_set.issubset(_name_set):
                return _tmp_name + " (subset)", _tmp_tags, self._current_snpdata
        return None, None, self._current_snpdata

    @pyqtSlot()
    def on_auto_column_width(self):
        # auto adjust column width
        m = self._tv.model()
        if m is None:
            return
        m.m_src.fit_view()

    @pyqtSlot(QFont)
    def on_font_changed(self, font):
        """Update font config for settings view.
        """
        self.font = font
        self.pref_dict['font'] = font
        m = self._tv.model()
        if m is None:
            return
        src_m = m.sourceModel()
        src_m.style_view(font=font)
        src_m.fit_view()

    def get_default_font_config(self):
        """Initial font config.
        """
        default_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        default_font_size = default_font.pointSize()
        return default_font, default_font_size

    @pyqtSlot(QVariant)
    def on_lattice_changed(self, o):
        # Lattice is loaded.
        # Update status of snp load tool
        # Update lattice info labels
        # Reset lattice
        #   Show the current element settings
        #
        if o is None:
            return

        if (o.last_machine_name == self._last_machine_name) and \
                (o.last_lattice_name == self._last_lattice_name):
            return

        # update lattice with the new one
        self._mp = o
        self._last_machine_name = self._mp.last_machine_name
        self._last_lattice_name = self._mp.last_lattice_name
        # reset self._lat
        self._lat = o.combined_lattice()
        self.lattice_loaded.emit(o)

        # show element settings
        if self.init_settings:  # in Preferences
            # if init settings, show settings to the view.
            self._elem_list = self._lat[:]
            self.element_list_changed.emit()
        else:
            # WIP
            # otherwise, user needs to 'Add Devices' to the view.
            # self._lat.reset_settings()
            # self._lat._elements = []
            pass

    def show_init_settings_info(self):
        if not self._post_info:
            return
        if not self.init_settings:
            QMessageBox.information(
                self, "Loaded Lattice",
                '<html><head/><body><p>Lattice is loaded, add device settings '
                'via <span style=" font-style:italic;">Add Devices</span> or '
                '<span style=" font-style:italic;">Load Settings </span>tools,'
                ' or check <span style=" font-style:italic;">Initialize with '
                'loaded lattice</span> in the right bottom window area to '
                'list all the devices.</p></body></html>', QMessageBox.Ok)

    def _enable_widgets(self, enabled):
        for w in (self.lv_lbl, self.lv_mach_lbl, self.lv_segm_lbl,
                  self.lv_view_btn, self.reload_lattice_btn):
            w.setEnabled(enabled)

    def update_lattice_info_lbls(self, mach, segm):
        self._enable_widgets(True)
        self.lv_mach_lbl.setText(mach)
        self.lv_segm_lbl.setText(segm)

    @pyqtSlot()
    def on_reload_lattice(self):
        """Reload lattice.
        """
        self.actionLoad_Lattice.triggered.emit()
        self._lattice_load_window.load_btn.clicked.emit()

    @pyqtSlot(QVariant, QVariant)
    def on_settings_loaded(self, flat_settings, settings):
        """Settings are loaded.
        """
        printlog("Loading settings...")
        self.__flat_settings = flat_settings
        self.__settings = settings
        self.__on_show_settings()

    def __on_show_settings(self):
        # visualize settings
        printlog("Setting data model...")
        model = SettingsModel(
            self._tv,
            self.__flat_settings,
            device_states=self._last_sts_dict,
            ndigit=self.ndigit,
            font=self.font,
            auto_fmt=self.auto_ndigit_chkbox.isChecked(),
            pv_map=self._pv_map,
        )
        model.settings_sts.connect(self.on_settings_sts)
        model.item_deletion_updated[list].connect(self.on_delete_items)
        model.checked_items_inc_dec_updated.connect(
            self.total_number_checked_items_changed)
        model.set_model()
        self._fld_obj = model._fld_obj
        self._fld_it = model._fld_it

        self.obj_it_tuple = tuple(zip(self._fld_obj, self._fld_it))

        # reset checked #
        self.n_all_checked_items_lbl.setText('0')

        #
        self.toggle_ftype()
        #
        printlog("Updating data values...")
        self.update_ctrl_btn.toggled.emit(self.update_ctrl_btn.isChecked())
        self.single_update_btn.clicked.emit()
        loop = QEventLoop()
        self.one_updater.finished.connect(self.on_auto_column_width)
        self.one_updater.finished.connect(loop.exit)
        loop.exec_()

    @pyqtSlot(int, int)
    def on_settings_sts(self, i, j):
        for s, v in zip(('elem', 'field'), (i, j)):
            o = getattr(self, 'total_{}_number_lbl'.format(s))
            o.setText(str(v))

    @pyqtSlot()
    def onResetMachState(self):
        """Reset captured machine state through CaptureMachineState tool.
        For view differences.
        """
        self._machstate = None

    def __post_init_ui(self):
        # the button for deleting rows from settings view
        self.delete_btn.setVisible(getuser() in ('zhangt', 'tong'))

        # hide change reason inputbox right of Apply button by default
        self.show_change_reason_input_chkbox.toggled.emit(False)

        # update toolbar
        self.__update_toolbar()

        # initial updater
        self.one_updater = None

        # apply ready?
        self.sigApplyReady.connect(self.apply_btn.setEnabled)
        # hide loaded snp info
        self.set_post_snp_info_visible(False)
        # hide last data refreshed info
        self.set_last_data_refreshed_info_visible(False)
        # data is refreshed
        self.last_refreshed.connect(self.on_data_refresh_done)

        # disable the ndigit sbox on the main UI
        self.ndigit_sbox.setEnabled(False)
        self.ndigit_sbox.setToolTip(
            "Go to 'Preferences -> Float number precision' to change the value."
        )
        # hide update_rate_cbb,
        self.update_rate_cbb.setCurrentText("20 s")  # 0.05 Hz
        self.update_rate_cbb.setVisible(False)
        # hide keep refreshing button (to be dropped)
        self.update_ctrl_btn.setVisible(False)

        # total number of checked items
        self.total_number_checked_items_changed.connect(
            self.on_nchecked_changed)

        # hide sts info
        self.show_sts_btn.setChecked(False)

        # reference set controls
        self.show_refset_ctrls_btn.toggled.connect(self.on_toggle_refset_ctrls)
        self.show_refset_ctrls_btn.setChecked(False)

        # device alarm switch controls
        self.show_alm_ctrls_btn.toggled.connect(self.on_toggle_alm_ctrls)
        self.show_alm_ctrls_btn.setChecked(False)

        # alarm type for disable/enable actions
        self._alm_type_idx_list = ALM_TYPE_MAP["All"]

        #
        self._post_info = True  # post info after loading lattice
        #
        self._tv = self.settingsView
        self._import_snp_dlg = None
        self._elem_select_dlg = None
        self._lattice_load_window = None
        self._fixnames_dlg = None
        self._date_range_dlg = None
        self._db_mgmt_dlg = None

        self._mp = None
        self._last_machine_name = None
        self._last_lattice_name = None
        self._lat = None  # loaded from latticeWidget
        self._elem_list = []  # element list for SettingsModel
        self._last_sts_dict = {}  # last device state dict

        self.__settings = Settings()
        self.__flat_settings = None

        self._eval_scaling_factor = False  # not eval sf (hit enter)

        self._eng_phy_toggle = {'ENG': True, 'PHY': False}
        self.on_lattice_changed(self._mp)

        # lattice viewer
        self._enable_widgets(False)
        self._lv = None
        self.lv_view_btn.clicked.connect(self.on_show_latinfo)

        # machine state
        self._machstate = None

        # snp dock
        self.snp_dock.closed.connect(
            lambda: self.actionSnapshots.setChecked(False))
        self.actionSnapshots.setChecked(True)

        # show lattice settings
        self.settingsLoaded.connect(self.on_settings_loaded)

        # update rate
        self.rate_changed.connect(self.on_update_rate_changed)
        self.update_rate_cbb.currentIndexChanged.emit(
            self.update_rate_cbb.currentIndex())

        # icon
        self._matched_px = QPixmap(":/sm-icons/done.png").scaled(
            32, 32, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self._not_matched_px = QPixmap(":/sm-icons/fail.png").scaled(
            32, 32, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        self.done_px = QPixmap(":/sm-icons/done.png")
        self.fail_px = QPixmap(":/sm-icons/fail.png")
        self._warning_px = QPixmap(":/sm-icons/warning.png").scaled(
            PX_SIZE, PX_SIZE)
        self._no_warning_px = QPixmap(QSize(PX_SIZE, PX_SIZE))
        self._no_warning_px.fill(QColor(*BG_COLOR_GOLDEN_NO))
        self._ok_px = QPixmap(":/sm-icons/ok.png")
        self._copy_text_icon = QIcon(QPixmap(":/sm-icons/copy_text.png"))
        self._copy_data_icon = QIcon(QPixmap(":/sm-icons/copy_data.png"))
        self._probe_icon = QIcon(QPixmap(":/sm-icons/probe.png"))
        self._trend_icon = QIcon(QPixmap(":/sm-icons/data-trend.png"))
        self._unsel_icon = QIcon(QPixmap(":/sm-icons/uncheck.png"))
        self._sel_icon = QIcon(QPixmap(":/sm-icons/check.png"))
        self._sel3_icon = QIcon(QPixmap(":/sm-icons/check3.png"))
        self._saveas_icon = QIcon(QPixmap(":/sm-icons/save.png"))
        self._read_icon = QIcon(QPixmap(":/sm-icons/readfile.png"))
        self._reveal_icon = QIcon(QPixmap(":/sm-icons/openfolder.png"))
        self._del_icon = QIcon(QPixmap(":/sm-icons/delete.png"))
        self._load_icon = QIcon(QPixmap(":/sm-icons/cast.png"))
        self._recommand_icon = QIcon(QPixmap(":/sm-icons/recommend.png"))
        # enabled/disabled alarms
        self._alm_enabled_px = QPixmap(":/sm-icons/alarm_on_green.png").scaled(
            PX_SIZE, PX_SIZE)
        self._alm_disabled_px = QPixmap(":/sm-icons/alarm_off_red.png").scaled(
            PX_SIZE, PX_SIZE)

        #
        self._turn_on_icon = QIcon(QPixmap(":/sm-icons/bolt_on.png"))
        self._turn_off_icon = QIcon(QPixmap(":/sm-icons/bolt_off.png"))
        self._power_switch_icon = QIcon(QPixmap(":/sm-icons/power_switch.png"))
        self._warning_amber_icon = QIcon(
            QPixmap(":/sm-icons/warning_amber.png"))
        self._chart_icon = QIcon(QPixmap(":/sm-icons/chart.png"))
        self._ext_app_icon = QIcon(QPixmap(":/sm-icons/rocket.png"))

        # pwr sts
        self._pwr_on_px = QPixmap(":/sm-icons/on.png")
        self._pwr_off_px = QPixmap(":/sm-icons/off.png")
        self._pwr_unknown_px = QPixmap(":/sm-icons/unknown.png")
        # blocking beam or not
        _blocking_px = QPixmap(":/sm-icons/off.png")
        _non_blocking_px = QPixmap(":/sm-icons/on.png")
        # ion active or not
        _ion_inactive_px = QPixmap(":/sm-icons/off.png")
        _ion_active_px = QPixmap(":/sm-icons/on.png")
        # aperture
        _ap_in_px, _ap_out_px = _blocking_px, _non_blocking_px
        self._ap_in_px_tuple = (_ap_out_px, _ap_in_px)
        # attenuator
        _att_in_px, _att_out_px = _blocking_px, _non_blocking_px
        self._att_out_px_tuple = (_att_in_px, _att_out_px)
        # position monitor (PPAC)
        self._pm_in_px_tuple = (_non_blocking_px, _blocking_px)
        # ion source active?
        self._ion_act_px_tuple = (_ion_inactive_px, _ion_active_px)
        # chopper
        self._chp_invalud_px = QPixmap(":/sm-icons/chp_invalid.png")
        self._chp_off_px = QPixmap(":/sm-icons/chp_off.png")
        self._chp_blocking_px = QPixmap(":/sm-icons/chp_blocking.png")
        self._chp_running_px = QPixmap(":/sm-icons/chp_running.png")
        self._chp_px_tuple = (self._chp_invalud_px, self._chp_off_px,
                              self._chp_blocking_px, self._chp_running_px)
        #

        # set skip none reachable option as True
        self.skip_none_chkbox.setChecked(True)

        # uncheck init_settings_chkbox when init_settings_btn is unchecked
        # other slots are set in designer.
        self.show_init_settings_btn.toggled.connect(
            self.on_toggle_show_init_settings_btn)
        # hide init settings hbox
        self.show_init_settings_btn.setChecked(False)
        #
        # selection, check/uncheck, for settings apply
        self.select_all_btn.clicked.connect(
            partial(self.on_select, 'all', True))
        self.invert_selection_btn.clicked.connect(
            partial(self.on_select, 'invert', None))
        self.deselect_all_btn.clicked.connect(
            partial(self.on_select, 'all', False))

        # filter
        self.init_filter()

        # stop auto update when lattice is changed
        # widget status regarding lattice changed.
        self.lattice_loaded.connect(self.on_update_widgets_status)
        #
        self.element_list_changed.connect(self.on_elemlist_changed)

        # context menu
        self.set_context_menu()
        self._probe_widgets_dict = {}
        self._data_trend_widgets_dict = {}  # key: (ename, fname)

        # dnd
        self.setAcceptDrops(True)

        # font size control
        zoom0 = QShortcut(QKeySequence("Ctrl+0"), self)
        zoom_in = QShortcut(QKeySequence.ZoomIn, self)
        zoom_out = QShortcut(QKeySequence.ZoomOut, self)
        zoom0.activated.connect(partial(self.on_change_font_size, 0))
        zoom_in.activated.connect(partial(self.on_change_font_size, 1))
        zoom_out.activated.connect(partial(self.on_change_font_size, -1))
        self.grow_fontsize_btn.clicked.connect(
            partial(self.on_change_font_size, 1))
        self.shrink_fontsize_btn.clicked.connect(
            partial(self.on_change_font_size, -1))

        # query tips
        self._query_tips_form = None
        self.filter_btn.toggled.connect(partial(self.on_enable_search, True))
        self.filter_btn.toggled.emit(self.filter_btn.isChecked())

        # snapshot dock
        self._snp_dock_list = []  # for snp_treeView

        # apply pb
        self.apply_pb.setVisible(False)
        # abort apply button
        self.abort_apply_btn.setVisible(False)
        # refset pb
        self.refset_pb.setVisible(False)
        # data refresh beat label
        self.refresh_beat_lbl.setPixmap(
            QPixmap(":/sm-icons/active.png").scaled(10, 10))
        self.refresh_beat_lbl.setVisible(False)
        # db pull pb
        self.db_pull_pb.setVisible(False)
        # almset pb
        self.alm_set_pb.setVisible(False)

        # current snp
        self._current_snpdata = None
        # originated template tuple: (name, taglist, snpdata_temp)
        self._current_snpdata_originated = (None, [], None)

        # template list, [(name, tag_list, snpdata),...]
        self.snp_template_list = []

        # snp filters, {btn_text (elemt, tag):ischecked?}
        self._current_btn_filter = dict()
        self._current_tag_filter = dict()
        self.snp_filters_updated.connect(self.on_snp_filters_updated)
        # URI for data source
        self.on_data_uri_changed(True, self.data_uri)

        # take snapshot tool
        self.actionTake_Snapshot.triggered.connect(
            lambda: self.take_snapshot())

        # originated snapshot template is changed
        self.sigOrigTemplateChanged.connect(self.onOrigTemplateChanged)
        #
        self.snp_loaded.connect(self.on_snp_loaded)
        # scaling factor hint
        self.snp_loaded.connect(self.on_hint_scaling_factor)
        # update filter button area (by field, type, ...)
        self.snp_loaded.connect(self.on_update_filter_controls)
        # update pos filter area
        self.snp_loaded.connect(self.on_update_pos_filter)
        # re-enable filter buttons if any
        self.snp_loaded.connect(self.refresh_filter_btns)
        # post loaded snp info
        self.snp_loaded.connect(self.post_snp_info)
        # enable take snapshot tool
        self.snp_loaded.connect(
            lambda: self.actionTake_Snapshot.setEnabled(True))
        #
        self.snp_saved.connect(self.on_snp_saved)

        # log dock

        # dict of SetLogMessagers,
        # key: timestamp of apply, value: EffSetLogMsgContainer
        self.effSetLogMsgContainer_dict = {}
        self._init_revert_area()

        #
        self.log_dock.closed.connect(
            lambda: self.actionShow_Device_Settings_Log.setChecked(False))
        self.actionShow_Device_Settings_Log.setChecked(False)
        self.sigSetLogColorChanged.connect(self.log_textEdit.setTextColor)
        self.sigSetLogColorReset.connect(
            lambda: self.log_textEdit.setTextColor(SetLogMessager.
                                                   DEFAULT_TEXT_COLOR))
        self.sigSetLogColorSkip.connect(lambda: self.log_textEdit.setTextColor(
            SetLogMessager.SKIP_SET_TEXT_COLOR))
        self.sigSetLogColorSet.connect(lambda: self.log_textEdit.setTextColor(
            SetLogMessager.SET_TEXT_COLOR))

        # hide findtext_lbl and findtext_lineEdit
        for o in (self.findtext_lbl, self.findtext_lineEdit):
            o.setVisible(False)

        # tag, ions filter buttons
        self.select_all_ions_btn.clicked.connect(
            partial(self.on_check_snp_filters, "ion", "all"))
        self.select_none_ions_btn.clicked.connect(
            partial(self.on_check_snp_filters, "ion", "none"))
        self.select_invert_ions_btn.clicked.connect(
            partial(self.on_check_snp_filters, "ion", "invert"))

        self.select_all_tags_btn.clicked.connect(
            partial(self.on_check_snp_filters, "tag", "all"))
        self.select_none_tags_btn.clicked.connect(
            partial(self.on_check_snp_filters, "tag", "none"))
        self.select_invert_tags_btn.clicked.connect(
            partial(self.on_check_snp_filters, "tag", "invert"))

        # settings view filter btn status
        self.filter_btn_group_status_changed.connect(
            self.on_filter_btn_group_status_changed)
        self.filter_btn_group_status_changed.emit()

        # pos filter button, apply logic OR for pos1 and pos2 filter
        self.pos_filter_btn.clicked.connect(
            lambda: self.pos_dspin.setValue(STRIPPER_POS))
        self.pos_filter_btn.clicked.emit()
        self.pos_filter_btn.clicked.connect(
            self.filter_lineEdit.editingFinished)
        self.pos1_filter_btn.toggled.connect(self.on_toggle_pos1_filter_btn)
        self.pos2_filter_btn.toggled.connect(self.on_toggle_pos2_filter_btn)
        self.pos_dspin.valueChanged.connect(self.update_pos_dspin_tooltip)
        self.pos_dspin.valueChanged.connect(
            lambda: self.pos1_filter_btn.toggled.emit(self.pos1_filter_btn.
                                                      isChecked()))
        self.pos_dspin.valueChanged.connect(
            lambda: self.pos2_filter_btn.toggled.emit(self.pos2_filter_btn.
                                                      isChecked()))
        self.pos_dspin.valueChanged.emit(self.pos_dspin.value())
        # do when snp_loaded as well
        self.on_update_pos_filter(None)  # pass fake (None) param as snpdata

        # snp date range filter
        self.snp_date_range_filter_enabled = False
        self.dateEdit1.setDate(
            QDate(NOW_YEAR, NOW_MONTH, NOW_DAY).addMonths(-12))
        self.dateEdit2.setDate(QDate(NOW_YEAR, NOW_MONTH, NOW_DAY))
        self.daterange_picker_btn.clicked.connect(self.on_select_daterange)
        self.filter_date_chkbox.toggled.connect(
            self.on_toggle_snp_filter_date_range)
        self.filter_date_chkbox.toggled.connect(self.on_date_range_visible)
        self.filter_date_chkbox.toggled.emit(False)
        # snp note filter
        self.snp_note_filter_enabled = False
        # hide snp filter note textedit
        self.filter_note_chkbox.toggled.emit(False)

        # expand/collapse snapshot tree
        self.snp_expand_btn.clicked.connect(partial(self.on_snp_expand, True))
        self.snp_collapse_btn.clicked.connect(
            partial(self.on_snp_expand, False))

        # setting logs
        self.log_textEdit.textChanged.connect(self.on_logtext_updated)

        # periodical clicker on single data refresh
        self._data_refresh_timer = QTimer(self)
        self._data_refresh_timer.timeout.connect(self.on_click_refresh_once)
        self._data_refresh_timer.start(REFRESH_INTERVAL_MAP["Normal"])
        # db refresher
        self._db_refresh_timer = QTimer(self)
        self._db_refresh_timer.timeout.connect(self.db_refresh)
        self._db_refresh_timer.start(DB_REFRESH_INTERVAL_MAP[1])

        # data refresher speed control
        self.refresh_speed_cbb.currentTextChanged.connect(
            self.onDataRefreshSpeedChanged)
        self.refresh_speed_cbb.setCurrentText("Normal")
        # db refresher speed control
        self.db_refresh_speed_cbb.currentIndexChanged.connect(
            self.onDbRefreshSpeedChanged)
        self.db_refresh_speed_cbb.setCurrentIndex(1)

    @pyqtSlot('QString')
    def onDataRefreshSpeedChanged(self, s: str):
        self._data_refresh_timer.setInterval(REFRESH_INTERVAL_MAP[s])

    @pyqtSlot(int)
    def onDbRefreshSpeedChanged(self, i: int):
        self._db_refresh_timer.setInterval(DB_REFRESH_INTERVAL_MAP[i])

    @pyqtSlot()
    def on_logtext_updated(self):
        # Setting logs updated.
        self.sender().document().setMaximumBlockCount(MAX_LOG_LINES)

    @pyqtSlot(bool)
    def on_date_range_visible(self, is_checked):
        """Update daterange controls visibility.
        """
        [
            o.setVisible(is_checked)
            for o in (self.dateEdit1, self.daterange_lbl, self.dateEdit2,
                      self.daterange_picker_btn)
        ]

    def on_click_refresh_once(self):
        if self._tv.model() is None:
            return
        self.single_update_btn.clicked.emit()

    @pyqtSlot(bool)
    def on_toggle_show_init_settings_btn(self, is_checked: bool):
        if not is_checked:
            # uncheck init_settings_chkbox when init_settings_btn is unchecked
            self.init_settings_chkbox.setChecked(False)
        #
        self.adv_frame.setVisible(is_checked)

    def on_update_filter_controls(self, snpdata):
        """Update filter controls
        """
        fname_set = set(snpdata.data.Field.to_list())
        dtype_set = set(snpdata.data.Type.to_list())
        self._build_filter_ctrls(self.filter_ctrls_hbox, sorted(fname_set),
                                 sorted(dtype_set))

    def _build_filter_ctrls(self, container, fnames, dtypes):
        #
        # reset field filter check states
        #
        _act_name_dict = {'field': fnames, 'type': dtypes}
        self._check_state_dict = {
            'field': {
                i: True
                for i in fnames
            },
            'type': {
                i: True
                for i in dtypes
            }
        }

        #
        # reset and build filter controls.
        #
        child = container.takeAt(0)
        while child:
            w = child.widget()
            if w is not None:
                w.setParent(None)
            del w
            del child
            child = container.takeAt(0)
        #
        def on_update_filter_string(k, category, btn, is_toggled):
            # field filter button actions is triggered.
            _d = self._check_state_dict[category]
            if k == 'All':  # update checkstates for other actions
                btn.toggled.disconnect()
                for obj in self.sender().parent().findChildren(QCheckBox):
                    obj.setChecked(is_toggled)
                btn.toggled.connect(
                    partial(on_toggle_filter_btn, category, btn))
            else:
                _d[k] = is_toggled
                obj = self.sender().parent().findChild(QCheckBox, "sel_act")
                obj.toggled.disconnect()
                obj.setChecked(all(_d.values()))
                obj.toggled.connect(
                    partial(on_update_filter_string, 'All', category, btn))

            btn.setToolTip("Filter by {}\nChecked: {}".format(
                category.capitalize(),
                ','.join([k for k, v in _d.items() if v])))
            btn.toggled.emit(btn.isChecked())

        #
        def on_toggle_filter_btn(category, btn, is_checked):
            # enable filtering by category if button is checked
            m = self._tv.model()
            if m is None:
                return
            _d = self._check_state_dict[category]
            if category == "field":
                m.filter_field_enabled = is_checked
                m.filter_field_list = [k for k, v in _d.items() if v]
            elif category == "type":
                m.filter_dtype_enabled = is_checked
                m.filter_dtype_list = [k for k, v in _d.items() if v]
            self.filter_lineEdit.editingFinished.emit()

        def _create_widgetaction(text, parent):
            _chkbox = QCheckBox(text, parent)
            _chkbox.setChecked(True)
            _wa = QWidgetAction(parent)
            _wa.setDefaultWidget(_chkbox)
            _chkbox.setStyleSheet("""QCheckBox{padding-left:10px;}""")
            return _chkbox, _wa

        def _build_actions(btn, category):
            menu = QMenu(self)
            for i in _act_name_dict[category]:
                _chkbox, _wa = _create_widgetaction(i, menu)
                _chkbox.toggled.connect(
                    partial(on_update_filter_string, i, category, btn))
                menu.addAction(_wa)
            menu.addSeparator()
            _chkbox_all, _wa_all = _create_widgetaction('All', menu)
            _chkbox_all.setObjectName("sel_act")
            _chkbox_all.toggled.connect(
                partial(on_update_filter_string, 'All', category, btn))
            menu.addAction(_wa_all)
            btn.setMenu(menu)

        # list of checkable field/dtype button actions
        self._fname_btn = fname_btn = QToolButton(self)
        fname_btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self._dtype_btn = dtype_btn = QToolButton(self)
        dtype_btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        fname_btn.setText("Field")
        fname_btn.setCheckable(True)
        fname_btn.setToolTip("Filter by Field")
        fname_btn.setPopupMode(QToolButton.MenuButtonPopup)
        fname_btn.toggled.connect(
            partial(on_toggle_filter_btn, 'field', fname_btn))

        dtype_btn.setText("Type")
        dtype_btn.setCheckable(True)
        dtype_btn.setToolTip("Filter by Type")
        dtype_btn.setPopupMode(QToolButton.MenuButtonPopup)
        dtype_btn.toggled.connect(
            partial(on_toggle_filter_btn, 'type', dtype_btn))

        container.addWidget(fname_btn)
        container.addWidget(dtype_btn)
        _build_actions(fname_btn, 'field')
        _build_actions(dtype_btn, 'type')

    @pyqtSlot()
    def on_filter_btn_group_status_changed(self):
        # Do logic 'or', if True, do global refresh when data refresher is on.
        self._filter_btn_enabled = self.show_warning_dx02_btn.isChecked() \
                or self.show_warning_dx12_btn.isChecked() or self.show_state_diff_btn.isChecked() \
                or self.show_live_sts_on_btn.isChecked() or self.show_live_sts_off_btn.isChecked()

    def resizeEvent(self, e):
        self.resizeDocks([self.snp_dock], [int(self.width() * 0.5)],
                         Qt.Horizontal)
        BaseAppForm.resizeEvent(self, e)

    def on_check_snp_filters(self, filter_type, check_type):
        area = getattr(self, f"{filter_type}_filter_area")
        if check_type == 'all':
            [i.setChecked(True) for i in area.findChildren(QToolButton)]
        elif check_type == 'none':
            [i.setChecked(False) for i in area.findChildren(QToolButton)]
        else:  # invert
            [
                i.setChecked(not i.isChecked())
                for i in area.findChildren(QToolButton)
            ]

    @pyqtSlot(bool)
    def on_enable_search(self, auto_collapse, enabled):
        if auto_collapse:
            self.filter_lineEdit.setVisible(enabled)
            self.strict_wildcard_chkbox.setVisible(enabled)
        if not enabled:
            self.filter_lineEdit.setText('')
            self.filter_lineEdit.editingFinished.emit()

    @pyqtSlot(bool)
    def on_toggle_strict_wildcard(self, on):
        delayed_exec(self.on_filter_changed, 100)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape and self.filter_btn.isChecked():
            self.filter_btn.setChecked(False)

    def on_change_font_size(self, v):
        if v == 0:
            font_size = self.default_font_size
        else:
            font_size = self.font.pointSize() + v
        self.font.setPointSize(font_size)
        self.font_changed.emit(self.font)

    def set_context_menu(self):
        for o in (self._tv, self.snp_treeView):
            o.setContextMenuPolicy(Qt.CustomContextMenu)
            o.customContextMenuRequested.connect(
                partial(self.on_custom_context_menu, o))

    @pyqtSlot()
    def on_copy_text(self, m, idx):
        text = m.data(idx)
        cb = QGuiApplication.clipboard()
        cb.setText(text)
        printlog('copied text: {}'.format(text))
        msg = '<html><head/><body><p><span style="color:#007BFF;">Copied text: </span><span style="color:#DC3545;">{}</span></p></body></html>'.format(
            text)
        self.statusInfoChanged.emit(msg)
        self._reset_status_info()

    @pyqtSlot()
    def on_probe_element(self, elem, fname):
        ename = elem.name
        if ename not in self._probe_widgets_dict:
            w = ProbeWidget(element=elem, detached=False)
            self._probe_widgets_dict[ename] = w
        w = self._probe_widgets_dict[ename]
        w.show()
        w.set_field(fname)

    @pyqtSlot()
    def on_data_trend(self, elem, fname):
        if (elem.name, fname) not in self._data_trend_widgets_dict:
            w = DataTrendWidget(elem, fname, client=self._aa_data_client)
            self._data_trend_widgets_dict[(elem.name, fname)] = w
        w = self._data_trend_widgets_dict[(elem.name, fname)]
        w.show()

    @pyqtSlot(QPoint)
    def on_custom_context_menu(self, view, pos):
        m = view.model()
        if m is None:
            return
        idx = view.indexAt(pos)
        if view == self._tv:
            menu = self._build_settings_context_menu(idx, m)
        else:
            menu = self._build_snp_context_menu(idx, m)
        #
        if menu is not None:
            menu.exec_(view.viewport().mapToGlobal(pos))

    def _build_snp_context_menu(self, idx, m):
        src_m = m.sourceModel()
        src_idx = m.mapToSource(idx)
        item = src_m.itemFromIndex(src_idx)
        text = item.text()
        if item.parent() is None:
            return None
        pindex = item.parent().index()
        #
        menu = QMenu(self)
        menu.setStyleSheet('QMenu {margin: 2px;}')
        #
        copy_action = QAction(self._copy_text_icon, "Copy Text", menu)
        copy_action.triggered.connect(partial(self.on_copy_text, m, idx))
        #
        item0 = src_m.itemFromIndex(
            src_m.index(src_idx.row(), src_m.i_ts, pindex))
        #
        if not hasattr(item0, 'snp_data'):
            return menu
        snpdata = item0.snp_data
        # copy data
        dcopy_action = QAction(self._copy_data_icon, "Copy Data", menu)
        dcopy_action.triggered.connect(partial(self.on_copy_snp, snpdata))
        # save-as
        saveas_action = QAction(self._saveas_icon, "E&xport", menu)
        saveas_action.triggered.connect(
            partial(self.on_saveas_settings, snpdata))
        # read
        read_action = QAction(self._read_icon, "&Read", menu)
        read_action.triggered.connect(partial(self.on_read_snp, snpdata))
        # viz machine state
        if self._machstate is not None:
            _mviz_text = "Machine State (diff)"
        else:
            _mviz_text = "Machine State"
        mviz_action = QAction(self._chart_icon, _mviz_text, menu)
        mviz_action.triggered.connect(partial(self.on_mviz, snpdata))
        # del
        del_action = QAction(self._del_icon, "&Delete", menu)
        del_action.triggered.connect(partial(self.on_del_settings, snpdata))

        # del admin
        del_admin_action = QAction(self._del_icon, "&Delete (Admin)", menu)
        del_admin_action.triggered.connect(
            partial(self.on_del_settings_admin, snpdata))
        # load
        load_action = QAction(self._load_icon, "&Load", menu)
        load_action.triggered.connect(partial(self.on_load_settings, snpdata))
        #
        # Set the snapshot as reference
        refpush_action = QAction(self._recommand_icon, "&Set As Reference",
                                 menu)
        refpush_action.triggered.connect(
            partial(self.on_push_ref_settings, snpdata))
        #
        menu.addAction(load_action)
        menu.addAction(refpush_action)
        menu.addSeparator()
        menu.addAction(copy_action)
        menu.addAction(dcopy_action)
        menu.addSeparator()
        menu.addAction(read_action)
        menu.addAction(mviz_action)
        menu.addSeparator()
        menu.addAction(saveas_action)
        menu.addAction(del_action)
        if getuser() in ('zhangt', 'tong'):  # Admin
            menu.addAction(del_admin_action)
        return menu

    @pyqtSlot()
    def on_set_tol_val(self, src_m, fld, src_idx, pv):
        if pv is not None:
            try:
                val = float(self.tol_val_lineEdit.text())
            except:
                pass
            else:
                r = pv.put(val, timeout=0.5)
                if r is None:  # failed
                    QMessageBox.warning(
                        self, "Set Tolerance",
                        f"Failed to set {pv.pvname} with {val}.",
                        QMessageBox.Ok)
                else:
                    delayed_exec(
                        partial(self._refresh_tol_values, src_m, fld, src_idx,
                                pv), 500)

    def _refresh_tol_values(self, m, fld, src_idx, pv):
        # TODO: refactor to a standard function for single row data refreshing
        # refresh tol and dx12 columns
        # after the tol being changed thru context menu.
        tol = pv.value
        irow = src_idx.row()
        x1 = fld.value
        x2 = fld.current_setting()
        dx12 = x1 - x2
        x1_idx = m.index(irow, m.i_rd)
        x2_idx = m.index(irow, m.i_cset)
        dx12_idx = m.index(irow, m.i_rd_cset)
        tol_idx = m.index(irow, m.i_tol)
        for iidx, iv in zip((x1_idx, x2_idx, dx12_idx, tol_idx),
                            (x1, x2, dx12, tol)):
            m.setData(iidx, self.fmt.format(iv), Qt.DisplayRole)
        if abs(dx12) > tol:
            m.setData(dx12_idx, self._warning_px, Qt.DecorationRole)
            m.setData(dx12_idx, 'warning', Qt.UserRole)
        else:
            m.setData(dx12_idx, self._no_warning_px, Qt.DecorationRole)
            m.setData(dx12_idx, None, Qt.UserRole)

    @pyqtSlot()
    def on_set_ref_val(self, src_m, fld, src_idx, pv):
        if pv is not None:
            try:
                val = float(self.ref_val_lineEdit.text())
            except:
                pass
            else:
                r = pv.put(val, timeout=0.1)
                if r is None:  # failed
                    QMessageBox.warning(
                        self, "Set Reference",
                        f"Failed to set {pv.pvname} with {val}.",
                        QMessageBox.Ok)
                else:
                    delayed_exec(
                        partial(self._refresh_ref_values, src_m, fld, src_idx,
                                pv), 500)

    def _refresh_ref_values(self, m, fld, src_idx, pv):
        # TODO: refactor to a standard function for single row data refreshing
        # refresh xref, dx2ref and dx0ref columns
        # after the xref being changed thru context menu.
        xref = pv.value
        irow = src_idx.row()
        x0_idx = m.index(irow, m.i_val0)
        x0 = float(m.data(x0_idx))
        x1 = fld.value
        x2 = fld.current_setting()
        dx01 = x0 - x1
        dx02 = x2 - x0
        dx12 = x1 - x2
        dx2ref = x2 - xref
        dx0ref = x0 - xref

        x1_idx = m.index(irow, m.i_rd)
        x2_idx = m.index(irow, m.i_cset)
        dx01_idx = m.index(irow, m.i_val0_rd)
        dx02_idx = m.index(irow, m.i_val0_cset)
        dx12_idx = m.index(irow, m.i_rd_cset)
        ref_st_idx = m.index(irow, m.i_ref_st)
        dx2ref_idx = m.index(irow, m.i_dstref)
        dx0ref_idx = m.index(irow, m.i_dval0ref)
        ratio_x20_idx = m.index(irow, m.i_ratio_x20)

        for iidx, iv in zip((ref_st_idx, dx2ref_idx, dx0ref_idx, x1_idx,
                             x2_idx, dx01_idx, dx02_idx, dx12_idx),
                            (xref, dx2ref, dx0ref, x1, x2, dx01, dx02, dx12)):
            m.setData(iidx, self.fmt.format(iv), Qt.DisplayRole)
        m.setData(ratio_x20_idx, get_ratio_as_string(x2, x0, self.fmt),
                  Qt.DisplayRole)

        tol_idx = m.index(irow, m.i_tol)
        tol = float(m.data(tol_idx))
        if abs(dx12) > tol:
            m.setData(dx12_idx, self._warning_px, Qt.DecorationRole)
            m.setData(dx12_idx, 'warning', Qt.UserRole)
        else:
            m.setData(dx12_idx, self._no_warning_px, Qt.DecorationRole)
            m.setData(dx12_idx, None, Qt.UserRole)

        if not is_close(x0, x2, self.ndigit):
            m.setData(dx02_idx, self._warning_px, Qt.DecorationRole)
            m.setData(dx02_idx, 'warning', Qt.UserRole)
        else:
            m.setData(dx02_idx, self._no_warning_px, Qt.DecorationRole)
            m.setData(dx02_idx, None, Qt.UserRole)

        for iidx, iv in zip((dx2ref_idx, dx0ref_idx), (x2, x0)):
            if not is_close(iv, xref, self.ndigit):
                m.setData(iidx, self._warning_px, Qt.DecorationRole)
                m.setData(iidx, "warning", Qt.UserRole)
            else:
                m.setData(iidx, self._no_warning_px, Qt.DecorationRole)
                m.setData(iidx, None, Qt.UserRole)

    @pyqtSlot()
    def on_fill_ref_with_x2(self, fld):
        """Fill ref_val_lineEdit with the current live setpoint.
        """
        x2 = fld.current_setting()
        self.ref_val_lineEdit.setText(str(x2))

    def _build_settings_context_menu(self, idx, m):
        src_m = m.sourceModel()
        src_idx = m.mapToSource(idx)
        item = src_m.itemFromIndex(src_idx)
        if item is None:
            return
        text = item.text()
        #
        menu = QMenu(self)
        menu.setStyleSheet("""
        QMenu {
            margin: 2px;
        }
        """)

        _title_w = QLabel(text)
        _title_w.setStyleSheet(f"""
            QLabel{{
                background: #FFCC82;
                font-weight: bold;
                padding: 2px 2px 2px {PX_SIZE+2}px;
            }}""")
        _title_act = QWidgetAction(self)
        _title_act.setDefaultWidget(_title_w)
        #
        menu.addAction(_title_act)

        #
        copy_action = QAction(self._copy_text_icon, "Copy Text", menu)
        copy_action.triggered.connect(partial(self.on_copy_text, m, idx))
        menu.addAction(copy_action)

        # tolerance column? add action for new value setting.
        if src_idx.column() == src_m.i_tol:
            tol_pv = src_m.data(src_idx, Qt.UserRole + 1)
            fld = src_m.itemFromIndex(src_m.index(src_idx.row(),
                                                  src_m.i_name)).fobj
            tol_set_lbl = QLabel("New Tolerance:", self)
            _tol_v_now_str = src_m.data(src_idx, Qt.DisplayRole)
            self.tol_val_lineEdit = QLineEdit(_tol_v_now_str, self)
            tol_set_btn = QToolButton(self)
            tol_set_btn.setText("Set")
            tol_set_btn.clicked.connect(
                partial(self.on_set_tol_val, src_m, fld, src_idx, tol_pv))
            tol_set_w = QWidget(self)
            tol_set_hbox = QHBoxLayout()
            tol_set_hbox.setContentsMargins(6, 4, 4, 4)
            tol_set_hbox.setSpacing(2)
            tol_set_hbox.addWidget(tol_set_lbl)
            tol_set_hbox.addWidget(self.tol_val_lineEdit, 1)
            tol_set_hbox.addWidget(tol_set_btn)
            tol_set_w.setLayout(tol_set_hbox)
            #
            tol_set_act = QWidgetAction(self)
            tol_set_act.setDefaultWidget(tol_set_w)
            #
            menu.addAction(tol_set_act)

        # refset column? add action for new value setting.
        if src_idx.column() == src_m.i_ref_st:
            ref_pv = src_m.data(src_idx, Qt.UserRole + 1)
            fld = src_m.itemFromIndex(src_m.index(src_idx.row(),
                                                  src_m.i_name)).fobj
            ref_set_lbl = QLabel("New Reference:", self)

            # _ref_v_now = caget(ref_pv, timeout=1)
            # if _ref_v_now is None:
            #     _ref_v_now_str = 'disconnected'
            # else:
            #     _ref_v_now_str = self.fmt.format(_ref_v_now)
            _ref_v_now_str = src_m.data(src_idx, Qt.DisplayRole)
            self.ref_val_lineEdit = QLineEdit(_ref_v_now_str, self)
            # self.ref_val_lineEdit.setValidator(QDoubleValidator())
            ref_set_btn = QToolButton(self)
            ref_set_btn.setText("Set")
            ref_set_btn.clicked.connect(
                partial(self.on_set_ref_val, src_m, fld, src_idx, ref_pv))
            # fetch and fill saved setpoint (x0)
            ref_set_fetch_x0_btn = QToolButton(self)
            ref_set_fetch_x0_btn.setText("x0")
            ref_set_fetch_x0_btn.setToolTip(
                "Fill out with saved setpoint (x0)")
            x0 = src_m.data(src_m.index(src_idx.row(), src_m.i_val0))
            ref_set_fetch_x0_btn.clicked.connect(
                lambda: self.ref_val_lineEdit.setText(x0))
            # fetch and fill live setpoint (x2)
            ref_set_fetch_x2_btn = QToolButton(self)
            ref_set_fetch_x2_btn.setText("x2")
            ref_set_fetch_x2_btn.setToolTip("Fill out with live setpoint (x2)")
            ref_set_fetch_x2_btn.clicked.connect(
                partial(self.on_fill_ref_with_x2, fld))
            #
            ref_set_w = QWidget(self)
            ref_set_hbox = QHBoxLayout()
            ref_set_hbox.setContentsMargins(6, 4, 4, 4)
            ref_set_hbox.setSpacing(2)
            ref_set_hbox.addWidget(ref_set_lbl)
            ref_set_hbox.addWidget(self.ref_val_lineEdit, 1)
            ref_set_hbox.addWidget(ref_set_fetch_x0_btn)
            ref_set_hbox.addWidget(ref_set_fetch_x2_btn)
            ref_set_hbox.addWidget(ref_set_btn)
            ref_set_w.setLayout(ref_set_hbox)
            #
            ref_set_act = QWidgetAction(self)
            ref_set_act.setDefaultWidget(ref_set_w)
            #
            menu.addAction(ref_set_act)

        #
        if hasattr(item, 'fobj'):
            ename = text
            elem = self._lat[ename]
            fld = item.fobj
            probe_action = QAction(self._probe_icon, "Probe Element", menu)
            probe_action.triggered.connect(
                partial(self.on_probe_element, elem, fld.name))
            menu.addAction(probe_action)

            # data log: set/read values
            if self._aa_data_client is not None:
                trend_action = QAction(self._trend_icon, "Data Trend", menu)
                trend_action.triggered.connect(
                    partial(self.on_data_trend, elem, fld.name))
                menu.addAction(trend_action)

        # toggle items action
        # selected_rows = {idx.row() for idx in self._tv.selectedIndexes()}

        selected_rows = []
        checked_status = []
        power_status = []  # list of (CaElement, PWRSTS, pwr_fname)
        for _idx in self._tv.selectedIndexes():
            if _idx.column() == src_m.i_name:
                selected_rows.append(_idx.row())
                power_status.append(self._get_pwrsts(src_m, m, _idx))
                checked_status.append(
                    is_item_checked(src_m.itemFromIndex(m.mapToSource(_idx))))

        n_rows = len(selected_rows)
        _item0 = src_m.itemFromIndex(src_m.index(src_idx.row(), src_m.i_name))
        is_checked = is_item_checked(_item0)
        if n_rows == 1:
            row_text = 'Row'
        else:
            row_text = 'Rows'
        if is_checked:
            new_check_state = False
            act_text = f"Uncheck All ({n_rows}) {row_text}"
        else:
            new_check_state = True
            act_text = f"Check All ({n_rows}) {row_text}"

        if all(checked_status):
            act_icon = self._unsel_icon
        elif not any(checked_status):
            act_icon = self._sel_icon
        else:
            act_icon = self._sel3_icon

        sel_action = QAction(act_icon, act_text, menu)
        sel_action.triggered.connect(
            partial(self.on_toggle_selected_rows, selected_rows, m,
                    new_check_state))
        menu.addAction(sel_action)

        # turn on/off PWRSTS field
        _add_switch_menu = False
        if n_rows == 1:
            if power_status[0][1] != None:  # show switch action
                new_power_status = not power_status[0][1]
                if new_power_status:
                    act_text = "Turn on"
                    act_icon = self._turn_on_icon
                else:
                    act_text = "Turn off"
                    act_icon = self._turn_off_icon
                switch_menu = menu.addMenu("Power Switch")
                sm_action = QAction(act_icon, act_text, switch_menu)
                sm_action.triggered.connect(
                    partial(self.on_toggle_pwrsts, selected_rows, m, src_m,
                            new_power_status, power_status))
                switch_menu.addAction(sm_action)
                _add_switch_menu = True
        else:
            if not all(i is None
                       for _, i, _ in power_status):  # show switch action
                new_power_status = not self._get_pwrsts(src_m, m, idx)[1]
                if new_power_status:
                    act_text = "Turn All on"
                    act_icon = self._turn_on_icon
                else:
                    act_text = "Turn All off"
                    act_icon = self._turn_off_icon
                switch_menu = menu.addMenu("Power Switch")
                sm_action = QAction(act_icon, act_text, switch_menu)
                sm_action.triggered.connect(
                    partial(self.on_toggle_pwrsts, selected_rows, m, src_m,
                            new_power_status, power_status))
                switch_menu.addAction(sm_action)
                _add_switch_menu = True

        if _add_switch_menu:
            sm_reset_act = QAction(self._warning_amber_icon,
                                   "Reset Trip Events", switch_menu)
            sm_reset_act.setToolTip("Only for turn on bias voltages.")
            sm_reset_act.triggered.connect(
                partial(self.on_reset_trip_events, power_status))
            switch_menu.addAction(sm_reset_act)
            switch_menu.setIcon(self._power_switch_icon)
            switch_menu.setToolTipsVisible(True)

        # External apps
        def _launch_app(_exec, _args='', _cwd=None):
            Popen(f'{_exec} {_args}', cwd=_cwd, shell=True)

        apps_conf = self.pref_dict.get('EXTERNAL_APPS', None)
        if apps_conf is None:
            return menu
        for _, _app_conf in apps_conf.items():
            _app_name = _app_conf['NAME']
            _app_exec = _app_conf['EXEC']
            _app_args = _app_conf.get('ARGS', '').format(
                ename=text,
                machine=self._last_machine_name,
                segment=self._last_lattice_name)
            _app_cwd = _app_conf.get('CWD', '')
            if _app_cwd == '':
                _app_cwd = None
            _app_act = QAction(self._ext_app_icon, "Start " + _app_name, menu)
            _app_act.triggered.connect(
                partial(_launch_app, _app_exec, _app_args, _app_cwd))
            menu.addAction(_app_act)

        return menu

    @pyqtSlot()
    def on_toggle_selected_rows(self, selected_rows, m, new_check_state):
        for i in selected_rows:
            m.select_one(i, new_check_state)

    @pyqtSlot()
    def on_reset_trip_events(self, power_status):
        # reset trip events, for ISEG PSs
        # _reset_trip_events()
        put_iseg_pvs = []
        for elem, _, _ in power_status:
            iseg_pv = caget(f"{elem.name}:VBS:doClear.NAME")
            if iseg_pv in put_iseg_pvs:
                continue
            caput(iseg_pv, 1)
            msg = "[{0}] Reset {1}.".format(
                datetime.fromtimestamp(time.time()).strftime(TS_FMT), iseg_pv)
            self.log_textEdit.append(msg)
            put_iseg_pvs.append(iseg_pv)

    def _get_pwrsts(self, m_src, m, idx):
        # power status from selected index, return tuple of CaElement, PWRSTS, pwr_fname (None if not defined).
        idx_src = m.mapToSource(m.index(idx.row(), idx.column()))
        it = m_src.itemFromIndex(idx_src)
        elem = self._lat[it.text()]
        fname = m_src.data(m_src.index(idx_src.row(), m_src.i_field))
        if fname == 'I_TC':
            pwr_fname = 'PWRSTS_TC'
        else:
            pwr_fname = 'PWRSTS'
        try:
            r = getattr(elem, pwr_fname)
        except AttributeError:
            r = None
        finally:
            return elem, r, pwr_fname

    @pyqtSlot()
    def on_toggle_pwrsts(self, selected_rows, m, m_src, new_power_status,
                         current_power_status):
        # current_power_status: list of (CaElement, PWRSTS, pwr_fname)
        for elem, _, pwr_fname in current_power_status:
            if pwr_fname in elem.fields:
                setattr(elem, pwr_fname, int(new_power_status))
                sts = 'ON' if new_power_status else 'OFF'
                msg = "[{0}] Turn power {2} for {1:<20s}".format(
                    datetime.fromtimestamp(time.time()).strftime(TS_FMT),
                    elem.name + '.', sts)
            else:
                msg = "[{0}] [Skip] Set power status for {1:<20s}".format(
                    datetime.fromtimestamp(time.time()).strftime(TS_FMT),
                    elem.name + '.')
            self.log_textEdit.append(msg)
        # refresh
        delayed_exec(lambda: self.single_update_btn.clicked.emit(), 2000)

    @pyqtSlot(QVariant)
    def on_update_widgets_status(self, o):
        # WIP: control widget status after lattice is loaded.
        self.update_lattice_info_lbls(o.last_machine_name, o.last_lattice_name)

    @pyqtSlot()
    def on_elemlist_changed(self):
        # element list changed
        # update flat_settings and settings
        # update settings view
        flat_settings, settings = pack_settings(
            self._elem_list,
            self._lat,
            settings=self._lat.settings,
            data_source=DATA_SRC_MAP[self.field_init_mode],
            only_physics=False,
            skip_none=self.skip_none_chkbox.isChecked())
        self.settingsLoaded.emit(flat_settings, settings)

    def init_filter(self):
        """Initial filter.
        """
        o = self.filter_lineEdit
        o.setToolTip(FILTER_TT)
        self._comp = QCompleter([], self)
        o.setCompleter(self._comp)

    def update_filter_completer(self, s):
        m = self._comp.model()
        sl = m.stringList()
        if s not in sl:
            sl.append(s)
        m.setStringList(sl)

    @pyqtSlot(int)
    def on_update_rate_changed(self, i):
        if i == 6:  # add 'auto' back to cbb index 6
            self._update_mode = 'auto'
            tt = "Auto updating rate."
        else:
            self._update_mode = 'thread'
            rate = IDX_RATE_MAP[i]
            self._update_delt = 1.0 / rate  # sec
            tt = "Updating at {0:.1f} Hz.".format(rate)
        self.update_rate_cbb.setToolTip(tt)

    @pyqtSlot()
    def onImport(self):
        """Import one or more .csv, .xlsx files as new snapshots.
        """
        if self._import_snp_dlg is None:
            self._import_snp_dlg = ImportSNPDialog(self)
        self._import_snp_dlg.sigRefreshDatabase.connect(self.db_refresh)
        self._import_snp_dlg.show()

    @pyqtSlot('QString')
    def on_scaling_factor_changed(self, s):
        self._eval_scaling_factor = False

    @pyqtSlot()
    def on_input_scaling_factor(self):
        """Input scaling factor and return.
        """
        v = str2float(self.scaling_factor_lineEdit.text())
        if v is None:
            v = 1.0
        self.scaling_factor_lineEdit.setText(str(v))
        self._eval_scaling_factor = True

    @pyqtSlot()
    def on_apply_settings(self):
        """Apply selected element settings.
        """
        m = self._tv.model()
        if m is None:
            return
        if not self._eval_scaling_factor:
            self.scaling_factor_lineEdit.returnPressed.emit()

        # scaling factor
        scaling_factor = float(self.scaling_factor_lineEdit.text())
        # scale operator, default is 0: 'x' [multiply], (1: '+') [plus]
        scale_op = SCALE_OP_MAP[self.scale_op_cbb.currentIndex()]

        #
        self.idx_px_list = [
        ]  # list to apply icon [(idx_src, px, setlogMessager)]
        settings_selected = m.get_selection()

        # show warning before applying
        if scale_op == 'x':
            r = QMessageBox.warning(
                self, "Apply Settings",
                '''<html><head/><body><p>You are about to apply ({0}) settings by scaling the factor of <span style=" font-weight:600; color:#ff007f;">{1:g}</span> ?</p></body></html>'''
                .format(len(settings_selected),
                        scaling_factor), QMessageBox.Yes | QMessageBox.No)
        elif scale_op == '+':
            r = QMessageBox.warning(
                self, "Apply Settings",
                '''<html><head/><body><p>You are about to apply ({0}) settings by shifting the value of <span style=" font-weight:600; color:#ff007f;">{1:g}</span> ?</p></body></html>'''
                .format(len(settings_selected),
                        scaling_factor), QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.No:
            return

        # when apply is triggered, reason of why change device settings
        _apply_ts = datetime.fromtimestamp(time.time()).strftime(TS_FMT)[:-3]
        _apply_reason = self.apply_reason_lineEdit.text()
        _effSetLogMsgContainer = self.effSetLogMsgContainer_dict.setdefault(
            _apply_ts, EffSetLogMsgContainer())
        _effSetLogMsgContainer.clear()
        #
        self.applyer = DAQT(daq_func=partial(self.apply_single, scaling_factor,
                                             scale_op),
                            daq_seq=settings_selected)
        self.applyer.daqStarted.connect(lambda: self.apply_pb.setVisible(True))
        self.applyer.daqStarted.connect(
            lambda: self.abort_apply_btn.setVisible(True))
        self.applyer.daqStarted.connect(
            partial(self.set_widgets_status_for_applying, 'START'))
        self.applyer.meta_signal1.connect(
            partial(self.on_update_setlog, _effSetLogMsgContainer,
                    m.sourceModel()))
        self.applyer.progressUpdated.connect(self.on_apply_settings_progress)
        self.applyer.daqFinished.connect(
            partial(self.set_widgets_status_for_applying, 'STOP'))
        self.applyer.daqFinished.connect(
            lambda: self.apply_pb.setVisible(False))
        self.applyer.daqFinished.connect(
            lambda: self.abort_apply_btn.setVisible(False))
        self.applyer.daqFinished.connect(
            lambda: self.single_update_btn.clicked.emit())
        self.applyer.daqFinished.connect(
            lambda: self.apply_reason_lineEdit.clear())
        self.applyer.daqFinished.connect(
            partial(self.add_new_revert, _apply_ts, _apply_reason))
        self.applyer.start()

    def apply_single(self, sf: float, sop: str, tuple_idx_settings: tuple):
        # sop: scale operator
        idx_src, settings, new_fval0 = tuple_idx_settings
        elem, fname, fld, fval0 = settings
        ename = elem.name
        # print("New fval: {}, fval0: {}".format(new_fval0, fval0))
        if sop == 'x':
            if fname in SCALABLE_FIELD_NAMES:
                fval_to_set = new_fval0 * sf
            else:
                fval_to_set = new_fval0
        elif sop == '+':
            fval_to_set = new_fval0 + sf
        #
        try:
            t0 = time.perf_counter()
            fval_current_settings = fld.current_setting()
            if is_close(fval_current_settings, fval_to_set, self.ndigit):
                msger = SetLogMessager(None, ename, fname,
                                       fval_current_settings, fval_to_set,
                                       new_fval0, sop, sf, idx_src, True)
            else:
                fld.value = fval_to_set
                msger = SetLogMessager(fld, ename, fname,
                                       fval_current_settings, fval_to_set,
                                       new_fval0, sop, sf, idx_src)
        except:
            px = self.fail_px
        else:
            self.applyer.meta_signal1.emit(msger)
            px = self.done_px
            dt = self.t_wait - (time.perf_counter() - t0)
            if dt > 0:
                time.sleep(dt)
        self.idx_px_list.append((idx_src, px, msger))

    def on_update_setlog(self, setLogMsgContainer, m, msger):
        """Update set log.
        """
        m.hlrow(msger._idx_src)
        if msger.is_skip_set():
            self.sigSetLogColorSkip.emit()
        else:
            self.sigSetLogColorSet.emit()
            # keep mesger for revert
            setLogMsgContainer.append(msger)
        self.log_textEdit.append(str(msger))

    @pyqtSlot(float, 'QString')
    def on_apply_settings_progress(self, per: float, str_idx: str):
        # note: time wait (self.t_wait) cannot be too small, otherwise, this routine does
        # not have enough time to proceed, thus happens with missed/duplicated log messagers.
        # effSetLogMsgContainer updating should be put into apply_single routine, and
        # progress update routine to on_setlog_changed method.
        self.apply_pb.setValue(int(per * 100))

    def closeEvent(self, e):
        self._data_refresh_timer.stop()
        if self.one_updater is not None and not self.one_updater.isFinished():
            self.one_updater.abort()
        BaseAppForm.closeEvent(self, e)

    def clean_up(self):
        try:
            os.remove(LOG_FILE)
        except:
            pass
        else:
            printlog("Cleaned up settings log.")
        try:
            for p, conn in self._db_conn_pool.items():
                conn.close()
        except:
            pass
        else:
            printlog(f"Closed connection to {p}.")

    @pyqtSlot(bool)
    def on_toggle_phyfields(self, f):
        self._eng_phy_toggle['PHY'] = f
        self.toggle_ftype()

    @pyqtSlot(bool)
    def on_toggle_engfields(self, f):
        self._eng_phy_toggle['ENG'] = f
        self.toggle_ftype()

    def toggle_ftype(self):
        m = self._tv.model()
        if m is None:
            return
        m.filter_ftypes = [
            k for k, v in self._eng_phy_toggle.items() if v is True
        ]
        self.filter_lineEdit.editingFinished.emit()

    @pyqtSlot()
    def on_load_lattice(self):
        """Load lattice.
        """
        if self._lattice_load_window is None:
            self._lattice_load_window = LatticeWidget()
            self._lattice_load_window.latticeChanged.connect(
                self.on_lattice_changed)
            self._lattice_load_window.latticeChanged.connect(
                self._lattice_load_window.close)
            self._lattice_load_window.latticeChanged.connect(
                self.show_init_settings_info)
        self._lattice_load_window.show()

    @pyqtSlot()
    def on_show_latinfo(self):
        machine = self.lv_mach_lbl.text()
        lattice = self.lv_segm_lbl.text()
        if machine == '' or lattice == '':
            return

        from phantasy_apps.lattice_viewer import LatticeViewerWindow
        from phantasy_apps.lattice_viewer import __version__
        from phantasy_apps.lattice_viewer import __title__

        if self._lv is None:
            self._lv = LatticeViewerWindow(__version__)
            self._lv.setWindowTitle("{} ({})".format(__title__,
                                                     self.getAppTitle()))
            self._lv._initialize_lattice_widget()
        lw = self._lv._lattice_load_window
        lw.mach_cbb.setCurrentText(machine)
        lw.seg_cbb.setCurrentText(lattice)
        lw.load_btn.clicked.emit()
        self._lv.show()

    def on_pressed_view(self, idx):
        m = self._tv.model()
        if m is None:
            return
        if QGuiApplication.mouseButtons() == Qt.MiddleButton:
            cb = QGuiApplication.clipboard()
            if cb.supportsSelection():
                text = m.data(idx)
                cb.setText(text, cb.Selection)
                msg = '<html><head/><body><p><span style=" color:#007bff;">Selected text: </span><span style=" color:#dc3545;">{}</span><span style=" color:#007bff;">, paste with middle button.</span></p></body></html>'.format(
                    text)
                self.statusInfoChanged.emit(msg)
                self._reset_status_info()

    def on_snpdock_top_level_changed(self, is_floating):
        if is_floating:
            self.sender().setWindowFlags(Qt.CustomizeWindowHint | Qt.Window
                                         | Qt.WindowMinimizeButtonHint
                                         | Qt.WindowMaximizeButtonHint)
            self.sender().show()

    def on_click_snpview(self, idx):
        return
        print("SNP Model: ", idx.model())
        r, c = idx.row(), idx.column()
        m = self.snp_treeView.model()
        src_m = m.sourceModel()
        src_idx = m.mapToSource(idx)
        src_r, src_c = src_idx.row(), src_idx.column()
        printlog("SNP, Index of PxyModel ({}, {}), text: {}".format(
            r, c, str(m.data(idx))))
        printlog("SNP, Index of SrcModel ({}, {}), text: {}".format(
            src_r, src_c, str(src_m.data(src_idx))))

        item = src_m.itemFromIndex(src_idx)
        printlog(
            "SNP, Clicked: ({}, {}), item is expanded? ({}), is checked? ({})".
            format(idx.row(), idx.column(), self.snp_treeView.isExpanded(idx),
                   is_item_checked(item)))

    def on_click_view(self, idx):
        return
        r, c = idx.row(), idx.column()
        m = self._tv.model()
        src_m = m.sourceModel()
        src_idx = m.mapToSource(idx)
        src_r, src_c = src_idx.row(), src_idx.column()
        # printlog("Index of PxyModel ({}, {}), text: {}".format(
        #     r, c, str(m.data(idx))))
        # printlog("Index of SrcModel ({}, {}), text: {}".format(
        #     src_r, src_c, str(src_m.data(src_idx))))

        item = src_m.itemFromIndex(src_idx)
        # printlog("Clicked: ({}, {}), item is expanded? ({}), is checked now? ({}) last state {}".format(
        #     idx.row(), idx.column(), self._tv.isExpanded(idx),
        #     is_item_checked(item), last_checkstate))

        if idx.column() == src_m.i_name:
            ename_item = src_m.itemFromIndex(src_idx)
            if hasattr(ename_item, 'fobj'):
                fobj = ename_item.fobj
                printlog("Auto-monitor on? ", fobj.get_auto_monitor())

    def on_dblclicked_view(self, idx):
        r, c = idx.row(), idx.column()
        self._tv.model().toggle_selection_one(r)

    def on_dblclicked_snp(self, idx):
        m = self.snp_treeView.model()
        if m is None:
            return
        src_m = m.sourceModel()
        src_idx = m.mapToSource(idx)
        item = src_m.itemFromIndex(src_idx)
        if item.parent() is None:
            return
        if src_idx.column() in (src_m.i_tags, src_m.i_note):
            return
        item0 = src_m.itemFromIndex(
            src_m.index(src_idx.row(), 0,
                        item.parent().index()))
        self.on_load_settings(item0.snp_data)

    @pyqtSlot()
    def on_filter_changed(self):
        m = self._tv.model()
        if m is None:
            return
        full_str = self.filter_lineEdit.text().strip()
        filter_key_value_tuples = []  # list of tuples of k, is_number_key, v
        for s in full_str.split('and'):
            s = s.strip()
            k = None
            kv = s.split('=', 1)
            if len(kv) == 2:
                k, v = kv[0].strip().lower(), kv[1].strip()
            else:
                v = s
            if v == '':
                v = '*'
            if not self.strict_wildcard_chkbox.isChecked():
                v = f"*{v}*"
            if k not in VALID_FILTER_KEYS:
                k = 'device'
            if k in VALID_FILTER_KEYS_NUM:
                is_number_key = True
            else:
                is_number_key = False
            filter_key_value_tuples.append((k, is_number_key, v))
            m.set_filters(filter_key_value_tuples)

            # Qt >= 5.12
            # re_str = QRegularExpression.wildcardToRegularExpression(v)
            # m.setFilterRegularExpression(re_str)

            # m.setFilterRegExp(QRegExp(v, Qt.CaseSensitive,
            #                          QRegExp.WildcardUnix))

            #if k in VALID_FILTER_KEYS_NUM:
            #    m.setFilterRegExp(v)
            #else:
            #    m.setFilterRegExp(fnmatch.translate(v))
        m.invalidate()
        #
        self.total_show_number_lbl.setText(str(m.rowCount()))
        self.update_filter_completer(full_str)
        # disable/enable apply button?
        if len(m.get_selection()) > 0:
            self.sigApplyReady.emit(True)
        else:
            self.sigApplyReady.emit(False)

    def __load_lattice(self, mach: str, segm: str, post_info: bool = True):
        self._post_info = post_info
        self.actionLoad_Lattice.triggered.emit()
        self._lattice_load_window.setVisible(False)
        self._lattice_load_window.mach_cbb.setCurrentText(mach)
        self._lattice_load_window.seg_cbb.setCurrentText(segm)
        self._lattice_load_window.auto_monitor_chkbox.setChecked(False)
        loop = QEventLoop()
        self._lattice_load_window.latticeChanged.connect(loop.exit)
        self._lattice_load_window.load_btn.clicked.emit()
        loop.exec_()

    @pyqtSlot(bool)
    def on_toggle_init_lattice_settings(self, enabled):
        """If checked, to initialize device settings with entire loaded lattice.
        """
        self.init_settings = enabled
        self.pref_dict['SETTINGS']['INIT_SETTINGS'] = enabled
        if enabled and self._mp is not None:
            self._elem_list[:] = self._lat[:]
            self.element_list_changed.emit()

    @pyqtSlot(int)
    def on_ndigit_valueChanged(self, i):
        self.ndigit = i
        self.pref_dict['ndigit'] = i
        self.ndigit_changed.emit(i)

    @pyqtSlot()
    def on_launch_preferences(self):
        """Launch preferences dialog.
        """
        pref_dlg = PreferencesDialog(self.pref_dict, self)
        pref_dlg.pref_changed.connect(self.on_update_pref)
        pref_dlg.visibility_changed.connect(self.on_update_visibility)
        # pref_dlg.config_changed.connect(self.on_config_updated)
        pref_dlg.font_changed.connect(self.font_changed)
        pref_dlg.init_settings_changed.connect(self.init_settings_changed)
        pref_dlg.ndigit_sbox.valueChanged.connect(self.ndigit_sbox.setValue)
        pref_dlg.data_uri_changed.connect(
            partial(self.on_data_uri_changed, True))
        r = pref_dlg.exec_()

    @pyqtSlot(dict)
    def on_update_pref(self, d):
        """Update app preferences.
        """
        for k, v in d.items():
            self.pref_dict[k].update(v)
        self.field_init_mode = self.pref_dict['SETTINGS']['FIELD_INIT_MODE']
        self.t_wait = self.pref_dict['SETTINGS']['T_WAIT']
        self.init_settings = self.pref_dict['SETTINGS']['INIT_SETTINGS']
        ndigit = self.pref_dict['SETTINGS']['PRECISION']
        if ndigit != self.ndigit:
            self.ndigit_changed.emit(ndigit)

    def __read_data2frame(self, n: int, d: str):
        # read data from database to dataframe
        _bound_tag = self.ops_bound_cbb.currentText()
        if _bound_tag == '*':
            _q_cond = ''
        else:  # LINAC, FSEE
            _q_cond = f"WHERE tags like '%{_bound_tag}%'"

        if n == 'All':
            _q = f"SELECT * FROM snapshot {_q_cond}"
        else:
            _q = f"SELECT rowid,* FROM snapshot {_q_cond} ORDER BY rowid DESC LIMIT {n}"

        w_list = (self.nsnp_btn, self.snp_refresh_btn, self.ops_bound_cbb)

        def _load_df(i):
            conn = ensure_connect_db(d)
            _df = pd.read_sql(_q, conn)
            conn.close()
            return _df

        def _load_ready(res):
            self.df_all_row_tuple = list(res[0].iterrows())
            self.db_pull.emit()

        def _load_started():
            [o.setEnabled(False) for o in w_list]
            self._task_list.append('Pulling snapshots from the database...')
            self._splash_msg_undone()

        def _load_done():
            task_name = "Pulling snapshots from the database..."
            self._task_list.remove(task_name)
            self._splash_msg("Pulled snapshots from the database.")
            self._splash_msg_undone()
            [o.setEnabled(True) for o in w_list]

        self._df_loader = DAQT(daq_func=_load_df, daq_seq=range(1))
        self._df_loader.daqStarted.connect(
            lambda: self.db_pull_pb.setVisible(True))
        self._df_loader.daqStarted.connect(_load_started)
        self._df_loader.resultsReady.connect(_load_ready)
        self._df_loader.daqFinished.connect(_load_done)
        self._df_loader.daqFinished.connect(
            lambda: self.db_pull_pb.setVisible(False))
        self._df_loader.start()

    @pyqtSlot('QString')
    def on_data_uri_changed(self, purge, d):
        # reset snp dock with files in d (recursively)
        if purge:
            del self._snp_dock_list[:]
        # DB
        self._db_conn = self._db_conn_pool.setdefault(d, ensure_connect_db(d))
        self.data_uri = d
        #
        self.__read_data2frame(self._n_snp_max, d)

    @pyqtSlot(int)
    def on_ndigit_changed(self, n):
        self.ndigit = n
        self.fmt = '{{0:>{0}.{1}f}}'.format(NUM_LENGTH, n)
        self.element_list_changed.emit()

    @pyqtSlot(bool)
    def on_auto_ndigit(self, enabled):
        # if enabled, use .g format
        if enabled:
            self.fmt = '{{0:{0}g}}'.format(self.ndigit)
        else:
            self.fmt = '{{0:>{0}.{1}f}}'.format(NUM_LENGTH, self.ndigit)
        self.element_list_changed.emit()

    @pyqtSlot(int)
    def on_update_rate(self, i):
        # update_rate_cbb index
        self.rate_changed.emit(i)

    def start_auto_update(self):
        # updating independently,
        # _update_mode: 'auto'
        printlog("Executing start_auto_update()...")

    def start_thread_update(self):
        # Update values every *delt* second(s),
        # _update_mode: 'thread'

        if self._tv.model() is None:
            return

        # if self._stop_update_thread:
        #    return

        delt = self._update_delt
        m0 = self._tv.model()
        m = m0.sourceModel()
        try:
            is_finished = self.updater.isFinished()
        except:
            is_finished = True
        if not is_finished:
            return
        self.updater = DAQT(daq_func=partial(self.update_value_single, m, m0,
                                             delt, False),
                            daq_seq=np.inf)
        self.updater.meta_signal1.connect(partial(self.on_update_display, m))
        self.updater.start()

    def _refresh_single(self, m, m0, viewport_only, iter_param, **kws):
        # refresh a single pair of CaField object and items.
        worker = kws.get('worker', self.one_updater)
        o, it = iter_param
        cnt_fld = 0
        idx0 = m.indexFromItem(it[0])  # rd
        if viewport_only and not self.is_idx_visible(m0.mapFromSource(idx0)):
            return cnt_fld
        idx1 = m.indexFromItem(it[1])  # cset
        irow = idx0.row()
        rd_val, sp_val = o.value, o.current_setting()

        #
        if o.name in ('NMR', 'NMR_phy', 'HALL', 'HALL_PROBE'):
            fmt, ndigit = self.fmt_nmr, 5
        else:
            fmt, ndigit = self.fmt, self.ndigit

        # write access
        wa_idx = m.index(irow, m.i_writable)
        wa = ELEM_WRITE_PERM.get(o.ename, o.write_access)
        worker.meta_signal1.emit((wa_idx, str(wa), Qt.DisplayRole))

        name_idx = m.index(irow, m.i_name)
        fname = m.data(m.index(irow, m.i_field))
        if None in (rd_val, sp_val):  # is not reachable
            worker.meta_signal1.emit(
                (name_idx, self.fail_px.scaled(PX_SIZE,
                                               PX_SIZE), Qt.DecorationRole))
            worker.meta_signal1.emit(
                (name_idx, "Device is not connected", Qt.ToolTipRole))
            return cnt_fld
        else:
            # is reachable
            worker.meta_signal1.emit((name_idx, QPixmap(), Qt.DecorationRole))
            worker.meta_signal1.emit(
                (name_idx, "Device is connected", Qt.ToolTipRole))

        x0_idx = m.index(irow, m.i_val0)
        x1_idx = m.index(irow, m.i_rd)
        x2_idx = m.index(irow, m.i_cset)
        tol_idx = m.index(irow, m.i_tol)
        dx01_idx = m.index(irow, m.i_val0_rd)
        dx02_idx = m.index(irow, m.i_val0_cset)
        dx12_idx = m.index(irow, m.i_rd_cset)
        sts_idx = m.index(irow, m.i_sts)
        ratio_x20_idx = m.index(irow, m.i_ratio_x20)
        ref_st_idx = m.index(irow, m.i_ref_st)
        dx2ref_idx = m.index(irow, m.i_dstref)
        dx0ref_idx = m.index(irow, m.i_dval0ref)
        read_alm_idx = m.index(irow, m.i_read_alm)
        tune_alm_idx = m.index(irow, m.i_tune_alm)
        tol_idx = m.index(irow, m.i_tol)

        idx_tuple = (idx0, idx1)
        v_tuple = (rd_val, sp_val)
        for iidx, val in zip(idx_tuple, v_tuple):
            worker.meta_signal1.emit((iidx, fmt.format(val), Qt.DisplayRole))

        x0 = float(m.data(x0_idx))
        x1, x2 = rd_val, sp_val
        dx01 = x0 - x1
        # dx02 = x0 - x2
        dx02 = x2 - x0
        dx12 = x1 - x2
        idx_tuple = (dx01_idx, dx02_idx, dx12_idx)
        v_tuple = (dx01, dx02, dx12)
        for iidx, val in zip(idx_tuple, v_tuple):
            worker.meta_signal1.emit((iidx, fmt.format(val), Qt.DisplayRole))
        worker.meta_signal1.emit(
            (ratio_x20_idx, get_ratio_as_string(x2, x0, fmt), Qt.DisplayRole))

        # tolerance
        tol_pv = m.data(tol_idx, Qt.UserRole + 1)
        tol_v0_str = m.data(tol_idx, Qt.DisplayRole)
        if tol_pv is not None:
            tol_v = tol_pv.value
            if tol_v is not None:
                tol_v_str = fmt.format(tol_v)
                if tol_v_str != tol_v0_str:
                    worker.meta_signal1.emit(
                        (tol_idx, tol_v_str, Qt.DisplayRole))

        tol = float(m.data(tol_idx))
        if abs(dx12) > tol:
            worker.meta_signal1.emit(
                (dx12_idx, self._warning_px, Qt.DecorationRole))
            worker.meta_signal1.emit((dx12_idx, 'warning', Qt.UserRole))
        else:
            worker.meta_signal1.emit(
                (dx12_idx, self._no_warning_px, Qt.DecorationRole))
            worker.meta_signal1.emit((dx12_idx, None, Qt.UserRole))

        if not is_close(x0, x2, ndigit):
            worker.meta_signal1.emit(
                (dx02_idx, self._warning_px, Qt.DecorationRole))
            worker.meta_signal1.emit((dx02_idx, 'warning', Qt.UserRole))
        else:
            worker.meta_signal1.emit(
                (dx02_idx, self._no_warning_px, Qt.DecorationRole))
            worker.meta_signal1.emit((dx02_idx, None, Qt.UserRole))

        if self.show_refset_ctrls_btn.isChecked():
            # ref set value
            ref_st_pv = m.data(ref_st_idx, Qt.UserRole + 1)
            if ref_st_pv is not None:
                ref_v = ref_st_pv.value
                if ref_v is not None:
                    dx2ref = x2 - ref_v
                    dx0ref = x0 - ref_v
                    for iidx, iv in zip((ref_st_idx, dx2ref_idx, dx0ref_idx),
                                        (ref_v, dx2ref, dx0ref)):
                        worker.meta_signal1.emit(
                            (iidx, fmt.format(iv), Qt.DisplayRole))

                    # warnings?
                    for iidx, iv in zip((dx2ref_idx, dx0ref_idx), (x2, x0)):
                        if not is_close(iv, ref_v, ndigit):
                            worker.meta_signal1.emit(
                                (iidx, self._warning_px, Qt.DecorationRole))
                            worker.meta_signal1.emit(
                                (iidx, "warning", Qt.UserRole))
                        else:
                            worker.meta_signal1.emit(
                                (iidx, self._no_warning_px, Qt.DecorationRole))
                            worker.meta_signal1.emit((iidx, None, Qt.UserRole))

        if self.show_alm_ctrls_btn.isChecked():
            # device read alarm switch status
            read_alm_act_pv = m.data(read_alm_idx, Qt.UserRole + 1)
            if read_alm_act_pv is not None:
                read_alm_v = read_alm_act_pv.value
                if read_alm_v == 1.0:
                    worker.meta_signal1.emit(
                        (read_alm_idx, self._alm_enabled_px,
                         Qt.DecorationRole))
                else:
                    worker.meta_signal1.emit(
                        (read_alm_idx, self._alm_disabled_px,
                         Qt.DecorationRole))
                worker.meta_signal1.emit(
                    (read_alm_idx, read_alm_v, Qt.UserRole))

            # device tune alarm switch status
            tune_alm_act_pv = m.data(tune_alm_idx, Qt.UserRole + 1)
            if tune_alm_act_pv is not None:
                tune_alm_v = tune_alm_act_pv.value
                if tune_alm_v == 1.0:
                    worker.meta_signal1.emit(
                        (tune_alm_idx, self._alm_enabled_px,
                         Qt.DecorationRole))
                else:
                    worker.meta_signal1.emit(
                        (tune_alm_idx, self._alm_disabled_px,
                         Qt.DecorationRole))
                worker.meta_signal1.emit(
                    (tune_alm_idx, tune_alm_v, Qt.UserRole))

        # a little higher time cost?
        # elem = self._lat[o.ename]
        # # emit signal to update power status
        # for _i, _r in get_pwr_sts(elem, o.name):
        #     worker.meta_signal1.emit((sts_idx, _i, _r))

        #
        pwr_is_on = 'Unknown'
        px = self._pwr_unknown_px
        tt = "Not a powered device, SRF cavity, nor other blocking devices."
        elem = self._lat[o.ename]
        if elem.family == 'CAV':
            r = re.match(r".*([1-3]+).*", o.name)
            if r is not None:  # D0987
                _fname = 'LKSTS' + r.group(1)
            else:
                _fname = 'LKSTS'
            if _fname in elem.fields:
                pwr_fld = elem.get_field(_fname)
                pwr_is_on = pwr_fld.value
            if pwr_is_on == 1.0:
                px = self._pwr_on_px
                tt = "Cavity phase is LOCKED"
            elif pwr_is_on == 0.0:
                px = self._pwr_off_px
                tt = "Cavity phase is UNLOCKED"

            # emit signal to update power status
            worker.meta_signal1.emit(
                (sts_idx, px.scaled(PX_SIZE, PX_SIZE), Qt.DecorationRole))
            worker.meta_signal1.emit((sts_idx, tt, Qt.ToolTipRole))

        elif elem.family == "CHP":
            sts = elem.get_field('STATE')
            sts_val_int = int(sts.value)
            sts_val_str = CHP_STS_TUPLE[sts_val_int]
            tt = f"Chopper state: {sts_val_str}"
            px = self._chp_px_tuple[sts_val_int]
            worker.meta_signal1.emit(
                (sts_idx, px.scaled(PX_SIZE, PX_SIZE), Qt.DecorationRole))
            worker.meta_signal1.emit((sts_idx, tt, Qt.ToolTipRole))

        elif elem.family == "AP":
            in_sts = elem.IN_STS
            px = self._ap_in_px_tuple[in_sts]
            if in_sts == 0:
                tt = "Aperture device is OUT"
            else:
                tt = "Aperture device is IN"
            worker.meta_signal1.emit(
                (sts_idx, px.scaled(PX_SIZE, PX_SIZE), Qt.DecorationRole))
            worker.meta_signal1.emit((sts_idx, tt, Qt.ToolTipRole))

        elif elem.family == "PM":
            if 'IN_STS' in elem.fields:
                in_sts = elem.IN_STS
                px = self._pm_in_px_tuple[in_sts]
                if in_sts == 0:
                    tt = "PPAC is OUT"
                else:
                    tt = "PPAC is IN"
            worker.meta_signal1.emit(
                (sts_idx, px.scaled(PX_SIZE, PX_SIZE), Qt.DecorationRole))
            worker.meta_signal1.emit((sts_idx, tt, Qt.ToolTipRole))

        elif elem.family == "FOIL":
            if 'IN_STS' in elem.fields:
                in_sts = elem.IN_STS
                px = self._pm_in_px_tuple[in_sts]
                if in_sts == 0:
                    tt = "Foil is OUT"
                else:
                    tt = "Foil is IN"
            worker.meta_signal1.emit(
                (sts_idx, px.scaled(PX_SIZE, PX_SIZE), Qt.DecorationRole))
            worker.meta_signal1.emit((sts_idx, tt, Qt.ToolTipRole))

        elif elem.family == "ION":
            if 'ACT' in elem.fields:
                act_sts = elem.ACT
                if act_sts is not None:
                    px = self._ion_act_px_tuple[int(act_sts)]
                    if act_sts == 0:
                        tt = "Ion source is inactive"
                    else:
                        tt = "Ion source is active"
                else:
                    tt = "Ion source is unknown"
            worker.meta_signal1.emit(
                (sts_idx, px.scaled(PX_SIZE, PX_SIZE), Qt.DecorationRole))
            worker.meta_signal1.emit((sts_idx, tt, Qt.ToolTipRole))

        elif elem.family == "BD":
            if 'IN_STS' in elem.fields:
                in_sts = elem.IN_STS
                px = self._pm_in_px_tuple[in_sts]
                if in_sts == 0:
                    tt = "Beam dump is OUT"
                else:
                    tt = "Beam dump is IN"
            worker.meta_signal1.emit(
                (sts_idx, px.scaled(PX_SIZE, PX_SIZE), Qt.DecorationRole))
            worker.meta_signal1.emit((sts_idx, tt, Qt.ToolTipRole))

        elif elem.family == "ELD":
            if 'IN_STS' in elem.fields:
                in_sts = elem.IN_STS
                px = self._pm_in_px_tuple[in_sts]
                if in_sts == 0:
                    tt = "Energy loss detector is OUT"
                else:
                    tt = "Energy loss detector is IN"
            worker.meta_signal1.emit(
                (sts_idx, px.scaled(PX_SIZE, PX_SIZE), Qt.DecorationRole))
            worker.meta_signal1.emit((sts_idx, tt, Qt.ToolTipRole))

        elif elem.family == "TID":
            if 'IN_STS' in elem.fields:
                in_sts = elem.IN_STS
                px = self._pm_in_px_tuple[in_sts]
                if in_sts == 0:
                    tt = "Timing detector is OUT"
                else:
                    tt = "Timing detector is IN"
            worker.meta_signal1.emit(
                (sts_idx, px.scaled(PX_SIZE, PX_SIZE), Qt.DecorationRole))
            worker.meta_signal1.emit((sts_idx, tt, Qt.ToolTipRole))

        elif elem.family == "PPOT":
            pos = elem.get_field('POS').value
            if elem.name == "FS_F2S1:PPOT_D1563":
                if pos == 0:
                    tt = "DB2 viewer/degrader is OUT"
                    px = self._pwr_on_px  # green
                elif pos == 2:
                    tt = "DB2 Viewer is IN"
                    px = self._pwr_off_px  # red
                elif pos == 3:
                    tt = "DB2 Degrader is IN"
                    px = self._pwr_off_px  # red

            elif elem.name == "FS_F2S2:PPOT_D1660":
                if pos == 0:
                    tt = "DB3 viewer/wedge is OUT"
                    px = self._pwr_on_px  # green
                elif pos == 2:
                    tt = "DB3 Viewer is IN"
                    px = self._pwr_off_px  # red
                elif pos == 3:
                    tt = "DB3 Wedge#1 is IN"
                    px = self._pwr_off_px  # red
                elif pos == 4:
                    tt = "DB3 Wedge#2 is IN"
                    px = self._pwr_off_px  # red
                elif pos == 5:
                    tt = "DB3 Wedge#3 is IN"
                    px = self._pwr_off_px  # red

            worker.meta_signal1.emit(
                (sts_idx, px.scaled(PX_SIZE, PX_SIZE), Qt.DecorationRole))
            worker.meta_signal1.emit((sts_idx, tt, Qt.ToolTipRole))

        elif elem.family == "ATT":
            if 'OUT_STS' in elem.fields:
                out_sts = elem.OUT_STS
                px = self._att_out_px_tuple[out_sts]
                if out_sts == 0:
                    tt = "Attenuator device is IN"
                else:
                    tt = "Attenuator device is OUT"
            elif 'ATT_TOTAL' in elem.fields:
                att_val = elem.ATT_TOTAL
                if att_val > 1:
                    px = self._att_out_px_tuple[0]
                    tt = "Attenuator(s) IN"
                else:
                    px = self._att_out_px_tuple[1]
                    tt = "Attenuator(s) OUT"
            worker.meta_signal1.emit(
                (sts_idx, px.scaled(PX_SIZE, PX_SIZE), Qt.DecorationRole))
            worker.meta_signal1.emit((sts_idx, tt, Qt.ToolTipRole))

        elif elem.family == "PTA":
            sts = elem.get_field('TGT')
            sts_val_int = sts.value
            sts_val_str = TGT_STS_TUPLE[sts_val_int]
            tt = f"Target state: {sts_val_str}"
            worker.meta_signal1.emit((sts_idx, sts_val_str, Qt.DisplayRole))
            worker.meta_signal1.emit((sts_idx, tt, Qt.ToolTipRole))

        elif elem.family == "SLT":
            if 'IN_STS' in elem.fields:
                in_sts = elem.IN_STS
                px = self._pm_in_px_tuple[in_sts]
                if in_sts == 0:
                    tt = "Slit is OUT"
                else:
                    tt = "Slit is IN"
            worker.meta_signal1.emit(
                (sts_idx, px.scaled(PX_SIZE, PX_SIZE), Qt.DecorationRole))
            worker.meta_signal1.emit((sts_idx, tt, Qt.ToolTipRole))

        else:  # others
            if 'PWRSTS' in elem.fields:
                if fname == 'I_TC':
                    pwr_fname = 'PWRSTS_TC'
                else:
                    pwr_fname = 'PWRSTS'

                pwr_fld = elem.get_field(pwr_fname)
                pwr_is_on = pwr_fld.value

                if pwr_is_on == 1.0:
                    px = self._pwr_on_px
                    tt = "Power is ON"
                elif pwr_is_on == 0.0:
                    px = self._pwr_off_px
                    tt = "Power is OFF"

            # emit signal to update power status
            worker.meta_signal1.emit(
                (sts_idx, px.scaled(PX_SIZE, PX_SIZE), Qt.DecorationRole))
            worker.meta_signal1.emit((sts_idx, tt, Qt.ToolTipRole))

        # u of pwr sts
        _, _u = STS_PX_MAP.get(tt)
        worker.meta_signal1.emit((sts_idx, _u, PWR_STS_U_ROLE))

        #
        cnt_fld += 1
        return cnt_fld

    def update_value_single(self, m, m0, delt, viewport_only, iiter):
        # update data tree for one time, iterate all items.

        #
        m0 = self._tv.model()
        if m0 is None:
            return
        m = m0.sourceModel()
        print(len(self.obj_it_tuple))
        #

        if delt == -1:
            worker = self._updater
        else:
            worker = self.updater
        t0 = time.time()
        cnt_fld = 0
        # if self._filter_btn_enabled:  # force iterate all if any (3) filter btn is on
        #    viewport_only = False
        for o, it in zip(m._fld_obj, m._fld_it):
            _cnt_fld = self._refresh_single(m,
                                            m0,
                                            viewport_only, (o, it),
                                            worker=worker)
            cnt_fld += _cnt_fld

        dt = time.time() - t0
        dt_residual = delt - dt
        # data is refreshed
        self.last_refreshed.emit()
        if delt == 0:
            printlog("Single update in {0:.1f} msec, no wait.".format(dt *
                                                                      1000))
        else:
            printlog("Refreshed data.")
            if dt_residual > 0:
                time.sleep(dt_residual)
                printlog("Waited {0:.0f} msec (Field: {1}).".format(
                    dt_residual * 1000, cnt_fld))
            else:
                printlog("Rate is {0:.1f} Hz (Field: {1}).".format(
                    1.0 / dt, cnt_fld))

    @pyqtSlot(bool)
    def on_toggle_update_btn(self, f):
        """Toggle update rate control.
        """
        if f:
            self.start_update()
        else:
            self.stop_update()

    def start_update(self):
        if self._update_mode == 'auto':
            self.start_auto_update()
            printlog("Start auto updating.")
        else:
            self._stop_update_thread = False
            self.start_thread_update()
            printlog("Start thread updating.")

    def stop_update(self):
        if self._update_mode == 'thread':
            self._stop_update_thread = True
            try:
                self.updater.requestInterruption()
            except:
                pass
            printlog("Stop thread updating.")
        else:
            printlog("Stop auto updating.")

    @pyqtSlot()
    def on_snp_expand(self, expanded):
        if expanded:
            self.snp_treeView.expandAll()
        else:
            self.snp_treeView.collapseAll()

    @pyqtSlot()
    def on_select(self, mode, checked=None):
        if mode == 'all':
            # select all
            self._tv.model().select_all(checked)
        else:
            # invert selection
            self._tv.model().invert_selection()

    @pyqtSlot()
    def on_remove_selected_settings(self):
        """Remove selected (checked) settings items from view.
        """
        self._tv.model().sourceModel().delete_selected_items.emit()
        self.filter_lineEdit.editingFinished.emit()

    def on_device_selected(self, selections):
        # Selected elements/fields
        self._elem_selected = selections

    @pyqtSlot()
    def on_add_devices(self):
        # Add devices, high-level fields or PV elements.
        if self._elem_select_dlg is None:
            self._elem_select_dlg = ElementSelectDialog(self,
                                                        "multi",
                                                        mp=self._mp)
            self._elem_select_dlg.pv_mode_radiobtn.setEnabled(False)
            self._elem_select_dlg.elem_mode_radiobtn.setChecked(True)
            self._elem_select_dlg.selection_changed.connect(
                self.on_device_selected)
            self.lattice_loaded.connect(
                self._elem_select_dlg.on_update_elem_tree)

        r = self._elem_select_dlg.exec_()
        if r == QDialog.Accepted:
            sel_elems, sel_elems_dis, sel_fields = self._elem_selected
            is_added_list = []
            for i in sel_elems_dis:
                self._lat.append(i)
                is_added_list.append(self.add_element(i))
            is_added = True in is_added_list
            if is_added:
                self.element_list_changed.emit()

    def add_element(self, elem):
        """Add *elem* to element list if not added.
        """
        if elem not in self._elem_list:
            self._elem_list.append(elem)
            return True
        else:
            return False

    @pyqtSlot(QVariant)
    def on_update_display(self, m, res):
        """Update variable display variables for one row, when data are ready.
        """
        # m.data_changed.emit(res)
        m.update_data(res)

    def is_idx_visible(self, idx):
        #
        # test if current row is visible in current viewport
        #
        viewport_rect = self._tv.viewport().rect()
        rect = self._tv.visualRect(idx)
        if not viewport_rect.contains(rect):
            return False
        if not rect.isValid():
            return False
        # print(f"- ({idx.row()}, {idx.column()}), {rect.x(), rect.y(), rect.width(), rect.height()}")
        return True

    def on_click_test_btn(self):
        # debug
        # list all rows currently are in the viewport
        #
        if self._tv.model() is None:
            return
        m = self._tv.model()
        m_src = m.sourceModel()
        # print("=" * 20)
        for i in range(m.rowCount()):
            idx = m.index(i, 0)
            is_visible = self.is_idx_visible(idx)
            if not is_visible:
                continue
            idx_src = m.mapToSource(idx)
            it_src = m_src.itemFromIndex(idx_src)
        #    print(f"-- Item in source model: {it_src.text()}, index: ({idx_src.row()}, {idx_src.column()})")
        # print("=" * 20)

    @pyqtSlot()
    def on_pull_data(self):
        """Pull data from dataframe.
        """
        w_list = (self.nsnp_btn, self.snp_refresh_btn, self.ops_bound_cbb)

        def _on_pull_data_one(iiter):
            idx, irow = iiter
            return read_data(irow, 'sql')

        def _on_db_pull_started():
            [o.setEnabled(False) for o in w_list]
            self.db_pull_pb.setRange(0, 100)
            self.db_pull_pb.setVisible(True)
            self._task_list.append('Presenting snapshots...')
            self._splash_msg_undone()

        def _on_db_pull_progressed(f, s):
            self.db_pull_pb.setValue(int(f * 100))

        def _on_db_pull_finished():
            self.db_pull_pb.setRange(0, 0)
            self.db_pull_pb.setVisible(False)
            task_name = "Presenting snapshots..."
            self._task_list.remove(task_name)
            self._splash_msg("Snapshots are ready to use.")
            self._splash_msg_undone()
            [o.setEnabled(True) for o in w_list]

        def _on_db_pull_resultsReady(res):
            self._snp_dock_list = [i for i in res if i is not None]
            n = len(self._snp_dock_list)
            self.total_snp_lbl.setText(str(n))
            self.update_snp_dock_view()
            # current snp
            if self._current_snpdata is not None:
                self.snp_loaded.emit(self._current_snpdata)
            self.snp_filters_updated.emit()
            printlog("DB puller is done...")

        self._db_puller = DAQT(daq_func=_on_pull_data_one,
                               daq_seq=self.df_all_row_tuple)
        self._db_puller.daqStarted.connect(_on_db_pull_started)
        self._db_puller.progressUpdated.connect(_on_db_pull_progressed)
        self._db_puller.resultsReady.connect(_on_db_pull_resultsReady)
        self._db_puller.daqFinished.connect(_on_db_pull_finished)
        self._db_puller.start()

    @pyqtSlot()
    def on_single_update(self):
        """Update values, indicators for one time."""
        if self._tv.model() is None:
            return
        m0 = self._tv.model()
        m = m0.sourceModel()
        try:
            is_finished = self.one_updater.isFinished()
        except:
            is_finished = True
        if not is_finished:
            return
        self.one_updater = DAQT(daq_func=partial(self._refresh_single, m, m0,
                                                 False),
                                daq_seq=self.obj_it_tuple,
                                nproc=2)
        self.one_updater.meta_signal1.connect(
            partial(self.on_update_display, m))
        #        self.one_updater.daqStarted.connect(lambda:printlog("Refreshing data..."))
        self.one_updater.daqStarted.connect(
            lambda: self.refresh_beat_lbl.setVisible(True))
        self.one_updater.daqStarted.connect(lambda: m.blockSignals(True))
        self.one_updater.daqFinished.connect(
            lambda: self.refresh_beat_lbl.setVisible(False))
        self.one_updater.daqFinished.connect(lambda: m.blockSignals(False))
        self.one_updater.daqFinished.connect(m._finish_update)
        self.one_updater.daqFinished.connect(self.last_refreshed)
        #        self.one_updater.daqFinished.connect(lambda:printlog("Refreshing data...done!"))
        self.one_updater.start()

    def on_data_refresh_done(self):
        # reset updater
        self.one_updater = None
        #
        self.set_last_data_refreshed_info_visible(True)
        # Data refreshing is done (before any waiting): update the last updated timestamp.
        ts = datetime.now().strftime("%Y-%m-%d %T")
        self.last_refreshed_lbl.setText(ts)
        # add log message
        # msg = "[{0}]: Data is refreshed.".format(
        #     datetime.fromtimestamp(time.time()).strftime(TS_FMT))
        # self.log_textEdit.append(msg)

    def set_widgets_status_for_updating(self, status, is_single=True):
        """Set widgets status for updating.
        """
        w1 = [
            self.update_rate_cbb, self.apply_btn, self.select_all_btn,
            self.deselect_all_btn, self.invert_selection_btn,
            self.single_update_btn, self.auto_ndigit_chkbox
        ]
        if is_single:
            w1.append(self.update_ctrl_btn)
            w1.append(self.snp_dock)
        [i.setDisabled(status == 'START') for i in w1]
        # auto ndigit
        for o in (self.ndigit_sbox, self.ndigit_lbl):
            o.setDisabled(status == 'START'
                          or self.auto_ndigit_chkbox.isChecked())

    def set_widgets_status_for_applying(self, status):
        """Set widgets status for applying.
        """
        w1 = (self.apply_btn, )
        [i.setDisabled(status == 'START') for i in w1]

    def set_widgets_status_for_ref_set(self, status):
        """Set widgets status for ref set.
        """
        w1 = (self.update_ref_btn, )
        [i.setDisabled(status == 'START') for i in w1]

    def sizeHint(self):
        return QSize(1920, 1440)

    @pyqtSlot(list)
    def on_delete_items(self, fobj_list):
        """Delete the element(s) from element list by given field object list.
        """
        for fobj in fobj_list:
            elem = self._lat[fobj.ename]
            # !! note: delete both ENG/PHY fields even if any one of ENG/PHY is deleted.
            if elem in self._elem_list:
                self._elem_list.remove(elem)
        self.element_list_changed.emit()

    @pyqtSlot(bool)
    def on_toggle_all_selected(self, selected):
        # disable 'Uncheck All' button: uncheck/check is applied one by one,
        # which will trigger filter updating, to cause confused behavior, when this filter button
        # is toggled, it is reasonable to disable the Uncheck All button.
        m = self._tv.model()
        if m is None:
            return
        self.deselect_all_btn.setEnabled(not selected)
        m.filter_checked_enabled = selected
        self.filter_lineEdit.editingFinished.emit()

    @pyqtSlot(bool)
    def on_show_warning_dx12(self, is_checked):
        # show all items with dx12 > tolerance
        self.filter_btn_group_status_changed.emit()
        m = self._tv.model()
        if m is None:
            return
        m.filter_dx12_warning_enabled = is_checked
        self.filter_lineEdit.editingFinished.emit()

    @pyqtSlot(bool)
    def on_show_warning_dx02(self, is_checked):
        # show all items with dx02 > tolerance
        self.filter_btn_group_status_changed.emit()
        m = self._tv.model()
        if m is None:
            return
        m.filter_dx02_warning_enabled = is_checked
        self.filter_lineEdit.editingFinished.emit()

    @pyqtSlot(bool)
    def on_show_warning_dx0ref(self, is_checked):
        # show all items with ref_st != x0
        self.filter_btn_group_status_changed.emit()
        m = self._tv.model()
        if m is None:
            return
        m.filter_dx0ref_warning_enabled = is_checked
        self.filter_lineEdit.editingFinished.emit()

    @pyqtSlot(bool)
    def on_show_warning_dx2ref(self, is_checked):
        # show all items with ref_st != x2
        self.filter_btn_group_status_changed.emit()
        m = self._tv.model()
        if m is None:
            return
        m.filter_dx2ref_warning_enabled = is_checked
        self.filter_lineEdit.editingFinished.emit()

    @pyqtSlot(bool)
    def on_show_disconnected_items(self, is_checked):
        # show all items that are not reachable
        self.filter_btn_group_status_changed.emit()
        m = self._tv.model()
        if m is None:
            return
        m.filter_disconnected_enabled = is_checked
        self.filter_lineEdit.editingFinished.emit()

    @pyqtSlot(bool)
    def on_show_disabled_read_alms(self, is_checked):
        # show all items that read alarm is disabled
        self.filter_btn_group_status_changed.emit()
        m = self._tv.model()
        if m is None:
            return
        m.filter_disabled_read_alm_enabled = is_checked
        self.filter_lineEdit.editingFinished.emit()

    @pyqtSlot(bool)
    def on_show_disabled_tune_alms(self, is_checked):
        # show all items that tune alarm is disabled
        self.filter_btn_group_status_changed.emit()
        m = self._tv.model()
        if m is None:
            return
        m.filter_disabled_tune_alm_enabled = is_checked
        self.filter_lineEdit.editingFinished.emit()

    @pyqtSlot(bool)
    def on_show_enabled_read_alms(self, is_checked):
        # show all items that read alarm is enabled
        self.filter_btn_group_status_changed.emit()
        m = self._tv.model()
        if m is None:
            return
        m.filter_enabled_read_alm_enabled = is_checked
        self.filter_lineEdit.editingFinished.emit()

    @pyqtSlot(bool)
    def on_show_enabled_tune_alms(self, is_checked):
        # show all items that tune alarm is enabled
        self.filter_btn_group_status_changed.emit()
        m = self._tv.model()
        if m is None:
            return
        m.filter_enabled_tune_alm_enabled = is_checked
        self.filter_lineEdit.editingFinished.emit()

    @pyqtSlot(bool)
    def on_show_state_diff_items(self, is_checked):
        # show all items that have different state and last_state values
        self.filter_btn_group_status_changed.emit()
        m = self._tv.model()
        if m is None:
            return
        m.filter_state_diff_enabled = is_checked
        self.filter_lineEdit.editingFinished.emit()

    @pyqtSlot(bool)
    def on_show_live_state_on_items(self, is_checked: bool):
        # show all item that live state is on (green)
        self.filter_btn_group_status_changed.emit()
        m = self._tv.model()
        if m is None:
            return
        m.filter_live_state_on_enabled = is_checked
        self.filter_lineEdit.editingFinished.emit()

    @pyqtSlot(bool)
    def on_show_live_state_off_items(self, is_checked: bool):
        # show all item that live state is off (ref)
        self.filter_btn_group_status_changed.emit()
        m = self._tv.model()
        if m is None:
            return
        m.filter_live_state_off_enabled = is_checked
        self.filter_lineEdit.editingFinished.emit()

    @pyqtSlot(bool)
    def on_toggle_pos1_filter_btn(self, is_checked):
        # show all item sb <= pos
        #
        m = self._tv.model()
        if m is None:
            return
        m.filter_pos1_enabled = is_checked
        m.filter_pos_value = self.pos_dspin.value()
        self.filter_lineEdit.editingFinished.emit()

    @pyqtSlot(bool)
    def on_toggle_pos2_filter_btn(self, is_checked):
        # show all item sb > pos
        #
        m = self._tv.model()
        if m is None:
            return
        m.filter_pos2_enabled = is_checked
        m.filter_pos_value = self.pos_dspin.value()
        self.filter_lineEdit.editingFinished.emit()

    def update_pos_dspin_tooltip(self, v):
        self.pos1_filter_btn.setToolTip(
            f"Filter devices locating before (<=) {v} m.")
        self.pos2_filter_btn.setToolTip(
            f"Filter devices locating after (>) {v} m.")

    def refresh_filter_btns(self, snpdata):
        for btn in (self.show_warning_dx02_btn, self.show_warning_dx12_btn,
                    self.show_state_diff_btn, self.show_live_sts_off_btn,
                    self.show_live_sts_on_btn):
            btn.toggled.emit(btn.isChecked())

    def on_update_pos_filter(self, snpdata):
        self.pos_filter_btn.toggled.emit(self.pos_filter_btn.isChecked())
        self.pos_dspin.valueChanged.emit(self.pos_dspin.value())

    def post_snp_info(self, snpdata):
        self.set_post_snp_info_visible(True)
        info_text = f"Snapshot: {snpdata.ts_as_str()}, {snpdata.ion_as_str()}"
        ts_text = f"Loaded at {datetime.now().strftime('%Y-%m-%d %T')}"
        self.loaded_snp_info_lbl.setText(info_text)
        self.loaded_snp_ts_lbl.setText(ts_text)
        self.set_loaded_snp_note_lbl(snpdata.note)

    def set_loaded_snp_note_lbl(self, full_note_text: str):
        note_lbl = self.loaded_snp_note_lbl
        note_text = QFontMetrics(note_lbl.font()).elidedText(
            full_note_text, Qt.ElideRight, note_lbl.width())
        note_lbl.setText(note_text)
        note_lbl.setToolTip(full_note_text)

    def update_loaded_snp_info(self, snpdata):
        """Update loaded snapshot info if any metadata of the snapshot data is changed.
        """
        if self._current_snpdata is None:
            print("Warning: No snapshot is loaded.")
            return
        if snpdata.name == self._current_snpdata.name:
            # update note string if Note is updated.
            note_str_now = self.loaded_snp_note_lbl.text()
            if snpdata.note != note_str_now:
                self.set_loaded_snp_note_lbl(snpdata.note)

    def set_post_snp_info_visible(self, visibility):
        [
            o.setVisible(visibility)
            for o in (self.loaded_snp_info_lbl, self.loaded_snp_ts_lbl,
                      self.loaded_snp_note_lbl, self.orig_template_info_frame)
        ]

    def set_last_data_refreshed_info_visible(self, visibility):
        [
            o.setVisible(visibility)
            for o in (self.last_refreshed_lbl, self.last_refreshed_title_lbl)
        ]

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        urls = e.mimeData().urls()
        for url in urls:
            path = url.toLocalFile()
            snp_data = read_data(pathlib.Path(path))
            if snp_data is None:
                QMessageBox.warning(self, "Load Snapshot",
                                    "Cannot load the file.", QMessageBox.Ok,
                                    QMessageBox.Ok)
                return
            if not is_snp_data_exist(snp_data, self._snp_dock_list):
                self._snp_dock_list.append(snp_data)
        self.update_snp_dock_view()
        self.on_load_settings(snp_data)
        n = len(self._snp_dock_list)
        self.total_snp_lbl.setText(str(n))
        # save into db by default
        self.on_save_settings(snp_data)

    @pyqtSlot(int, bool)
    def on_update_visibility(self, idx, f):
        self._tv.setColumnHidden(idx, f)

    def turn_off_updater_if_necessary(self):
        # obsoleted.
        # This is not safe, to be improved!!!
        if self.update_ctrl_btn.isChecked():
            self.update_ctrl_btn.setChecked(False)
            milli_sleep(100)

    def take_snapshot(self,
                      cast=True,
                      only_checked_items=False,
                      post_current_sp=True):
        # take but not cast (show in the settings view) for only checked items or not.
        # cast: if cast snapshot or not
        # only_checked_items: if take snapshot of checked items or not
        # post_current_sp: if update x0 with x2 column or not
        m = self._tv.model()
        if m is None:
            return

        def _onSnapshotTaken(snp_data: SnapshotData, to_load: bool):
            self._snp_dock_list.append(snp_data)
            n = len(self._snp_dock_list)
            self.total_snp_lbl.setText(str(n))
            self.update_snp_dock_view()
            self.snp_filters_updated.emit()
            self.on_save_settings(snp_data)
            if to_load:
                self.on_load_settings(snp_data)

        # pop up a dialog for tag selection
        postsnp_dlg = PostSnapshotDialog(
            self.default_font_size, self.snp_template_list,
            self._current_snpdata_originated,
            self.pref_dict['MACH_STATE']['ENABLED'], self)
        postsnp_dlg.snapshotTaken.connect(_onSnapshotTaken)
        postsnp_dlg.exec_()

    @pyqtSlot()
    def on_show_query_tips(self):
        if self._query_tips_form is None:
            self._query_tips_form = w = QWidget()
            ui = QueryTipsForm()
            ui.setupUi(w)
            w.setWindowTitle("Query Tips")
        self._query_tips_form.show()

    @pyqtSlot()
    def on_copy_snp(self, data):
        data.extract_blob()
        data.data.to_clipboard(excel=True, index=False)
        msg = '<html><head/><body><p><span style="color:#007BFF;">Copied snapshot data at: </span><span style="color:#DC3545;">{}</span></p></body></html>'.format(
            data.ts_as_str())
        self.statusInfoChanged.emit(msg)
        self._reset_status_info()

    @pyqtSlot()
    def on_read_snp(self, data):
        data.extract_blob()
        _, filename = tempfile.mkstemp('.xlsx')
        self._save_settings(data, filename, 'xlsx')
        QDesktopServices.openUrl(QUrl(filename))

    @pyqtSlot()
    def on_mviz(self, data):
        """Visualize machine state data
        """
        data.extract_blob()
        if data.machstate is None:
            QMessageBox.warning(self, "Machine State Data",
                                "No machine state data to show.",
                                QMessageBox.Ok)
            return
        else:
            # groups = ('traj-x', 'traj-y', 'phase', 'energy')
            groups = ('BPM-X', 'BPM-Y', 'BPM-PHA', 'BPM-MAG')
            self._bpmviz_w = BPMVizWidget(data.machstate,
                                          self._machstate,
                                          groups=groups)
            self._bpmviz_w.show()

    def on_snp_filters_updated(self):
        # update snp btn filters
        self.update_snp_btn_filters()
        # apply filter
        self.apply_snp_btn_filters()
        self.snp_expand_btn.clicked.emit()

    def update_snp_btn_filters(self):
        ion_btn_filters = {}  # {ion_name: {A: {Q1,Q2...}}, ...}
        tag_btn_filters = set()
        user_filters = set()
        d = None
        for data in self._snp_dock_list:
            d = ion_btn_filters.setdefault(data.ion_name, {})
            d.setdefault(data.ion_mass, set()).add(data.ion_charge)
            if data.tags == []:
                tag_btn_filters.add('NOTAG')
            else:
                tag_btn_filters.update(data.tags)
            user_filters.add(data.user)
        del d
        _ion_btn_filters = OrderedDict(
            sorted(ion_btn_filters.items(), key=lambda i: _sym2z(i[0])))
        self._build_btn_filters(self.ion_filter_area, _ion_btn_filters)
        self._build_tag_filters(self.tag_filter_area, tag_btn_filters)
        # dropdown menu for checkable user names.
        self._build_user_filters(self.snp_filter_ctrls_hbox, user_filters)

    def _build_user_filters(self, container, filters):
        # dropdown menu with checkable user names
        #
        child = container.takeAt(0)
        while child:
            w = child.widget()
            if w is not None:
                w.setParent(None)
            del w
            del child
            child = container.takeAt(0)
        #
        filters = sorted(filters)
        _d = {i: True for i in filters}

        #
        def _on_update_filter_string(k, btn, is_toggled):
            if k == 'All':  # update checkstates for other actions
                btn.toggled.disconnect()
                for obj in self.sender().parent().findChildren(QCheckBox):
                    obj.setChecked(is_toggled)
                btn.toggled.connect(partial(_on_toggle_filter_btn, btn))
            else:
                _d[k] = is_toggled
                obj = self.sender().parent().findChild(QCheckBox,
                                                       "sel_user_act")
                obj.toggled.disconnect()
                obj.setChecked(all(_d.values()))
                obj.toggled.connect(
                    partial(_on_update_filter_string, 'All', btn))

            btn.setToolTip(
                "Check to enable filtering by {}\nChecked: {}".format(
                    'User', ','.join([k for k, v in _d.items() if v])))
            btn.toggled.emit(btn.isChecked())

        #
        def _on_toggle_filter_btn(btn, is_checked):
            m = self.snp_treeView.model()
            if m is None:
                return
            m.filter_user_enabled = is_checked
            m.filter_user_list = [k for k, v in _d.items() if v]
            m.invalidate()
            self.snp_expand_btn.clicked.emit()

        def _create_widgetaction(text, parent):
            _chkbox = QCheckBox(text, parent)
            _chkbox.setChecked(True)
            _wa = QWidgetAction(parent)
            _wa.setDefaultWidget(_chkbox)
            _chkbox.setStyleSheet("""QCheckBox{padding-left:10px;}""")
            return _chkbox, _wa

        def _build_actions(btn):
            menu = QMenu(self)
            for i in filters:
                _chkbox, _wa = _create_widgetaction(i, menu)
                _chkbox.toggled.connect(
                    partial(_on_update_filter_string, i, btn))
                menu.addAction(_wa)
            menu.addSeparator()
            _chkbox_all, _wa_all = _create_widgetaction('All', menu)
            _chkbox_all.setObjectName("sel_user_act")
            _chkbox_all.toggled.connect(
                partial(_on_update_filter_string, 'All', btn))
            menu.addAction(_wa_all)
            btn.setMenu(menu)

        #
        _btn = QToolButton(self)
        _btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        _btn.setText("User")
        _btn.setCheckable(True)
        _btn.setToolTip("Filter by User")
        _btn.setIcon(QIcon(QPixmap(":/sm-icons/person.png")))
        _btn.setIconSize(QSize(PX_SIZE, PX_SIZE))
        _btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        _btn.setPopupMode(QToolButton.MenuButtonPopup)
        _btn.toggled.connect(partial(_on_toggle_filter_btn, _btn))
        #
        container.addWidget(_btn)
        _build_actions(_btn)

    def _build_tag_filters(self, area, filters):
        w = area.takeWidget()
        w.setParent(None)
        w = QWidget(self)
        w.setContentsMargins(0, 6, 0, 0)
        layout = FlowLayout()
        if 'NOTAG' in filters:
            filters.remove('NOTAG')
            _filters = ['NOTAG'] + sorted(list(filters))
        else:
            _filters = sorted(list(filters))
        for tag in _filters:
            o = QToolButton(self.snp_dock)
            o.setText(tag)
            o.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            o.setStyleSheet(TAG_BTN_STY.format(fs=self.default_font_size - 1))
            o.setCheckable(True)
            o.toggled.connect(partial(self.on_update_tag_filters, tag))
            layout.addWidget(o)
            o.setChecked(self._current_tag_filter.get(tag, True))
            if tag == 'ARCHIVE':  # not show ARCHIVEd snapshots
                o.setChecked(False)
        w.setLayout(layout)
        area.setWidget(w)

    @pyqtSlot(bool)
    def on_update_tag_filters(self, tag, is_checked):
        # printlog(f"{tag} button filter is {is_checked}")
        self._current_tag_filter[tag] = is_checked
        self.apply_snp_btn_filters()

    def _build_btn_filters(self, area, filters):
        w = area.takeWidget()
        w.setParent(None)
        w = QWidget(self)
        w.setContentsMargins(0, 6, 0, 0)
        layout = FlowLayout()
        for k, v in filters.items():
            # k: ion name, v: {A: {Q...}}
            btn = QToolButton(self.snp_dock)
            btn.setText(k)
            px_tuple = ELEMT_PX_MAP.get(k, None)
            if px_tuple is not None:
                icon = QIcon()
                for pi, st in zip(px_tuple, (QIcon.On, QIcon.Off)):
                    icon.addPixmap(QPixmap(pi), QIcon.Normal, st)
                btn.setIcon(icon)
                btn.setIconSize(QSize(ION_ICON_SIZE, ION_ICON_SIZE))
            else:
                size = QSize(ION_ICON_SIZE, ION_ICON_SIZE)
                px = QPixmap(size)
                px.fill(QColor(255, 255, 255, 0))
                pt = QPainter(px)
                ft = pt.font()
                ft.setPointSize(ft.pointSize() + 2)
                pt.setFont(ft)
                pt.drawText(QRect(0, 0, ION_ICON_SIZE, ION_ICON_SIZE),
                            Qt.AlignCenter, k)
                pt.end()
                btn.setIcon(QIcon(px))
                btn.setIconSize(size)

            btn.setCheckable(True)
            btn.toggled.connect(partial(self.on_update_snp_filters, k))
            layout.addWidget(btn)
            btn.setChecked(self._current_btn_filter.get(k, True))
        w.setLayout(layout)
        area.setWidget(w)

    def apply_snp_btn_filters(self):
        # ion, tag
        m = self.snp_treeView.model()
        m.m_src.set_ion_filters(self._current_btn_filter)
        m.m_src.set_tag_filters(self._current_tag_filter)
        m.reset_cache()
        m.invalidate()
        self.snp_expand_btn.clicked.emit()
        # ion cnt
        ion_cnt = self.snp_treeView.model().m_src._ion_filter_cnt
        layouts = self.ion_filter_area.findChildren(FlowLayout)
        if layouts == []:
            return
        layout = layouts[0]
        for i in range(layout.count()):
            w = layout.itemAt(i).widget()
            if w is None:
                continue
            k = w.text()
            w.setToolTip(f"Hit {ion_cnt[w.text()]} entries of {k}.")
        # tag cnt
        tag_cnt = self.snp_treeView.model().m_src._tag_filter_cnt
        layouts = self.tag_filter_area.findChildren(FlowLayout)
        if layouts == []:
            return
        layout = layouts[0]
        for i in range(layout.count()):
            w = layout.itemAt(i).widget()
            if w is None:
                continue
            if w.text() == '':
                k = ''
            else:
                k = w.text().split(' ')[0]
            w.setText(f"{k} ({tag_cnt[k]})")

    @pyqtSlot(bool)
    def on_update_snp_filters(self, text, is_checked):
        self._current_btn_filter[text] = is_checked
        self.apply_snp_btn_filters()

    def update_snp_dock_view(self):
        m = SnapshotDataModel(self.snp_treeView, self._snp_dock_list)
        m.set_model()
        m.save_settings.connect(self.on_save_settings)
        m.save_settings.connect(
            self.snp_filters_updated)  # update dynamic filter buttons (tag)
        m.save_settings.connect(self.update_loaded_snp_info)

    def on_snp_filter_date_range_updated(self):
        """Filter snapshots by data range
        """
        if not self.snp_date_range_filter_enabled:
            return
        m = self.snp_treeView.model()
        if m is None:
            return
        m.filter_date_enabled = self.snp_date_range_filter_enabled
        self._apply_snp_date_range_filter(m)
        self.snp_expand_btn.clicked.emit()

    def _apply_snp_date_range_filter(self, m):
        _d1 = self.dateEdit1.date()
        _d2 = self.dateEdit2.date()
        date1 = datetime.strptime(_d1.toString("yyyy-MM-dd"), "%Y-%m-%d")
        date2 = datetime.strptime(_d2.toString("yyyy-MM-dd"), "%Y-%m-%d")
        if date1 > date2:
            date1, date2 = date2, date1
        m.filter_date_tuple = (date1, date2)
        m.invalidate()

    @pyqtSlot()
    def on_select_daterange(self):
        if self._date_range_dlg is None:
            self._date_range_dlg = DateRangeDialog()
            self._date_range_dlg.dateFromChanged.connect(
                self.dateEdit1.setDate)
            self._date_range_dlg.dateToChanged.connect(self.dateEdit2.setDate)
        self._date_range_dlg.show()

    def _apply_snp_note_filter(self, m):
        m.filter_note_string = f"*{self.snp_note_filter_lineEdit.text().strip()}*"
        m.invalidate()

    @pyqtSlot(bool)
    def on_toggle_snp_filter_date_range(self, is_checked):
        """Enable/disable snp date range filter.
        """
        self.snp_date_range_filter_enabled = is_checked
        if is_checked:
            self.on_snp_filter_date_range_updated()
        else:
            m = self.snp_treeView.model()
            if m is None:
                return
            m.filter_date_enabled = is_checked
            m.invalidate()

    def on_snp_filter_note_updated(self):
        """Filter snapshots by note string.
        """
        if not self.snp_note_filter_enabled:
            return
        m = self.snp_treeView.model()
        if m is None:
            return
        m.filter_note_enabled = self.snp_note_filter_enabled
        self._apply_snp_note_filter(m)
        self.snp_expand_btn.clicked.emit()

    @pyqtSlot(bool)
    def on_toggle_snp_filter_note(self, is_checked):
        """Enable/disable snp note filter.
        """
        self.snp_note_filter_enabled = is_checked
        if is_checked:
            self.on_snp_filter_note_updated()
        else:
            m = self.snp_treeView.model()
            if m is None:
                return
            m.filter_note_enabled = is_checked
            m.invalidate()

    def on_del_settings(self, data):
        # delete from MEM (done), and model, and datafile (if exists)
        r = QMessageBox.warning(
            None, "Delete Snapshot",
            f"Are you sure to delete the snapshot created at {data.ts_as_str()}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if r == QMessageBox.No:
            return
        for i, d in enumerate(self._snp_dock_list):
            if d.name == data.name:
                data_to_del = self._snp_dock_list.pop(i)
                break
        #
        m = self.snp_treeView.model().m_src
        m.remove_data(data_to_del)

        # override tags with 'ARCHIVE'
        data_to_del.tags = 'ARCHIVE'
        self.on_save_settings(data_to_del)

        self.total_snp_lbl.setText(str(len(self._snp_dock_list)))
        del data_to_del

    def on_del_settings_admin(self, data):
        # delete from MEM (done), and model, and datafile (if exists)
        r = QMessageBox.warning(
            None, "Delete Snapshot",
            f"Are you sure to delete the snapshot created at {data.ts_as_str()}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if r == QMessageBox.No:
            return
        for i, d in enumerate(self._snp_dock_list):
            if d.name == data.name:
                data_to_del = self._snp_dock_list.pop(i)
                break
        #
        m = self.snp_treeView.model().m_src
        m.remove_data(data_to_del)

        # delete from DB
        delete_data(self._db_conn_pool.get(self.data_uri), data)
        self.total_snp_lbl.setText(str(len(self._snp_dock_list)))
        del data_to_del

    def on_save_settings(self, data):
        # in-place save data to data_path.
        data.extract_blob()
        # add new entry to database
        insert_update_data(self._db_conn_pool.get(self.data_uri), data)

    def on_saveas_settings(self, data):
        # data: SnapshotData
        # settings(data.data): DataFrame
        # !won't update data_path attr!
        # !update name attr to be uniqe!
        # !add 'copy' into tag list!
        data.extract_blob()

        data1 = data.clone()

        if data1.data_path is None or not os.path.exists(data1.data_path):
            cdir = data1.get_default_data_path(self.data_uri, DEFAULT_DATA_FMT)
        else:
            cdir = data1.data_path
        filename, ext = get_save_filename(
            self,
            caption="Save Settings to a File",
            cdir=cdir,
            type_filter=
            "XLSX Files (*.xlsx);;HDF5 Files (*.h5);;CSV Files (*.csv)")
        if filename is None:
            return
        # data1.name = re.sub(r"(.*)_[0-9]+\.[0-9]+",r"\1_{}".format(time.time()), data1.name)
        if 'copy' not in data.tags:
            data1.tags.append('copy')
        # update timestamp, datetime, name
        data1.update_name()
        self._save_settings(data1, filename, ext)

    def _save_settings(self, data, filename, ftype='xlsx'):
        for k, v in zip(('app', 'version', 'user', 'machine', 'segment'),
                        ('Settings Manager', f'{self._version}', getuser(),
                         self._last_machine_name, self._last_lattice_name)):
            if not k in data.info and v is not None:
                setattr(data, k, v)
        data.write(filename, ftype)

    def on_load_settings(self, data):
        # data: SnapshotData
        # settings(data.data): DataFrame
        # self.turn_off_updater_if_necessary()

        # disable take snapshot tool
        self.actionTake_Snapshot.setEnabled(False)
        #
        if self._lat is None or self._last_machine_name != data.machine or \
                self._last_lattice_name != data.segment:
            self.__load_lattice(data.machine, data.segment)
        lat = self._lat
        data.extract_blob()
        s, self._last_sts_dict = make_physics_settings(data.data.to_numpy(),
                                                       lat)
        lat.settings.update(s)
        _elem_list = []
        _invalid_elem_list = []
        for ename, settings in s.items():
            _elem = lat[ename]
            if _elem is None:
                _invalid_elem_list.append((ename, settings))
            else:
                _elem_list.append(_elem)
        self._elem_list[:] = _elem_list
        if _invalid_elem_list:
            self.on_show_invalid_elemlist(_invalid_elem_list)
            print(f"Skip non-existing devices: {_invalid_elem_list}")
        self.element_list_changed.emit()
        self.snp_loaded.emit(data)

    def on_push_ref_settings(self, data):
        # data: SnapshotData
        # settings(data.data): DataFrame
        print("Push snpdata as reference settings.")
        r = QMessageBox.question(
            self, "Publish Snapshot",
            '''<html><head/><body><p>Are you sure to publish snapshot: <span style=" color:#0055ff;">{}</span> as the reference settings?</p><p>This is to set all device reference set PVs with the values in <span style=" font-style:italic;">Setpoint(x0)</span> column of the snapshot.</p><p>All the snapshot information and the device settings will be available in <span style=" font-style:italic;">Settings Manager OPI</span>.</p></body></html>'''
            .format(data.ts_as_str() + ',' + data.ion_as_str()),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if r == QMessageBox.No:
            return
        data.extract_blob()
        for i, irow in data.data.iterrows():
            ename, fname, val0 = irow.Name, irow.Field, irow.Setpoint
            ref_st_pv = self._pv_map.get('refset').get(f'{ename}-{fname}',
                                                       None)
            if ref_st_pv is not None:
                msg = "[{0}] {1}[{2}]: Set {3} to {4}.".format(
                    datetime.fromtimestamp(time.time()).strftime(TS_FMT),
                    ename, fname, ref_st_pv.pvname, val0)
                self.log_textEdit.append(msg)
                ref_st_pv.value = val0
        # update metadata onto OPI
        snp_name = data.ts_as_str()
        snp_ion_str = data.ion_as_str()
        snp_author = data.user
        snp_note = '' if data.note == "Input note ..." else data.note
        if snp_name != caget(SNP_NAME_PV):
            caput(SNP_NAME_PV, snp_name, wait=False)
            caput(SNP_NOTE_PV, snp_note, wait=False)
            caput(SNP_ION_PV, snp_ion_str, wait=False)
            caput(SNP_AUTHOR_PV, snp_author, wait=False)
            caput(SNP_PUBLISHER_PV, getuser(), wait=False)

    def on_snp_loaded(self, data):
        m = self.snp_treeView.model()
        if m is None:
            return
        m.m_src.on_snp_loaded(data)
        self._current_snpdata = data

        # figure out the originated template
        self._current_snpdata_originated = self.get_originated_template()

        # check if loaded snapshot matches beam ops
        self.sigOrigTemplateChanged.emit(self._current_snpdata_originated[0])

    @pyqtSlot('QString')
    def onOrigTemplateChanged(self, name: str):
        """The name of originated snapshot template is changed.
        """
        if name in ('LINAC', 'FSEE'):  # signal from mach_bound
            name = self._current_snpdata_originated[0]
        # post info
        self.orig_template_name_lbl.setText(name)
        isrc_name, bound_name, _ = self.beam_display_widget.get_bound_info()
        temp_name_in_op = f"{bound_name}_{ISRC_NAME_MAP[isrc_name]}"
        # check if loaded snapshot matches beam ops
        if name == temp_name_in_op:
            self.is_match_lbl.setToolTip(
                "The loaded snapshot MATCHES beam operations.")
            self.is_match_lbl.setPixmap(self._matched_px)
            self.orig_template_info_frame.setStyleSheet(MATCH_STY)
        else:
            self.is_match_lbl.setToolTip(
                "The loaded snapshot does NOT MATCH beam operations!")
            self.is_match_lbl.setPixmap(self._not_matched_px)
            self.orig_template_info_frame.setStyleSheet(NOT_MATCH_STY)

    def on_snp_saved(self, name, path):
        m = self.snp_treeView.model()
        if m is None:
            return
        m.m_src.on_snp_saved(name, path)

    def clear_load_status(self):
        # Clear load status in snp dock.
        if not self.snp_dock.isVisible():
            return
        self.snp_treeView.model().clear_load_status()

    @pyqtSlot()
    def onFixCorNames(self):
        # ! only needed for ancient saved csv files before phantasy-machines commits (39c94e5)
        from .app_fixnames import FixNamesDialog
        if self._fixnames_dlg is None:
            self._fixnames_dlg = FixNamesDialog(self)
        self._fixnames_dlg.show()

    @pyqtSlot()
    def on_help(self):
        from phantasy_apps.utils import launch_assistant
        path = os.path.join(os.path.dirname(__file__), "docs",
                            "settings_manager.qhc")
        if os.path.isfile(path):
            launch_assistant(path)

    def on_hint_scaling_factor(self, snpdata):
        btn = self.auto_sf_btn
        if btn.isChecked():
            _, a1, _, q1 = self.beam_display_widget.get_species()
            a0, q0 = snpdata.ion_mass, snpdata.ion_charge
            try:
                sf = (float(q0) / float(a0)) / (q1 / a1)
            except:
                sf = 1.0
            finally:
                self.scaling_factor_lineEdit.setText(f"{sf:.5g}")

    @pyqtSlot(bool)
    def on_enable_logdock(self, enabled):
        if enabled:
            self.log_dock.show()
        else:
            self.log_dock.close()

    @pyqtSlot(bool)
    def on_enable_snpdock(self, enabled):
        if enabled:
            self.snp_dock.show()
        else:
            self.snp_dock.close()

    @pyqtSlot()
    def on_find_text_in_setlog(self):
        # find text in device set log window
        from PyQt5.QtGui import QTextCursor
        from PyQt5.QtGui import QTextCharFormat
        from PyQt5.QtGui import QTextDocument
        from PyQt5.QtCore import Qt
        from PyQt5.QtCore import QRegExp

        search_string = self.sender().text()

        def clear(cursor):
            cursor.select(QTextCursor.Document)
            cursor.setCharFormat(QTextCharFormat())
            cursor.clearSelection()

        document = self.log_textEdit.document()
        cursor = QTextCursor(document)

        clear(cursor)
        if search_string == '':
            return

        plain_fmt = QTextCharFormat(cursor.charFormat())
        color_fmt = plain_fmt
        color_fmt.setBackground(Qt.yellow)

        regex = QRegExp(search_string, Qt.CaseSensitive, QRegExp.Wildcard)

        pos = 0
        plainText = self.log_textEdit.toPlainText()
        index = regex.indexIn(plainText, pos)
        while (index != -1):
            cursor.setPosition(index)
            cursor.movePosition(QTextCursor.EndOfWord, 1)
            cursor.mergeCharFormat(color_fmt)
            pos = index + regex.matchedLength()
            index = regex.indexIn(plainText, pos)

    @pyqtSlot()
    def on_open_texteditor(self):
        with open(LOG_FILE, "w") as fp:
            fp.write(self.log_textEdit.toPlainText())
        QDesktopServices.openUrl(QUrl(LOG_FILE))

    @pyqtSlot()
    def on_setlog_changed(self):
        doc = self.log_textEdit.document()
        if doc.isEmpty():
            cnt = 0
        else:
            cnt = doc.lineCount()
        self.setlog_count_lbl.setText(str(cnt))

    @pyqtSlot()
    def on_refresh_snp(self):
        # refresh snp as wdir is updated.
        self.on_data_uri_changed(True, self.data_uri)

    def _splash_msg_undone(self):
        delayed_exec(
            lambda: self._splash_w.showMessage(
                "\n".join(self._task_list), Qt.AlignBottom | Qt.AlignHCenter),
            500)

    def _splash_msg(self, msg: str):
        self._splash_w.showMessage(msg, Qt.AlignBottom | Qt.AlignHCenter)

    def __preload_lattice(self, mach: str, segm: str):
        # instantiating MachinePortal
        task_name = f'Loading lattice: {mach}/{segm}...'
        self._task_list.append(task_name)
        self._splash_msg_undone()
        self.__load_lattice(mach, segm, False)
        self._task_list.remove(task_name)
        self._splash_msg(f"Loaded lattice: {mach}/{segm}.")
        self._splash_msg_undone()

    def __update_toolbar(self):
        ## hide obsoleted tools
        self.actionFix_Corrector_Names.setVisible(False)

        ## add a submenu to CaptureMachineState tool (QAction)
        ms_capture_btn = QToolButton(self)
        ms_capture_btn.setToolTip(
            "Capture additional machine state data, and save with a snapshot or for comparison visualization."
        )
        ms_capture_btn.setIcon(QIcon(QPixmap(":/sm-icons/machstate.png")))
        ms_capture_btn.setIconSize(self.toolBar.iconSize())
        ms_capture_btn.setText("Fetch Machine State")
        ms_capture_btn.setPopupMode(QToolButton.MenuButtonPopup)
        ms_capture_btn.clicked.connect(self.on_capture_machstate)
        ms_capture_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        _m = QMenu()
        # reset machine state (clear captured machine state dset)
        _act = QAction(QIcon(QPixmap(":/sm-icons/clear_ms.png")), "Reset Diff",
                       _m)
        _act.triggered.connect(self.onResetMachState)
        _m.addAction(_act)
        ms_capture_btn.setMenu(_m)
        self.toolBar.insertWidget(self.actionTake_Snapshot, ms_capture_btn)
        ##

        ## add beamSpeciesDisplayWidget
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolBar.addWidget(spacer)
        self.beam_display_widget = BeamSpeciesDisplayWidget()
        self.beam_display_widget.set_wait_until_ready(True)
        self.beam_display_widget.set_expanded(True)
        self.beam_display_widget.set_power_panel(True)
        self.beam_display_widget.set_allow_clicking_src_btns(False)
        self.beam_display_widget.mach_bound_changed.connect(
            self.sigOrigTemplateChanged)
        self.toolBar.addWidget(self.beam_display_widget)
        #
        _beam_src, _ops_bound, _beam_dest = self.beam_display_widget.get_bound_info(
        )
        self.ops_bound_cbb.setCurrentText(_ops_bound)
        printlog(
            f"Machine bound: {_ops_bound}, from {_beam_src} to {_beam_dest}")
        self.ops_bound_cbb.currentTextChanged.connect(
            lambda: self.snp_refresh_btn.clicked.emit())
        #
        self.beam_display_widget.mach_bound_changed.connect(
            self.ops_bound_cbb.setCurrentText)
        ##

    def _meta_fetcher_started(self):
        printlog("Start to fetch machine state...")
        self._meta_fetcher_pb = QProgressBar()
        self._meta_fetcher_pb.setStyleSheet("""
        QProgressBar {
            border: 1px solid gray;
            border-radius: 1px;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #7AAFF4;
            width: 10px;
            margin: 0.5px;
        }""")
        self._meta_fetcher_pb.setWindowTitle("Capturing Machine State")
        self._meta_fetcher_pb.setWindowFlags(Qt.CustomizeWindowHint
                                             | Qt.WindowTitleHint)
        self._meta_fetcher_pb.setRange(0, 100)
        self._meta_fetcher_pb.move(
            int(self.geometry().x() + self.geometry().width() / 2 -
                self._meta_fetcher_pb.geometry().width() / 2),
            int(self.geometry().y() + self.geometry().height() / 2 -
                self._meta_fetcher_pb.geometry().height() / 2))
        self._meta_fetcher_pb.show()
        self.setEnabled(False)

    def _meta_fetcher_stopped(self):
        printlog("Stopped fetching machine state.")
        self._meta_fetcher_pb.setVisible(False)

    def _meta_fetcher_progressed(self, f, s):
        printlog(f"Fetching machine state: {f * 100:>5.1f}%, {s}")
        self._meta_fetcher_pb.setValue(int(100 * f))
        self._meta_fetcher_pb.move(
            self.geometry().x() + self.geometry().width() / 2 -
            self._meta_fetcher_pb.geometry().width() / 2,
            self.geometry().y() + self.geometry().height() / 2 -
            self._meta_fetcher_pb.geometry().height() / 2)

    def _meta_fetcher_got_results(self, pv_list, grp_list, res):
        self._machstate = _build_dataframe(res, pv_list, grp_list)
        self._meta_fetcher_pb.reset()
        self._meta_fetcher_pb.deleteLater()
        self.setEnabled(True)

    def _meta_fetcher_daq_func(self, pv_list, dt, iiter):
        return _daq_func(pv_list, dt)

    @pyqtSlot()
    def on_capture_machstate(self):
        # Capture machine state defined in config/metadata.toml.
        self.__config_meta_fetcher()
        self._meta_fetcher.finished.connect(self.on_save_machine_state)
        self._meta_fetcher.start()

    def on_save_machine_state(self):
        msg = QMessageBox.question(
            self, "Save Machine State",
            "Would you like to save fetched machine state data into a file?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if msg == QMessageBox.Yes:
            filename, ext = get_save_filename(
                self,
                caption="Save Machine State to a File",
                cdir='.',
                type_filter=
                "XLSX Files (*.xlsx);;HDF5 Files (*.h5);;CSV Files (*.csv)")
            if filename is None:
                return
            r = SnapshotData.export_machine_state(self._machstate, filename,
                                                  ext)
            if r is not None:
                QMessageBox.information(
                    self, "Save Machine State",
                    f"Saved machine state data to {os.path.abspath(filename)}.",
                    QMessageBox.Ok, QMessageBox.Ok)

    def get_ms_config(self):
        """Return the configurations for machine state capture.
        """
        conf = get_meta_conf_dict(self.pref_dict['MACH_STATE']['CONFIG_PATH'])
        _rate = self.pref_dict['MACH_STATE'].get('DAQ_RATE', None)
        _nshot = self.pref_dict['MACH_STATE'].get('DAQ_NSHOT', None)
        mach_state_conf = merge_mach_conf(
            conf, nshot=_nshot, rate=_rate)  # redefine nshot, rate here
        return mach_state_conf

    def __config_meta_fetcher(self):
        # init mach state retriever
        self._mach_state_config = mach_state_conf = self.get_ms_config()
        pv_list = mach_state_conf['pv_list']
        grp_list = mach_state_conf['grp_list']
        daq_rate = mach_state_conf['daq_rate']
        daq_nshot = mach_state_conf['daq_nshot']
        self._meta_fetcher = DAQT(daq_func=partial(self._meta_fetcher_daq_func,
                                                   pv_list, 1.0 / daq_rate),
                                  daq_seq=range(daq_nshot))
        self._meta_fetcher.daqStarted.connect(self._meta_fetcher_started)
        self._meta_fetcher.progressUpdated.connect(
            self._meta_fetcher_progressed)
        self._meta_fetcher.daqFinished.connect(self._meta_fetcher_stopped)
        self._meta_fetcher.resultsReady.connect(
            partial(self._meta_fetcher_got_results, pv_list, grp_list))

    def __init_dsrc(self, dsrc_dict: dict):
        # initialize data source (db only)
        self._db_conn_pool = {}
        # to full uri
        self.data_uri = os.path.abspath(os.path.expanduser(dsrc_dict['uri']))
        # ensure the existence of parent directory(ies)
        pathlib.Path(self.data_uri).parent.mkdir(parents=True, exist_ok=True)
        # open db
        self._db_conn_pool.setdefault(
            self.data_uri, ensure_connect_db(
                self.data_uri))  # other DB_ENGINEs to be supported
        # n_snp_max (50,100,500,'All') -> All
        self.nsnp_btn.setVisible(True)
        for i in range(4):
            self.nsnp_btn.click()
        #
        self.db_refresh.connect(self.snp_refresh_btn.click)
        self.db_pull.connect(self.on_pull_data)

    @pyqtSlot()
    def on_update_nsnp(self):
        """Cycle the total number of snapshots to display.
        """
        self._n_snp_max = next(N_SNP_MAX)
        self.sender().setText(str(self._n_snp_max))

    @pyqtSlot()
    def onShowChangelog(self):
        """Open and read changelog.
        """
        QDesktopServices.openUrl(QUrl(_CHANGELOG_FILE))

    @pyqtSlot()
    def onShowUserGuide(self):
        """Open and read user guide.
        """
        QDesktopServices.openUrl(QUrl(_USERGUIDE_FILE))

    @pyqtSlot()
    def onManageDB(self):
        """Manage database
        """
        from .app_dbmgmt import DBManagerDialog
        if self._db_mgmt_dlg is None:
            self._db_mgmt_dlg = DBManagerDialog(self)
        self._db_mgmt_dlg.show()

    def on_show_invalid_elemlist(self, elemlist: list):
        """Show a table of invalid elements, with saved settings.
        """
        from .app_invalid_elemlist import InvalidElementListDialog
        self._dlg = InvalidElementListDialog(elemlist, self)
        self._dlg.show()

    @pyqtSlot(int)
    def on_nchecked_changed(self, i):
        """Total number of checked items is changed by amount of *i*.
        """
        n = int(self.n_all_checked_items_lbl.text())
        n_new = n + i
        self.n_all_checked_items_lbl.setText(str(n_new))
        if n_new > 0:
            self.sigApplyReady.emit(True)
        else:
            self.sigApplyReady.emit(False)

    @pyqtSlot()
    def on_update_ref_values(self):
        """Update reference settings with saved settings (x0 column).
        """
        m = self._tv.model()
        if m is None:
            return
        settings_selected = m.get_selection_refset()
        if len(settings_selected) == 0:
            QMessageBox.warning(
                self, "Update reference Settings",
                '<html><head/><body><p>Not any items are checked, <span style=" '
                'font-style:italic;">Update reference settings </span>only works with checked items in current page<span style=" '
                'font-style:italic;">.</span></p></body></html>',
                QMessageBox.Ok)
            return
        #
        self._refset_pb_list = []
        self._setter = DAQT(daq_func=self.set_ref_single,
                            daq_seq=settings_selected)
        self._setter.daqStarted.connect(
            lambda: self.refset_pb.setVisible(True))
        self._setter.daqStarted.connect(
            partial(self.set_widgets_status_for_ref_set, 'START'))
        self._setter.progressUpdated.connect(
            partial(self.on_refset_progress, self._refset_pb_list,
                    m.sourceModel()))
        self._setter.daqFinished.connect(
            partial(self.set_widgets_status_for_ref_set, 'STOP'))
        self._setter.daqFinished.connect(
            lambda: self.refset_pb.setVisible(False))
        self._setter.daqFinished.connect(
            lambda: self.single_update_btn.clicked.emit())
        self._setter.start()

    def set_ref_single(self, tuple_idx_settings):
        # ref_v_now: current ref set
        # ref_val0: x0 # -> (ref_v)
        # live set: fld.value
        ref_st_idx, ref_st_pv, ref_v = tuple_idx_settings
        if ref_st_pv is not None:
            ref_v_now = ref_st_pv.value
            if not is_close(ref_v_now, ref_v, self.ndigit):
                msg = "[{0}] Set {1:<35s} reference value from {2:.3f} to {3:.3f}.".format(
                    datetime.fromtimestamp(time.time()).strftime(TS_FMT),
                    ref_st_pv.pvname, float(ref_v_now), ref_v)
                ref_st_pv.value = ref_v
                self._refset_pb_list.append((ref_st_idx, msg))
                time.sleep(0.001)
        else:
            self._refset_pb_list.append((ref_st_idx, "No Reference"))

    @pyqtSlot(float, 'QString')
    def on_refset_progress(self, refset_pb_list, m, per, str_idx):
        idx_src, msg = refset_pb_list[-1]
        m.hlrow(idx_src)
        self.log_textEdit.append(msg)
        self.refset_pb.setValue(int(per * 100))

    @pyqtSlot(bool)
    def on_toggle_refset_ctrls(self, is_checked):
        """If checked, show the controls for reference set.
        """
        for w in (self.update_ref_btn, self.show_diff_x0ref_btn,
                  self.show_diff_x2ref_btn):
            w.setVisible(is_checked)
        m = self.settingsView.model()
        if m is None:
            return
        src_m = m.sourceModel()
        for i in (
                src_m.i_ref_st,
                src_m.i_dstref,
                src_m.i_dval0ref,
        ):
            self._tv.setColumnHidden(i, not is_checked)

    @pyqtSlot(bool)
    def on_toggle_alm_ctrls(self, is_checked):
        """If checked, show the controls for device alarms.
        """
        for w in (self.enable_alms_btn, self.disable_alms_btn,
                  self.alm_dec_line, self.show_disabled_read_alms_btn,
                  self.show_disabled_tune_alms_btn,
                  self.show_enabled_read_alms_btn,
                  self.show_enabled_tune_alms_btn, self.alm_type_cbb):
            w.setVisible(is_checked)
        m = self.settingsView.model()
        if m is None:
            return
        src_m = m.sourceModel()
        for i in (src_m.i_read_alm, src_m.i_tune_alm):
            self._tv.setColumnHidden(i, not is_checked)

    @pyqtSlot()
    def on_click_enable_alms_btn(self):
        """Enable alarms for all checked rows.
        """
        self._alm_set(False)

    @pyqtSlot()
    def on_click_disable_alms_btn(self):
        """Disable alarms for all checked rows.
        """
        self._alm_set(True)

    def _alm_set(self, to_disable=False):
        if to_disable:
            new_val = 0
            msg_title = "Disable Device Alarms"
        else:
            new_val = 1
            msg_title = "Enable Device Alarms"

        m = self._tv.model()
        if m is None:
            return
        settings_selected = m.get_selection_almset()
        if len(settings_selected) == 0:
            QMessageBox.warning(
                self, f"{msg_title}",
                '<html><head/><body><p>Not any items are checked, <span style=" '
                f'font-style:italic;">{msg_title} </span>only works with checked items in current page<span style=" '
                'font-style:italic;">.</span></p></body></html>',
                QMessageBox.Ok)
            return
        #
        self._alm_set_pb_list = []
        self._alm_worker = DAQT(daq_func=partial(self.set_alm_single, new_val,
                                                 self._alm_type_idx_list),
                                daq_seq=settings_selected)
        self._alm_worker.daqStarted.connect(
            lambda: self.alm_set_pb.setVisible(True))
        self._alm_worker.daqStarted.connect(
            partial(self.set_widgets_status_for_alm_set, 'START'))
        self._alm_worker.progressUpdated.connect(
            partial(self.on_alm_set_progress, self._alm_set_pb_list,
                    m.sourceModel()))
        self._alm_worker.daqFinished.connect(
            partial(self.set_widgets_status_for_alm_set, 'STOP'))
        self._alm_worker.daqFinished.connect(
            lambda: self.alm_set_pb.setVisible(False))
        self._alm_worker.daqFinished.connect(
            lambda: self.single_update_btn.clicked.emit())
        self._alm_worker.start()

    def set_alm_single(self, value, alarm_type_idx_list, tuple_idx_settings):
        # value: new alarm switch value to set
        read_alm_idx, read_alm_pv, tune_alm_idx, tune_alm_pv = tuple_idx_settings
        _idx_pv_list = np.array([(read_alm_idx, read_alm_pv),
                                 (tune_alm_idx, tune_alm_pv)
                                 ])[alarm_type_idx_list]

        for _idx, _pv in _idx_pv_list:
            if _pv is not None:
                msg = "[{0}] Set {1:<35s} to {2}.".format(
                    datetime.fromtimestamp(time.time()).strftime(TS_FMT),
                    _pv.pvname, value)
                _pv.value = value
                self._alm_set_pb_list.append((_idx, msg))
                time.sleep(0.02)
            else:
                self._alm_set_pb_list.append((_idx, "No alarm to set"))

    @pyqtSlot(float, 'QString')
    def on_alm_set_progress(self, alm_set_pb_list, m, per, str_idx):
        idx_src, msg = alm_set_pb_list[-1]
        m.hlrow(idx_src)
        self.log_textEdit.append(msg)
        self.refset_pb.setValue(int(per * 100))

    def set_widgets_status_for_alm_set(self, status):
        """Set widgets status for alm set.
        """
        w1 = (self.enable_alms_btn, self.disable_alms_btn, self.alm_type_cbb)
        [i.setDisabled(status == 'START') for i in w1]

    @pyqtSlot('QString')
    def on_alm_type_changed(self, s):
        """Alarm type to enable/disable is changed.
        """
        tt1 = "Disable {0} alarms for checked items."
        tt2 = "Enable {0} alarms for checked items."
        self.disable_alms_btn.setToolTip(tt1.format(s))
        self.enable_alms_btn.setToolTip(tt2.format(s))
        self._alm_type_idx_list = ALM_TYPE_MAP[s]

    def load_snapshot(self, name: str):
        # load the snapshot named by *name* (to match datetime column)
        o = get_snapshotdata(name, self.data_uri)
        if o is None:
            QMessageBox.warning(self, "Load Snapshot",
                                f"Cannot find the snapshot: '{name}'",
                                QMessageBox.Ok, QMessageBox.Ok)
            return
        else:
            self.on_load_settings(o)

    @pyqtSlot()
    def on_abort_apply(self):
        """Abort settings apply immediately.
        """
        self.applyer.abort()

    @pyqtSlot()
    def on_revert_apply(self, apply_ts: str, btn: QToolButton):
        """Revert settings changed by last "Apply".
        """
        # title: name of apply
        # btn: original toobutton where click singal is from
        setLogMsgContainer = self.effSetLogMsgContainer_dict.get(apply_ts)

        def _revert_single(item: SetLogMessager):
            # print(f"Revert {item._ename} [{item._fname}] to {item._old_set}")
            item._fld.value = item._old_set
            msger = SetLogMessager(None,
                                   item._ename,
                                   item._fname,
                                   item._new_set,
                                   item._old_set,
                                   item._old_set,
                                   '*',
                                   1,
                                   item._idx_src,
                                   is_revert=True,
                                   orig_ts=item._ts)
            self._reverter.meta_signal1.emit(msger)
            time.sleep(self.t_wait)

        def _on_update_revertlog(m, msger):
            m.hlrow(msger._idx_src)
            self.sigSetLogColorReset.emit()
            self.log_textEdit.append(str(msger))

        def _on_revert_progress(p: float, s: str):
            self.apply_pb.setValue(int(p * 100))

        self._reverter = DAQT(daq_func=_revert_single,
                              daq_seq=setLogMsgContainer._items[::-1])
        self._reverter.daqStarted.connect(
            lambda: self.apply_pb.setVisible(True))
        self._reverter.daqStarted.connect(
            partial(self.set_widgets_status_for_applying, 'START'))
        self._reverter.daqStarted.connect(lambda: btn.setDisabled(True))
        self._reverter.meta_signal1.connect(
            partial(_on_update_revertlog,
                    self._tv.model().sourceModel()))
        self._reverter.progressUpdated.connect(_on_revert_progress)
        self._reverter.daqFinished.connect(
            partial(self.set_widgets_status_for_applying, 'STOP'))
        self._reverter.daqFinished.connect(lambda: btn.setDisabled(False))
        self._reverter.daqFinished.connect(
            lambda: self.apply_pb.setVisible(False))
        self._reverter.daqFinished.connect(
            lambda: self.effSetLogMsgContainer_dict.get(apply_ts).clear())
        self._reverter.daqFinished.connect(
            lambda: self.single_update_btn.clicked.emit())
        self._reverter.start()

    def _init_revert_area(self):
        # layout for revert buttons
        w = QWidget(self)
        w.setContentsMargins(0, 6, 0, 0)
        layout = FlowLayout()
        w.setLayout(layout)
        self.revert_area.setWidget(w)

    def build_revert_button(self, apply_ts: str, apply_reason: str):
        # Build a button for revert after Apply is triggered.
        n = self.effSetLogMsgContainer_dict.get(apply_ts).count_items()
        if n == 0:
            return None
        btn = QToolButton()
        btn.setIcon(QIcon(QPixmap(":/sm-icons/revert.png")))
        btn.setIconSize(QSize(PX_SIZE * 2, PX_SIZE * 2))
        op = SCALE_OP_MAP[self.scale_op_cbb.currentIndex()]
        ov = float(self.scaling_factor_lineEdit.text())
        snp_name = self._current_snpdata.ts_as_str(
        ) + "-" + self._current_snpdata.ion_as_str()
        if apply_reason == '':
            btn.setToolTip(
                REVERT_TT_NO_REASON.format(n=n,
                                           op=op,
                                           ov=ov,
                                           ts=apply_ts,
                                           snapshot=snp_name))
        else:
            btn.setToolTip(
                REVERT_TT_REASON.format(n=n,
                                        op=op,
                                        ov=ov,
                                        ts=apply_ts,
                                        reason=apply_reason,
                                        snapshot=snp_name))
        btn.setText(f"{apply_ts}\n{apply_reason} ({op} {ov})")
        # btn.setAutoRaise(True)
        btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        btn.clicked.connect(partial(self.on_revert_apply, apply_ts, btn))
        self.effSetLogMsgContainer_dict.get(apply_ts).sigHasItems.connect(
            btn.setVisible)
        return btn

    def add_new_revert(self, apply_ts: str, apply_reason: str):
        """Build a new toolbutton for revert apply.
        """
        layout = self.revert_area.findChildren(FlowLayout)[0]
        btn = self.build_revert_button(apply_ts, apply_reason)
        if btn is not None:
            layout.addWidget(btn)

    @pyqtSlot()
    def on_purge_reverts(self):
        """Purge all reverts.
        """
        for _, v in self.effSetLogMsgContainer_dict.items():
            v.clear()
        self.effSetLogMsgContainer_dict = {}
        w = self.revert_area.takeWidget()
        w.setParent(None)
        self._init_revert_area()


def get_snapshotdata(query_str: str, uri: str, column_name='datetime'):
    """Search and return a  object from the database defined by *uri*, where
    *query_str* matches the value of *column_name*.
    """
    db_conn = ensure_connect_db(uri)
    df = pd.read_sql(
        f"SELECT * FROM snapshot WHERE {column_name} = '{query_str}' LIMIT 1",
        db_conn)
    if df.empty:
        print(f"Invalid snapshot named '{query_str}'")
        o = None
    else:
        o = read_data(list(df.iterrows())[0][1],
                      'sql')  # see df_all.iterrows()
    db_conn.close()
    return o


def is_snp_data_exist(snpdata, snpdata_list):
    # if snpdata named 'name' exists.
    for i in snpdata_list:
        if snpdata.name == i.name:
            return True
    return False


def make_tolerance_dict_from_table_settings(table_settings):
    """Create tolerance dict from TableSettings.
    """
    r = {}
    for i in table_settings:
        ename, fname, tol = i[0], i[1], i[7]
        if ename in r:
            r[ename].update({fname: tol})
        else:
            r[ename] = {fname: tol}
    return r


def is_close(x, y, decimal=6):
    if abs(x - y) < 1.5 * 10**(-decimal):
        return True
    return False


_ISEG_PVS = (
    # N0106
    'ISEG:5230096:0:0:Control:doClear',
    'ISEG:5230096:0:1:Control:doClear',
    'ISEG:5230096:0:2:Control:doClear',
    'ISEG:5230096:0:3:Control:doClear',

    # N0306
    'ISEG:5230103:0:0:Control:doClear',
    'ISEG:5230103:0:1:Control:doClear',

    # LS1_N0604
    'ISEG:5230127:0:0:Control:doClear',
    'ISEG:5230127:0:1:Control:doClear',

    # LS1_N1501
    'ISEG:5230126:0:0:Control:doClear',

    # LS1_N1902
    'ISEG:5230100:0:0:Control:doClear',

    # FS1_N0302
    'ISEG:5230093:0:0:Control:doClear',
    'ISEG:5230093:0:1:Control:doClear',

    # FS1_N0506
    'ISEG:5230104:0:0:Control:doClear',

    # LS2_N0808
    'ISEG:5230097:0:0:Control:doClear',
    'ISEG:5230097:0:1:Control:doClear',

    # LS2_N1708
    'ISEG:5230098:0:0:Control:doClear',
    'ISEG:5230098:0:1:Control:doClear',

    # LS2_N4202
    'ISEG:5230095:0:0:Control:doClear',
    'ISEG:5230095:0:1:Control:doClear',

    # FS2_N0108
    'ISEG:5230094:0:0:Control:doClear',
    'ISEG:5230094:0:1:Control:doClear',

    # LS3_N1108
    # 'ISEG:5230099:0:0:Control:doClear',

    # LS3_N2101
    'ISEG:5230101:0:0:Control:doClear',
    'ISEG:5230101:0:1:Control:doClear',
)


def _reset_ca():
    ca.clear_cache()
    ca.finalize_libca()
    ca.initialize_libca()


def _reset_trip_events():
    # reset trip events only for BIAS_VOLTAGE controls of PM, FC, EMS
    # 'PM', 'FC', 'EMS', 'ND', 'HMR', 'IC'):
    for pv in _ISEG_PVS:
        caput(pv, 1)


def _sym2z(sym: str):
    z = sym2z(sym)
    if z is None:
        z = 999
    return z
