# -*- coding: utf-8 -*-

import sys
from phantasy_ui import QApp as QApplication

from .app import MyAppWindow
from .mach_state import fetch as fetch_mach_state


__authors__ = "Tong Zhang"
__copyright__ = "(c) 2021, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "Machine State Data Visualizer"
__version__ = '0.1'


def run(cli=False):
    app = QApplication(sys.argv)
    w = MyAppWindow(version=__version__)
    w.setWindowTitle(__title__)
    w.show()

    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
