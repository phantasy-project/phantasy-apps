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

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QUrl

from PyQt5.QtGui import QKeySequence

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QShortcut

from phantasy import MachinePortal

from phantasy_ui import BaseAppForm
from phantasy_ui import get_open_filename
from phantasy_ui import printlog

from phantasy_apps.synoptic_app.control import Controller
from phantasy_apps.synoptic_app.webview import MyWebView
from phantasy_apps.synoptic_app.ui.ui_app import Ui_MainWindow


class MyAppWindow(BaseAppForm, Ui_MainWindow):

    def __init__(self, version, filepath, **kws):
        super(self.__class__, self).__init__()

        # app version, title
        self.setAppVersion(version)
        self.setAppTitle("My App")

        # app info in about dialog
        # self.app_about_info = "About info of My App."

        # UI
        self.setupUi(self)
        self.postInitUi()

        #
        mp = MachinePortal("FRIB_VA", 'LS1FS1')
        self.lattice = mp.work_lattice_conf

        #
        self.post_init()
        #
        self.set_view(filepath)

    def post_init(self):
        self.view = MyWebView()
        self.vbox.addWidget(self.view)

        frame = self.view.page().mainFrame()
        frame.loadFinished.connect(self.on_frame_loaded)

        # keyshorts
        self.action_zoom_in.setShortcut(QKeySequence.ZoomIn)
        self.action_zoom_out.setShortcut(QKeySequence.ZoomOut)
        zoom0 = QShortcut(QKeySequence("Ctrl+0"), self)
        zoom0.activated.connect(self.on_zoom_reset_view)

    def set_view(self, filepath):
        printlog("Set view with {}".format(filepath))
        #
        self.view.load(QUrl.fromLocalFile(os.path.abspath(filepath)))
        #
        self.frame = self.view.page().mainFrame()
        self.controller = Controller(self.frame, self.lattice)
        self.controller.status_info_changed.connect(self.statusInfoChanged)
        self.controller.pointed_device_changed.connect(self.on_pointed_device_changed)
        self.frame.addToJavaScriptWindowObject('CTRL', self.controller)
        self.view.show()
        self.frame.javaScriptWindowObjectCleared.connect(self.on_javaScriptWindowObjectCleared)

    def on_javaScriptWindowObjectCleared(self):
        #self.frame = self.view.page().mainFrame()
        #self.controller = Controller(self.frame, self.lattice)
        self.frame.addToJavaScriptWindowObject('CTRL', self.controller)

    @pyqtSlot(bool)
    def on_frame_loaded(self, f):
        printlog("Page is loaded")
        contentsSize = self.frame.contentsSize()
        viewSize = self.view.frameSize()
        print(contentsSize, viewSize)

    @pyqtSlot('QString')
    def on_pointed_device_changed(self, devname):
        self.current_pointed_device_lineEdit.setText(devname)

    @pyqtSlot()
    def on_open_file(self):
        """Open SVG file.
        """
        filepath, ext = get_open_filename(self,
            type_filter="SVG Files (*.svg)")
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
    def on_zoom_reset_view(self):
        self.view.zoom_factor = 100
        self.view.zooming_view.emit()

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    version = 0.1
    app = QApplication(sys.argv)
    w = MyAppWindow(version, sys.argv[1])
    w.show()
    w.setWindowTitle("This is an app from template")

    sys.exit(app.exec_())
