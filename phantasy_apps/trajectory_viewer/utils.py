# -*- coding: utf-8 -*-

import getpass
import os
import time
from collections import OrderedDict
from functools import partial

from PyQt5.QtCore import QItemSelectionModel
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QToolButton
from phantasy import MachinePortal
from phantasy import epoch2human
from phantasy_ui.widgets import is_item_checked

from phantasy_apps.correlation_visualizer.data import JSONDataSheet
from phantasy_apps.correlation_visualizer.scan import load_lattice
from .ui import details_icon

TS_FMT = "%Y-%m-%d %H:%M:%S"

try:
    basestring
except NameError:
    basestring = str

COLUMN_SFIELD_MAP_LITE = OrderedDict((
    ('Name', 'name'),
    ('Type', 'family'),
    ('Pos [m]', 'sb'),
    ('Length [m]', 'length'),
    ('Index', 'index'),
))

COLUMN_NAMES_LITE = list(COLUMN_SFIELD_MAP_LITE.keys())
SFIELD_NAMES_LITE = list(COLUMN_SFIELD_MAP_LITE.values())


class ElementListModel(QStandardItemModel):
    """Show list of elements.
    """
    # item selected
    elementSelected = pyqtSignal(OrderedDict)

    # n item selected
    nElementSelected = pyqtSignal(int)

    # fields wrt the selected element dtype
    fieldsSelected = pyqtSignal(list)

    def __init__(self, parent, mp, enames, **kws):
        QStandardItemModel.__init__(self, parent)
        self._v = parent
        self._mp = mp
        self._enames = enames

        # mapping of ename and element
        if self._mp is not None:
            self.name_elem_map = {i.name: i for i in self._mp.work_lattice_conf}
        else:
            self.name_elem_map = {}

        col_name_map = OrderedDict((
            ('Name', 'name'),
            ('Field', 'field'),
            ('', 'info'),
        ))
        self._col_name_map = col_name_map
        # header
        self.header = self.h_name, self.h_field, self.h_info = \
            list(col_name_map.keys())
        self.ids = self.i_name, self.i_field, self.i_info = \
            range(len(self.header))
        # set data, do not set field and info colmuns
        self.set_data()
        # set headers
        for i, s in zip(self.ids, self.header):
            self.setHeaderData(i, Qt.Horizontal, s)

        # selected elements: k: ename, v: list of field names.
        self._selected_elements = OrderedDict()
        self._selected_nelem = 0

    def set_model(self):
        if self._mp is None:
            return
        # set model
        self._v.setModel(self)
        self.set_columns()
        #
        self.__post_init_ui(self._v)
        #
        self.itemChanged.connect(self.on_item_changed)

    def set_data(self):
        # name w/ chkbox, field (cbb), detail (btn)
        v = self._v
        for ename in self._enames:
            row = []
            for f in self._col_name_map.values():
                if f == 'name':
                    item = QStandardItem(ename)
                    item.setCheckable(True)
                else:
                    item = QStandardItem('TBF')
                item.setEditable(False)
                row.append(item)
            self.appendRow(row)

    def set_columns(self):
        v = self._v
        for i, ename in enumerate(self._enames):
            # fields
            elem = self.name_elem_map[ename]
            cbb = QComboBox()
            cbb.addItems(elem.fields)
            if elem.family == 'BPM':
                cbb.addItem('X&Y')  # To all monitors
            v.setIndexWidget(self.index(i, self.i_field), cbb)
            elem_item = self.item(i, self.i_name)
            cbb.currentTextChanged.connect(
                partial(self.on_field_changed, elem_item))
            # info
            btn = QToolButton()
            btn.setIcon(QIcon(QPixmap(details_icon)))
            btn.setIconSize(QSize(24, 24))
            btn.setToolTip("Show details of {}.".format(ename))
            v.setIndexWidget(self.index(i, self.i_info), btn)
            btn.clicked.connect(partial(self.show_elem_info, elem))
        try:
            # emit list of element fields
            self.fieldsSelected.emit(elem.fields)
        except:
            print("No selected fields.")

    @pyqtSlot()
    def show_elem_info(self, elem):
        """Show element details.
        """
        from phantasy_ui.widgets.elementwidget import ElementWidget

        self.ew = ElementWidget(elem)
        self.ew.setWindowTitle(elem.name)
        self.ew.show()

    @pyqtSlot('QString')
    def on_field_changed(self, item, field):
        is_checked = is_item_checked(item)
        if is_checked:
            self._selected_elements.update({item.text(): str2list(field)})

        # print selected elements
        print("Field is updated: ", self._selected_elements)
        self.elementSelected.emit(self._selected_elements)

    def on_item_changed(self, item):
        idx = item.index()
        ename = item.text()
        if is_item_checked(item):
            print("Add {}".format(ename))
            fld_widget = self._v.indexWidget(self.index(idx.row(), self.i_field))
            fname = fld_widget.currentText()
            self._selected_elements.update({ename: str2list(fname)})
            self._selected_nelem += 1
        else:
            print("Remove {}".format(ename))
            self._selected_elements.pop(ename)
            self._selected_nelem -= 1

        # print selected elements
        print(self._selected_elements)
        self.elementSelected.emit(self._selected_elements)
        self.nElementSelected.emit(self._selected_nelem)

    def get_elements(self, category="all"):
        """Return a list of CaElement, if *category* is 'all', return all
        elements in this model, or 'selected' just return selected ones.
        """
        if category == 'all':
            names = self._enames
        else:
            names = self._selected_elements
        return [self.name_elem_map[i] for i in sorted(names, key=lambda i: i[-4:])]

    def __post_init_ui(self, tv):
        # view properties
        tv.setStyleSheet("font-family: monospace;")
        tv.setAlternatingRowColors(True)
        tv.header().setStretchLastSection(False)
        # tv.setSortingEnabled(True)
        for i in self.ids:
            tv.resizeColumnToContents(i)
        # tv.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # tv.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def select_item(self, ename):
        i = self._enames.index(ename)
        self.item(i, 0).setCheckState(Qt.Checked)

    def select_all_items(self):
        """Mark all items as checked.
        """
        for irow in range(self.rowCount()):
            item = self.item(irow, 0)
            item.setCheckState(Qt.Checked)

    def inverse_current_selection(self):
        """Inverse current selection.
        """
        for irow in range(self.rowCount()):
            item = self.item(irow, 0)
            state = item.checkState()
            if state == Qt.Unchecked:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)

    def change_field(self, s):
        """Change the field to *s* for all items.
        """
        for irow in range(self.rowCount()):
            item00 = self.item(irow, self.i_name)
            if is_item_checked(item00):
                cbb = self._v.indexWidget(self.index(irow, self.i_field))
                cbb.setCurrentText(s)

    def select_hl_item(self, it):
        self._v.selectionModel().select(it.index(),
                QItemSelectionModel.Select | QItemSelectionModel.Rows)
        self._v.scrollTo(it.index())


