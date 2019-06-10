# -*- coding: utf8 -*-

import sys

from phantasy_ui import QApp as QApplication

from .app import OrbitResponseMatrixWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2018-2019, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "Optics Response Matrix: Steer the Beam Trajectory Like A Master"
__version__ = '3.3'


def run(cli=False):
    app = QApplication(sys.argv)
    w = OrbitResponseMatrixWindow(None, version=__version__)
    w.setWindowTitle(__title__)
    w.show()
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
