# -*- coding: utf-8 -*-
import logging
import os

logging.getLogger(__name__).setLevel(logging.INFO)
logging.basicConfig(
        format="%(levelname)s: %(asctime)s: %(name)s: %(message)s"
)

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2019, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__version__ = "2.1.0"

__doc__ = \
"""High-level physics controls applications built upon `PHANTASY`.

:version: %s
:authors: %s
""" % (__version__, __authors__)


k = "PHANTASY_CONFIG_DIR"
os.environ.setdefault(k, "/usr/lib/phantasy-machines")
