# -*- coding: utf8 -*-

import argparse
import sys
from phantasy_ui import QApp as QApplication
from phantasy_ui import set_mplstyle

from .app import CorrelationVisualizerWindow

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2018-2019, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "Correlation Visualizer: Generic Parameters Scan and Correlation Analysis"
__version__ = '6.1'


def run(cli=False):
    parser = argparse.ArgumentParser(
        description=
        "General parameters scan, correlation anlysis and visualization.")
    parser.add_argument("--machine",
                        dest="machine",
                        help="The name of the machine.")
    parser.add_argument("--segment",
                        dest="segment",
                        help="The name of the segment.")
    parser.add_argument("--config",
                        dest="config",
                        help="The path for the configuration file.")

    args = parser.parse_args(sys.argv[1:])

    if args.config is not None:
        config_file = os.path.abspath(os.path.expanduser(args.config))
        if not os.path.isfile(config_file):
            print("Invalid configuration file passed.")
            parser.print_help()
            sys.exit(1)
        else:
            config_file = config_file
    else:
        config_file = None

    set_mplstyle(sys.argv)
    app = QApplication(sys.argv)
    w = CorrelationVisualizerWindow(version=__version__,
                                    machine=args.machine,
                                    segment=args.segment,
                                    config=config_file)
    w.show()
    w.setWindowTitle(__title__)
    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())
