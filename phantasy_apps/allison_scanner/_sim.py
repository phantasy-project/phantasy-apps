import epics
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from numpy import ndarray


class SimDevice(QObject):
    data_changed = pyqtSignal(ndarray)
    pos_changed = pyqtSignal(float)
    status_in_changed = pyqtSignal(float)
    status_out_changed = pyqtSignal(float)
    itlk_changed = pyqtSignal(float)
    status_enable_changed = pyqtSignal(float)
    finished = pyqtSignal()
    def __init__(self, data_pv, status_pv, trigger_pv, pos_pv,
                 in_pv=None, out_pv=None, itlk_pv=None, en_pv=None):
        super(self.__class__, self).__init__()

        # pv names --> PV
        self._trigger_pv = trigger_pv

        # live only
        self._in_pv = self._out_pv = self._itlk_pv = self._en_pv = None
        if in_pv is not None:
            self._in_pv = epics.PV(in_pv)
            self._incid = self._in_pv.add_callback(self.on_update_in)
        if out_pv is not None:
            self._out_pv = epics.PV(out_pv)
            self._outcid = self._in_pv.add_callback(self.on_update_out)
        if itlk_pv is not None:
            self._itlk_pv = epics.PV(itlk_pv)
            self._itlkcid = self._itlk_pv.add_callback(self.on_update_itlk)
        if en_pv is not None:
            self._en_pv = epics.PV(en_pv)
            self._encid = self._en_pv.add_callback(self.on_update_en)
        #

        self._status_pv = epics.PV(status_pv, auto_monitor=True)
        self._pos_pv = epics.PV(pos_pv)
        self._data_pv = epics.PV(data_pv, auto_monitor=True)
        self._scid = self._status_pv.add_callback(self.on_update_s)
        self._dcid = self._data_pv.add_callback(self.on_update)
        self._pcid = self._pos_pv.add_callback(self.on_update_p)

    def on_update(self, value, **kws):
        self.data_changed.emit(value)

    def start(self):
        epics.caput(self._trigger_pv, 1)

    def reset_data_cb(self):
        self._data_pv.remove_callback(self._dcid)
        self._status_pv.remove_callback(self._scid)
        # self._pos_pv.remove_callback(self._pcid)
        self.finished.emit()

    def on_update_p(self, value, **kws):
        self.pos_changed.emit(value)

    def on_update_s(self, value, **kws):
        if value == 12:
            self.reset_data_cb()

    def on_update_in(self, value, **kws):
        self.status_in_changed.emit(value)

    def on_update_out(self, value, **kws):
        self.status_out_changed.emit(value)

    def on_update_itlk(self, value, **kws):
        self.itlk_changed.emit(value)

    def on_update_en(self, value, **kws):
        self.status_enable_changed.emit(value)
