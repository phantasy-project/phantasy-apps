#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from collections import OrderedDict
from functools import partial

import numpy as np
from numpy.testing import assert_almost_equal

from phantasy import MachinePortal
from phantasy_apps.utils import find_dconf as _find_dconf

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QToolButton


def find_dconf():
    """Find parameter configuration file for wire-scanners.
    searching the following locations:
    * ~/.phantasy/ems.ini
    * /etc/phantasy/ems.ini
    * package location: apps/allison_scanner/config/ems.ini
    """
    return _find_dconf('allison_scanner', 'ems.ini')


def get_all_devices(machine="FRIB", segment="LEBT", type="EMS"):
    """Return dict of `(name, elem)`.
    """
    mp = MachinePortal(machine, segment)
    elems = mp.get_elements(type=type)
    r = [(i.name, i) for i in sorted(elems, key=lambda x:x.name[-4:])]
    return OrderedDict(r)


def point_in_ellipse(x, y, ellipse, factor=1.0):
    """Test if point `(x, y)` in *ellipse* or not.

    Parameters
    ----------
    x : float
        Point x coord.
    y : float
        Point y coord.
    ellipse :
        Ellipse patch.
    factor : float
        Increase/shrink the ellipse by applying coef onto both width and
        eight, default is 1.0.
    """
    x0, y0 = ellipse.center
    w, h = ellipse.width, ellipse.height
    theta = np.deg2rad(ellipse.angle)
    x -= x0
    y -= y0
    x1 = np.cos(theta) * x + np.sin(theta) * y
    y1 = -np.sin(theta) * x + np.cos(theta) * y
    return (x1 * x1 / w / w + y1 * y1 / h / h) <= 0.25 * factor * factor


def is_integer(a):
    """Test if float(a) == int(a).
    e.g. is_integer(4.0) returns True, while is_integer(4.01) returns False.
    """
    try:
        assert_almost_equal(a, int(a))
    except AssertionError:
        return False
    else:
        return True


class SettingsModel(QStandardItemModel):
    remove_settings = pyqtSignal(float)
    apply_settings = pyqtSignal(float)
    view_size = pyqtSignal(int, int)

    def __init__(self, parent, data, **kws):
        super(self.__class__, self).__init__(parent)
        self._v = parent
        self._data = data
        self.fmt = kws.get('fmt', '{0:>.2f}')

        # header
        self.header = self.h_idx, self.h_name, self.h_xoy, \
                      self.h_npoints, self.h_shape, \
                      self.h_pos_begin, self.h_pos_end, self.h_pos_step, \
                      self.h_volt_begin, self.h_volt_end, self.h_volt_step, \
                      self.h_apply, self.h_delete = \
            "", "Name", "X/Y", \
            "Points", "Shape", \
            "Pos Begin", "Pos End", "Pos Step", \
            "Volt Begin", "Volt End", "Volt Step", \
            "Apply", "Delete"
        self.ids = self.i_idx, self.i_name, self.i_xoy, \
                   self.i_npoints, self.i_shape, \
                   self.i_pos_begin, self.i_pos_end, self.i_pos_step, \
                   self.i_volt_begin, self.i_volt_end, self.i_volt_step, \
                   self.i_apply, self.i_delete = \
            range(len(self.header))
        #
        self.set_data()
        #
        for i, s in zip(self.ids, self.header):
            self.setHeaderData(i, Qt.Horizontal, s)

    def set_model(self):
        # set model
        self._v.setModel(self)
        #
        self._set_actions()
        self.__post_init_ui(self._v)
        #

    def set_data(self):
        for i, d in enumerate(self._data):
            ts = d['timestamp']
            name = d['name']
            xoy = d['xoy']
            pb, pe, ps = d['pos_begin'], d['pos_end'], d['pos_step']
            vb, ve, vs = d['volt_begin'], d['volt_end'], d['volt_step']

            row = []
            item_idx = QStandardItem('{0:02d}'.format(i + 1))
            item_name = QStandardItem(name)
            item_xoy = QStandardItem(xoy)

            nx = int((pe - pb) / ps + 1)
            ny = int((ve - vb) / vs + 1)
            item_nsize = QStandardItem('{0:d}'.format(nx * ny))
            item_shape = QStandardItem('{0:d}{2}{1:d}'.format(ny, nx, u"\u00D7"))

            item_pb = QStandardItem(self.fmt.format(pb))
            item_pe = QStandardItem(self.fmt.format(pe))
            item_ps = QStandardItem(self.fmt.format(ps))

            item_vb = QStandardItem(self.fmt.format(vb))
            item_ve = QStandardItem(self.fmt.format(ve))
            item_vs = QStandardItem(self.fmt.format(vs))

            item_apply = QStandardItem('')
            item_delete = QStandardItem('')

            for item in (item_idx, item_name, item_xoy,
                         item_nsize, item_shape,
                         item_pb, item_pe, item_ps,
                         item_vb, item_ve, item_vs,
                         item_apply, item_delete,):
                if i == 0:
                    item_idx.setBackground(QBrush(QColor('#F57900')))
                    item_idx.setForeground(QBrush(QColor('#FFFFFF')))
                item.setEditable(False)
                row.append(item)
            self.appendRow(row)

    def _set_actions(self):
        v = self._v
        for i, d in enumerate(self._data):
            btn1 = QToolButton()
            btn1.setAutoRaise(True)
            btn1.setIcon(QIcon(QPixmap(":/icons/apply.png")))
            btn1.setToolTip("Click to apply current settings.")
            idx1 = self.index(i, self.i_apply)
            v.setIndexWidget(idx1, btn1)
            btn1.clicked.connect(partial(self.on_apply, d['timestamp']))

            btn2 = QToolButton()
            btn2.setAutoRaise(True)
            btn2.setIcon(QIcon(QPixmap(":/icons/delete-as.png")))
            btn2.setToolTip("Click to remove current settings.")
            idx2 = self.index(i, self.i_delete)
            v.setIndexWidget(idx2, btn2)
            btn2.clicked.connect(partial(self.on_delete, d['timestamp']))
            if i == 0:
                btn2.setEnabled(False)

    @pyqtSlot()
    def on_apply(self, ts):
        self.apply_settings.emit(ts)

    @pyqtSlot()
    def on_delete(self, ts):
        self.remove_settings.emit(ts)

    def __post_init_ui(self, tv):
        # view properties
        tv.setStyleSheet("font-family: monospace;")
        tv.setAlternatingRowColors(True)
        # tv.setSortingEnabled(True)
        tv.header().setStretchLastSection(False)
        w = 0
        for i in self.ids:
            tv.resizeColumnToContents(i)
            w += tv.columnWidth(i)
        h = 0
        for i in range(len(self._data)):
            h += tv.rowHeight(self.item(i, 0).index())
        # self.sort(self.i_idx, Qt.AscendingOrder)
        # tv.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # tv.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view_size.emit(w, h)
