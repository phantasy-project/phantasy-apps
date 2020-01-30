#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module is dedicated for bending strenth tuning application.
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import logging


__authors__ = "Kei Fukushima"
__copyright__ = "(c) 2017, Facility for Rare Isotope beams," \
                "Michigan State University"
__contact__ = "Kei Fukushima <fukushim@frib.msu.edu>"

_LOGGER = logging.getLogger(__name__)

import time
import numpy as np

from phantasy_apps.achromat_tuning import common

class BendTune(object):
    """Python class for bending strength tuning by using BPMs.

    Parameters
    ----------
    m : callable
        MachinePortal object in phantasy or Machine object in FLAME.
    knob : list
        List of tuning knobs.
    scan : ndarray
        Scan range of the tuning knobs.
    target : float
        Target value for the cost function.
    monitor : list of str
        List of monitors.
    cor : 'X' or 'Y'
        Target coodinate for tuning the dispersion.
    wait : float
        Wait time for evaluating monitors.
    cnv_unit : callable
        Unit conversion function from FLAME to device.
    cnv_field : callable
        Field name conversion function from device to FLAME.

    Attributes
    ----------
    knob_ini : ndarray
        Initial settings of the tuning knobs.

    """

    def __init__(self, m, knob=None, scan=np.linspace(-0.1,0.1,5), target=0.0,
                 monitor=None, cor='X', wait=2, cnv_unit=common.cnv_unit, cnv_field=common.cnv_field):
        self.m = m
        try:
            self.io = self.m.work_lattice_conf
        except:
            self.io = common.ModelControl(machine=self.m, cnv_unit=cnv_unit, cnv_field=cnv_field)

        self.knob = knob
        self.monitor = monitor
        self.cor = cor
        self.wait = wait
        self.scan = scan
        self.target = target

        self.renew()

    def renew(self):
        """Renew initial parameters.

        Note
        ----
        Update `knob_ini` by the current settings.

        """
        self.knob_ini = np.asarray([self.io.get(k,'B')['B'] for k in self.knob])

    def show(self):
        """Print the tuning parameters."""
        print('--- Main parameters ---')
        print('Tuning knob          : '+str(self.knob))
        print('Scan point [ratio]   : '+str(self.scan))
        print('Monitor              : '+str(self.monitor))
        print()
        print('--- Initial parameters ---')
        print('Knob setting [1]   : '+str(self.knob_ini))
        print()
        print('--- Other parameters ---')
        print('Tuning coordinate     : '+str(self.cor))
        print('Monitor evaluation wait time [sec] : '+str(self.wait))


    def run(self):
        """Run bending strength tuning.

        Note
        ----
        If there is a crossing point to the `target` value, input the optimized value to `m` .
        Otherwise, input the initial value and raise `ValueError`.

        Raises
        ------
        ValueError
            There is no crossing point in the scan range.

        """
        self.yls = np.asarray([self._bpm_ev(inp) for inp in self.scan])
        coef = np.polyfit(self.yls, self.scan, 2)
        self.fnc = lambda x : coef[0]*x*x + coef[1]*x + coef[2]
        try:
            self._bpm_ev(self.fnc(self.target))
        except ValueError:
            self._bpm_ev(0.0)
            print('ValueError: There is no crossing point in the scan range. '\
                  'Pleas try wider scan range.')

    def _bpm_ev(self, inp):
        """Get the cost function with inputted setting"""
        for i,j in zip(self.knob,self.knob_ini):
            self.io.set(i,float(j*(1.0+inp)),'B')
        time.sleep(self.wait)
        bpms = np.asarray([self.io.get(m,self.cor)[self.cor] for m in self.monitor])
        return np.average(bpms)
