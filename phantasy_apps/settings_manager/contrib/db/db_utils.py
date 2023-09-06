# -*- coding: utf-8 -*-

import sqlite3
import os
import pathlib
from phantasy_apps.settings_manager.data import read_data


cdir = os.path.dirname(os.path.abspath(__file__))

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as err:
        print(err)
    else:
        return conn


def insert_data(cursor, *data):
    cmd = ''' INSERT INTO snapshot (timestamp, datetime, name, note, user, ion_name, ion_number, ion_mass, ion_charge, machine, segment, tags, app, version, data_format, data) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?); '''
    cursor.execute(cmd, data)


def get_blob(filepath):
    # pathlib.Path
    with filepath.open('rb') as fp:
        return fp.read()


def init_db(db_file):
    conn = create_connection(db_file)
    cursor = conn.cursor()
    with open(os.path.join(cdir, "init.sql"), 'r') as fp:
        cursor.executescript(fp.read())
        conn.commit()
    conn.close()


def file2db(db_file, sm_path):
    # add data
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cnt = 0
    for path in sorted(pathlib.Path(sm_path).glob("**/*"), key=os.path.getctime):
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
    return cnt


def ensure_connect_db(db_file: str,
                      constraint_foreign_keys: bool = True):
    """Connect a db file, otherwise create a new one then connect.
    """
    init_db(db_file) # ensure db_file is ready to use.
    conn = sqlite3.connect(db_file)
    if constraint_foreign_keys:
        conn.execute('PRAGMA foreign_keys = ON;')
    return conn
