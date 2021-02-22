#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import fnmatch
import json
import os
import re
import tempfile
import time
from collections import OrderedDict
from datetime import datetime
from functools import partial
from getpass import getuser

from PyQt5.QtCore import QEventLoop
from PyQt5.QtCore import QFileSystemWatcher
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QKeySequence
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtWidgets import QWidget
from phantasy import CaField
from phantasy import Settings
from phantasy import build_element
from phantasy import Lattice
from phantasy_ui import BaseAppForm
from phantasy_ui import delayed_exec
from phantasy_ui import get_open_filename
from phantasy_ui import get_save_filename
from phantasy_ui import printlog
from phantasy_ui import milli_sleep
from phantasy_ui.widgets import is_item_checked
from phantasy_ui.widgets import BeamSpeciesDisplayWidget
from phantasy_ui.widgets import DataAcquisitionThread as DAQT
from phantasy_ui.widgets import ElementSelectDialog
from phantasy_ui.widgets import FlowLayout
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
from .data import read_data
from .ui.ui_app import Ui_MainWindow
from .ui.ui_query_tips import Ui_Form as QueryTipsForm
from .utils import FMT
from .utils import ELEMT_PX_MAP
from .utils import TBTN_STY_REGULAR
from .utils import TBTN_STY_GOLDEN
from .utils import SettingsModel
from .utils import pack_settings
from .utils import str2float
from .utils import get_ratio_as_string
from .utils import init_config_dir
from .utils import VALID_FILTER_KEYS
from .utils import VALID_FILTER_KEYS_NUM
from .utils import SnapshotDataModel
from .data import DEFAULT_MACHINE, DEFAULT_SEGMENT

NPROC = 4
PX_SIZE = 24
ION_ICON_SIZE = 48
DATA_SRC_MAP = {'model': 'model', 'live': 'control'}
IDX_RATE_MAP = {0: 1.0, 1: 2.0, 2: 5.0, 3: 0.5, 4: 0.2, 5: 0.1}
FILTER_TT = """\
Filter strings 'keyword=pattern', multiple conditions could be linked with 'and', support 'in'
test. More details please click the right help button."""
TS_FMT = "%Y-%m-%dT%H:%M:%S.%f"
_, LOG_FILE = tempfile.mkstemp(datetime.now().strftime(TS_FMT), "settings_manager_setlog_", "/tmp")


