#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lmfit
import numpy as np
from functools import partial
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from phantasy import MachinePortal
from phantasy_ui import BaseAppForm

from phantasy_apps.correlation_visualizer.data import JSONDataSheet
from phantasy_apps.correlation_visualizer.data import ScanDataModel
from phantasy_ui import get_open_filename
from .ui.ui_app import Ui_MainWindow
from .utils import draw_beam_ellipse

LIGHT_SPEED = 299792458 # [m/s]
ION_ES = 931.49432e+06  # rest energy [eV/u]

# sample point for fitting curve
N_SAMPLE = 100

# unit
UNIT_FAC = {"mm": 1.0e-3, "m": 1.0}

class QuadScanWindow(BaseAppForm, Ui_MainWindow):

    # scan plot curve w/ errorbar
    curveUpdated = pyqtSignal(QVariant, QVariant, QVariant, QVariant)

    # update fitting curve
    fitCurveChanged = pyqtSignal(QVariant, QVariant)

    def __init__(self, version, data=None):
        super(QuadScanWindow, self).__init__()

        # app version
        self._version = version

        # window title/icon
        self.setWindowTitle("Quadrupole Scan App")
        #self.setWindowIcon(QIcon(QPixmap(icon)))

        # set app properties
        self.setAppTitle("Quadrupole Scan App")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Quadrupole Scan App</h4>
            <p>This app is created to analyze the data from quadrupole
            scan, to calculate the beam transverse emittance and Twiss
            parameters, current version is {}.
            </p>
            <p>Copyright (C) 2018 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

        # events
        self.curveUpdated.connect(self.matplotliberrorbarWidget.update_curve)

        # post init ui
        self.post_init_ui()

        # data from app: Correlation Visualizer
        # try to load data
        self.qs_data = data
        self.update_ui_with_data(self.qs_data)

    def post_init_ui(self):
        all_objs = self.beam_info_groupBox.findChildren(QLineEdit) \
                 + self.fitting_input_groupBox.findChildren(QLineEdit)
        for obj in all_objs:
            obj.setValidator(QDoubleValidator())

        for o in self.findChildren(QLineEdit):
            o.textChanged.connect(self.highlight_text)

        # reset beam_ellipse_plot
        self.beam_ellipse_plot.axes.clear()
        self.beam_ellipse_plot.axes.axis('off')
        self.beam_ellipse_plot.update_figure()

        # data viz: matplotliberrorbarWidget
        # add one more curve for fitting
        self.matplotliberrorbarWidget.add_curve()
        # set the line label as 'Fitting'
        self.matplotliberrorbarWidget.setLineID(1)
        self.matplotliberrorbarWidget.setLineLabel("Fitting")
        self.matplotliberrorbarWidget.setLineID(0)
        self.matplotliberrorbarWidget.setFigureXlabel("Quad Gradient [T/m]")
        self.matplotliberrorbarWidget.setFigureYlabel("$\sigma^2\,\mathrm{[m^2]}$")

        # set empty canvas
        self.matplotliberrorbarWidget.setEbLineID(0)
        self.matplotliberrorbarWidget.setLineID(0)
        self.curveUpdated.emit([], [], [], [])

        # events
        self.fitCurveChanged[QVariant, QVariant].connect(self.update_fitting_curve)
        self.matplotliberrorbarWidget.setYTickFormat("Custom", "%.3g")

        # units
        self.unit_mm_rbtn.toggled.connect(
                partial(self.on_update_unit, 'mm'))
        self.unit_meter_rbtn.toggled.connect(
                partial(self.on_update_unit, 'm'))
        self.unit_mm_rbtn.setChecked(True)
        assert self._unit == "mm"

    @pyqtSlot(bool)
    def on_update_unit(self, unit, f):
        if f:
            self._unit = unit
        if hasattr(self, '_scan_data_model'):
            self.on_update_ydata(self.monitors_cbb.currentIndex())

    @pyqtSlot(QVariant, QVariant)
    def update_fitting_curve(self, x, y):
        """Update fitting line.
        """
        self.matplotliberrorbarWidget.setLineID(1)
        self.matplotliberrorbarWidget.setXData(x)
        self.matplotliberrorbarWidget.setYData(y)

    @pyqtSlot()
    def onOpen(self):
        """Open data sheet for quad scan, which is generated from
        'Correlation Visualizer' app.
        """
        filepath, ext = get_open_filename(self,
            type_filter="JSON Files (*.json);;HDF5 Files (*.hdf5 *.h5)")
        if filepath is None:
            return
        if ext.upper() == 'JSON':
            # process json data sheet
            self.qs_data = JSONDataSheet(filepath)
        elif ext.upper() == 'H5':
            # process h5 data sheet
            pass

        # present data
        self.update_ui_with_data(self.qs_data)

    def update_ui_with_data(self, data=None):
        """Present data.
        """
        if data is None:
            return

        data_ts_created = data['data']['created']
        task_duration_in_sec = data['task']['duration']
        data_shape = data['data']['shape']
        quad_name = data['devices']['alter_element']['name']
        monitors = [(m['name'], m['field']) for m in data['devices']['monitors']]
        scan_range = data['task']['scan_range']
        scan_data_model = ScanDataModel(np.asarray(data['data']['array']))
        self._scan_data_model = scan_data_model

        # fillout lineEdits
        self.data_ts_created_lineEdit.setText(data_ts_created)
        self.task_duration_lineEdit.setText('{0:.2f}'.format(task_duration_in_sec))
        self.data_size_lineEdit.setText(
                "(niter:{s[0]} nshot:{s[1]} ndim:{s[2]})".format(s=data_shape))
        self.quad_name_lineEdit.setText(quad_name)

        self.monitors_cbb.addItems(['{} [{}]'.format(name, field) for name, field in monitors])

        self.scan_range_lineEdit.setText('from {smin:.2f} to {smax:.2f} ({snum}) points'.format(
                smin=min(scan_range), smax=max(scan_range),
                snum=len(scan_range)))

        # y data event
        self.monitors_cbb.currentIndexChanged.connect(self.on_update_ydata)

        self.on_update_ydata(0)

    @pyqtSlot(int)
    def on_update_ydata(self, idx):
        """Update y data.
        """
        ind = idx + 1
        # show data on figure widget
        sm = self._scan_data_model
        x, y = sm.get_xavg(), sm.get_yavg(ind=ind)
        xerr, yerr = sm.get_xerr(), sm.get_yerr(ind=ind)

        self.x, self.y = x, (y * UNIT_FAC[self._unit])**2
        self.matplotliberrorbarWidget.setEbLineID(0)
        self.matplotliberrorbarWidget.setLineID(0)
        self.curveUpdated.emit(self.x, self.y, xerr, yerr)

    @pyqtSlot()
    def on_fit_parabola(self):
        """Fit parabola curve with defined parameters.
        """
        ion_z = float(self.ref_IonZ_lineEdit.text())
        ion_ek = float(self.ref_IonEk_lineEdit.text())
        l_quad = float(self.quad_length_lineEdit.text())
        l_drift = float(self.distance_lineEdit.text())
        ion_w = ion_ek + ION_ES
        ion_gamma = 1 + ion_ek/ION_ES
        ion_beta = (1 - 1.0/ion_gamma**2)**0.5
        brho = ion_beta * ion_w / ion_z / LIGHT_SPEED
        bg = ion_beta * ion_w / ION_ES

        #
        a0 = float(self.coef_a_init_lineEdit.text())
        b0 = float(self.coef_b_init_lineEdit.text())
        c0 = float(self.coef_c_init_lineEdit.text())
        method = self.opt_method_comboBox.currentText()

        a, b, c, res = parabola_fitting(a0, b0, c0, self.x, self.y, method)

        (emit, nemit), (alpha, beta, gamma) = \
            single_quad_scan_analysis((a, b, c), l_quad, l_drift, brho, bg)

        # present results
        self.coef_a_final_lineEdit.setText('{0:.6g}'.format(a))
        self.coef_b_final_lineEdit.setText('{0:.6g}'.format(b))
        self.coef_c_final_lineEdit.setText('{0:.6g}'.format(c))
        self.resi_chisqr_lineEdit.setText('{0:.6g}'.format(res))

        self.emit_lineEdit.setText('{0:.6g}'.format(emit * 1e6))
        self.nemit_lineEdit.setText('{0:.6g}'.format(nemit * 1e6))
        self.twiss_alpha_lineEdit.setText('{0:.6g}'.format(alpha))
        self.twiss_beta_lineEdit.setText('{0:.6g}'.format(beta))
        self.twiss_gamma_lineEdit.setText('{0:.6g}'.format(gamma))

        # draw beam ellipse
        try:
            draw_beam_ellipse(self.beam_ellipse_plot.axes, alpha, beta, gamma, emit)
            self.beam_ellipse_plot.update_figure()
        except:
            QMessageBox.warning(self, "",
                    "Fatal error encountered.",
                    QMessageBox.Ok)

        # viz the fitting curve
        xx = np.linspace(self.x.min(), self.x.max(), N_SAMPLE)
        yy = (lambda x:a* x**2 + b * x + c)(xx)
        self.fitCurveChanged.emit(xx, yy)

    @pyqtSlot()
    def on_sync_coefs(self):
        """Sync the fitted ABC values to be the new set of initial settings.
        """
        self.coef_a_init_lineEdit.setText(self.coef_a_final_lineEdit.text())
        self.coef_b_init_lineEdit.setText(self.coef_b_final_lineEdit.text())
        self.coef_c_init_lineEdit.setText(self.coef_c_final_lineEdit.text())

    @pyqtSlot()
    def on_autofill_beam_params(self):
        """Autofill beam parameters based on current physics model settings
        """
        quad_name = self.quad_name_lineEdit.text()
        pm_name = self.monitors_cbb.currentText().split()[0]

        segment = 'LEBT'
        if 'MEBT' in quad_name:
            segment = 'MEBT'

        mp = MachinePortal("FRIB", segment)
        q = mp.get_elements(name=quad_name)[0]
        p = mp.get_elements(name=pm_name)[0]

        self.quad_length_lineEdit.setText('{0:.3g}'.format(q.length))
        self.distance_lineEdit.setText('{0:.3g}'.format(p.sb - q.se))


