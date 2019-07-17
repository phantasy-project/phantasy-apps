#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog

from .ui.ui_settings import Ui_Dialog


class AppSettingsWidget(QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__()
        self.parent = parent

        self.setupUi(self)
        self.setWindowTitle("App Settings")


