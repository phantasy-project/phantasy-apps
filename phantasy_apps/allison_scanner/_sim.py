import epics
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from numpy import ndarray


class SimDevice(QObject):

    data_changed = pyqtSignal(ndarray)
    ioc_ready_changed = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, data_pv, status_pv, trigger_pv, pos_pv,
                 pos_begin_pv, pos_end_pv, pos_step_pv,
                 volt_begin_pv, volt_end_pv, volt_step_pv,
                 in_pv=None, out_pv=None, itlk_pv=None, en_pv=None,
                 bias_on_pv=None, pos_set_pv=None,
                 bias_volt_pv=None, bias_volt_set_pv=None,
                 ready_pv=None):
        super(self.__class__, self).__init__()

        # pv names --> PV
        self._trigger_pv = trigger_pv

        # live only
        self._in_pv = self._out_pv = self._itlk_pv = self._en_pv = self._bias_on_pv = \
                self._pos_pv, self._pos_set_pv, self._bias_volt_pv, self._bias_volt_set_pv = None
        if in_pv is not None:
            self._in_pv = epics.PV(in_pv)
            self._incid = self._in_pv.add_callback(self.on_update_in)
        if out_pv is not None:
            self._out_pv = epics.PV(out_pv)
            self._outcid = self._out_pv.add_callback(self.on_update_out)
        if itlk_pv is not None:
            self._itlk_pv = epics.PV(itlk_pv)
            self._itlkcid = self._itlk_pv.add_callback(self.on_update_itlk)
        if en_pv is not None:
            self._en_pv = epics.PV(en_pv)
            self._encid = self._en_pv.add_callback(self.on_update_en)
        if bias_on_pv is not None:
            self._bias_on_pv = epics.PV(bias_on_pv)
            self._biasoncid = self._bias_on_pv.add_callback(self.on_update_biason)
        if pos_set_pv is not None:
            self._pos_set_pv = epics.PV(pos_set_pv)
            self._postsetcid = self._pos_set_pv.add_callback(self.on_update_pos_set)
        if bias_volt_pv is not None:
            self._bias_volt_pv = epics.PV(bias_volt_pv)
            self._biasvoltcid = self._bias_volt_pv.add_callback(self.on_update_biasvolt)
        if bias_volt_set_pv is not None:
            self._bias_volt_set_pv = epics.PV(bias_volt_set_pv)
            self._biasvoltsetcid = self._bias_volt_set_pv.add_callback(self.on_update_biasvolt_set)
        #
        if ready_pv is not None:
            # sim only
            self._ready_pv = epics.PV(ready_pv, auto_monitor=True)
            self._rcid = self._ready_pv.add_callback(self.on_update_ioc_ready)

        self._status_pv = epics.PV(status_pv, auto_monitor=True)
        self._pos_pv = epics.PV(pos_pv)
        self._data_pv = epics.PV(data_pv, auto_monitor=True)
        self._scid = self._status_pv.add_callback(self.on_update_s)
        self._dcid = self._data_pv.add_callback(self.on_update)
        self._pcid = self._pos_pv.add_callback(self.on_update_p)

        self._pos_begin_pv = epics.PV(pos_begin_pv)
        self._pos_end_pv = epics.PV(pos_end_pv)
        self._pos_step_pv = epics.PV(pos_step_pv)
        self._volt_begin_pv = epics.PV(volt_begin_pv)
        self._volt_end_pv = epics.PV(volt_end_pv)
        self._volt_step_pv = epics.PV(volt_step_pv)

        self._pbcid = self._pos_begin_pv.add_callback(self.on_update_pb)
        self._pecid = self._pos_end_pv.add_callback(self.on_update_pe)
        self._pscid = self._pos_step_pv.add_callback(self.on_update_ps)
        self._vbcid = self._volt_begin_pv.add_callback(self.on_update_vb)
        self._vecid = self._volt_end_pv.add_callback(self.on_update_ve)
        self._vscid = self._volt_step_pv.add_callback(self.on_update_vs)

    def on_update(self, value, **kws):
        self.data_changed.emit(value)

    def start(self):
        epics.caput(self._trigger_pv, 1)

    def reset_data_cb(self):
        # self._data_pv.remove_callback(self._dcid)
        # self._status_pv.remove_callback(self._scid)
        # self._pos_pv.remove_callback(self._pcid)
        self.finished.emit()

    def on_update_ioc_ready(self, value, **kws):
        # sim only
        self.ioc_ready_changed.emit(value)

    def on_update_s(self, value, **kws):
        if value == 12:
            self.reset_data_cb()


