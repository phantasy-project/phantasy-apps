# -*- coding: utf-8 -*-

import sqlite3


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

