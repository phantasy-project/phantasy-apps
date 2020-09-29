#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import time
import shutil
from collections import OrderedDict
from fnmatch import translate
from functools import partial
from numpy.testing import assert_almost_equal

from PyQt5.QtCore import QSize
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtCore import QPersistentModelIndex
from PyQt5.QtCore import QItemSelectionModel
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QDesktopServices
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

FMT = "{0:.6g}"

X0 = 'x\N{SUBSCRIPT ZERO}'
X1 = 'x\N{SUBSCRIPT ONE}'
X2 = 'x\N{SUBSCRIPT TWO}'
DELTA = '\N{GREEK CAPITAL LETTER DELTA}'

COLUMN_NAMES1 = ['Device', 'Field']

COLUMN_NAMES2 = [
    'Setpoint({})'.format(X0),
    'Live Readback({})'.format(X1),
    'Live Setpoint({})'.format(X2),
    '{D}({x0},{x1})'.format(D=DELTA, x0=X0, x1=X1),
    '{D}({x0},{x2})'.format(D=DELTA, x0=X0, x2=X2),
    '{D}({x1},{x2})'.format(D=DELTA, x1=X1, x2=X2),
    'Tolerance', 'Writable', f'{X2}/{X0}'
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
                     'writable'] + VALID_FILTER_KEYS_NUM

BG_COLOR_GOLDEN_YES = "#FFDE03"
BG_COLOR_GOLDEN_NO = "#FFFFFF"
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

PX_SIZE = 24
ACT_BTN_CONF = {
    # op, (tt, text, px_path)
    'del': ('Delete this snapshot.', '', ":/sm-icons/delete.png"),
    'cast': ('Cast this snapshot', 'Cast', None),
    'save': ('Save the snapshot as a file, after that, all the row changes will be saved in place.',
             'Save As', None),
    'reveal': ('Reveal in File Explorer.', '', ':/sm-icons/openfolder.png'),
    'read': ('Oprn and read data file.', '', ':/sm-icons/readfile.png'),
}

