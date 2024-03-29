#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools
import time
import pandas as pd
import numpy as np
from functools import partial
from fnmatch import translate
from phantasy import MachinePortal
from phantasy_ui.widgets import DataAcquisitionThread as DAQT
from PyQt5.QtWidgets import (
    QStyledItemDelegate,
    QWidget,
)
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QModelIndex

COLUMNS = [
    'Device',
    'Average', # LAVG, long average
    'ShortAvg', # FAVG, short average
    'Peak Avg.',
    '1 MHz Std.',
    'Avg. Time',
    'LongAvg.Th(H)',
    'LongAvg.Th(H)?',
    'LongAvg.Th(L)',
    'LongAvg.Th(L)?',
    '10ms Th(H)',
    '10ms Th(H)?',
    '10ms Th(L)',
    '10ms Th(L)?',
    '1500us Th(H)',
    '1500us Th(H)?',
    '1500us Th(L)',
    '1500us Th(L)?',
    '150us Th(H)',
    '150us Th(H)?',
    '150us Th(L)',
    '150us Th(L)?',
    '15us Th(H)',
    '15us Th(H)?',
    '15us Th(L)',
    '15us Th(L)?',
]

ROW_HEIGHT = 36
PX_SIZE = 20
RED_COLOR = QColor(220, 53, 69, 240)
GREEN_COLOR = QColor(40, 167, 69, 240)
BLUE_COLOR = QColor(0, 123, 255, 240)
WHITE_COLOR = QColor(255, 255, 255, 255)
BLACK_COLOR = QColor(0, 0, 0, 255)
DIM_COLOR = QColor(0, 0, 0, 200)
FONT_NO_DIFF = QFontDatabase.systemFont(QFontDatabase.FixedFont)
FONT_DIFF = QFont(FONT_NO_DIFF)
FONT_DIFF.setWeight(QFont.DemiBold)

MP = MachinePortal("FRIB", "MPS", auto_monitor=True)
time.sleep(1.0)
NAME_MAP = {i.name: i for i in MP.get_elements(name='*')}
DF_ELEM_ND = pd.DataFrame.from_records([[i.name] + 25 * ['-']
                                        for i in MP.get_elements(type='ND')],
                                       columns=COLUMNS)
DF_ELEM_IC = pd.DataFrame.from_records([[i.name] + 25 * ['-']
                                        for i in MP.get_elements(type='IC')],
                                       columns=COLUMNS)
DF_ELEM_HMR = pd.DataFrame.from_records([[i.name] + 25 * ['-']
                                         for i in MP.get_elements(type='HMR')],
                                        columns=COLUMNS)

GREEK_MU = u'\N{GREEK SMALL LETTER MU}'
UNIT_MAP = {
    'ND': f' {GREEK_MU}A',
    'IC': f' {GREEK_MU}A',
    'HMR': f' {GREEK_MU}A',
}

DF_MAP = {
    'ND': DF_ELEM_ND,
    'IC': DF_ELEM_IC,
    'HMR': DF_ELEM_HMR,
}

DEST_COLOR_MAP = {
    'LEBT': '#5988E6',
    'MEBT': '#ED9800',
    'FS1A': '#54ED00',
    'FS1B': '#E8ED00',
    'TARGET': '#ED1700',
}


