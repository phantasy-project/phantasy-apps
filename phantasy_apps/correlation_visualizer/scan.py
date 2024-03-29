#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from collections import OrderedDict

import numpy as np
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import pyqtSignal
from phantasy import CaField
from phantasy import MachinePortal
from phantasy import ensure_get
from phantasy import ensure_put
from phantasy import PVElement
from phantasy import PVElementReadonly
from phantasy.library.physics.devices import process_devices

from phantasy_ui import printlog
from phantasy_apps.utils import current_datetime
from phantasy_apps.correlation_visualizer.data import JSONDataSheet
from phantasy_apps.correlation_visualizer.alter_actions import DEFAULT_ALTER_ACTION
from phantasy_apps.correlation_visualizer.alter_actions import DEFAULT_ALTER_ACTION_CODE
from phantasy_ui import random_string
from phantasy_ui import milli_sleep
from phantasy_ui.widgets import str2func


class ScanTask(object):
    """Class to abstract scan routine.
    """

    def __init__(self, name, mode="1D"):
        # task name identifier
        self.name = name

        # mode: 1D or 2D
        self.mode = mode

        # nested task for 2D
        self._nested_task = None

        # start timestamp
        self._ts_start = time.time()
        # stop timestamp
        self._ts_stop = time.time()

        # element to scan
        self._alter_elem = None

        # element to monitor (main)
        self._monitor_elem = None

        # high-level lattice
        self._lattice = None

        # array mode bit
        self._array_mode = None

        # additional monitors
        self._extra_monitor_elem = []

        # scan start value
        self._alter_start = 0
        # scan stop value
        self._alter_stop = 1
        # number of scan point
        self._alter_number = 10
        # shot/iter
        self._shotnum = 5

        # timeout in sec
        self._wait_sec = 1.0

        # extra wait in sec
        self._extra_wait_sec = 0.0

        # daq rate
        self._daq_rate = 1.0

        # alter action, mode: 'regular'
        self.alter_action = None
        self.alter_action_code = None

        # initialize out data
        self.init_out_data()
        # set alter array
        self.set_alter_array()

    @property
    def mode(self):
        """str: Mode of scan task.
        """
        return self._mode

    @mode.setter
    def mode(self, s):
        self._mode = "1D" if s is None else s

    @property
    def name(self):
        """str: Name of scan task.
        """
        return self._name

    @name.setter
    def name(self, s):
        if s is None:
            s = random_string(6)
        self._name = s

    @property
    def ts_start(self):
        """float: Timestamp of when task starts, epoch sec.
        """
        return self._ts_start

    @ts_start.setter
    def ts_start(self, t):
        self._ts_start = t

    @property
    def ts_stop(self):
        """float: Timestamp of when task stops, epoch sec.
        """
        return self._ts_stop

    @ts_stop.setter
    def ts_stop(self, t):
        self._ts_stop = t

    @property
    def alter_element(self):
        """obj: Element object to alter.
        """
        return self._alter_elem

    @alter_element.setter
    def alter_element(self, o):
        self._alter_elem = o
        self.set_initial_setting()

    @property
    def monitor_element(self):
        """obj: Element object to monitor.
        """
        return self._monitor_elem

    @monitor_element.setter
    def monitor_element(self, o):
        self._monitor_elem = o

    def add_extra_monitor(self, elem):
        """Add one extra monitor.
        """
        if elem in self._extra_monitor_elem:
            return
        self._extra_monitor_elem.append(elem)

    def del_extra_monitor(self, i):
        """Delete one extra monitor according to index *i*.
        """
        self._extra_monitor_elem.pop(i)

    def add_extra_monitors(self, elems):
        """Add a list of elems as extra monitors.
        """
        for elem in elems:
            if elem not in self._extra_monitor_elem:
                self._extra_monitor_elem.append(elem)

    def get_extra_monitors(self):
        """Return all extra monitor elements.
        """
        return self._extra_monitor_elem

    @property
    def alter_action_code(self):
        """str: Definition of alter action.
        """
        return self._alter_action_code

    @alter_action_code.setter
    def alter_action_code(self, s=None):
        if s is None:
            self._alter_action_code = DEFAULT_ALTER_ACTION_CODE
        else:
            self._alter_action_code = s

    @property
    def alter_action(self):
        """Function for setting alter element with the new value.
        """
        return self._alter_action

    @alter_action.setter
    def alter_action(self, fn=None):
        if fn is None:
            self._alter_action = DEFAULT_ALTER_ACTION
            self._alter_action_mode = 'regular'
        else:
            self._alter_action = fn
            self._alter_action_mode = 'advanced'

    @property
    def alter_start(self):
        """float: Begining value where scan starts.
        """
        return self._alter_start

    @alter_start.setter
    def alter_start(self, x):
        self._alter_start = x
        self.set_alter_array()

    @property
    def alter_stop(self):
        """float: Ending value where scan stops.
        """
        return self._alter_stop

    @alter_stop.setter
    def alter_stop(self, x):
        self._alter_stop = x
        self.set_alter_array()

    @property
    def alter_number(self):
        """int: Total number of points of scan routine,
        one point is one iteration.
        """
        return self._alter_number

    @alter_number.setter
    def alter_number(self, n):
        self._alter_number = n
        self.set_alter_array()

    @property
    def shotnum(self):
        """int: Total number of DAQ event within each iteration.
        """
        return self._shotnum

    @shotnum.setter
    def shotnum(self, n):
        self._shotnum = n

    @property
    def t_wait(self):
        """float: Maximum wait time in second for each ensure set.
        """
        return self._wait_sec

    @t_wait.setter
    def t_wait(self, s):
        self._wait_sec = s

    @property
    def t_wait_extra(self):
        """float: Additional wait time in second after each ensure set point.
        """
        return self._extra_wait_sec

    @t_wait_extra.setter
    def t_wait_extra(self, s):
        self._extra_wait_sec = s

    @property
    def daq_rate(self):
        """float: DAQ rate in Hz of fetching monitor values.
        """
        return self._daq_rate

    @daq_rate.setter
    def daq_rate(self, x):
        self._daq_rate = x

    @property
    def tolerance(self):
        """float: The tolerated discrepancy between readback and set value
        of alter element.
        """
        return self._tol

    @tolerance.setter
    def tolerance(self, x):
        self._tol = x

    @property
    def array_mode(self):
        return self._array_mode

    @array_mode.setter
    def array_mode(self, f):
        """If arbitary array input as alter range is enabled.
        """
        self._array_mode = f

    def get_alter_array(self):
        return self._alter_array

    def set_alter_array(self, array=None):
        """Set up the value array for alter elem scan.
        if *array* is defined, use passed *array*.
        """
        if array is not None:
            self._alter_array = np.array(array)
            # update new start, stop and number
            self._alter_start = array[0]
            self._alter_stop = array[-1]
            self._alter_number = self._alter_array.size
        else:
            v1, v2, n = self.alter_start, self.alter_stop, self.alter_number
            self._alter_array = np.linspace(v1, v2, n)

    def init_out_data(self):
        """Initialize array for scan output data.
        """
        ndim = 2 + len(self.get_extra_monitors())
        self._scan_out_per_iter = np.zeros((self.shotnum, ndim))
        self._scan_out_all = np.asarray([
            [np.ones(ndim) * np.nan] * self.shotnum] * self.alter_number)

    @property
    def scan_out_data_per_iter(self):
        return self._scan_out_per_iter

    @property
    def scan_out_data(self):
        return self._scan_out_all

    @scan_out_data.setter
    def scan_out_data(self, arr):
        self._scan_out_all = arr

    def __repr__(self):
        if self.mode == "1D":
            return "Scan Task: {name}\n" \
                   "Task Mode: 1D\n" \
                   "Timeout [s]: {twait}\n" \
                   "Extra wait time [s]: {extra_twait}\n" \
                   "Shot Num: {nshot}\n" \
                   "DAQ Rate: {rate}\n" \
                   "Array mode: {array_mode}\n" \
                   "Alter array: {array}\n" \
                   "Alter Number: {niter}\n" \
                   "Alter start: {sstart}\n" \
                   "Alter stop: {sstop}\n" \
                   "Alter element: {alter}\n" \
                   "Monitor element: {moni}\n" \
                   "Extra monitors: {extra_moni}\n" \
                .format(
                name=self.name,
                niter=self.alter_number,
                twait=self.t_wait,
                extra_twait=self.t_wait_extra,
                nshot=self.shotnum,
                rate=self.daq_rate,
                sstart=self.alter_start,
                sstop=self.alter_stop,
                array_mode=self.array_mode,
                array=str(self.get_alter_array()),
                alter=self.print_element(self.alter_element),
                moni=self.print_element(self.monitor_element),
                extra_moni=[self.print_element(i) for i in self.get_extra_monitors()],)
        else:
            nested_task = self.get_nested_task()
            if nested_task is None:
                nested_task_name = 'undefined'
            else:
                nested_task_name = nested_task.name
            return "Scan Task: {name}\n" \
                   "Task Mode: 2D\n" \
                   "Timeout [s]: {twait}\n" \
                   "Extra wait time [s]: {extra_twait}\n" \
                   "Array mode: {array_mode}\n" \
                   "Alter array: {array}\n" \
                   "Alter Number: {niter}\n" \
                   "Alter start: {sstart}\n" \
                   "Alter stop: {sstop}\n" \
                   "Alter element: {alter}\n" \
                   "Nested Task: {nname}\n" \
                .format(
                name=self.name,
                niter=self.alter_number,
                twait=self.t_wait,
                extra_twait=self.t_wait_extra,
                sstart=self.alter_start,
                sstop=self.alter_stop,
                array_mode=self.array_mode,
                array=str(self.get_alter_array()),
                alter=self.print_element(self.alter_element),
                nname=nested_task_name)

    def get_nested_task(self):
        """Return nested task, only for 2D mode.
        """
        return self._nested_task

    def set_nested_task(self, scan_task):
        """Set 1D scan task as inner loop, only for 2D mode.

        Parameters
        ----------
        scan_task :
            1D scan task instance.
        """
        self._nested_task = scan_task

    def is_valid(self):
        """Check scan task, if valid return True, otherwise return False.
        """
        try:
            if not self.alter_element.connected:
                return False
            if not self.monitor_element.connected:
                return False
            return True
        except:
            return False

    def set_initial_setting(self):
        """Set initial setting for alter element.
        Every time set alter element, set initial setting.
        """
        sppv = self.alter_element.setpoint_pv[0]
        self._val0 = ensure_get(sppv.pvname)

    def get_initial_setting(self):
        """Return the initial setting of alter element.
        """
        return self._val0

    def to_datasheet(self):
        """return JSONDataSheet object.
        """
        data_sheet = JSONDataSheet()
        # task
        task_dict = OrderedDict()
        task_dict['name'] = self.name
        task_dict['mode'] = mode = self.mode
        task_dict['start'] = current_datetime(self.ts_start)
        task_dict['stop'] = current_datetime(self.ts_stop)
        task_dict['duration'] = self.ts_stop - self.ts_start
        task_dict['n_iteration'] = self.alter_number
        if mode == '1D':
            task_dict['n_shot'] = self.shotnum
            task_dict['n_dim'] = 2 + len(self.get_extra_monitors())
            task_dict['daq_rate'] = self.daq_rate
        task_dict['scan_range'] = self.get_alter_array().tolist()
        task_dict['t_wait'] = self.t_wait
        task_dict['t_wait_extra'] = self.t_wait_extra
        task_dict['tolerance'] = self.tolerance
        data_sheet.update({'task': task_dict})

        # alter action
        action_dict = OrderedDict()
        action_dict['mode'] = self._alter_action_mode
        action_dict['function'] = {
                'name': self._alter_action.__name__,
                'code': self._alter_action_code}
        data_sheet.update({'alter_action': action_dict})

        # devices
        dev_dict = OrderedDict()
        dev_dict['alter_element'] = {
            'name': self.alter_element.ename,
            'field': self.alter_element.name,
            'readback_pv': self.alter_element.get_pv_name('readback'),
            'setpoint_pv': self.alter_element.get_pv_name('setpoint'),
        }
        dev_dict['monitors'] = []
        for elem in [self.monitor_element] + self.get_extra_monitors():
            if elem is None:
                continue
            dev_dict['monitors'].append({
                'name': elem.ename,
                'field': elem.name,
                'readback_pv': elem.get_pv_name('readback'),
            })
        data_sheet.update({'devices': dev_dict})

        # data
        data_dict = OrderedDict()
        data_dict['created'] = current_datetime()
        data_dict['shape'] = self.scan_out_data.shape
        data_dict['array'] = self.scan_out_data.tolist()
        data_sheet.update({'data': data_dict})

        return data_sheet

    @staticmethod
    def print_element(elem):
        if isinstance(elem, CaField):
            print_name = '{0} [{1}]'.format(elem.ename, elem.name)
        else:
            print_name = elem.ename
        return print_name

    @property
    def lattice(self):
        return self._lattice

    @lattice.setter
    def lattice(self, o):
        """MachinePortal instance.
        """
        self._lattice = o


