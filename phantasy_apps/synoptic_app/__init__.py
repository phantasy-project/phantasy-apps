# -*- coding: utf8 -*-

import sys

from phantasy_ui import QApp as QApplication

from .app import MyAppWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2020, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "Synoptic View & Control: Another novel way to visualize and control the facility"
__version__ = '0.1'


def run(cli=False):
    # synoptic_app [--svgfile --machine --segment --debug]
    args = sys.argv
    if '--machine' in args:
        machine = args[args.index('--machine') + 1]
    else:
        machine = None

    if '--segment' in args:
        segment = args[args.index('--segment') + 1]
    else:
        segment = None

    if '--svgfile' in args:
        svgfile = args[args.index('--svgfile') + 1]
    else:
        svgfile = None

    if '--debug' in args:
        debug = bool(args[args.index('--debug') + 1])
    else:
        debug = False

    app = QApplication(sys.argv)
    w = MyAppWindow(__version__, svgfile, debug,
                    machine=machine, segment=segment)
    w.show()
    w.setWindowTitle(__title__)
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
