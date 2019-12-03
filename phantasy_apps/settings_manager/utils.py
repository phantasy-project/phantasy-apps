#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
from functools import partial
import re

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSortFilterProxyModel
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
))
COLUMN_NAMES_ATTR = list(COLUMN_SFIELD_MAP.keys())
SFIELD_NAMES_ATTR = list(COLUMN_SFIELD_MAP.values())

COLUMN_NAMES = COLUMN_NAMES1 + COLUMN_NAMES_ATTR


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
        self.header = self.h_name, self.h_field, self.h_val0, self.h_rd, self.h_cset, \
                      self.h_type, self.h_pos, self.h_len \
            = COLUMN_NAMES
        self.ids = self.i_name, self.i_field, self.i_val0, self.i_rd, self.i_cset, \
                   self.i_type, self.i_pos, self.i_len \
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
        ii = 1
        root_pt = self.invisibleRootItem()
        for elem, fname, fval0 in self._settings:
            item_ename = QStandardItem(elem.name)

            # debug
            print('{0}:{1}[{2}]'.format(ii, elem.name, fname))
            #

            fld = elem.get_field(fname)
            item_ename.fobj = fld
            if fld is None:
                print("{} [{}] is invalid.".format(elem.name, fname))
                continue

            # PVs, setpoint and readback
            for sp_obj, rd_obj in zip(fld.setpoint_pv, fld.readback_pv):
                it_sp_n = QStandardItem(sp_obj.pvname)
                it_sp_v = QStandardItem(FMT.format(sp_obj.value))
                it_rd_n = QStandardItem(rd_obj.pvname)
                it_rd_v = QStandardItem(FMT.format(rd_obj.value))

                item_ename.appendRow((it_sp_n, it_sp_v))
                item_ename.appendRow((it_rd_n, it_rd_v))

            #


            item_fname = QStandardItem(fname)
            item_val0 = QStandardItem(FMT.format(fval0))

            item_rd = QStandardItem(FMT.format(fld.value))
            # item_rd = QStandardItem('Current Readback')

            item_cset = QStandardItem(FMT.format(elem.current_setting(fname)))
            # item_cset = QStandardItem('Current Setpoint')

            row = [item_ename, item_fname, item_val0, item_rd, item_cset, ]
            for i, f in enumerate(COLUMN_NAMES):
                if f in COLUMN_NAMES_ATTR:
                    v = getattr(elem, COLUMN_SFIELD_MAP[f])
                    if not isinstance(v, basestring):
                        v = '{0:.4f}'.format(v)
                    item = QStandardItem(v)
                    row.append(item)
            self.appendRow(row)
            ii += 1

    def set_model(self):
        # set model, set field column
        proxy_model = _SortProxyModel(self)
        self._tv.setModel(proxy_model)
        #
        self.set_cbs()
        self.__post_init_ui(self._tv)

    def set_cbs(self):
        def _cb(item_name, icol, fld, vtyp, **kws):
            if vtyp == 'rd':
                val = fld.value
            else:
                val = fld.current_setting()
            item = QStandardItem(FMT.format(val))
            idx = item_name.index()
            self.item_changed.emit((idx.row(), icol, item))

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
                pv.add_callback(partial(_cb, item0, icol, fld, vtyp))
                self._pvs.append(pv)

    def __post_init_ui(self, tv):
        # view properties
        tv.setStyleSheet("font-family: monospace;")
        tv.setAlternatingRowColors(True)
        for i in self.ids:
            tv.resizeColumnToContents(i)
        tv.setSortingEnabled(True)
        self.sort(self.i_pos, Qt.AscendingOrder)
        tv.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # tv.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # tv.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


class _SortProxyModel(QSortFilterProxyModel):

    def __init__(self, model):
        super(self.__class__, self).__init__()
        self.setSourceModel(model)

    def lessThan(self, left, right):
        left_data = left.data(Qt.DisplayRole)
        right_data = right.data(Qt.DisplayRole)

        if left_data is None or right_data is None:
            return True

        try:
            r = float(left_data) < float(right_data)
        except ValueError:
            if left.column() == 0:  # ename
                r_left = re.match(r'.*_(D[0-9]{4}).*', left_data)
                r_right = re.match(r'.*_(D[0-9]{4}).*', right_data)
                if r_left is not None and r_right is not None:
                    left_data = r_left.group(1)
                    right_data = r_right.group(1)
            r = left_data < right_data

        return not r

