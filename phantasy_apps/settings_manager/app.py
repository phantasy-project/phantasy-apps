#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
from fnmatch import translate
from functools import partial

from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from phantasy import CaField
from phantasy import Settings
from phantasy_ui import BaseAppForm
from phantasy_ui import get_open_filename
from phantasy_ui import get_save_filename
from phantasy_ui import printlog
from phantasy_ui.widgets import DataAcquisitionThread as DAQT
from phantasy_ui.widgets import ElementSelectDialog
from phantasy_ui.widgets import LatticeWidget

from .app_loadfrom import LoadSettingsDialog
from .app_pref import PreferencesDialog
from .app_pref import DEFAULT_PREF
from .data import TableSettings
from .data import make_physics_settings
from .ui.ui_app import Ui_MainWindow
from .utils import FMT
from .utils import SettingsModel
from .utils import pack_lattice_settings
from .utils import convert_settings

DATA_SRC_MAP = {'model': 'model', 'live': 'control'}
IDX_RATE_MAP = {1: 0.5, 2: 1.0, 3: 2.0}
FILTER_TT = """Input filter string with the format of 'keyword=pattern', valid keywords as the headers show, pattern applies Unix wildcard rules.
Keyword is case insensitive, if keyword is not defined, 'device' is used.
For 'setpoint', the keyword 'x0' could be used, the same rule applies to 'x1', 'x2', 'dx01', 'dx02', 'dx03',
where 'dxij' is 'xi - xj' as show in the headers.

Press Enter to activate the filter, here is some examples:
1. *: match all device names, which is equivalent of device=*;
2. *LEBT*: match device name which has string 'LEBT';
3. type='CAV': match all devices of type 'CAV';
4. ? is to match one char or digit, pure '' is to interpret as *."""


