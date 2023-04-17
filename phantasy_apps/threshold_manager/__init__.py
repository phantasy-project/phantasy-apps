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
    parser = argparse.ArgumentParser(
        description=
        "Manage the threshold data for diagnostics MPS configurations.")
    parser.add_argument("--config",
                        dest="config",
                        help="Path of the configuration file")
    args = parser.parse_args(sys.argv[1:])

    if args.config is None:
        configpath = os.path.join(os.path.dirname(__file__),
                                  "config/sample.toml")
    else:
        configpath = args.config

    app = QApplication(sys.argv)
    #
    w = MPSThresholdManagerWindow(version=__version__, configpath=configpath)
    w.setWindowTitle(__title__)
    w.show()

    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
