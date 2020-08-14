# -*- coding: utf8 -*-

import sys
from phantasy_ui import QApp as QApplication

from .app_new import AppLauncherWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2019, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "Global Launcher for FRIB Physics Apps"
__version__ = '4.0'


def run(cli=False):
    app = QApplication(sys.argv)
    arg = sys.argv
    if '--log' in arg:
        logfile = arg[arg.index('--log') + 1]
    else:
        logfile = None
    if '--config' in arg:
        config_file = arg[arg.index('--config') + 1]
    else:
        config_file = None

## FRIB/AP only
    if '--dev-mode' in arg:
        dev_mode = arg[arg.index('--dev-mode') + 1] == 'true'
    else:
        dev_mode = False

    if dev_mode:
        import os
        from subprocess import Popen
        dev_cmd = '/files/shared/ap/run_apps.sh'
        if os.path.isfile(dev_cmd):
            print("Run App Launcher in development mode: ")
            print("  " + dev_cmd)
            Popen(dev_cmd, shell=True)
            return
##
    w = AppLauncherWindow(version=__version__,
                          logfile=logfile,
                          config=config_file)
    w.show()
    w.setWindowTitle(__title__)
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
