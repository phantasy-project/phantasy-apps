#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from collections import OrderedDict
from functools import partial

from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QAbstractScrollArea
from PyQt5.QtWidgets import QHeaderView
from phantasy_ui.widgets import is_item_checked

from phantasy import CaElement
from phantasy import PVElement

FMT = "{0:.6g}"

X0 = 'x\N{SUBSCRIPT ZERO}'
X1 = 'x\N{SUBSCRIPT ONE}'
X2 = 'x\N{SUBSCRIPT TWO}'
DELTA = '\N{GREEK CAPITAL LETTER DELTA}'

COLUMN_NAMES1 = ['Device', 'Field', 'Setpoint({})'.format(X0),
                 'Live Readback({})'.format(X1),
                 'Live Setpoint({})'.format(X2)]
COLUMN_NAMES2 = ['{D}({x0}-{x1})'.format(D=DELTA, x0=X0, x1=X1),
                 '{D}({x0}-{x2})'.format(D=DELTA, x0=X0, x2=X2),
                 '{D}({x1}-{x2})'.format(D=DELTA, x1=X1, x2=X2),
                 'Tolerance', 'Writable']
COLUMN_SFIELD_MAP = OrderedDict((
    ('Type', 'family'),
    ('Pos [m]', 'sb'),
))
COLUMN_NAMES_ATTR = list(COLUMN_SFIELD_MAP.keys())
SFIELD_NAMES_ATTR = list(COLUMN_SFIELD_MAP.values())

COLUMN_NAMES = COLUMN_NAMES1 + COLUMN_NAMES_ATTR + COLUMN_NAMES2

VALID_FILTER_KEYS = ('device', 'field', 'pos', 'type',
                     'x0', 'x1', 'x2', 'dx01', 'dx02', 'dx12')

BG_COLOR_DEFAULT = "#FFFFFF"
BG_COLOR_MAP = {
    # system: background
    "FE": "#e0f7fa",
    "LS1": "#ffebee",
    "FS1": "#e3f2fd",
    "LS2": "#e8f5e9",
    "FS2": "#fff3e0",
}

FG_COLOR_MAP = {
    # writable or not
    True: "#343A40",
    False: "#6C757D",
}


class SettingsModel(QStandardItemModel):
    """Settings model from Settings instance.

    Parameters
    ----------
    flat_settings : list
        List of setting with the format of ``(elem, fname, field, fval0)``,
        ``elem`` is CaElement object, ``fname`` is field name, ``field`` is
        CaField object, ``fval0`` is saved field value of setpoint.
    """

    data_changed = pyqtSignal(QVariant)
    settings_sts = pyqtSignal(int, int, int)
    reset_icon = pyqtSignal()
    delete_selected_items = pyqtSignal()

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
                      self.h_type, self.h_pos, self.h_val0_rd, self.h_val0_cset, self.h_rd_cset, \
                      self.h_tol, self.h_writable \
            = COLUMN_NAMES
        self.ids = self.i_name, self.i_field, self.i_val0, self.i_rd, self.i_cset, \
                   self.i_type, self.i_pos, self.i_val0_rd, self.i_val0_cset, self.i_rd_cset, \
                   self.i_tol, self.i_writable \
            = range(len(self.header))

        #
        self.data_changed.connect(self.update_data)
        self.reset_icon.connect(self.reset_setdone_icons)
        self.delete_selected_items.connect(self.on_delete_selected_items)

        self._filter_key = 'device'

    def set_filter_key(self, s):
        """set key for filtering."""
        if s not in VALID_FILTER_KEYS:
            self._filter_key = 'device'
        else:
            self._filter_key = s

    def get_filter_key(self):
        return self._filter_key.lower()

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
            bgcolor = get_bg_color(elem.ename)

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
                    if not isinstance(v, str):
                        v = '{0:.4f}'.format(v)
                    item = QStandardItem(v)
                    row.append(item)
            # dx01,02,12
            v_d01 = float(item_val0.text()) - float(item_rd.text())
            v_d02 = float(item_val0.text()) - float(item_cset.text())
            v_d12 = float(item_rd.text()) - float(item_cset.text())
            for v in (v_d01, v_d02, v_d12):
                item = QStandardItem(FMT.format(v))
                row.append(item)

            # editable
            for i in row:
                i.setEditable(False)

            # tolerance for dx12
            tol = fld.tolerance
            item_tol = QStandardItem(FMT.format(tol))
            row.append(item_tol)

            # writable
            write_access = fld.write_access
            item_wa = QStandardItem(str(write_access))
            item_wa.setEditable(False)
            row.append(item_wa)
            fgcolor = get_fg_color(write_access)

            # color
            for i in row:
                i.setData(QBrush(QColor(bgcolor)), Qt.BackgroundRole)
                i.setData(QBrush(QColor(fgcolor)), Qt.ForegroundRole)

            self.appendRow(row)
            ename_set.add(elem.name)

        self.settings_sts.emit(len(ename_set), len(sppv_set), len(rdpv_set))

    def set_model(self):
        # set data
        self.set_data()
        # set model
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
            self._m_idx.append(
                [self.index(irow, self.i_rd),
                 self.index(irow, self.i_cset),])
                 # self.index(irow, self.i_val0_rd),    # x0-x1
                 # self.index(irow, self.i_val0_cset),  # x0-x2
                 # self.index(irow, self.i_rd_cset)])   # x1-x2

    def __post_init_ui(self, tv):
        # set headers
        for i, s in zip(self.ids, self.header):
            self.setHeaderData(i, Qt.Horizontal, s)

        # view properties
        tv.setStyleSheet("font-family: monospace;")
        tv.expandAll()
        for i in self.ids:
            tv.resizeColumnToContents(i)
        tv.setSortingEnabled(True)
        tv.model().sort(self.i_pos)
        tv.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        tv.collapseAll()

    @pyqtSlot()
    def reset_setdone_icons(self):
        # reset set done icons.
        for i in range(self.rowCount()):
            self.setData(self.index(i, self.i_name), QIcon(), Qt.DecorationRole)

    @pyqtSlot()
    def on_delete_selected_items(self):
        # delete selected items ?
        checked_items = []
        for i in range(self.rowCount()):
            idx = self.index(i, self.i_name)
            it_name = self.itemFromIndex(idx)
            if is_item_checked(it_name):
                checked_items.append(it_name)

        for item in checked_items:
            idx = self.indexFromItem(item)
            irow = idx.row()
            name = item.text()
            self.removeRow(irow)
            #print("Delete {} at {}".format(name, irow))


