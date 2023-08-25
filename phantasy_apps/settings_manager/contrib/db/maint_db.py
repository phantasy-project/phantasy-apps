#!/usr/bin/env python
# coding: utf-8

# Database Maintenance

import pandas as pd
import random
from datetime import datetime
from datetime import timedelta
import sqlite3
import numpy as np
from phantasy_apps.settings_manager.data import read_sql


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
    df.drop(columns=['name'], inplace=True)
    con.close()

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
        df.to_sql('snapshot', con_new, index=False, if_exists='replace')
        con_new.execute("CREATE INDEX IF NOT EXISTS datetime_idx ON snapshot (datetime)")
    con_new.close()


if __name__ == "__main__":
    input_db = "/home/tong/Downloads/20230816T000001_SM.db"
    output_db = "/home/tong/Downloads/20230816T000001_SM_new.db"
    # input_db = "/home/tong/Dropbox/phantasy-project/phantasy-apps/phantasy_apps/settings_manager/testdata/settings_manager/sm1.db"
    # output_db = "/home/tong/Dropbox/phantasy-project/phantasy-apps/phantasy_apps/settings_manager/testdata/settings_manager/sm1_new.db"

    process_db(input_db, output_db)
