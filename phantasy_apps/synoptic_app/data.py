# -*- coding: utf-8 -*-

import time

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot


class DataAgent(QThread):

    # value changed, rd, [sp], ename, fname
    value_changed = pyqtSignal([float, float, 'QString', 'QString'],
                               [float, 'QString', 'QString'])

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
            for ename, fname_list in self.controller.annote_anchors.items():
                elem = lat[ename]
                for fname in fname_list:
                    fld = elem.get_field(fname)
                    rd = fld.value
                    sp = fld.current_setting()
                    if rd is not None:
                        if sp is not None:
                            self.value_changed[float, float, 'QString', 'QString'].emit(rd, sp, ename, fname)
                        else:
                            self.value_changed[float, 'QString', 'QString'].emit(rd, ename, fname)
            dt = self.settling_time - (time.time() - t0)
            if dt > 0:
                time.sleep(dt)

    def stop(self):
        self.run_flag = False
