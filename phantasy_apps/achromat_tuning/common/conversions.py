#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module is dedicated for VA unit and field conversion to flame.
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

def cnv_field(elem_type, field, cor):
    """Convert EPICS field name to flame lattice parameter."""

    if elem_type == 'quadrupole' and field == 'GRAD':
        return 'B2'
    elif elem_type == 'sbend' and field == 'B':
        return 'bg'
    elif elem_type == 'rfcavity' and field == 'PHA':
        return 'phi'
    elif elem_type == 'orbtrim' and field == 'ANG':
        if cor == 'X':
            return 'theta_x'
        elif cor == 'Y':
            return 'theta_y'
        else :
            raise Exception('cor= "X" or "Y" information is required to get parameter from correctors.')
    else:
        return field
        

def cnv_unit(state, field):
    """Convert EPICS field name to flame beam state."""
    if field == 'X':
        return state.moment0_env[0]*1e-3
        # convert mm to m
    elif field == 'Y':
        return state.moment0_env[2]*1e-3
        # convert mm to m
    elif field == 'ENG':
        return state.ref_IonEk*1e-6
        # convert eV to MeV
    elif field == 'PHA':
        return np.mod(2.0*state.ref_phis*(180e0/np.pi),360e0)
        # convert rad to deg and adjust for 161MHz sampling frequency
    elif field == 'XRMS':
        return state.moment0_rms[0]*1e-3
        # convert mm to m
    elif field == 'YRMS':
        return state.moment0_rms[2]*1e-3
        # convert mm to m
    elif hasattr(state,field):
        return state.field
    else:
        return state