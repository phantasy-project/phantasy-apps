# -*- coding: utf-8 -*-

import argparse
import os
import sys
from phantasy_ui import QApp as QApplication

from .app import PermissionManagerWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2023, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "Permission Manager: Manage the folder permission"
__version__ = '0.2'


def run(cli=False):
    parser = argparse.ArgumentParser(
            description="Manage the folder permissions.")
    parser.add_argument("--config", dest="config",
            help="Path of the configuration file")
    args = parser.parse_args(sys.argv[1:])

    if args.config is None:
        configpath = os.path.join(os.path.dirname(__file__), "config/sample.toml")
    else:
        configpath = args.config

    print(f"Permission Manager: using config from {configpath}")
    app = QApplication(sys.argv)
    w = PermissionManagerWindow(version=__version__, configpath=configpath)
    w.show()
    w.setWindowTitle(__title__)
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
