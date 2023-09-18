# -*- coding: utf8 -*-

import os
import sys
import argparse
from phantasy_ui import QApp as QApplication
from .app import MPSThresholdManagerWindow
from .data import read_config
from .tools import take_snapshot
from .db.utils import ensure_connect_db

__authors__ = "Tong Zhang"
__copyright__ = "(c) 2023, Facility for Rare Isotope beams," \
                " Michigan State University"
__contact__ = "Tong Zhang <zhangt@frib.msu.edu>"
__title__ = "MPS Data Manager: Manage the diagnostics threshold data for MPS configurations"
__version__ = '1.3'


def run(cli=False):
    parser = argparse.ArgumentParser(
        description=
        "Manage the threshold data for diagnostics MPS configurations.")
    parser.add_argument("--config",
                        dest="config",
                        help="Path of the configuration file")
    args = parser.parse_args(sys.argv[1:])

    if args.config is None:
        configpath = os.path.join(os.path.dirname(__file__),
                                  "config/sample.toml")
    else:
        configpath = args.config

    app = QApplication(sys.argv)
    #
    w = MPSThresholdManagerWindow(version=__version__, configpath=configpath)
    w.setWindowTitle(__title__)
    w.show()

    if cli:
        app.exec_()
    else:
        sys.exit(app.exec_())

def take_snapshot_tool():
    parser = argparse.ArgumentParser(
                description="Capture the diagnostics threshold data for MPS configurations.")
    parser.add_argument("--config", dest="config", help="Path of the configuration file.")
    parser.add_argument("--dtype", action="append", dest="dtype_list",
                        help="Device type of MPS threshold data to capture, "
                             "'ND', 'IC' or 'HMR' is supported, "
                             "pass one type at one time with --dtype.")
    parser.add_argument("--tag", action="append", dest="tag_list",
                        help="Tag string to label the snapshot, "
                             "pass one tag with --tag at one time.")
    parser.add_argument("--note", dest="note", default="", help="Additional notes for the snapshot.")

    args = parser.parse_args(sys.argv[1:])
    if args.dtype_list is None:
        args.dtype_list = ['ND', 'IC', 'HMR']

    dtype_list = []
    for i in args.dtype_list:
        if i.upper() not in ('ND', 'IC', 'HMR'):
            print(f"'{i}' is an invalid device type, pass 'ND', 'IC' or 'HMR'")
            continue
        dtype_list.append(i.upper())

    if args.tag_list is None:
        args.tag_list = []
    tag_list = sorted(set(i.upper() for i in args.tag_list + dtype_list))

    if args.config is None:
        configpath = os.path.join(os.path.dirname(__file__),
                                  "config/sample.toml")
    else:
        configpath = args.config

    conf = read_config(configpath)
    conn = ensure_connect_db(conf['db_uri'])
    take_snapshot(dtype_list, note=args.note, tags=tag_list, conn=conn)
    conn.close()


def mps_take_snapshot(dtypes: list, note: str, tags: list):
    """ Take a snapshot for the diagnotic threshold data for MPS configurations, and
    save to the database.

    Use the GUI app "MPS Data Manager" to view the data.

    Parameters
    ----------
    dtypes : list
        A list of device types, a device type could be `ND`, `IC` or `HMR`.
    note : str
        A string of note.
    tags : list
        A list of strings as tags, besides the auto-tagged with 'ND', 'IC' or 'HMR'.

    Examples
    --------
    >>> from phantasy_apps import mps_take_snapshot
    >>> take_snapshot(["ND"], "Capture MPS ND data", ["ND"])
    """
    configpath = os.path.join(os.path.dirname(__file__), "config/sample.toml")
    conf = read_config(configpath)
    conn = ensure_connect_db(conf['db_uri'])
    tag_list = sorted(set(i.upper() for i in tags + dtypes))
    take_snapshot(dtypes, note=note, tags=tag_list, conn=conn)
    conn.close()



