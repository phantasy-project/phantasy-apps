# -*- coding: utf8 -*-

import os
import sys
import argparse
from phantasy_ui import QApp as QApplication
from .app import MPSThresholdManagerWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2023, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "Threshold Manager: Manage the diagnostics threshold data for MPS configurations"
__version__ = '0.1'


def run(cli=False):
    app = QApplication(sys.argv)
    #
    w = MPSThresholdManagerWindow(version=__version__)
    w.setWindowTitle(__title__)
    w.show()

    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
