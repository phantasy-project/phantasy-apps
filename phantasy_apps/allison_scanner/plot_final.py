#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMessageBox

from phantasy_ui import BaseAppForm
from phantasy_ui import delayed_exec
from phantasy_ui.widgets.beam_species_displayWidget import SRC_NAME_MAP

from .ui.ui_plot_results import Ui_MainWindow


class PlotResults(BaseAppForm, Ui_MainWindow):

    def __init__(self, elem, auto_push, is_file_load, parent=None):
        super(PlotResults, self).__init__()
        self.setupUi(self)
        self._o = self.matplotlibimageWidget
        self._r = None
        self._ax = self._o.axes
        self._parent = parent
        self._data = parent._data
        self._elem = elem
        self._auto_push = auto_push
        self._last_loading = is_file_load

        self.setAppVersion(parent._version)
        self.setAppTitle("{} - {}".format(parent.getAppTitle(), 'Results'))

        self.push_to_pv_btn.clicked.connect(self.on_push_results)
        self._norm_inten = False
        self.norm_chkbox.toggled.connect(self.on_norm_inten)
        delayed_exec(lambda: self.norm_chkbox.setChecked(True), 0)
        self.resize(1200, 800)

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

        u, ks, fs = self._get_keys(self._r)
        # results
        self._show_results(self._r, u, ks)
        # set xylabels
        self._o.setFigureXlabel("${}\,\mathrm{{[mm]}}$".format(u))
        self._o.setFigureYlabel("${}'\,\mathrm{{[mrad]}}$".format(u))
        # push results to PVs
        if self._auto_push and not self._last_loading:
            self._push_results(self._r, u, ks, fs)

    def _get_keys(self, r):
        for k in r:
            if k.startswith('alpha'):
                u = k[-1]
                break
        U = u.upper()
        ks = f'{u}_cen,{u}p_cen,{u}_rms,{u}p_rms,alpha_{u},beta_{u},gamma_{u},emit_{u},emitn_{u},total_intensity'.split(',')
        fs = f'{U}CEN,{U}PCEN,{U}RMS,{U}PRMS,{U}ALPHA,{U}BETA,{U}GAMMA,{U}EMIT,{U}NEMIT,{U}INTEN'.split(',')
        return u, ks, fs

    def on_push_results(self):
        if self._r is None:
            QMessageBox.warning(self, "Push Results",
                    "No data to push to PVs.", QMessageBox.Ok)
        else:
            u, ks, fs = self._get_keys(self._r)
            self._push_results(self._r, u, ks, fs)
            QMessageBox.information(self, "Push Results",
                    "Pushed results to PVs.", QMessageBox.Ok)

    def _push_results(self, r, u, ks, fs):
        # push results to PVs.
        for k, f in zip(ks, fs):
            pv = self._elem.pv(field=f, handle='setpoint')[0]
            val = r.get(k)
            setattr(self._elem, f, val)
            print(f"Set field {f:<6s} ({pv:<30s}) with {val}")

    def _get_isrc_name(self):
        """Get the name for ion source name either for live mode or offline mode.
        """
        return SRC_NAME_MAP[self._parent.beamSpeciesDisplayWidget.get_full_info()[0]]

    def _post_beam_info(self):
        """Post beam info.
        """
        # beam info: name, Q, A, Z, Q/A, beam energy, voltage to angle
        n, q, a, ek =  self._parent._get_ion_info("as-is")
        isrc_name = f'<h1 style=" margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:x-large; font-weight:600; color:#dc3545; vertical-align:super;">{a}</span><span style=" font-size:x-large; font-weight:600;">{n}</span><span style=" font-size:x-large; font-weight:600; color:#ffc107; vertical-align:super;">{q}+</span></h1>'
        s = f'<h4>Ion Source: {self._get_isrc_name()}</h4><span>{isrc_name}</span>'
        s += '<h4>{0:s}: {1:.3f}</h4>'.format("Q/A", q/a)
        s += '<h4>{0:s}: {1:.6g} eV</h4>'.format("Ion Energy", ek)
        s += '<h4>{0:s}: {1:.3f} mrad/kV</h4>'.format("Volt2Angle", self._parent._model.voltage_to_divergence(1000)[1] * 1000)
        self.beam_textEdit.setHtml(f"<html>{s}</html>")

    def _show_results(self, r, u, ks):
        # post the beam info along with the results.
        self._post_beam_info()
        #
        names = [f"{i}<sub>{j}</sub>" for (i, j) in
                 zip((u, u + "'", '&sigma;', '&sigma;', '&alpha;',
                     '&beta;', '&gamma;', '&epsilon;', '&epsilon;'),
                     (0, 0, u, u + "'", u, u, u, u, u + '<sup>n</sup>'))]
        us = ("mm", "mrad", "mm", "mrad", "", "m", "m<sup>-1</sup>",
              "mm&middot;mrad", "mm&middot;mrad")

        s =['<h4>{0:<3s} = {1:.4f} {2:>10s}</h4>'.format(n, r.get(k), ui)
                for (n, k, ui) in zip(names, ks, us) if k != 'total_intensity']
        s.append('<hr>')
        s.append('<h4>Total Intensity: {0:.4f} &mu;A</h4>'.format(r.get('total_intensity')))
        self.results_textEdit.setHtml("<html>{}</html>".format(''.join(s)))

    def closeEvent(self, e):
        pass

