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

import numpy as np
from functools import partial

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QMainWindow

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
        self.params = (
                'pulse_length', 'rep_rate', 'peak_current',
                'ion_mass', 'ion_charge', 'beam_energy')
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
            eta, w = f_beam_power(
                             self._beam_energy, self._peak_current,
                             self._ion_mass, self._ion_charge,
                             self._pulse_length, self._rep_rate)
        except AttributeError:
            pass
        else:
            self.beam_power_lineEdit.setText(FMT.format(w))
            self.duty_cycle_lineEdit.setText(FMT.format(eta))


def f_beam_power(beam_energy, peak_current,
                 ion_mass, ion_charge,
                 pulse_length, rep_rate, **kws):
    duty_cycle = rep_rate * pulse_length * 1e-4
    beam_power = beam_energy * peak_current / ion_charge * ion_mass * duty_cycle * 0.01
    return duty_cycle, beam_power



if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    version = 0.1
    app = QApplication(sys.argv)
    w = MyAppWindow(version)
    w.show()
    w.setWindowTitle("This is an app from template")
    sys.exit(app.exec_())
