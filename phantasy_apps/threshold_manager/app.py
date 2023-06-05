#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import toml
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from phantasy_ui import BaseAppForm
from phantasy_ui.widgets import DockWidget, SnapshotWidget
from phantasy_apps.threshold_manager._widget import MPSDiagWidget
from phantasy_apps.threshold_manager.ui.ui_app import Ui_MainWindow

OUT_DATA_DIR = "/tmp"

_CDIR = os.path.dirname(__file__)

def read_config(configpath: str):
    _c = toml.load(configpath)


class MPSThresholdManagerWindow(BaseAppForm, Ui_MainWindow):

    def __init__(self, version: str, configpath: str):
        super().__init__()

        self._version = version
        self.setWindowTitle("MPS Threshold Data Manager")
        self.setAppTitle("MPS Threshold Data Manager")
        self.setAppVersion(self._version)

        self.app_about_info = """
            <html>
            <h4>About Threshold Data Manager</h4>
            <p>This app is created to manage the diagostics threshold data for MPS configuration, current version is {}.
            </p>
            <p>Copyright (C) 2023 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)
        self.postInitUi()

        self._post_init()
        # resizing
        self.resize(1920, 1440)

    def _post_init(self):
        self.nd_widget = MPSDiagWidget("ND", OUT_DATA_DIR)
        self.ic_widget = MPSDiagWidget("IC", OUT_DATA_DIR)
        self.hmr_widget = MPSDiagWidget("HMR", OUT_DATA_DIR)

        self.nd_dock = DockWidget(self)
        self.nd_dock.setWindowTitle("Neutron Detectors")
        self.ic_dock = DockWidget(self)
        self.ic_dock.setWindowTitle("Ionization Chambers")
        self.hmr_dock = DockWidget(self)
        self.hmr_dock.setWindowTitle("Halo Monitor Rings")

        self.nd_dock.setWidget(self.nd_widget)
        self.ic_dock.setWidget(self.ic_widget)
        self.hmr_dock.setWidget(self.hmr_widget)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.nd_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.ic_dock)
        self.tabifyDockWidget(self.nd_dock, self.ic_dock)
        self.tabifyDockWidget(self.ic_dock, self.hmr_dock)
        QTimer.singleShot(50, lambda:self.nd_dock.raise_())

        # snapshot dock
        self.snp_widget = SnapshotWidget("ND")
        self.snp_dock = DockWidget(self)
        self.snp_dock.setWindowTitle("Snapshots")
        self.snp_dock.setWidget(self.snp_widget)
        self.addDockWidget(Qt.TopDockWidgetArea, self.snp_dock)

        #
        for i in (self.nd_widget, self.ic_widget, self.hmr_widget):
            i.set_snp_parent(self.snp_widget)

        # test:
        test_db_path = os.path.join(_CDIR, "tests/mps_model/test.db")
        self.snp_widget.db_path_lineEdit.setText(test_db_path)
        self.snp_widget.db_open_btn.click()


    def resizeEvent(self, e):
        # resize dock widget
        self.resizeDocks([self.nd_dock, self.ic_dock, self.hmr_dock],
                [self.width(), self.width(), self.width()], Qt.Horizontal)
        BaseAppForm.resizeEvent(self, e)


    @pyqtSlot()
    def onTakeSnapshot(self):
        """Take snapshots for all pages.
        """
        print("Take a new snapshot.")
