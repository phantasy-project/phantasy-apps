#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import pandas as pd
from phantasy import MachinePortal
from phantasy_ui.widgets import DataAcquisitionThread as DAQT
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QModelIndex

COLUMNS = [
    'Device', 'Average', 'Peak Avg.', '1 MHz Std.', 'Avg. Time',
    'LongAvg.Th(H)', 'LongAvg.Th(H)?', 'LongAvg.Th(L)', 'LongAvg.Th(L)?',
    '10ms Th(H)', '10ms Th(H)?', '10ms Th(L)', '10ms Th(L)?',
    '1500us Th(H)', '1500us Th(H)?', '1500us Th(L)', '1500us Th(L)?',
    '150us Th(H)', '150us Th(H)?', '150us Th(L)', '150us Th(L)?',
    '15us Th(H)', '15us Th(H)?', '15us Th(L)', '15us Th(L)?',
]

ROW_HEIGHT = 48
PX_SIZE = 20

MP = MachinePortal("FRIB", "MPS")
NAME_MAP = {i.name: i for i in MP.get_elements(name='*')}
DF_ELEM_ND = pd.DataFrame.from_records(
    [[i.name] + 24 * ['-'] for i in MP.get_elements(type='ND')], columns=COLUMNS)
DF_ELEM_IC = pd.DataFrame.from_records(
    [[i.name] + 24 * ['-'] for i in MP.get_elements(type='IC')], columns=COLUMNS)
DF_ELEM_HMR = pd.DataFrame.from_records(
    [[i.name] + 24 * ['-'] for i in MP.get_elements(type='HMR')], columns=COLUMNS)

GREEK_MU = u'\N{GREEK SMALL LETTER MU}'
UNIT_MAP = {
    'ND': f'{GREEK_MU}A',
    'IC': f'{GREEK_MU}A',
    'HMR': f'{GREEK_MU}A',
}

DF_MAP = {
    'ND': DF_ELEM_ND,
    'IC': DF_ELEM_IC,
    'HMR': DF_ELEM_HMR,
}


def _gen_data(irow: pd.Series):
    """Get a row of data for device of *name*.
    """
    name = irow.Device
    elem = NAME_MAP[name]
    mps_trip_bits = format(elem.MPS_EN_CMD, "08b")
    _10ms_h, _10ms_l, _1500us_h, _1500us_l, _150us_h, _150us_l, _15us_h, _15us_l = \
        [int(i) for i in list(mps_trip_bits)]
    _10ms_th_h, _10ms_th_l = elem.MPS_10MSHI_TH, elem.MPS_10MSLO_TH
    _1500us_th_h, _1500us_th_l = elem.MPS_1500USHI_TH, elem.MPS_1500USLO_TH
    _150us_th_h, _150us_th_l = elem.MPS_150USHI_TH, elem.MPS_150USLO_TH
    _15us_th_h, _15us_th_l = elem.MPS_15USHI_TH, elem.MPS_15USLO_TH
    # long average
    _lavg_h, _lavg_l = elem.MPS_EN_CMD_LAVGHI, elem.MPS_EN_CMD_LAVGLO
    _lavg_th_h, _lavg_th_l = elem.MPS_LAVGHI_TH, elem.MPS_LAVGLO_TH
    _lavg, _lavg_t = elem.LAVG, elem.MPS_LAVG_T
    _pkavg = elem.PKAVG
    _std = elem.STD
    return name, _lavg, _pkavg, _std, _lavg_t, \
        _lavg_th_h, _lavg_h, _lavg_th_l, _lavg_l, \
        _10ms_th_h, _10ms_h, _10ms_th_l, _10ms_l, \
        _1500us_th_h, _1500us_h, _1500us_th_l, _1500us_l, \
        _150us_th_h, _150us_h, _150us_th_l, _150us_l, \
        _15us_th_h, _15us_h, _15us_th_l, _15us_l


def _get_dataframe(dtype: str):
    # test with local data
    # df = pd.read_csv('tests/mps_model/test.csv', index_col=0)

    # with live data
    _s = DF_MAP[dtype].apply(_gen_data, axis=1)
    df = pd.DataFrame.from_records(_s.to_list(), columns=COLUMNS)
    return df


