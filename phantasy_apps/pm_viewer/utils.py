#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QSize, pyqtSignal, QVariant, pyqtSlot
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem, QPixmap, QIcon

from phantasy_apps.wire_scanner.device import Device
from phantasy import Configuration, MachinePortal
from phantasy_apps.utils import find_dconf
from phantasy_apps.correlation_visualizer.utils import delayed_exec
from epics import caget, PV
from functools import partial
from phantasy import epoch2human

FMT = "{0:<12.6g}"


class DataModel(QStandardItemModel):

    item_changed = pyqtSignal(QVariant)
    # status changed at i-th row, mark new flag
    status_changed = pyqtSignal(int)

    # kws: segment (LINAC), machine (FRIB)
    def __init__(self, parent, devices=None, **kws):
        super(self.__class__, self).__init__(parent)
        self._v = parent
        if devices is None:
            self._devices = init_devices(
                    machine=kws.get('machine', 'FRIB'),
                    segment=kws.get('segment', 'LEBT'))
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
        self.fnames = ('XCEN', 'YCEN', 'XRMS', 'YRMS', 'CXY')
        self.fname_ids = (self.i_x0, self.i_y0, self.i_xrms, self.i_yrms,
                          self.i_cxy)

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
            i_ts = QStandardItem(get_ts(elem.get_field('XCEN')))
            i_ts.setIcon(QIcon(self.px_current))
            row = [i_name, i_dtype,
                   i_x0, i_y0, i_xrms, i_yrms, i_cxy, i_ts]
            [i.setEditable(False) for i in row]
            self.appendRow(row)

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
                fmt = "{}"
            else:
                fmt = FMT
            item = QStandardItem(fmt.format(fld.value))
            item.setEditable(False)
            self.item_changed.emit((row, col, item))
            self.update_ts(row, self.i_ts, fld)

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
        print("Updating...", row, col, fld)
        ts = get_ts(fld)
        item = QStandardItem(ts)
        item.setEditable(False)
        self.item_changed.emit((row, col, item))
        # new??
        self.status_changed.emit(row)

    @pyqtSlot(int)
    def mark_new_flag(self, row):
        self._i = self.item(row, self.i_ts)
        self._i.setIcon(QIcon(self.px_new))
        delayed_exec(lambda:self._i.setIcon(QIcon(self.px_current)), 120000)

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
    print("Initial devices...done")
    return devices


def get_ts(fld):
    """Return the timestamp for the most recent (approx) updating.
    """
    ts = fld.setpoint_pv[0].timestamp
    return epoch2human(ts, fmt="%Y-%m-%dT%H:%M:%S")
