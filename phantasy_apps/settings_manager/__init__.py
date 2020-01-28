# -*- coding: utf8 -*-

import os
import sys

from phantasy_ui import QApp as QApplication

from .app import SettingsManagerWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2019, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__version__ = '1.0'

CONFIG_PATH = "~/.phantasy-apps/settings-manager"


def init_config_dir():
    # initialize configuration directory
    confdir = os.path.expanduser(CONFIG_PATH)
    if not os.path.exists(confdir):
        os.makedirs(confdir)
    return confdir


def run(cli=False):
    confdir = init_config_dir()

    app = QApplication(sys.argv)
    w = SettingsManagerWindow(version=__version__, config_dir=confdir)
    w.show()
    w.setWindowTitle("Settings Manager: Manage Physics Configurations of Accelerator System")
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