class MPSBeamLossDataModel(QAbstractTableModel):

    # column ids
    ColumnDevice, ColumnLongAvg, ColumnPeakAvg, ColumnStd, ColumnLongAvgTime, \
        ColumnLAvgThHi, ColumnLAvgThHi_E, ColumnLAvgThLo, ColumnLAvgThLo_E, \
        Column10msThHi, Column10msThHi_E, Column10msThLo, Column10msThLo_E, \
        Column1500usThHi, Column1500usThHi_E, Column1500usThLo, Column1500usThLo_E, \
        Column150usThHi, Column150usThHi_E, Column150usThLo, Column150usThLo_E, \
        Column15usThHi, Column15usThHi_E, Column15usThLo, Column15usThLo_E, \
        ColumnCount = range(26)

    # column names
    columnNameMap = {
        ColumnDevice: "Device\nName",
        ColumnLongAvg: "Long\nAverage",
        ColumnPeakAvg: "Peak\nAverage",
        ColumnStd: "1 MHz\nStd.",
        ColumnLongAvgTime: "Long Avg.\nTime",
        ColumnLAvgThHi: "Long Avg.(High)\nThreshold",
        ColumnLAvgThHi_E: "",
        ColumnLAvgThLo: "Long Avg.(Low)\nThreshold",
        ColumnLAvgThLo_E: "",
        Column10msThHi: "10 ms (High)\nThreshold",
        Column10msThHi_E: "",
        Column10msThLo: "10 ms (Low)\nThreshold",
        Column10msThLo_E: "",
        Column1500usThHi: f"1500 {GREEK_MU}s (High)\nThreshold",
        Column1500usThHi_E: "",
        Column1500usThLo: f"1500 {GREEK_MU}s (Low)\nThreshold",
        Column1500usThLo_E: "",
        Column150usThHi: f"150 {GREEK_MU}s (High)\nThreshold",
        Column150usThHi_E: "",
        Column150usThLo: f"150 {GREEK_MU}s (Low)\nThreshold",
        Column150usThLo_E: "",
        Column15usThHi: f"15 {GREEK_MU}s (High)\nThreshold",
        Column15usThHi_E: "",
        Column15usThLo: f"15 {GREEK_MU}s (Low)\nThreshold",
        Column15usThLo_E: "",
    }

    CHK_COLUMNS = (
        ColumnLAvgThHi_E, Column10msThHi_E, Column1500usThHi_E, Column150usThHi_E, Column15usThHi_E,
        ColumnLAvgThLo_E, Column10msThLo_E, Column1500usThLo_E, Column150usThLo_E, Column15usThLo_E
    )
    STR_COLUMNS = (ColumnDevice,)

    columnFormat = {
        ColumnLongAvg: "{value:.6f} {unit}",
        ColumnPeakAvg: "{value:.3f} {unit}",
        ColumnStd: "{value:.3f} {unit}",
        ColumnLongAvgTime: "{value:.1f} s",
        ColumnLAvgThHi: "{value:.2e} {unit}",
        ColumnLAvgThLo: "{value:.2e} {unit}",
        Column10msThHi: "{value:.2e} {unit}",
        Column10msThLo: "{value:.2e} {unit}",
        Column1500usThHi: "{value:.2e} {unit}",
        Column1500usThLo: "{value:.2e} {unit}",
        Column150usThHi: "{value:.2e} {unit}",
        Column150usThLo: "{value:.2e} {unit}",
        Column15usThHi: "{value:.2e} {unit}",
        Column15usThLo: "{value:.2e} {unit}",
    }

    columnHiddenMap = {
        'ND': (
            ColumnLAvgThHi, Column10msThHi, Column1500usThHi, Column150usThHi, Column15usThHi,
            ColumnLAvgThHi_E, Column10msThHi_E, Column1500usThHi_E, Column150usThHi_E, Column15usThHi_E
        ),
        'IC': (
            ColumnLAvgThHi, Column10msThHi, Column1500usThHi, Column150usThHi, Column15usThHi,
            ColumnLAvgThHi_E, Column10msThHi_E, Column1500usThHi_E, Column150usThHi_E, Column15usThHi_E
        ),
        'HMR': (
            ColumnLAvgThLo, Column10msThLo, Column1500usThLo, Column150usThLo, Column15usThLo,
            ColumnLAvgThLo_E, Column10msThLo_E, Column1500usThLo_E, Column150usThLo_E, Column15usThLo_E
        ),
    }

    #
    dataframeUpdated = pyqtSignal(pd.DataFrame)
    # data refreshing started
    dataRefreshStarted = pyqtSignal()
    # data refreshing stopped
    dataRefreshStopped = pyqtSignal()

    def __init__(self, device_type: str, parent=None):
        super(self.__class__, self).__init__(parent)
        #
        self.device_type = device_type
        self._unit = UNIT_MAP[device_type]
        data = DF_MAP[device_type]
        self.set_dataframe(data)
        #
        self.__post_init()
        # start data refreshing thread
        self.dataframeUpdated.connect(self.update_dataframe)

        #
        self.refresh_data()

    def __post_init(self):
        #
        pass

    def columnCount(self, parent=None):
        return self.ColumnCount

    def rowCount(self, parent):
        if parent.isValid():
            return 0
        return self._data.shape[0]

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None
        row, column = index.row(), index.column()
        v = self._data.iloc[row, column]
        if role == Qt.DisplayRole and column not in MPSBeamLossDataModel.CHK_COLUMNS:
            if v != '-' and column in MPSBeamLossDataModel.columnFormat:
                return MPSBeamLossDataModel.columnFormat[column].format(
                    value=float(v), unit=self._unit)
            else:
                return v

        if role == Qt.DecorationRole:
            if column in MPSBeamLossDataModel.CHK_COLUMNS:
                if v == 1.0:
                    return QPixmap(":/sm-icons/check-square-fill.png").scaled(PX_SIZE, PX_SIZE,
                                                                              Qt.KeepAspectRatio, Qt.SmoothTransformation)
                else:  # v == 0.0
                    return QPixmap(":/sm-icons/uncheck-square.png").scaled(PX_SIZE, PX_SIZE,
                                                                           Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # elif role == Qt.CheckStateRole and column == self.ColumnDevice:
        #    return Qt.Checked if self._data['_checkState'].iat[row] else Qt.Unchecked
        # elif role == Qt.UserRole + 10: # not writable
        #    return self._data.Writable.iat[row] == False

    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole):
        # if role == Qt.CheckStateRole:
        #     self._data['_checkState'].iat[index.row()] = value == Qt.Checked
        return True

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if orientation != Qt.Horizontal:
            return None
        if role != Qt.DisplayRole:
            return None
        return self.columnNameMap.get(section)

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return Qt.NoItemFlags
        if self.data(index, Qt.UserRole + 10):
            return Qt.NoItemFlags
        # if index.column() == self.ColumnDevice:
        #    return Qt.ItemIsUserCheckable | QAbstractItemModel.flags(self, index)
        return QAbstractTableModel.flags(self, index)

    def set_dataframe(self, df: pd.DataFrame):
        self._data = df

    def update_dataframe(self, df: pd.DataFrame):
        # update data
        t0 = time.time()
        self.layoutAboutToBeChanged.emit()
        self.set_dataframe(df)
        self.layoutChanged.emit()

    def refresh_data(self):
        def _onUpdateData(i):
            t0 = time.time()
            # update data
            self._data = _get_dataframe(self.device_type)
            self.dataframeUpdated.emit(self._data)
            print(
                f"[{self.device_type}] Data Refreshed: {(time.time() - t0) * 1e3:.1f} ms")
        #
        self._th = DAQT(daq_func=_onUpdateData, daq_seq=range(1))
        self._th.daqStarted.connect(self.dataRefreshStarted)
        self._th.daqFinished.connect(self.dataRefreshStopped)
        self._th.start()

    def get_hidden_columns(self):
        return MPSBeamLossDataModel.columnHiddenMap[self.device_type]


