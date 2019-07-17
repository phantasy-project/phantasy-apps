#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from functools import partial

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QDialog

from phantasy_ui import BaseAppForm
from phantasy_ui.widgets import DataAcquisitionThread as DAQT
from phantasy.library.physics.devices import process_devices

from .app_settings import AppSettingsWidget
from .ui.ui_app import Ui_MainWindow
from .utils import DataModel

NEW_DURATION_IN_SEC = 300

FOOTNOTE_TEMPLATE = '<html><head/><body><p><span style="vertical-align:super;">*</span>The units for beam center and size are all millimeter.</p><p><span style="vertical-align:super;">*</span>Last updates in the past {} seconds will be marked as NEW.</p></body></html>'


class PMViewerWindow(BaseAppForm, Ui_MainWindow):

    def __init__(self, version):
        super(self.__class__, self).__init__()

        self._version = version
        self.setWindowTitle("Profile Monitors Viewer")
        self.setAppTitle("PM Viewer")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Profile Monitors Viewer</h4>
            <p>Inspect and operate a bunch of profile monitors in one window,
            current version is {}.
            </p>
            <p>Copyright (C) 2019 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

        self.pb.setValue(0)
        self.pb.setVisible(False)
        # vars
        self._app_settings_widget = None
        self._fresh_duration = NEW_DURATION_IN_SEC
        self.footnote_lbl.setText(FOOTNOTE_TEMPLATE.format(self._fresh_duration))

        self.v = self.treeView
        self.set_viewer()

    def set_viewer(self):
        """Set up viewer.
        """
        m = DataModel(self.v, segment='LINAC',
                      fresh_duration=self._fresh_duration)
        m.set_model()

    def on_run_devices(self):
        """Run selected devices.
        """
        m = self.v.model()
        self.selected_elems = m.get_selection()
        n = len(self.selected_elems)
        if n == 0:
            QMessageBox.warning(self, "Run Devices",
                    "Not any devices are selected.",
                    QMessageBox.Ok)
            return

        self.daq_th = DAQT(daq_func=self.daq_single, daq_seq=range(n))
        self.daq_th.daqStarted.connect(partial(self.set_widgets_status, "START"))
        self.daq_th.progressUpdated.connect(self.on_update_daq_status)
        self.daq_th.resultsReady.connect(self.on_daq_results_ready)
        self.daq_th.daqFinished.connect(partial(self.set_widgets_status, "STOP"))
        self.daq_th.start()

    def on_daq_results_ready(self, r):
        self.pb.setVisible(False)
        print("Running is done...")

    def daq_single(self, iiter):
        t0 = time.time()
        elem = self.selected_elems[iiter]
        print("-- Processing device: {}".format(elem.name))
        process_devices((elem,))
        dt = time.time() - t0
        print("-- Execution Time: {0:.2f} sec".format(dt))

    def on_update_daq_status(self, f, s):
        print('Progress: {}, {}'.format(f, s))
        self.pb.setValue(f * 100)

    def set_widgets_status(self, status):
        olist1 = (self.run_btn, )
        olist2 = (self.stop_btn, )
        if status != "START": # not running
            [o.setEnabled(True) for o in olist1]
            [o.setEnabled(False) for o in olist2]
        else: # running
            self.pb.setVisible(True)
            [o.setEnabled(False) for o in olist1]
            [o.setEnabled(True) for o in olist2]

    @pyqtSlot()
    def onLaunchAppSettings(self):
        """Launch widget for app settings.
        """
        if self._app_settings_widget is None:
            self._app_settings_widget = AppSettingsWidget(self)
        self._app_settings_widget.dtsec_dsbox.setValue(NEW_DURATION_IN_SEC)
        r = self._app_settings_widget.exec_()
        if r == QDialog.Accepted:
            self._fresh_duration = self._app_settings_widget.dtsec_dsbox.value()
            self.footnote_lbl.setText(FOOTNOTE_TEMPLATE.format(self._fresh_duration))
            self.set_viewer()
