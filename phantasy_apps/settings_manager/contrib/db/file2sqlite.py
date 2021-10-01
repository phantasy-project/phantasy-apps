#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pack snapshot files of Settings Manager to a SQLite database.

Usage: file2sqlite.py

Tong Zhang <zhangt@frib.msu.edu>
2021-09-23 13:26:42 EDT
"""

from db_utils import file2db, init_db


db_filepath = "sm.db"
sm_path="/files/shared/ap/settings_manager"

# init
init_db(db_filepath)

# add data
file2db(db_filepath, sm_path)
