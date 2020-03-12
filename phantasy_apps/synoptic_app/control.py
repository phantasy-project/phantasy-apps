# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot

from phantasy_ui import printlog
from phantasy_ui.widgets import ProbeWidget
from phantasy_ui import delayed_exec


class Controller(QObject):
    """Interface between webview and control system."""

    # info to publish on status bar
    status_info_changed = pyqtSignal('QString')

    # pointed device
    pointed_device_changed = pyqtSignal('QString')

    # svg basesize, width, height
    svg_basesize_changed = pyqtSignal(float, float)

    def __init__(self, frame, lattice, parent=None):
        super(self.__class__, self).__init__(parent)
        self.lattice = lattice
        self.frame = frame
        self.open = False
        self._devices = dict()
        self.selected_device = None
        self.annote_anchors = {}
        #
        self._probe_widgets_dict = {}

    @pyqtSlot(QVariant)
    def on_lattice_changed(self, lat):
        """Lattice is changed.
        """
        self.lattice = lat

    @pyqtSlot('QString')
    def select(self, devname):
        printlog("Select: ", devname)
        if not devname == self.selected_device:
            self.frame.evaluateJavaScript("Ui.select('{}')".format(devname))
            self.selected_device = devname
            msg = '<html><head/><body><p><span style=" color:#007bff;">Selected: </span><span style=" color:#dc3545;">{}</span></p></body></html>'.format(devname)
            self.status_info_changed.emit(msg)
            delayed_exec(lambda:self.status_info_changed.emit(''), 2000)

    @pyqtSlot('QString')
    def dblSelect(self, devname):
        printlog("DblSelect: ", devname)
        elem = self.lattice[devname]
        if devname not in self._probe_widgets_dict:
            w = ProbeWidget(element=self.lattice[devname])
            self._probe_widgets_dict[devname] = w
        w = self._probe_widgets_dict[devname]
        w.show()

    @pyqtSlot('QString')
    def registerDevice(self, devname):
        self._devices[devname] = False
        msg = "Registered device {}".format(devname)
        printlog(msg)

    @pyqtSlot('QString', 'QString', 'QString', int)
    def registerAnnoteAnchor(self, devname, fname, handle, nprec):
        if devname not in self.annote_anchors:
            self.annote_anchors[devname] = [(fname, handle, nprec)]
        else:
            self.annote_anchors[devname].append((fname, handle, nprec))
        printlog("Registed anchor for {} [{}] {} {}".format(devname, fname, handle, nprec))

    @pyqtSlot('QString')
    def mouseOver(self, devname):
        msg = "Hover device {}".format(devname)
        printlog(msg)
        self.pointed_device_changed.emit(devname)
        self.frame.evaluateJavaScript("Ui.hover('{}')".format(devname))

    @pyqtSlot()
    def loadDeviceDone(self):
        n = len([k for k, v in self._devices.items() if not v])
        msg = "Loaded {} devices.".format(n)
        self.status_info_changed.emit(msg)
        delayed_exec(lambda:self.status_info_changed.emit(''), 5000)

    def set_status(self, devname, status):
        if status != self._devices[devname]:
            printlog(status, self._devices[devname])
            self.frame.evaluateJavaScript("Ui.setStatus('{}', '{}')".format(
                                          devname, status))
            self._devices[devname] = status

    @pyqtSlot(float, float)
    def get_content_size(self, w, h):
        """Get SVG base size of width x height in px.
        """
        self.svg_basesize_changed.emit(w, h)

    @pyqtSlot(float, 'QString', 'QString', 'QString', int)
    def on_update_value(self, value, devname, fname, handle, nprec):
        # update value
        self.frame.evaluateJavaScript(
            "Ui.updateData({}, '{}', '{}', '{}', {})".format(
                value, devname, fname, handle, nprec))
