# -*- coding: utf8 -*-

import os
import sys
import argparse
from phantasy_ui import QApp as QApplication
from .app import SettingsManagerWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2019-2021, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "Settings Manager: Manage Physics Configurations of Accelerator System"
__version__ = '9.7'


def run(cli=False):
    parser = argparse.ArgumentParser(
            description="Manage the physics settings of an accelerator")
    parser.add_argument("--config", dest="config",
            help="Path of the configuration file")

    args = parser.parse_args(sys.argv[1:])

    if args.config is not None:
        config_file = os.path.abspath(os.path.expanduser(args.config))
        if not os.path.isfile(config_file):
            print("Invalid configuration file passed.")
            parser.print_help()
            sys.exit(1)

    app = QApplication(sys.argv)
    #
    w = SettingsManagerWindow(version=__version__, config_dir=args.config)
    w.setWindowTitle(__title__)

    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
