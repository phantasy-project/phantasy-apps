#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import Qt

from .utils import get_ion_px
from .data import SnapshotData

from .ui.ui_snpdiff import Ui_Form

X0 = 'x\N{SUBSCRIPT ZERO}'
Y0 = 'y\N{SUBSCRIPT ZERO}'


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

        if len(self.snp_dq) != 2:
            return
        df_diffmerge = snp_diff(self.snp_dq[0], self.snp_dq[1])
        # update diff view
        self.m = DiffDataModel(df_diffmerge, self)
        self.snpdiffView.setModel(self.m)
        self.snpdiffView.resizeColumnsToContents()
        self.snpdiffView.resizeRowsToContents()
        # trigger filter
        self.applyFilter()

    def applyFilter(self):
        self.show_opt_rgrp.idToggled.emit(self.show_opt_rgrp.checkedId(), True)

    def _post_init(self):
        #
        self.splitter.setSizes([1, 10000])
        #
        self.absdiff_lineEdit.setValidator(QDoubleValidator(0.0, 9999, 4))
        self.absdiff_lineEdit.returnPressed.connect(self.applyFilter)
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

        #
        self.snpdiffView.setItemDelegate(DiffDataDelegateModel(self.snpdiffView))

    @pyqtSlot(int, bool)
    def onShowOptChanged(self, btn_id: int, checked: bool):
        """Show option changed, either show items out of diff range or in range.
        """
        m = self.snpdiffView.model()
        if m is None:
            return
        is_reldiff, v_diff = self.get_diff_range()
        df0 = snp_diff(self.snp_dq[0], self.snp_dq[1])
        if btn_id == 0: # show items beyond diff range
            if is_reldiff:
                df = df0[(df0["dx"]/df0["Setpoint_1"] < -v_diff) | (df0["dx"]/df0["Setpoint_1"] > v_diff)]
            else:
                df = df0[(df0["dx"] < -v_diff) | (df0["dx"] > v_diff)]
        else: # show items within diff range
            if is_reldiff:
                df = df0[(df0["dx"]/df0["Setpoint_1"] >= -v_diff) & (df0["dx"]/df0["Setpoint_1"] <= v_diff)]
            else:
                df = df0[(df0["dx"] >= -v_diff) & (df0["dx"] <= v_diff)]
        self.m.updateData(df)

    @pyqtSlot(int, bool)
    def onDiffLevelTypeChanged(self, btn_id: int, checked: bool):
        """Diff level type changed, either relative or absolute.
        """
        m = self.snpdiffView.model()
        if m is None:
            return
        self.applyFilter()

    @pyqtSlot(SnapshotData)
    def onSnapshotLeftChanged(self, data: SnapshotData):
        """The left snapshot data is changed.
        """
        self.snp_one_name_lbl.setText(f"{data.name} - {data.ion_as_str()}")
        self.snp_one_note_plainTextEdit.setPlainText(data.note)
        self.snp_one_pix.setPixmap(get_ion_px(data.ion_name, 64))
        self.snp_one_isrc_name_lbl.setText(get_isrc_name(data))

    @pyqtSlot(SnapshotData)
    def onSnapshotRightChanged(self, data: SnapshotData):
        """The right snapshot data is changed.
        """
        self.snp_two_name_lbl.setText(f"{data.name} - {data.ion_as_str()}")
        self.snp_two_note_plainTextEdit.setPlainText(data.note)
        self.snp_two_pix.setPixmap(get_ion_px(data.ion_name, 64))
        self.snp_two_isrc_name_lbl.setText(get_isrc_name(data))

    def get_diff_range(self):
        """Return the range of discrenpancy level.
        """
        if self.diff_level_rgrp.checkedId() == 0: # relative diff
            v_diff = self.reldiff_sbox.value() / 100
            is_rel = True
        else:
            v_diff = float(self.absdiff_lineEdit.text())
            is_rel = False
        return is_rel, v_diff


class DiffDataModel(QAbstractTableModel):
    ColumnName, ColumnField, ColumnSetpoint_1, ColumnSetpoint_2, ColumnSetpoint_d12, \
            ColumnSetpoint_r12, ColumnCount = range(7)

    columnNameMap = {
        ColumnName: "Device\nName",
        ColumnField: "Field\nName",
        ColumnSetpoint_1: f"SavedSet1\n({X0})",
        ColumnSetpoint_2: f"SavedSet2\n({Y0})",
        ColumnSetpoint_d12: f"SavedSet1-SavedSet2\n({X0}-{Y0})",
        ColumnSetpoint_r12: f"SavedSet1/SavedSet2\n({X0}/{Y0})",
    }

    def __init__(self, data: pd.DataFrame, parent=None):
        super(self.__class__, self).__init__(parent)
        self.df = data

    def rowCount(self, parent=None):
        return len(self.df.index)

    def columnCount(self, parent=None):
        return self.ColumnCount

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None

        row, column = index.row(), index.column()
        if role == Qt.DisplayRole:
            if column == self.ColumnName or column == self.ColumnField:
                return self.df.iloc[row, column]
            else:
                return f"{self.df.iloc[row, column]:.6g}"

        return None

    def headerData(self, section: int, orientaion: Qt.Orientation, role: int):
        if role == Qt.DisplayRole:
            if orientaion == Qt.Horizontal:
                return self.columnNameMap.get(section)
            else:
                return str(section + 1)
        return None

    def updateData(self, df: pd.DataFrame):
        """Update the data
        """
        self.beginResetModel()
        self.df = df
        self.endResetModel()


class DiffDataDelegateModel(QStyledItemDelegate):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__()

    def sizeHint(self, option, index):
        size = QStyledItemDelegate.sizeHint(self, option, index)
        size.setHeight(int(size.height() * 1.1))
        return size

    def paint(self, painter, option, index):
        if index.column() == DiffDataModel.ColumnField:
            option.displayAlignment = Qt.AlignHCenter | Qt.AlignVCenter
        elif index.column() == DiffDataModel.ColumnName:
            option.displayAlignment = Qt.AlignLeft | Qt.AlignVCenter
        else:
            option.displayAlignment = Qt.AlignRight | Qt.AlignVCenter

        QStyledItemDelegate.paint(self, painter, option, index)


def get_isrc_name(snp: SnapshotData):
    """Get (guess) the ion source name from the saved data.
    """
    snp.extract_blob()
    if snp.data.Name.str.contains('FE_ISRC1:BEAM').any():
        return "Artemis"
    elif snp.data.Name.str.contains('FE_ISRC2:BEAM').any():
        return "HP-ECR"
    else:
        return "TBD"


def snp_diff(snp1: SnapshotData, snp2: SnapshotData):
    """Return a dataframe from the given two SnapshotData
    """
    col_list = ['Name', 'Field', 'Setpoint']
    snp1.extract_blob()
    snp2.extract_blob()
    df1 = snp1.data[col_list]
    df2 = snp2.data[col_list]
    df12 = pd.merge(df1, df2, on=['Name', 'Field'], how='outer', suffixes=("_1", "_2"))
    df12['dx'] = df12['Setpoint_1'] - df12['Setpoint_2']
    df12['x1/x2'] = df12['Setpoint_1'] / df12['Setpoint_2']
    return df12