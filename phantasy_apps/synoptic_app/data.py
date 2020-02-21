# -*- coding: utf-8 -*-

import time

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal


class DataAgent(QThread):

    # value changed, value, ename, fname
    value_changed = pyqtSignal(float, 'QString', 'QString')

    def __init__(self, controller, interval=1.0):
        super(self.__class__, self).__init__()
        self.controller = controller
        self.interval = interval

    def run(self):
        self.run_flag = True
        lat = self.controller.lattice
        while self.run_flag:
            for ename, fname_list in self.controller.annote_anchors.items():
                elem = lat[ename]
                for fname in fname_list:
                    fld = elem.get_field(fname)
                    val = fld.value
                    if val is not None:
                        self.value_changed.emit(val, ename, fname)
            time.sleep(self.interval)

    def stop(self):
        self.run_flag = False
