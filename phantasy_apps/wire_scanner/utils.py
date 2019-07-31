#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

import numpy as np
from mpl4qt.widgets.utils import MatplotlibCurveWidgetSettings
from phantasy import epoch2human
from phantasy_apps.utils import find_dconf as _find_dconf

_LOGGER = logging.getLogger(__name__)

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty


class QCallback(object):
    def __init__(self, q, goal):
        self.q = q
        self.goal = goal

    def __call__(self, **kws):
        val = kws.get('value')
        if val == self.goal:
            self.q.put(val)
            idx, obj = kws.get('cb_info')
            obj.remove_callback(idx)


def wait(pv, goal, timeout=60):
    if pv.value == goal:
        _LOGGER.warning("Already reached {}...".format(goal))
        return
    q = Queue(1)
    cid = pv.add_callback(QCallback(q, goal))
    try:
        if q.get(timeout=timeout):
            _LOGGER.info("{} reached, unblocking...".format(goal))
    except Empty:
        _LOGGER.warning("Timeout, no changes detected.")
        pv.remove_callback(cid)


def find_dconf():
    """Find parameter configuration file for wire-scanners.
    searching the following locations:
    * ~/.phantasy/ws.ini
    * /etc/phantasy/ws.ini
    * package location: apps/wire_scanner/config/ws.ini
    """
    return _find_dconf('wire_scanner', 'ws.ini')


def get_value_with_timestamp(elem, fname):
    """Get field (readback) value with timestamp, value is de-serialized.

    Parameters
    ----------
    elem :
        High-level element object.
    fname : str
        Dynamic field name of element.

    Returns
    -------
    ret : dict
        Value of current readback pv, Keys: 'pv', 'value', 'timestamp'.
    """
    fld = elem.get_field(fname)
    pv_name, pv = fld.readback[0], fld.readback_pv[0]
    val, ts = pv.get(), epoch2human(pv.timestamp)
    if isinstance(val, np.ndarray): val = val.tolist()
    return {'pv': pv_name, 'value': val, 'timestamp': ts}
