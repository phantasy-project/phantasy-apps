#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import time
from collections import OrderedDict
from fnmatch import translate
from functools import partial

from PyQt5.QtCore import QSize
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QWidget
from phantasy import CaField
from phantasy import Settings
from phantasy import build_element
from phantasy_ui import BaseAppForm
from phantasy_ui import get_open_filename
from phantasy_ui import get_save_filename
from phantasy_ui import printlog
from phantasy_ui.widgets import BeamSpeciesDisplayWidget
from phantasy_ui.widgets import DataAcquisitionThread as DAQT
from phantasy_ui.widgets import ElementSelectDialog
from phantasy_ui.widgets import LatticeWidget

from .app_loadfrom import LoadSettingsDialog
from .app_pref import DEFAULT_PREF
from .app_pref import PreferencesDialog
from .data import CSV_HEADER
from .data import ElementPVConfig
from .data import TableSettings
from .data import ToleranceSettings
from .data import get_csv_settings
from .data import make_physics_settings
from .ui.ui_app import Ui_MainWindow
from .utils import FMT
from .utils import SettingsModel
from .utils import pack_settings

DATA_SRC_MAP = {'model': 'model', 'live': 'control'}
IDX_RATE_MAP = {0: 0.1, 1: 0.2, 2: 0.5, 3: 1.0, 4: 2.0}
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
5. ? is to match one char or digit, pure '' is to interpret as *.\
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

    def __init__(self, version, config_dir):
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

        self._confdir = config_dir

        # UI
        self.setupUi(self)
        self.postInitUi()

        # config
        self.init_config(self._confdir)

        # post init ui
        self.__post_init_ui()

        self.adjustSize()

    def init_config(self, confdir):
        # tolerance settings (ts)
        ts_confpath = os.path.join(confdir, 'tolerance.json')
        self._tolerance_settings = ToleranceSettings(ts_confpath)

        # predefined model settings (ms)
        self.ms_confpath = os.path.join(confdir, 'settings.json')
        self._model_settings = Settings(self.ms_confpath)

        # elements from PVs
        self.elem_confpath = os.path.join(confdir, 'elements.json')
        self._elem_pvconf = ElementPVConfig(self.elem_confpath)

        #
        self.config_timer = QTimer(self)
        self.config_timer.timeout.connect(self.on_update_dump_config)

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
                'index': -1,
                'length': 0.0,
                'sb': -1,
                'family': 'PV',
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
        if is_same_lattice(o, self._mp):
            return
        # update lattice with the new one
        self._mp = o
        # reset self._lat
        self._lat = o.work_lattice_conf
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
        if not self.init_settings:
            QMessageBox.information(self, "Loaded Lattice",
                                    "Lattice is loaded, add settings from 'Add Devices' tool.",
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
        self.__flat_settings = flat_settings
        self.__settings = settings
        self.__on_show_settings()

    def __on_show_settings(self):
        # visualize settings
        self.reset_pvs()
        model = SettingsModel(self._tv, self.__flat_settings)
        model.settings_sts.connect(self.on_settings_sts)
        model.item_deletion_updated[list].connect(self.on_delete_items)
        model.set_model()
        self._pvs = model._pvs
        self._m_obj = model._m_obj
        self._m_it = model._m_it

        #
        self.toggle_ftype()
        #
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

        self._mp = None
        self._lat = None
        self._elem_list = []  # element list for SettingsModel

        self.__settings = Settings()
        self.__flat_settings = None

        self._pvs = []
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
        self.scaling_factor_lineEdit.setValidator(QDoubleValidator(0.0, 10, 6))

        # preferences
        # see preference dialog class
        self.pref_dict = DEFAULT_PREF
        self.field_init_mode = self.pref_dict['field_init_mode']
        self.t_wait = self.pref_dict['t_wait']
        self.init_settings = self.pref_dict['init_settings']
        self.tolerance = self.pref_dict['tolerance']
        self.dt_confsync = self.pref_dict['dt_confsync']

        self.tolerance_changed[float].connect(self.on_tolerance_float_changed)
        self.tolerance_changed[ToleranceSettings].connect(self.on_tolerance_dict_changed)
        self.model_settings_changed.connect(self.on_model_settings_changed)
        self.element_from_pv_added.connect(self.on_element_from_pv_added)

        # icon
        self.done_icon = QPixmap(":/sm-icons/done.png")
        self.fail_icon = QPixmap(":/sm-icons/fail.png")
        self._warning_px = QPixmap(":/sm-icons/warning.png")
        self._ok_px = QPixmap(":/sm-icons/ok.png")

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

        # start config sync timer
        self.config_timer.start(self.dt_confsync * 1000)

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
            src_m.setData(src_m.index(i, src_m.i_tol), FMT.format(tol),
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
                    src_m.index(i, src_m.i_tol), FMT.format(tol),
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

    @pyqtSlot()
    def on_apply_settings(self):
        """Apply selected element settings.
        """
        # scaling factor
        scaling_factor = float(self.scaling_factor_lineEdit.text())
        #
        self.idx_px_list = []  # list to apply icon [(idx_src, px)]
        m = self._tv.model()
        settings_selected = m.get_selection()
        self.applyer = DAQT(daq_func=partial(self.apply_single, scaling_factor),
                            daq_seq=settings_selected)
        self.applyer.daqStarted.connect(partial(
            self.set_widgets_status_for_applying, 'START'))
        self.applyer.progressUpdated.connect(
            partial(self.on_apply_settings_progress,
                    self.idx_px_list, m.sourceModel()))
        self.applyer.daqFinished.connect(partial(
            self.set_widgets_status_for_applying, 'STOP'))
        self.applyer.start()

    def apply_single(self, sf, tuple_idx_settings):
        idx_src, settings = tuple_idx_settings
        elem, fname, fld, fval0 = settings
        ename = elem.name
        try:
            t0 = time.time()
            fld.value = fval0 * sf
        except:
            px = self.fail_icon
        else:
            px = self.done_icon
            printlog("- Set {} [{}] to {}.".format(ename, fname, fval0))
            dt = self.t_wait - (time.time() - t0)
            if dt > 0:
                time.sleep(dt)
                printlog("Wait time: {} sec.".format(dt))
        self.idx_px_list.append((idx_src, px))

    @pyqtSlot(float, 'QString')
    def on_apply_settings_progress(self, idx_px_list, m, per, str_idx):
        printlog("Apply settings: {0:.1f} %".format(per * 100))
        idx_src, px = idx_px_list[-1]
        m.setData(idx_src, QIcon(px), Qt.DecorationRole)

    def closeEvent(self, e):
        self.on_update_dump_config()
        r = BaseAppForm.closeEvent(self, e)
        if r:
            for pv in self._pvs:
                pv.auto_monitor = False
                pv.clear_callbacks()

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
        lw = self._lv.latticeWidget
        lw.mach_cbb.setCurrentText(machine)
        lw.seg_cbb.setCurrentText(lattice)
        lw.load_btn.clicked.emit()
        lw.setEnabled(False)
        self._lv.show()

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

        printlog("Clicked: ({}, {}), item is expanded? ({})".format(
            idx.row(), idx.column(), self._tv.isExpanded(idx)))

    def reset_pvs(self):
        printlog("Reset {} PVs".format(len(self._pvs)))
        for pv in self._pvs:
            pv.auto_monitor = False
            pv.clear_callbacks()

    @pyqtSlot()
    def on_filter_changed(self):
        m = self._tv.model()
        if m is None:
            return
        s = self.sender().text()
        k = None
        kv = s.split('=', 1)
        if len(kv) == 2:
            k, v = kv
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

        m.setFilterRegExp(translate(v))

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
        ext = ext.upper()
        if ext == 'CSV':
            self._load_settings_from_csv(filepath)
        elif ext == 'JSON':
            self._load_settings_from_json(filepath)
        elif ext == 'H5':
            self._load_settings_from_h5(filepath)
        QMessageBox.information(
            self, "", "Loaded data to {}".format(filepath))
        printlog("Loaded settings from {}.".format(filepath))

    def _load_settings_from_csv(self, filepath):
        lat = self.build_lattice()
        table_settings = TableSettings(filepath)
        s = make_physics_settings(table_settings, lat)
        lat.settings.update(s)
        self._elem_list = [lat[ename] for ename in s]
        self.element_list_changed.emit()

    def _load_settings_from_json(self, filepath):
        pass

    def _load_settings_from_h5(self, filepath):
        pass

    @pyqtSlot()
    def on_launch_preferences(self):
        """Launch preferences dialog.
        """
        pref_dlg = PreferencesDialog(self)
        pref_dlg.pref_changed.connect(self.on_update_pref)
        r = pref_dlg.exec_()
        if r == QDialog.Accepted:
            printlog("Updated pref --> {}".format(self.pref_dict))
        else:
            printlog("Unchanged pref: {}".format(self.pref_dict))

    @pyqtSlot(dict)
    def on_update_pref(self, d):
        """Update app preferences.
        """
        self.pref_dict.update(d)
        self.field_init_mode = self.pref_dict['field_init_mode']
        self.t_wait = self.pref_dict['t_wait']
        self.init_settings = self.pref_dict['init_settings']
        tol = self.pref_dict['tolerance']
        self.tolerance_changed[float].emit(tol)
        self.tolerance = tol
        dt_confsync = self.pref_dict['dt_confsync']
        if dt_confsync != self.dt_confsync:
            self.config_timer.stop()
            self.dt_confsync = dt_confsync
            self.config_timer.start(self.dt_confsync * 1000)

    @pyqtSlot(int)
    def on_update_rate(self, i):
        # update_rate_cbb index
        self.rate_changed.emit(i)

    def start_auto_update(self):
        # updating independently,
        # _update_mode: 'auto'
        for pv in self._pvs:
            pv.auto_monitor = True

    def stop_auto_update(self):
        # stop auto updating.
        for pv in self._pvs:
            pv.auto_monitor = False

    def start_thread_update(self):
        # Update values every *delt* second(s),
        # _update_mode: 'thread'

        if self._stop_update_thread:
            return

        delt = self._update_delt
        m = self._tv.model().sourceModel()
        self.updater = DAQT(daq_func=partial(self.update_value_single, m, delt),
                            daq_seq=range(1))
        self.updater.resultsReady.connect(
            partial(self.on_values_ready, m))
        self.updater.finished.connect(self.start_thread_update)
        self.updater.start()

    def on_values_ready(self, m, res):
        """Results are ready for updating.
        """
        # res --> [res in daq_func] : [(idx, val, role)... ]
        for (idx, val, role) in res[0]:
            m.data_changed.emit((idx, val, role))
        self._update_cnt += 1

    def update_value_single(self, m, delt, iiter):
        # res: [(idx, val, role)..., ]
        t0 = time.time()
        res = []
        for o, it in zip(self._m_obj, self._m_it):
            if not isinstance(o, CaField):  # PV
                val = o.get()
                for iit in it:
                    idx = m.indexFromItem(iit)
                    res.append((idx, FMT.format(val), Qt.DisplayRole))
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
                    res.append((iidx, FMT.format(val), Qt.DisplayRole))
                res.append((wa_idx, str(wa), Qt.DisplayRole))
                tol = float(m.data(tol_idx))
                if abs(dx12) > tol:
                    diff_status_px = self._warning_px
                else:
                    diff_status_px = self._ok_px
                res.append((dx12_idx, QIcon(diff_status_px), Qt.DecorationRole))

        dt = time.time() - t0
        dt_residual = delt - dt
        if dt_residual > 0 and self._update_cnt != 0:
            time.sleep(dt_residual)
            printlog("Wait {} msec.".format(dt_residual * 1000))
        else:
            printlog("Update rate is too high.")

        return res

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
            self._update_cnt = 0
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
                self.element_list_changed.emit()

    def build_lattice(self):
        """Build lattice based on machine/lattice name, and add elements from
        PV configs from elem_pvconf, the model settings of the new elements
        are pulled from model_settings if available.

        Returns
        -------
        r : Lattice
            Updated high-level lattice object.
        """
        # load mp
        # add elements rom elem_pvconf
        lat = self._lat
        ms = self._model_settings
        for ename, conf in self._elem_pvconf.items():
            field_eng = conf['field']
            field_phy = conf['field_phy']
            sp_pv = conf['setpoint']
            rd_pv = conf['readback']
            index = conf['index']
            length = conf['length']
            sb = conf['sb']
            elem = build_element(sp_pv, rd_pv, ename=ename, fname=field_eng,
                                 field_phy=field_phy, index=index,
                                 length=length, sb=sb)
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

    @pyqtSlot()
    def on_single_update(self):
        """Update values, indicators for one time."""
        self._update_cnt = 0
        m = self._tv.model().sourceModel()
        self.one_updater = DAQT(daq_func=partial(self.update_value_single, m, 0),
                                daq_seq=range(1))
        self.one_updater.daqStarted.connect(partial(
            self.set_widgets_status_for_updating, 'START'))
        self.one_updater.resultsReady.connect(
            partial(self.on_values_ready, m))
        self.one_updater.finished.connect(partial(
            self.set_widgets_status_for_updating, 'STOP'))
        self.one_updater.start()

    def set_widgets_status_for_updating(self, status):
        """Set widgets status for updating.
        """
        w1 = (self.update_ctrl_btn, self.update_rate_cbb, self.apply_btn,
              self.single_update_btn,)
        [i.setDisabled(status == 'START') for i in w1]

    def set_widgets_status_for_applying(self, status):
        """Set widgets status for applying.
        """
        w1 = (self.apply_btn,)
        [i.setDisabled(status == 'START') for i in w1]

    def sizeHint(self):
        return QSize(1800, 1200)

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
        printlog("Update and dump configurations...")
        self.snapshot_tolerance_settings()

    @pyqtSlot(Settings)
    def on_model_settings_changed(self, settings):
        """Update and dump model settings.
        """
        if settings != self._model_settings:
            self._model_settings.update(settings)
            self._model_settings.write(self.ms_confpath)
            printlog("Update model settings snapshot.")


def is_same_lattice(new_mp, current_mp):
    """Test if the current loaded lattice of new_mp and current_mp is the same.
    """
    # new_mp is not None
    if current_mp is None:
        return False
    return (new_mp.last_machine_name == current_mp.last_machine_name) and \
           (new_mp.last_lattice_name == current_mp.last_lattice_name)


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
