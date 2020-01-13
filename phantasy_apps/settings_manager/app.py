#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
from functools import partial
from collections import OrderedDict
from fnmatch import translate
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QDialog
from phantasy_ui import BaseAppForm
from phantasy_ui import get_save_filename
from phantasy_ui import get_open_filename
from phantasy_ui.widgets import LatticeWidget
from phantasy_ui.widgets import DataAcquisitionThread as DAQT
from phantasy_apps.utils import printlog
from phantasy_apps.correlation_visualizer.utils import delayed_exec
from phantasy import Settings
from phantasy import CaField

from .app_loadfrom import LoadSettingsDialog
from .app_pref import PreferencesDialog
from .ui.ui_app import Ui_MainWindow
from .utils import SettingsModel
from .utils import pack_lattice_settings
from .utils import FMT
from .data import FlatSettings
from .data import make_physics_settings


DATA_SRC_MAP = {'model': 'model', 'live': 'control'}


class SettingsManagerWindow(BaseAppForm, Ui_MainWindow):

    # signal: settings loaded, emit flat_settings and settings.
    settingsLoaded = pyqtSignal(QVariant, QVariant)

    # refresh rate
    rate_changed = pyqtSignal(int)

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
        self._mp = o
        #
        snpload_status = True if self._mp is not None else False
        self.actionLoad_From_Snapshot.setEnabled(snpload_status)
        #
        if o is None:
            return
        #
        self.update_lattice_info_lbls(o.last_machine_name, o.last_lattice_name)
        # show element settings
        flat_settings, settings = pack_lattice_settings(o.work_lattice_conf,
                        data_source=DATA_SRC_MAP[self.field_init_mode],
                        only_physics=False)
        self.settingsLoaded.emit(flat_settings, settings)
        printlog("Lattice is changed")

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
        self._lattice_load_window = None
        self._mp = None
        self.__settings = None
        self.__flat_settings = None
        self._pvs = []
        self._eng_phy_toggle = {'ENG': True, 'PHY': True}
        self.on_lattice_changed(self._mp)

        # lattice viewer
        self._enable_widgets(False)
        self._lv = None
        self.lv_view_btn.clicked.connect(self.on_show_latinfo)

        # show lattice settings
        self.settingsLoaded.connect(self.on_settings_loaded)

        # update rate
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.on_update_by_time)
        self.rate_changed.connect(self.on_update_rate_changed)

        # preferences
        # see preference dialog class
        self.field_init_mode = 'model'
        self.t_wait = 0.05 # second
        self.pref_dict = {
            'field_init_mode': self.field_init_mode,
            't_wait': self.t_wait,
        }

        # icon
        self.done_icon = QPixmap(":/sm-icons/done.png")
        self.fail_icon = QPixmap(":/sm-icons/fail.png")

        # selection
        self.select_all_btn.clicked.connect(partial(self.on_select, 'all'))
        self.invert_selection_btn.clicked.connect(partial(self.on_select, 'invert'))

        # filter
        self.init_filter()

    def init_filter(self):
        """Initial filter.
        """
        o = self.namefilter_lineEdit
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
        # cases:
        # 1. 0: auto, max rate depends on devices
        # 2. i > 0: update every 1/i second
        self.stop_update_timer()
        if i == 0:
            tt = "Auto updating rate."
        else:
            printlog('updating controled by timer')
            tt = "Updating at {} Hz.".format(i)
        self.start_update(i)
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
                self, "", "Saved data to {}".format(filename))
        printlog("Saved settings to {}.".format(filename))

    def _save_settings_as_json(self, filename):
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

        data = FlatSettings()
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
        m = self._tv.model()
        settings_selected = m.get_selection()
        self.applyer = DAQT(daq_func=partial(self.apply_single, m.sourceModel()),
                            daq_seq=settings_selected)
        self.applyer.daqStarted.connect(self.on_apply_settings_started)
        self.applyer.progressUpdated.connect(self.on_apply_settings_progress)
        self.applyer.daqFinished.connect(self.on_apply_settings_finished)
        self.applyer.start()

    def apply_single(self, model_src, tuple_idx_settings):
        idx_src, settings = tuple_idx_settings
        elem, fname, fld, fval0 = settings
        ename = elem.name
        try:
            fld.value = fval0
        except:
            px = self.fail_icon
        else:
            px = self.done_icon
            printlog("- Set {} [{}] to {}.".format(ename, fname, fval0))
            print("wait time:", self.t_wait)
            time.sleep(self.t_wait)
        finally:
            model_src.setData(idx_src, QIcon(px), Qt.DecorationRole)

    @pyqtSlot(float, 'QString')
    def on_apply_settings_progress(self, per, str_idx):
        printlog("Apply settings: {} %".format(per * 100))

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
        self.namefilter_lineEdit.editingFinished.emit()

    @pyqtSlot()
    def on_load_lattice(self):
        """Load lattice.
        """
        if self._lattice_load_window is None:
            self._lattice_load_window = LatticeWidget()
            self._lattice_load_window.latticeChanged.connect(
                    self.on_lattice_changed)
            self._lattice_load_window.latticeChanged.connect(self._lattice_load_window.close)
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
    def on_namefilter_changed(self):
        s = self.sender().text()
        k = None
        kv = s.split('=', 1)
        if len(kv) == 2:
            k, v = kv
        else:
            v = s
        if v == '':
            v = '*'
        m = self._tv.model()
        m.sourceModel().set_filter_key(k)
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
        s = make_physics_settings(FlatSettings(filepath), lat)
        lat.settings = s
        flat_settings, settings = pack_lattice_settings(lat,
                data_source=DATA_SRC_MAP[self.field_init_mode],
                only_physics=False)
        self.settingsLoaded.emit(flat_settings, settings)
        self.__settings = s

    def _load_settings_from_json(self, filepath):
        pass

    def _load_settings_from_h5(self, filepath):
        pass

    @pyqtSlot()
    def on_launch_preferences(self):
        """Launch preferences dialog.
        """
        pref_dlg = PreferencesDialog(self.pref_dict, self)
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

    @pyqtSlot()
    def on_update_by_time(self):
        """Update values by time.
        """
        printlog("Updating...")
        m = self._tv.model().sourceModel()
        for i, o in enumerate(self._m_obj):
            if not isinstance(o, CaField): # PV
                val = o.get()
                for idx in self._m_idx[i]:
