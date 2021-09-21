# -*- coding: utf8 -*-

import sys
from phantasy_ui import QApp as QApplication
from phantasy_ui import set_mplstyle

from .app import CorrelationVisualizerWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2018-2019, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "Correlation Visualizer: Generic Parameters Scan and Correlation Analysis"
__version__ = '6.1'


def run(cli=False):
    args = sys.argv
    set_mplstyle(sys.argv)

    if '--machine' in args:
        mach = args[args.index('--machine') + 1]
    else:
        mach = None
    if '--segment' in args:
        segm = args[args.index('--segment') + 1]
    else:
        segm = None

    app = QApplication(sys.argv)
    w = CorrelationVisualizerWindow(version=__version__, machine=mach, segment=segm)
    w.show()
    w.setWindowTitle(__title__)
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
