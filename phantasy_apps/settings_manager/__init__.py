# -*- coding: utf8 -*-

import os
import sys
import argparse
from phantasy_ui import QApp as QApplication
from phantasy_ui.widgets import SplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from .app import SettingsManagerWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2019-2023, Facility for Rare Isotope Beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "Settings Manager: Manage Physics Configurations of Accelerator System"
__version__ = '12.1'


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
    else:
        config_file = None # search per app's rules.

    app = QApplication(sys.argv)
    #
    splash_w = SplashScreen(QPixmap(":/sm-icons/sm-splash.png"))
    splash_w.show()
    splash_w.showMessage("Starting up Settings Manager...", Qt.AlignBottom | Qt.AlignHCenter)

    w = SettingsManagerWindow(version=__version__, config_file=config_file,
                              title=__title__, splash=splash_w)
    w.show()
    splash_w.finish(w)
    if args.snapshot_window_off:
        w.snp_dock.close()

    if args.snapshot is not None:
        w.snp_dock.close()
        w.load_snapshot(args.snapshot)

    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