class _SortProxyModel(QSortFilterProxyModel):

    def __init__(self, model):
        super(self.__class__, self).__init__()
        self.m_src = model
        self.setSourceModel(model)
        self.filter_col_index = {
            'device': model.i_name,
            'field': model.i_field,
            'pos': model.i_pos,
            'type': model.i_type,
            'x0': model.i_val0,
            'x1': model.i_rd,
            'x2': model.i_cset,
            'dx01': model.i_val0_rd,
            'dx02': model.i_val0_cset,
            'dx12': model.i_rd_cset,
        }
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
        if not isinstance(var, str):
            var = FMT.format(var)
        # Qt >= 5.12
        # regex = self.filterRegularExpression()
        # return ftype in self.filter_ftypes and regex.match(var).hasMatch()

        # wildcardunix
        #regex = self.filterRegExp()
        #return ftype in self.filter_ftypes and regex.exactMatch(var)

        #
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
    """Convert hierarchical `Settings` to flat list of tuples as the return,
    each tuple is composed of (CaElement, field name, CaField, field value).
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
    lat :
        Lattice object.
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


def get_bg_color(name):
    """Return background color based on naming rule.
    """
    a, _ = name.split('_', 1)
    if ':' in a:
        system = a.split(':')[1]
    else:
        system = a
    return BG_COLOR_MAP.get(system, BG_COLOR_DEFAULT)


def get_fg_color(writable):
    return FG_COLOR_MAP.get(writable)


def build_element(sp_pv, rd_pv, ename=None, fname=None):
    """Build high-level element from setpoint and readback PV names.

    Parameters
    ----------
    sp_pv : str
        Setpoint PV name.
    rd_pv : str
        Readback PV name.
    ename : str
        Element name.
    fname : str
        Field name.

    Returns
    -------
    elem : CaElement
        CaElement object.
    """
    pv_elem = PVElement(sp_pv, rd_pv)
    if ename is None:
        ename = pv_elem.ename
    if fname is None:
        fname = pv_elem.fname
    elem = CaElement(name=ename)
    pv_props = {'field_eng': fname, 'field_phy': '{}_phy'.format(fname),
            'handle': 'readback', 'pv_policy': 'DEFAULT', 'index': '-1',
            'length': '0.0', 'sb': -1, 'family': 'PV'}
    pv_tags = []
    for pv, handle in zip((sp_pv, rd_pv), ('setpoint', 'readback')):
        pv_props['handle'] = handle
        elem.process_pv(pv, pv_props, pv_tags)
    return elem
