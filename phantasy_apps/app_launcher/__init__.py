# -*- coding: utf8 -*-

import argparse
import os
import sys
import getpass
from subprocess import Popen
from phantasy_ui import QApp as QApplication
from PyQt5.QtCore import QSharedMemory

from .app_new import AppLauncherWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2019-2021, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "Global Launcher for FRIB Physics Applications [devel]"
__version__ = '4.3'


def _run_in_dev_mode():
    dev_cmd = '/files/shared/ap/run_apps.sh'
    if os.path.isfile(dev_cmd):
        print("Run App Launcher in development mode: ")
        print("  " + dev_cmd)
        Popen(dev_cmd, shell=True)


def _run_in_ops_mode():
    dev_cmd = '/files/shared/ap/HLA/operation/run_apps.sh'
    if os.path.isfile(dev_cmd):
        print("Run App Launcher in operation mode: ")
        print("  " + dev_cmd)
        Popen(dev_cmd, shell=True)


def run(cli=False):
    parser = argparse.ArgumentParser(
        description="Global launcher for FRIB physics applications.")
    parser.add_argument("--config",
                        dest="config",
                        help="Path of the configuration file")
    parser.add_argument("--log", dest="logfile", help="Path of the log file")
    parser.add_argument("--dev-mode", action="store_true",
            help="Run in development mode, brief for '--mode devel', override --mode")
    parser.add_argument("--mode",
                        dest="mode",
                        help="Working mode, regular(default), devel, ops")

    args = parser.parse_args(sys.argv[1:])

    # share_m = QSharedMemory(getpass.getuser() + __title__)
    # if not share_m.create(1):
    #     raise_app()
    #     return 0

    run_mode = args.mode

    # override run_mode if --dev-mode is set
    if args.dev_mode:
        run_mode = "devel"

    if run_mode == "devel":  # FRIB FTC devel, AP only
        print("run in devel mode")
        _run_in_dev_mode()
    elif run_mode == "ops":  # FRIB FTC operations
        print("run in ops mode")
        _run_in_ops_mode()
    else:  # regular, system-deploy mode
        print("run app launcher")
        app = QApplication(sys.argv)
        w = AppLauncherWindow(version=__version__,
                              logfile=args.logfile,
                              config=args.config)
        w.show()
        w.setWindowTitle(__title__)
        if cli:
            app.exec_()
        else:
            sys.exit(app.exec_())


def raise_app():
    # linux
    Popen("wmctrl -a " + __title__, shell=True)
