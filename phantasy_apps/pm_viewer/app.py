#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from phantasy_ui import BaseAppForm

from .ui.ui_app import Ui_MainWindow


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

