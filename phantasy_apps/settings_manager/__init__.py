# -*- coding: utf8 -*-

import sys
from phantasy_ui import QApp as QApplication
from .app import SettingsManagerWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2019-2020, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "Settings Manager: Manage Physics Configurations of Accelerator System"
__version__ = '9.0'

# ENV: LIVE_MODE ([True], False), e.g.: LIVE_MODE=False settings_manager
# ENV: DSRC_MODE ([DB], FILE): data source mode
# ENV: DATABASE ([sm.db],): database name, path is wdir --> to be changed with fullpath
# ENV: ENABLE_MS ([True], False): enable machine state capture or not

def run(cli=False):
    args = sys.argv
    if '--config' in args:
        confdir = args[args.index('--config') + 1]
    else:
        confdir = None
    if '--machine' in args:
        mach = args[args.index('--machine') + 1]
    else:
        mach = None
    if '--segment' in args:
        segm = args[args.index('--segment') + 1]
    else:
        segm = None

    app = QApplication(sys.argv)

    #
    w = SettingsManagerWindow(version=__version__, config_dir=confdir, machine=mach, segment=segm)
    w.setWindowTitle(__title__)

    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
