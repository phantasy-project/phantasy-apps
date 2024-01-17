# -*- coding: utf8 -*-

import sys

from phantasy_ui import QApp as QApplication
from phantasy_ui import set_mplstyle

from .app import AllisonScannerWindow
from .data import Data
from .data import draw_beam_ellipse_with_params
from .device import Device
from .model import Model
from .utils import point_in_ellipse

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2019-2024, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "Allison Scanner: Measure Transverse Emittance and Twiss Parameters"
__version__ = '4.3'
__last_updated__ = "2024-01-17"


def run(cli=False):
    args = sys.argv
    set_mplstyle(args)
    app = QApplication(args)
    w = AllisonScannerWindow(version=__version__, last_updated=__last_updated__)
    w.show()
    w.setWindowTitle(__title__)
    w.resize(1920, 1440)
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
