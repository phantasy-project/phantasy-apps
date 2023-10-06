#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot

import numpy as np
from numpy import ndarray
from matplotlib.patches import Polygon

from .data import draw_beam_ellipse_with_params
from .ui.ui_plot_region import Ui_Form


class PlotWidget(QWidget, Ui_Form):

    data_changed = pyqtSignal(ndarray)
    boundary_changed = pyqtSignal(ndarray)

    def __init__(self, parent=None):
        super(PlotWidget, self).__init__()
        self.setupUi(self)
        self._o1 = self.intensity_plot
        self._o2 = self.classification_plot
        self._ax1 = self._o1.axes
        self._ax2 = self._o2.axes
        self._parent = parent
        self._sf = self._parent._ellipse_sf
        self.data_changed.connect(self._o1.update_image)
        self.boundary_changed.connect(self._o2.update_image)

        # noise/signal ROI selection
        self._o1.selectedIndicesUpdated.connect(
                self.on_noise_signal_boundary_changed)

    def on_noise_signal_boundary_changed(self, ind, pts):
        self._update_plot(mode='manual', pts=pts, ind=ind)

    def plot(self):
        for o in (self._o1, self._o2):
            o.setXData(self._parent._data.x_grid)
            o.setYData(self._parent._data.xp_grid)

    @pyqtSlot(bool)
    def on_auto_boundary(self, f):
        # enable auto drawing ellipse or manually from lasso-tool.
        if f:
            self._parent.results_changed.connect(self.on_ellipse_updated)
            self._parent.size_factor_changed.connect(self.on_ellipse_size_updated)
        else:
            self._parent.results_changed.disconnect()
            self._parent.size_factor_changed.disconnect()

    @pyqtSlot(dict)
    def on_ellipse_updated(self, r):
        # updadte ellipse
        self._r = r
        self._update_plot()

    @pyqtSlot(float)
    def on_ellipse_size_updated(self, sf):
        # update ellipse size.
        self._sf = sf
        self._update_plot()

    def _update_plot(self, mode='auto', **kws):
        # mode: auto (from evaluated Twiss params), or manual (from drawing)
        xoy = self._parent._ems_device.xoy.lower()
        self._update_xylabels(xoy)
        self._ax1.patches.clear()
        if mode == 'auto':
            ellipse, _, _ = draw_beam_ellipse_with_params(
                              self._r, color='w', factor=self._sf,
                              ax=self._ax1, xoy=xoy)
            self._o1.update_figure()
            # update classification
            noise_signal_arr = self._parent._data.tag_noise_signal(
                                    ellipse=ellipse,
                                    factor=1.0)
        else:
            pts = kws.get('pts', None)
            ind = kws.get('ind', None)
            assert pts is not None
            assert ind is not None

            self._ax1.add_patch(Polygon(pts, ec='w', fill=False, alpha=0.4))
            self._o1.update_figure()

            arr = self._o1.get_data()
            shape = arr.shape
            arr = arr.flatten()
            z = np.ones(arr.size) * False
            z[np.ix_(ind)] = True
            z = z.reshape(shape)
            noise_signal_arr = z

        self.boundary_changed.emit(noise_signal_arr)
        self._parent._noise_signal_arr = noise_signal_arr
        # update noise diagram
        o = self._parent.noise_threshold_sbox
        o.valueChanged.emit(o.value())

    def _update_xylabels(self, u):
        xlbl = "${}\,\mathrm{{[mm]}}$".format(u)
        ylbl = "${}'\,\mathrm{{[mm]}}$".format(u)
        for o in (self._o1, self._o2):
            o.setFigureXlabel(xlbl)
            o.setFigureYlabel(ylbl)
