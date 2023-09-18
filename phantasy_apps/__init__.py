# -*- coding: utf-8 -*-
import logging
import os
from .msviz import fetch_mach_state

logging.getLogger(__name__).setLevel(logging.INFO)
logging.basicConfig(
        format="%(levelname)s: %(asctime)s: %(name)s: %(message)s"
)

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2019-2023, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__version__ = "5.7.0"

__doc__ = \
"""High-level physics controls applications built upon `PHANTASY`.

:version: %s
:authors: %s
""" % (__version__, __authors__)


k = "PHANTASY_CONFIG_DIR"
os.environ.setdefault(k, "/usr/lib/phantasy-machines")

from .threshold_manager import mps_take_snapshot
