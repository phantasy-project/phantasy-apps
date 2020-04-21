# -*- coding: utf-8 -*-

import sys
from phantasy_ui import QApp as QApplication
from phantasy_ui import set_mplstyle

from .app import PMViewerWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2019, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "Profile Monitors Viewer: Inspect and Operate PM devices"
__version__ = '0.2'


def run(cli=False):
    set_mplstyle(sys.argv)
    app = QApplication(sys.argv)
    w = PMViewerWindow(version=__version__)
    w.show()
    w.setWindowTitle(__title__)
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
