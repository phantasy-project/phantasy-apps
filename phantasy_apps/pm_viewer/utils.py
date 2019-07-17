#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import partial
import logging
import time

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem

from phantasy import epoch2human
from phantasy import Configuration
from phantasy import MachinePortal
from phantasy_apps.correlation_visualizer.utils import delayed_exec
from phantasy_apps.wire_scanner.device import Device
from phantasy_apps.utils import find_dconf

FMT = "{0:<12.6g}"
NEW_DURATION_IN_SEC = 300
LTIME_ATTR = 'LTIME'
LTIME_ATTR = 'XCEN' # for testing

_LOGGER = logging.getLogger(__name__)


class DataModel(QStandardItemModel):

    item_changed = pyqtSignal(QVariant)
    # status changed at i-th row, mark new flag
    status_changed = pyqtSignal(int)

    # kws: segment (LINAC), machine (FRIB)
    def __init__(self, parent, devices=None, fresh_duration=None, **kws):
        super(self.__class__, self).__init__(parent)
        self._v = parent
        self._fresh_duration = NEW_DURATION_IN_SEC if fresh_duration is \
                                    None else fresh_duration
        if devices is None:
            self._devices = init_devices(
                    machine=kws.get('machine', 'FRIB'),
                    segment=kws.get('segment', 'LINAC'))
        else:
            self._devices = devices

        self.header = self.h_name, self.h_dtype, \
                      self.h_x0, self.h_y0, self.h_xrms, self.h_yrms, \
                      self.h_cxy, self.h_ts = \
                ('Name', 'Type', 'XCEN', 'YCEN', 'XRMS', 'YRMS', 'CXY',
                 'Last Updated')
        self.ids = self.i_name, self.i_dtype, \
                   self.i_x0, self.i_y0, self.i_xrms, self.i_yrms, \
                   self.i_cxy, self.i_ts = \
                range(len(self.header))
        self.fnames = ('XCEN', 'YCEN', 'XRMS', 'YRMS', 'CXY', LTIME_ATTR)
        self.fname_ids = (self.i_x0, self.i_y0, self.i_xrms, self.i_yrms,
                          self.i_cxy, self.i_ts)

        self.item_changed.connect(self.update_item)
        self._pvs = [] # w/ cbs.

        # status pix
        self.px_current = QPixmap(":/icons/current.png")
        self.px_new = QPixmap(":/icons/new.png")
        self.status_changed.connect(self.mark_new_flag)

    def set_header(self):
        for i, s in zip(self.ids, self.header):
            self.setHeaderData(i, Qt.Horizontal, s)

    def set_data(self):
        for device in self._devices:
            elem = device.elem
            print("Setting {}...".format(elem.name))
            i_name = QStandardItem("{0:<20s}".format(device.name))
            i_name.elem = elem
            i_name.setCheckable(True)
            i_dtype = QStandardItem(
                '{0:<10s}'.format(device.dtype.upper()))
            i_x0 = QStandardItem(FMT.format(elem.XCEN))
            i_y0 = QStandardItem(FMT.format(elem.YCEN))
            i_xrms = QStandardItem(FMT.format(elem.XRMS))
            i_yrms = QStandardItem(FMT.format(elem.YRMS))
            i_cxy = QStandardItem(FMT.format(elem.CXY))
            i_ts = self.init_ts_item(elem.get_field(LTIME_ATTR))
            row = [i_name, i_dtype,
                   i_x0, i_y0, i_xrms, i_yrms, i_cxy, i_ts]
            [i.setEditable(False) for i in row]
            self.appendRow(row)

    def init_ts_item(self, fld):
        """Initialize last updated item.
        """
        ts = get_ts(fld, formated=False)
        ts_as_str = epoch2human(ts, fmt="%Y-%m-%d %H:%M:%S")
        i_ts = QStandardItem(ts_as_str)
        if time.time() - ts < NEW_DURATION_IN_SEC:
            px = self.px_new
        else:
            px = self.px_current
        i_ts.setIcon(QIcon(px))
        delayed_exec(lambda:i_ts.setIcon(QIcon(self.px_current)),
                     self._fresh_duration * 1000)
        return i_ts

    def set_model(self):
        self.set_data()
        self.set_header()
        self._v.setModel(self)
        self.__post_init_ui(self._v)
        self.set_cbs()

    def __post_init_ui(self, v):
        # view properties
        v.setStyleSheet("font-family: monospace;")
        v.setIconSize(QSize(28, 28))
        v.setAlternatingRowColors(True)
        try:
            # tree
            v.header().setStretchLastSection(True)
        except:
            # table
            v.horizontalHeader().setStretchLastSection(True)
        # v.setSortingEnabled(True)
        # self.sort(self.i_name, Qt.AscendingOrder)
        for i in self.ids:
            v.resizeColumnToContents(i)

        m = v.model()
        for i in range(self.rowCount()):
            for j in self.ids:
                idx = m.index(i, j)
                m.setData(idx, QSize(48, 48), Qt.SizeHintRole)

    def set_cbs(self):
        def _cb(row, col, fld, **kws):
            if col == self.i_ts:
                self.update_ts(row, col, fld)
            else:
                fmt = FMT
                item = QStandardItem(fmt.format(fld.value))
                item.setEditable(False)
                self.item_changed.emit((row, col, item))

        for i in range(self.rowCount()):
            item = self.item(i, 0)
            elem = item.elem
            for j, fname in zip(self.fname_ids, self.fnames):
                _it = self.item(i, j)
                fld = elem.get_field(fname)
                pv = fld.readback_pv[0]
                pv.add_callback(partial(_cb, i, j, fld))
                self._pvs.append(pv)

    def update_ts(self, row, col, fld):
        # update ts col
        msg = "Updating ({0},{1}) [{2}] with {3:.6g}..".format(
                row, col, fld.name, fld.value)
        _LOGGER.info(msg)
        print(msg)
        item = QStandardItem(get_ts(fld))
        item.setEditable(False)
        self.item_changed.emit((row, col, item))
        # new??
        self.status_changed.emit(row)

    @pyqtSlot(int)
    def mark_new_flag(self, row):
        self._i = self.item(row, self.i_ts)
        self._i.setIcon(QIcon(self.px_new))
        delayed_exec(lambda:self._i.setIcon(QIcon(self.px_current)),
                     self._fresh_duration * 1000)

    def update_item(self, p):
        self.setItem(*p)

    def get_selection(self,):
        r = []
        for i in range(self.rowCount()):
            item = self.item(i, self.i_name)
            if item.checkState() == Qt.Checked:
                r.append(item.elem)
        return r


def init_devices(conf_path=None, machine='FRIB', segment='LINAC'):
    """Initial list of wire-scanner Devices.
    """
    _LOGGER.info("Initial devices...")
    print("Initial devices...")
    mp = MachinePortal(machine=machine, segment=segment)
    pms = mp.get_elements(type='PM')
    pms_dict = {o.name: o for o in pms}

    if conf_path is None:
        conf_path = find_dconf('wire_scanner', 'ws.ini')
    conf = Configuration(conf_path)

    ks = [i for i in conf.keys() if i != 'DEFAULT' and i in pms_dict \
          and conf[i]['info'] == 'Installed']
    devices = [Device(pms_dict[k], conf) for k in ks]
    _LOGGER.info("Initial devices... done!")
    print("Initial devices... done!")
    return devices


def get_ts(fld, formated=True):
    """Return the timestamp for the most recent (approx) updating.
    """
    ts = fld.readback_pv[0].timestamp
    if formated:
        return epoch2human(ts, fmt="%Y-%m-%d %H:%M:%S")
    else:
        return ts
