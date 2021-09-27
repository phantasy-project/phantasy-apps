#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pack snapshot files of Settings Manager to a SQLite database.

Usage: file2sqlite.py

Tong Zhang <zhangt@frib.msu.edu>
2021-09-23 13:26:42 EDT
"""

import sqlite3
from db_utils import create_connection, insert_data, get_blob
import pathlib
from phantasy_apps.settings_manager.data import read_data


db_filepath = "sm.db"
sm_path="/home/tong/Dropbox/phantasy-project/phantasy-apps/phantasy_apps/settings_manager/testdata/settings_manager"

conn = create_connection(db_filepath)
cursor = conn.cursor()

# init
with open('init.sql', 'r') as fp:
    cursor.executescript(fp.read())
    conn.commit()

# add data
cnt = 0
for path in pathlib.Path(sm_path).glob("**/*"):
    if not path.is_file():
        continue
    snp_data = read_data(path)
    if snp_data is None:
        print(f"Failed to load {path.resolve()}")
        continue
    data_tuple = snp_data.timestamp, snp_data.datetime, snp_data.name, \
                 snp_data.note, \
                 snp_data.user, snp_data.ion_name, \
                 int(snp_data.ion_number), int(snp_data.ion_mass), \
                 int(snp_data.ion_charge), snp_data.machine, \
                 snp_data.segment, snp_data.tags_as_str(), \
                 snp_data.app, snp_data.version, path.suffix[1:], get_blob(path)
    cnt += 1
    print(f"{cnt:>02d} Insert with data from {path}...")
    insert_data(cursor, *data_tuple)

conn.commit()
cursor.close()
conn.close()
