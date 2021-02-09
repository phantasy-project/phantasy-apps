# -*- coding: utf8 -*-

import sys
from phantasy_ui import QApp as QApplication
from .app import SettingsManagerWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2019-2020, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "Settings Manager: Manage Physics Configurations of Accelerator System"
__version__ = '6.0'

# ENV: LIVE_MODE, e.g.: LIVE_MODE=False settings_manager

def run(cli=False):
    args = sys.argv
    if '--config' in args:
        confdir = args[args.index('--config') + 1]
    else:
        confdir = None

    app = QApplication(sys.argv)

    #
    w = SettingsManagerWindow(version=__version__, config_dir=confdir)
    w.setWindowTitle(__title__)

    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
