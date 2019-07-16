#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from phantasy_ui import BaseAppForm
from phantasy_ui.widgets import DataAcquisitionThread as DAQT

from .utils import DataModel
from .ui.ui_app import Ui_MainWindow

import time
from functools import partial


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
            <p>Run and see a bunch of profile monitors in one window,
            current version is {}.
            </p>
            <p>Copyright (C) 2019 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

        self.v = self.treeView
        self.set_viewer()

    def set_viewer(self):
        """Set up viewer.
        """
        m = DataModel(self.v, segment='LEBT')
        m.set_model()

    def on_run_devices(self):
        """Run selected devices.
        """
        m = self.v.model()
        self.selected_devices = sorted(m._selected_items, key=lambda x:x[-4:])

        self.daq_th = DAQT(daq_func=self.daq_single, daq_seq=range(1))
        self.daq_th.started.connect(partial(self.set_widgets_status, "START"))
        self.daq_th.progressUpdated.connect(self.on_update_daq_status)
        self.daq_th.resultsReady.connect(self.on_daq_results_ready)
        self.daq_th.finished.connect(partial(self.set_widgets_status, "STOP"))
        self.daq_th.start()

    def on_daq_results_ready(self, r):
        data = r[0]
        print("Running is done...")

    def daq_single(self, iiter):
        for i in self.selected_devices:
            t0 = time.time()
            print("-- Processing device: {}".format(i))
            time.sleep(2.0)
            dt = time.time() - t0
            print("-- Execution Time: {} ms".format(dt * 1000))

    def on_update_daq_status(self, f, s):
        print('Progress: {}, {}'.format(f, s))

    def set_widgets_status(self, status):
        olist1 = (self.run_btn,)
        olist2 = (self.stop_btn, )
        if status != "START":
            [o.setEnabled(True) for o in olist1]
            [o.setEnabled(False) for o in olist2]
        else:
            [o.setEnabled(False) for o in olist1]
            [o.setEnabled(True) for o in olist2]
