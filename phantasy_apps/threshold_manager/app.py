#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functools import partial
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QWidget, QSizePolicy
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from phantasy_ui import BaseAppForm
from phantasy_ui import delayed_exec
from phantasy_ui.widgets import DockWidget, BeamSpeciesDisplayWidget
from phantasy_apps.threshold_manager._widget import MPSDiagWidget, SnapshotWidget
from phantasy_apps.threshold_manager.ui.ui_app import Ui_MainWindow
from phantasy_apps.threshold_manager.tools import take_snapshot
from phantasy_apps.threshold_manager.data import read_config


class MPSThresholdManagerWindow(BaseAppForm, Ui_MainWindow):

    def __init__(self, version: str, configpath: str):
        super().__init__()

        self._version = version
        self.config_dict = read_config(configpath)
        self.setWindowTitle("MPS Data Manager")
        self.setAppTitle("MPS Data Manager")
        self.setAppVersion(self._version)

        self.app_about_info = """
            <html>
            <h4>About MPS Data Manager</h4>
            <p>This app is created to manage the diagostic threshold data for MPS configurations, current version is {}.
            </p>
            <p>Copyright (C) 2023 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)
        self.postInitUi()

        # resizing
        self.resize(1920, 1440)

        self.__set_up_post_0()
        self.__set_up_events()
        self.__set_up_post_1()

    def __set_up_post_0(self):
        # prior events binding

        # add beamSpeciesDisplayWidget
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolBar.addWidget(spacer)
        self.beam_display_widget = BeamSpeciesDisplayWidget()
        self.beam_display_widget.set_wait_until_ready(True)
        self.beam_display_widget.set_expanded(True)
        self.beam_display_widget.set_power_panel(True)
        self.beam_display_widget.set_allow_clicking_src_btns(False)
        self.toolBar.addWidget(self.beam_display_widget)

        #
        self.nd_widget = MPSDiagWidget("ND")
        self.ic_widget = MPSDiagWidget("IC")
        self.hmr_widget = MPSDiagWidget("HMR")

        self.nd_dock = DockWidget(self)
        self.nd_dock.setWindowTitle("Neutron Detectors")
        self.nd_dock.setTitleText("Read-Only MPS Threshold Configurations (ND)")
        self.ic_dock = DockWidget(self)
        self.ic_dock.setWindowTitle("Ionization Chambers")
        self.ic_dock.setTitleText("Read-Only MPS Threshold Configurations (IC)")
        self.hmr_dock = DockWidget(self)
        self.hmr_dock.setWindowTitle("Halo Monitor Rings")
        self.hmr_dock.setTitleText("Read-Only MPS Threshold Configurations (HMR)")

        self.nd_dock.setWidget(self.nd_widget)
        self.ic_dock.setWidget(self.ic_widget)
        self.hmr_dock.setWidget(self.hmr_widget)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.nd_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.ic_dock)
        self.tabifyDockWidget(self.nd_dock, self.ic_dock)
        self.tabifyDockWidget(self.ic_dock, self.hmr_dock)
        #
        self.setTabPosition(Qt.LeftDockWidgetArea, QTabWidget.North);

        # snapshot dock
        self.snp_widget = SnapshotWidget("ND")
        self.snp_dock = DockWidget(self)
        self.snp_dock.setStyleSheet("""
            QDockWidget::title {
                background: #8AE234;
        }""")
        self.snp_dock.setWindowTitle("Snapshots")
        self.snp_dock.setWidget(self.snp_widget)
        self.addDockWidget(Qt.TopDockWidgetArea, self.snp_dock)

        #
        for i in (self.nd_widget, self.ic_widget, self.hmr_widget):
            i.set_snp_parent(self.snp_widget)

    def __set_up_events(self):
        # menu actions, dock widgets
        for act, dock in zip(
            (self.actionViewSNP, self.actionViewND, self.actionViewIC,
             self.actionViewHMR),
            (self.snp_dock, self.nd_dock, self.ic_dock, self.hmr_dock)):
            act.toggled.connect(partial(self.onToggleDock, dock))
            dock.closed.connect(partial(self.onCloseDock, act))
            dock.topLevelChanged.connect(self.onDockTopLevelChanged)
        # snapshot widget
        self.snp_widget.textCopied.connect(self.statusInfoChanged)

        for w in (self.nd_widget, self.ic_widget, self.hmr_widget):
            w.dataSaved.connect(self.snp_widget.db_open_btn.click)
            # locate snapshot for diff
            w.snapshotToLocate.connect(self.snp_widget.onHighlightSnapshot)

        # dataloaded connection
        self.snp_widget.ndDataLoaded.connect(self.nd_widget.onDataLoaded)
        self.snp_widget.icDataLoaded.connect(self.ic_widget.onDataLoaded)
        self.snp_widget.hmrDataLoaded.connect(self.hmr_widget.onDataLoaded)

    @pyqtSlot(bool)
    def onDockTopLevelChanged(self, is_floating: bool):
        dock = self.sender()
        if is_floating:
            dock.setWindowFlags(Qt.CustomizeWindowHint | Qt.Window
                                | Qt.WindowMinimizeButtonHint
                                | Qt.WindowMaximizeButtonHint
                                | Qt.WindowCloseButtonHint)

            dock.show()

    @pyqtSlot(bool)
    def onToggleDock(self, dock: DockWidget, is_checked: bool):
        if is_checked:
            dock.show()
        else:
            dock.close()

    @pyqtSlot()
    def onCloseDock(self, act: QAction):
        """Sync View/dock menu when dock is closed.
        """
        act.setChecked(False)

    def __set_up_post_1(self):
        # post events binding
        #
        # show and raise nd dock tab
        delayed_exec(lambda: self.nd_dock.raise_(), 50)

        # start nd and ic, pause hmr
        self.nd_widget.refresh_data(auto=True)
        self.ic_widget.refresh_data(auto=True)
        self.hmr_widget.refresh_data(auto=False)

        # open the database
        db_path = self.config_dict['db_uri']
        self.snp_widget.db_path_lineEdit.setText(db_path)
        self.snp_widget.db_open_btn.click()

    def resizeEvent(self, e):
        # resize dock widget
        self.resizeDocks(
            [self.nd_dock, self.ic_dock, self.hmr_dock],
            [self.width(), self.width(),
             self.width()], Qt.Horizontal)
        BaseAppForm.resizeEvent(self, e)

    @pyqtSlot()
    def onTakeSnapshot(self):
        """Take snapshots for all pages.
        """
        take_snapshot(['ND', 'IC', 'HMR'],
                      note='Full snapshot for ND,IC,HMR',
                      tags=['ND', 'IC', 'HMR'],
                      conn=self.snp_widget.get_db_conn())
        self.snp_widget.db_open_btn.click()