def single_quad_scan_analysis(params, quad_length, drift_length,
                              rigidity, lorentz_energy):
    """Calculate the emittance and Twiss parameters from parabola coeffients
    and beam parameters.

    Parameters
    ----------
    params : tuple
        Tuple of a, b, c, from which parabola curve could be built as:
        f(G) = a * G^2 + b * G + c, where G is the quadrupole gradient in T/m.
    quad_length : float
        Quadrupole length in m.
    drift_length : float
        Drift between the beam size monitor and quadrupole, in m.
    rigidity : float
        Beam rigidity the quadrupole, as known as brho.
    lorentz_energy : float
        Relativistic lorentz factor of ion energy.

    Returns
    -------
    r : tuple
        Tuple of (geometrical emittance, normalized emittance),
        (alpha, beta, gamma), i.e. the first element is tuple of emittances,
        and the second element is tuple of Twiss parameters.
        Units: emittance: m.rad
    """
    a, b, c = params
    lq, d = quad_length, drift_length
    brho, bg = rigidity, lorentz_energy

    s11 = a * brho**2 / d / d / lq / lq
    s12 = (-b * brho - 2 * d * lq * s11) / (2 * d * d * lq)
    s22 = (c - s11 - 2 * d * s12) / d / d

    epsilon = (s11 * s22 - s12 ** 2) ** 0.5
    epsilon_n = epsilon * bg

    alpha, beta, gamma = -s12/epsilon, s11/epsilon, s22/epsilon

    return (epsilon, epsilon_n), (alpha, beta, gamma)


def parabola_fitting(a0, b0, c0, x, y, method):
    """Parabola curve fitting.
    """
    p = lmfit.Parameters()
    p.add('a', value=a0)
    p.add('b', value=b0)
    p.add('c', value=c0)

    def f(p, x, y):
        return p['a'] * x**2 + p['b'] * x + p['c'] - y

    res = lmfit.minimize(f, p, method, args=(x, y))

    a, b, c = res.params['a'].value, res.params['b'].value, res.params['c'].value

    return a, b, c, res.chisqr
