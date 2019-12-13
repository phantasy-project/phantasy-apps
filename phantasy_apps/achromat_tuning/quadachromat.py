#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module is dedicated for linear achromatic tuning application.
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import logging


__authors__ = "Kei Fukushima"
__copyright__ = "(c) 2017, Facility for Rare Isotope beams, Michigan State University"
__contact__ = "Kei Fukushima <fukushim@frib.msu.edu>"

_LOGGER = logging.getLogger(__name__)

import time
import numpy as np

from scipy.optimize import minimize
from scipy.optimize import leastsq
from scipy.interpolate import interp1d

from phantasy_apps.achromat_tuning import common

class QuadAchromat(object):
    """Python class for quadrupole tuning for linear achromat.

    Parameters
    ----------
    m : callable
        MachinePortal object in phantasy or Machine object in FLAME.
    knob : list
        List of tuning knobs.
    sym : list of int
        Symmetic condition of the tuning knobs. e.g. ::\n
            sym = [0,1,1,0] means reflectionally symmetry.
            sym = [0,1,2,3] means no symmetricity.
    scan : ndarray (linspace(-0.1,0.1,5))
        Scan range of the tuning knobs.
    monitor : list
        List of monitors.
    cavity : list
        List of the cavity which used for the achromat tuning.
    cav_shift : float
        Value ofthe synchronous phase shift for the cavity.
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
    cav_ini : ndarray
        Initial settings of the cavity.
    dim : int
        Dimension of the scan process which based on the number of knobs and the symmetric condition.

    """

    def __init__(self, m, knob=None, sym=None, scan=np.linspace(-0.1,0.1,5),
                 monitor=None, cavity=None, cav_shift=60.0, cor='X', wait=2,
                 cnv_unit=common.cnv_unit, cnv_field=common.cnv_field):
        self.m = m

        try:
            self.io = self.m.work_lattice_conf
        except:
            self.io = common.ModelControl(machine=self.m, cnv_unit=cnv_unit, cnv_field=cnv_field)

        self.knob = knob
        self.sym = sym
        self.monitor = monitor
        self.cavity = cavity
        self.cor = cor
        self.wait = wait
        self.knob_scan = scan
        self.cav_shift = cav_shift

        self.renew()

    def renew(self):
        """Renew initial parametes.

        Note
        ----
        Update `knob_ini`, `cav_ini`, and `dim` by the current settings.

        """
        self.knob_ini = np.asarray([self.io.get(k,'GRAD')['GRAD'] for k in self.knob])
        self.cavity = self.cavity if isinstance(self.cavity,(list,tuple)) else [self.cavity]
        self.cav_ini = np.asarray([self.io.get(k,'PHASE')['PHASE'] for k in self.cavity])
        self._cav_shifted = self.cav_ini + self.cav_shift

        self.dim = len(np.unique(self.sym))

    def show(self):
        """Print the tuning parameters."""
        print('--- Main parameters ---')
        print('Tuning knob          : '+str(self.knob))
        print('Symmetricity         : '+str(self.sym))
        print('Scan point [ratio]   : '+str(self.knob_scan))
        print('Monitor              : '+str(self.monitor))
        print('Cavity for use       : '+str(self.cavity))
        print('Cavity phase shift [deg.] : '+str(self.cav_shift))
        print()
        print('--- Initial parameters ---')
        print('Knob setting [GRAD]   : '+str(self.knob_ini))
        print('Cavity setting [deg.] : '+str(self.cav_ini))
        print()
        print('--- Other parameters ---')
        print('Tuning coordinate     : '+str(self.cor))
        print('Monitor evaluation wait time [sec] : '+str(self.wait))

    def dispersion(self):
        """Evaluate dispersion function.

        Return
        ------
        ndarray
            List of the dispersion functions at the monitors

        """
        self._cav_set(self.cavity, self._cav_shifted)
        time.sleep(self.wait)

        eng = np.asarray([self.io.get(m,'ENG')['ENG'] for m in self.monitor])
        cen = np.asarray([self.io.get(m,self.cor)[self.cor] for m in self.monitor])

        self._cav_set(self.cavity, self.cav_ini)
        time.sleep(self.wait)
        eng /= np.asarray([self.io.get(m,'ENG')['ENG'] for m in self.monitor])
        cen -= np.asarray([self.io.get(m,self.cor)[self.cor] for m in self.monitor])

        return cen/(1e0 - np.sqrt(1e0/eng))


    def run(self, method='TNC', auto_app=True):
        """Run linar achromat tuning for the quadrupoles.

        Parameters
        ----------
        method : str
            Optimize method for `scipy.optimize.minimize()`.
        auto_app : bool
            Apply the optimized parameter to `m` automatically.

        Return
        ------
        ndarray
            Optimized parameter ratio. it can be applied by usign apply().

        """
        bpm0, grid = self._ndscan()

        self._cav_set(self.cavity, self._cav_shifted)

        bpm1 = bpm0-self._ndscan()[0]

        self._cav_set(self.cavity, self.cav_ini)

        fit_ini = np.zeros(pow(2,self.dim))
        fit_para = [None]*len(bpm1)
        for i in range(len(bpm1)):
            fit_para[i] = leastsq(self._lfnc,fit_ini,args=(grid,bpm1[i]))[0]

        opt_ini = np.zeros(self.dim)
        ans = minimize(self._cost_fnc,opt_ini,args=(fit_para,),method=method).x
        inp = self._symmetrize(ans)

        if auto_app == True:
            rbpm = self._bpm_ev(inp)

        self.c_grid = grid
        self.c_bpm0 = bpm0
        self.c_bpm = bpm1
        self.c_fit = fit_para
        self.c_ans = ans

        return inp

    def apply(self,inp):
        rbpm = self._bpm_ev(inp)

    def _cav_set(self, cav_name, cav_pha):
        for i,j in zip(cav_name, cav_pha):
            self.io.set(i,j,'PHASE')

    def _ndscan(self):
        """n-dimensional scan"""
        grid = np.meshgrid(*[[self.knob_scan]]*self.dim)
        fgrid = np.asarray([grid[i].flatten() for i in range(len(grid))])

        map_len = len(self.knob_scan)**self.dim
        bpms_map = np.zeros([len(self.monitor),map_len])

        for i in range(map_len):
            inp = self._symmetrize(fgrid[:,i])
            bpms_map[:,i] = self._bpm_ev(inp)
        self._resetknob()
        return bpms_map, fgrid

    def _symmetrize(self, data):
        """Symmetrize input setting"""
        inp = np.zeros(len(self.knob))
        for j,sym_flag in enumerate(np.unique(self.sym)):
            inp[sym_flag==self.sym] = data[j]
        return inp


    def _bpm_ev(self, inp):
        """Get bpm readings with inputted setting"""
        for i,j,k in zip(self.knob,self.knob_ini,inp):
            self.io.set(i,float(j*(1.0+k)),'GRAD')
        time.sleep(self.wait)
        bpms = np.asarray([self.io.get(m,self.cor)[self.cor] for m in self.monitor])
        return bpms

    def _resetknob(self):
        """Reset tuning knobs"""
        for i,j in zip(self.knob,self.knob_ini):
            self.io.set(i,float(j),'GRAD')

    def _lfnc(self, p, x, y):
        """Linear function for fitting"""
        res = -y
        for i,nn in enumerate(zip(*[c.flatten() for c in np.meshgrid(*[[0,1]]*self.dim)])):
            tmp = p[i]
            for j,m in enumerate(nn):
                tmp *= pow(x[j],m)
            res += tmp
        return res

    def _cost_fnc(self, inp, para):
        """Cost function for minimizing"""
        diff = np.asarray([np.abs(self._lfnc(para[i],inp,0)) for i in range(len(para))])
        return np.average(diff)