class SettingsManagerWindow(BaseAppForm, Ui_MainWindow):
    # settings view filter button group status (or) changed --> update
    filter_btn_group_status_changed = pyqtSignal()

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
    snapshots_changed = pyqtSignal()

    # snp saved, snpdata name, filepath
    snp_saved = pyqtSignal('QString', 'QString')

    # snp loaded, snpdata
    snp_loaded = pyqtSignal(SnapshotData)

    # snp filter (snp dock)
    snp_filters_updated = pyqtSignal()

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

        #
        self.show()
        self.preload_lattice(DEFAULT_MACHINE, DEFAULT_SEGMENT)

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

    @pyqtSlot()
    def on_auto_column_width(self):
        # auto adjust column width
        m = self._tv.model()
        if m is None:
            return
        m.m_src.fit_view()

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

        self._lat = self.__init_lat + self._lat
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
            QMessageBox.information(self, "Loaded Lattice",
                                    '<html><head/><body><p>Lattice is loaded, add device settings '
                                    'via <span style=" font-style:italic;">Add Devices</span> or '
                                    '<span style=" font-style:italic;">Load Settings </span>tools,'
                                    ' or check <span style=" font-style:italic;">Initialize with '
                                    'loaded lattice</span> in the right bottom window area to '
                                    'list all the devices.</p></body></html>',
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
                              ndigit=self.ndigit, font=self.font,
                              auto_fmt=self.auto_ndigit_chkbox.isChecked())
        model.settings_sts.connect(self.on_settings_sts)
        model.item_deletion_updated[list].connect(self.on_delete_items)
        model.set_model()
        self._fld_obj = model._fld_obj
        self._fld_it = model._fld_it

        self.obj_it_tuple = tuple(zip(self._fld_obj, self._fld_it))

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

    def __post_init_ui(self):
        # hide sts info
        self.show_sts_btn.setChecked(False)
        # add beamSpeciesDisplayWidget
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolBar.addWidget(spacer)
        self.beam_display_widget = BeamSpeciesDisplayWidget()
        self.toolBar.addWidget(self.beam_display_widget)
        #
        self._post_info = True  # post info after loading lattice
        #
        self._tv = self.settingsView
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

        # snp dock
        self.snp_dock.closed.connect(lambda:self.actionSnapshots.setChecked(False))
        self.actionSnapshots.setChecked(True)

        # show lattice settings
        self.settingsLoaded.connect(self.on_settings_loaded)

        # update rate
        self.rate_changed.connect(self.on_update_rate_changed)
        self.update_rate_cbb.currentIndexChanged.emit(
            self.update_rate_cbb.currentIndex())

        # icon
        self.done_px = QPixmap(":/sm-icons/done.png")
        self.fail_px = QPixmap(":/sm-icons/fail.png")
        self._warning_px = QPixmap(":/sm-icons/warning.png")
        self._ok_px = QPixmap(":/sm-icons/ok.png")
        self._copy_text_icon = QIcon(QPixmap(":/sm-icons/copy_text.png"))
        self._copy_data_icon = QIcon(QPixmap(":/sm-icons/copy_data.png"))
        self._probe_icon = QIcon(QPixmap(":/sm-icons/probe.png"))
        self._unsel_icon = QIcon(QPixmap(":/sm-icons/uncheck.png"))
        self._sel_icon = QIcon(QPixmap(":/sm-icons/check.png"))
        self._sel3_icon = QIcon(QPixmap(":/sm-icons/check3.png"))
        self._saveas_icon = QIcon(QPixmap(":/sm-icons/save.png"))
        self._read_icon = QIcon(QPixmap(":/sm-icons/readfile.png"))
        self._reveal_icon = QIcon(QPixmap(":/sm-icons/openfolder.png"))
        self._del_icon = QIcon(QPixmap(":/sm-icons/delete.png"))
        self._load_icon = QIcon(QPixmap(":/sm-icons/cast.png"))
        self._pwr_on_px = QPixmap(":/sm-icons/on.png")
        self._pwr_off_px = QPixmap(":/sm-icons/off.png")
        self._pwr_unknown_px = QPixmap(":/sm-icons/unknown.png")

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
        self._snp_dock_list = []  # for snp_treeView
        self.snapshots_changed.connect(lambda:self.on_snapshots_changed())
        self.snapshots_changed.emit()

        # apply pb
        self.apply_pb.setVisible(False)
        # refresh pb
        self.refresh_pb.setVisible(False)

        # current snp lbl/le
        self._current_snpdata = None
        for i in (self.current_snp_lbl, self.current_snp_lineEdit):
            i.setVisible(False)

        # snp filters, {btn_text (elemt, tag):ischecked?}
        self._current_btn_filter = dict()
        self._current_tag_filter = dict()
        self.snp_filters_updated.connect(self.on_snp_filters_updated)
        #
        self.fm = QFileSystemWatcher([self.wdir], self)
        self.fm.directoryChanged.connect(self.on_wdir_new)
        # working directory
        self.on_wdir_changed(True, self.wdir)

        # take snapshot tool
        self.actionTake_Snapshot.triggered.connect(lambda:self.take_snapshot())

        # scaling factor hint
        self.snp_loaded.connect(self.on_hint_scaling_factor)
        #
        self.snp_loaded.connect(self.on_snp_loaded)
        self.snp_saved.connect(self.on_snp_saved)

        # log dock
        self.log_dock.closed.connect(lambda:self.actionShow_Device_Settings_Log.setChecked(False))
        self.actionShow_Device_Settings_Log.setChecked(False)

        # hide findtext_lbl and findtext_lineEdit
        for o in (self.findtext_lbl, self.findtext_lineEdit):
            o.setVisible(False)
        # hide save/load settings tools
        for o in (self.actionLoad_Settings, self.action_Save):
            o.setVisible(False)

        # snp wdir new?
        self.snp_new_lbl.setPixmap(QPixmap(":/sm-icons/new.png").scaled(PX_SIZE, PX_SIZE))
        self.snp_new_lbl.setVisible(False)

        # expand all snps
        self.snp_expand_btn.setChecked(True)

        # tag,ions filters, radiobtn
        self.select_all_ions_btn.clicked.connect(partial(self.on_snp_filters_select_all_ions, True))
        self.select_none_ions_btn.clicked.connect(partial(self.on_snp_filters_select_all_ions, False))
        self.select_all_tags_btn.clicked.connect(partial(self.on_snp_filters_select_all_tags, True))
        self.select_none_tags_btn.clicked.connect(partial(self.on_snp_filters_select_all_tags, False))

        # settings view filter btn status
        self.filter_btn_group_status_changed.connect(self.on_filter_btn_group_status_changed)
        self.filter_btn_group_status_changed.emit()

    @pyqtSlot()
    def on_filter_btn_group_status_changed(self):
        # Do logic 'or', if True, do global refresh when data refresher is on.
        self._filter_btn_enabled = self.show_warning_dx02_btn.isChecked() \
                or self.show_warning_dx12_btn.isChecked()

    def resizeEvent(self, e):
        self.resizeDocks([self.snp_dock], [self.width() * 0.5],
                          Qt.Horizontal)
        BaseAppForm.resizeEvent(self, e)

    def on_snp_filters_select_all_tags(self, is_checked):
        for i in self.tag_filter_area.findChildren(QToolButton):
            i.setChecked(is_checked)

    def on_snp_filters_select_all_ions(self, is_checked):
        l = self.snp_filter_hbox
        for i in range(l.count()):
            w = l.itemAt(i).widget()
            if w is None:
                continue
            w.setChecked(is_checked)

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
            o.customContextMenuRequested.connect(partial(self.on_custom_context_menu, o))

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
            w = ProbeWidget(element=elem, detached=False)
            self._probe_widgets_dict[ename] = w
        w = self._probe_widgets_dict[ename]
        w.show()
        w.set_field(fname)

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
        menu.addAction(copy_action)
        #
        item0 = src_m.itemFromIndex(src_m.index(src_idx.row(), src_m.i_ts, pindex))
        #
        if not hasattr(item0, 'snp_data'):
            return menu
        snpdata = item0.snp_data
        # copy data
        dcopy_action = QAction(self._copy_data_icon, "Copy Data", menu)
        dcopy_action.triggered.connect(partial(self.on_copy_snp, snpdata))
        # save-as
        saveas_action = QAction(self._saveas_icon, "E&xport", menu)
        saveas_action.triggered.connect(partial(self.on_saveas_settings, snpdata))
        # read
        read_action = QAction(self._read_icon, "&Read", menu)
        read_action.triggered.connect(partial(self.on_read_snp, snpdata))
        # reveal
        reveal_action = QAction(self._reveal_icon, "Show in &Files", menu)
        reveal_action.triggered.connect(partial(self.on_reveal_snp, snpdata))
        # del
        del_action = QAction(self._del_icon, "&Delete", menu)
        del_action.triggered.connect(partial(self.on_del_settings, snpdata))
        # load
        load_action = QAction(self._load_icon, "&Load", menu)
        load_action.triggered.connect(partial(self.on_load_settings, snpdata))
        #
        menu.insertAction(copy_action, load_action)
        menu.insertAction(copy_action, dcopy_action)
        menu.addSeparator()
        menu.addAction(read_action)
        menu.addAction(reveal_action)
        menu.addSeparator()
        menu.addAction(saveas_action)
        menu.addAction(del_action)
        return menu

    def _build_settings_context_menu(self, idx, m):
        src_m = m.sourceModel()
        src_idx = m.mapToSource(idx)
        item = src_m.itemFromIndex(src_idx)
        text = item.text()
        #
        menu = QMenu(self)
        menu.setStyleSheet('QMenu {margin: 2px;}')

        #
        copy_action = QAction(self._copy_text_icon, "Copy Text", menu)
        copy_action.triggered.connect(partial(self.on_copy_text, m, idx))
        menu.addAction(copy_action)

        #
        if hasattr(item, 'fobj'):
            ename = text
            elem = self._lat[ename]
            fld = item.fobj
            probe_action = QAction(self._probe_icon, "Probe Element", menu)
            probe_action.triggered.connect(
                    partial(self.on_probe_element, elem, fld.name))
            menu.addAction(probe_action)

        # toggle items action
        selected_rows = {idx.row() for idx in self._tv.selectedIndexes()}

        selected_rows = []
        checked_status = []
        for _idx in self._tv.selectedIndexes():
            if _idx.column() == src_m.i_name:
                selected_rows.append(_idx.row())
                checked_status.append(is_item_checked(src_m.itemFromIndex(m.mapToSource(_idx))))

        n_rows = len(selected_rows)
        _item0 = src_m.itemFromIndex(src_m.index(src_idx.row(), src_m.i_name))
        is_checked = is_item_checked(_item0)
        if n_rows == 1:
            row_text = 'Row'
        else:
            row_text = 'Rows'
        if is_checked:
            new_check_state = Qt.Unchecked
            act_text = f"Uncheck All ({n_rows}) {row_text}"
        else:
            new_check_state = Qt.Checked
            act_text = f"Check All ({n_rows}) {row_text}"

        if all(checked_status):
            act_icon = self._unsel_icon
        elif not any(checked_status):
            act_icon = self._sel_icon
        else:
            act_icon = self._sel3_icon

        sel_action = QAction(act_icon, act_text, menu)
        sel_action.triggered.connect(partial(self.on_toggle_selected_rows,
                                     selected_rows, m, src_m, new_check_state))
        menu.addAction(sel_action)
        return menu

    @pyqtSlot()
    def on_toggle_selected_rows(self, selected_rows, m, m_src, new_check_state):
        for i in selected_rows:
            idx = m.mapToSource(m.index(i, 0))
            it = m_src.itemFromIndex(idx)
            if it.isEnabled():
                it.setCheckState(new_check_state)

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
            self._elem_list, self._lat,
            settings=self._lat.settings,
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
        if i == 6:  # add 'auto' back to cbb index 6
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
        m = self._tv.model()
        if m is None:
            return
        if not self._eval_scaling_factor:
            self.scaling_factor_lineEdit.returnPressed.emit()

        # scaling factor
        scaling_factor = float(self.scaling_factor_lineEdit.text())
        #
        self.idx_px_list = []  # list to apply icon [(idx_src, px, log_msg)]
        settings_selected = m.get_selection()
        if len(settings_selected) == 0:
            QMessageBox.warning(self, "Apply Settings",
                    '<html><head/><body><p>Not any items are checked, <span style=" '
                    'font-style:italic;">Apply </span>only work with checked items<span style=" '
                    'font-style:italic;">.</span></p></body></html>',
                    QMessageBox.Ok)
            return

        # ask if want to take a snapshot of current settings of all checked devices
        r = QMessageBox.question(self, "Take Snapshot",
                                 "Do you want to take a snapshot before changing devices?",
                                 QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.Yes:
            # take a snapshot
            self.take_snapshot(cast=False, only_checked_items=False, post_current_sp=False)
            msg = "Taked snapshot, now start to set device settings."
        else:
            msg = "Now start to set device settings."

        r = QMessageBox.information(self, "Apply Settings", msg, QMessageBox.Ok | QMessageBox.Cancel)
        if r == QMessageBox.Cancel:
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
        self.applyer.daqFinished.connect(lambda:self.single_update_btn.clicked.emit())
        self.applyer.start()

    def apply_single(self, sf, tuple_idx_settings):
        idx_src, settings, new_fval0 = tuple_idx_settings
        elem, fname, fld, fval0 = settings
        ename = elem.name
        # print("New fval: {}, fval0: {}".format(new_fval0, fval0))
        fval_to_set = new_fval0 * sf
        try:
            t0 = time.time()
            fval_current_settings = fld.current_setting()
            if is_close(fval_current_settings, fval_to_set, self.ndigit):
                msg = "[{0}] [Skip] Set {1:<20s} [{2}] from {3} to {4} (raw set value: {5}).".format(
                        datetime.fromtimestamp(time.time()).strftime(TS_FMT),
                        ename, fname, fval_current_settings, fval_to_set, new_fval0)
            else:
                fld.value = fval_to_set
                msg = "[{0}] Set {1:<20s} [{2}] from {3} to {4} (raw set value: {5}).".format(
                        datetime.fromtimestamp(time.time()).strftime(TS_FMT),
                        ename, fname, fval_current_settings, fval_to_set, new_fval0)
        except:
            px = self.fail_px
        else:
            px = self.done_px
            dt = self.t_wait - (time.time() - t0)
            if dt > 0:
                time.sleep(dt)
        self.idx_px_list.append((idx_src, px, msg))

    @pyqtSlot(float, 'QString')
    def on_apply_settings_progress(self, idx_px_list, m, per, str_idx):
        idx_src, _, msg = idx_px_list[-1]
        m.hlrow(idx_src)
        self.log_textEdit.append(msg)
        self.apply_pb.setValue(per * 100)

    def closeEvent(self, e):
        self.on_update_dump_config()
        # os.remove(LOG_FILE)
        BaseAppForm.closeEvent(self, e)

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

    def on_snpdock_top_level_changed(self, is_floating):
        if is_floating:
            self.sender().setWindowFlags(Qt.CustomizeWindowHint | Qt.Window |
                    Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
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
        printlog("SNP, Clicked: ({}, {}), item is expanded? ({}), is checked? ({})".format(
            idx.row(), idx.column(), self.snp_treeView.isExpanded(idx),
            is_item_checked(item)))

    def on_click_view(self, idx):
        return
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
        item0 = src_m.itemFromIndex(src_m.index(src_idx.row(), 0, item.parent().index()))
        self.on_load_settings(item0.snp_data)

    @pyqtSlot()
    def on_filter_changed(self):
        m = self._tv.model()
        if m is None:
            return
        full_str = self.filter_lineEdit.text().strip()
        filter_key_value_tuples = [] # list of tuples of k, is_number_key, v
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
            self.clear_load_status()

    def _load_settings_from_csv(self, filepath):
        table_settings = TableSettings(filepath)

        if self._lat is None:
            mach = table_settings.meta.get('machine', DEFAULT_MACHINE)
            segm = table_settings.meta.get('segment', DEFAULT_SEGMENT)
            self.__load_lattice(mach, segm)

        lat = self._lat
        s = make_physics_settings(table_settings, lat)
        lat.settings.update(s)
        self._elem_list = [lat[ename] for ename in s]
        self.element_list_changed.emit()

    def __load_lattice(self, mach, segm, post_info=True):
        self._post_info = post_info
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
        pref_dlg.wdir_changed.connect(partial(self.on_wdir_changed, True))
        r = pref_dlg.exec_()

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
    def on_wdir_changed(self, purge, d):
        # reset snp dock with files in d (recursively)
        self.wdir = d
        if purge:
            del self._snp_dock_list[:]
        for root, dnames, fnames in os.walk(d):
            for fname in fnmatch.filter(fnames, "*.csv"):
                path = os.path.join(root, fname)
                snp_data = read_data(path)
                # skip snapshot that name conflicts
                if is_snp_data_exist(snp_data, self._snp_dock_list):
                    continue
                self._snp_dock_list.append(snp_data)
        self.update_snp_dock_view()
        self.wdir_lineEdit.setText(self.wdir)
        n = len(self._snp_dock_list)
        self.total_snp_lbl.setText(str(n))
        #
        self.fm.removePaths(self.fm.directories())
        self.fm.addPath(self.wdir)
        # current snp
        if self._current_snpdata is not None:
            self.snp_loaded.emit(self._current_snpdata)
        self.snp_filters_updated.emit()

    @pyqtSlot(int)
    def on_ndigit_changed(self, n):
        self.ndigit = n
        self.fmt = '{{0:.{0}f}}'.format(n)
        self.element_list_changed.emit()

    @pyqtSlot(bool)
    def on_auto_ndigit(self, enabled):
        # if enabled, use .g format
        if enabled:
            self.fmt = '{{0:{0}g}}'.format(self.ndigit)
        else:
            self.fmt = '{{0:.{0}f}}'.format(self.ndigit)
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
        m0 = self._tv.model()
        m = m0.sourceModel()
        self.updater = DAQT(daq_func=partial(self.update_value_single, m, m0, delt, True),
                            daq_seq=range(1))
        self.updater.meta_signal1.connect(partial(
            self.on_update_display, m))
        self.updater.daqStarted.connect(partial(
            self.set_widgets_status_for_updating, 'START', False))
        self.updater.finished.connect(partial(
            self.set_widgets_status_for_updating, 'STOP', False))
        self.updater.finished.connect(self.start_thread_update)
        self.updater.start()

    def _refresh_single(self, m, m0, viewport_only, iter_param, **kws):
        # refresh a single pair of CaField object and items.
        worker = kws.get('worker', self.one_updater)
        o, it = iter_param
        cnt_fld = 0
        idx0 = m.indexFromItem(it[0]) # rd
        if viewport_only and not self.is_idx_visible(m0.mapFromSource(idx0)):
            return cnt_fld
        idx1 = m.indexFromItem(it[1]) # cset
        irow = idx0.row()
        rd_val, sp_val = o.value, o.current_setting()
        x0_idx = m.index(irow, m.i_val0)
        x1_idx = m.index(irow, m.i_rd)
        x2_idx = m.index(irow, m.i_cset)
        tol_idx = m.index(irow, m.i_tol)
        dx01_idx = m.index(irow, m.i_val0_rd)
        dx02_idx = m.index(irow, m.i_val0_cset)
        dx12_idx = m.index(irow, m.i_rd_cset)
        pwr_idx = m.index(irow, m.i_pwr)
        ratio_x20_idx = m.index(irow, m.i_ratio_x20)
        wa_idx = m.index(irow, m.i_writable)
        wa = o.write_access
        idx_tuple = (idx0, idx1)
        v_tuple = (rd_val, sp_val)
        for iidx, val in zip(idx_tuple, v_tuple):
            worker.meta_signal1.emit((iidx, self.fmt.format(val), Qt.DisplayRole))
        worker.meta_signal1.emit((wa_idx, str(wa), Qt.DisplayRole))

        x0 = float(m.data(x0_idx))
        x1, x2 = rd_val, sp_val
        dx01 = x0 - x1
        dx02 = x0 - x2
        dx12 = x1 - x2
        idx_tuple = (dx01_idx, dx02_idx, dx12_idx)
        v_tuple = (dx01, dx02, dx12)
        for iidx, val in zip(idx_tuple, v_tuple):
            worker.meta_signal1.emit((iidx, self.fmt.format(val), Qt.DisplayRole))
        worker.meta_signal1.emit((ratio_x20_idx, get_ratio_as_string(x2, x0, self.fmt),
                                  Qt.DisplayRole))

        tol = float(m.data(tol_idx))
        if abs(dx12) > tol:
            worker.meta_signal1.emit((dx12_idx, self._warning_px.scaled(PX_SIZE, PX_SIZE), Qt.DecorationRole))
        else:
            worker.meta_signal1.emit((dx12_idx, None, Qt.DecorationRole))

        if not is_close(x0, x2, self.ndigit):
            worker.meta_signal1.emit((dx02_idx, self._warning_px.scaled(PX_SIZE, PX_SIZE), Qt.DecorationRole))
        else:
            worker.meta_signal1.emit((dx02_idx, None, Qt.DecorationRole))

        #
        pwr_is_on = 'Unknown'
        elem = self._lat[o.ename]
        if elem.family != 'CAV':
            if 'PWRSTS' in elem.fields:
                pwr_fld = elem.get_field('PWRSTS')
                pwr_is_on = pwr_fld.value
        else: # CAV
            r = re.match(r".*([1-3]+).*", o.name)
            if r is not None: # D0987
                _fname = 'ITLKSTS' + r.group(1)
            else:
                _fname = 'ITLKSTS'
            if _fname in elem.fields:
                pwr_fld = elem.get_field(_fname)
                pwr_is_on = pwr_fld.value
        if pwr_is_on == 1.0:
            px = self._pwr_on_px
            tt = "Power is ON"
        elif pwr_is_on == 0.0:
            px = self._pwr_off_px
            tt = "Power is OFF"
        else:
            px = self._pwr_unknown_px
            tt = "Power is UNKNOWN"
        # emit signal to update power status
        worker.meta_signal1.emit((pwr_idx, px.scaled(PX_SIZE, PX_SIZE), Qt.DecorationRole))
        worker.meta_signal1.emit((pwr_idx, tt, Qt.ToolTipRole))
        #
        cnt_fld += 1
        return cnt_fld

    def update_value_single(self, m, m0, delt, viewport_only, iiter):
        # update data tree for one time, iterate all items.
        if delt == -1:
            worker = self._updater
        else:
            worker = self.updater
        t0 = time.time()
        cnt_fld = 0
        if self._filter_btn_enabled: # force iterate all if any (2) filter btn is on
            viewport_only = False
        for o, it in self.obj_it_tuple:
            _cnt_fld = self._refresh_single(m, m0, viewport_only, (o, it), worker=worker)
            cnt_fld += _cnt_fld

        dt = time.time() - t0
        dt_residual = delt - dt
        if delt == 0:
            printlog("Single update in {0:.1f} msec, no wait.".format(dt * 1000))
        else:
            if dt_residual > 0:
                time.sleep(dt_residual)
                printlog("Waited {0:.0f} msec (Field: {1}).".format(dt_residual * 1000,
                         cnt_fld))
            else:
                printlog("Rate is {0:.1f} Hz (Field: {1}).".format(1.0 / dt,
                         cnt_fld))

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
                    self._lat.append(i)
                    is_added_list.append(self.add_element(i))
                is_added = True in is_added_list
            else:
                sel_elems, _, _ = self._elem_selected
                pv_elem = sel_elems[0]
                elem = build_element(pv_elem.setpoint[0], pv_elem.readback[0])
                self._lat.append(elem)
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

    @pyqtSlot(float, 'QString')
    def _on_data_refresh_progressed(self, per, str_idx):
        self.refresh_pb.setValue(per * 100)

    @pyqtSlot()
    def on_single_update(self):
        """Update values, indicators for one time."""
        if self._tv.model() is None:
            return
        m0 = self._tv.model()
        m = m0.sourceModel()
        self.one_updater = DAQT(daq_func=partial(self._refresh_single, m, m0, False),
                                daq_seq=self.obj_it_tuple, nproc=NPROC)
        self.one_updater.meta_signal1.connect(partial(
            self.on_update_display, m))
        #self.one_updater.daqStarted.connect(lambda:self.refresh_pb.setVisible(True))
        self.one_updater.daqStarted.connect(lambda:printlog("Data refreshing..."))
        self.one_updater.daqStarted.connect(partial(
            self.set_widgets_status_for_updating, 'START'))
        #self.one_updater.progressUpdated.connect(self._on_data_refresh_progressed)
        self.one_updater.finished.connect(partial(
            self.set_widgets_status_for_updating, 'STOP'))
        #self.one_updater.daqFinished.connect(lambda:self.refresh_pb.setVisible(False))
        self.one_updater.daqFinished.connect(lambda:printlog("Data refreshing...done."))
        self.one_updater.start()

    def set_widgets_status_for_updating(self, status, is_single=True):
        """Set widgets status for updating.
        """
        w1 = [self.update_rate_cbb, self.apply_btn,
              self.single_update_btn, self.auto_ndigit_chkbox]
        if is_single:
            w1.append(self.update_ctrl_btn)
            w1.append(self.snp_dock)
        [i.setDisabled(status=='START') for i in w1]
        # auto ndigit
        for o in (self.ndigit_sbox, self.ndigit_lbl):
            o.setDisabled(status=='START' or self.auto_ndigit_chkbox.isChecked())

    def set_widgets_status_for_applying(self, status):
        """Set widgets status for applying.
        """
        w1 = (self.apply_btn,)
        [i.setDisabled(status=='START') for i in w1]

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

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        urls = e.mimeData().urls()
        for url in urls:
            path = url.toLocalFile()
            ext = path.rsplit('.', 1)[-1]
            if ext.upper() != 'CSV':
                continue
            snp_data = read_data(path)
            if not is_snp_data_exist(snp_data, self._snp_dock_list):
                self._snp_dock_list.append(snp_data)
        self.update_snp_dock_view()
        self.on_load_settings(snp_data)
        n = len(self._snp_dock_list)
        self.total_snp_lbl.setText(str(n))

    @pyqtSlot(int, bool)
    def on_update_visibility(self, idx, f):
        self._tv.setColumnHidden(idx, f)

    def turn_off_updater_if_necessary(self):
        if self.update_ctrl_btn.isChecked():
            self.update_ctrl_btn.setChecked(False)
            milli_sleep(100)

    def take_snapshot(self, cast=True, only_checked_items=False, post_current_sp=True):
        # take but not cast (show in the settings view) for only checked items or not.
        # cast: if cast snapshot or not
        # only_checked_items: if take snapshot of checked items or not
        # post_current_sp: if update x0 with x2 column or not
        m = self._tv.model()
        if m is None:
             return
        self.turn_off_updater_if_necessary()
        src_m = m.sourceModel()
        # single update
        self._updater = DAQT(daq_func=partial(self.update_value_single, src_m, m, -1, False),
                             daq_seq=range(1))
        self._updater.meta_signal1.connect(partial(self.on_update_display, src_m))
        self._updater.daqStarted.connect(partial(self.set_widgets_status_for_updating, 'START'))
        self._updater.finished.connect(partial(self.set_widgets_status_for_updating, 'STOP'))
        loop = QEventLoop()
        self._updater.finished.connect(loop.exit)
        self._updater.start()
        loop.exec_()
        #
        if post_current_sp:
            current_sp_idx = src_m.i_cset
            stored_sp_idx = src_m.i_val0
            for i in range(m.rowCount()):
                sp_val_str = m.data(m.index(i, current_sp_idx))
                m.setData(m.index(i, stored_sp_idx), sp_val_str)
        #
        self.on_snapshots_changed(cast)

    @pyqtSlot()
    def on_show_query_tips(self):
        if self._query_tips_form is None:
            self._query_tips_form = w = QWidget()
            ui = QueryTipsForm()
            ui.setupUi(w)
            w.setWindowTitle("Query Tips")
        self._query_tips_form.show()

    def on_snapshots_changed(self, cast=True):
        """Number of runtime snapshots is changed.
        """
        # update snpdata to snp dock.
        if self._tv.model() is None:
            return
        #
        ion_name, ion_mass, ion_number, ion_charge = self.beam_display_widget.get_species()
        if self.filter_lineEdit.text() == '':
            note = None
        else:
            note = f"Filter: {self.filter_lineEdit.text()}, "
        snp_data = SnapshotData(get_csv_settings(self._tv.model()),
                ion_name=ion_name, ion_number=ion_number, ion_mass=ion_mass, ion_charge=ion_charge,
                machine=self._last_machine_name, segment=self._last_lattice_name,
                version=self._version, note=note)
        #
        self._snp_dock_list.append(snp_data)
        n = len(self._snp_dock_list)
        self.wdir_lineEdit.setText(self.wdir)
        self.total_snp_lbl.setText(str(n))
        self.update_snp_dock_view()
        if cast:
            self.on_load_settings(snp_data)
        self.snp_filters_updated.emit()
        # save by default // to control with preference option.
        self.on_save_settings(snp_data)

    @pyqtSlot()
    def on_reveal_snp(self, data):
        # !! requires nautilus !!
        from PyQt5.QtCore import QProcess
        p = QProcess(self)
        p.setArguments(["-s", data.data_path])
        p.setProgram("nautilus")
        p.startDetached()

    @pyqtSlot()
    def on_copy_snp(self, data):
        cb = QGuiApplication.clipboard()
        cb.setText(str(data))
        msg = '<html><head/><body><p><span style="color:#007BFF;">Copied snapshot data at: </span><span style="color:#DC3545;">{}</span></p></body></html>'.format(data.ts_as_str())
        self.statusInfoChanged.emit(msg)
        self._reset_status_info()

    @pyqtSlot()
    def on_read_snp(self, data):
        QDesktopServices.openUrl(QUrl(data.data_path))

    def on_snp_filters_updated(self):
        # update btn filters
        self.update_btn_filters()
        # apply filter
        self.apply_snp_btn_filters()

    def update_btn_filters(self):
        ion_btn_filters = {}
        tag_btn_filters = set()
        d = None
        for data in self._snp_dock_list:
            d = ion_btn_filters.setdefault(data.ion_name, {})
            d.setdefault(data.ion_mass, set()).add(data.ion_charge)
            if data.tags == []:
                tag_btn_filters.add('NOTAG')
            else:
                tag_btn_filters.update(data.tags)
        del d
        self._build_btn_filters(self.snp_filter_hbox, ion_btn_filters)
        self._build_tag_filters(self.tag_filter_area, tag_btn_filters)

    def _build_tag_filters(self, area, filters):
        w = area.takeWidget()
        w.setParent(None)
        w = QWidget(self)
        w.setContentsMargins(0, 6, 0, 0)
        layout = FlowLayout()
        if 'NOTAG' in filters:
            filters.remove('NOTAG')
            _filters = ['NOTAG'] + list(filters)
        else:
            _filters = list(filters)
        for tag in _filters:
            o = QToolButton(self.snp_dock)
            o.setText(tag)
            o.setCheckable(True)
            o.toggled.connect(partial(self.on_update_tag_filters, tag))
            layout.addWidget(o)
            o.setChecked(self._current_tag_filter.get(tag, True))
        w.setLayout(layout)
        area.setWidget(w)

    @pyqtSlot(bool)
    def on_update_tag_filters(self, tag, is_checked):
        # printlog(f"{tag} button filter is {is_checked}")
        self._current_tag_filter[tag] = is_checked
        self.apply_snp_btn_filters()

    def _build_btn_filters(self, container, filters):
        child = container.takeAt(0)
        while child:
            w = child.widget()
            if w is not None:
                self._current_btn_filter[w.text()] = w.isChecked()
                w.setParent(None)
            del w
            del child
            child = container.takeAt(0)
        container.addStretch(1)
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
                btn.setFixedSize(QSize(ION_ICON_SIZE, ION_ICON_SIZE))
            btn.setCheckable(True)
            btn.toggled.connect(partial(self.on_update_snp_filters, k))
            container.addWidget(btn)
            btn.setChecked(self._current_btn_filter.get(k, True))

    def apply_snp_btn_filters(self):
        # ion, tag
        m = self.snp_treeView.model()
        m.m_src.set_ion_filters(self._current_btn_filter)
        m.m_src.set_tag_filters(self._current_tag_filter)
        m.reset_cache()
        m.invalidate()
        self.snp_expand_btn.toggled.emit(self.snp_expand_btn.isChecked())
        # ion cnt
        ion_cnt = self.snp_treeView.model().m_src._ion_filter_cnt
        layout = self.snp_filter_hbox
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
        self.snp_expand_btn.toggled.emit(self.snp_expand_btn.isChecked())
        m.save_settings.connect(self.on_save_settings)
        m.save_settings.connect(self.snp_filters_updated) # update dynamic filter buttons (tag)

    def on_del_settings(self, data):
        # delete from MEM (done), and model, and datafile (if exists)
        r = QMessageBox.warning(None, "Delete Snapshot",
                "Are you sure to delete this snapshot?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if r == QMessageBox.No:
            return
        for i, d in enumerate(self._snp_dock_list):
            if d.name == data.name:
                data_to_del = self._snp_dock_list.pop(i)
                break
        m = self.snp_treeView.model().m_src
        m.remove_data(data_to_del)
        filepath = data_to_del.data_path
        if filepath is not None and os.path.isfile(filepath):
            os.remove(filepath)
        self.total_snp_lbl.setText(str(len(self._snp_dock_list)))
        del data_to_del

    def on_save_settings(self, data):
        # in-place save data to data_path.
        if data.data_path is None or not os.path.exists(data.data_path):
            data.data_path = data.get_default_data_path(self.wdir, 'csv')
            dirname = os.path.dirname(data.data_path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
        self._save_settings(data, data.data_path)
        self.snp_saved.emit(data.name, data.data_path)

    def on_saveas_settings(self, data):
        # data: SnapshotData
        # settings(data.data): TableSettings
        # !won't update data_path attr!
        # !update name attr to be uniqe!
        # !add 'copy' into tag list!
        if data.data_path is None or not os.path.exists(data.data_path):
            cdir = data.get_default_data_path(self.wdir, 'csv')
        else:
            cdir = data.data_path
        filename, ext = get_save_filename(self,
                                          caption="Save Settings to a File",
                                          cdir=cdir,
                                          type_filter="CSV Files (*.csv);;JSON Files (*.json);;HDF5 Files (*.h5)")
        if filename is None:
            return
        data.name = re.sub(r"(.*)_[0-9]+\.[0-9]+",r"\1_{}".format(time.time()), data.name)
        if 'copy' not in data.tags:
            data.tags.append('copy')
        self._save_settings(data, filename)

    def _save_settings(self, data, filename):
        for k, v in zip(('app', 'version', 'user', 'machine', 'segment'),
                ('Settings Manager', f'{self._version}', getuser(),
                    self._last_machine_name, self._last_lattice_name)):
                 if not k in data.meta_keys and v is not None:
                     setattr(data, k, v)
        data.write(filename)

    def on_load_settings(self, data):
        # data: SnapshotData
        # settings(data.data): TableSettings
        self.turn_off_updater_if_necessary()
        if self._lat is None or self._last_machine_name != data.machine or \
                self._last_lattice_name != data.segment:
            self.__load_lattice(data.machine, data.segment)
        lat = self._lat
        s = make_physics_settings(data.data, lat)
        lat.settings.update(s)
        self._elem_list = [lat[ename] for ename in s]
        self.element_list_changed.emit()
        self.snp_loaded.emit(data)

    def on_snp_loaded(self, data):
        m = self.snp_treeView.model()
        if m is None:
            return
        m.m_src.on_snp_loaded(data)
        self._current_snpdata = data

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
        path = os.path.join(os.path.dirname(__file__), "docs", "settings_manager.qhc")
        if os.path.isfile(path):
            launch_assistant(path)

    def on_hint_scaling_factor(self, snpdata):
        btn = self.auto_sf_btn
        _, a1, _, q1 = self.beam_display_widget.get_species()
        if btn.isChecked():
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

    def on_wdir_new(self, path):
        self.snp_new_lbl.setVisible(True)

    def on_refresh_snp(self):
        # refresh snp as wdir is updated.
        self.on_wdir_changed(True, self.wdir)
        self.snp_new_lbl.setVisible(False)

    def preload_lattice(self, mach, segm):
        return self.__load_lattice(mach, segm, False)


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
    if abs(x - y) < 1.5 * 10 ** (-decimal):
        return True
    return False
