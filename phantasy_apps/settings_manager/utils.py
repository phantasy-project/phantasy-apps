#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import toml
import os
import re
import time
import shutil
from collections import Counter
from collections import OrderedDict
from datetime import datetime
from epics import get_pv
from fnmatch import translate
from functools import partial
from numpy.testing import assert_almost_equal

from PyQt5.QtCore import QObject
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtCore import QPersistentModelIndex
from PyQt5.QtCore import QItemSelectionModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSizePolicy
from phantasy import get_settings_from_element_list
from phantasy_ui.widgets import is_item_checked
from phantasy_apps.utils import find_dconf
from .data import SnapshotData

AVAILABLE_IONS = ('He', 'Ne', 'Ar', 'Kr', 'Xe', 'U', 'Se', 'Ca', 'Pb',
                  'O', 'Bi', 'Zn', 'Tm', 'Pt')

FMT = "{0:.6g}"

X0 = 'x\N{SUBSCRIPT ZERO}'
X1 = 'x\N{SUBSCRIPT ONE}'
X2 = 'x\N{SUBSCRIPT TWO}'
XREF = 'xref'
DELTA = '\N{GREEK CAPITAL LETTER DELTA}'

COLUMN_NAMES1 = ['Device', 'Field']

COLUMN_NAMES2 = [
    f'Setpoint({X0})',
    f'Live Readback({X1})',
    f'Live Setpoint({X2})',
    f'{DELTA}({X0},{X1})',
#    f'{DELTA}({X0},{X2})',
    f'{DELTA}({X2},{X0})',
    f'{DELTA}({X1},{X2})',
    'Tolerance', 'Writable', f'{X2}/{X0}',
    'Live State',
    'State',
    f'Reference Set ({XREF})',
    f'{DELTA}({X2},{XREF})',
    f'{DELTA}({X0},{XREF})',
    f'Tune ALM?',  # if tune alarm is activated?
    f'Read ALM?',  # if read alarm is activated?
]
COLUMN_SFIELD_MAP = OrderedDict((
    ('Type', 'family'),
    ('Pos [m]', 'sb'),
))
COLUMN_NAMES_ATTR = list(COLUMN_SFIELD_MAP.keys())
SFIELD_NAMES_ATTR = list(COLUMN_SFIELD_MAP.values())

COLUMN_NAMES = COLUMN_NAMES1 + COLUMN_NAMES_ATTR + COLUMN_NAMES2

VALID_FILTER_KEYS_NUM = ['x0', 'x1', 'x2', 'dx01', 'dx02', 'dx12',
                         'pos', 'tolerance', 'x2/x0']
VALID_FILTER_KEYS = ['device', 'field', 'type',
                     'writable', 'state', 'last_state'] + VALID_FILTER_KEYS_NUM

BG_COLOR_GOLDEN_YES = (255, 222, 3, 200) # #FFDE03
BG_COLOR_GOLDEN_NO = (255, 255, 255, 0) # #FFFFFF
BG_COLOR_DEFAULT = "#FFFFFF"
BG_COLOR_MAP = {
    # system: background
    "FE": "#e0f7fa",
    "LS1": "#ffebee",
    "FS1": "#e3f2fd",
    "LS2": "#e8f5e9",
    "FS2": "#fff3e0",
}

FG_NO_WRITE = "#6C757D"
FG_COLOR_MAP = {
    # writable or not
    True: "#343A40",
    False: FG_NO_WRITE,
}

TT_LOADED = "loaded"
TT_NOT_LOADED= "not-loaded"
TT_GOLDEN = "Golden Setting!"
TT_NOT_GOLDEN = "Light up if 'golden' in tags!"

PX_SIZE = 24
ACT_BTN_CONF = {}

ELEMT_PX_MAP = {i: [f':/elements/elements/{i}{s}.png' for s in ('', '-off')]
                for i in AVAILABLE_IONS}

DEFAULT_TS_PATH = find_dconf("settings_manager", "tolerance.json")
DEFAULT_MS_PATH = find_dconf("settings_manager", "settings.json")
DEFAULT_ELEM_PATH = find_dconf("settings_manager", "elements.json")

TBTN_STY_COLOR_TUPLE = ('#EEEEEC', '#F7F7F7', '#90B5F0', '#6EA1F1', '#E7EFFD', '#CBDAF1')
TBTN_STY_COLOR_TUPLE_GOLDEN = ('#FFF7B3', '#F5E345', '#FFCD03', '#FFC503', '#FAED11', '#FAE111')
TBTN_STY_BASE = """
QToolButton {{
    border: 1px solid #2E3436;
    border-radius: 4px;
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {c[0]}, stop: 1 {c[1]});
}}
QToolButton:pressed {{
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {c[2]}, stop: 1 {c[3]});
}}
QToolButton:hover {{
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {c[4]}, stop: 1 {c[5]});
    border: 2px solid #2E3436;
}}
QToolButton:checked {{
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {c[2]}, stop: 1 {c[3]});
}}"""
TBTN_STY_GOLDEN = TBTN_STY_BASE.format(c=TBTN_STY_COLOR_TUPLE_GOLDEN)
TBTN_STY_REGULAR = TBTN_STY_BASE.format(c=TBTN_STY_COLOR_TUPLE)

DEFAULT_X12_TOL = 0.15

TAG_BTN_STY = """
QToolButton {{
    font-size: {fs}pt;
    padding: 3px 3px 3px 3px;
    background-color: rgb(255, 133, 170);
    border: none;
    border-radius: 6px;
    color: rgb(255, 255, 255);
    qproperty-icon: url(":/sm-icons/plus-white.png") off, url(":/sm-icons/checkmark-white.png") on;
}}
QToolButton:hover {{
    background-color: rgb(255, 158, 195);
}}
QToolButton:checked {{
    background-color: rgb(0, 123, 255);
}}
"""

TAG_BTN_STY1 = """
QToolButton {{
    font-size: {fs}pt;
    border-radius: 6px;
    padding: 3px 3px 3px 3px;
    color: rgb(18, 18, 18);
    border-top: 2px solid rgb(139, 139, 139);
    border-left: 2px solid rgb(139, 139, 139);
    border-right: 2px solid rgb(139, 139, 139);
    border-bottom: 2px solid rgb(139, 139, 139);
    qproperty-icon: url("none") off, url(":/sm-icons/checkmark-blue.png") on;
}}
QToolButton:hover {{
    background-color: rgb(224, 238, 255);
}}
QToolButton:checked {{
    color: rgb(45, 91, 227);
    border-top: 2px solid rgb(50, 105, 255);
    border-left: 2px solid rgb(50, 105, 255);
    border-right: 2px solid rgb(50, 105, 255);
    border-bottom: 2px solid rgb(50, 105, 255);
}}
"""


def get_foi_dict(filepath):
    """Return a dict of field of interest per element type.
    """
    conf = toml.load(filepath)
    return {k: v['fields'] for k, v in conf.items()}

DEFAULT_FOI_PATH = find_dconf("settings_manager", "fields.toml")
DEFAULT_FOI_DICT = get_foi_dict(DEFAULT_FOI_PATH)

# override write permission (for those does not have correct ACF)
ELEM_WRITE_PERM = {
 'FE_ISRC1:BEAM': False,
 'FE_ISRC2:BEAM': False,
 'FE_RFQ:CAV_D1005': False,
 'FE_ISRC1:DRV_D0686:POS': False,
 'FE_ISRC1:DRV_D0686': False,
 'FS1_CSS:STRIP_D2249': False,
 'FE_LEBT:BEAM': False,
 'FE_LEBT:ATT_D0957-1': False,
 'FE_LEBT:ATT_D0957-2': False,
 'FE_LEBT:ATT_D0974-1': False,
 'FE_LEBT:ATT_D0974-2': False,
 'FE_LEBT:AP_D0796': False,
 'FE_LEBT:AP_D0807': False,
}

