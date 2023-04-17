#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import toml
from phantasy_ui import BaseAppForm
from phantasy_apps.threshold_manager._widget import MPSDiagWidget
from phantasy_apps.threshold_manager._widget import SnapshotWidget
from phantasy_apps.threshold_manager.ui.ui_app import Ui_MainWindow

OUT_DATA_DIR = "/tmp"


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
        # resizing
        self.resize(1920, 1440)

        self._post_init()

    def _post_init(self):
        self.nd_widget = MPSDiagWidget("ND", OUT_DATA_DIR)
        self.ic_widget = MPSDiagWidget("IC", OUT_DATA_DIR)
        self.hmr_widget = MPSDiagWidget("HMR", OUT_DATA_DIR)

        self.nb_hbox.addWidget(self.nd_widget)
        self.ic_hbox.addWidget(self.ic_widget)
        self.hmr_hbox.addWidget(self.hmr_widget)

        self.snp_widget = SnapshotWidget("ND")
        self.snp_hbox.addWidget(self.snp_widget)

        # test:
        test_db_path = "/home/tong/Dropbox/phantasy-project/phantasy-apps/phantasy_apps/threshold_manager/tests/mps_model/test.db"
        self.snp_widget.db_path_lineEdit.setText(test_db_path)
