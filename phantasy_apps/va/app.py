#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import partial

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot

from PyQt5.QtGui import QColor
from PyQt5.QtGui import QBrush

from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

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
        # events
        self.va_tab.currentChanged[int].connect(self.on_current_tab_changed)
        self.va_listWidget.currentItemChanged.connect(self.on_current_item_changed)

        # list of va widget and va_list_item
        self._va_widget_list = []
        self._va_item_list = []

        # initialize the first tab page
        self.va_tab.tabBarClicked.emit(self.va_tab.count() - 1)

    @pyqtSlot(int)
    def on_clicked_tabbar(self, index):
        """Clicked tabbar.
        """
        if index == self.va_tab.count() - 1:
            # dis
            self.va_tab.currentChanged[int].disconnect(self.on_current_tab_changed)
            self.va_listWidget.currentItemChanged.disconnect(self.on_current_item_changed)
            #
            w = self.create_new_va_page()
            self.va_tab.insertTab(index, w, "")
            va_widget = w.findChild(VirtualAcceleratorWidget)
            va_list_item = QListWidgetItem("")
            va_widget.sig_va_status_changed['QString', QColor].connect(
                    lambda s,c:va_list_item.setBackground(QBrush(c)))
            va_widget.sig_va_name_changed['QString'].connect(va_list_item.setText)
            va_widget.sig_va_name_changed[tuple].connect(
                    lambda t:self.va_tab.setTabText(index, t[1]))
            va_widget.reinit_va_info()
            self.va_listWidget.addItem(va_list_item)
            self._va_widget_list.append(va_widget)
            self._va_item_list.append(va_list_item)
            self.va_tab.setCurrentIndex(index)
            self.va_listWidget.setCurrentItem(va_list_item)
            # conn
            self.va_tab.currentChanged[int].connect(self.on_current_tab_changed)
            self.va_listWidget.currentItemChanged.connect(self.on_current_item_changed)

    @pyqtSlot(int)
    def on_current_tab_changed(self, index):
        """Current tab is changed.
        """
        if index == self.va_tab.count() - 1:
            pass
        else:
            widget = self.va_tab.widget(index).findChild(VirtualAcceleratorWidget)
            idx = self._va_widget_list.index(widget)
            self.va_listWidget.setCurrentRow(idx)

    def create_new_va_page(self):
        """Create va tab page.
        """
        w = QWidget()
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(VirtualAcceleratorWidget(w))
        vbox.addStretch(1)
        w.setLayout(vbox)
        return w

    @pyqtSlot()
    def on_delete_current_page(self):
        """Delete current selected VA page.
        """
        r = QMessageBox.question(self, "Delete VA",
                "Are you sure to delete and stop the current selected VA?",
                QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.Yes:
            if self.va_tab.count() == 2:
                QMessageBox.warning(self, "Delete VA",
                        "Cannot delete the last VA.",
                        QMessageBox.Ok)
                return
            # dis
            self.va_tab.currentChanged[int].disconnect(self.on_current_tab_changed)
            self.va_listWidget.currentItemChanged.disconnect(self.on_current_item_changed)

            current_widget = self.va_tab.currentWidget()
            va_widget = current_widget.findChild(VirtualAcceleratorWidget)
            idx = self._va_widget_list.index(va_widget)
            va_widget.close()
            current_index = self.va_tab.indexOf(current_widget)
            self.va_tab.removeTab(current_index)
            li = self.va_listWidget.takeItem(self.va_listWidget.currentRow())
            self._va_item_list.pop(idx)
            self._va_widget_list.pop(idx)
            del li
            # conn
            self.va_tab.currentChanged[int].connect(self.on_current_tab_changed)
            self.va_listWidget.currentItemChanged.connect(self.on_current_item_changed)
            # set previous as current tab
            self.va_tab.setCurrentIndex(current_index - 1)

    def on_current_item_changed(self, current_item, last_item):
        idx = self._va_item_list.index(current_item)
        va_widget = self._va_widget_list[idx]
        self.va_tab.setCurrentWidget(va_widget.parent())

    def closeEvent(self, e):
        r = QMessageBox.warning(self, "Warning", "Exit this application?",
                                QMessageBox.Cancel | QMessageBox.Yes,
                                QMessageBox.Cancel)
        if r == QMessageBox.Yes:
            for i in range(self.va_tab.count() - 1):
                page = self.va_tab.widget(i).findChild(VirtualAcceleratorWidget)
                page.close()
            e.accept()
        else:
            e.ignore()
