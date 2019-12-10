#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module is dedicated for control flame by using EPICS field name.
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

from phantasy import ModelFlame

class ModelControl(ModelFlame):
    def __init__(self, lat_file=None, machine=None, cnv_unit=None, cnv_field=None):
        ModelFlame.__init__(self, lat_file=lat_file)
        self._mach_states = machine.allocState({})
        self._mach_ins = machine

        if cnv_unit is None:
            self._cnv_unit = lambda x,field: getattr(x, field) if hasattr(x, field) else x
        else:
            self._cnv_unit = cnv_unit

        if cnv_unit is None:
            self._cnv_field = lambda field, *args, **kws: field
        else:
            self._cnv_field = cnv_field

    @property
    def cnv_unit(self):
        """Unit conversion function from device to FLAME lattice element"""
        return self._cnv_unit

    @cnv_unit.setter
    def cnv_unit(self, cnv_func):
        if callable(cnv_func): self._cnv_unit = cnv_func

    @property
    def cnv_field(self):
        """Field conversion function from device to FLAME lattice element"""
        return self._cnv_field

    @cnv_field.setter
    def cnv_field(self, cnv_func):
        if callable(cnv_func): self._cnv_field = cnv_func

    def get(self, elem, field, cor=None, data=None, **kws):
        """Get beam or lattice element infromation by using EPICS field name.
        (Compatible function with MachinePortal lattice.get function)

        Parameters
        ----------
        elem : str or int
            Name or index of the lattice element.
        value : float
            New value for the parameter.
        field : str
            EPICS field name to input.
        cor : 'X', 'Y' or None
            Optional parameter for correctors\n
            field = 'ANG' and cor = 'X' :
                Input horizontal kick angle to the corrector.
            field = 'ANG' and cor = 'Y' :
                Input vertical kick angle to the corrector.
        """
        m = self._mach_ins
        elem = elem.name if hasattr(elem,'name') else elem

        if isinstance(elem,(str,unicode)):
            fres = m.find(name=elem)
            id = fres[0] if (len(fres) != 0) else -1
        else:
            id = elem

        if id >= 0 :
            mconf = m.conf(id)
            if data == 'lattice' or not mconf['type'] in ['bpm','marker']:
                f = self._cnv_field(mconf['type'],field,cor)
                retval = mconf[f]

            else:
                self._cache = self._cache if hasattr(self,'_cache') else False
                if not self._cache:
                    self._cache_res = self.run(monitor=range(len(self._mach_ins)))[0]
                self._cache = True
                retval = self._cnv_unit(self._cache_res[id][1],field)
        else :
            retval = None

        return {field:retval}

    def set(self, elem, value, field, cor=None, **kws):
        """Input lattice element parameter by using EPICS field.
        (Compatible function with MachinePortal lattice.set function)

        Parameters
        ----------
        elem : str or int
            Name or index of the lattice element.
        value : float
            New value for the parameter.
        field : str
            EPICS field name to input.
        cor : 'X', 'Y' or None
            Optional parameter for correctors\n
            field = 'ANG' and cor = 'X' :
                Input horizontal kick angle to the corrector.
            field = 'ANG' and cor = 'Y' :
                Input vertical kick angle to the corrector.
        """
        m = self._mach_ins
        elem = elem.name if hasattr(elem,'name') else elem
        id = m.find(name=elem)[0] if isinstance(elem,(str,unicode)) else elem
        f = self._cnv_field(m.conf(id)['type'],field,cor)
        m.reconfigure(id,{f:value})
        self._cache = False