def load_lattice(mach, segm, o):
    if o is None:
        mp = MachinePortal(mach, segm)
        printlog("Loading new machine: {}/{}.".format(mach, segm))
    elif mach == o.last_machine_name:
        o.load_lattice(segm)
        if segm != o.last_lattice_name:
            msg = "Loading new segment: {}/{}.".format(mach, segm)
        else:
            msg = "Reloading segment: {}/{}.".format(mach, segm)
        printlog(msg)
        mp = o
    else:
        mp = MachinePortal(mach, segm)
        printlog("Loading new machine: {}/{}.".format(mach, segm))
    return mp


def load_task(filepath, o, mach="FRIB", segm="LINAC"):
    """Instantiate ScanTask from the saved JSON file from CV app.
    """
    task = JSONDataSheet(filepath)

    name = task['task'].get('name', None)
    mode = task['task'].get('mode', '1D')
    scan_task = ScanTask(name, mode=mode)
    scan_task.alter_number = task['task']['n_iteration']
    scan_task.t_wait = task['task']['t_wait']
    scan_task.t_wait_extra = task['task'].get('t_wait_extra', 0.0)
    scan_task.tolerance = task['task'].get('tolerance', 0.10)
    if mode == "1D":
        scan_task.shotnum = task['task']['n_shot']
        scan_task.daq_rate = task['task']['daq_rate']
    array_mode = task['task'].get('array_mode', False)
    array = task['task']['scan_range']
    scan_task.set_alter_array(array)
    scan_task.array_mode = array_mode

    # alter action
    default_action_dict = {'mode': 'regular', 'function': None}
    alter_action_dict = task.get('alter_action', default_action_dict)
    if alter_action_dict['mode'] == 'regular':
        scan_task.alter_action = None
    else:
        f_name = alter_action_dict['function']['name']
        f_code = alter_action_dict['function']['code']
        scan_task.alter_action_code = f_code
        scan_task.alter_action = str2func(f_code, func_name=f_name)

    # acquired data
    scan_task.scan_out_data = np.asarray(task['data']['array'])

    # mp
    machine = task['task'].get('machine', mach)
    segment = task['task'].get('segment', segm)
    printlog("Starting to load lattice for task '{}'.".format(scan_task.name))
    mp = load_lattice(machine, segment, o)
    if mp.last_load_success:
        scan_task.lattice = mp
    milli_sleep(100)
    printlog("Loaded {}/{} for task '{}'.".format(machine, segment, scan_task.name))

    # alter device
    alter_objs = read_element(task, 'alter_element', mp)

    scan_task.alter_element = alter_objs[0][0]
    scan_task._alter_element_display = alter_objs[1][0]
    if mode == "1D":
        # monitor
        moni_objs = read_element(task, 'monitor', mp)
        scan_task.monitor_element = moni_objs[0][0]
        scan_task._monitor_element_display = moni_objs[1][0]
        # extra monitor
        extra_moni_objs = read_element(task, 'extra', mp)
        scan_task.add_extra_monitors(extra_moni_objs[0])
        scan_task._extra_moni_display = extra_moni_objs[1]
    else:  # 2D
        nested_task_filepath = task['task']['nested_task']['filepath']
        nested_task = load_task(
                locate_nested_datafile(filepath, nested_task_filepath),
                mp) # 1D and 2D widget only load the same lattice.
        scan_task.set_nested_task(nested_task)

    return scan_task


