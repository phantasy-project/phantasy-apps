#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
from functools import partial
import re

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QAbstractScrollArea

from phantasy_apps.utils import printlog

try:
    basestring
except NameError:
    basestring = str

FMT = "{0:.6g}"

COLUMN_NAMES1 = ['Device', 'Field', 'Setpoint', 'Live Readback', 'Live Setpoint']
COLUMN_SFIELD_MAP = OrderedDict((
    ('Type', 'family'),
    ('Pos [m]', 'sb'),
))
COLUMN_NAMES_ATTR = list(COLUMN_SFIELD_MAP.keys())
SFIELD_NAMES_ATTR = list(COLUMN_SFIELD_MAP.values())

COLUMN_NAMES = COLUMN_NAMES1 + COLUMN_NAMES_ATTR

BG_COLOR_DEFAULT = "#FFFFFF"
COLOR_MAP = {
    # system: background
    "FE": "#e0f7fa",
    "LS1": "#ffebee",
    "FS1": "#e3f2fd",
    "LS2": "#e8f5e9",
    "FS2": "#fff3e0",
}


class SettingsModel(QStandardItemModel):
    """Settings model from Settings instance.

    Parameters
    ----------
    flat_settings : list
        List of setting with the format of ``(elem, fname, fval0)``,
        ``elem`` is CaElement object, ``fname`` is field name, ``fval0`` is
        saved field value of setpoint.
    """

    data_changed = pyqtSignal(QVariant)
    settings_sts = pyqtSignal(int, int, int)
    reset_icon = pyqtSignal()

    def __init__(self, parent, flat_settings):
        super(self.__class__, self).__init__(parent)
        self._settings = flat_settings
        self._tv = parent
        # [PV] cb PV pool
        self._pvs = []
        # [obj(PV/CaField)]: [index[list]]
        self._m_obj = [] # PV and CaField
        self._m_idx = [] # list of index(parent), [rd, sp]


        # header
        self.header = self.h_name, self.h_field, self.h_val0, self.h_rd, self.h_cset, \
                      self.h_type, self.h_pos \
            = COLUMN_NAMES
        self.ids = self.i_name, self.i_field, self.i_val0, self.i_rd, self.i_cset, \
                   self.i_type, self.i_pos \
            = range(len(self.header))

        #
        self.data_changed.connect(self.update_data)
        self.reset_icon.connect(self.reset_setdone_icons)

        self._filter_key = 'device'

    def set_filter_key(self, s):
        """set key for filtering."""
        if not s:
            self._filter_key = 'device'
        else:
            self._filter_key = s

    def get_filter_key(self):
        return self._filter_key

    def update_data(self, p):
        self.setData(*p)

    def set_data(self):

        def _cb(item_val, **kws):
                val = FMT.format(kws.get('value'))
                idx_c = item_val.index()
                self.data_changed.emit((idx_c, val, Qt.DisplayRole))

        sppv_set = set()
        rdpv_set = set()
        ename_set = set()

        for elem, fname, fld, fval0 in self._settings:
            item_ename = QStandardItem(elem.name)
            bgcolor = get_color(elem.ename)

            if fld is None:
                # debug
                # printlog("{} [{}] is invalid.".format(elem.name, fname))
                continue
            item_ename.fobj = fld
            item_ename.ftype = fld.ftype
            item_ename.setCheckable(True)

            # PVs, setpoint and readback
            for sp_obj, rd_obj in zip(fld.setpoint_pv, fld.readback_pv):
                it_sp_n = QStandardItem(sp_obj.pvname)
                it_sp_v = QStandardItem(FMT.format(sp_obj.value))
                it_rd_n = QStandardItem(rd_obj.pvname)
                it_rd_v = QStandardItem(FMT.format(rd_obj.value))

                [i.setEditable(False) for i in (it_sp_n, it_sp_v,
                                                it_rd_n, it_rd_v)]

                item_ename.appendRow((it_sp_n, QStandardItem('-'), QStandardItem('-'), QStandardItem('-'), it_sp_v))
                item_ename.appendRow((it_rd_n, QStandardItem('-'), QStandardItem('-'), it_rd_v, QStandardItem('-')))

                # cbs
                sp_obj.add_callback(partial(_cb, it_sp_v))
                rd_obj.add_callback(partial(_cb, it_rd_v))
                for o in (sp_obj, rd_obj,):
                    if o not in self._pvs:
                        self._pvs.append(o)

                for o, item in zip((sp_obj, rd_obj), (it_sp_v, it_rd_v)):
                    idx = self.indexFromItem(item)
                    if o not in self._m_obj:
                        self._m_obj.append(o)
                        self._m_idx.append([idx])
                    else:
                        self._m_idx[self._m_obj.index(o)].append(idx)

                sppv_set.add(sp_obj.pvname)
                rdpv_set.add(rd_obj.pvname)

            #
            item_fname = QStandardItem(fname)
            item_val0 = QStandardItem(FMT.format(fval0))

            item_rd = QStandardItem(FMT.format(fld.value))
            item_cset = QStandardItem(FMT.format(elem.current_setting(fname)))

            row = [item_ename, item_fname, item_val0, item_rd, item_cset, ]
            for i, f in enumerate(COLUMN_NAMES):
                if f in COLUMN_NAMES_ATTR:
                    v = getattr(elem, COLUMN_SFIELD_MAP[f])
                    if not isinstance(v, basestring):
                        v = '{0:.4f}'.format(v)
                    item = QStandardItem(v)
                    row.append(item)

            # color, readonly
            for i in row:
                i.setEditable(False)
                i.setData(QBrush(QColor(bgcolor)), Qt.BackgroundRole)
            #
            self.appendRow(row)
            ename_set.add(elem.name)

        self.settings_sts.emit(len(ename_set), len(sppv_set), len(rdpv_set))

    def set_model(self):
        # set data
        self.set_data()
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
            idx = item_name.index()
            self.data_changed.emit(
                    (self.index(idx.row(), icol),
                    FMT.format(val), Qt.DisplayRole))

        for irow in range(self.rowCount()):
            item0 = self.item(irow, self.i_name)
            fld = item0.fobj
            if fld is None:
                continue
            rd_pv0 = fld.readback_pv[0]
            sp_pv0 = fld.setpoint_pv[0]
            fld.set_auto_monitor(True, 'readback')
            fld.set_auto_monitor(True, 'setpoint')
            for (icol, pv, vtyp) in zip(
                    (self.i_rd, self.i_cset),
                    (rd_pv0, sp_pv0),
                    ('rd', 'sp')):
                pv.add_callback(partial(_cb, item0, icol, fld, vtyp))
            for o in fld.readback_pv + fld.setpoint_pv:
                if o not in self._pvs:
                    self._pvs.append(o)

            self._m_obj.append(fld)
            self._m_idx.append([self.index(irow, self.i_rd), self.index(irow, self.i_cset)])

    def __post_init_ui(self, tv):
        # set headers
        for i, s in zip(self.ids, self.header):
            self.setHeaderData(i, Qt.Horizontal, s)

        # view properties
        tv.setStyleSheet("font-family: monospace;")
        tv.setAlternatingRowColors(True)
        tv.expandAll()
        for i in self.ids:
            tv.resizeColumnToContents(i)
        tv.setSortingEnabled(True)
        tv.model().sort(self.i_pos)
        tv.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        tv.collapseAll()

    def reset_setdone_icons(self):
        # reset set done icons.
        for i in range(self.rowCount()):
            self.setData(self.index(i, self.i_name), QIcon(), Qt.DecorationRole)


