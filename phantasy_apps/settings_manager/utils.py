#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import time
from collections import OrderedDict
from fnmatch import translate
from functools import partial
from numpy.testing import assert_almost_equal

from PyQt5.QtCore import QSize
from PyQt5.QtCore import QSortFilterProxyModel
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
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QSizePolicy
from phantasy import get_settings_from_element_list
from phantasy_ui.widgets import is_item_checked
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
    'Tolerance', 'Writable'
]
COLUMN_SFIELD_MAP = OrderedDict((
    ('Type', 'family'),
    ('Pos [m]', 'sb'),
))
COLUMN_NAMES_ATTR = list(COLUMN_SFIELD_MAP.keys())
SFIELD_NAMES_ATTR = list(COLUMN_SFIELD_MAP.values())

COLUMN_NAMES = COLUMN_NAMES1 + COLUMN_NAMES_ATTR + COLUMN_NAMES2

VALID_FILTER_KEYS_NUM = ['x0', 'x1', 'x2', 'dx01', 'dx02', 'dx12',
                         'pos', 'tolerance']
VALID_FILTER_KEYS = ['device', 'field', 'type',
                     'writable'] + VALID_FILTER_KEYS_NUM

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

    # reset item0 icon if applied
    reset_icon = pyqtSignal()

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
                      self.h_tol, self.h_writable \
            = COLUMN_NAMES
        self.ids = self.i_name, self.i_field, self.i_type, self.i_pos, \
                   self.i_val0, self.i_rd, self.i_cset, \
                   self.i_val0_rd, self.i_val0_cset, self.i_rd_cset, \
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
            # dx01,02,12
            v_d01 = float(item_val0.text()) - float(item_rd.text())
            v_d02 = float(item_val0.text()) - float(item_cset.text())
            v_d12 = float(item_rd.text()) - float(item_cset.text())
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
        # hide columns: writable (11)
        self._tv.setColumnHidden(11, True)
        #
        self.__post_init_ui()

    def __post_init_ui(self):
        # set headers
        tv = self._tv
        tv.setSortingEnabled(True)
        for i, s in zip(self.ids, self.header):
            self.setHeaderData(i, Qt.Horizontal, s)
        tv.model().sort(self.i_pos)

        #
        self.style_view(font=self._font)
        self.fit_view()
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
    def reset_setdone_icons(self):
        # reset set done icons.
        for i in range(self.rowCount()):
            self.setData(self.index(i, self.i_name), QPixmap(), Qt.DecorationRole)

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
    ts_confpath = os.path.join(confdir, 'tolerance.json')
    ms_confpath = os.path.join(confdir, 'settings.json')
    elem_confpath = os.path.join(confdir, 'elements.json')
    return confdir, ts_confpath, ms_confpath, elem_confpath


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


