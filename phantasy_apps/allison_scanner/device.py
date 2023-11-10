#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Build device upon a collection of CaFields attached to EMS element.
"""

import logging
import os
import numpy as np

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from numpy import ndarray
from numpy.testing import assert_almost_equal

from phantasy import Configuration
from phantasy import pass_arg
from phantasy_ui import printlog
from phantasy_apps.wire_scanner.utils import wait as _wait
from .utils import find_dconf

_LOGGER = logging.getLogger(__name__)


TS_FMT = "%Y-%m-%d %H:%M:%S"

XY2ID = {'X': 1, 'Y': 2}


class Device(QObject):
    """Build allison-scanner devices from CaElement, which family is 'EMS',
    After instantiating, the operations like device control, data analysis
    control could be expected.

    Parameters
    ----------
    elem : CaElement
        CaElement object, which is one element of high-level lattice.
    xoy : str
        Define the measurement direction, 'X' or 'Y'.
    dconf : callable or str
        Configuration object for this device, or file path of the
        configuration file (.ini file). If not given, will read from
        the following locations, `~/.phantasy/ems.ini`,
        `/etc/phantasy/ems.ini` or from the package directory, see the
        loaded full path: `Device.dconf.config_path`.
    """

    data_changed = pyqtSignal(ndarray)
    finished = pyqtSignal()

    # pos begin
    pb_changed = pyqtSignal(float)
    # pos end
    pe_changed = pyqtSignal(float)
    # pos step
    ps_changed = pyqtSignal(float)
    # voltage begin
    vb_changed = pyqtSignal(float)
    # voltage end
    ve_changed = pyqtSignal(float)
    # voltage step
    vs_changed = pyqtSignal(float)

    # motor fork pos in status
    status_in_changed = pyqtSignal(bool)
    # motor fork pos out status
    status_out_changed = pyqtSignal(bool)
    # interlock ok status
    status_itlk_ok_changed = pyqtSignal(bool)
    # scan enabled
    status_enabled_changed = pyqtSignal(bool)
    # position readback
    pos_read_changed = pyqtSignal(float)
    # position setpoint
    pos_set_changed = pyqtSignal(float)
    # bias voltage on
    bias_volt_on_changed = pyqtSignal(bool)
    # bias voltage readback
    bias_volt_read_changed = pyqtSignal(float)
    # bias voltage setpoint
    bias_volt_set_changed = pyqtSignal(float)

    def __init__(self, elem, xoy='X', dconf=None):
        super(self.__class__, self).__init__()
        self.elem = elem

        if dconf is None:
            self.dconf = Configuration(find_dconf())
        elif isinstance(dconf, Configuration):
            self.dconf = dconf
        elif isinstance(dconf, str) and os.path.isfile(dconf):
            self.dconf = Configuration(dconf)
        else:
            _LOGGER.error("Cannot find device configuration.")

        # device name
        self.name = name = elem.name
        # orientation
        self.xoy = xoy

        # length: [mm]
        self.length = float(self.dconf.get(name, 'length'))

        # length1,2: [mm]
        self.length1 = float(self.dconf.get(name, 'length1'))
        self.length2 = float(self.dconf.get(name, 'length2'))

        # gap: [mm]
        self.gap = float(self.dconf.get(name, 'gap'))

        # slit, width & thickness: [mm]
        self.slit_width = float(self.dconf.get(name, 'slit_width'))
        self.slit_thickness = float(self.dconf.get(name, 'slit_thickness'))

        # bias volt threshold
        self.bias_volt_threshold = float(self.dconf.get(name, 'bias_volt_threshold'))

        # info, e.g. Installed or not-installed
        self.info = self.dconf.get(name, 'info')

    def update_xoy_conf(self, name: str):
        # xoy
        # default pos/volt alter ranges, [mm], [V], settling time: [sec]
        self.kxoy = kxoy = "{}.{}".format(name, self.xoy)
        self.pos_begin = float(self.dconf.get(kxoy, 'pos_begin'))
        self.pos_end = float(self.dconf.get(kxoy, 'pos_end'))
        self.pos_step = float(self.dconf.get(kxoy, 'pos_step'))
        self.pos_settling_time = float(self.dconf.get(kxoy, 'pos_settling_time'))
        self.volt_begin = float(self.dconf.get(kxoy, 'volt_begin'))
        self.volt_end = float(self.dconf.get(kxoy, 'volt_end'))
        self.volt_step = float(self.dconf.get(kxoy, 'volt_step'))
        self.volt_settling_time = float(self.dconf.get(kxoy, 'volt_settling_time'))

    def get_live_pos(self):
        """Get live readback of position.
        """
        return getattr(self.elem, f"POS{self._id}")

    def get_data(self):
        """Get live value as an array from DATA# field.
        """
        return self.get_data_pv().get()

    def get_data_pv(self):
        """Get the PV object of the DATA# field.
        """
        return self.elem.get_field(f'DATA{self._id}').readback_pv[0]

    def get_data_pvname(self):
        """Get the PV name of the DATA# field.
        """
        return self.get_data_pv().pvname

    @property
    def xoy(self):
        """str: Device is for 'X' measurement or 'Y'."""
        return self._xoy

    @xoy.setter
    def xoy(self, s):
        s = s.upper()
        if s not in ('X', 'Y'):
            s = 'X'
        self._xoy = s
        self._id = XY2ID[self._xoy]
        self.update_xoy_conf(self.name)

    @property
    def name(self):
        """str: Element/device name."""
        return self._name

    @name.setter
    def name(self, s):
        self._name = s

    @property
    def length(self):
        """float: E-dipole plat length, [mm]."""
        return self._length

    @length.setter
    def length(self, x):
        self._length = x
        self.dconf.set(self.name, 'length', str(x))

    @property
    def length1(self):
        """float: Length from slit-entrance to plate, [mm]."""
        return self._length1

    @length1.setter
    def length1(self, x):
        self._length1 = x
        self.dconf.set(self.name, 'length1', str(x))

    @property
    def length2(self):
        """float: Length from plate to slit-exit, [mm]."""
        return self._length2

    @length2.setter
    def length2(self, x):
        self._length2 = x
        self.dconf.set(self.name, 'length2', str(x))

    @property
    def gap(self):
        """float: Distance between plates, [mm]."""
        return self._gap

    @gap.setter
    def gap(self, x):
        self._gap = x
        self.dconf.set(self.name, 'gap', str(x))

    @property
    def slit_width(self):
        """float: Slit width, [mm]."""
        return self._slit_width

    @slit_width.setter
    def slit_width(self, x):
        self._slit_width = x
        self.dconf.set(self.name, 'slit_width', str(x))

    @property
    def slit_thickness(self):
        """float: Slit thickness, [mm]."""
        return self._slit_thickness

    @slit_thickness.setter
    def slit_thickness(self, x):
        self._slit_thickness = x
        self.dconf.set(self.name, 'slit_thickness', str(x))

    @property
    def pos_begin(self):
        """float: Start position of motor, [mm]."""
        return self._pos_begin

    @pos_begin.setter
    def pos_begin(self, x):
        self._pos_begin = x
        self.dconf.set(self.kxoy, 'pos_begin', str(x))

    @property
    def pos_end(self):
        """float: End position of motor, [mm]."""
        return self._pos_end

    @pos_end.setter
    def pos_end(self, x):
        self._pos_end = x
        self.dconf.set(self.kxoy, 'pos_end', str(x))

    @property
    def pos_step(self):
        """float: Step of motor moving, [mm]."""
        return self._pos_step

    @pos_step.setter
    def pos_step(self, x):
        self._pos_step = x
        self.dconf.set(self.kxoy, 'pos_step', str(x))

    @property
    def volt_begin(self):
        """float: Start voltage applied on plates, [V]."""
        return self._volt_begin

    @volt_begin.setter
    def volt_begin(self, x):
        self._volt_begin = x
        self.dconf.set(self.kxoy, 'volt_begin', str(x))

    @property
    def volt_end(self):
        """float: End voltage applied on plates, [V]."""
        return self._volt_end

    @volt_end.setter
    def volt_end(self, x):
        self._volt_end = x
        self.dconf.set(self.kxoy, 'volt_end', str(x))

    @property
    def volt_step(self):
        """float: Step of voltage altering, [V]."""
        return self._volt_step

    @volt_step.setter
    def volt_step(self, x):
        self._volt_step = x
        self.dconf.set(self.kxoy, 'volt_step', str(x))

    @property
    def pos_settling_time(self):
        """float: Settling time of position altering, [sec]."""
        return self._pos_settling_time

    @pos_settling_time.setter
    def pos_settling_time(self, x):
        self._pos_settling_time = x
        self.dconf.set(self.kxoy, 'pos_settling_time', str(x))

    @property
    def volt_settling_time(self):
        """float: Settling time of voltage altering, [sec]."""
        return self._volt_settling_time

    @volt_settling_time.setter
    def volt_settling_time(self, x):
        self._volt_settling_time = x
        self.dconf.set(self.kxoy, 'volt_settling_time', str(x))

    @property
    def bias_volt_threshold(self):
        """float: Threshold of bias voltage applied on FC, [V], the applied
        bias voltage should be less or equal than this value."""
        return self._bias_volt_threshold

    @bias_volt_threshold.setter
    def bias_volt_threshold(self, x):
        self._bias_volt_threshold = x
        self.dconf.set(self.name, 'bias_volt_threshold', str(x))

    def is_bias_volt_ready(self, mode):
        # test if bias voltage (setpoint, readback) for FC is OK.
        if mode == 'setpoint':
            return self.elem.current_setting(field="BIAS_VOLT") <= self.bias_volt_threshold
        else:  # readback
            return self.elem.BIAS_VOLT <= self.bias_volt_threshold

    def init_bias_voltage(self, timeout=10):
        _LOGGER.info("Initialize bias voltage for FC...")
        s1 = self.turn_on_bias_voltage(timeout)
        if s1:
            self.set_bias_voltage(timeout)

    def turn_on_bias_voltage(self, timeout=10):
        _LOGGER.info("Turn on bias voltage for FC...")
        self.elem.ensure_put('BIAS_VOLT_ON', 1, tol=1.0, timeout=timeout)
        if self.elem.BIAS_VOLT_ON == 1:
            _LOGGER.info("Bias voltage switch is ON.")
            return True
        else:
            _LOGGER.info("Bias voltage switch cannot be ON.")
            return False

    def set_bias_voltage(self, timeout=10):
        _LOGGER.info("Set bias voltage for FC...")
        volt = self.bias_volt_threshold
        self.elem.ensure_put('BIAS_VOLT', volt, tol=1.0, timeout=timeout)
        _LOGGER.info("Bias voltage now is {}.".format(self.elem.BIAS_VOLT))
        if self.is_bias_volt_ready('readback'):
            _LOGGER.info("Bias voltage is ready.")
            return True
        else:
            _LOGGER.info("Bias voltage is not ready.")
            return False

    def enable(self, timeout=10):
        """Make device ready for the movement."""
        _LOGGER.info("Enable device...")
        fname = "ENABLE_SCAN{}".format(self._id)
        r = self.elem.ensure_put(fname, 1, tol=1.0, timeout=timeout)
        if r == 'PutFinished':
            _LOGGER.info("Device is enabled.")
            return True
        else:
            _LOGGER.info("Device is not enabled.")
            return False

    def set_pos_begin(self):
        """Set live config with current config."""
        setattr(self.elem, f'START_POS{self._id}', self.pos_begin)

    def set_pos_end(self):
        setattr(self.elem, f'STOP_POS{self._id}', self.pos_end)

    def set_pos_step(self):
        setattr(self.elem, f'STEP_POS{self._id}', self.pos_step)

    def set_volt_begin(self):
        setattr(self.elem, f'START_VOLT{self._id}', self.volt_begin)

    def set_volt_end(self):
        setattr(self.elem, f'STOP_VOLT{self._id}', self.volt_end)

    def set_volt_step(self):
        setattr(self.elem, f'STEP_VOLT{self._id}', self.volt_step)

    def set_pos_settling_time(self):
        setattr(self.elem, f'WAIT_POS{self._id}', self.pos_settling_time)

    def set_volt_settling_time(self):
        setattr(self.elem, f'WAIT_VOLT{self._id}', self.volt_settling_time)

    def get_pos_begin(self):
        """Return live config from controls network."""
        return getattr(self.elem, f'START_POS{self._id}')

    def get_pos_end(self):
        return getattr(self.elem, f'STOP_POS{self._id}')

    def get_pos_step(self):
        return getattr(self.elem, f'STEP_POS{self._id}')

    def get_volt_begin(self):
        return getattr(self.elem, f'START_VOLT{self._id}')

    def get_volt_end(self):
        return getattr(self.elem, f'STOP_VOLT{self._id}')

    def get_volt_step(self):
        return getattr(self.elem, f'STEP_VOLT{self._id}')

    def get_pos_settling_time(self):
        return getattr(self.elem, f'WAIT_POS{self._id}')

    def get_volt_settling_time(self):
        return getattr(self.elem, f'WAIT_VOLT{self._id}')

    def sync_params(self):
        """Pull device config from controls network, update
        regarding attr, and dconf as well.
        """
        ks = ['{}_{}'.format(u, v) for u in ('pos', 'volt')
              for v in ('begin', 'end', 'step', 'settling_time')]
        for s in ks:
            v = getattr(self, 'get_{}'.format(s))()
            setattr(self, s, v)
            _LOGGER.info("Sync '{}' with '{}'.".format(s, v))

    def set_params(self):
        self.set_pos_begin()
        self.set_pos_end()
        self.set_pos_step()
        self.set_volt_begin()
        self.set_volt_end()
        self.set_volt_step()

    def enable_device(self):
        setattr(self.elem, f"ENABLE_SCAN{self._id}", 1)

    def reset_interlock(self):
        printlog(f"Reset interlock for {self.name}")
        setattr(self.elem, 'RESET_ITLK', 1)
        #fld = self.elem.get_field('INTERLOCK{}'.format(self._id))
        #re_tries = 0
        #while fld.value != 0:
        #    re_tries += 1
        #    setattr(self.elem, 'RESET_ITLK', 1)
        #    _wait(fld.readback_pv[0], 0, 5)
        #    if re_tries > 3:
        #        break
        #        print("--- Cannot reset interlock...")
        #        return
        #print("--- Reset interlock-{}: Done!".format(self._id))

    def retract(self, pos0=200.0):
        pos_fld = self.elem.get_field('POS{}'.format(self._id))
        pos_fld.value = pos0
        return pos_fld

    def abort(self):
        setattr(self.elem, 'ABORT_SCAN{}'.format(self._id), 1)

    def move(self, timeout=600, wait=True, validate=False):
        """Start scan."""
        if validate:  # check scan status or not
            s = self.check_status()
            if s != "IDLE":
                raise RuntimeError("Device is busy, not be ready for moving.")

        self.init_data_cb()
        setattr(self.elem, 'START_SCAN{}'.format(self._id), 1)
        if wait:
            _wait(self.get_status_pv(), "IDLE", timeout)
            self._reset_data_cb()
            print("Move is done.")

    def get_status_pv(self):
        ss_fld_name = 'SCAN_STATUS{}'.format(self._id)
        ss_fld = self.elem.get_field(ss_fld_name)
        ss_pv = ss_fld.readback_pv[0]
        return ss_pv

    def check_status(self):
        # Return the scan status
        pv = self.get_status_pv()
        return pv.get(as_string=True)

    def run_all_in_one(self):
        # self.enable()
        self.set_params()
        self.move()
        print("Run-All-in-One is done.")

    def init_run(self):
        self.init_bias_voltage()
        # self.enable()
        self.set_params()

    def init_data_cb(self):
        printlog(f"Initial data cb: {self.name} [{self.xoy}, {self._id}]")
        self.elem.monitor(f"SCAN_STATUS{self._id}", self.onScanStatusUpdated,
                          name=f"SCAN_STATUS{self._id}")
        self.elem.monitor(f"DATA{self._id}", self.onDataUpdated,
                          name=f"DATA{self._id}")

    def _reset_data_cb(self):
        self.elem.unmonitor(f"SCAN_STATUS{self._id}", name=f"SCAN_STATUS{self._id}")
        self.elem.unmonitor(f"DATA{self._id}", name=f"DATA{self._id}")
        self.finished.emit()

    @pass_arg('fld')
    def onScanStatusUpdated(self, fld, **kws):
        """Scan status is updated.
        """
        s = kws.get("char_value")
        if s == "SCAN_DONE":
            self._reset_data_cb()

    @pass_arg('fld')
    def onDataUpdated(self, fld, **kws):
        """Array data is updated.
        """
        value = kws.get("value")
        self.data_changed.emit(value)

    def __repr__(self):
        s = "Device configuration: [{}.{}]".format(self.name, self.xoy)
        s += "\n--- info: {}".format(self.info)
        s += "\n--- length: {0:.2f} mm".format(self.length)
        s += "\n--- length-1: {0:.2f} mm, length-2: {1:.2} mm".format(self.length1, self.length2)
        s += "\n--- gap: {0:.2f} mm".format(self.gap)
        s += "\n--- slit width: {0:.2f} mm".format(self.slit_width)
        s += "\n--- slit thickness: {0:.2f} mm".format(self.slit_thickness)
        s += "\n--- bias voltage threshold: {} V".format(self.bias_volt_threshold)
        s += "\n--- pos [mm] start: {0:.1f}, end: {1:.1f}, step: {2:.1f}".format(self.pos_begin, self.pos_end, self.pos_step)
        s += "\n--- volt [V] start: {0:.1f}, end: {1:.1f}, step: {2:.1f}".format(self.volt_begin, self.volt_end, self.volt_step)
        s += "\n--- settling time [s], pos: {0:.1f}, volt: {1:.1f}".format(self.pos_settling_time, self.volt_settling_time)
        return s

    def save_dconf(self, filepath):
        with open(filepath, 'w') as f:
            self.dconf.write(f)

    def __eq__(self, other):
        xoy0, xoy0_other = self.xoy, other.xoy
        attr_all = ('bias_volt_threshold', 'gap',
                    'length', 'length1', 'length2',
                    'slit_width', 'slit_thickness',
                    'pos_begin', 'pos_end', 'pos_step',
                    'pos_settling_time',
                    'volt_begin', 'volt_end', 'volt_step',
                    'volt_settling_time')
        for xoy in ['X', 'Y']:
            self.xoy = xoy
            other.xoy = xoy
            for i in attr_all:
                if getattr(self, i) != getattr(other, i):
                    self.xoy = xoy0
                    other.xoy = xoy0_other
                    return False

        self.xoy = xoy0
        other.xoy = xoy0_other
        return True

    @property
    def geometric_factor(self):
        """float: Geometric factor based on device configuration.
        """
        l_total = self.length + self.length1 + self.length2
        return (self.length + 2 * self.length2) / l_total

    @property
    def prefactor1(self):
        return (self.length + 2 * self.length1) / (self.length + 2 * self.length2)

    @property
    def prefactor2(self):
        l_total = self.length + self.length1 + self.length2
        slit_thickness = self.slit_thickness
        return slit_thickness * 2 * (self.length2 - self.length1) / \
                l_total / (l_total + 2 * slit_thickness)

    @property
    def dxp0(self):
        # delta_x'
        return 2 * self.slit_width / (self.length + self.length1 + self.length2)

    def monitor(self):
        """Monitor field value changes.
        """
        oid = self._id
        self.elem.monitor(f"STATUS_IN{oid}", self.onUpdateStatusIn)
        self.elem.monitor(f"STATUS_OUT{oid}", self.onUpdateStatusOut)
        self.elem.monitor(f"INTERLOCK{oid}", self.onUpdateStatusInterlockOK)
        self.elem.monitor(f"POS{oid}", self.onUpdatePosRead)
        self.elem.monitor(f"POS{oid}", self.onUpdatePosSet, "setpoint")
        self.elem.monitor(f"ENABLE_SCAN{oid}", self.onUpdateStatusEnabled)
        self.elem.monitor(f"BIAS_VOLT_ON", self.onUpdateBiasVoltOn)
        self.elem.monitor(f"BIAS_VOLT", self.onUpdateBiasVoltRead)
        self.elem.monitor(f"BIAS_VOLT", self.onUpdateBiasVoltSet, "setpoint")

        # pos scan range
        self.elem.monitor(f"START_POS{oid}", self.onUpdatePosBegin)
        self.elem.monitor(f"STOP_POS{oid}", self.onUpdatePosEnd)
        self.elem.monitor(f"STEP_POS{oid}", self.onUpdatePosStep)
        # volt scan range
        self.elem.monitor(f"START_VOLT{oid}", self.onUpdateVoltBegin)
        self.elem.monitor(f"STOP_VOLT{oid}", self.onUpdateVoltEnd)
        self.elem.monitor(f"STEP_VOLT{oid}", self.onUpdateVoltStep)

    def unmonitor(self):
        """Stop monitor field value changes for both X and Y.
        """
        [self.elem.unmonitor(f"STATUS_IN{i}") for i in (1, 2)]
        [self.elem.unmonitor(f"STATUS_OUT{i}") for i in (1, 2)]
        [self.elem.unmonitor(f"START_POS{i}") for i in (1, 2)]
        [self.elem.unmonitor(f"STOP_POS{i}") for i in (1, 2)]
        [self.elem.unmonitor(f"STEP_POS{i}")  for i in (1, 2)]
        [self.elem.unmonitor(f"START_VOLT{i}") for i in (1, 2)]
        [self.elem.unmonitor(f"STOP_VOLT{i}") for i in (1, 2)]
        [self.elem.unmonitor(f"STEP_VOLT{i}") for i in (1, 2)]
        [self.elem.unmonitor(f"INTERLOCK{i}") for i in (1, 2)]
        [self.elem.unmonitor(f"POS{i}") for i in (1, 2)]
        [self.elem.unmonitor(f"POS{i}", handle="setpoint") for i in (1, 2)]
        [self.elem.unmonitor(f"ENABLE_SCAN{i}") for i in (1, 2)]
        self.elem.unmonitor("BIAS_VOLT_ON")
        self.elem.unmonitor("BIAS_VOLT")
        self.elem.unmonitor("BIAS_VOLT", handle="setpoint")

    @pass_arg('fld')
    def onUpdatePosBegin(self, fld, **kws):
        value = kws.get('value')
        self.pb_changed.emit(value)

    @pass_arg('fld')
    def onUpdatePosEnd(self, fld, **kws):
        value = kws.get('value')
        self.pe_changed.emit(value)

    @pass_arg('fld')
    def onUpdatePosStep(self, fld, **kws):
        value = kws.get('value')
        self.ps_changed.emit(value)

    @pass_arg('fld')
    def onUpdateVoltBegin(self, fld, **kws):
        value = kws.get('value')
        self.vb_changed.emit(value)

    @pass_arg('fld')
    def onUpdateVoltEnd(self, fld, **kws):
        value = kws.get('value')
        self.ve_changed.emit(value)

    @pass_arg('fld')
    def onUpdateVoltStep(self, fld, **kws):
        value = kws.get('value')
        self.vs_changed.emit(value)

    @pass_arg('fld')
    def onUpdateStatusIn(self, fld, **kws):
        # motor fork (pos) in status
        value = kws.get('value')
        # print(f"{self.name}[{self.xoy}] STATUS_IN: {value} {value==1.0}")
        self.status_in_changed.emit(value==1.0)

    @pass_arg('fld')
    def onUpdateStatusOut(self, fld, **kws):
        # motor fork (pos) out status
        value = kws.get('value')
        # print(f"{self.name}[{self.xoy}] STATUS_OUT: {value} {value==1.0}")
        self.status_out_changed.emit(value==1.0)

    @pass_arg('fld')
    def onUpdateStatusInterlockOK(self, fld, **kws):
        # motor fork interlock status
        value = kws.get('value')
        self.status_itlk_ok_changed.emit(value==0.0)

    @pass_arg('fld')
    def onUpdatePosRead(self, fld, **kws):
        value = kws.get('value')
        self.pos_read_changed.emit(value)

    @pass_arg('fld')
    def onUpdatePosSet(self, fld, **kws):
        value = kws.get('value')
        self.pos_set_changed.emit(value)

    @pass_arg('fld')
    def onUpdateStatusEnabled(self, fld, **kws):
        value = kws.get('value')
        self.status_enabled_changed.emit(value==1.0)

    @pass_arg('fld')
    def onUpdateBiasVoltOn(self, fld, **kws):
        value = kws.get('value')
        self.bias_volt_on_changed.emit(value==1.0)

    @pass_arg('fld')
    def onUpdateBiasVoltRead(self, fld, **kws):
        value = kws.get('value')
        self.bias_volt_read_changed.emit(value)

    @pass_arg('fld')
    def onUpdateBiasVoltSet(self, fld, **kws):
        value = kws.get('value')
        self.bias_volt_set_changed.emit(value)

    def is_pos_at_begin(self):
        """Test if motor is at the begin position.
        """
        print(f"Reached begin test: {self.name} [{self.xoy}]")
        live_pos = self.get_live_pos() 
        begin_pos = self.get_pos_begin()
        if np.abs(live_pos - begin_pos) < 0.05:
            return True
        return False