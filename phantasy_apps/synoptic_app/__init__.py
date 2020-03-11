# -*- coding: utf8 -*-

import sys

from phantasy_ui import QApp as QApplication

from .app import MyAppWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2020, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__version__ = '0.1'


def run(cli=False):
    # synoptic_app [--svgfile --machine --segment]
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

    app = QApplication(sys.argv)
    w = MyAppWindow(__version__, svgfile,
                    machine=machine, segment=segment)
    w.show()
    w.setWindowTitle("Synoptic View & Control: Visualize and Control Accelerator")
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
