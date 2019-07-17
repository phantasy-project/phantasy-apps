#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from phantasy_ui import BaseAppForm
from phantasy_apps.correlation_visualizer.utils import delayed_exec

from .ui.ui_plot_results import Ui_MainWindow


class PlotResults(BaseAppForm, Ui_MainWindow):

    def __init__(self, parent=None):
        super(PlotResults, self).__init__()
        self.setupUi(self)
        self._o = self.matplotlibimageWidget
        self._ax = self._o.axes
        self._parent = parent
        self._data = parent._data

        self.setAppVersion(parent._version)
        self.setAppTitle("{} - {}".format(parent.getAppTitle(), 'Results'))

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

    @property
    def results(self):
        return self._r

    @results.setter
    def results(self, r):
        self._r = r

    def plot_data(self):
        m = self._parent.matplotlibimageWidget.get_data()
        self._raw_m = m
        self._o.setXData(self._data.x_grid)
        self._o.setYData(self._data.xp_grid)
        if self._norm_inten:
            self._o.update_image(m / m.max())
        else:
            self._o.update_image(m)
        self._data.plot(m, results=self._r, ax=self._ax, image_on=False,
                profile_on=True, profile_opt={'lw': 1.5, 'color': 'w'},
                ellipse_on=True, ellipse_opt={'c': 'w', 'color': 'w'})
        # results
        self._show_results(self._r)
        # set xylabels
        self._o.setFigureXlabel("${}\,\mathrm{{[mm]}}$".format(self._u))
        self._o.setFigureYlabel("${}'\,\mathrm{{[mrad]}}$".format(self._u))

    def _show_results(self, r):
        for k in r:
            if k.startswith('alpha'):
                u = k[-1]
                break
        self._u = u

        ks = '{u}_cen,{u}p_cen,{u}_rms,{u}p_rms,alpha_{u},beta_{u},gamma_{u},emit_{u},emitn_{u},total_intensity'.format(u=u).split(',')
        names = ["{}<sub>{}</sub>".format(i, j) for (i, j) in
                 zip((u, u + "'", '&sigma;', '&sigma;', '&alpha;',
                     '&beta;', '&gamma;', '&epsilon;', '&epsilon;',
                     'Total Intensity'),
                     (0, 0, u, u + "'", u, u, u, u, u + '<sup>n</sup>', ''))]
        us = ("mm", "mrad", "mm", "mrad", "", "m", "m<sup>-1</sup>",
              "mm&middot;mrad", "mm&middot;mrad", "&mu;A")

        s =['<h5>{0:<3s} = {1:.6f} {2}<h5>'.format(n, r.get(k), ui) for (n, k, ui) in zip(names, ks, us)]
        self.textEdit.setHtml("<html>{}</html>".format(''.join(s)))

    def closeEvent(self, e):
        pass