class ScanWorker(QObject):
    """Perform scan routine.

    Parameters
    ----------
    scantask :
        `ScanTask` instance, describe scan.
    starting_index : int
        Starting index of scan routine.
    index_array : list
        List of indices of scan, if defined, overrides *starting_index*.
    """
    # the whole scan routine is done
    scanFinished = pyqtSignal()
    # scan routine is stopped by STOP btn
    scanStopped = pyqtSignal()
    # scan routine is stopped at (index, value)
    scanStoppedAt = pyqtSignal(int, float)
    # scan routine is paused by PAUSE btn
    scanPaused = pyqtSignal()
    scanPausedAtIndex = pyqtSignal(int)
    # one iteration is done, param: index and value, array
    scanOneIterFinished = pyqtSignal(int, float, QVariant)
    # scan is done, param: scan out data array
    scanAllDataReady = pyqtSignal(QVariant)

    def __init__(self, scantask, starting_index=0, index_array=None,
                 parent=None):
        super(ScanWorker, self).__init__()
        self.task = scantask
        self.parent = parent
        self.run_flag = True
        self.pause_flag = False
        self.starting_index = starting_index
        self.index_array = index_array

    def run(self):
        # enames of wire-scanners that have been processed

        nshot = self.task.shotnum
        alter_array = self.task.get_alter_array()
        alter_elem = self.task.alter_element
        monitor_elem = self.task.monitor_element
        extra_monitors = self.task.get_extra_monitors()
        all_monitors = [alter_elem, monitor_elem] + extra_monitors
        out_data = self.task.scan_out_data
        tmp_data = self.task.scan_out_data_per_iter
        wait_sec = self.task.t_wait
        extra_wait_sec = self.task.t_wait_extra
        tol = self.task.tolerance
        daq_rate = self.task.daq_rate
        daq_delt = 1.0 / daq_rate
        alter_action = self.task.alter_action

        index_array = range(self.starting_index, alter_array.size)

        # override index_array if arbitrary index array is defined
        # could be activated by RETAKE
        if self.index_array is not None:
            index_array = self.index_array

        for idx, x in enumerate(alter_array):

            self._processed_ws = []

            if idx not in index_array:
                continue

            if not self.run_flag:
                printlog("Break scan by STOP button.")
                self.scanStopped.emit()
                self.scanStoppedAt.emit(idx, alter_array[idx - 1])
                break

            if self.pause_flag:
                # save current idx, resume at this idx
                printlog("Break scan by PAUSE button.")
                self.scanPaused.emit()
                self.scanPausedAtIndex.emit(idx)
                break

            alter_action(x, alter_elem=alter_elem, tolerance=tol,
                         timeout=wait_sec, extra_wait=extra_wait_sec, alter_idx=idx)

            # DAQ
            for i in range(nshot):
                # tmp_data[i, :] = [elem.value for elem in all_monitors]
                tmp_data[i, :] = self.get_readings(i, all_monitors)
                time.sleep(daq_delt)
            out_data[idx, :, :] = tmp_data
            self.scanOneIterFinished.emit(idx, x, out_data)

        if idx == alter_array.size - 1:
            self.scanAllDataReady.emit(out_data)
            self.scanFinished.emit()
        #
        self.run_flag = False

    def get_readings(self, i, all_elements):
        # all_elements: list of PVElement/Readonly, or CaField
        readings = []
        for elem in all_elements:
            ename = elem.ename
            if not self.parent.is_virtual_mode():
                if 'PM' in ename and 'BPM' not in ename:
                    self.process_ws(ename)
            readings.append(elem.value)
        return readings

    def stop(self):
        """Stop scan worker
        """
        self.run_flag = False

    def pause(self):
        """Pause scan worker
        """
        self.pause_flag = True

    def is_running(self):
        """Return if scan task is running or not.
        """
        return self.run_flag

    def process_ws(self, ename, machine="FRIB", segment="LINAC"):
        if ename in self._processed_ws:
            return
        print("Processing", ename)

        from phantasy import MachinePortal
        mp = MachinePortal(machine, segment)
        elem = mp.get_elements(name=ename)[0]
        process_devices((elem, ))

