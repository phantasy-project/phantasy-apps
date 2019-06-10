# -*- coding: utf-8 -*-

import getpass
import os
import time
from collections import OrderedDict
from functools import partial

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
from mpl4qt.widgets.utils import MatplotlibCurveWidgetSettings
from phantasy import MachinePortal
from phantasy import epoch2human

from phantasy_apps.correlation_visualizer.data import JSONDataSheet
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

DTYPE_HINT_MAP = {
    'BCM': 'Beam Current Monitor',
    'BEND': 'Magnetic Dipole',
    'BPM': 'Beam Position Monitor',
    'CAV': 'RF Cavity',
    'EBEND': 'Electric Dipole',
    'EQUAD': 'Electric Quadrupole',
    'FC': 'Faraday Cup',
    'HCOR': 'Horizontal Corrector',
    'HMR': 'Halo Ring Monitor',
    'IC': 'Ionization Chamber',
    'ND': 'Neutron Detector',
    'PM': 'Profile Monitor (Wire Scanner)',
    'QUAD': 'Magnetic Quadrupole',
    'SEXT': 'Sextupole',
    'SOL': 'Solenoid',
    'VCOR': 'Vertical Corrector',
}


def find_conf(filename=None):
    """Find configuration file (JSON) for matplotlibcurvewidget,
    searching the following locations:
    * ~/.phantasy/apps/mpl_settings_tv.json
    * /etc/phanasy/apps/mpl_settings_tv.json
    * package root location for this app/config/mpl_settings_tv.json
    """
    if filename is None:
        filename = 'mpl_settings_tv.json'
    home_conf = os.path.expanduser('~/.phantasy/apps/{}'.format(filename))
    sys_conf = '/etc/phantasy/apps/{}'.format(filename)
    if os.path.isfile(home_conf):
        return home_conf
    elif os.path.isfile(sys_conf):
        return sys_conf
    else:
        basedir = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(basedir, 'config/{}'.format(filename))


def apply_mplcurve_settings(mplcurveWidget, json_path=None, filename=None):
    """Apply JSON settings read from *json_path* to *mplcurveWidget*.

    Parameters
    ----------
    mplcurveWidget : MatplotlibCurveWidget
        Instance of MatplotlibCurveWidget.
    json_path : str
        Path of JSON settings file.
    """
    if json_path is None:
        json_path = find_conf(filename)
    s = MatplotlibCurveWidgetSettings(json_path)
    mplcurveWidget.apply_mpl_settings(s)


class LatticeDataModel(QStandardItemModel):
    """Lattice data model fot TV.
    """
    # items are selected, list of element names
    itemsSelected = pyqtSignal(list)

    # n selected items
    selectedItemsNumberChanged = pyqtSignal(int)

    def __init__(self, parent, mp=None, **kws):
        super(self.__class__, self).__init__(parent)
        self._tv = parent
        self._mp = mp

        self.header = self.h_name, self.h_type, self.h_pos, self.h_len, self.h_index = \
            COLUMN_NAMES_LITE
        self.ids = self.i_name, self.i_type, self.i_pos, self.i_len, self.i_index = \
            range(len(self.header))

        # selected items
        self._selected_items = []

        # item is changed, selected
        self.itemChanged.connect(self.on_item_changed)

        # keyword arguments
        self.kws = kws

    def set_model(self):
        self.set_data(**self.kws)
        for i, s in zip(self.ids, self.header):
            self.setHeaderData(i, Qt.Horizontal, s)
        self._tv.setModel(self)
        self.__post_init_ui(self._tv)

    def on_item_changed(self, item):
        index = item.index()
        ename = self.item(index.row(), index.column()).text()
        self._update_selection(ename, item)

    def _update_selection(self, ename, item):
        # update selected items
        if is_item_checked(item):
            self._selected_items.append(ename)
        else:
            self._selected_items.remove(ename)
        self.itemsSelected.emit(self._selected_items)
        self.selectedItemsNumberChanged.emit(len(self._selected_items))
        # print(self._selected_items)

    def set_data(self, **kws):
        dtypes = kws.get('dtypes', None)
        if dtypes is None:
            dtypes = self._mp.get_all_types()

        for elem in self._mp.work_lattice_conf:

            if elem.family not in dtypes:
                # print(elem.name, 'is skipped')
                continue
            row = []
            for i, f in enumerate(SFIELD_NAMES_LITE):
                v = getattr(elem, f)
                if i == self.i_index:
                    v = '{0:04d}'.format(v)
                if not isinstance(v, basestring):
                    v = '{0:.4f}'.format(v)
                item = QStandardItem(v)
                if i == 0:
                    item.setCheckable(True)
                    item.setCheckState(Qt.Checked)
                    self._update_selection(item.text(), item)
                item.setEditable(False)
                row.append(item)
            self.appendRow(row)

    def __post_init_ui(self, tv):
        # view properties
        tv.setStyleSheet("font-family: monospace;")
        tv.setAlternatingRowColors(True)
        tv.setSortingEnabled(True)
        for i in self.ids:
            tv.resizeColumnToContents(i)
        self.sort(self.i_index, Qt.AscendingOrder)
        tv.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        tv.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


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


def is_item_checked(item):
    return item.checkState() == Qt.Checked


def str2list(fname):
    # 20190610: field mapping is required for non-BPMs.
    # Convert 'X' to ['X'], and 'X&Y' to ['X', 'Y']
    #if '&' in fname:
    #    return fname.split('&')
    #else:
    return [fname]


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
