#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from scipy.interpolate import griddata
import numpy.ma as ma

from phantasy_ui import BaseAppForm
from phantasy_apps.correlation_visualizer.utils import delayed_exec

from .ui.ui_plot3d import Ui_MainWindow


class Plot3dData(BaseAppForm, Ui_MainWindow):

    def __init__(self, parent=None):
        super(Plot3dData, self).__init__()
        self.setupUi(self)
        self._o = self.matplotlibimageWidget
        self._ax = self._o.axes
        self._parent = parent

        self.setAppVersion(parent._version)
        self.setAppTitle('{} - {}'.format(parent.getAppTitle(), 'Data'))
        self.setWindowTitle(parent.getAppTitle())

        self._norm_inten = False
        self.norm_chkbox.toggled.connect(self.on_norm_inten)
        delayed_exec(lambda: self.norm_chkbox.setChecked(True), 0)

    def on_norm_inten(self, f):
        self._norm_inten = f
        try:
            if f:
                self._o.update_image(self._raw_m / self._raw_m.max())
            else:
                self._o.update_image(self._raw_m)
        except:
            pass

    def set_interp(self, m, nx, ny):
        self._interp_method = m.lower()
        self._interp_nx = nx
        self._interp_ny = ny

    def set_xdata(self, data):
        self._xdata = data

    def set_ydata(self, data):
        self._ydata = data

    def set_zdata(self, data):
        self._zdata = data

    def plot_data(self):
        method = self._interp_method
        nx, ny = self._interp_nx, self._interp_ny
        x, y, z = self._xdata, self._ydata, self._zdata
        x0, x1, y0, y1 = x.min(), x.max(), y.min(), y.max()
        xx, yy = np.meshgrid(np.linspace(x0, x1, nx),
                             np.linspace(y0, y1, ny))
        m_arr = griddata((x, y), z, (xx, yy), method=method)
        m = ma.masked_invalid(m_arr)
        self._raw_m = m
        self._o.setXData(xx)
        self._o.setYData(yy)
        if self._norm_inten:
            self._o.update_image(m / m.max())
        else:
            self._o.update_image(m)

        # set xylabels and title
        xlbl = self._parent.xdata_cbb.currentText()
        ylbl = self._parent.ydata_cbb.currentText()
        tl = self._parent.zdata_cbb.currentText()
        self._o.setFigureXlabel(xlbl)
        self._o.setFigureYlabel(ylbl)
        self._o.setFigureTitle(tl)

    def closeEvent(self, e):
        pass
