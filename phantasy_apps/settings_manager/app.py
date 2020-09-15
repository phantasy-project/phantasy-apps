#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import fnmatch
import json
import os
import time
from collections import OrderedDict
from functools import partial
from getpass import getuser

from PyQt5.QtCore import QEventLoop
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QKeySequence
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtWidgets import QWidget
from phantasy import CaField
from phantasy import Settings
from phantasy import build_element
from phantasy import Lattice
from phantasy_ui import BaseAppForm
from phantasy_ui import get_open_filename
from phantasy_ui import get_save_filename
from phantasy_ui import printlog
from phantasy_ui.widgets import is_item_checked
from phantasy_ui.widgets import BeamSpeciesDisplayWidget
from phantasy_ui.widgets import DataAcquisitionThread as DAQT
from phantasy_ui.widgets import ElementSelectDialog
from phantasy_ui.widgets import LatticeWidget
from phantasy_ui.widgets import ProbeWidget

from .app_loadfrom import LoadSettingsDialog
from .app_pref import DEFAULT_PREF
from .app_pref import DEFAULT_CONFIG_PATH
from .app_pref import PreferencesDialog
from .data import CSV_HEADER
from .data import ElementPVConfig
from .data import TableSettings
from .data import ToleranceSettings
from .data import SnapshotData
from .data import get_csv_settings
from .data import make_physics_settings
from .ui.ui_app import Ui_MainWindow
from .ui.ui_query_tips import Ui_Form as QueryTipsForm
from .utils import FMT
from .utils import SettingsModel
from .utils import pack_settings
from .utils import str2float
from .utils import init_config_dir
from .utils import VALID_FILTER_KEYS_NUM
from .utils import SnapshotDataModel

LIVE = False

if not LIVE:
    DEFAULT_MACH = "FRIB_VA"
    DEFAULT_SEGM = "LS1FS1"
else:
    DEFAULT_MACH = "FRIB"
    DEFAULT_SEGM = "LINAC"

PX_SIZE = 24
DATA_SRC_MAP = {'model': 'model', 'live': 'control'}
IDX_RATE_MAP = {0: 1.0, 1: 0.5, 2: 2.0, 3: 0.2, 4: 0.1}
FILTER_TT = """\
Input filter string with the format of 'keyword=pattern', valid keywords as
the headers show, pattern applies Unix wildcard rules.
Keyword is case insensitive, if keyword is not defined, 'device' is used.
For 'setpoint', the keyword 'x0' is used, the same rule applies to 'x1', 'x2',
'dx01', 'dx02', 'dx03', where 'dxij' is 'xi - xj' as show in the headers.

Press Enter to activate the filter, here is some examples:
1. *: match all device names, which is equivalent of device=*;
2. *LEBT*: match device name which has string 'LEBT';
3. type='CAV': match all devices of type 'CAV';
4. dx12=0.00*: match the diff between readback and setpoint of 0.00xx..;
5. ? is to match one char or digit, pure '' is to interpret as *.

For the number columns, value range or single value filter is supported, e.g.
1. pos=(1,) matches all the position value equal or greater than 1.0;
2. x1=(-1, 2) matches current readback value is in [-1, 2] range.
3. dx12=0.1 matches the discrenpacy between the live readback and setpoint is 0.1.\
"""


