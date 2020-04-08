#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import partial

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot

from PyQt5.QtGui import QColor
from PyQt5.QtGui import QBrush

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QListWidgetItem

from phantasy_ui import BaseAppForm
from phantasy_ui.widgets import VirtualAcceleratorWidget

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

        #
        self._post_init()

    def _post_init(self):
        # list of tuple of va_page and va_list_item
        self._va_page_item_list = []

        # initialize the first tab page
        self.va_tab.currentChanged.emit(self.va_tab.count() - 1)

    @pyqtSlot(int)
    def on_current_tab_changed(self, index):
        """Current tab is changed.
        """
        if index == self.va_tab.count() - 1:
            w = self.create_new_va_page()
            self.va_tab.insertTab(index, w, "")
            self.va_tab.setCurrentIndex(index)
            va_page = w.findChild(VirtualAcceleratorWidget)
            va_list_item = QListWidgetItem("")
            va_page.sig_va_status_changed['QString', QColor].connect(
                    lambda s,c:va_list_item.setBackground(QBrush(c)))
            va_page.sig_va_name_changed['QString'].connect(va_list_item.setText)
            va_page.sig_va_name_changed[tuple].connect(
                    lambda t:self.va_tab.setTabText(index, t[1]))
            va_page.reinit_va_info()
            self.va_listWidget.addItem(va_list_item)
            self._va_page_item_list.append((va_page, va_list_item))

    def create_new_va_page(self):
        w = QWidget()
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(VirtualAcceleratorWidget(w))
        vbox.addStretch(1)
        w.setLayout(vbox)
        return w
