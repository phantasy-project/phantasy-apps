#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot

from .data import SnapshotData

from .ui.ui_snpdiff import Ui_Form


class SnapshotDiffWidget(QWidget, Ui_Form):

    snapshotsChanged = pyqtSignal()
    snapshotLeftChanged = pyqtSignal(SnapshotData)
    snapshotRightChanged = pyqtSignal(SnapshotData)

    def __init__(self, parent):
        super(self.__class__, self).__init__()
        self.parent = parent
        self.snp_dq = self.parent._snp_diff_dq

        self.setupUi(self)
        self.setWindowTitle("Snapshot DiffView")

        self._post_init()

    @pyqtSlot()
    def onRefreshDiff(self):
        """Refresh diff view as snapshots (either left or right) are changed.
        """
        for snp_data, sig in zip(self.snp_dq,
                                (self.snapshotLeftChanged, self.snapshotRightChanged)):
            sig.emit(snp_data)

    def _post_init(self):
        #
        self.snapshotsChanged.connect(self.onRefreshDiff)
        self.snapshotLeftChanged.connect(self.onSnapshotLeftChanged)
        self.snapshotRightChanged.connect(self.onSnapshotRightChanged)

        #
        self.diff_level_rgrp.setId(self.enable_reldiff_rbtn, 0)
        self.diff_level_rgrp.setId(self.enable_absdiff_rbtn, 1)
        self.diff_level_rgrp.idToggled.connect(self.onDiffLevelTypeChanged)
        # defaults absolute diff range
        self.enable_absdiff_rbtn.setChecked(True)

        #
        self.show_opt_rgrp.setId(self.show_outrange_rbtn, 0)
        self.show_opt_rgrp.setId(self.show_inrange_rbtn, 1)
        self.show_opt_rgrp.idToggled.connect(self.onShowOptChanged)
        # show out of diff range items only
        self.show_outrange_rbtn.setChecked(True)

    @pyqtSlot(int, bool)
    def onShowOptChanged(self, btn_id: int, checked: bool):
        """Show option changed, either show items out of diff range or in range.
        """
        if checked:
            print(f"Show button id {btn_id} is checked.")

    @pyqtSlot(int, bool)
    def onDiffLevelTypeChanged(self, btn_id: int, checked: bool):
        """Diff level type changed, either relative or absolute.
        """
        if checked:
            print(f"Diff Button id {btn_id} is checked.")

    @pyqtSlot(SnapshotData)
    def onSnapshotLeftChanged(self, data: SnapshotData):
        """The left snapshot data is changed.
        """
        self.snp_one_name_lbl.setText(f"{data.name} - {data.ion_as_str()}")

    @pyqtSlot(SnapshotData)
    def onSnapshotRightChanged(self, data: SnapshotData):
        """The right snapshot data is changed.
        """
        self.snp_two_name_lbl.setText(f"{data.name} - {data.ion_as_str()}")

