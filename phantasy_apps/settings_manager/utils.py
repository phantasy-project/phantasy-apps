#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QAbstractScrollArea

try:
    basestring
except NameError:
    basestring = str

FMT = "{0:.6g}"

COLUMN_NAMES1 = ['Device', 'Field', 'Setpoint', 'Live Readback', 'Live Setpoint']
COLUMN_SFIELD_MAP = OrderedDict((
    ('Type', 'family'),
    ('Pos [m]', 'sb'),
    ('Length [m]', 'length'),
    ('Index', 'index'),
))
COLUMN_NAMES_ATTR = list(COLUMN_SFIELD_MAP.keys())
SFIELD_NAMES_ATTR = list(COLUMN_SFIELD_MAP.values())

COLUMN_NAMES = [''] + COLUMN_NAMES1 + COLUMN_NAMES_ATTR


class SettingsModel(QStandardItemModel):
    """Settings model from Settings instance.

    Parameters
    ----------
    flat_settings : list
        List of setting with the format of ``(elem, fname, fval0)``,
        ``elem`` is CaElement object, ``fname`` is field name, ``fval0`` is
        saved field value of setpoint.
    """

    item_changed = pyqtSignal(QVariant)

    def __init__(self, parent, flat_settings):
        super(self.__class__, self).__init__(parent)
        self._settings = flat_settings
        self._tv = parent
        #
        self._pvs = []

        # header
        self.header = self.h_id, self.h_name, self.h_field, self.h_val0, self.h_rd, self.h_cset, \
                      self.h_type, self.h_pos, self.h_len, self.h_index \
            = COLUMN_NAMES
        self.ids = self.i_id, self.i_name, self.i_field, self.i_val0, self.i_rd, self.i_cset, \
                   self.i_type, self.i_pos, self.i_len, self.i_index \
            = range(len(self.header))

        # set data (pure)
        self.set_data()

        # set headers
        for i, s in zip(self.ids, self.header):
            self.setHeaderData(i, Qt.Horizontal, s)

        #
        self.item_changed.connect(self.update_item)

    def update_item(self, p):
        self.setItem(*p)

    def set_data(self):
        for ii, (elem, fname, fval0) in enumerate(self._settings, 1):
            item_ename = QStandardItem(elem.name)

            # debug
            print('{0:02d}:{1}[{2}]'.format(ii, elem.name, fname))
            #
            fld = elem.get_field(fname)
            item_ename.fobj = fld
            if fld is None:
                print("{} [{}] is invalid.".format(elem.name, fname))
                continue

            item_fname = QStandardItem(fname)
            item_val0 = QStandardItem(FMT.format(fval0))
            # item_rd = QStandardItem(FMT.format(fld.value))
            item_rd = QStandardItem('Current Readback')
            # item_cset = QStandardItem(FMT.format(elem.current_setting(fname)))
            item_cset = QStandardItem('Current Setpoint')
            row = [QStandardItem('{0:03d}'.format(ii)), item_ename, item_fname, item_val0, item_rd, item_cset, ]
            for i, f in enumerate(COLUMN_NAMES):
                if f in COLUMN_NAMES_ATTR:
                    v = getattr(elem, COLUMN_SFIELD_MAP[f])
                    if i == self.i_index:
                        v = '{0:04d}'.format(v)
                    if not isinstance(v, basestring):
                        v = '{0:.4f}'.format(v)
                    item = QStandardItem(v)
                    row.append(item)
            self.appendRow(row)

    def set_model(self):
        # set model, set field column
        self._tv.setModel(self)
        #
        # self.set_cbs()
        self.__post_init_ui(self._tv)

    def set_cbs(self):
        def _cb(row, col, fld, vtyp, **kws):
            if vtyp == 'rd':
                val = fld.value
            else:
                val = fld.current_setting()
            item = QStandardItem(FMT.format(val))
            self.item_changed.emit((row, col, item))

        for irow in range(self.rowCount()):
            item0 = self.item(irow, self.i_name)
            fld = item0.fobj
            if fld is None:
                continue
            rd_pv0 = fld.readback_pv[0]
            sp_pv0 = fld.setpoint_pv[0]
            for (icol, pv, vtyp) in zip(
                    (self.i_rd, self.i_cset),
                    (rd_pv0, sp_pv0),
                    ('rd', 'sp')):
                pv.add_callback(partial(_cb, irow, icol, fld, vtyp))
                self._pvs.append(pv)

    def __post_init_ui(self, tv):
        # view properties
        tv.setStyleSheet("font-family: monospace;")
        tv.setAlternatingRowColors(True)
        for i in self.ids:
            tv.resizeColumnToContents(i)
        tv.setSortingEnabled(True)
        self.sort(self.i_index, Qt.AscendingOrder)
        tv.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # tv.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # tv.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
