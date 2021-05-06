#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""CLI tools for machine state data fetching.
"""

import argparse
import json
import os
import sys

from phantasy_apps.msviz.mach_state import DEFAULT_META_CONF_PATH
from phantasy_apps.msviz.mach_state import fetch_data
from phantasy_apps.msviz.mach_state import get_meta_conf_dict
from phantasy_apps.msviz.mach_state import merge_mach_conf

VER = 1.0


class Formatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass

parser = argparse.ArgumentParser(
        description="Retrieve machine state by fetching data from EPICS controls network.",
        formatter_class=Formatter)
parser.add_argument('--config', dest='config', default=None,
        help="File path of PV configuration files, use default if not defined")
parser.add_argument('--show-config', dest='show_config', default=False,
        type=bool, const=True, nargs='?',
        help="Print the content of configuration file to stdout")
parser.add_argument('--rate', dest='rate', default=None, type=float,
        help="DAQ rate, use one from configuration file if not defined")
parser.add_argument('--nshot', dest='nshot', default=None, type=int,
        help="Total DAQ shots, use one from configuration file if not defined")
parser.add_argument('--verbose', '-v', action='count', default=1,
        help="Verbosity level of the log output, default output progress, -v: with description")
parser.add_argument('-o', '--output', dest='output', default=None,
        help="File path for output data, print to stdout if not defined")
parser.add_argument('-f', '--output-format', dest='fmt', default='csv',
        help="File format for output data, supported: csv, hdf, excel, html, ...")
parser.add_argument('--format-args', dest='fmt_args', type=json.loads, default='{}',
        help='''Additional arguments passed to data export function in the form of dict, e.g. '{"key":"data"}' (for hdf format)''')
parser.add_argument('--version', dest='show_version', default=False,
        type=bool, const=True, nargs='?',
        help="Print version info")

prog = os.path.basename(sys.argv[0])
parser.epilog = \
"""
Examples:
# Fetch with default configurations
$ {n}                              # print fetched data on stdout, support piping.
$ {n} -vv                          # show progress info.
$ {n} -o data.[csv,hdf,excel,html] # save fetched data into a file.

# Override DAQ parameters
$ {n} -vv --rate 1 --shot 10       # Fetch data at 1 shot per second for 10 shots in total.

# Output configuration file
$ {n} --show-config                # print configuration file content to stdout, support piping.

# Work with user-defined configuration file
$ {n} --config <config filepath> --vv -o data.csv
""".format(n=prog)

def main():
    args = parser.parse_args(sys.argv[1:])

    # version info
    if args.show_version:
        print(f"{prog}: version {VER}\nShow help message with -h option.")
        sys.exit(0)

    # PV configs
    if args.config is None:
        config_path = DEFAULT_META_CONF_PATH
    else:
        if not os.path.isfile(args.config):
            print("Invalid file path for configurations.")
            parser.print_help()
            sys.exit(1)
        else:
            config_path = args.config

    # show configs?
    if args.show_config:
        with open(config_path, "r") as fp:
            print(fp.read(), file=sys.stdout)
        sys.exit(0)

    # override config if possible
    # parse config
    conf = get_meta_conf_dict(config_path)
    mach_state_conf = merge_mach_conf(conf, args.rate, args.nshot)

    # fetch data
    dset = fetch_data(mach_state_conf, verbose=args.verbose)

    # output
    output = args.output
    if output is None:
        print(dset.to_string())
    else:
        attr_fmt = f"to_{args.fmt}"
        if hasattr(dset, attr_fmt):
            if args.fmt == 'hdf':
                args.fmt_args.setdefault('key', 'data')
            getattr(dset, attr_fmt)(output, **args.fmt_args)
        else:
            print(f"{args.fmt}: no supported export function.")
            sys.exit(1)
