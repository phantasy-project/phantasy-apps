# -*- coding: utf-8 -*-

import sys
from phantasy_ui import QApp as QApplication
from phantasy_ui import set_mplstyle

from .bendtune import BendTune
from .quadachromat import QuadAchromat
from .app import MyAppWindow

__all__ = ['BendTune', 'QuadAchromat']
__authors__ = ("Kei Fukushima", "Tong Zhang")
__copyright__ = "(c) 2019-2020, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = ("Kei Fukushima <fukushim@frib.msu.edu>",
               "Tong Zhang <zhangt@frib.msu.edu>")
__title__ = "Achromat Tuning for FRIB Folding Segments"
__version__ = '0.1'


def run(cli=False):
    set_mplstyle(sys.argv)
    app = QApplication(sys.argv)
    w = MyAppWindow(version=__version__)
    w.show()
    w.setWindowTitle(__title__)
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
