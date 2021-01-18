#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Rename snapshot files, apply the new naming convention, to make
them be compatible with Windows platform.

1. Remove ':'
2. If match the old naming rule, rename by the new rule

Usage: rename_snapshot_files <directory keeps snp data files>

Tong Zhang <zhangt@frib.msu.edu>
2021-01-13 16:14:18 EST
"""

import fnmatch
import os
import re
import shutil
import sys
import tempfile


regex = re.compile(r"([0-9]*.*\+[1-9]*\_)([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2})\:([0-9]{2})\:([0-9]{2}).csv")

def main(wdir):
    for root, dnames, fnames in os.walk(wdir):
        for fname in fnmatch.filter(fnames, "*.csv"):
            path = os.path.join(root, fname)
            to_rename = False
            r = regex.match(fname)
            if r is None:
                if ':' in fname:
                    new_path = os.path.join(root, fname.replace(":", ""))
                    to_rename = True
            else:
                new_path = os.path.join(root,
                            f"{r[1]}{r[2]}{r[3]}{r[4]}T{r[5]}{r[6]}{r[7]}.csv")
                to_rename = True

            if to_rename:
                print(f"Rename {path} --> {new_path}")
                update_datafile(path, new_path)
            else:
                print(f"{path}: delete filepath line if existing.")
                update_datafile(path)


def update_datafile(filepath, new_filepath=None):
    # delete filepath line in *filepath*,
    # if new_filepath is provided, do rename
    tmpfile = tempfile.mktemp()
    fp_out = open(tmpfile, 'w')
    for line in open(filepath, 'r'):
        if line.startswith("# filepath"):
            continue
        fp_out.write(line)
    fp_out.close()
    if new_filepath is None:
        shutil.move(tmpfile, filepath)
    else:
        shutil.move(tmpfile, new_filepath)
        os.remove(filepath)


if __name__ == "__main__":
    wdir = sys.argv[1]  # directory name
    main(wdir)
