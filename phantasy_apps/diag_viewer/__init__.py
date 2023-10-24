# -*- coding: utf8 -*-

"""2020-10-09 v3.0

- Add support to build devices with arbitrary PV strings.
"""

import sys

from phantasy_ui import QApp as QApplication
from phantasy_ui import set_mplstyle

from .app import DeviceViewerWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2019-2023, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "Device Viewer: Visualize Device Readings and Settings"
__version__ = '3.2'


def run(cli=False):
    set_mplstyle(sys.argv)
    app = QApplication(sys.argv)
    w = DeviceViewerWindow(version=__version__)
    w.setWindowTitle(__title__)
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
