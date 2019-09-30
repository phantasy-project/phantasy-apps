# -*- coding: utf-8 -*-

import random
import time

import epics
from PyQt5.QtCore import QEventLoop
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMessageBox

# https://getbootstrap.com/docs/4.0/utilities/colors/
COLOR_DANGER = QColor('#DC3545')
COLOR_INFO = QColor('#17A2B8')
COLOR_WARNING = QColor('#FFC107')
COLOR_PRIMARY = QColor('#007BFF')


class PVElement(object):
    """Unified interface for `get` and `put` operations to a PV.

    Examples
    --------
    >>> elem = PVElement('VA:LS1_BTS:QH_D1942:I_CSET',
                         'VA:LS1_BTS:QH_D1942:I_RD')
    >>> elem.value # get value
    >>> elem.value = 1 # put with a new value
    """

    def __init__(self, put_pv_name, get_pv_name):
        self._put_pvname = put_pv_name
        self._get_pvname = get_pv_name
        self._putPV = epics.PV(put_pv_name)
        self._getPV = epics.PV(get_pv_name)

    @property
    def fname(self):
        """Default CA field name.
        """
        return self.pvname[0]

    name = fname

    @property
    def value(self):
        """generic attribute name to present this PV element's value.
        """
        return self._getPV.get()

    @value.setter
    def value(self, x):
        self._putPV.put(x, wait=True)

    @property
    def connected(self):
        return self._putPV.connected and self._getPV.connected

    def __repr__(self):
        return "Element: {name}, cset: {cset}, rd: {rd}".format(
            name=self.name, cset=str(self._putPV), rd=str(self._getPV))

    def get_pv_name(self, type='readback'):
        if type == 'readback':
            pv = self._get_pvname
        elif type == 'setpoint':
            pv = self._put_pvname
        return pv

    @property
    def pvname(self):
        return self._put_pvname, self._get_pvname

    @property
    def ename(self):
        """just guess element name.
        """
        a, b = self.get_pv_name('readback'), self.get_pv_name('setpoint')
        n = set(a.rsplit(':', 1)).intersection(b.rsplit(':', 1))
        if n:
            return n.pop()
        else:
            return 'undefined'

    @property
    def readback(self):
        return [self._get_pvname]

    @property
    def setpoint(self):
        return [self._put_pvname]

    @property
    def readback_pv(self):
        return [self._getPV]

    @property
    def setpoint_pv(self):
        return [self._putPV]


class PVElementReadonly(object):
    """Unified interface for `get` to a PV, i.e. readonly.

    Examples
    --------
    >>> elem = PVElement('VA:LS1_BTS:QH_D1942:I_RD')
    >>> elem.value # get value
    """

    def __init__(self, get_pv_name):
        self._get_pvname = get_pv_name
        self._getPV = epics.PV(get_pv_name)

    @property
    def fname(self):
        """Default CA field name.
        """
        return self.pvname[0]

    name = fname

    @property
    def value(self):
        """generic attribute name to present this PV element's value.
        """
        return self._getPV.get()

    @property
    def connected(self):
        return self._getPV.connected

    def __repr__(self):
        return "Element: {name}, rd: {rd}".format(
            name=self.name, rd=str(self._getPV))

    @property
    def pvname(self):
        return self._get_pvname,

    @property
    def ename(self):
        """just guess element name.
        """
        return self.get_pv_name('readback').rsplit(':', 1)[0]

    @property
    def readback(self):
        return [self.get_pv_name('readback')]

    @property
    def setpoint(self):
        return []

    @property
    def readback_pv(self):
        return [self._getPV]

    def get_pv_name(self, type='readback'):
        if type == 'readback':
            pv = self._get_pvname
        elif type == 'setpoint':
            pv = self._put_pvname
        return pv


def delayed_exec(f, delay, *args, **kws):
    """Execute *f* after *delay* msecm `*args` and `**kws` is for *f*.
    """

    def func():
        return f(*args, **kws)

    QTimer.singleShot(delay, func)


def milli_sleep(qApp, msec):
    t0 = time.time()
    while (time.time() - t0) * 1000 < msec:
        qApp.processEvents()


def milli_sleep1(msec):
    loop = QEventLoop()
    QTimer.singleShot(msec, loop.exit)
    loop.exec_()


def delayed_check_pv_status(obj, pvelem, delay=1000):
    """Check PV element connected or not.

    Parameters
    ----------
    obj :
        Widget, as parent.
    pvelem : obj
        Instance of `epics.PV`, `PVElement`, `PVElementReadonly`.
    delay : float
        Delay milliseconds to check PV status.
    """

    def check_status(elem):
        if not elem.connected:
            QMessageBox.warning(obj, "Warning",
                                "Cannot connect to the input PV(s).",
                                QMessageBox.Ok)

    QTimer.singleShot(delay, lambda: check_status(pvelem))
