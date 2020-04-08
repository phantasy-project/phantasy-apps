#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from phantasy_ui import BaseAppForm

from .ui.ui_app import Ui_MainWindow


class VALauncherWindow(BaseAppForm, Ui_MainWindow):
    def __init__(self, version):
        super(VALauncherWindow, self).__init__()

        # app version
        self._version = version

        # window title/icon
        self.setWindowTitle("Virtual Accelerator Launcher")

        # set app properties
        self.setAppTitle("VA Launcher")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Virtual Accelerator Launcher</h4>
            <p>Start virtual accelerators of FRIB for app development,
            current version is {}.
            </p>
            <p>Copyright (C) 2018 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)
        self.postInitUi()
