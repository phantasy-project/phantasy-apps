#!/usr/bin/env python
# coding: utf-8

# Database Maintenance, run process_db() to update the database scheme 2023/08.

import pandas as pd
import random
from datetime import datetime
from datetime import timedelta
import sqlite3
import numpy as np
from phantasy_apps.settings_manager.data import read_sql
from phantasy_apps.settings_manager.contrib.db.db_utils import init_db


def process_db(input_dbpath: str, output_dbpath: str):
    #
    # Add 'date' column
    # Drop 'name' column
    # Add 'parent' column
    # Create an index on 'datetime' column
    #
    con = sqlite3.connect(input_dbpath)
    df = pd.read_sql('SELECT * FROM snapshot', con)
    df['date'] = df['timestamp'].apply(lambda i: datetime.fromtimestamp(i).strftime("%Y-%m-%d %A"))
    con.close()

    # drop duplicated rows on 'datetime'
    dup_idx = df[df.datetime.duplicated()].index
    if not dup_idx.empty:
        print("Duplicated rows on 'datetime':")
        print(df.loc[dup_idx, ['id', 'timestamp', 'date', 'name', 'note']])
        replace_duplicates = input("Replace 'datetime' with 'name' for the duplicated items? [Y]/N ")
        if replace_duplicates in ('N', 'n'):
            return
        df.loc[dup_idx, 'datetime'] = df.loc[dup_idx, 'name']

    # drop name column
    df.drop(columns=['name'], inplace=True)

    parent_list = []
    n_rows = df.shape[0]
    for i, irow in df.iterrows():
        print(f"Processing {i+1} / {n_rows}...")
        _df_info = read_sql(irow)[1]
        if 'parent' in _df_info:
            parent = _df_info.parent.item()
        else:
            parent = None
        parent_list.append(parent)
    df['parent'] = parent_list

    # write to output db path
    con_new = sqlite3.connect(output_dbpath)
    with con_new:
        df.to_sql('snapshot', con_new, index=False, if_exists='replace',
                  dtype={'id': 'INTEGER PRIMARY KEY AUTOINCREMENT'})
        # see init_db()
        # con_new.execute("CREATE INDEX IF NOT EXISTS datetime_idx ON snapshot (datetime)")
    con_new.close()


if __name__ == "__main__":
    # input_db = "/home/tong/Downloads/20230816T000001_SM.db"
    # output_db = "/home/tong/Downloads/20230816T000001_SM_new.db"
    # input_db = "/home/tong/Dropbox/phantasy-project/phantasy-apps/phantasy_apps/settings_manager/testdata/settings_manager/sm1.db"
    # output_db = "/home/tong/Dropbox/phantasy-project/phantasy-apps/phantasy_apps/settings_manager/testdata/settings_manager/sm1_new.db"
    input_db = "/files/shared/ap/settings_manager/sm.db"
    output_db = "/files/shared/ap/settings_manager/sm_new.db"
    process_db(input_db, output_db)
    init_db(output_db)