class SettingsManagerWindow(BaseAppForm, Ui_MainWindow):
    # signal: settings loaded, emit flat_settings and settings.
    settingsLoaded = pyqtSignal(QVariant, QVariant)

    # refresh rate
    rate_changed = pyqtSignal(int)

    # lattice is loaded
    lattice_loaded = pyqtSignal(QVariant)

    # discrenpancy tolerance
    # float: tolerance value
    # ToleranceSettings: {ename: {fname: tolerance value}}
    tolerance_changed = pyqtSignal([float], [ToleranceSettings])

    # the list of element list is changed --> update settings model
    element_list_changed = pyqtSignal()

    # model settings is changed --> update settings snapshot
    model_settings_changed = pyqtSignal(Settings)

    # element from PVs
    element_from_pv_added = pyqtSignal(QVariant)

    # ndigit
    ndigit_changed = pyqtSignal(int)

    # font
    font_changed = pyqtSignal(QFont)

    # bool
    init_settings_changed = pyqtSignal(bool)

    # runtime snapshots
    snapshots_number_changed = pyqtSignal(int)

    # snp saved, snpdata name, filepath
    snp_saved = pyqtSignal('QString', 'QString')

    # snp casted, snpdata name
    snp_casted = pyqtSignal('QString')

    def __init__(self, version, config_dir=None):
        super(SettingsManagerWindow, self).__init__()

        # app version
        self._version = version

        # window title/icon
        self.setWindowTitle("Settings Manager")

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

        self.default_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.default_font_size = self.default_font.pointSize()

        # config
        self.init_config(config_dir)

        # post init ui
        self.__post_init_ui()

        self.adjustSize()

    def init_config(self, confdir):
        # preferences
        # see preference dialog class
        self.pref_dict = DEFAULT_PREF
        self.field_init_mode = self.pref_dict['field_init_mode']
        self.t_wait = self.pref_dict['t_wait']
        self.init_settings = self.pref_dict['init_settings']
        self.tolerance = self.pref_dict['tolerance']
        self.dt_confsync = self.pref_dict['dt_confsync']
        self.ndigit = self.pref_dict['ndigit']
        self.fmt = '{{0:.{0}f}}'.format(self.ndigit)
        self.wdir = self.pref_dict['wdir']

        self.tolerance_changed[ToleranceSettings].connect(self.on_tolerance_dict_changed)
        self.tolerance_changed[float].connect(self.on_tolerance_float_changed)
        self.model_settings_changed.connect(self.on_model_settings_changed)
        self.element_from_pv_added.connect(self.on_element_from_pv_added)
        self.ndigit_changed.connect(self.on_ndigit_changed)

        # init dir
        confdir = self.pref_dict['config_path'] if confdir is None else confdir
        self.pref_dict['config_path'] = os.path.abspath(os.path.expanduser(confdir))
        _, ts_confpath, ms_confpath, elem_confpath = init_config_dir(confdir)

        # tolerance settings (ts)
        self._tolerance_settings = ToleranceSettings(ts_confpath)

        # predefined model settings (ms)
        self.ms_confpath = ms_confpath
        self._model_settings = Settings(self.ms_confpath)

        # elements from PVs
        self.elem_confpath = elem_confpath
        self._elem_pvconf = ElementPVConfig(self.elem_confpath)

        # element sequence: initial lattice, maintain internal only
        self.__init_lat = self.build_lattice()

        # config sync timer
        self.config_timer = QTimer(self)
        self.config_timer.timeout.connect(self.on_update_dump_config)
        #
        # disable this timer 2020-03-09
        # self.config_timer.start(self.dt_confsync * 1000)
        #

        # font
        self.font = self.get_font_config()
        self.pref_dict['font'] = self.font
        self.font_changed.connect(self.on_font_changed)

        # init settings boolean
        self.init_settings_changed.connect(self.init_settings_chkbox.setChecked)

    @pyqtSlot(QFont)
    def on_font_changed(self, font):
        """Update font config.
        """
        self.font = font
        self.pref_dict['font'] = font
        m = self._tv.model()
        if m is None:
            return
        src_m = m.sourceModel()
        src_m.style_view(font=font)
        src_m.fit_view()

    def get_font_config(self):
        """Initial font config.
        """
        return self.default_font

    @pyqtSlot(QVariant)
    def on_element_from_pv_added(self, elem):
        """CaElement from PVs is added, update elem_pvconf.
        """
        ename = elem.name
        if ename not in self._elem_pvconf:
            eng_field = elem.get_eng_fields()[0]
            phy_field = elem.get_phy_fields()[0]
            sp_pv = elem.pv(handle='setpoint', field=eng_field)[0]
            rd_pv = elem.pv(handle='readback', field=eng_field)[0]
            self._elem_pvconf[ename] = {
                'setpoint': sp_pv,
                'readback': rd_pv,
                'index': elem.index,
                'length': elem.length,
                'sb': elem.sb,
                'family': elem.family,
                'field': eng_field,
                'field_phy': phy_field
            }
            self._elem_pvconf.write(self.elem_confpath)

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

        self.__init_lat = self.__init_lat + self._lat
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
        if not self.init_settings:
            QMessageBox.information(self, "Loaded Lattice",
                                    "Lattice is loaded, add device settings via 'Add Devices' or "
                                    "'Load Settings' tools, "
                                    "or initialize with all the devices in the loaded lattice.",
                                    QMessageBox.Ok)

    def _enable_widgets(self, enabled):
        for w in (self.lv_lbl, self.lv_mach_lbl, self.lv_segm_lbl,
                  self.lv_view_btn,
                  self.reload_lattice_btn):
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
        model = SettingsModel(self._tv, self.__flat_settings,
                              ndigit=self.ndigit, font=self.font)
        model.settings_sts.connect(self.on_settings_sts)
        model.item_deletion_updated[list].connect(self.on_delete_items)
        model.set_model()
        self._fld_obj, self._pv_obj = model._fld_obj, model._pv_obj
        self._fld_it, self._pv_it = model._fld_it, model._pv_it

        #
        self.toggle_ftype()
        #
        printlog("Updating data values...")
        self.update_ctrl_btn.toggled.emit(self.update_ctrl_btn.isChecked())
        self.single_update_btn.clicked.emit()

    @pyqtSlot(int, int, int)
    def on_settings_sts(self, i, j, k):
        for s, v in zip(('elem', 'sppv', 'rdpv'), (i, j, k)):
            o = getattr(self, 'total_{}_number_lbl'.format(s))
            o.setText(str(v))

    def __post_init_ui(self):
        # add beamSpeciesDisplayWidget
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolBar.addWidget(spacer)
        self.beam_display_widget = BeamSpeciesDisplayWidget()
        self.toolBar.addWidget(self.beam_display_widget)
        #

        self._tv = self.treeView
        self._load_from_dlg = None
        self._elem_select_dlg = None
        self._lattice_load_window = None
        self._fixnames_dlg = None

        self._mp = None
        self._last_machine_name = None
        self._last_lattice_name = None
        self._lat = None # loaded from latticeWidget
        self._elem_list = []  # element list for SettingsModel

        self.__settings = Settings()
        self.__flat_settings = None

        self._eval_scaling_factor = False # not eval sf (hit enter)

        self._eng_phy_toggle = {'ENG': True, 'PHY': False}
        self.on_lattice_changed(self._mp)

        # lattice viewer
        self._enable_widgets(False)
        self._lv = None
        self.lv_view_btn.clicked.connect(self.on_show_latinfo)

        # show lattice settings
        self.settingsLoaded.connect(self.on_settings_loaded)

        # update rate
        self.rate_changed.connect(self.on_update_rate_changed)
        self.update_rate_cbb.currentIndexChanged.emit(
            self.update_rate_cbb.currentIndex())

        # scaling factor lineEdit
        #self.scaling_factor_lineEdit.setValidator(QDoubleValidator(0.0, 10, 6))

        # icon
        self.done_px = QPixmap(":/sm-icons/done.png")
        self.fail_px = QPixmap(":/sm-icons/fail.png")
        self._warning_px = QPixmap(":/sm-icons/warning.png")
        self._ok_px = QPixmap(":/sm-icons/ok.png")
        self._copy_icon = QIcon(QPixmap(":/sm-icons/copy.png"))
        self._probe_icon = QIcon(QPixmap(":/sm-icons/probe.png"))
        self._unsel_icon = QIcon(QPixmap(":/sm-icons/uncheck.png"))
        self._sel_icon = QIcon(QPixmap(":/sm-icons/check.png"))

        # selection
        self.select_all_btn.clicked.connect(partial(self.on_select, 'all'))
        self.invert_selection_btn.clicked.connect(partial(self.on_select, 'invert'))

        # filter
        self.init_filter()

        # stop auto update when lattice is changed
        self.lattice_loaded.connect(self.stop_auto_update)
        # widget status regarding lattice changed.
        self.lattice_loaded.connect(self.on_update_widgets_status)
        #
        self.element_list_changed.connect(self.on_elemlist_changed)

        # context menu
        self.set_context_menu()
        self._probe_widgets_dict = {}

        # dnd
        self.setAcceptDrops(True)

        # font size control
        zoom0 = QShortcut(QKeySequence("Ctrl+0"), self)
        zoom_in = QShortcut(QKeySequence.ZoomIn, self)
        zoom_out = QShortcut(QKeySequence.ZoomOut, self)
        zoom0.activated.connect(partial(self.on_change_font_size, 0))
        zoom_in.activated.connect(partial(self.on_change_font_size, 1))
        zoom_out.activated.connect(partial(self.on_change_font_size, -1))
        self.grow_fontsize_btn.clicked.connect(partial(
            self.on_change_font_size, 1))
        self.shrink_fontsize_btn.clicked.connect(partial(
            self.on_change_font_size, -1))

        # query tips
        self._query_tips_form = None
        self.filter_btn.toggled.connect(partial(self.on_enable_search, True))
        self.filter_btn.toggled.emit(self.filter_btn.isChecked())

        # snapshot dock
        self._snapshots_count = 0
        self.snapshots_number_changed.connect(self.on_snapshots_changed)
        self.snapshots_number_changed.emit(self._snapshots_count)
        self._snp_dock_list = []  # for snp_treeView

        # apply pb
        self.apply_pb.setVisible(False)

    @pyqtSlot(bool)
    def on_enable_search(self, auto_collapse, enabled):
        if auto_collapse:
            self.filter_lineEdit.setVisible(enabled)
        if not enabled:
            self.filter_lineEdit.setText('')
            self.filter_lineEdit.editingFinished.emit()

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
        self._tv.setContextMenuPolicy(Qt.CustomContextMenu)
        self._tv.customContextMenuRequested.connect(self.on_custom_context_menu)

    @pyqtSlot()
    def on_copy_text(self, m, idx):
        text = m.data(idx)
        cb = QGuiApplication.clipboard()
        cb.setText(text)
        printlog('copied text: {}'.format(text))
        msg = '<html><head/><body><p><span style="color:#007BFF;">Copied text: </span><span style="color:#DC3545;">{}</span></p></body></html>'.format(text)
        self.statusInfoChanged.emit(msg)
        self._reset_status_info()

    @pyqtSlot()
    def on_probe_element(self, elem, fname):
        ename = elem.name
        if ename not in self._probe_widgets_dict:
            w = ProbeWidget(element=elem)
            [o.setEnabled(False) for o in (w.locate_btn, w.lattice_load_btn)]
            self._probe_widgets_dict[ename] = w
        w = self._probe_widgets_dict[ename]
        w.show()
        w.fields_cbb.setCurrentText(fname)

    @pyqtSlot(QPoint)
    def on_custom_context_menu(self, pos):
        m = self._tv.model()
        if m is None:
            return
        src_m = m.sourceModel()
        idx = self._tv.indexAt(pos)
        src_idx = m.mapToSource(idx)
        item = src_m.itemFromIndex(src_idx)
        text = item.text()

        #
        menu = QMenu(self)
        menu.setStyleSheet('QMenu {margin: 2px;}')

        #
        copy_action = QAction(self._copy_icon,
                              "Copy '{}'".format(text), menu)
        copy_action.triggered.connect(partial(self.on_copy_text, m, idx))
        menu.addAction(copy_action)

        #
        if hasattr(item, 'fobj'):
            ename = text
            elem = self.__init_lat[ename]
            fld = item.fobj
            probe_action = QAction(self._probe_icon,
                                   "Probe '{}'".format(ename), menu)
            probe_action.triggered.connect(
                    partial(self.on_probe_element, elem, fld.name))
            menu.addAction(probe_action)

        # toggle items action
        m = self._tv.model()
        m_src = m.sourceModel()
        selected_rows = {idx.row() for idx in self._tv.selectedIndexes()}
        n_rows = len(selected_rows)
        _item0 = m_src.itemFromIndex(m.mapToSource(self._tv.selectedIndexes()[0]))
        is_checked = is_item_checked(_item0)
        if n_rows == 1:
            row_text = 'row'
        else:
            row_text = 'rows'
        if is_checked:
            new_check_state = Qt.Unchecked
            act_icon = self._unsel_icon
            act_text = "Uncheck all ({}) {}".format(n_rows, row_text)
        else:
            new_check_state = Qt.Checked
            act_icon = self._sel_icon
            act_text = "Check all ({}) {}".format(n_rows, row_text)
        sel_action = QAction(act_icon, act_text, menu)
        sel_action.triggered.connect(partial(self.on_toggle_selected_rows,
                                     selected_rows, m, m_src, new_check_state))
        menu.addAction(sel_action)

        #
        menu.exec_(self._tv.viewport().mapToGlobal(pos))

    @pyqtSlot()
    def on_toggle_selected_rows(self, selected_rows, m, m_src, new_check_state):
        for i in selected_rows:
            m_src.itemFromIndex(m.mapToSource(m.index(i, 0))).setCheckState(new_check_state)

    @pyqtSlot(QVariant)
    def on_update_widgets_status(self, o):
        # WIP: control widget status after lattice is loaded.
        self.actionLoad_From_Snapshot.setEnabled(True)
        self.update_lattice_info_lbls(o.last_machine_name, o.last_lattice_name)

    @pyqtSlot()
    def on_elemlist_changed(self):
        # element list changed
        # update flat_settings and settings
        # update settings view
        flat_settings, settings = pack_settings(
            self._elem_list, self.__init_lat,
            settings=self.__init_lat.settings,
            data_source=DATA_SRC_MAP[self.field_init_mode],
            only_physics=False)
        self.settingsLoaded.emit(flat_settings, settings)
        self.tolerance_changed[ToleranceSettings].emit(self._tolerance_settings)
        self.model_settings_changed.emit(settings)

    @pyqtSlot(float)
    def on_tolerance_float_changed(self, tol):
        # set tolerance with the same value.
        # update _tolerance_settings
        m = self._tv.model()
        if m is None:
            return
        src_m = m.sourceModel()
        for i in range(src_m.rowCount()):
            src_m.setData(src_m.index(i, src_m.i_tol), self.fmt.format(tol),
                          Qt.DisplayRole)
            # update tolerance settings
            ename = src_m.data(src_m.index(i, src_m.i_name))
            fname = src_m.data(src_m.index(i, src_m.i_field))
            if ename not in self._tolerance_settings:
                self._tolerance_settings[ename] = OrderedDict([(fname, tol)])
            else:
                self._tolerance_settings[ename].update([(fname, tol)])
        self._tolerance_settings.write(self._tolerance_settings.settings_path)

    @pyqtSlot(ToleranceSettings)
    def on_tolerance_dict_changed(self, tol_settings):
        # set tolerance with a tolerance settings
        m = self._tv.model()
        if m is None:
            return
        src_m = m.sourceModel()
        for i in range(src_m.rowCount()):
            ename = src_m.data(src_m.index(i, src_m.i_name))
            fname = src_m.data(src_m.index(i, src_m.i_field))
            if ename not in tol_settings:
                continue
            elif fname not in tol_settings[ename]:
                continue
            else:
                tol = tol_settings[ename][fname]
                src_m.setData(
                    src_m.index(i, src_m.i_tol), self.fmt.format(tol),
                    Qt.DisplayRole)

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
        if i == 5:  # add 'auto' back to cbb index 5
            self._update_mode = 'auto'
            tt = "Auto updating rate."
        else:
            self._update_mode = 'thread'
            rate = IDX_RATE_MAP[i]
            self._update_delt = 1.0 / rate  # sec
            tt = "Updating at {0:.1f} Hz.".format(rate)
        self.update_rate_cbb.setToolTip(tt)

    def on_save(self):
        """Save settings to file.
        """
        filename, ext = get_save_filename(self,
                                          caption="Save Settings to a File",
                                          type_filter="CSV Files (*.csv);;JSON Files (*.json);;HDF5 Files (*.h5)")
        if filename is None:
            return
        ext = ext.upper()
        if ext == 'CSV':
            self._save_settings_as_csv(filename)
        if ext == 'JSON':
            self._save_settings_as_json(filename)
        elif ext == 'H5':
            self._save_settings_as_h5(filename)

        QMessageBox.information(
            self, "", "Saved data to {}".format(filename),
            QMessageBox.Ok)
        printlog("Saved settings to {}.".format(filename))

    def _save_settings_as_json(self, filename):
        # WIP
        s = self.get_settings()
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    def _save_settings_as_csv(self, filename):
        s = get_csv_settings(self._tv.model())
        s.write(filename, header=CSV_HEADER)

    def _save_settings_as_h5(self, filename):
        pass

    def _save_settings_as_h5(self, filename):
        pass

    @pyqtSlot()
    def on_load_from_snp(self):
        """Load settings from .snp file.
        """
        if self._load_from_dlg is None:
            self._load_from_dlg = LoadSettingsDialog(self)
        self._load_from_dlg.settingsLoaded.connect(self.on_settings_loaded)
        self._load_from_dlg.show()

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
        if not self._eval_scaling_factor:
            self.scaling_factor_lineEdit.returnPressed.emit()

        # scaling factor
        scaling_factor = float(self.scaling_factor_lineEdit.text())
        #
        self.idx_px_list = []  # list to apply icon [(idx_src, px)]
        m = self._tv.model()
        settings_selected = m.get_selection()
        if len(settings_selected) == 0:
            QMessageBox.warning(self, "Apply Settings",
                    '<html><head/><body><p>Not any items are checked, <span style=" font-style:italic;">Apply </span>only work with checked items<span style=" font-style:italic;">.</span></p></body></html>',
                    QMessageBox.Ok)
            return

        self.applyer = DAQT(daq_func=partial(self.apply_single, scaling_factor),
                            daq_seq=settings_selected)
        self.applyer.daqStarted.connect(lambda:self.apply_pb.setVisible(True))
        self.applyer.daqStarted.connect(partial(
            self.set_widgets_status_for_applying, 'START'))
        self.applyer.progressUpdated.connect(
            partial(self.on_apply_settings_progress,
                    self.idx_px_list, m.sourceModel()))
        self.applyer.daqFinished.connect(partial(
            self.set_widgets_status_for_applying, 'STOP'))
        self.applyer.daqFinished.connect(lambda:self.apply_pb.setVisible(False))
        self.applyer.start()

    def apply_single(self, sf, tuple_idx_settings):
        idx_src, settings, new_fval0 = tuple_idx_settings
        elem, fname, fld, fval0 = settings
        ename = elem.name
        print("New fval: {}, fval0: {}".format(new_fval0, fval0))
        fval_to_set = new_fval0 * sf
        try:
            t0 = time.time()
            fval_current_settings = fld.current_setting()
            fld.value = fval_to_set
        except:
            px = self.fail_px
        else:
            px = self.done_px
            printlog("- Set {} [{}] from {} to {} ({}).".format(
                ename, fname, fval_current_settings, fval_to_set, new_fval0))
            dt = self.t_wait - (time.time() - t0)
            if dt > 0:
                time.sleep(dt)
                printlog("Wait time: {} sec.".format(dt))
        self.idx_px_list.append((idx_src, px))

    @pyqtSlot(float, 'QString')
    def on_apply_settings_progress(self, idx_px_list, m, per, str_idx):
        printlog("Apply settings: {0:.1f} %".format(per * 100))
        idx_src, px = idx_px_list[-1]
        m.setData(idx_src, px.scaled(PX_SIZE, PX_SIZE), Qt.DecorationRole)
        self.apply_pb.setValue(per * 100)

    def closeEvent(self, e):
        self.on_update_dump_config()
        r = BaseAppForm.closeEvent(self, e)

    def snapshot_tolerance_settings(self):
        """Iterate all the tolerance settings, update and save.
        """
        m = self._tv.model()
        if m is None:
            return
        src_m = m.sourceModel()
        is_changed = False
        for i in range(src_m.rowCount()):
            ename = src_m.data(src_m.index(i, src_m.i_name))
            fname = src_m.data(src_m.index(i, src_m.i_field))
            v_tol = float(src_m.data(src_m.index(i, src_m.i_tol)))
            if ename not in self._tolerance_settings:
                self._tolerance_settings[ename] = OrderedDict([(fname, v_tol)])
                is_changed = True
            else:
                if fname not in self._tolerance_settings[ename]:
                    is_changed = True
                elif self._tolerance_settings[ename][fname] != v_tol:
                    is_changed = True
                self._tolerance_settings[ename].update([(fname, v_tol)])
        if is_changed:
            self._tolerance_settings.write(self._tolerance_settings.settings_path)
            printlog("Update tolerance settings snapshot.")

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
        m.filter_ftypes = [k for k, v in self._eng_phy_toggle.items() if v is True]
        self.filter_lineEdit.editingFinished.emit()

    @pyqtSlot()
    def on_load_lattice(self):
        """Load lattice.
        """
        if self._lattice_load_window is None:
            self._lattice_load_window = LatticeWidget()
            self._lattice_load_window.latticeChanged.connect(
                self.on_lattice_changed)
            self._lattice_load_window.latticeChanged.connect(self._lattice_load_window.close)
            self._lattice_load_window.latticeChanged.connect(self.show_init_settings_info)
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
            self._lv.setWindowTitle("{} ({})".format(__title__, self.getAppTitle()))
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
                msg = '<html><head/><body><p><span style=" color:#007bff;">Selected text: </span><span style=" color:#dc3545;">{}</span><span style=" color:#007bff;">, paste with middle button.</span></p></body></html>'.format(text)
                self.statusInfoChanged.emit(msg)
                self._reset_status_info()

    def on_click_view(self, idx):
        r, c = idx.row(), idx.column()
        m = self._tv.model()
        src_m = m.sourceModel()
        src_idx = m.mapToSource(idx)
        src_r, src_c = src_idx.row(), src_idx.column()
        printlog("Index of PxyModel ({}, {}), text: {}".format(
            r, c, str(m.data(idx))))
        printlog("Index of SrcModel ({}, {}), text: {}".format(
            src_r, src_c, str(src_m.data(src_idx))))

        item = src_m.itemFromIndex(src_idx)
        printlog("Clicked: ({}, {}), item is expanded? ({}), is checked? ({})".format(
            idx.row(), idx.column(), self._tv.isExpanded(idx),
            is_item_checked(item)))

        if idx.column() == src_m.i_name:
            ename_item = src_m.itemFromIndex(src_idx)
            if hasattr(ename_item, 'fobj'):
                fobj = ename_item.fobj
                printlog("Auto-monitor on? ", fobj.get_auto_monitor())

    @pyqtSlot()
    def on_filter_changed(self):
        m = self._tv.model()
        if m is None:
            return
        s = self.sender().text().strip()
        k = None
        kv = s.split('=', 1)
        if len(kv) == 2:
            k, v = kv[0].strip(), kv[1].strip()
        else:
            v = s
        if v == '':
            v = '*'
        m.sourceModel().set_filter_key(k)

        # Qt >= 5.12
        # re_str = QRegularExpression.wildcardToRegularExpression(v)
        # m.setFilterRegularExpression(re_str)

        # m.setFilterRegExp(QRegExp(v, Qt.CaseSensitive,
        #                          QRegExp.WildcardUnix))

        if k in VALID_FILTER_KEYS_NUM:
            m.setFilterRegExp(v)
        else:
            m.setFilterRegExp(fnmatch.translate(v))

        self.total_show_number_lbl.setText(str(m.rowCount()))
        self.update_filter_completer(s)

    @pyqtSlot()
    def on_load(self):
        """Load settings from file."""
        filepath, ext = get_open_filename(self,
                                          caption="Load Settings from a File",
                                          type_filter="CSV Files (*.csv);;JSON Files (*.json);;HDF5 Files (*.h5)")
        if filepath is None:
            return

        self.load_file(filepath, ext)

    def load_file(self, filepath, ext):
        ext = ext.upper()
        try:
            if ext == 'CSV':
                self._load_settings_from_csv(filepath)
            elif ext == 'JSON':
                self._load_settings_from_json(filepath)
            elif ext == 'H5':
                self._load_settings_from_h5(filepath)
        except RuntimeError:
            pass
        else:
            msg = "Loaded data from {}".format(filepath)
            self.statusInfoChanged.emit(msg)
            self._reset_status_info(5000)
            QMessageBox.information(
                self, "Load Settings File", msg)
            printlog(msg)
        finally:
            self.clear_cast_status()

    def _load_settings_from_csv(self, filepath):
        table_settings = TableSettings(filepath)

        if self._lat is None:
            mach = table_settings.meta.get('machine', DEFAULT_MACH)
            segm = table_settings.meta.get('segment', DEFAULT_SEGM)
            self.__load_lattice(mach, segm)

        lat = self.__init_lat
        s = make_physics_settings(table_settings, lat)
        lat.settings.update(s)
        self._elem_list = [lat[ename] for ename in s]
        self.element_list_changed.emit()

    def __load_lattice(self, mach, segm):
        self.actionLoad_Lattice.triggered.emit()
        self._lattice_load_window.mach_cbb.setCurrentText(mach)
        self._lattice_load_window.seg_cbb.setCurrentText(segm)
        loop = QEventLoop()
        self._lattice_load_window.latticeChanged.connect(loop.exit)
        self._lattice_load_window.load_btn.clicked.emit()
        loop.exec_()

    def _load_settings_from_json(self, filepath):
        pass

    def _load_settings_from_h5(self, filepath):
        pass

    @pyqtSlot()
    def on_config_updated(self):
        """config from Preferences is changed, model settings, tolerance
        settings, element PV config.
        """
        confdir = self.pref_dict['config_path']
        _, ts_confpath, ms_confpath, elem_confpath = init_config_dir(confdir)

        # tolerance settings (ts)
        self._tolerance_settings = ToleranceSettings(ts_confpath)

        # predefined model settings (ms)
        self._model_settings = Settings(self.ms_confpath)

        # elements from PVs
        self._elem_pvconf = ElementPVConfig(self.elem_confpath)

        self.__init_lat = self.build_lattice()

    @pyqtSlot(bool)
    def on_toggle_init_lattice_settings(self, enabled):
        """If checked, to initialize device settings with entire loaded lattice.
        """
        self.init_settings = enabled
        self.pref_dict['init_settings'] = enabled
        if enabled and self._mp is not None:
            self._elem_list = self._lat[:]
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
        pref_dlg = PreferencesDialog(self, self.pref_dict)
        pref_dlg.pref_changed.connect(self.on_update_pref)
        pref_dlg.visibility_changed.connect(self.on_update_visibility)
        pref_dlg.config_changed.connect(self.on_config_updated)
        pref_dlg.font_changed.connect(self.font_changed)
        pref_dlg.init_settings_changed.connect(self.init_settings_changed)
        pref_dlg.ndigit_sbox.valueChanged.connect(self.ndigit_sbox.setValue)
        pref_dlg.wdir_changed.connect(self.on_wdir_changed)
        r = pref_dlg.exec_()
        # if r == QDialog.Accepted:
        #     printlog("Updated pref --> {}".format(self.pref_dict))
        # else:
        #     printlog("Unchanged pref: {}".format(self.pref_dict))

    @pyqtSlot(dict)
    def on_update_pref(self, d):
        """Update app preferences.
        """
        self.pref_dict.update(d)
        self.field_init_mode = self.pref_dict['field_init_mode']
        self.t_wait = self.pref_dict['t_wait']
        self.init_settings = self.pref_dict['init_settings']
        tol = self.pref_dict['tolerance']
        if self.tolerance != tol:
            r = QMessageBox.question(self, "Change Tolerance",
                    "Are you sure to change all the discrepancy tolerance to {0:.2f}?".format(tol),
                    QMessageBox.Yes | QMessageBox.No)
            if r == QMessageBox.Yes:
                self.tolerance_changed[float].emit(tol)
                self.tolerance = tol
        dt_confsync = self.pref_dict['dt_confsync']
        if dt_confsync != self.dt_confsync:
            self.config_timer.stop()
            self.dt_confsync = dt_confsync
            # self.config_timer.start(self.dt_confsync * 1000)
        ndigit = self.pref_dict['ndigit']
        if ndigit != self.ndigit:
            self.ndigit_changed.emit(ndigit)

    @pyqtSlot('QString')
    def on_wdir_changed(self, d):
        # reset snp dock with files in d (recursively)
        self.wdir = d
        self._snp_dock_list = []
        self._snapshots_count = i = 0
        for root, dnames, fnames in os.walk(d):
            for fname in fnmatch.filter(fnames, "*.csv"):
                path = os.path.join(root, fname)
                table_settings = TableSettings(path)
                snp_data = SnapshotData(table_settings)
                snp_data.name = table_settings.meta.get('name', None)
                if is_snp_data_exist(snp_data, self._snp_dock_list):
                    continue
                snp_data.note = table_settings.meta.get('note', None)
                snp_data.filepath = table_settings.meta.get('filepath', path)
                snp_data.timestamp = table_settings.meta.get('timestamp', None)
                i += 1
                self._snp_dock_list.append(snp_data)
        self._snapshots_count += i
        self.snp_dock.setVisible(self._snapshots_count!=0)
        self.update_snp_dock_view()
        self.wdir_lineEdit.setText(self.wdir)
        self.total_snp_lbl.setText(str(i))

    @pyqtSlot(int)
    def on_ndigit_changed(self, n):
        self.ndigit = n
        self.fmt = '{{0:.{0}f}}'.format(n)
        self.element_list_changed.emit()

    @pyqtSlot(int)
    def on_update_rate(self, i):
        # update_rate_cbb index
        self.rate_changed.emit(i)

    def start_auto_update(self):
        # updating independently,
        # _update_mode: 'auto'
        printlog("Executing start_auto_update()...")

    def stop_auto_update(self):
        # stop auto updating.
        printlog("Executing stop_auto_update()...")

    def start_thread_update(self):
        # Update values every *delt* second(s),
        # _update_mode: 'thread'

        if self._tv.model() is None:
            return

        if self._stop_update_thread:
            return

        delt = self._update_delt
        m = self._tv.model().sourceModel()
        self.updater = DAQT(daq_func=partial(self.update_value_single, m, delt),
                            daq_seq=range(1))
        self.updater.meta_signal1.connect(partial(
            self.on_update_display, m))
        self.updater.finished.connect(self.start_thread_update)
        self.updater.start()

    def update_value_single(self, m, delt, iiter):
        # update data tree for one time, iterate all items.
        if delt == 0:
            worker = self.one_updater
        elif delt == -1:
            worker = self._updater
        else:
            worker = self.updater
        t0 = time.time()
        for o, it in zip(self._fld_obj + self._pv_obj, self._fld_it + self._pv_it):
            if not isinstance(o, CaField):  # PV
                val = o.get()
                for iit in it:
                    idx = m.indexFromItem(iit)
                    worker.meta_signal1.emit((idx, self.fmt.format(val), Qt.DisplayRole))
            else:  # CaField
                idx0 = m.indexFromItem(it[0])
                idx1 = m.indexFromItem(it[1])
                irow = idx0.row()
                rd_val, sp_val = o.value, o.current_setting()
                x0_idx = m.index(irow, m.i_val0)
                x1_idx = m.index(irow, m.i_rd)
                x2_idx = m.index(irow, m.i_cset)
                tol_idx = m.index(irow, m.i_tol)
                dx01_idx = m.index(irow, m.i_val0_rd)
                dx02_idx = m.index(irow, m.i_val0_cset)
                dx12_idx = m.index(irow, m.i_rd_cset)
                x0 = float(m.data(x0_idx))
                x1 = float(m.data(x1_idx))
                x2 = float(m.data(x2_idx))
                dx01 = x0 - x1
                dx02 = x0 - x2
                dx12 = x1 - x2
                wa_idx = m.index(irow, m.i_writable)
                wa = o.write_access
                idx_tuple = (idx0, idx1, dx01_idx, dx02_idx, dx12_idx)
                v_tuple = (rd_val, sp_val, dx01, dx02, dx12)
                for iidx, val in zip(idx_tuple, v_tuple):
                    worker.meta_signal1.emit((iidx, self.fmt.format(val), Qt.DisplayRole))
                worker.meta_signal1.emit((wa_idx, str(wa), Qt.DisplayRole))
                tol = float(m.data(tol_idx))
                if abs(dx12) > tol:
                    diff_status_px = self._warning_px
                else:
                    diff_status_px = self._ok_px
                worker.meta_signal1.emit((dx12_idx, diff_status_px.scaled(PX_SIZE, PX_SIZE), Qt.DecorationRole))

        dt = time.time() - t0
        dt_residual = delt - dt
        if delt == 0:
            printlog("Single update in {0:.1f} msec, no wait.".format(dt * 1000))
        else:
            if dt_residual > 0:
                time.sleep(dt_residual)
                printlog("Waited {0:.0f} msec.".format(dt_residual * 1000))
            else:
                printlog("Rate is {0:.1f} Hz.".format(1.0 / dt))

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
            # chances auto update be set after loading settings from file,
            # so stop it.
            self.stop_auto_update()
            self._stop_update_thread = True
            printlog("Stop thread updating.")
        else:
            self.stop_auto_update()
            printlog("Stop auto updating.")

    @pyqtSlot()
    def on_reset_set_status(self):
        self._tv.model().sourceModel().reset_icon.emit()

    @pyqtSlot(bool)
    def on_expand_collapse_view(self, expanded):
        if expanded:
            self._tv.expandAll()
            tt = "Click to collapse all."
        else:
            self._tv.collapseAll()
            tt = "Click to expand all."
        self.sender().setToolTip(tt)

    @pyqtSlot(bool)
    def on_snp_expand_collapse(self, expanded):
        if expanded:
            self.snp_treeView.expandAll()
            tt = "Click to collapse all."
        else:
            self.snp_treeView.collapseAll()
            tt = "Click to expand all."
        self.sender().setToolTip(tt)

    @pyqtSlot()
    def on_select(self, mode):
        if mode == 'all':
            # select all
            self._tv.model().select_all()
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
        # debug
        # print(selections)

    @pyqtSlot(bool)
    def on_pv_mode_toggled(self, is_checked):
        # pv mode: True, element mode: False
        self._pv_mode = is_checked

    @pyqtSlot()
    def on_add_devices(self):
        # Add devices, high-level fields or PV elements.
        if self._elem_select_dlg is None:
            self._elem_select_dlg = ElementSelectDialog(self, "multi", mp=self._mp)
            self._elem_select_dlg.selection_changed.connect(self.on_device_selected)
            self._elem_select_dlg.pv_mode_toggled.connect(self.on_pv_mode_toggled)
            self.lattice_loaded.connect(self._elem_select_dlg.on_update_elem_tree)

        r = self._elem_select_dlg.exec_()
        if r == QDialog.Accepted:
            if not self._pv_mode:
                sel_elems, sel_elems_dis, sel_fields = self._elem_selected

                is_added_list = []
                for i in sel_elems_dis:
                    self.__init_lat.append(i)
                    is_added_list.append(self.add_element(i))
                is_added = True in is_added_list
            else:
                sel_elems, _, _ = self._elem_selected
                pv_elem = sel_elems[0]
                elem = build_element(pv_elem.setpoint[0], pv_elem.readback[0])
                self.__init_lat.append(elem)
                is_added = self.add_element(elem)
                if is_added:
                    self.element_from_pv_added.emit(elem)
            if is_added:
                self.element_list_changed.emit()

    def build_lattice(self):
        """Build a sequence of high-level elements from PV configs defined by
        *elem_pvconf*, the model settings of the new elements are pulled from
        model_settings if available.

        Returns
        -------
        r : Lattice
            Initialized high-level lattice object.
        """
        # load mp
        # add elements from elem_pvconf
        lat = Lattice(self.__class__)
        ms = self._model_settings
        for ename, conf in self._elem_pvconf.items():
            field_eng = conf['field']
            field_phy = conf['field_phy']
            sp_pv = conf['setpoint']
            rd_pv = conf['readback']
            index = conf['index']
            length = conf['length']
            family = conf['family']
            sb = conf['sb']
            elem = build_element(sp_pv, rd_pv, ename=ename, fname=field_eng,
                                 field_phy=field_phy, index=index,
                                 length=length, sb=sb, family=family)
            lat.append(elem)
            if ename in ms:
                lat.settings[ename] = ms[ename]
        return lat

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
        m.data_changed.emit(res)

    @pyqtSlot()
    def on_single_update(self):
        """Update values, indicators for one time."""
        if self._tv.model() is None:
            return
        m = self._tv.model().sourceModel()
        self.one_updater = DAQT(daq_func=partial(self.update_value_single, m, 0),
                                daq_seq=range(1))
        self.one_updater.meta_signal1.connect(partial(
            self.on_update_display, m))
        self.one_updater.daqStarted.connect(partial(
            self.set_widgets_status_for_updating, 'START'))
        self.one_updater.finished.connect(partial(
            self.set_widgets_status_for_updating, 'STOP'))
        self.one_updater.start()

    def set_widgets_status_for_updating(self, status):
        """Set widgets status for updating.
        """
        w1 = (self.update_ctrl_btn, self.update_rate_cbb, self.apply_btn,
              self.single_update_btn, self.ndigit_sbox, self.snp_dock)
        [i.setDisabled(status == 'START') for i in w1]

    def set_widgets_status_for_applying(self, status):
        """Set widgets status for applying.
        """
        w1 = (self.apply_btn,)
        [i.setDisabled(status == 'START') for i in w1]

    def sizeHint(self):
        return QSize(1300, 975)

    @pyqtSlot(list)
    def on_delete_items(self, fobj_list):
        """Delete the element(s) from element list by given field object list.
        """
        for fobj in fobj_list:
            elem = self.__init_lat[fobj.ename]
            # !! note: delete both ENG/PHY fields even if any one of ENG/PHY is deleted.
            if elem in self._elem_list:
                self._elem_list.remove(elem)
        self.element_list_changed.emit()

    @pyqtSlot()
    def on_update_dump_config(self):
        """Update and dump configurations.
        """
        # printlog("Update and dump configurations...")
        self.snapshot_tolerance_settings()

    @pyqtSlot(Settings)
    def on_model_settings_changed(self, settings):
        """Update and dump model settings.
        """
        if settings != self._model_settings:
            self._model_settings.update(settings)
            self._model_settings.write(self.ms_confpath)
            printlog("Update model settings snapshot.")

    @pyqtSlot(bool)
    def on_toggle_all_selected(self, selected):
        m = self._tv.model()
        if m is None:
            return
        m.filter_checked_enabled = selected
        self.filter_lineEdit.editingFinished.emit()

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        urls = e.mimeData().urls()
        i = 0
        for url in urls:
            path = url.toLocalFile()
            ext = path.rsplit('.', 1)[-1]
            if ext.upper() != 'CSV':
                continue
            table_settings = TableSettings(path)
            snp_data = SnapshotData(table_settings)
            snp_data.name = table_settings.meta.get('name', None)
            if is_snp_data_exist(snp_data, self._snp_dock_list):
                continue
            snp_data.note = table_settings.meta.get('note', None)
            snp_data.filepath = table_settings.meta.get('filepath', path)
            snp_data.timestamp = table_settings.meta.get('timestamp', None)
            i += 1
            self._snp_dock_list.append(snp_data)
        self._snapshots_count += i
        self.snp_dock.setVisible(self._snapshots_count!=0)
        self.update_snp_dock_view()
        #
        # self.load_file(path, ext)
        # cast last one
        self.on_cast_settings(snp_data)
        self.total_snp_lbl.setText(str(i))

    @pyqtSlot(int, bool)
    def on_update_visibility(self, idx, f):
        self._tv.setColumnHidden(idx, f)

    @pyqtSlot()
    def on_take_settings_snapshot(self):
        """Take current settings, update 'Setpoint(x0)' column.
        """
        m = self._tv.model()
        if m is None:
            return
        src_m = m.sourceModel()
        # single update
        self._updater = DAQT(daq_func=partial(self.update_value_single, src_m, -1),
                                daq_seq=range(1))
        self._updater.meta_signal1.connect(partial(self.on_update_display, src_m))
        self._updater.daqStarted.connect(partial(self.set_widgets_status_for_updating, 'START'))
        self._updater.finished.connect(partial(self.set_widgets_status_for_updating, 'STOP'))
        loop = QEventLoop()
        self._updater.finished.connect(loop.exit)
        self._updater.start()
        loop.exec_()
        #
        current_sp_idx = src_m.i_cset
        stored_sp_idx = src_m.i_val0
        for i in range(m.rowCount()):
            sp_val_str = m.data(m.index(i, current_sp_idx))
            m.setData(m.index(i, stored_sp_idx), sp_val_str)
        self.incr_snapshots_count()

    @pyqtSlot()
    def on_show_query_tips(self):
        if self._query_tips_form is None:
            self._query_tips_form = w = QWidget()
            ui = QueryTipsForm()
            ui.setupUi(w)
            w.setWindowTitle("Query Tips")
        self._query_tips_form.show()

    @pyqtSlot(int)
    def on_snapshots_changed(self, i):
        """Number of runtime snapshots is changed.
        """
        self.snp_dock.setVisible(i!=0)
        self.wdir_lineEdit.setText(self.wdir)
        self.total_snp_lbl.setText(str(i))
        # update snpdata to snp dock.
        if self._tv.model() is None:
            return
        sp = self.beam_display_widget.get_species()
        snp_data = SnapshotData(get_csv_settings(self._tv.model()),
                wdir = self.wdir,
                ion=f'{sp[1]}{sp[0]}{sp[2]}+{sp[3]}',
                machine=self._last_machine_name, segment=self._last_lattice_name,
                filter=self.filter_lineEdit.text())
        self._snp_dock_list.append(snp_data)
        self.update_snp_dock_view()
        self.on_cast_settings(snp_data)
        self.total_snp_lbl.setText(str(i))

    def incr_snapshots_count(self, incr=1):
        self._snapshots_count += incr
        self.snapshots_number_changed.emit(self._snapshots_count)

    def update_snp_dock_view(self):
        m = SnapshotDataModel(self.snp_treeView, self._snp_dock_list)
        m.set_model()
        self.snp_expand_btn.toggled.emit(self.snp_expand_btn.isChecked())
        m.save_settings.connect(self.on_save_settings)
        self.snp_saved.connect(m.on_snp_saved)
        m.cast_settings.connect(self.on_cast_settings)
        self.snp_casted['QString'].connect(m.on_snp_casted)

    def on_save_settings(self, data):
        # data: SnapshotData
        # settings(data.data): TableSettings
        if data.filepath is None:
            cdir = data.wdir
        else:
            cdir = data.filepath
        filename, ext = get_save_filename(self,
                                          caption="Save Settings to a File",
                                          cdir=cdir,
                                          type_filter="CSV Files (*.csv);;JSON Files (*.json);;HDF5 Files (*.h5)")
        if filename is None:
            return
        settings = data.data
        settings.meta.update({
            'filepath': filename,
        })
        for k, v in zip(('app', 'version', 'user', 'machine', 'segment'),
             ('Settings Manager', f'{self._version}', getuser(),
               self._last_machine_name, self._last_lattice_name)):
                 if not k in settings.meta:
                     settings.meta.update({k: v})
        settings.write(filename, header=CSV_HEADER)
        self.snp_saved.emit(data.name, filename)

    def on_cast_settings(self, data):
        # data: SnapshotData
        # settings(data.data): TableSettings
        settings = data.data
        if self._lat is None:
            mach = settings.meta.get('machine', DEFAULT_MACH)
            segm = settings.meta.get('segment', DEFAULT_SEGM)
            self.__load_lattice(mach, segm)
        lat = self.__init_lat
        table_settings = data.data
        s = make_physics_settings(table_settings, lat)
        lat.settings.update(s)
        self._elem_list = [lat[ename] for ename in s]
        self.element_list_changed.emit()
        self.snp_casted['QString'].emit(data.name)

    def clear_cast_status(self):
        # Clear cast status in snp dock.
        if not self.snp_dock.isVisible():
            return
        self.snp_treeView.model().clear_cast_status()

    @pyqtSlot()
    def onFixCorNames(self):
        # ! only needed for ancient saved csv files before phantasy-machines commits (39c94e5)
        from .app_fixnames import FixNamesDialog
        if self._fixnames_dlg is None:
            self._fixnames_dlg = FixNamesDialog(self)
        self._fixnames_dlg.show()


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