#                    print("PV:", (idx.row(), idx.column()), val)
                    m.data_changed.emit((idx, FMT.format(val), Qt.DisplayRole))
            else: # CaField
                rd_val, sp_val = o.value, o.current_setting()
                for idx, val in zip(self._m_idx[i], (rd_val, sp_val)):
#                    print("Field:", (idx.row(), idx.column()), val)
                    m.data_changed.emit((idx, FMT.format(val), Qt.DisplayRole))

    @pyqtSlot(int)
    def on_update_rate(self, i):
        # update_rate_cbb index
        self.rate_changed.emit(i)

    def auto_update(self):
        # resume updating.
        for pv in self._pvs:
            pv.auto_monitor = True

    def pause_update(self):
        # pause updating.
        for pv in self._pvs:
            pv.auto_monitor = False

    @pyqtSlot(bool)
    def on_toggle_rate_ctrl_btn(self, f):
        """Toggle update rate control.
        """
        if f:
            i = self.update_rate_cbb.currentIndex()
            self.start_update(i)
        else:
            self.stop_update()

    def start_update(self, i):
        if i == 0:
            # auto update
            self.auto_update()
        else:
            self.pause_update()
            self.update_timer.start(1000.0 / i)

    def stop_update(self):
        self.stop_update_timer()
        self.pause_update()

    def stop_update_timer(self):
        if self.update_timer.isActive():
            self.update_timer.stop()

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


def make_settings(filepath, lat):
    """Make settings, if both ENG and PHY exist, only keep PHY."""
    s = Settings(filepath)
    nm = {o.name:o for o in lat}
    s_phy = s.copy()
    for k, v in s.items():
        elem = nm[k]
        phy_fields = elem.get_phy_fields()
        if phy_fields:
            s_phy[k] = {}
            for f in phy_fields:
                s_phy[k].update({f: v[f]})
    return s_phy


