# -*- coding: utf-8 -*-

import sys

from phantasy_ui import QApp as QApplication

from .app import UnicornApp

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2018, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "Unicorn App: Manage Device Scaling Laws of Physics and Engineering Units"
__version__ = '1.4'


def run(cli=False):
    app = QApplication(sys.argv)
    w = UnicornApp(version=__version__)
    w.show()
    w.setWindowTitle(__title__)
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
