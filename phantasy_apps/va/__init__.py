# -*- coding: utf8 -*-

import sys

from phantasy_ui import QApp as QApplication

from .app import VALauncherWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2018-2020, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__version__ = '2.2'


def run(cli=False):
    app = QApplication(sys.argv)
    w = VALauncherWindow(version=__version__)
    w.adjustSize()
    w.show()
    w.setWindowTitle("Virtual Accelerator Launcher")
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
