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

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QMainWindow
from phantasy_ui import BaseAppForm
from phantasy_ui import get_open_filename
from phantasy_apps.utils import apply_mplcurve_settings
from phantasy_apps.correlation_visualizer.data import ScanDataModel
from phantasy_apps.correlation_visualizer.data import JSONDataSheet

from .ui.ui_app import Ui_MainWindow

N_SAMPLE = 100


class MyAppWindow(BaseAppForm, Ui_MainWindow):

    # scan plot curve w/ errorbar
    curve_updated = pyqtSignal(QVariant, QVariant, QVariant, QVariant)

    # update fitting curve
    fit_curve_changed = pyqtSignal(QVariant, QVariant)

    #
    auto_scale_changed = pyqtSignal(bool)

    def __init__(self, version, **kws):
        super(self.__class__, self).__init__()

        # app version, title
        self.setAppVersion(version)
        self.setAppTitle("Achromat Tuning")

        # app info in about dialog
        self.app_about_info = """
            <html>
            <h4>About Achromat Tuning</h4>
            <p>This app is created for achromat tuning in the bending
            sections of an accelerator.
            </p>
            <p>Copyright (c) 2020 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self.getAppVersion())

        # UI
        self.setupUi(self)
        self.postInitUi()

        self._post_init()

    def _post_init(self):
        self.curve_updated.connect(self.update_curve)
        self.fit_curve_changed.connect(self.update_fitting_curve)
        self.auto_scale_changed.connect(self.bend_tuning_plot.setFigureAutoScale)

        # data viz: bend_tuning_plot
        # add one more curve for fitting
        o = self.bend_tuning_plot
        o.add_curve()
        # set the line label as 'Fitting'
        o.setLineID(1)
        o.setLineLabel("Fitting")
        o.setLineID(0)
        o.setLineLabel("Measurement")

        o.setFigureXlabel("Dipole Field [I]")
        o.setFigureYlabel("BPM Readings [mm]")
        o.setYTickFormat("Custom", "%.3g")

        # set empty canvas
        o.setEbLineID(0)
        o.setLineID(0)
        o.clear_data()

        apply_mplcurve_settings(o, 'achromat_tuning',
                                filename='mpl_settings.json')

    @pyqtSlot()
    def on_load_data(self):
        """Load data for analysis.
        """
        filepath, ext = get_open_filename(self,
                                          caption="Load Data from a File",
                                          type_filter="JSON Files (*.json);;HDF5 Files (*.h5)")
        if filepath is None:
            return

        self.load_file(filepath, ext)

    def load_file(self, filepath, ext):
        self.auto_scale_changed.emit(False)

        ds = JSONDataSheet(filepath)
        sm = ScanDataModel(np.asarray(ds['data']['array']))

        data = sm.get_avg()
        bend_settings = data[:, 0]
        avg_bpm_readings = data[:, 1:].mean(axis=1)

        self.curve_updated.emit(bend_settings, avg_bpm_readings, [], [])

        fit_p = np.polyfit(avg_bpm_readings, bend_settings, 2)
        fit_fn = np.poly1d(fit_p)
        x_opt = fit_fn(0.0)

        x_fit = np.linspace(avg_bpm_readings.min(), avg_bpm_readings.max(), N_SAMPLE)
        y_fit = fit_fn(x_fit)
        self.fit_curve_changed.emit(y_fit, x_fit)
        self.auto_scale_changed.emit(True)

    @pyqtSlot(QVariant, QVariant)
    def update_fitting_curve(self, x, y):
        """Update fitting line.
        """
        o = self.bend_tuning_plot
        o.setLineID(1)
        o.setXData(x)
        o.setYData(y)

    @pyqtSlot(QVariant, QVariant, QVariant, QVariant)
    def update_curve(self, x, y, xerr, yerr):
        o = self.bend_tuning_plot
        if xerr != [] and yerr != []:
            o.setEbLineID(0)
            o.setLineID(0)
            o.update_curve(x, y, xerr, yerr)
        else:
            o.setLineID(0)
            o.setXData(x)
            o.setYData(y)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    version = 0.1
    app = QApplication(sys.argv)
    w = MyAppWindow(version)
    w.show()
    w.setWindowTitle("This is an app from template")
    sys.exit(app.exec_())