DEFAULT_TS_PATH = find_dconf("settings_manager", "tolerance.json")
DEFAULT_MS_PATH = find_dconf("settings_manager", "settings.json")
DEFAULT_ELEM_PATH = find_dconf("settings_manager", "elements.json")


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

    # statistics for loaded items, PVs
    settings_sts = pyqtSignal(int, int, int)

    # delete checked items
    delete_selected_items = pyqtSignal()

    # delete checked items from original element list,
    # signal list of CaField objects.
    item_deletion_updated = pyqtSignal(list)

    def __init__(self, parent, flat_settings, **kws):
        # kw: ndigit, font
        super(self.__class__, self).__init__(parent)
        self._ndigit = kws.get('ndigit', None)
        self._font = kws.get('font', None)

        if self._ndigit is None:
            self.fmt = FMT
        else:
            self.fmt = '{{0:.{0}f}}'.format(self._ndigit)

        if self._font is None:
            self._font = QFontDatabase.systemFont(QFontDatabase.FixedFont)

        self._settings = flat_settings
        self._tv = parent
        # [obj(PV/CaField)] --> [items]
        self._fld_obj = []  # CaField
        self._fld_it = []   # list of items, [rd/sp]
        self._pv_obj = []   # PV
        self._pv_it = []    # list of items, [rd/sp]

        # header
        self.header = self.h_name, self.h_field, self.h_type, self.h_pos, \
                      self.h_val0, self.h_rd, self.h_cset, \
                      self.h_val0_rd, self.h_val0_cset, self.h_rd_cset, \
                      self.h_tol, self.h_writable, self.h_ratio_x20 \
            = COLUMN_NAMES
        self.ids = self.i_name, self.i_field, self.i_type, self.i_pos, \
                   self.i_val0, self.i_rd, self.i_cset, \
                   self.i_val0_rd, self.i_val0_cset, self.i_rd_cset, \
                   self.i_tol, self.i_writable, self.i_ratio_x20 \
            = range(len(self.header))

        #
        self.data_changed.connect(self.update_data)
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
        sppv_set = set()
        rdpv_set = set()
        ename_set = set()

        for elem, fname, fld, fval0 in self._settings:
            item_ename = QStandardItem(elem.name)
            # bgcolor = get_bg_color(elem.ename)

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
                it_sp_v = QStandardItem(self.fmt.format(sp_obj.value))
                it_rd_n = QStandardItem(rd_obj.pvname)
                it_rd_v = QStandardItem(self.fmt.format(rd_obj.value))

                [i.setEditable(False) for i in (it_sp_n, it_sp_v,
                                                it_rd_n, it_rd_v)]

                item_ename.appendRow(
                    (it_sp_n, QStandardItem('-'), QStandardItem('-'),
                     QStandardItem('-'), QStandardItem('-'),
                     QStandardItem('-'), it_sp_v)
                )
                item_ename.appendRow(
                    (it_rd_n, QStandardItem('-'), QStandardItem('-'),
                     QStandardItem('-'), QStandardItem('-'),
                     it_rd_v, QStandardItem('-'))
                )

                for o, item in zip((sp_obj, rd_obj), (it_sp_v, it_rd_v)):
                    # PHY and ENG fields share the same sp/rd pvs.
                    if o not in self._pv_obj:
                        self._pv_obj.append(o)
                        self._pv_it.append([item])  # put item instead of idx
                    else:
                        self._pv_it[self._pv_obj.index(o)].append(item)

                sppv_set.add(sp_obj.pvname)
                rdpv_set.add(rd_obj.pvname)

            #
            item_fname = QStandardItem(fname)
            item_val0 = QStandardItem(self.fmt.format(fval0))

            item_rd = QStandardItem(self.fmt.format(fld.value))
            item_cset = QStandardItem(self.fmt.format(elem.current_setting(fname)))

            self._fld_obj.append(fld)
            self._fld_it.append([item_rd, item_cset])

            row = [item_ename, item_fname]
            for i, f in enumerate(COLUMN_NAMES):
                if f in COLUMN_NAMES_ATTR:
                    v = getattr(elem, COLUMN_SFIELD_MAP[f])
                    if not isinstance(v, str):
                        v = '{0:.4f}'.format(v)
                    item = QStandardItem(v)
                    row.append(item)
            #
            row.extend([item_val0, item_rd, item_cset])
            x0 = float(item_val0.text())
            x1 = float(item_rd.text())
            x2 = float(item_cset.text())
            # dx01,02,12
            v_d01 = x0 - x1
            v_d02 = x0 - x2
            v_d12 = x1 - x2
            for v in (v_d01, v_d02, v_d12):
                item = QStandardItem(self.fmt.format(v))
                row.append(item)

            # editable
            for i in row:
                i.setEditable(False)

            # tolerance for dx12
            tol = fld.tolerance
            item_tol = QStandardItem(self.fmt.format(tol))
            item_tol.setEditable(True)
            row.append(item_tol)

            # writable
            write_access = fld.write_access
            item_wa = QStandardItem(str(write_access))
            item_wa.setEditable(False)
            row.append(item_wa)
            item_ename.setEnabled(write_access)

            # x2/x0
            item_ratio_x20 = QStandardItem(get_ratio_as_string(x2, x0, self.fmt))
            item_ratio_x20.setEditable(False)
            row.append(item_ratio_x20)

            if not write_access:
                for i in row:
                    i.setSelectable(False)
                    i.setData(QBrush(QColor(FG_NO_WRITE)), Qt.ForegroundRole)

            # fgcolor = get_fg_color(write_access)

            # color
            # for i in row:
                # i.setData(QBrush(QColor(bgcolor)), Qt.BackgroundRole)
                # i.setData(QBrush(QColor(fgcolor)), Qt.ForegroundRole)

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
        # hide columns: dx01, writable
        for i in (self.i_val0_rd, self.i_tol, self.i_writable,):
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
                font-size: 14pt;
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
        tv.expandAll()
        for i in self.ids:
            tv.resizeColumnToContents(i)
        tv.collapseAll()

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
            for pv in fobj.setpoint_pv + fobj.readback_pv:
                # ENH and PHY fields share the same sp/rd/ pvs.
                if pv not in self._pv_obj:
                    continue
                i = self._pv_obj.index(pv)
                self._pv_it.pop(i)
                self._pv_obj.pop(i)
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
        }
        self.filter_ftypes = ['ENG', 'PHY']
        # if True, filter checked items, otherwise show all items.
        self.filter_checked_enabled = False

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
        # ENG/PHY
        ftype = src_model.item(src_row, src_model.i_name).ftype
        # checked items
        if self.filter_checked_enabled:
            item_checked = is_item_checked(
                    src_model.item(src_row, src_model.i_name))
        else:
            item_checked = True

        idx = self.filter_col_index[filter_key]
        src_index = src_model.index(src_row, idx)
        var = src_index.data(Qt.DisplayRole)

        if not isinstance(var, str):
            var = self.fmt.format(var)

        # number keys
        if filter_key in VALID_FILTER_KEYS_NUM:
            var = float(var)
            filter_str = self.filterRegExp().pattern()
            try:
                t = eval(filter_str)
                # (x1, x2) or [x1, x2], or (x1, x2, x3) (only use x1, x2)
                if isinstance(t, (tuple, list)):
                    if len(t) > 1:
                        x1, x2 = t[0], t[1]
                        return ftype in self.filter_ftypes and \
                                item_checked and \
                                (var >= x1 and var <= x2)
                    elif len(t) == 1:
                        # (x1,) or [x1,]
                        return ftype in self.filter_ftypes and \
                                item_checked and \
                                var >= t[0]
                    else:
                        raise SyntaxError
                elif isinstance(t, (float, int)):
                        return ftype in self.filter_ftypes and \
                                item_checked and \
                                is_equal(var, t, 3)
                else:
                    raise SyntaxError
            except SyntaxError:
                return ftype in self.filter_ftypes and item_checked and \
                    re.match(translate(filter_str), str(var)) is not None
        else:
            # Qt >= 5.12
            # regex = self.filterRegularExpression()
            # return ftype in self.filter_ftypes and regex.match(var).hasMatch()

            # wildcardunix
            # regex = self.filterRegExp()
            # return ftype in self.filter_ftypes and regex.exactMatch(var)

            #
            return ftype in self.filter_ftypes and item_checked and \
                   re.match(self.filterRegExp().pattern(), var) is not None

    def get_selection(self):
        # Return a list of selected items, [(idx_src, settings)].
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

    def select_all(self):
        for i in range(self.rowCount()):
            idx = self.index(i, self.m_src.i_name)
            idx_src = self.mapToSource(idx)
            it_name_src = self.m_src.itemFromIndex(idx_src)
            if it_name_src.isEnabled():
                it_name_src.setCheckState(Qt.Checked)

    def invert_selection(self):
        for i in range(self.rowCount()):
            idx = self.index(i, self.m_src.i_name)
            idx_src = self.mapToSource(idx)
            it_name_src = self.m_src.itemFromIndex(idx_src)
            if not it_name_src.isEnabled():
                continue
            if not is_item_checked(it_name_src):
                it_name_src.setCheckState(Qt.Checked)
            else:
                it_name_src.setCheckState(Qt.Unchecked)


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
    settings = get_settings_from_element_list(elem_list, **kws)
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

    saveas_settings = pyqtSignal(SnapshotData)
    save_settings = pyqtSignal(SnapshotData)
    cast_settings = pyqtSignal(SnapshotData)
    del_settings = pyqtSignal(SnapshotData)

    def __init__(self,  parent, snp_list, **kws):
        super(self.__class__, self).__init__(parent)
        self._v = parent
        self._snp_list = snp_list
        # [
        #  SnapshotData,
        # ]
        self.casted_px = QPixmap(":/sm-icons/cast_connected.png").scaled(PX_SIZE, PX_SIZE)
        self.cast_px = QPixmap(":/sm-icons/cast.png").scaled(PX_SIZE, PX_SIZE)
        self.note_px = QPixmap(":/sm-icons/comment.png").scaled(PX_SIZE, PX_SIZE)
        self.tags_px = QPixmap(":/sm-icons/label.png").scaled(PX_SIZE, PX_SIZE)
        self.save_px = QPixmap(":/sm-icons/save-snp.png").scaled(PX_SIZE, PX_SIZE)
        self.saved_px = QPixmap(":/sm-icons/saved.png").scaled(PX_SIZE, PX_SIZE)

        self.header = self.h_ts, self.h_name, \
                      self.h_ion, self.h_ion_number, self.h_ion_mass, self.h_ion_charge, \
                      self.h_cast_status, self.h_cast, self.h_save_status, self.h_save, \
                      self.h_browse, self.h_read, self.h_user, \
                      self.h_is_golden, self.h_tags, self.h_delete, self.h_note \
                    = "Timestamp", "Name", "Ion", "Z", "A", "Q", "", "", "", "", \
                      "", "", "User", \
                      "", "Tags", "", "Note"
        self.ids = self.i_ts, self.i_name, \
                   self.i_ion, self.i_ion_number, self.i_ion_mass, self.i_ion_charge, \
                   self.i_cast_status, self.i_cast, self.i_save_status, self.i_save, \
                   self.i_browse, self.i_read, self.i_user, \
                   self.i_is_golden, self.i_tags, self.i_delete, self.i_note \
                 = range(len(self.header))

        self.itemChanged.connect(self.on_item_changed)

        #
        self._filter_list = []

    def set_filters(self, d):
        self._filter_list = [k for k, v in d.items() if v]

    def get_filters(self):
        return self._filter_list

    def set_model(self):
        self.set_data()
        _model = _SnpProxyModel(self)
        self._v.setModel(_model)
        self._post_init_ui(self._v)

    def set_data(self):
        data = {}
        for i in self._snp_list:
            data.setdefault(i.ts_as_date(), []).append(i)
        self._data = data

        for ts_date in sorted(data):
            #
            ts_data_list = data[ts_date]
            it_root = QStandardItem(ts_date)
            it_root.setEditable(False)

            for snp_data in ts_data_list:
                # ts
                it_ts = QStandardItem(snp_data.ts_as_str())
                it_ts.setEditable(False)
                it_ts.snp_data = snp_data
                # name
                it_name = QStandardItem(snp_data.name)
                it_name.setToolTip(snp_data.name)
                # ion
                it_ion = QStandardItem(snp_data.ion_name)
                it_ion.setEditable(False)
                # Z
                it_ion_number = QStandardItem(snp_data.ion_number)
                it_ion_number.setEditable(False)
                # A
                it_ion_mass = QStandardItem(snp_data.ion_mass)
                it_ion_mass.setEditable(False)
                # Q
                it_ion_charge = QStandardItem(snp_data.ion_charge)
                it_ion_charge.setEditable(False)
                # user
                it_user = QStandardItem(snp_data.username)
                it_user.setEditable(False)

                # tags
                tags_as_str = snp_data.tags_as_str()
                it_tags = QStandardItem(tags_as_str)
                it_tags.setData(self.tags_px, Qt.DecorationRole)
                if tags_as_str == '':
                    it_tags.setToolTip("Input strings seperated by comma as tags.")
                else:
                    it_tags.setToolTip(tags_as_str)
                # is golden?
                it_is_golden = QStandardItem()
                px = QPixmap(QSize(PX_SIZE, PX_SIZE))
                if snp_data.is_golden():
                    bgc = BG_COLOR_GOLDEN_YES
                    is_golden_tip = "Golden Setting!"
                else:
                    bgc = BG_COLOR_GOLDEN_NO
                    is_golden_tip = "Not Golden Setting!"
                px.fill(QColor(bgc))
                it_is_golden.setData(px, Qt.DecorationRole)
                it_is_golden.setToolTip(is_golden_tip)

                # note
                it_note = QStandardItem(snp_data.note)
                it_note.setData(self.note_px, Qt.DecorationRole)
                it_note.setToolTip(snp_data.note)
                # cast
                it_cast_status = QStandardItem()
                it_cast_status.setData(self.cast_px, Qt.DecorationRole)
                it_cast = QStandardItem('Cast')
                it_cast.setEditable(False)
                it_cast.setData("cast", Qt.UserRole + 1)
                # save
                it_save_status = QStandardItem()
                it_save = QStandardItem('Save')
                it_save.setEditable(False)
                it_save.setData("save", Qt.UserRole + 1)
                if snp_data.filepath is None:
                    it_save_status.setData(self.save_px, Qt.DecorationRole)
                else:
                    it_save_status.setData(self.saved_px, Qt.DecorationRole)
                    it_save_status.setToolTip(snp_data.filepath)
                # browse
                it_browse = QStandardItem('Browse')
                it_browse.setEditable(False)
                it_browse.setData("reveal", Qt.UserRole + 1)
                # read
                it_read = QStandardItem('Read')
                it_read.setEditable(False)
                it_read.setData("read", Qt.UserRole + 1)
                # delete
                it_delete = QStandardItem('Delete')
                it_delete.setEditable(False)
                it_delete.setData("del", Qt.UserRole + 1)
                row = (it_ts, it_name,
                       it_ion, it_ion_number, it_ion_mass, it_ion_charge,
                       it_cast_status, it_cast, it_save_status, it_save, it_browse, it_read,
                       it_user, it_is_golden, it_tags, it_delete, it_note,)
                it_root.appendRow(row)

            ph_list = []
            for i in range(len(self.header) - 1):
                it = QStandardItem('')
                it.setEditable(False)
                ph_list.append(it)
            self.appendRow((it_root, *ph_list))

    def on_item_changed(self, item):
        if item.parent() is None:
            return
        idx = item.index()
        s = item.text()
        i, j = idx.row(), idx.column()
        snp_data = self.itemFromIndex(self.index(i, self.i_ts, item.parent().index())).snp_data
        if j == self.i_note:
            snp_data.note = s
            item.setToolTip(s)
        elif j == self.i_name:
            snp_data.name = s
            item.setToolTip(s)
        elif j == self.i_tags:
            snp_data.tags = s
            item.setToolTip(s)
            it = self.itemFromIndex(self.index(i, self.i_is_golden, item.parent().index()))
            if snp_data.is_golden():
                bgc = BG_COLOR_GOLDEN_YES
                is_golden_tip = "Golden Setting!"
            else:
                bgc = BG_COLOR_GOLDEN_NO
                is_golden_tip = "Not Golden Setting!"
            px = QPixmap(QSize(PX_SIZE, PX_SIZE))
            px.fill(QColor(bgc))
            it.setData(px, Qt.DecorationRole)
            it.setToolTip(is_golden_tip)
        # in place save
        self.save_settings.emit(snp_data)

    @pyqtSlot()
    def on_browse_snp(self):
        # !! requires nautilus !!
        from PyQt5.QtCore import QProcess
        data = self.sender().property('data')
        p = QProcess(self)
        p.setArguments(["-s", data.filepath])
        p.setProgram("nautilus")
        p.startDetached()

    @pyqtSlot()
    def on_read_snp(self):
        data = self.sender().property('data')
        QDesktopServices.openUrl(QUrl(data.filepath))

    @pyqtSlot()
    def on_cast_snp(self):
        data = self.sender().property('data')
        self.cast_settings.emit(data)

    @pyqtSlot()
    def on_save_snp(self):
        data = self.sender().property('data')
        self.saveas_settings.emit(data)

    @pyqtSlot()
    def on_del_snp(self):
        data = self.sender().property('data')
        self.del_settings.emit(data)

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

            QTreeView::item:selected {
                border: 1px solid #567DBC;
                background-color: #D3D7CF;
            }

            QTreeView::item:selected:active{
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);
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

        v.expandAll()
        for i in (self.i_ts, self.i_name,
                  self.i_ion, self.i_ion_number, self.i_ion_mass, self.i_ion_charge,
                  self.i_cast_status, self.i_save_status,
                  self.i_browse, self.i_read, self.i_delete, self.i_user, self.i_is_golden,
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
            del data

    @pyqtSlot('QString', 'QString')
    def on_snp_saved(self, snp_name, filepath):
        # tag as saved for *snp_name*, update SnapshotData
        # enable locate and read.
        found = False
        for ii in range(self.rowCount()):
            ridx = self.index(ii, 0)
            if not self.hasChildren(ridx):
                continue
            for i in range(self.rowCount(ridx)):
                it0 = self.itemFromIndex(self.index(i, self.i_ts, ridx))
                it = self.itemFromIndex(self.index(i, self.i_name, ridx))
                if it.text() == snp_name:
                    found = True
                    idx = self.index(i, self.i_save_status, ridx)
                    self.setData(idx, self.saved_px, Qt.DecorationRole)
                    it0.snp_data.filepath = filepath
                    self.itemFromIndex(idx).setToolTip(filepath)
                    #for j in (self.i_browse, self.i_read):
                    #    idx = self.index(i, j, ridx)
                    #    w = self._v.indexWidget(idx)
                    #    # !! not fully understood !!
                    #    if w is None:
                    #        pass
                    #    else:
                    #        w.setEnabled(True)
                    break
            if found:
                break

    @pyqtSlot(SnapshotData)
    def on_snp_casted(self, snpdata):
        # updated casted dec role for ALL rows, hl casted row.
        snp_name = snpdata.name
        self._v.clearSelection()
        for ii in range(self.rowCount()):
            ridx = self.index(ii, 0)
            if not self.hasChildren(ridx):
                continue
            for i in range(self.rowCount(ridx)):
                if self.itemFromIndex(self.index(i, self.i_name, ridx)).text() == snp_name:
                    casted = True
                else:
                    casted = False
                idx = self.index(i, self.i_cast_status, ridx)
                self.set_casted(idx, casted)
                if casted:
                    self._v.scrollTo(idx)
                    self._v.selectionModel().select(idx,
                            QItemSelectionModel.Select | QItemSelectionModel.Rows)

    def clear_cast_status(self):
        for ii in range(self.rowCount()):
            ridx = self.index(ii, 0)
            if not self.hasChildren(ridx):
                continue
            for i in range(self.rowCount(ridx)):
                idx = self.index(i, self.i_cast, ridx)
                if self.data(idx, Qt.UserRole) == 'casted':
                    self.set_casted(idx, False)
                    break
            break

    def set_casted(self, idx, casted):
        if casted:
            self.setData(idx, self.casted_px, Qt.DecorationRole)
            self.setData(idx, 'casted', Qt.UserRole)
        else:
            self.setData(idx, self.cast_px, Qt.DecorationRole)
            self.setData(idx, 'not-casted', Qt.UserRole)

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
        # test:
        print(data.ts_as_str(), data.name)
        #
        self.sender().setProperty('data', data)
        if op == 'del':
            src_m.on_del_snp()
        elif op == 'cast':
            src_m.on_cast_snp()
        elif op == 'save':
            src_m.on_save_snp()
        elif op == 'reveal':
            src_m.on_browse_snp()
        elif op == 'read':
            src_m.on_read_snp()

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
        super(self.__class__, self).__init__()
        self.m_src = model
        self.setSourceModel(model)
        self.setRecursiveFilteringEnabled(True)

    def filterAcceptsRow(self, src_row, src_parent):
        m = self.sourceModel()
        filter_list = m.get_filters()
        if filter_list == []:
            return True
        ion_name = m.data(m.index(src_row, m.i_ion, src_parent))
        return ion_name in filter_list
