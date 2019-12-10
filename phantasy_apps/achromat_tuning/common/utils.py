#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module is dedicated for utility functions.
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division

from __future__ import print_function
import logging
import numpy as np

__authors__ = "Kei Fukushima"
__copyright__ = "(c) 2017, Facility for Rare Isotope beams," \
                "Michigan State University"
__contact__ = "Kei Fukushima <fukushim@frib.msu.edu>"

_LOGGER = logging.getLogger(__name__)

def isuniquelist(inp, type1, type2):
    """Return whether an input is an unique type list."""
    type1 = type1 if isinstance(type1, (list, tuple)) else [type1]
    type2 = type2 if isinstance(type2, (list, tuple)) else [type2]

    bool1 = isinstance(inp, type1)
    if bool1:
        inp2 = np.unique(map(type, inp))
        bool2 = len(inp2) == 1 and inp2[0] in type2
    else:
        bool2 = False
    return bool1 and bool2