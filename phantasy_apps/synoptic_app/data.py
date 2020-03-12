# -*- coding: utf-8 -*-

import time

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot


class DataAgent(QThread):

    # value changed, value, ename, fname, handle, nprec
    value_changed = pyqtSignal(float, 'QString', 'QString', 'QString', int)

    def __init__(self, controller, settling_time):
        super(self.__class__, self).__init__()
        self.controller = controller
        self.settling_time = settling_time

    @pyqtSlot(float)
    def on_settling_time_changed(self, x):
        self.settling_time = x

    def run(self):
        self.run_flag = True
        lat = self.controller.lattice
        while self.run_flag:
            t0 = time.time()
            if lat is None:
                time.sleep(self.settling_time)
                continue
            for ename, fconf_list in self.controller.annote_anchors.items():
                elem = lat[ename]
                for (fname, handle, nprec) in fconf_list:
                    fld = elem.get_field(fname)
                    if handle == 'setpoint':
                        value = fld.current_setting()
                    elif handle == 'readback':
                        value = fld.value
                    if value is not None:
                        self.value_changed.emit(value, ename, fname, handle, nprec)
            dt = self.settling_time - (time.time() - t0)
            if dt > 0:
                time.sleep(dt)

    def stop(self):
        self.run_flag = False
