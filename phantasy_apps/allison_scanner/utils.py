#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from collections import OrderedDict

import numpy as np
from numpy.testing import assert_almost_equal

from phantasy import MachinePortal
from phantasy_apps.utils import find_dconf as _find_dconf


def find_dconf():
    """Find parameter configuration file for wire-scanners.
    searching the following locations:
    * ~/.phantasy/ems.ini
    * /etc/phantasy/ems.ini
    * package location: apps/allison_scanner/config/ems.ini
    """
    return _find_dconf('allison_scanner', 'ems.ini')


def get_all_devices(machine="FRIB", segment="LEBT", type="EMS"):
    """Return dict of `(name, elem)`.
    """
    mp = MachinePortal(machine, segment)
    elems = mp.get_elements(type=type)
    r = [(i.name, i) for i in sorted(elems, key=lambda x:x.name[-4:])]
    return OrderedDict(r)


def point_in_ellipse(x, y, ellipse, factor=1.0):
    """Test if point `(x, y)` in *ellipse* or not.

    Parameters
    ----------
    x : float
        Point x coord.
    y : float
        Point y coord.
    ellipse :
        Ellipse patch.
    factor : float
        Increase/shrink the ellipse by applying coef onto both width and
        eight, default is 1.0.
    """
    x0, y0 = ellipse.center
    w, h = ellipse.width, ellipse.height
    theta = np.deg2rad(ellipse.angle)
    x -= x0
    y -= y0
    x1 = np.cos(theta) * x + np.sin(theta) * y
    y1 = -np.sin(theta) * x + np.cos(theta) * y
    return (x1 * x1 / w / w + y1 * y1 / h / h) <= 0.25 * factor * factor


def is_integer(a):
    """Test if float(a) == int(a).
    e.g. is_integer(4.0) returns True, while is_integer(4.01) returns False.
    """
    try:
        assert_almost_equal(a, int(a))
    except AssertionError:
        return False
    else:
        return True