def str2list(fname):
    # 20190610: field mapping is required for non-BPMs.
    # Convert 'X' to ['X'], and 'X&Y' to ['X', 'Y']
    #if '&' in fname:
    #    return fname.split('&')
    #else:
    return [fname]


class TVDataSheet(JSONDataSheet):
    def __init__(self, path=None):
        super(self.__class__, self).__init__(path)

        if path is None:
            d = OrderedDict()
            d['info'] = {
                'user': getpass.getuser(),
                'created': epoch2human(time.time(), fmt=TS_FMT)
            }
            d['monitors'] = {}
            d['correctors'] = {}
            d['machine'] = ''
            d['segment'] = ''
            d['config'] = OrderedDict()
            d['mpl_config'] = {}
            self.update(d)


class MonitorReadingsDataSheet(JSONDataSheet):
    def __init__(self, path=None):
        super(self.__class__, self).__init__(path)

        if path is None:
            d = OrderedDict()
            d['user'] = getpass.getuser()
            d['created'] = epoch2human(time.time(), fmt=TS_FMT)
            d['readings'] = {}
            d['machine'] = ''
            d['segment'] = ''
            self.update(d)


def load_readings_sheet(filepath):
    """Load BPM readings from *filepath*, which defines
    MonitorReadingsDataSheet.
    """
    ds = MonitorReadingsDataSheet(filepath)
    machine, segment = ds['machine'], ds['segment']
    readings_conf = ds['readings']
    mp = MachinePortal(machine, segment)
    name_elem_map = {i.name: i for i in mp.work_lattice_conf}
    readings = []
    for ename, econf in readings_conf:
        readings.append(
            (name_elem_map[ename], econf))

    return readings
