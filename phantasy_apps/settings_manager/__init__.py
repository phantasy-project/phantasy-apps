# -*- coding: utf8 -*-

import os
import sys
import argparse
from phantasy_ui import QApp as QApplication
from .app import SettingsManagerWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2019-2022, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "Settings Manager: Manage Physics Configurations of Accelerator System"
__version__ = '10.4'


def run(cli=False):
    parser = argparse.ArgumentParser(
            description="Manage the physics settings of an accelerator")
    parser.add_argument("--config", dest="config",
            help="Path of the configuration file")
    parser.add_argument("--snapshot", dest="snapshot",
            help="The name of a snapshot to load, if valid one is defined")
    parser.add_argument("--snapshot-window-off", action='store_true',
            help="Turn off the snapshot window")

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
    if args.snapshot_window_off:
        w.snp_dock.close()

    if args.snapshot is not None:
        w.snp_dock.close()
        w.load_snapshot(args.snapshot)

    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