class SettingsManagerWindow(BaseAppForm, Ui_MainWindow):
    # signal: settings loaded, emit flat_settings and settings.
    settingsLoaded = pyqtSignal(QVariant, QVariant)

    # refresh rate
    rate_changed = pyqtSignal(int)

    # lattice is loaded
    lattice_loaded = pyqtSignal(QVariant)

    def __init__(self, version):
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

        # post init ui
        self.__post_init_ui()

    @pyqtSlot(QVariant)
    def on_lattice_changed(self, o):
        """Lattice is loaded.
        1. Update status of snp load tool
        2. Update lattice info labels
        3. Show the current element settings
        """
        if o is None:
            return
        self._mp = o
        #
        snpload_status = True if self._mp is not None else False
        self.actionLoad_From_Snapshot.setEnabled(snpload_status)
        #
        self.update_lattice_info_lbls(o.last_machine_name, o.last_lattice_name)

        # show element settings
        if self.init_settings:
            flat_settings, settings = pack_lattice_settings(
                    o.work_lattice_conf,
                    data_source=DATA_SRC_MAP[self.field_init_mode],
                    only_physics=False)
            self.settingsLoaded.emit(flat_settings, settings)
        #
        printlog("Lattice is changed")
        self.lattice_loaded.emit(o)

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
        model.set_model()
        self._pvs = model._pvs
        self._m_obj = model._m_obj
        self._m_idx = model._m_idx

        #
        self.toggle_ftype()
        #
        self.update_ctrl_btn.toggled.emit(self.update_ctrl_btn.isChecked())

    @pyqtSlot(int, int, int)
    def on_settings_sts(self, i, j, k):
        for s, v in zip(('elem', 'sppv', 'rdpv'), (i, j, k)):
            o = getattr(self, 'total_{}_number_lbl'.format(s))
            o.setText(str(v))

    def __post_init_ui(self):
        self._tv = self.treeView
        self._load_from_dlg = None
        self._elem_select_dlg = None
        self._lattice_load_window = None
        self._mp = None
        self.__settings = Settings()
        self.__flat_settings = None
        self._elem_list = []  #  selected element list
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

        # preferences
        # see preference dialog class
        self.pref_dict = DEFAULT_PREF
        self.field_init_mode = self.pref_dict['field_init_mode']
        self.t_wait = self.pref_dict['t_wait']
        self.init_settings = self.pref_dict['init_settings']

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
        if i == 0:
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
        s = self.get_settings()
        header = ('name', 'field', 'setpoint', 'readback', 'last_setpoint')
        s.write(filename, header=header)

    def _save_settings_as_h5(self, filename):
        pass

    def get_settings(self):
        m = self._tv.model()
        src_m = m.sourceModel()
        # sp: last_sp
        # live_sp: sp about to save
        # live_rd: rb at live_sp
        i_name, i_field, i_sp, i_live_rd, i_live_sp = \
            src_m.i_name, src_m.i_field, src_m.i_val0, src_m.i_rd, src_m.i_cset

        data = TableSettings()
        for irow in range(m.rowCount()):
            ename = m.data(m.index(irow, i_name))
            fname = m.data(m.index(irow, i_field))
            f_new_sp = float(m.data(m.index(irow, i_live_sp)))
            f_old_sp = float(m.data(m.index(irow, i_sp)))
            f_new_rd = float(m.data(m.index(irow, i_live_rd)))
            data.append((ename, fname, f_new_sp, f_new_rd, f_old_sp))
        return data

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
        self.idx_px_list = []  # list to apply icon [(idx_src, px)]
        m = self._tv.model()
        settings_selected = m.get_selection()
        self.applyer = DAQT(daq_func=self.apply_single,
                            daq_seq=settings_selected)
        self.applyer.daqStarted.connect(self.on_apply_settings_started)
        self.applyer.progressUpdated.connect(
            partial(self.on_apply_settings_progress,
                    self.idx_px_list, m.sourceModel()))
        self.applyer.daqFinished.connect(self.on_apply_settings_finished)
        self.applyer.start()

    def apply_single(self, tuple_idx_settings):
        idx_src, settings = tuple_idx_settings
        elem, fname, fld, fval0 = settings
        ename = elem.name
        try:
            t0 = time.time()
            fld.value = fval0
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

    @pyqtSlot()
    def on_apply_settings_started(self):
        printlog("Start to apply settings...")

    @pyqtSlot()
    def on_apply_settings_finished(self):
        printlog("Finish applying settings...")

    def closeEvent(self, e):
        r = BaseAppForm.closeEvent(self, e)
        if r:
            for pv in self._pvs:
                pv.auto_monitor = False
                pv.clear_callbacks()

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

        #m.setFilterRegExp(QRegExp(v, Qt.CaseSensitive,
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
        lat = self._mp.work_lattice_conf
        s = make_physics_settings(TableSettings(filepath), lat)
        lat.settings.update(s)
        flat_settings, settings = pack_lattice_settings(lat,
                                                        data_source=DATA_SRC_MAP[self.field_init_mode],
                                                        only_physics=False)
        self.settingsLoaded.emit(flat_settings, settings)

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
            self.field_init_mode = self.pref_dict['field_init_mode']
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

    def update_value_single(self, m, delt, iiter):
        # res: [(idx, val, role)..., ]
        t0 = time.time()
        res = []
        for o, idx in zip(self._m_obj, self._m_idx):
            if not isinstance(o, CaField):  # PV
                val = o.get()
                for iidx in idx:
                    res.append((iidx, FMT.format(val), Qt.DisplayRole))
            else:  # CaField
                irow = idx[0].row()
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
                idx_tuple = (idx[0], idx[1], dx01_idx, dx02_idx, dx12_idx)
                v_tuple = (rd_val, sp_val, dx01, dx02, dx12)
                for iidx, val in zip(idx_tuple, v_tuple):
                    res.append((iidx, FMT.format(val), Qt.DisplayRole))
                tol = float(m.data(tol_idx))
                if abs(dx12) > tol:
                    diff_status_px = self._warning_px
                else:
                    diff_status_px = self._ok_px
                res.append((dx12_idx, QIcon(diff_status_px), Qt.DecorationRole))

        dt = time.time() - t0
        dt_residual = delt - dt
        if dt_residual > 0:
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
            self.start_thread_update()
            printlog("Start thread updating.")

    def stop_update(self):
        if self._update_mode == 'thread':
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
        #debug
        #print(selections)

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
                lat = self._mp.work_lattice_conf
                elems = sel_elems_dis
                _, settings = pack_lattice_settings(
                        lat, elems,
                        data_source=DATA_SRC_MAP[self.field_init_mode],
                        only_physics=False)
                self.__settings.update(settings)
                for elem in lat:
                    if elem not in self._elem_list:
                        self._elem_list.append(elem)
            else:
                # WIP: this part should be refactored
                from .utils import build_element
                settings = Settings()
                sel_elems, _, _ = self._elem_selected
                pv_elem = sel_elems[0]

                ename = pv_elem.ename
                fname = pv_elem.fname
                elem = build_element(pv_elem.setpoint[0], pv_elem.readback[0],
                                     ename=ename, fname=fname)
                settings.update([(ename, {fname: getattr(elem, fname),
                                  fname + '_phy': getattr(elem, fname)})])
                self.__settings.update(settings)
                if elem not in self._elem_list:
                    self._elem_list.append(elem)

            #
            self.__flat_settings = convert_settings(self.__settings, self._elem_list)
            self.settingsLoaded.emit(self.__flat_settings, self.__settings)