def _gen_data(irow: pd.Series):
    """Get a row of live data for device of *name*.
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
    _favg = elem.FAVG
    return name, _lavg, _favg, _pkavg, _std, _lavg_t, \
        _lavg_th_h, _lavg_h, _lavg_th_l, _lavg_l, \
        _10ms_th_h, _10ms_h, _10ms_th_l, _10ms_l, \
        _1500us_th_h, _1500us_h, _1500us_th_l, _1500us_l, \
        _150us_th_h, _150us_h, _150us_th_l, _150us_l, \
        _15us_th_h, _15us_h, _15us_th_l, _15us_l


def _gen_pv(irow: pd.Series):
    # AA
    name = irow.Device
    elem = NAME_MAP[name]
    # long avg
    _lavg_pv = elem.pv('LAVG', 'readback')[0]
    _lavg_t_pv = elem.pv('MPS_LAVG_T', 'readback')[0]
    # peak avg
    _pkavg_pv = elem.pv('PKAVG', 'readback')[0]
    # std
    _std_pv = elem.pv('STD', 'readback')[0]
    # long avg th
    _lavg_h_pv, _lavg_l_pv = elem.pv('MPS_EN_CMD_LAVGHI', 'readback')[0], elem.pv('MPS_EN_CMD_LAVGLO', 'readback')[0]
    _lavg_th_h_pv, _lavg_th_l_pv = elem.pv('MPS_LAVGHI_TH', 'readback')[0], elem.pv('MPS_LAVGLO_TH', 'readback')[0]
    # switches
    mps_trip_bits_pv = elem.pv('MPS_EN_CMD', 'readback')[0]
    # thresholds
    _10ms_th_h_pv, _10ms_th_l_pv = elem.pv('MPS_10MSHI_TH', 'readback')[0], elem.pv('MPS_10MSLO_TH', 'readback')[0]
    _1500us_th_h_pv, _1500us_th_l_pv = elem.pv('MPS_1500USHI_TH', 'readback')[0], elem.pv('MPS_1500USLO_TH', 'readback')[0]
    _150us_th_h_pv, _150us_th_l_pv = elem.pv('MPS_150USHI_TH', 'readback')[0], elem.pv('MPS_150USLO_TH', 'readback')[0]
    _15us_th_h_pv, _15us_th_l_pv = elem.pv('MPS_15USHI_TH', 'readback')[0], elem.pv('MPS_15USLO_TH', 'readback')[0]
    return _lavg_pv, _pkavg_pv, _std_pv, _lavg_t_pv, \
           _lavg_th_h_pv, _lavg_h_pv, _lavg_th_l_pv, _lavg_l_pv, \
           mps_trip_bits_pv, \
           _10ms_th_h_pv, _10ms_th_l_pv, \
           _1500us_th_h_pv, _1500us_th_l_pv, \
           _150us_th_h_pv, _150us_th_l_pv, \
           _15us_th_h_pv, _15us_th_l_pv


def get_pv(dtype: str):
    # AA
    """Return an iterate object for all the PVs.
    """
    _s = DF_MAP[dtype].apply(_gen_pv, axis=1)
    pvlist_it = itertools.chain(*_s.tolist())
    return pvlist_it


def _get_cell_value(data_dict: dict, irow: pd.Series):
    # AA
    """Return a list of tuple of cell values as diag snapshot dataset.
    """
    _lavg_pv, _pkavg_pv, _std_pv, _lavg_t_pv, \
     _lavg_th_h_pv, _lavg_h_pv, _lavg_th_l_pv, _lavg_l_pv, \
     mps_trip_bits_pv, \
     _10ms_th_h_pv, _10ms_th_l_pv, \
     _1500us_th_h_pv, _1500us_th_l_pv, \
     _150us_th_h_pv, _150us_th_l_pv, \
     _15us_th_h_pv, _15us_th_l_pv = _gen_pv(irow)

    mps_bit_v = data_dict.get(mps_trip_bits_pv)
    if mps_bit_v is None:
        return irow.Device, *[None] * 24
    else:
        mps_trip_bits = format(int(mps_bit_v), "08b")

    _10ms_h, _10ms_l, _1500us_h, _1500us_l, _150us_h, _150us_l, _15us_h, _15us_l = \
        [int(i) for i in list(mps_trip_bits)]
    _10ms_th_h, _10ms_th_l = data_dict.get(_10ms_th_h_pv), data_dict.get(_10ms_th_l_pv)
    _1500us_th_h, _1500us_th_l = data_dict.get(_1500us_th_h_pv), data_dict.get(_1500us_th_l_pv)
    _150us_th_h, _150us_th_l = data_dict.get(_150us_th_h_pv), data_dict.get(_150us_th_l_pv)
    _15us_th_h, _15us_th_l = data_dict.get(_15us_th_h_pv), data_dict.get(_15us_th_l_pv)
    # long average
    _lavg_h, _lavg_l = data_dict.get(_lavg_h_pv), data_dict.get(_lavg_l_pv)
    _lavg_th_h, _lavg_th_l = data_dict.get(_lavg_th_h_pv), data_dict.get(_lavg_th_l_pv)
    _lavg, _lavg_t = data_dict.get(_lavg_pv), data_dict.get(_lavg_t_pv)
    _pkavg = data_dict.get(_pkavg_pv)
    _std = data_dict.get(_std_pv)
    return irow.Device, _lavg, _pkavg, _std, _lavg_t, \
           _lavg_th_h, _lavg_h, _lavg_th_l, _lavg_l, \
           _10ms_th_h, _10ms_h, _10ms_th_l, _10ms_l, \
           _1500us_th_h, _1500us_h, _1500us_th_l, _1500us_l, \
           _150us_th_h, _150us_h, _150us_th_l, _150us_l, \
           _15us_th_h, _15us_h, _15us_th_l, _15us_l


def _get_dataframe_(dtype: str, data_dict: dict):
    # AA
    """return a dataframe for the diag snapshot from data_dict (archived data)
    """
    # with archived data
    _s = DF_MAP[dtype].apply(partial(_get_cell_value, data_dict), axis=1)
    df = pd.DataFrame.from_records(_s.to_list(), columns=COLUMNS)
    return df


def _get_dataframe(dtype: str):
    # with live data
    _s = DF_MAP[dtype].apply(_gen_data, axis=1)
    df = pd.DataFrame.from_records(_s.to_list(), columns=COLUMNS)
    return df


class MPSBeamLossDataModel(QAbstractTableModel):

    # column ids
    ColumnDevice, ColumnLongAvg, ColumnShortAvg, ColumnPeakAvg, ColumnStd, ColumnLongAvgTime, \
        ColumnLAvgThHi, ColumnLAvgThHi_E, ColumnLAvgThLo, ColumnLAvgThLo_E, \
        Column10msThHi, Column10msThHi_E, Column10msThLo, Column10msThLo_E, \
        Column1500usThHi, Column1500usThHi_E, Column1500usThLo, Column1500usThLo_E, \
        Column150usThHi, Column150usThHi_E, Column150usThLo, Column150usThLo_E, \
        Column15usThHi, Column15usThHi_E, Column15usThLo, Column15usThLo_E, \
        ColumnCount = range(27)

    # column names
    columnNameMap = {
        ColumnDevice: "Device\nName",
        ColumnLongAvg: "Long\nAverage",
        ColumnShortAvg: "Short (10 ms)\nAverage",
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

    CHK_COLUMNS = (ColumnLAvgThHi_E, Column10msThHi_E, Column1500usThHi_E,
                   Column150usThHi_E, Column15usThHi_E, ColumnLAvgThLo_E,
                   Column10msThLo_E, Column1500usThLo_E, Column150usThLo_E,
                   Column15usThLo_E)
    STR_COLUMNS = (ColumnDevice, )

    columnFormat = {
        ColumnLongAvg: "{value:.3g}{unit}",
        ColumnShortAvg: "{value:.3g}{unit}",
        ColumnPeakAvg: "{value:.3g}{unit}",
        ColumnStd: "{value:.3g}{unit}",
        ColumnLongAvgTime: "{value:.1f}s",
        ColumnLAvgThHi: "{value:.3g}{unit}",
        ColumnLAvgThLo: "{value:.3g}{unit}",
        Column10msThHi: "{value:.3g}{unit}",
        Column10msThLo: "{value:.3g}{unit}",
        Column1500usThHi: "{value:.3g}{unit}",
        Column1500usThLo: "{value:.3g}{unit}",
        Column150usThHi: "{value:.3g}{unit}",
        Column150usThLo: "{value:.3g}{unit}",
        Column15usThHi: "{value:.3g}{unit}",
        Column15usThLo: "{value:.3g}{unit}",
    }

    columnHiddenMap = {
        'ND':
        (ColumnLAvgThHi, Column10msThHi, Column1500usThHi, Column150usThHi,
         Column15usThHi, ColumnLAvgThHi_E, Column10msThHi_E,
         Column1500usThHi_E, Column150usThHi_E, Column15usThHi_E),
        'IC':
        (ColumnLAvgThHi, Column10msThHi, Column1500usThHi, Column150usThHi,
         Column15usThHi, ColumnLAvgThHi_E, Column10msThHi_E,
         Column1500usThHi_E, Column150usThHi_E, Column15usThHi_E),
        'HMR':
        (ColumnLAvgThLo, Column10msThLo, Column1500usThLo, Column150usThLo,
         Column15usThLo, ColumnLAvgThLo_E, Column10msThLo_E,
         Column1500usThLo_E, Column150usThLo_E, Column15usThLo_E),
    }

    #
    dataframeUpdated = pyqtSignal(pd.DataFrame)
    refDataframeUpdated = pyqtSignal(pd.DataFrame)
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
        self.set_ref_dataframe(None)
        #
        self.__post_init()
        # start data refreshing thread
        self.dataframeUpdated.connect(self.update_dataframe)
        self.refDataframeUpdated.connect(self.update_ref_dataframe)

        #
        # self.refresh_data()

    def __post_init(self):
        #
        pass

    def columnCount(self, parent=None):
        return self.ColumnCount

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return self._data.shape[0]

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None
        row, column = index.row(), index.column()
        v = self._data.iloc[row, column]
        v_ref = None if self._ref_data is None else self._ref_data.iloc[row,
                                                                        column]
        is_diff = v_ref is not None and not is_equal(v_ref, v)
        if role == Qt.DisplayRole and column not in MPSBeamLossDataModel.CHK_COLUMNS:
            if v != '-' and column in MPSBeamLossDataModel.columnFormat:
                _disp_val = MPSBeamLossDataModel.columnFormat[column].format(
                    value=float(v), unit=self._unit)
            else:
                _disp_val = v
            if is_diff:
                if column not in MPSBeamLossDataModel.CHK_COLUMNS:
                    v_ref_fmted = MPSBeamLossDataModel.columnFormat[
                        column].format(value=float(v_ref), unit='')
                    return f"{_disp_val}\nRef {v_ref_fmted}"
                else:
                    return _disp_val
            else:
                return _disp_val

        if role == Qt.DecorationRole:
            if column in MPSBeamLossDataModel.CHK_COLUMNS:
                if v == 1.0:
                    if is_diff:
                        return QPixmap(
                            ":/tm-icons/check-square-fill-red.png").scaled(
                                PX_SIZE, PX_SIZE, Qt.KeepAspectRatio,
                                Qt.SmoothTransformation)
                    else:
                        return QPixmap(
                            ":/tm-icons/check-square-fill.png").scaled(
                                PX_SIZE, PX_SIZE, Qt.KeepAspectRatio,
                                Qt.SmoothTransformation)
                else:  # v == 0.0
                    if is_diff:
                        return QPixmap(
                            ":/tm-icons/uncheck-square-green.png").scaled(
                                PX_SIZE, PX_SIZE, Qt.KeepAspectRatio,
                                Qt.SmoothTransformation)
                    else:
                        return QPixmap(":/tm-icons/uncheck-square.png").scaled(
                            PX_SIZE, PX_SIZE, Qt.KeepAspectRatio,
                            Qt.SmoothTransformation)

        if role == Qt.FontRole:
            if is_diff:
                if v != v_ref:
                    return FONT_DIFF
            else:
                return FONT_NO_DIFF

        if role == Qt.ForegroundRole:
            if is_diff:
                if v != v_ref:
                    return QBrush(BLACK_COLOR)
            else:
                return QBrush(DIM_COLOR)

        if role == Qt.ToolTipRole:
            if is_diff:
                if column not in MPSBeamLossDataModel.CHK_COLUMNS:
                    v_ref_fmted = MPSBeamLossDataModel.columnFormat[
                        column].format(value=float(v_ref), unit=self._unit)
                    rel_per = f" [{(v - v_ref)/abs(v_ref) * 100:+.1f}%]"
                else:
                    v_ref_fmted = "Enabled" if v_ref == 1.0 else "Disabled"
                    rel_per = ''
                if v > v_ref:
                    cname = RED_COLOR.name()
                else:
                    cname = GREEN_COLOR.name()
                return f'''<p><span style=" text-decoration: underline;">Reference value is:</span></p><p><span style=" color:{cname};">{v_ref_fmted}{rel_per}</span>.</p>'''
            else:
                return None

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

    def set_ref_dataframe(self, ref_df: pd.DataFrame):
        self._ref_data = ref_df

    def get_dataframe(self):
        return self._data

    def get_ref_dataframe(self):
        return self._ref_data

    def update_dataframe(self, df: pd.DataFrame):
        # update data
        self.layoutAboutToBeChanged.emit()
        self.set_dataframe(df)
        self.layoutChanged.emit()

    def update_ref_dataframe(self, df: pd.DataFrame):
        # update ref data
        self.layoutAboutToBeChanged.emit()
        self.set_ref_dataframe(df)
        self.layoutChanged.emit()

    def refresh_data(self):

        def _onUpdateData(i):
            # t0 = time.time()
            # update data
            self._data = _get_dataframe(self.device_type)
            self.dataframeUpdated.emit(self._data)
            # print(
            #     f"[{self.device_type}] Data Refreshed: {(time.time() - t0) * 1e3:.1f} ms"
            # )

        #
        self._th = DAQT(daq_func=_onUpdateData, daq_seq=range(1))
        self._th.daqStarted.connect(self.dataRefreshStarted)
        self._th.daqFinished.connect(self.dataRefreshStopped)
        self._th.start()

    def get_hidden_columns(self):
        return MPSBeamLossDataModel.columnHiddenMap[self.device_type]

    def highlight_diff(self, ref_df: pd.DataFrame):
        """Highlight the cells with different values by comparing with the input data.
        """

        # test
        #df = pd.read_csv('/tmp/20230412T091656_ND.csv')
        #df_bool_diff = self._data != df # dataframe of boolean of current data is diff from the loaded one
        #df_val_diff = df[df_bool_diff]  # cell values from the loaded dataframe, not NaN
        def _onUpdateData(i):
            self.refDataframeUpdated.emit(ref_df)

        #
        self._t = DAQT(daq_func=_onUpdateData, daq_seq=range(1))
        self._t.start()


class MPSBeamLossDataDelegateModel(QStyledItemDelegate):

    def __init__(self, parent=None, **kws):
        super(self.__class__, self).__init__()
        self.default_font_size = QFontDatabase.systemFont(
            QFontDatabase.FixedFont).pointSize()
        self._row_height = ROW_HEIGHT

    def setRowHeight(self, i: int):
        self._row_height = i

    def sizeHint(self, option, index):
        size = QStyledItemDelegate.sizeHint(self, option, index)
        size.setHeight(self._row_height)
        return size

    #def displayText(self, value, locale):
    #    if isinstance(value, (float, int)):
    #        return f"{value:.6f}"
    #    else:
    #        return str(value)

    def paint(self, painter, option, index):
        if index.column() in MPSBeamLossDataModel.STR_COLUMNS:
            option.displayAlignment = Qt.AlignRight | Qt.AlignVCenter
        else:
            option.displayAlignment = Qt.AlignRight | Qt.AlignVCenter
        QStyledItemDelegate.paint(self, painter, option, index)


def is_equal(a, b, decimal=6):
    if isinstance(a, str):
        return a == b

    try:
        np.testing.assert_almost_equal(a, b, decimal)
    except AssertionError:
        return False
    else:
        return True


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