#        from phantasy import MachinePortal
#        from phantasy_apps.wire_scanner.device import Device
#        from phantasy_apps.wire_scanner.device import PMData
#        #
#        if "MEBT" in ename: segment = "MEBT"
#        mp = MachinePortal(machine, segment)
#        # process wire-scanner
#        elem = mp.get_elements(name=ename)[0]
#        ws = Device(elem)
#        # online
#        print("Run device...")
#        ws.run_all()
#        print("Sync data...")
#        ws.sync_data(mode='live')
#        # offline
#        # ws.sync_data(mode='file', filename=fn)
#        print("Analyzing data...")
#        ws_data = PMData(ws)
#        ws_data.analyze()
#        print("Sync results to device...")
#        ws_data.sync_results_to_ioc()

        # put processed flag
        self._processed_ws.append(ename)


def read_element(task, etype, mp):
    """Read element(field object to scan) from task config.

    Parameters
    ----------
    task : dict
        JSON data sheet.
    etype: str
        One of 'alter_element', 'monitor', 'extra'.
    mp :
        MachinePortal instance.

    Returns
    -------
    r : tuple
        List of field obj, and list of elem obj.
    """
    if etype == 'alter_element':
        elem_confs = [task['devices']['alter_element']]
    elif etype == 'monitor':
        elem_confs = [task['devices']['monitors'][0]]
    elif etype == 'extra':
        elem_confs = task['devices']['monitors'][1:]

    elems = []
    flds = []
    for conf in elem_confs:
        ename = conf.get('name')
        fname = conf.get('field')
        if not ':' in fname:
            elem = mp.get_elements(name=ename)[0]
            fld = elem.get_field(fname)
        else:
            rdbk_pv = conf.get('readback_pv')
            if etype == 'alter_element':
                cset_pv = conf.get('setpoint_pv')
                fld = PVElement(cset_pv, rdbk_pv)
            else:
                fld = PVElementReadonly(rdbk_pv)
            # time.sleep(2.0)
            elem = fld
        flds.append(fld)
        elems.append(elem)
    return flds, elems


def locate_nested_datafile(filepath1, filepath2):
    """Locate the fullpath of 1D scan task data file.

    Parameters
    ----------
    filepath1: str
        Fullpath of 2D scan task data file.
    filepath2: str
        Relative path of 1D scan task.

    Returns
    -------
    r : str
        Fullpath of nested 1D scan task data file.
    """
    if os.path.isabs(filepath2):
        filename = os.path.basename(filepath2)
    else:
        filename = filepath2
    return os.path.join(os.path.dirname(filepath1), filename)


if __name__ == '__main__':
    task = ScanTask("SCAN #1")
    print(task)

    task.alter_start = 0
    task.alter_stop = 10
    task.alter_number = 10
    print(task.get_alter_array(), task.alter_step)

    task.alter_stop = -10
    print(task.get_alter_array())

    task.alter_number = 5
    print(task.get_alter_array())

    task.alter_start = 10
    print(task.get_alter_array())

    task.set_alter_array([1, 3, 4, 5])
    print(task.get_alter_array())
    print(task.alter_start, task.alter_stop, task.alter_number, task.alter_step)
