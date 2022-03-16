#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Template Python module generated based on 'app_template', 'phantasy-ui'
is required to make it executable as a PyQt5 app.

Created by: makeBasePyQtApp.

An example to create an app template:

>>> makeBasePyQtApp --app my_great_app --template AppWindow

Show the available templates:

>>> makeBasePyQtApp -l
"""

import epics
import numpy as np
from functools import partial

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox

from phantasy_ui import BaseAppForm

from .ui.ui_app import Ui_MainWindow

PER = 0.2
N = 100
FMT = "{0:.6g}"


class MyAppWindow(BaseAppForm, Ui_MainWindow):
    def __init__(self, version, **kws):
        super(self.__class__, self).__init__()

        # app version, title
        self.setAppVersion(version)
        self.setAppTitle("Calculator")

        # app info in about dialog
        self.app_about_info = """
            <html>
            <h4>About Calculator</h4>
            <p>This app is created for physics calculator regarding LINAC.
            </p>
            <p>Copyright (c) 2020 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self.getAppVersion())

        # UI
        self.setupUi(self)
        self.postInitUi()

        #
        self._post_init()

    def _post_init(self):
        #
        self.params = ('pulse_length', 'rep_rate', 'peak_current', 'ion_mass',
                       'ion_charge', 'beam_energy')
        for p in self.params:
            o = getattr(self, p + '_lineEdit')
            o.setValidator(QDoubleValidator(0, 1e10, 6))
            o.textChanged.connect(partial(self.on_update_params, p))
            o.textChanged.emit(o.text())

        #
        self.param_cbb.addItems(self.params)
        self.param_cbb.currentTextChanged.connect(self.on_param_changed)
        self.draw_btn.clicked.connect(self.on_draw)
        self.param_cbb.currentTextChanged.emit(self.param_cbb.currentText())

        # FSEE Flux
        # fc_pv_name = "FS1_SEE:FC_D2569:AVG_RD"
        fc_pv_name = "VA:SVR:NOISE"
        self.fc_pv = epics.PV(fc_pv_name)
        for p in ('fc_intensity', 'charge_state', 'k', 'area_w', 'area_h'):
            o = getattr(self, f"{p}_lineEdit")
            o.setValidator(QDoubleValidator(0, 1e6, 6))
            o.textChanged.connect(partial(self.on_update_flux, p))
            o.textChanged.emit(o.text())

    @pyqtSlot('QString')
    def on_update_flux(self, param, s):
        try:
            float(s)
        except ValueError:
            pass
        else:
            setattr(self, '_' + param, float(s))
        finally:
            self.update_flux()

    def update_flux(self):
        try:
            area, rate, flux = f_fsee_flux(self._fc_intensity,
                                           self._charge_state, self._k,
                                           self._area_w, self._area_h)
        except AttributeError:
            pass
        else:
            self.area_lineEdit.setText(FMT.format(area))
            self.beam_rate_lineEdit.setText(FMT.format(rate))
            self.beam_flux_lineEdit.setText(FMT.format(flux))

    @pyqtSlot('QString')
    def on_param_changed(self, s):
        self.current_param = s
        v = getattr(self, "_" + s)
        vmin, vmax = v * (1 - PER), v * (1 + PER)
        vstep = (vmax - vmin) / (N - 1)
        self.from_lineEdit.setText(FMT.format(vmin))
        self.to_lineEdit.setText(FMT.format(vmax))
        self.step_lineEdit.setText("{0:.2g}".format(vstep))
        self.draw_btn.clicked.emit()

    @pyqtSlot()
    def on_draw(self):
        x1 = float(self.from_lineEdit.text())
        x2 = float(self.to_lineEdit.text())
        dx = float(self.step_lineEdit.text())
        x = np.arange(x1, x2 + dx, dx)
        nsize = x.size
        param_dict = {
            p: np.ones(nsize) * getattr(self, "_" + p)
            for p in self.params
        }
        param_dict[self.current_param] = x
        eta, w = f_beam_power(**param_dict)

        o = self.matplotlibcurveWidget
        o.update_curve(x, w)
        o.setFigureXlabel(self.current_param)
        o.setFigureYlabel("Beam Power [W]")

    @pyqtSlot('QString')
    def on_update_params(self, param, s):
        try:
            float(s)
        except ValueError:
            pass
        else:
            setattr(self, '_' + param, float(s))
        finally:
            self.update_results()

    def update_results(self):
        try:
            eta, w = f_beam_power(self._beam_energy, self._peak_current,
                                  self._ion_mass, self._ion_charge,
                                  self._pulse_length, self._rep_rate)
        except AttributeError:
            pass
        else:
            self.beam_power_lineEdit.setText(FMT.format(w))
            self.duty_cycle_lineEdit.setText(FMT.format(eta))

    @pyqtSlot()
    def on_pull_fc2569(self):
        """Pull FC2569 reading and fill out the input box.
        """
        if not self.fc_pv.connected:
            QMessageBox.warning(self, "Fetch FC Intensity Reading",
                                f"Cannot reach '{self.fc_pv.pvname}'.", QMessageBox.Ok,
                                QMessageBox.Ok)
        else:
            v = self.fc_pv.value
            if v is not None:
                self.fc_intensity_lineEdit.setText(FMT.format(v))


def f_beam_power(beam_energy, peak_current, ion_mass, ion_charge, pulse_length,
                 rep_rate, **kws):
    duty_cycle = rep_rate * pulse_length * 1e-4
    beam_power = beam_energy * peak_current / ion_charge * ion_mass * duty_cycle * 0.01
    return duty_cycle, beam_power


def f_fsee_flux(fc_intensity, charge_state, k, area_w, area_h):
    # pA, 1, 1, mm, mm
    # area: cm^2
    # rate: pps
    # flux: pps/cm^2
    rate = fc_intensity * 1e-12 / charge_state / 1.6e-19 / k
    area = area_w * area_h / 100
    flux = rate / area
    return area, rate, flux


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    version = 0.1
    app = QApplication(sys.argv)
    w = MyAppWindow(version)
    w.show()
    w.setWindowTitle("This is an app from template")
    sys.exit(app.exec_())
