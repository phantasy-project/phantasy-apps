# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot

from phantasy_ui import printlog
from phantasy_ui.widgets import ProbeWidget
from phantasy_ui import delayed_exec

HANDLE = {'setpoint': 'SP', 'readback': 'RD'}


class Controller(QObject):
    """Interface between webview and control system."""

    # info to publish on status bar
    status_info_changed = pyqtSignal('QString')

    # pointed device
    pointed_device_changed = pyqtSignal('QString')

    # svg basesize, width, height
    svg_basesize_changed = pyqtSignal(float, float)

    # data changed
    data_changed = pyqtSignal(dict)

    def __init__(self, frame, lattice, parent=None):
        super(self.__class__, self).__init__(parent)
        self.lattice = lattice
        self.frame = frame
        self.open = False
        self._devices = dict()
        self.selected_device = None
        self.annote_anchors = {}

        # data, {devname: {(fname, handle): (value, nprec)}} 
        self.data = {}
        self.data_changed.connect(self.on_data_changed)

        # pointed device
        self.pointed_device = None
        self.pointed_device_changed.connect(self.on_pointed_device_changed)

        #
        self._probe_widgets_dict = {}

    @pyqtSlot(QVariant)
    def on_lattice_changed(self, lat):
        """Lattice is changed.
        """
        self.lattice = lat

    @pyqtSlot('QString')
    def select(self, devname):
        printlog("Click on: {}".format(devname))
        self.frame.evaluateJavaScript("Ui.select('{}')".format(devname))

    @pyqtSlot('QString', 'QString')
    def updateSelection(self, devname, selected):
        is_selected = selected == 'true'
        if is_selected:
            self.selected_device = devname
            msg = '<html><head/><body><p><span style=" color:#007bff;">Selected: </span><span style=" color:#dc3545;">{}</span></p></body></html>'.format(devname)
        else:
            self.selected_device = None
            msg = '<html><head/><body><p><span style=" color:#007bff;">Deselected: </span><span style=" color:#dc3545;">{}</span></p></body></html>'.format(devname)
        self.status_info_changed.emit(msg)
        delayed_exec(lambda:self.status_info_changed.emit(''), 5000)

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
        # value info -->
        #self.frame.evaluateJavaScript("Ui.updateTooltip('{}')".format(
        #    devname))
    
    def on_data_changed(self, data):
        # data changed.
        printlog(data)
        if self.pointed_device is None:
            return

        printlog(self.pointed_device)
        if self.pointed_device not in data:
            printlog("device is not in data", self.pointed_device)
            return

        value_list = []
        for (fname, handle), (value, nprec) in sorted(data[self.pointed_device].items()):
            l = "[{0}]({1}): {2}".format(fname, HANDLE[handle], round(value, nprec))
            value_list.append(l)
        m = len(value_list) // 2
        self.frame.evaluateJavaScript("Ui.updateTooltip('{}', '{}', '{}')".format(
            self.pointed_device, " ".join(value_list[0:m]), " ".join(value_list[m:])))

    @pyqtSlot('QString')
    def on_pointed_device_changed(self, devname):
        self.pointed_device = devname

    @pyqtSlot('QString')
    def mouseLeave(self, devname):
        self.frame.evaluateJavaScript("Ui.leave('{}')".format(devname))

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

        # !keep fresh data!
        if devname not in self.data:
            self.data[devname] = {(fname, handle): (float(value), nprec)}
        else:
            self.data[devname].update({(fname, handle): (float(value), nprec)})
        self.data_changed.emit(self.data)
