#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QColor

from functools import partial
from phantasy_apps.correlation_visualizer.ui.ui_plot_all import Ui_Form
from mpl4qt.widgets.mplconfig import MatplotlibConfigPanel
from mpl4qt.widgets.utils import mplcolor2hex


class PlotAllWidget(QWidget, Ui_Form):
    curve_data_changed = pyqtSignal(QVariant, QVariant, QVariant, QVariant)
    curve_ylabel_changed = pyqtSignal('QString')
    xlabel_changed = pyqtSignal('QString')
    line_id_changed = pyqtSignal(int)
    def __init__(self, parent, data):
        super(PlotAllWidget, self).__init__()
        self.parent = parent

        # UI
        self.setupUi(self)
        self.setWindowTitle("Plot All Curves")
        self._curve_widget = self.matplotliberrorbarWidget

        #
        self.line_id_changed.connect(self._curve_widget.setLineID)
        self.line_id_changed.connect(self._curve_widget.setEbLineID)
        self.curve_data_changed.connect(self._curve_widget.update_curve)
        self.xlabel_changed.connect(self._curve_widget.setFigureXlabel)
        self.curve_ylabel_changed.connect(self._curve_widget.setFigureYlabel)
        #
        self.set_data(data)
        self.init_dataviz()
        self.update_curve(data)

    def closeEvent(self, evt):
        self._show_flag = False

    def is_show(self):
        return self._show_flag

    def reset(self):
        data = self.parent._get_all_data()
        self.set_data(data)
        self.init_dataviz()
        self.update_curve(data)
        self.update_line_status()

    def init_dataviz(self):
        """Initialize the draw area.
        """
        o = self._curve_widget
        o.setLineColor(QColor("black"))
        o.setMkFaceColor(QColor("black"))
        o.setMkEdgeColor(QColor("black"))
        for i, l in enumerate(o.get_all_curves()):
            self.line_id_changed.emit(i)
            o.setLineLabel(f"_line{i}")
            o.clear_data()

        #
        self.xlabel_changed.emit(self.xdata[0])

        for i, (ylbl,_,_) in enumerate(self.ydata):
            if len(o.get_all_curves()) < i + 1:
                o.add_curve(None, None, None, None)
            self.line_id_changed.emit(i)
            o.setLineLabel(ylbl)

        self.update_line_status()

    def update_line_status(self):
        o = self._curve_widget

        def show_line(line_id, is_checked):
            o.setLineID(line_id)
            o.setLineVisible(is_checked)
            o.setEbLineID(line_id)
            o.setEbLineVisible(is_checked)

        w = self.option_area.takeWidget()
        w.setParent(None)
        w = QWidget(self)
        w.setContentsMargins(0, 6, 0, 0)
        layout = QVBoxLayout()
        for i, (ylbl, _, _) in enumerate(self.ydata):
            hbox = QHBoxLayout()
            i_btn = QToolButton()
            c = QColor(mplcolor2hex(o._lines[i].get_c()))
            MatplotlibConfigPanel.set_btn_color(i_btn, c)
            i_chkbox = QCheckBox(ylbl, self)
            i_chkbox.setChecked(True)
            i_chkbox.toggled.connect(partial(show_line, i))
            hbox.addWidget(i_btn)
            hbox.addWidget(i_chkbox)
            layout.addLayout(hbox)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(spacer)
        w.setLayout(layout)
        self.option_area.setWidget(w)

    def set_data(self, data):
        self.xdata, self.ydata = data[0], data[1:]
        # xdata: (lbl, xavg, xerr)
        # ydata: [(ilbl, iyavg, iyerr),...]

    def update_curve(self, new_data):
        self.set_data(new_data)
        xavg, xerr = self.xdata[1], self.xdata[2]
        for i, (ylbl, yavg, yerr) in enumerate(self.ydata):
            self.line_id_changed.emit(i)
            self.curve_data_changed.emit(xavg, yavg, xerr, yerr)