class MPSBeamLossDataDelegateModel(QStyledItemDelegate):
    def __init__(self, parent=None, **kws):
        super(self.__class__, self).__init__()
        self.default_font_size = QFontDatabase.systemFont(
            QFontDatabase.FixedFont).pointSize()

    def sizeHint(self, option, index):
        size = QStyledItemDelegate.sizeHint(self, option, index)
        size.setHeight(int(ROW_HEIGHT * 0.8))
        return size

    def displayText(self, value, locale):
        if isinstance(value, (float, int)):
            return f"{value:.6f}"
        else:
            return str(value)

    def paint(self, painter, option, index):
        if index.column() in MPSBeamLossDataModel.STR_COLUMNS:
            option.displayAlignment = Qt.AlignRight | Qt.AlignVCenter
        else:
            option.displayAlignment = Qt.AlignRight | Qt.AlignVCenter
        QStyledItemDelegate.paint(self, painter, option, index)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QWidget, QTreeView, QVBoxLayout
    from PyQt5.QtCore import QSize
    import sys

    app = QApplication(sys.argv)
    w = QWidget()
    v = QTreeView(w)
    v.setStyleSheet("""
QHeaderView {
        font-weight: bold;
}

QTreeView {
    font-family: monospace;
    show-decoration-selected: 1;
    alternate-background-color: #D3D7CF;
}

QTreeView::item {
    /*color: black;*/
    border: 1px solid #D9D9D9;
    border-top-color: transparent;
    border-bottom-color: transparent;
}

QTreeView::item:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);
    border: 1px solid #bfcde4;
}

QTreeView::item:selected {
    border: 1px solid #567DBC;
    background-color: #D3D7CF;
}

QTreeView::item:selected:active{
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);
}""")
    v.setUniformRowHeights(True)
    layout = QVBoxLayout()
    layout.setContentsMargins(2, 2, 2, 2)
    layout.addWidget(v)
    w.setLayout(layout)

    # set model
    m = MPSBeamLossDataModel('ND')
    v.setItemDelegate(MPSBeamLossDataDelegateModel(v))
    v.setModel(m)
    for _ic in range(m.ColumnCount):
        v.resizeColumnToContents(_ic)

    w.show()
    w.setWindowTitle("MPS Configurations for Beam Loss Threshold")
    w.resize(QSize(800, 600))

    sys.exit(app.exec_())
