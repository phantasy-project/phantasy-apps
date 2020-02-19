# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSlot


class Controller(QObject):
    """Interface between webview and control system."""

    def __init__(self, frame, parent=None):
        super(self.__class__, self).__init__(parent)
        self.frame = frame
        self.open = False
        self._devices = dict()
        self.selected_device = None

    @pyqtSlot(str)
    def select(self, devname):
        print("select: ", devname)
        if not devname == self.selected_device:
            self.frame.evaluateJavaScript("Ui.select('{}')".format(devname))
            self.selected_device = devname

    @pyqtSlot(str)
    def registerDevice(self, devname):
        self._devices[devname] = False
        print("Registered device %s" % devname)

    def set_status(self, devname, status):
        if status != self._devices[devname]:
            print(status, self._devices[devname])
            self.frame.evaluateJavaScript("Ui.setStatus('{}', '{}')".format(
                                          devname, status))
            self._devices[devname] = status