class _SortProxyModel(QSortFilterProxyModel):

    def __init__(self, model):
        super(self.__class__, self).__init__()
        self.m_src = model
        self.setSourceModel(model)
        self.filter_col_index = {
            'device': model.i_name,
            'field': model.i_field,
            'pos': model.i_pos,
            'setpoint': model.i_val0,
            'live_readback': model.i_rd,
            'live_setpoint': model.i_cset,
            'type': model.i_type}
        self.filter_ftypes = ['ENG', 'PHY']

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
        return r

    def filterAcceptsRow(self, src_row, src_parent):
        if src_parent.isValid():
            return True

        src_model = self.sourceModel()
        filter_key = src_model.get_filter_key()
        ftype = src_model.item(src_row, 0).ftype

        idx = self.filter_col_index[filter_key]
        src_index = src_model.index(src_row, idx)
        var = src_index.data(Qt.DisplayRole)
        return ftype in self.filter_ftypes and \
                re.match(self.filterRegExp().pattern(), var) is not None

    def get_selection(self):
        # Return a list of selected items, [(idx_src, settings)].
        settings_selected = []
        for i in range(self.rowCount()):
            idx = self.index(i, self.m_src.i_name)
            idx_src = self.mapToSource(idx)
            it_name_src = self.m_src.itemFromIndex(idx_src)
            if is_item_checked(it_name_src):
                print(self.data(idx), it_name_src.text(), idx_src.row())
                settings_selected.append((idx_src, self.m_src._settings[idx_src.row()]))
        return settings_selected

    def select_all(self):
        for i in range(self.rowCount()):
            idx = self.index(i, self.m_src.i_name)
            idx_src = self.mapToSource(idx)
            it_name_src = self.m_src.itemFromIndex(idx_src)
            it_name_src.setCheckState(Qt.Checked)

    def invert_selection(self):
        for i in range(self.rowCount()):
            idx = self.index(i, self.m_src.i_name)
            idx_src = self.mapToSource(idx)
            it_name_src = self.m_src.itemFromIndex(idx_src)
            if not is_item_checked(it_name_src):
                it_name_src.setCheckState(Qt.Checked)
            else:
                it_name_src.setCheckState(Qt.Unchecked)


def convert_settings(settings_read, elem_list):
    """Convert settings to flat, each tuple is composed of (CaElement,
    field name, CaField, field value)
    """
    flat_settings = []
    nm = {o.name: o for o in elem_list}
    for ename, econf in settings_read.items():
        elem = nm.get(ename, None)
        if elem is None:
            print("{} is not in lattice but defined in the settings.".format(ename))
            continue
        for fname, fval0 in econf.items():
            confline = (elem, fname, elem.get_field(fname), fval0)
            flat_settings.append(confline)
    return flat_settings


def pack_lattice_settings(lat, elem_list=None, **kws):
    """Pack up element settings of lattice object as a tuple to return.

    Parameters
    ----------
    elem_list : list
        List of CaElement, if not defined, use the whole lattice.

    Keyword Arguments
    -----------------
    data_source : str
        'model' or 'control', get element settings from MODEL environment if
        *data_source* is 'model', otherwise get live settings from controls
        network.
    only_physics : bool
        If True, onle get physics settings, other wise, get engineering
        settings as well.

    Returns
    -------
    t : tuple
        Tuple of (flat_s[list], s[Settings]), element of flat_s:
        (CaElement, field_name, CaField, field_value)
    """
    elems = lat if elem_list is None else elem_list
    settings = lat.get_settings_from_element_list(elems, **kws)
    flat_settings = convert_settings(settings, elems)
    return flat_settings, settings


def is_item_checked(item):
    return item.checkState() == Qt.Checked


def get_color(name):
    """Return background color based on naming rule.
    """
    a, _ = name.split('_', 1)
    if ':' in a:
        system = a.split(':')[1]
    else:
        system = a
    return COLOR_MAP.get(system, BG_COLOR_DEFAULT)

