#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fnmatch import translate
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from phantasy_ui import BaseAppForm
from phantasy_ui.widgets import LatticeWidget
from phantasy_apps.utils import printlog

from .app_loadfrom import LoadSettingsDialog
from .ui.ui_app import Ui_MainWindow
from .utils import SettingsModel
from .utils import pack_lattice_settings


class SettingsManagerWindow(BaseAppForm, Ui_MainWindow):

    # signal: settings loaded, emit flat_settings and settings.
    settingsLoaded = pyqtSignal(QVariant, QVariant)

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
        flat_settings, settings = pack_lattice_settings(o.work_lattice_conf)
        self.settingsLoaded.emit(flat_settings, settings)
        print("Lattice is changed ...")

    def update_lattice_info_lbls(self, mach, segm):
        for w in (self.lv_lbl, self.lv_mach_lbl, self.lv_segm_lbl,
                  self.lv_view_btn):
            w.setVisible(True)
        self.lv_mach_lbl.setText(mach)
        self.lv_segm_lbl.setText(segm)

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
        model = SettingsModel(self.treeView, self.__flat_settings)
        model.settings_sts.connect(self.on_settings_sts)
        model.set_model()
        self._pvs = model._pvs

        #
        self.namefilter_lineEdit.textChanged.emit(self.namefilter_lineEdit.text())

    @pyqtSlot(int, int, int)
    def on_settings_sts(self, i, j, k):
        for s, v in zip(('elem', 'sppv', 'rdpv'), (i, j, k)):
            o = getattr(self, 'total_{}_number_lbl'.format(s))
            o.setText(str(v))

    def __post_init_ui(self):
        self._load_from_dlg = None
        self._lattice_load_window = None
        self._mp = None
        self.__settings = None
        self.__flat_settings = None
        self._pvs = []
        self.on_lattice_changed(self._mp)

        # lattice viewer
        for w in (self.lv_lbl, self.lv_mach_lbl, self.lv_segm_lbl,
                  self.lv_view_btn):
            w.setVisible(False)
        self._lv = None
        self.lv_view_btn.clicked.connect(self.on_show_latinfo)

        # show lattice settings
        self.settingsLoaded.connect(self.on_settings_loaded)

    def on_save(self):
        """Save settings to file.
        """
        print("Save settings to file")

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
        """Apply (selected) settings to machine.
        """
        if self.__settings is None:
            return
        try:
            lat = self._mp.work_lattice_conf
            lat.settings = self.__settings
            lat.sync_settings(data_source='model')
        except:
            QMessageBox.warning(self, "Apply Settings",
                    "Failed to apply settings to accelerator.",
                    QMessageBox.Ok)

        else:
            QMessageBox.information(self, "Apply Settings",
                    "Successfully applied settings to accelerator.",
                    QMessageBox.Ok)

    def closeEvent(self, e):
        r = BaseAppForm.closeEvent(self, e)
        if r:
            for pv in self._pvs:
                pv.auto_monitor = False
                pv.clear_callbacks()

    @pyqtSlot(bool)
    def on_toggle_phyfields(self, f):
        if f:
            print("Show PHY fields...")
        else:
            print("Hide PHY fields...")

    @pyqtSlot(bool)
    def on_toggle_engfields(self, f):
        if f:
            print("Show ENG fields...")
        else:
            print("Hide ENG fields...")

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
        printlog("Clicked: ({}, {}), item is expanded? ({})".format(
            idx.row(), idx.column(), self.treeView.isExpanded(idx)))

    def reset_pvs(self):
        print("-" * 30)
        print("Reset {} PVs".format(len(self._pvs)))
        for pv in self._pvs:
            pv.auto_monitor = False
            pv.clear_callbacks()

    @pyqtSlot('QString')
    def on_namefilter_changed(self, s):
        k = None
        kv = s.split('=', 1)
        if len(kv) == 2:
            k, v = kv
        else:
            v = s
        if v == '':
            v = '*'
        m = self.treeView.model()
        m.sourceModel().set_filter_key(k)
        m.setFilterRegExp(translate(v))
        self.total_show_number_lbl.setText(str(m.rowCount()))