# default length for number display
NUM_LENGTH = 9


# Chopper state map
# CHP_STS_TUPLE = PV("ACS_DIAG:CHP:STATE_RD").enum_strs
CHP_STS_TUPLE = ("Invalid Input", "Off", "Blocking", "Running")

# Target state map
# TGT_STS_TUPLE = PV("FS_PTG:BEAM:TARGET").enum_strs
TGT_STS_TUPLE = ('Invalid', 'Home/Be 3.811 mm', 'Viewer', 'Be 4064 mm',
                 'Pattern-11 holes', 'Be 8.892 mm', 'Be 3.811 mm',
                 'Empty hole', 'Be 4.189 mm', 'Pattern- 1 center hole',
                 'Be 8.892 mm')


class SettingsModel(QStandardItemModel):
    """Settings model from Settings instance.

    Parameters
    ----------
    flat_settings : list
        List of setting with the format of ``(elem, fname, field, fval0)``,
        ``elem`` is CaElement object, ``fname`` is field name, ``field`` is
        CaField object, ``fval0`` is saved field value of setpoint.
    """

    # data changed, e.g. field/PV value is updated
    data_changed = pyqtSignal(QVariant)

    # statistics for loaded items (element name and CaField count)
    settings_sts = pyqtSignal(int, int)

    # delete checked items
    delete_selected_items = pyqtSignal()

    # delete checked items from original element list,
    # signal list of CaField objects.
    item_deletion_updated = pyqtSignal(list)

    # number of checked items is changed
    checked_items_inc_dec_updated = pyqtSignal(int)

    def __init__(self, parent, flat_settings, **kws):
        # kw: ndigit, font, auto_fmt, device_states
        # pv_map: dict of additional pv data
        super(self.__class__, self).__init__(parent)
        self._ndigit = kws.get('ndigit', 6)
        self._font = kws.get('font', None)
        self._auto_fmt = kws.get('auto_fmt', False)
        self._last_sts_dict = kws.get('device_states', {})
        self._pv_map = kws.get('pv_map', {})
        self.ref_st_pv_map = self._pv_map.get('refset', {})
        self.tol_pv_map = self._pv_map.get('tol', {})
        self.alm_act_pv_map = self._pv_map.get('almact', {})

        if self._auto_fmt:
            self.fmt = '{{0:{0}g}}'.format(self._ndigit)
        else:
            self.fmt = '{{0:>{0}.{1}f}}'.format(NUM_LENGTH, self._ndigit)

        # for field NMR, HALL
        self.fmt_nmr = '{{0:>{0}.{1}f}}'.format(NUM_LENGTH, 5)

        if self._font is None:
            self._font = QFontDatabase.systemFont(QFontDatabase.FixedFont)

        self._settings = flat_settings
        self._tv = parent
        # [obj(CaField)] --> [items]
        self._fld_obj = []  # CaField
        self._fld_it = []   # list of items, [rd/sp]

        # header
        self.header = self.h_name, self.h_field, self.h_type, self.h_pos, \
                      self.h_val0, self.h_rd, self.h_cset, \
                      self.h_val0_rd, self.h_val0_cset, self.h_rd_cset, \
                      self.h_tol, self.h_writable, self.h_ratio_x20, \
                      self.h_sts, self.h_last_sts, \
                      self.h_ref_st, self.h_dsetref, self.h_dval0ref, \
                      self.h_tune_alm, self.h_read_alm \
            = COLUMN_NAMES
        self.ids = self.i_name, self.i_field, self.i_type, self.i_pos, \
                   self.i_val0, self.i_rd, self.i_cset, \
                   self.i_val0_rd, self.i_val0_cset, self.i_rd_cset, \
                   self.i_tol, self.i_writable, self.i_ratio_x20, \
                   self.i_sts, self.i_last_sts, \
                   self.i_ref_st, self.i_dstref, self.i_dval0ref, \
                   self.i_tune_alm, self.i_read_alm \
            = range(len(self.header))

        #
        self.data_changed.connect(self.update_data)
        self.delete_selected_items.connect(self.on_delete_selected_items)
        #
        self.itemChanged.connect(self.on_item_changed)

    def on_item_changed(self, item):
        idx = item.index()
        if not idx.column() == self.i_name:
            return
        it = self.itemFromIndex(idx)
        last_checkstate = it.data(Qt.UserRole + 2)
        current_checkstate = it.checkState()
        if current_checkstate != last_checkstate:
            if current_checkstate == Qt.Checked:
                n_inc = 1
            else:
                n_inc = -1
            it.setData(current_checkstate, Qt.UserRole + 2)
            self.checked_items_inc_dec_updated.emit(n_inc)

    def update_data(self, p):
        self.setData(*p)

        # write access column only
        i, j = p[0].row(), p[0].column()
        if j == self.i_writable:
            if p[1] == 'None':
                wa = False
            else:
                wa = p[1] == 'True'
            # disable/enable name item.
            self.item(i, 0).setEnabled(wa)
            #
            for j in self.ids:
                it = self.item(i, j)
                it.setSelectable(wa)
                it.setData(QBrush(QColor(FG_COLOR_MAP[wa])), Qt.ForegroundRole)
            #

    def set_data(self):
        field_cnt = 0
        ename_set = set()

        for elem, fname, fld, fval0 in self._settings:
            # add an exception for number format
            if fname in ('NMR', 'NMR_phy', 'HALL', 'HALL_PROBE'):
                fmt = self.fmt_nmr
            else:
                fmt = self.fmt
            #
            ename = elem.name
            item_ename = QStandardItem(ename)
            item_ename.setData(elem.sb, Qt.UserRole + 1)

            if fld is None:
                continue
            item_ename.fobj = fld
            item_ename.ftype = fld.ftype
            item_ename.setCheckable(True)
            item_ename.setData(Qt.Unchecked, Qt.UserRole + 2) # last checkstate

            #
            item_fname = QStandardItem(fname)
            if fval0 is None:
                item_val0 = QStandardItem('-')
            else:
                item_val0 = QStandardItem(fmt.format(fval0))
            item_rd = QStandardItem('-')
            item_cset = QStandardItem('-')

            self._fld_obj.append(fld)
            self._fld_it.append([item_rd, item_cset])

            row = [item_ename, item_fname]
            for _, f in zip(COLUMN_NAMES_ATTR, SFIELD_NAMES_ATTR):
                v = getattr(elem, f)
                if not isinstance(v, str):
                    v = '{0:.4f}'.format(v)
                item = QStandardItem(v)
                row.append(item)

            #
            row.extend([item_val0, item_rd, item_cset,
                        QStandardItem('-'), QStandardItem('-'), QStandardItem('-')])
            [i.setEditable(False) for i in row]

            # tolerance for dx12
            # tol is read from _TOL PV
            item_tol = QStandardItem(fmt.format(DEFAULT_X12_TOL))
            item_tol.setData(self.get_tol_pv(fld.ename, fld.name), Qt.UserRole + 1) # None if not support
            item_tol.setEditable(False)
            row.append(item_tol)

            # writable
            write_access = ELEM_WRITE_PERM.get(fld.ename, fld.write_access)
            item_wa = QStandardItem(str(write_access))
            item_wa.setEditable(False)
            row.append(item_wa)
            # item_ename.setEnabled(write_access)

            # x2/x0
            item_ratio_x20 = QStandardItem('-')
            item_ratio_x20.setEditable(False)
            row.append(item_ratio_x20)

            # current device state
            item_sts = QStandardItem('')
            row.append(item_sts)

            # last device state
            item_last_sts = set_device_state_item(self._last_sts_dict.get(f"{ename}-{fname}", 'nan'))
            row.append(item_last_sts)

            #
            # reference value, xref
            item_ref_st = QStandardItem('-')
            item_ref_st.setData(self.get_ref_pv(fld.ename, fld.name), Qt.UserRole + 1) # None if not available
            item_ref_st.setEditable(False)
            # extend with x2 - xref, x0 - xref
            ref_row = [item_ref_st, QStandardItem('-'), QStandardItem('-')]
            [i.setEditable(False) for i in ref_row]
            row.extend(ref_row)

            # alarm switches, read and tune alms
            tune_alm_pv, read_alm_pv = self.get_alm_pv(fld.ename, fld.name)
            item_read_alm = QStandardItem('')
            item_read_alm.setData(read_alm_pv, Qt.UserRole + 1) # None if not availble
            item_read_alm.setEditable(False)
            item_tune_alm = QStandardItem('')
            item_tune_alm.setData(tune_alm_pv, Qt.UserRole + 1) # None if not availble
            item_tune_alm.setEditable(False)
            row.extend([item_tune_alm, item_read_alm])

            #
            self.appendRow(row)
            ename_set.add(elem.name)
            field_cnt += 1

        self.settings_sts.emit(len(ename_set), field_cnt)

    def set_model(self):
        # set data
        self.set_data()
        # set model
        proxy_model = _SortProxyModel(self)
        self._tv.setModel(proxy_model)
        #
        # hide columns: pos, dx01, tolerance, writable
        for i in (self.i_pos, self.i_val0_rd, self.i_tol, self.i_writable,
                  self.i_ref_st, self.i_dstref, self.i_dval0ref,
                  self.i_read_alm, self.i_tune_alm):
            self._tv.setColumnHidden(i, True)
        #
        self.__post_init_ui()

    def __post_init_ui(self):
        # set headers
        tv = self._tv
        tv.setSortingEnabled(True)
        for i, s in zip(self.ids, self.header):
            self.setHeaderData(i, Qt.Horizontal, s)
        tv.model().sort(self.i_pos)
        tv.header().setStyleSheet("""
            QHeaderView {
                font-weight: bold;
            }""")
        #
        self.style_view(font=self._font)
        tv.setStyleSheet("""
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
        self.fit_view()

    def style_view(self, **kws):
        """
        font, font_size, font_family
        """
        self._tv.setItemDelegate(_Delegate(**kws))

    def fit_view(self):
        tv = self._tv
        #tv.expandAll()
        for i in self.ids:
            tv.resizeColumnToContents(i)
        #tv.collapseAll()

    @pyqtSlot()
    def on_delete_selected_items(self):
        # delete selected items ?
        checked_items = []
        for i in range(self.rowCount()):
            idx = self.index(i, self.i_name)
            it_name = self.itemFromIndex(idx)
            if is_item_checked(it_name):
                checked_items.append(it_name)

        fobj_list = []
        for item in checked_items:
            idx = self.indexFromItem(item)
            irow = idx.row()
            ename = item.text()
            fobj = item.fobj

            print("{} [{}] is to be deleted.".format(fobj.ename, fobj.name))
            # delete items from self._fld(pv)_it and self._fld(pv)_obj
            ind = self._fld_obj.index(fobj)
            self._fld_it.pop(ind)
            self._fld_obj.pop(ind)
            #
            fobj_list.append(fobj)
            # delete
            self.removeRow(irow)

        # field object list that to be deleted
        self.item_deletion_updated.emit(fobj_list)

    def hlrow(self, idx_src):
        idx = self._tv.model().mapFromSource(idx_src)
        self._tv.scrollTo(idx)
        self._tv.selectionModel().select(idx,
                QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)

    def get_checked_items_number(self):
        """Get the total number of checked items.
        """
        # for double-check when applying device settings.
        # not used, use len(_SortProxyModel.get_selection()) instead
        n = 0
        for i in range(self.rowCount()):
            idx = self.index(i, self.i_name)
            it = self.itemFromIndex(idx)
            if is_item_checked(it):
                n += 1
        return n

    def get_ref_pv(self, ename, fname):
        # Return the PV obj for reference set.
        return self.ref_st_pv_map.get(f"{ename}-{fname}", None)

    def get_tol_pv(self, ename, fname):
        # Return the PV obj for live rd-st tolerance.
        return self.tol_pv_map.get(f"{ename}-{fname}", None)

    def get_alm_pv(self, ename, fname):
        # Return the PV objs for alarm switches, (tune, read)
        return self.alm_act_pv_map.get(f"{ename}-{fname}", (None, None))


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
            'tolerance': model.i_tol,
            'writable': model.i_writable,
            'x2/x0': model.i_ratio_x20,
            'state': model.i_sts,
            'last_state': model.i_last_sts,
            'ref_st': model.i_ref_st,
            'dx2ref': model.i_dstref,
            'dx0ref': model.i_dval0ref,
            'read_alm': model.i_read_alm,
            'tune_alm': model.i_tune_alm,
        }
        self.filter_ftypes = ['ENG', 'PHY']
        # if True, filter checked items, otherwise show all items.
        self.filter_checked_enabled = False
        self.filter_dx12_warning_enabled = False
        self.filter_dx02_warning_enabled = False
        self.filter_disconnected_enabled = False
        self.filter_dx0ref_warning_enabled = False
        self.filter_dx2ref_warning_enabled = False
        self.filter_disabled_read_alm_enabled = False
        self.filter_disabled_tune_alm_enabled = False
        self.filter_enabled_read_alm_enabled = False
        self.filter_enabled_tune_alm_enabled = False
        # field filter
        self.filter_field_enabled = False
        self.filter_field_list = []
        # dtype filter
        self.filter_dtype_enabled = False
        self.filter_dtype_list = []
        # pos filter <->
        self.filter_pos1_enabled = False
        self.filter_pos2_enabled = False
        self.filter_pos_value = None

        # state diff
        self.filter_state_diff_enabled = False

        #
        self._filter_tuples = None

    def lessThan(self, left, right):
        left_data = left.data(Qt.DisplayRole)
        right_data = right.data(Qt.DisplayRole)

        if left_data is None or right_data is None:
            return True

        if left.column() == self.filter_col_index['device']: # ename
           left_data = left.data(Qt.UserRole + 1)
           right_data = right.data(Qt.UserRole + 1)

        try:
            r = float(left_data) < float(right_data)
        except ValueError:
            if left.column() in (self.filter_col_index['state'],
                                 self.filter_col_index['last_state']): # state and last state
                left_data = left.data(Qt.ToolTipRole)
                right_data = right.data(Qt.ToolTipRole)
                if left_data is None or right_data is None:
                    left_data = right_data = 'None'
            r = left_data < right_data
        return r

    def test_string_filters(self, src_row, m_src):
        if self.get_filters() is None:
            return True
        for key, is_number_key, value in self.get_filters():
            if not self.test_one_string_filter(src_row, m_src, key, is_number_key, value):
                return False
        return True

    def test_one_string_filter(self, src_row, m_src, key, is_number_key, value):
        # test if the value of *key* of *m_src* matches *value*
        # 1. for number columns: value range is supported
        # 2. for string columns: 'in' operation is supported
        #
        idx = self.filter_col_index[key]
        src_index = m_src.index(src_row, idx)
        if key in ('state', 'last_state'):
            var = src_index.data(Qt.ToolTipRole)
        else:
            var = src_index.data(Qt.DisplayRole)

        if not isinstance(var, str):
            var = str(var)

        # number keys
        if is_number_key:
            var = float(var)
            filter_str = value
            # in test?
            if 'in' in value:
                try:
                    val_test = eval(f'{var} {value}')
                except (SyntaxError, NameError):
                    pass
                else:
                    return val_test
            #
            try:
                t = eval(filter_str)
                # (x1, x2) or [x1, x2], or (x1, x2, x3) (only use x1, x2)
                if isinstance(t, (tuple, list)):
                    if len(t) > 1:
                        x1, x2 = t[0], t[1]
                        val_test = (var >= x1 and var <= x2)
                    elif len(t) == 1:
                        # (x1,) or [x1,]
                        val_test = var >= t[0]
                    else:
                        raise SyntaxError
                elif isinstance(t, (float, int)):
                        val_test = is_equal(var, t, ndigit)
                else:
                    raise SyntaxError
            except (SyntaxError, NameError):
                val_test = re.match(translate(filter_str), str(var)) is not None
            finally:
                return val_test
        else:
            if 'in' in value:
                try:
                    val_test = eval(f'"{var}" {value}')
                except (SyntaxError, NameError):
                    pass
                else:
                    return val_test
            # Qt >= 5.12
            # regex = self.filterRegularExpression()
            # return ftype in self.filter_ftypes and regex.match(var).hasMatch()

            # wildcardunix
            # regex = self.filterRegExp()
            # return ftype in self.filter_ftypes and regex.exactMatch(var)
            #
            return re.match(translate(value), var) is not None

    def filterAcceptsRow(self, src_row, src_parent):
        if src_parent.isValid():
            return True
        src_model = self.sourceModel()
        ndigit = src_model._ndigit

        # ENG/PHY
        try:
            ftype = src_model.item(src_row, src_model.i_name).ftype
            ftype_test = ftype in self.filter_ftypes
        except AttributeError:
            ftype_test = True
        #
        if not ftype_test:
            return False

        # checked items
        try:
            if self.filter_checked_enabled:
                item_checked_test = is_item_checked(
                        src_model.item(src_row, src_model.i_name))
            else:
                item_checked_test = True
        except AttributeError:
            item_checked_test = True
        #
        if not item_checked_test:
            return False

        # dx12 checked
        try:
            if self.filter_dx12_warning_enabled:
                data = src_model.data(
                        src_model.index(src_row, self.filter_col_index['dx12']),
                        Qt.UserRole)
                dx12_warning_test = data is not None
            else:
                dx12_warning_test = True
        except AttributeError:
            dx12_warning_test = True
        #
        if not dx12_warning_test:
            return False

        # dx02 checked
        try:
            if self.filter_dx02_warning_enabled:
                data = src_model.data(
                        src_model.index(src_row, self.filter_col_index['dx02']),
                        Qt.UserRole)
                dx02_warning_test = data is not None
            else:
                dx02_warning_test = True
        except AttributeError:
            dx02_warning_test = True
        #
        if not dx02_warning_test:
            return False

        # diff(x0, ref_st) checked
        try:
            if self.filter_dx0ref_warning_enabled:
                data = src_model.data(
                        src_model.index(src_row, self.filter_col_index['dx0ref']),
                        Qt.UserRole)
                dx0ref_warning_test = data is not None
            else:
                dx0ref_warning_test = True
        except AttributeError:
            dx0ref_warning_test = True
        #
        if not dx0ref_warning_test:
            return False

        # diff(x2, ref_st) checked
        try:
            if self.filter_dx2ref_warning_enabled:
                data = src_model.data(
                        src_model.index(src_row, self.filter_col_index['dx2ref']),
                        Qt.UserRole)
                dx2ref_warning_test = data is not None
            else:
                dx2ref_warning_test = True
        except AttributeError:
            dx2ref_warning_test = True
        #
        if not dx2ref_warning_test:
            return False

        # disconnected checked
        try:
            if self.filter_disconnected_enabled:
                data = src_model.data(
                        src_model.index(src_row, self.filter_col_index['device']),
                        Qt.ToolTipRole)
                disconnected_test = data == 'Device is not connected'
            else:
                disconnected_test = True
        except AttributeError:
            disconnected_test = True
        #
        if not disconnected_test:
            return False

        # disabled read alam checked
        try:
            if self.filter_disabled_read_alm_enabled:
                data = src_model.data(
                        src_model.index(src_row, self.filter_col_index['read_alm']),
                        Qt.UserRole)
                disabled_read_alm_test = data == 0.0
            else:
                disabled_read_alm_test = True
        except AttributeError:
            disabled_read_alm_test = True
        #
        if not disabled_read_alm_test:
            return False

        # disabled tune alam checked
        try:
            if self.filter_disabled_tune_alm_enabled:
                data = src_model.data(
                        src_model.index(src_row, self.filter_col_index['tune_alm']),
                        Qt.UserRole)
                disabled_tune_alm_test = data == 0.0
            else:
                disabled_tune_alm_test = True
        except AttributeError:
            disabled_tune_alm_test = True
        #
        if not disabled_tune_alm_test:
            return False

        # enabled read alam checked
        try:
            if self.filter_enabled_read_alm_enabled:
                data = src_model.data(
                        src_model.index(src_row, self.filter_col_index['read_alm']),
                        Qt.UserRole)
                enabled_read_alm_test = data == 1.0
            else:
                enabled_read_alm_test = True
        except AttributeError:
            enabled_read_alm_test = True
        #
        if not enabled_read_alm_test:
            return False

        # enabled tune alam checked
        try:
            if self.filter_enabled_tune_alm_enabled:
                data = src_model.data(
                        src_model.index(src_row, self.filter_col_index['tune_alm']),
                        Qt.UserRole)
                enabled_tune_alm_test = data == 1.0
            else:
                enabled_tune_alm_test = True
        except AttributeError:
            enabled_tune_alm_test = True
        #
        if not enabled_tune_alm_test:
            return False

        # state diff checked
        try:
            if self.filter_state_diff_enabled:
                sts = src_model.data(
                        src_model.index(src_row, self.filter_col_index['state']),
                        Qt.ToolTipRole)
                last_sts = src_model.data(
                        src_model.index(src_row, self.filter_col_index['last_state']),
                        Qt.ToolTipRole)
                state_diff_test = sts != last_sts
            else:
                state_diff_test = True
        except AttributeError:
            state_diff_test = True
        #
        if not state_diff_test:
            return False

        # field test
        try:
            if self.filter_field_enabled:
                data = src_model.data(
                        src_model.index(src_row, self.filter_col_index['field']),
                        Qt.DisplayRole)
                field_test = data in self.filter_field_list
            else:
                field_test = True
        except AttributeError:
            field_test = True
        #
        if not field_test:
            return False

        # dtype test
        try:
            if self.filter_dtype_enabled:
                data = src_model.data(
                        src_model.index(src_row, self.filter_col_index['type']),
                        Qt.DisplayRole)
                dtype_test = data in self.filter_dtype_list
            else:
                dtype_test = True
        except AttributeError:
            dtype_test = True
        #
        if not dtype_test:
            return False

        # pos test (sb <= pos or sb > pos)
        try:
            if self.filter_pos1_enabled or self.filter_pos2_enabled:
                data = src_model.data(
                        src_model.index(src_row, self.filter_col_index['pos']),
                        Qt.DisplayRole)
                v = float(data)
                pos1_test = False
                pos2_test = False
                pos = self.filter_pos_value
                if self.filter_pos1_enabled:
                    pos1_test = v <= pos
                if self.filter_pos2_enabled:
                    pos2_test = v > pos
                pos_test = pos1_test or pos2_test
            else:
                pos_test = True
        except AttributeError:
            pos_test = True
        #
        if not pos_test:
            return False

        # string filters
        try:
            if not self.test_string_filters(src_row, src_model):
                return False
        except AttributeError:
            return True

        return True

    def set_filters(self, filter_tuples):
        # filter_tuples: list of tuples of (key, is_number_key, shell_pattern_string)
        self._filter_tuples = filter_tuples

    def get_filters(self,):
        return self._filter_tuples

    def get_selection(self):
        # Return a list of selected items, [(idx_src, settings, new_fval0)].
        settings_selected = []
        for i in range(self.rowCount()):
            idx = self.index(i, self.m_src.i_name)
            idx_src = self.mapToSource(idx)
            it_name_src = self.m_src.itemFromIndex(idx_src)
            if is_item_checked(it_name_src):
                # print(self.data(idx), it_name_src.text(), idx_src.row())
                new_fval0 = float(self.m_src.data(
                                  self.m_src.index(idx_src.row(), self.m_src.i_val0)))
                settings_selected.append((idx_src, self.m_src._settings[idx_src.row()], new_fval0))
        return settings_selected

    def get_selection_refset(self):
        # Return a list of selected items, [(ref_st_idx(src), ref_st_pv, new_fval0)].
        settings_selected = []
        for i in range(self.rowCount()):
            idx = self.index(i, self.m_src.i_name)
            idx_src = self.mapToSource(idx)
            it_name_src = self.m_src.itemFromIndex(idx_src)
            if is_item_checked(it_name_src):
                # new_fval0 = float(self.m_src.data(
                #                   self.m_src.index(idx_src.row(), self.m_src.i_val0)))
                _, _, _, new_fval0 = self.m_src._settings[idx_src.row()] # elem, fname, fld, fval0
                ref_st_idx = self.m_src.index(idx_src.row(), self.m_src.i_ref_st)
                ref_st_pv = self.m_src.data(ref_st_idx, Qt.UserRole + 1)
                # ref_v0 = self.m_src.data(ref_st_idx, Qt.DisplayRole) # current refset, maybe -
                settings_selected.append((ref_st_idx, ref_st_pv, new_fval0))
        return settings_selected

    def get_selection_almset(self):
        # Return a list of selected items
        # [(read_alm_idx(src), read_alm_pv, tune_alm_idx(src), tune_alm_pv)].
        settings_selected = []
        for i in range(self.rowCount()):
            idx = self.index(i, self.m_src.i_name)
            idx_src = self.mapToSource(idx)
            it_name_src = self.m_src.itemFromIndex(idx_src)
            if is_item_checked(it_name_src):
                read_alm_idx = self.m_src.index(idx_src.row(), self.m_src.i_read_alm)
                read_alm_pv = self.m_src.data(read_alm_idx, Qt.UserRole + 1)
                tune_alm_idx = self.m_src.index(idx_src.row(), self.m_src.i_tune_alm)
                tune_alm_pv = self.m_src.data(tune_alm_idx, Qt.UserRole + 1)
                settings_selected.append((read_alm_idx, read_alm_pv, tune_alm_idx, tune_alm_pv))
        return settings_selected

    def select_one(self, row_idx, checked):
        idx = self.index(row_idx, self.m_src.i_name)
        idx_src = self.mapToSource(idx)
        it_name_src = self.m_src.itemFromIndex(idx_src)
        if not it_name_src.isEnabled():
            return
        current_check_state = it_name_src.checkState()
        if checked:
            check_state = Qt.Checked
        else:
            check_state = Qt.Unchecked
        if current_check_state == check_state:
            return
        it_name_src.setCheckState(check_state)

    def toggle_selection_one(self, row_idx: int):
        idx = self.index(row_idx, self.m_src.i_name)
        idx_src = self.mapToSource(idx)
        it_name_src = self.m_src.itemFromIndex(idx_src)
        if not it_name_src.isEnabled():
            return
        if not is_item_checked(it_name_src):
            check_state = Qt.Checked
        else:
            check_state = Qt.Unchecked
        it_name_src.setCheckState(check_state)

    def select_all(self, checked=True):
        for i in range(self.rowCount()):
            self.select_one(i, checked)

    def invert_selection(self):
        check_state_list = []
        for i in range(self.rowCount()):
            idx = self.index(i, self.m_src.i_name)
            idx_src = self.mapToSource(idx)
            it_name_src = self.m_src.itemFromIndex(idx_src)
            if not it_name_src.isEnabled():
                continue
            if not is_item_checked(it_name_src):
                check_state = Qt.Checked
            else:
                check_state = Qt.Unchecked
            check_state_list.append((it_name_src, check_state))
        [it.setCheckState(st) for it, st in check_state_list]


class _Delegate(QStyledItemDelegate):

    def __init__(self, **kws):
        super(self.__class__, self).__init__()
        self.font = kws.get('font', None)
        self.font_size = kws.get('font_size', None)
        self.font_family = kws.get('font_family', None)

    def initStyleOption(self, option, index):
        if self.font is not None:
            option.font = self.font
        else:
            if self.font_size is not None:
                option.font.setPointSize(self.font_size)
            if self.font_family is not None:
                option.font.setFamily(self.font_family)
        QStyledItemDelegate.initStyleOption(self, option, index)

    def sizeHint(self, option, index):
        size = QStyledItemDelegate.sizeHint(self, option, index)
        size.setHeight(int(size.height() * 1.3))
        return size


def convert_settings(settings_read, lat):
    """Convert hierarchical `Settings` to flat list of tuples as the return,
    each tuple is composed of (CaElement, field name, CaField, field value).

    Parameters
    ----------
    settings_read : Settings
        Key-value pairs of element settings, value is key-value pairs of field
        and value.
    lat : Lattice
        High-level lattice object.

    Returns
    -------
    r : list
        List of tuple of settings.
    """
    flat_settings = []
    for ename, econf in settings_read.items():
        elem = lat[ename]
        # if elem is None:
        #    print("{} is not in lattice but defined in the settings.".format(ename))
        #    continue
        for fname, fval0 in econf.items():
            confline = (elem, fname, elem.get_field(fname), fval0)
            flat_settings.append(confline)
    return flat_settings


def pack_settings(elem_list, lat, **kws):
    """Pack up element settings of as a tuple to return.

    Parameters
    ----------
    elem_list : list
        List of CaElement.
    lat : Lattice
        High-level lattice object.

    Keyword Arguments
    -----------------
    data_source : str
        'model' or 'control', get element settings from MODEL environment if
        *data_source* is 'model', otherwise get live settings from controls
        network.
    settings : Settings
        Predefined physics Settings from '.json' file which should includes
        all the elements in *elem_list*.
    only_physics : bool
        If True, onle get physics settings, other wise, get engineering
        settings as well.

    Returns
    -------
    t : tuple
        Tuple of (flat_s[list], s[Settings]), element of flat_s:
        (CaElement, field_name, CaField, field_value)
    """
    foi = kws.pop('field_of_interest', DEFAULT_FOI_DICT)
    settings = get_settings_from_element_list(elem_list,
                                              field_of_interest=foi,
                                              **kws)
    flat_settings = convert_settings(settings, lat)
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


def is_equal(a, b, decimal=6):
    """Test if a and b is almost equal.
    """
    try:
        assert_almost_equal(a, b, decimal=decimal)
        return True
    except AssertionError:
        return False


def init_config_dir(confdir):
    # initialize configuration directory
    # return the fullpaths of root path, ts, ms, elem paths.
    confdir = os.path.expanduser(confdir)
    if not os.path.exists(confdir):
        os.makedirs(confdir)
        reset_config(confdir)

    ts_confpath = os.path.join(confdir, 'tolerance.json')
    ms_confpath = os.path.join(confdir, 'settings.json')
    elem_confpath = os.path.join(confdir, 'elements.json')

    if not os.path.exists(elem_confpath):
        shutil.copy2(DEFAULT_ELEM_PATH, elem_confpath)

    return confdir, ts_confpath, ms_confpath, elem_confpath


def reset_config(current_config_path):
    ts_path = os.path.join(current_config_path, 'tolerance.json')
    ms_path = os.path.join(current_config_path, 'settings.json')
    elem_path = os.path.join(current_config_path, 'elements.json')

    for default_path, path in zip(
            (DEFAULT_TS_PATH, DEFAULT_MS_PATH, DEFAULT_ELEM_PATH),
            (ts_path, ms_path, elem_path)):
        shutil.copy2(default_path, path)


def str2float(s):
    """Convert string to float, if s is an valid expression, return
    the evaluated result, otherwise return None.
    """
    try:
        r = float(s)
    except ValueError:
        try:
            r = eval(s)
        except (SyntaxError, NameError):
            r = None
    finally:
        return r


def get_ratio_as_string(a, b, fmt):
    # return a/b, if b is zero, return -
    try:
        r = fmt.format(a / b)
    except ZeroDivisionError:
        r = 'inf'
    finally:
        return r


class SnapshotDataModel(QStandardItemModel):

    save_settings = pyqtSignal(SnapshotData)

    def __init__(self, parent, snp_list, **kws):
        super(self.__class__, self).__init__(parent)
        self._v = parent
        self._snp_list = snp_list
        # [
        #  SnapshotData,
        # ]
        self.loaded_px = QPixmap(":/sm-icons/cast_connected.png").scaled(PX_SIZE, PX_SIZE)
        self.load_px = QPixmap(":/sm-icons/cast.png").scaled(PX_SIZE, PX_SIZE)
        self.note_px = QPixmap(":/sm-icons/comment.png").scaled(PX_SIZE, PX_SIZE)
        self.tags_px = QPixmap(":/sm-icons/label.png").scaled(PX_SIZE, PX_SIZE)

        self.header = self.h_ts, self.h_name, \
                      self.h_ion, self.h_ion_number, self.h_ion_mass, self.h_ion_charge, \
                      self.h_load_status, self.h_user, \
                      self.h_is_golden, self.h_tags, self.h_note \
                    = "Timestamp", "Name", \
                      "Ion", "Z", "A", "Q", \
                      "", "User", \
                      "", "Tags", "Note"
        self.ids = self.i_ts, self.i_name, \
                   self.i_ion, self.i_ion_number, self.i_ion_mass, self.i_ion_charge, \
                   self.i_load_status, self.i_user, \
                   self.i_is_golden, self.i_tags, self.i_note \
                 = range(len(self.header))

        self.dataChanged.connect(self.on_data_changed)

        # filters
        self._ion_filter_list = None
        self._ion_filter_cnt = Counter()
        #
        self._tag_filter_list = None
        self._tag_filter_cnt = Counter()

    def set_ion_filters(self, d):
        self._ion_filter_cnt = Counter()
        self._ion_filter_list = [k for k, v in d.items() if v]

    def get_ion_filters(self):
        return self._ion_filter_list

    def set_tag_filters(self, d):
        self._tag_filter_cnt = Counter()
        self._tag_filter_list = [k for k, v in d.items() if v]

    def get_tag_filters(self):
        return self._tag_filter_list

    def set_model(self):
        self.set_data()
        self._v.setModel(_SnpProxyModel(self))
        self._post_init_ui(self._v)

    def set_data(self):
        data = {}  # root-i: [snp-1, snp-2, ...]
        for i in self._snp_list:
            data.setdefault(i.ts_as_date(), []).append(i)
        self._data = data

        for ts_date in sorted(data):
            #
            ts_snp_data_list = data[ts_date]  # snp data under ts_date root
            it_root = QStandardItem(ts_date)
            it_root.setEditable(False)

            for snp_data in ts_snp_data_list:
                # ts
                it_ts = QStandardItem(snp_data.ts_as_str())
                it_ts.setEditable(False)
                it_ts.snp_data = snp_data

                # name (invisible)
                it_name = QStandardItem(snp_data.name)

                # ion: name
                it_ion_name = QStandardItem(snp_data.ion_name)
                it_ion_name.setEditable(False)
                _z, _a, _q = snp_data.ion_number, snp_data.ion_mass, snp_data.ion_charge
                # ion: Z (str)
                it_ion_number = QStandardItem(_z)
                it_ion_number.setData(int(_z), Qt.UserRole)
                it_ion_number.setEditable(False)
                # ion: A (str)
                it_ion_mass = QStandardItem(_a)
                it_ion_mass.setData(int(_a), Qt.UserRole)
                it_ion_mass.setEditable(False)
                # ion: Q (str)
                it_ion_charge = QStandardItem(_q)
                it_ion_charge.setData(int(_q), Qt.UserRole)
                it_ion_charge.setEditable(False)
                # user
                it_user = QStandardItem(snp_data.user)
                it_user.setEditable(False)

                # tags (list), editable
                tags_as_str = snp_data.tags_as_str()
                it_tags = QStandardItem(tags_as_str)
                it_tags.setData(self.tags_px, Qt.DecorationRole)
                if tags_as_str == '':
                    it_tags.setToolTip("Input strings seperated by comma as tags.")
                else:
                    it_tags.setToolTip(tags_as_str)
                # is golden?
                it_is_golden = QStandardItem()
                self.set_golden_status(snp_data.is_golden(), it_is_golden)

                # note (str)
                it_note = QStandardItem(snp_data.note)
                it_note.setData(self.note_px, Qt.DecorationRole)
                it_note.setToolTip(snp_data.note)

                # load status
                it_load_status = QStandardItem()
                it_load_status.setData(self.load_px, Qt.DecorationRole)
                it_load_status.setData("not-loaded", Qt.UserRole)
                it_load_status.setToolTip("Load snapshot by double-clicking")

                row = (
                    it_ts, it_name,
                    it_ion_name, it_ion_number, it_ion_mass, it_ion_charge,
                    it_load_status,
                    it_user, it_is_golden, it_tags, it_note
                )
                it_root.appendRow(row)

            #
            ph_list = []
            for i in range(len(self.header) - 1):
                it = QStandardItem('')
                it.setEditable(False)
                ph_list.append(it)
            self.appendRow((it_root, *ph_list))

    def on_data_changed(self, idx1, idx2):
        if idx1.column() in (self.i_load_status, self.i_is_golden):
            return
        s = idx1.data(Qt.DisplayRole)
        i, j = idx1.row(), idx1.column()
        pindex = idx1.parent()
        snp_data = self.itemFromIndex(self.index(i, self.i_ts, pindex)).snp_data
        if j == self.i_note:
            snp_data.note = s
        elif j == self.i_name:
            snp_data.name = s
        elif j == self.i_tags:
            snp_data.tags = s
            it = self.itemFromIndex(self.index(i, self.i_is_golden, pindex))
            self.set_golden_status(snp_data.is_golden(), it)
        self.dataChanged.disconnect()
        self.itemFromIndex(idx1).setToolTip(s)
        self.dataChanged.connect(self.on_data_changed)
        self.save_settings.emit(snp_data)

    def _post_init_ui(self, v):
        for i, s in zip(self.ids, self.header):
            self.setHeaderData(i, Qt.Horizontal, s)
        # view properties
        v.setStyleSheet("""
            QTreeView {
                font-family: monospace;
                show-decoration-selected: 1;
                alternate-background-color: #F7F7F7;
            }

            QTreeView::item {
                border: 1px solid #D9D9D9;
                border-top-color: transparent;
                border-bottom-color: transparent;
            }

            QTreeView::item:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);
                border: 1px solid #bfcde4;
            }

            QTreeView::item:selected:!has-children {
                border: 1px solid #567DBC;
                background-color: #D3D7CF;
            }

            QTreeView::item:selected:active:!has-children {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #99C0FC, stop: 1 #7BACF9);
            }

            QTreeView::item::has-children {
                color: #308CC6;
            }

            /*
            QTreeView::branch {
                    background: palette(base);
            }

            QTreeView::branch:has-siblings:!adjoins-item {
                    background: cyan;
            }

            QTreeView::branch:has-siblings:adjoins-item {
                    background: red;
            }

            QTreeView::branch:!has-children:!has-siblings:adjoins-item {
                    background: blue;
            }

            QTreeView::branch:closed:has-children:has-siblings {
                    background: pink;
            }

            QTreeView::branch:has-children:!has-siblings:closed {
                    background: gray;
            }

            QTreeView::branch:open:has-children:has-siblings {
                    background: magenta;
            }

            QTreeView::branch:open:has-children:!has-siblings {
                    background: green;
            }
            */
            """)
        #
        self.style_view(v)
        #
        v.setAlternatingRowColors(True)
        v.header().setStretchLastSection(True)
        v.header().setStyleSheet("""
            QHeaderView {
                font-weight: bold;
            }""")

        #
        v.expandAll()
        for i in (self.i_ts, self.i_name,
                  self.i_ion, self.i_ion_number, self.i_ion_mass, self.i_ion_charge,
                  self.i_load_status, self.i_user, self.i_is_golden,
                  self.i_tags):
            v.resizeColumnToContents(i)
        v.collapseAll()

        # hide name col
        v.setColumnHidden(self.i_name, True)
        #
        v.setSortingEnabled(True)

    def remove_data(self, data):
        # remove snp
        found = False
        for ii in range(self.rowCount()):
            ridx = self.index(ii, 0)
            if not self.hasChildren(ridx):
                continue
            for i in range(self.rowCount(ridx)):
                it = self.itemFromIndex(self.index(i, self.i_name, ridx))
                if it.text() == data.name:
                    irow = i
                    iidx = ridx
                    found = True
                    break
            if found:
                break
        if found:
            self.removeRow(irow, iidx)

    @pyqtSlot('QString', 'QString')
    def on_snp_saved(self, snp_name, filepath):
        # snp data is saved/updated
        pass

    def set_golden_status(self, is_golden: bool, it: QStandardItem) -> None:
        px = QPixmap(QSize(PX_SIZE, PX_SIZE))
        if is_golden:
            bgc = BG_COLOR_GOLDEN_YES
            tt = TT_GOLDEN
        else:
            bgc = BG_COLOR_GOLDEN_NO
            tt = TT_NOT_GOLDEN
        px.fill(QColor(*bgc))
        it.setData(px, Qt.DecorationRole)
        it.setData(tt, Qt.UserRole)
        it.setToolTip(tt)

    @pyqtSlot(SnapshotData)
    def on_snp_loaded(self, snpdata):
        # updated loaded dec role for ALL rows, hl casted row.
        snp_name = snpdata.name
        self._v.clearSelection()
        for ii in range(self.rowCount()):
            ridx = self.index(ii, 0)
            if not self.hasChildren(ridx):
                continue
            for i in range(self.rowCount(ridx)):
                if self.itemFromIndex(self.index(i, self.i_name, ridx)).text() == snp_name:
                    loaded = True
                else:
                    loaded = False
                idx = self.index(i, self.i_load_status, ridx)
                self.set_loaded(idx, loaded)
                if loaded:
                    idx = self._v.model().mapFromSource(idx)
                    self._v.scrollTo(idx)
                    self._v.selectionModel().select(idx,
                            QItemSelectionModel.Select | QItemSelectionModel.Rows)

    def clear_load_status(self):
        for ii in range(self.rowCount()):
            ridx = self.index(ii, 0)
            if not self.hasChildren(ridx):
                continue
            for i in range(self.rowCount(ridx)):
                idx = self.index(i, self.i_load_status, ridx)
                if self.data(idx, Qt.UserRole) == 'loaded':
                    self.set_loaded(idx, False)
                    break
            break

    def set_loaded(self, idx, loaded):
        if loaded:
            self.setData(idx, self.loaded_px, Qt.DecorationRole)
            self.setData(idx, TT_LOADED, Qt.UserRole)
            tt = "Snapshot loaded."
        else:
            self.setData(idx, self.load_px, Qt.DecorationRole)
            self.setData(idx, TT_NOT_LOADED, Qt.UserRole)
            tt = "Load snapshot by double-clicking"
        self.setData(idx, tt, Qt.ToolTipRole)

    def style_view(self, v):
        v.setItemDelegate(_DelegateSnapshot(v))


class _DelegateSnapshot(QStyledItemDelegate):

    def __init__(self, parent=None, **kws):
        super(self.__class__, self).__init__()
        self.v = parent
        self.v.setMouseTracking(True)
        self.v.entered.connect(self.on_item_entered)
        self.is_item_in_edit_mode = False
        self.current_edited_item_index = QPersistentModelIndex()

    def createEditor(self, parent, option, index):
        op = index.model().data(index, Qt.UserRole + 1)
        if op in ACT_BTN_CONF:
            tt, text, px_path = ACT_BTN_CONF[op]
            btn = QPushButton(parent)
            if px_path is not None:
                btn.setIcon(QIcon(QPixmap(px_path)))
                btn.setIconSize(QSize(PX_SIZE, PX_SIZE))
            if text is not None:
                btn.setText(text)
            btn.setToolTip(tt)
            btn.setGeometry(option.rect)
            btn.clicked.connect(partial(self.on_btn_clicked, index, op))
            return btn
        else:
            return QStyledItemDelegate.createEditor(self, parent, option, index)

    def paint(self, painter, option, index):
        op = index.model().data(index, Qt.UserRole + 1)
        if op in ACT_BTN_CONF:
            tt, text, px_path = ACT_BTN_CONF[op]
            btn = QPushButton(self.v)
            if px_path is not None:
                btn.setIcon(QIcon(QPixmap(px_path)))
                btn.setIconSize(QSize(PX_SIZE, PX_SIZE))
            if text is not None:
                btn.setText(text)
            btn.setToolTip(tt)
            btn.setGeometry(option.rect)
            if option.state == QStyle.State_Selected:
                painter.fillRect(option.rect, option.palette.highlight())
            painter.drawPixmap(option.rect.x(), option.rect.y(), btn.grab())
        else:
            QStyledItemDelegate.paint(self, painter, option, index)

    @pyqtSlot()
    def on_btn_clicked(self, index, op):
        m = index.model()
        src_m = m.sourceModel()
        src_idx = m.mapToSource(index)
        data = src_m.itemFromIndex(src_m.index(src_idx.row(), src_m.i_ts, src_idx.parent())).snp_data

    def setEditorData(self, editor, index):
        QStyledItemDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        QStyledItemDelegate.setModelData(self, editor, model, index)

    def updateEditorGeometry(self, editor, option, index):
        if index.model().data(index, Qt.UserRole + 1) in ACT_BTN_CONF:
            editor.setGeometry(option.rect)
        else:
            QStyledItemDelegate.updateEditorGeometry(self, editor, option, index)

    def on_item_entered(self, index):
        op = index.model().data(index, Qt.UserRole + 1)
        if op in ACT_BTN_CONF:
            if self.is_item_in_edit_mode:
                self.v.closePersistentEditor(self.current_edited_item_index)
            self.v.openPersistentEditor(index)
            self.is_item_in_edit_mode = True
            self.current_edited_item_index = index
        else:
            if self.is_item_in_edit_mode:
                self.is_item_in_edit_mode = False
                self.v.closePersistentEditor(self.current_edited_item_index)

    def initStyleOption(self, option, index):
        QStyledItemDelegate.initStyleOption(self, option, index)

    def sizeHint(self, option, index):
        size = QStyledItemDelegate.sizeHint(self, option, index)
        size.setHeight(48)
        return size


class _SnpProxyModel(QSortFilterProxyModel):

    def __init__(self, model):
        super(_SnpProxyModel, self).__init__()
        self.m_src = model
        self.setSourceModel(model)
        self.setRecursiveFilteringEnabled(True)
        self.reset_cache()
        # date range filter
        self.filter_date_enabled = False
        self.filter_date_tuple = None # (date1, date2)
        # note filter
        self.filter_note_enabled = False
        self.filter_note_string = None
        # user name filter
        self.filter_user_enabled = False
        self.filter_user_list = []

    def reset_cache(self):
        self._ion_hit_cache = {}
        self._tag_hit_cache = {}

    def lessThan(self, left, right):
        left_data1, left_data2 = left.data(Qt.DisplayRole), left.data(Qt.UserRole)
        right_data1, right_data2 = right.data(Qt.DisplayRole), right.data(Qt.UserRole)
        if left_data2 is not None:
            return left_data2 < right_data2
        return QSortFilterProxyModel.lessThan(self, left, right)

    def filterAcceptsRow(self, src_row, src_parent):
        if not src_parent.isValid():
            return False
        m = self.sourceModel()
        ion_filter_list = m.get_ion_filters()
        tag_filter_list = m.get_tag_filters()
        snp_data = m.itemFromIndex(m.index(src_row, m.i_ts, src_parent)).snp_data
        if ion_filter_list is None:
            ion_test = True
        else:
            ion_name = snp_data.ion_name
            is_cnted = self._ion_hit_cache.setdefault(snp_data.name, False)
            if not is_cnted:
                m._ion_filter_cnt[ion_name] += 1
                self._ion_hit_cache[snp_data.name] = True
            ion_test = ion_name in ion_filter_list
        if not ion_test:
            return False

        if tag_filter_list is None:
            tag_test = True
        else:
            if snp_data.tags == []:
                tags = ['NOTAG']
            else:
                tags = snp_data.tags
            tag_test = False
            for tag in tags:
                if not tag_test and tag in tag_filter_list:
                    tag_test = True
                is_cnted = self._tag_hit_cache.setdefault(snp_data.name, False)
                if not is_cnted:
                    for i in tags:
                        m._tag_filter_cnt[i] += 1 # +1 for all tags of this snp
                    self._tag_hit_cache[snp_data.name] = True

        if not tag_test:
            return False

        # date
        try:
            if self.filter_date_enabled:
                dt1, dt2 = self.filter_date_tuple
                date_test = (dt1 <= snp_data.ts_as_datetime() <= dt2)
            else:
                date_test = True
        except AttributeError:
            date_test = True

        if not date_test:
            return False

        # note
        try:
            if self.filter_note_enabled:
                # ignore case, loose wild card match
                note_test = re.match(translate(self.filter_note_string.lower()),
                        snp_data.note.lower()) is not None
            else:
                note_test = True
        except AttributeError:
            note_test = True

        if not note_test:
            return False

        # user name test
        try:
            if self.filter_user_enabled:
                user_test = snp_data.user in self.filter_user_list
            else:
                user_test = True
        except AttributeError:
            user_test = True

        if not user_test:
            return False

        #
        return True


STS_PX_MAP = {
"nan": ":/sm-icons/unknown.png", # when first added into the list

"Not a powered device, SRF cavity, nor other blocking devices.": ":/sm-icons/unknown.png",
"Power is UNKNOWN": ":/sm-icons/unknown.png",
"Non-existing": ":/sm-icons/unknown.png", # the snapshot that does not saved last device state data (initial version of the data structure)

"Attenuator(s) IN": ":/sm-icons/off.png",
"Attenuator(s) OUT": ":/sm-icons/on.png",
"Attenuator device is IN": ":/sm-icons/off.png",
"Attenuator device is OUT": ":/sm-icons/on.png",

"Aperture device is OUT": ":/sm-icons/on.png",
"Aperture device is IN": ":/sm-icons/off.png",

"PPAC is OUT": ":/sm-icons/on.png",
"PPAC is IN": ":/sm-icons/off.png",

"Beam dump is OUT": ":/sm-icons/on.png",
"Beam dump is IN": ":/sm-icons/off.png",

"Energy loss detector is OUT": ":/sm-icons/on.png",
"Energy loss detector is IN": ":/sm-icons/off.png",

"Timing detector is OUT": ":/sm-icons/on.png",
"Timing detector is IN": ":/sm-icons/off.png",

"Slit is OUT": ":/sm-icons/on.png",
"Slit is IN": ":/sm-icons/off.png",

"DB2 viewer/degrader is OUT": ":/sm-icons/on.png",
"DB3 viewer/wedge is OUT": ":/sm-icons/on.png",

"Cavity phase is LOCKED": ":/sm-icons/on.png",
"Device is Locked": ":/sm-icons/on.png",
"Cavity phase is UNLOCKED": ":/sm-icons/off.png",
"Device is Unlocked": ":/sm-icons/off.png",

"Power is ON": ":/sm-icons/on.png",
"Power is OFF": ":/sm-icons/off.png",

"Chopper state: Invalid Input": ":/sm-icons/chp_invalid.png",
"Chopper state: Off": ":/sm-icons/chp_off.png",
"Chopper state: Blocking": ":/sm-icons/chp_blocking.png",
"Chopper state: Running": ":/sm-icons/chp_running.png",

"Ion source is active": ":/sm-icons/on.png",
"Ion source is inactive": ":/sm-icons/off.png",
}
def set_device_state_item(sts_str):
    """Return QStandardItem object based on the input device state string (*sts_str*).
    """
    item = QStandardItem('')
    sts_px_path = STS_PX_MAP.get(sts_str)
    if sts_px_path is not None:
        px = QPixmap(sts_px_path).scaled(PX_SIZE, PX_SIZE)
        item.setData(px, Qt.DecorationRole)
    else:
        item.setData(sts_str, Qt.DisplayRole)
    item.setData(sts_str, Qt.ToolTipRole)
    return item


TS_FMT = "%Y-%m-%dT%H:%M:%S.%f"
class SetLogMessager:
    """Message for set log.
    """
    DEFAULT_TEXT_COLOR = QColor("#343A40") # .bg-dark
    SKIP_SET_TEXT_COLOR = QColor("#DC3545") # .bg-danger
    SET_TEXT_COLOR = QColor("#17A2B8") # .bg-info
    def __init__(self, fld, ename: str, fname: str, old_set: float,
                 new_set: float, raw_set: float, set_op: str, set_fac: float,
                 idx_src: QModelIndex,
                 is_skip: bool = False, **kws):
        # fld: CaField object
        # if is_skip, do nothing, else set
        # Device {ename} [{fname}] is set from {old_set} to {new_set},
        # {new_set} = {raw_set} * ({new_set} / {raw_set}), or:
        # {new_set} = {raw_set} + ({new_set} - {raw_set})
        self._fld = fld
        self._ename = ename
        self._fname = fname
        self._old_set = old_set # current setting
        self._new_set = new_set # new setting (after scaling/shifting)
        self._raw_set = raw_set # saved setting (before scaling/shifting)
        self._set_op = set_op # '*' or '+'
        self._set_fac = set_fac # scaling factor or shifting amount
        self._idx_src = idx_src
        self._is_skip = is_skip
        self._ts = time.time()
        # revert
        self._is_revert = kws.get('is_revert', False)
        self._orig_ts = kws.get('orig_ts') # original timestamp when set is done.

    def is_skip_set(self):
        return self._is_skip

    def __str__(self):
        if self._is_skip:
            msg = "[{0}] [Skip] {1:<20s} [{2}] from {3} to {4} ({5} {6} {7}).".format(
                datetime.fromtimestamp(self._ts).strftime(TS_FMT),
                self._ename, self._fname, self._old_set, self._new_set, self._raw_set,
                self._set_op, self._set_fac)
        elif self._is_revert:
            msg = "[{0}] [Revert] {1:<20s} [{2}] from {3} to {4} -> [{5}].".format(
                datetime.fromtimestamp(self._ts).strftime(TS_FMT),
                self._ename, self._fname, self._old_set, self._new_set,
                datetime.fromtimestamp(self._orig_ts).strftime(TS_FMT))
        else:
            msg = "[{0}] [Set] {1:<20s} [{2}] from {3} to {4} ({5} {6} {7}).".format(
                datetime.fromtimestamp(self._ts).strftime(TS_FMT),
                self._ename, self._fname, self._old_set, self._new_set, self._raw_set,
                self._set_op, self._set_fac)
        return msg


class EffSetLogMsgContainer(QObject):
    """Container for keeping SetLogMessager objects.
    """

    # if contains items
    sigHasItems = pyqtSignal(bool)

    def __init__(self, parent):
        super(self.__class__, self).__init__()
        self.parent = parent
        self.clear()

    def append(self, o: SetLogMessager):
        self._items.append(o)
        self.sigHasItems.emit(True)

    def clear(self):
        self._items = []
        self.sigHasItems.emit(False)
