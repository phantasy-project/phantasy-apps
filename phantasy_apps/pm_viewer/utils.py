#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QSize, pyqtSignal, QVariant
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem

from phantasy_apps.wire_scanner.device import Device
from phantasy import Configuration, MachinePortal
from phantasy_apps.utils import find_dconf


class DataModel(QStandardItemModel):

    itemSelected = pyqtSignal('QString')

    def __init__(self, parent, devices=None, **kws):
        super(self.__class__, self).__init__(parent)
        self._v = parent
        if devices is None:
            self._devices = init_devices(
                    segment=kws.get('segment', 'LEBT'))
        else:
            self._devices = devices

        self.header = self.h_name, self.h_dtype, self.h_info, \
                      self.h_x0, self.h_y0, self.h_xrms, self.h_yrms, \
                      self.h_cxy, self.h_ts = \
                ('Name', 'Type', 'Info', 'x0', 'y0', 'xrms', 'yrms', 'cxy',
                 'Last Updated')
        self.ids = self.i_name, self.i_dtype, self.i_info, \
                   self.i_x0, self.i_y0, self.i_xrms, self.i_yrms, \
                   self.i_cxy, self.i_ts = \
                range(len(self.header))

        self._selected_items = set()

    def set_header(self):
        for i, s in zip(self.ids, self.header):
            self.setHeaderData(i, Qt.Horizontal, s)

    def set_data(self):
        for device in self._devices:
            elem = device.elem
            i_name = QStandardItem(device.name)
            i_name.setProperty('elem', elem)
            i_name.setCheckable(True)
            i_dtype = QStandardItem(device.dtype)
            i_info = QStandardItem(device.misc_info)
            i_x0 = QStandardItem(elem.XCEN)
            i_y0 = QStandardItem(elem.YCEN)
            i_xrms = QStandardItem(elem.XRMS)
            i_yrms = QStandardItem(elem.YRMS)
            i_cxy = QStandardItem(elem.CXY)
            i_ts = QStandardItem('TS')
            row = [i0, i1, i2, i_x0, i_y0, i_xrms, i_yrms, i_cxy, i_ts]
            [i.setEditable(False) for i in row]
            self.appendRow(row)

    def set_model(self):
        self.set_data()
        self.set_header()
        self._v.setModel(self)
        self.__post_init_ui(self._v)
        # model item is changed: line is selected (first item is checked)
        self.itemChanged.connect(self.on_item_changed)

    def __post_init_ui(self, v):
        # view properties
        v.setStyleSheet("font-family: monospace;")
        v.setIconSize(QSize(24, 24))
        v.setAlternatingRowColors(True)
        try:
            # tree
            v.header().setStretchLastSection(True)
        except:
            # table
            v.horizontalHeader().setStretchLastSection(True)
        v.setSortingEnabled(True)
        self.sort(self.i_name, Qt.AscendingOrder)
        for i in self.ids:
            v.resizeColumnToContents(i)

    def on_item_changed(self, item):
        # slot
        # emit: ename
        ename = item.text()
        if ename not in self._selected_items:
            self._selected_items.add(ename)
        else:
            self._selected_items.remove(ename)
        self.itemSelected.emit(ename)


def init_devices(conf_path=None, machine='FRIB', segment='LINAC'):
    """Initial list of wire-scanner Devices.
    """
    mp = MachinePortal(machine=machine, segment=segment)
    pms = mp.get_elements(type='PM')
    pms_dict = {o.name: o for o in pms}

    if conf_path is None:
        conf_path = find_dconf('wire_scanner', 'ws.ini')
    conf = Configuration(conf_path)

    ks = [i for i in conf.keys() if i != 'DEFAULT' and i in pms_dict]
    devices = [Device(pms_dict[k], conf) for k in ks]

    return devices
