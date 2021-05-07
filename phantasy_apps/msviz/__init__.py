# -*- coding: utf-8 -*-

try:
    from IPython import get_ipython
    if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
        NB_SHELL = True
    else:
        NB_SHELL = False
except ImportError:
    NB_SHELL = False
finally:
    import pkg_resources
    try:
        pkg_resources.get_distribution('tqdm')
    except pkg_resources.DistributionNotFound:
        TQDM_INSTALLED = False
    else:
        TQDM_INSTALLED = True
        if NB_SHELL:
            from tqdm.notebook import tqdm
        else:
            from tqdm import tqdm

import sys
from phantasy_ui import QApp as QApplication

from .app import MyAppWindow
from .mach_state import fetch as fetch_mach_state


__authors__ = "Tong Zhang"
__copyright__ = "(c) 2021, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "Machine State Data Visualizer"
__version__ = '0.1'


def run(cli=False):
    app = QApplication(sys.argv)
    w = MyAppWindow(version=__version__)
    w.setWindowTitle(__title__)
    w.show()

    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
