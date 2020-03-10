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
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QMainWindow
from phantasy_ui import BaseAppForm
from phantasy_ui import get_open_filename
from phantasy_apps.utils import apply_mplcurve_settings
from phantasy_apps.correlation_visualizer.data import ScanDataModel
from phantasy_apps.correlation_visualizer.scan import load_task

from .ui.ui_app import Ui_MainWindow

N_SAMPLE = 100


class MyAppWindow(BaseAppForm, Ui_MainWindow):

    # scan plot curve w/ errorbar
    curve_updated = pyqtSignal(QVariant, QVariant, QVariant, QVariant)

    # update fitting curve
    fit_curve_changed = pyqtSignal(QVariant, QVariant)

    #
    auto_scale_changed = pyqtSignal(bool)

    #
    bend_tune_fn_changed = pyqtSignal(QVariant)

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
        # events
        self.curve_updated.connect(self.update_curve)
        self.fit_curve_changed.connect(self.update_fitting_curve)
        self.auto_scale_changed.connect(self.bend_tuning_plot.setFigureAutoScale)
        self.set_bend_goal_btn.clicked.connect(self.on_set_bend_goal)
        self.bpm_goal_lineEdit.textChanged.connect(self.on_eval_bend_goal)
        self.bpm_goal_lineEdit.returnPressed.connect(self.on_eval_bend_goal_pressed)
        self.bend_tune_fn_changed.connect(self.on_bend_tune_fn_changed)
        self.open_in_cv_btn.clicked.connect(self.on_open_in_cv)

        #
        self.bpm_goal_lineEdit.setValidator(QDoubleValidator())

        # vars
        self._mp = None
        self._current_datafile = None
        self._cv_window = None
        self.task = None
        self.bend_fn = None
        for o in (self.bpm_goal_lineEdit, self.bend_goal_lineEdit,
                  self.set_bend_goal_btn):
            o.setEnabled(False)

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
    def on_open_in_cv(self):
        """Open data file in Correlation Visualizer.
        """
        if self._current_datafile is None:
            return

        from phantasy_apps.correlation_visualizer import CorrelationVisualizerWindow
        from phantasy_apps.correlation_visualizer import __version__
        from phantasy_apps.correlation_visualizer import __title__

        if self._cv_window is None:
            self._cv_window = CorrelationVisualizerWindow(__version__)
            self._cv_window.setWindowTitle(__title__)
        self._cv_window.load_task_from_file(self._current_datafile)
        self._cv_window.show()

    @pyqtSlot(QVariant)
    def on_bend_tune_fn_changed(self, fn):
        for o in (self.bpm_goal_lineEdit, self.bend_goal_lineEdit,
                  self.set_bend_goal_btn):
            o.setEnabled(True)
        self.bend_fn = fn
        self.bpm_goal_lineEdit.textChanged.emit(self.bpm_goal_lineEdit.text())

    @pyqtSlot()
    def on_eval_bend_goal_pressed(self):
        self.on_eval_bend_goal(self.sender().text())

    @pyqtSlot('QString')
    def on_eval_bend_goal(self, s):
        try:
            v = float(s)
        except ValueError:
            pass
        else:
            goal = self.bend_fn(v)
            self.bend_goal_lineEdit.setText("{0:.4g}".format(goal))

    @pyqtSlot()
    def on_set_bend_goal(self):
        v = float(self.bend_goal_lineEdit.text())
        f = self.task.alter_action
        if self.task._alter_action_mode == 'regular':
            f(v, alter_elem=self.task.alter_element)
        else:
            f(v)

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
        self._current_datafile = filepath
        self.auto_scale_changed.emit(False)

        self.task = load_task(filepath, self._mp)
        if hasattr(self.task, '_lattice'):
            self._mp = self.task._lattice
        sm = ScanDataModel(self.task.scan_out_data)

        data = sm.get_avg()
        bend_settings = data[:, 0]
        avg_bpm_readings = data[:, 1:].mean(axis=1)

        self.curve_updated.emit(bend_settings, avg_bpm_readings, [], [])

        fit_p = np.polyfit(avg_bpm_readings, bend_settings, 2)
        fit_fn = np.poly1d(fit_p)
        self.bend_tune_fn_changed.emit(fit_fn)

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
