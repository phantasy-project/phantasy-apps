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
import os
from functools import partial

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import QUrl

from PyQt5.QtGui import QKeySequence
from PyQt5.QtGui import QIcon, QPixmap

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QShortcut

from phantasy import MachinePortal

from phantasy_ui import BaseAppForm
from phantasy_ui import get_open_filename
from phantasy_ui import printlog
from phantasy_ui.widgets import LatticeWidget

from phantasy_apps.utils import find_dconf
from phantasy_apps.synoptic_app.control import Controller
from phantasy_apps.synoptic_app.webview import MyWebView
from phantasy_apps.synoptic_app.data import DataAgent
from phantasy_apps.synoptic_app.ui.ui_app import Ui_MainWindow

DEFAULT_SVGFILE = find_dconf("synoptic_app", "svgfiles/fs1-arc.svg")
SVGFILE_DIR = os.path.dirname(DEFAULT_SVGFILE)


class MyAppWindow(BaseAppForm, Ui_MainWindow):

    # lattice is changed
    lattice_changed = pyqtSignal(QVariant)

    # settling time is changed
    settling_time_changed = pyqtSignal(float)

    def __init__(self, version, filepath=None, debug=False, **kws):
        super(self.__class__, self).__init__()

        # app version, title
        self.setAppTitle("Synoptic View & Control")
        self.setAppVersion(version)

        # app info in about dialog
        self.app_about_info = """
            <html>
            <h4>About Synoptic View & Control</h4>
            <p>This app is created to visualize the accelerator, and control the device as well, current version is {}.
            </p>
            <p>Copyright (C) 2020 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)
        self.postInitUi()

        # lattice
        self._lattice_load_window = None
        mach = kws.get('machine')
        segm = kws.get('segment')
        machine = 'FRIB' if mach is None else mach
        segment = 'LINAC' if segm is None else segm
        mp = MachinePortal(machine, segment)
        self.lattice = mp.work_lattice_conf

        #
        self.post_init(debug=debug)

        #
        if filepath is None:
            filepath = DEFAULT_SVGFILE
        self.set_view(filepath)

    def post_init(self, debug):
        #
        self.svg_basesize = None
        self._start_icon = QIcon(QPixmap(":/sn-app/icons/start.png"))
        self._stop_icon = QIcon(QPixmap(":/sn-app/icons/stop.png"))
        #
        self.view = MyWebView(debug_mode=debug)
        self.vbox.addWidget(self.view)

        self.frame = self.view.page().mainFrame()
        self.frame.loadFinished.connect(self.on_frame_loaded)

        self.controller = Controller(self.frame, self.lattice)
        self.controller.status_info_changed.connect(self.statusInfoChanged)
        self.controller.pointed_device_changed.connect(self.on_pointed_device_changed)
        self.controller.svg_basesize_changed.connect(self.on_svg_basesize_changed)
        self.lattice_changed.connect(self.controller.on_lattice_changed)

        self.frame.addToJavaScriptWindowObject('CTRL', self.controller)
        self.frame.javaScriptWindowObjectCleared.connect(
                self.on_javaScriptWindowObjectCleared)

        # data
        settling_time = self.settling_time_dsbox.value()
        self.data_agent = DataAgent(self.controller, settling_time)
        self.settling_time_changed.connect(self.data_agent.on_settling_time_changed)
        self.data_agent.value_changed.connect(self.controller.on_update_value)
        self.data_agent.started.connect(self.on_data_agent_started)
        self.data_agent.finished.connect(self.on_data_agent_finished)
        #self.data_agent.finished.connect(self.data_agent.deleteLater)

        # keyshorts
        self.action_zoom_in.setShortcut(QKeySequence.ZoomIn)
        self.action_zoom_out.setShortcut(QKeySequence.ZoomOut)
        zoom0 = QShortcut(QKeySequence("Ctrl+0"), self)
        zoom0.activated.connect(partial(self.on_zoom_set_view, 100))

    @pyqtSlot()
    def on_data_agent_started(self):
        o = self.start_data_agent_btn
        o.setText("STOP")
        o.setIcon(self._stop_icon)

    @pyqtSlot()
    def on_data_agent_finished(self):
        o = self.start_data_agent_btn
        o.setText("START")
        o.setIcon(self._start_icon)

    @pyqtSlot()
    def on_click_start_btn(self):
        # start data agent.
        text = self.start_data_agent_btn.text()
        if text == 'START':
            if not self.data_agent.isRunning():
                self.data_agent.start()
        else:
            if self.data_agent.isRunning():
                self.data_agent.stop()

    def set_view(self, filepath):
        printlog("Set view with {}".format(filepath))
        #
        self.view.load(QUrl.fromLocalFile(os.path.abspath(filepath)))
        self.view.show()

    def on_javaScriptWindowObjectCleared(self):
        self.frame.addToJavaScriptWindowObject('CTRL', self.controller)

    @pyqtSlot(bool)
    def on_frame_loaded(self, f):
        printlog("Page is loaded, start data agent.")
        # start data agent
        self.on_click_start_btn()

    @pyqtSlot('QString')
    def on_pointed_device_changed(self, devname):
        self.current_pointed_device_lineEdit.setText(devname)

    @pyqtSlot(float, float)
    def on_svg_basesize_changed(self, w, h):
        self.svg_basesize = (w, h)
        self.on_zoom_fit_page_view()

    @pyqtSlot()
    def on_open_file(self):
        """Open SVG file.
        """
        filepath, ext = get_open_filename(self,
            type_filter="SVG Files (*.svg)", cdir=SVGFILE_DIR)
        if filepath is None:
            return
        self.set_view(filepath)

    @pyqtSlot()
    def on_zoom_in_view(self):
        self.view.change_zoom_factor(10)

    @pyqtSlot()
    def on_zoom_out_view(self):
        self.view.change_zoom_factor(-10)

    @pyqtSlot()
    def on_zoom_set_view(self, zf=100.0):
        self.view.zoom_factor = zf
        self.view.zooming_view.emit()

    @pyqtSlot()
    def on_zoom_fit_page_view(self):
        if self.svg_basesize is None:
            return
        w, h = self.svg_basesize
        printlog("Resize view to ({}, {}).".format(w, h))
        viewSize = self.view.frameSize()
        zf_w = viewSize.width() / w * 100
        zf_h = viewSize.height() / h * 100
        self.on_zoom_set_view(min(zf_w, zf_h))

    def resizeEvent(self, evt):
        # do not trigger very often!
        self.on_zoom_fit_page_view()
        QMainWindow.resizeEvent(self, evt)

    @pyqtSlot(QVariant)
    def on_lattice_changed(self, o):
        """Lattice is changed.
        """
        self.lattice = o.combined_lattice()
        self.lattice_changed.emit(self.lattice)

    @pyqtSlot()
    def on_load_lattice(self):
        """Load lattice.
        """
        if self._lattice_load_window is None:
            self._lattice_load_window = LatticeWidget()
            self._lattice_load_window.latticeChanged.connect(
                self.on_lattice_changed)
            self._lattice_load_window.latticeChanged.connect(self._lattice_load_window.close)
            #self._lattice_load_window.latticeChanged.connect(self.show_init_settings_info)
        self._lattice_load_window.show()

    @pyqtSlot(float)
    def on_settling_time_changed(self, x):
        """Settling time (second) for data updating is changed.
        """
        self.settling_time_changed.emit(x)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    version = 0.1
    app = QApplication(sys.argv)
    w = MyAppWindow(version, None, machine="FRIB_VA", segment="LS1FS1")
    w.show()
    w.setWindowTitle("This is an app from template")

    sys.exit(app.exec_())