class SnapshotDataModel(QStandardItemModel):

    save_settings = pyqtSignal(SnapshotData)
    cast_settings = pyqtSignal(SnapshotData)

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
        self.save_px = QPixmap(":/sm-icons/save-snp.png").scaled(PX_SIZE, PX_SIZE)
        self.saved_px = QPixmap(":/sm-icons/saved.png").scaled(PX_SIZE, PX_SIZE)

        self.header = self.h_ts, self.h_name, \
                      self.h_ion, self.h_ion_number, self.h_ion_mass, self.h_ion_charge, \
                      self.h_cast, self.h_save, self.h_browse, self.h_read, self.h_user, self.h_note \
                    = "Timestamp", "Name", "Ion", "Z", "A", "Q", "Cast", "Save", "", "", "User", "Note"
        self.ids = self.i_ts, self.i_name, \
                      self.i_ion, self.i_ion_number, self.i_ion_mass, self.i_ion_charge, \
                   self.i_cast, self.i_save, self.i_browse, self.i_read, self.i_user, self.i_note \
                 = range(len(self.header))
        self.set_data()

        self.itemChanged.connect(self.on_item_changed)

    def set_model(self):
        self._v.setModel(self)
        self.set_actions()
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
                it_name.snp_data = snp_data
                it_name.setToolTip(snp_data.name)
                # ion
                it_ion = QStandardItem(snp_data.ion_name)
                # Z
                it_ion_number = QStandardItem(snp_data.ion_number)
                # A
                it_ion_mass = QStandardItem(snp_data.ion_mass)
                # Q
                it_ion_charge = QStandardItem(snp_data.ion_charge)
                # user
                it_user = QStandardItem(snp_data.username)
                it_user.setEditable(False)
                # note
                it_note = QStandardItem(snp_data.note)
                it_note.setData(self.note_px, Qt.DecorationRole)
                it_note.setToolTip(snp_data.note)
                # cast
                it_cast = QStandardItem('Cast')
                it_cast.setEditable(False)
                it_cast.setData(self.cast_px, Qt.DecorationRole)
                # save
                it_save = QStandardItem('Save')
                it_save.setEditable(False)
                if snp_data.filepath is None:
                    it_save.setData(self.save_px, Qt.DecorationRole)
                else:
                    it_save.setData(self.saved_px, Qt.DecorationRole)
                    it_save.setToolTip(snp_data.filepath)
                # browse
                it_browse = QStandardItem('Browse')
                it_browse.setEditable(False)
                # read
                it_read = QStandardItem('Read')
                it_read.setEditable(False)
                it_root.appendRow((it_ts, it_name,
                                   it_ion, it_ion_number, it_ion_mass, it_ion_charge,
                                   it_cast, it_save, it_browse, it_read,
                                   it_user, it_note,))

            ph_list = []
            for i in range(11):
                it = QStandardItem('')
                it.setEditable(False)
                ph_list.append(it)
            self.appendRow((it_root, *ph_list))

    def set_actions(self):
        for ii in range(self.rowCount()):
            ridx = self.index(ii, 0)
            if self.hasChildren(ridx):
                for i in range(self.rowCount(ridx)):
                    snp_data = self.itemFromIndex(self.index(i, 0, ridx)).snp_data
                    # cast
                    cast_btn = QToolButton(self._v)
                    cast_btn.setProperty('data', snp_data)
                    cast_btn.setText("Cast")
                    cast_btn.setToolTip("Cast current snapshot.")
                    cast_btn.setAutoRaise(False)
                    cast_btn.clicked.connect(self.on_cast_snp)
                    self._v.setIndexWidget(self.index(i, self.i_cast, ridx), cast_btn)
                    # save
                    save_btn = QToolButton(self._v)
                    save_btn.setText("Save")
                    save_btn.setProperty('data', snp_data)
                    save_btn.setToolTip("Save current snapshot as a file.")
                    save_btn.setAutoRaise(False)
                    save_btn.clicked.connect(self.on_save_snp)
                    self._v.setIndexWidget(self.index(i, self.i_save, ridx), save_btn)
                    # browse
                    browse_btn = QToolButton(self._v)
                    browse_btn.setDisabled(snp_data.filepath is None)
                    browse_btn.setIcon(QIcon(QPixmap(":/sm-icons/openfolder.png")))
                    browse_btn.setIconSize(QSize(PX_SIZE, PX_SIZE))
                    browse_btn.setText("Browse")
                    browse_btn.setProperty('data', snp_data)
                    browse_btn.setToolTip("Locate the saved folder.")
                    browse_btn.setAutoRaise(False)
                    browse_btn.clicked.connect(self.on_browse_snp)
                    self._v.setIndexWidget(self.index(i, self.i_browse, ridx), browse_btn)
                    # read file
                    read_btn = QToolButton(self._v)
                    read_btn.setDisabled(snp_data.filepath is None)
                    read_btn.setIcon(QIcon(QPixmap(":/sm-icons/readfile.png")))
                    read_btn.setIconSize(QSize(PX_SIZE, PX_SIZE))
                    read_btn.setText("read")
                    read_btn.setProperty('data', snp_data)
                    read_btn.setToolTip("Open and read saved file.")
                    read_btn.setAutoRaise(False)
                    read_btn.clicked.connect(self.on_read_snp)
                    self._v.setIndexWidget(self.index(i, self.i_read, ridx), read_btn)

    def on_item_changed(self, item):
        idx = item.index()
        s = item.text()
        i, j = idx.row(), idx.column()
        snp_data = self.itemFromIndex(self.index(i, 0, item.parent().index())).snp_data
        if j == self.i_note:
            snp_data.note = s
            item.setToolTip(s)
        elif j == self.i_name:
            snp_data.name = s
            item.setToolTip(s)

    @pyqtSlot()
    def on_browse_snp(self):
        data = self.sender().property('data')
        QDesktopServices.openUrl(QUrl(os.path.dirname(data.filepath)))

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
        data.update_meta()
        self.save_settings.emit(data)

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
        v.setAlternatingRowColors(True)
        v.header().setStretchLastSection(True)

        v.expandAll()
        for i in (self.i_ts, self.i_name,
                  self.i_ion, self.i_ion_number, self.i_ion_mass, self.i_ion_charge,
                  self.i_browse, self.i_read, self.i_user):
            v.resizeColumnToContents(i)
        v.collapseAll()

        # hide name col
        v.setColumnHidden(self.i_name, True)

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
                it = self.itemFromIndex(self.index(i, self.i_name, ridx))
                if it.text() == snp_name:
                    found = True
                    idx = self.index(i, self.i_save, ridx)
                    self.setData(idx, self.saved_px, Qt.DecorationRole)
                    it.snp_data.filepath = filepath
                    self.itemFromIndex(idx).setToolTip(filepath)
                    for j in (self.i_browse, self.i_read):
                        idx = self.index(i, j, ridx)
                        self._v.indexWidget(idx).setEnabled(True)
                    break
            if found:
                break

    @pyqtSlot('QString')
    def on_snp_casted(self, snp_name):
        # updated casted dec role for ALL rows, hl casted row.
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
                idx = self.index(i, self.i_cast, ridx)
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
