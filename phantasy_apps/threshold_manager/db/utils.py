#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import os
from ..data import SnapshotData

cdir = os.path.dirname(os.path.abspath(__file__))


def create_connection(db_file: str) -> sqlite3.Connection:
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as err:
        print(err)
    else:
        return conn


def init_db(db_file: str):
    conn = create_connection(db_file)
    cursor = conn.cursor()
    with open(os.path.join(cdir, "init.sql"), 'r') as fp:
        cursor.executescript(fp.read())
        conn.commit()
    conn.close()


def ensure_connect_db(db_file: str) -> sqlite3.Connection:
    """Connect a db file, otherwise create a new one then connect.
    """
    init_db(db_file) # ensure db_file is ready to use.
    return sqlite3.connect(db_file)


def insert_update_data(conn, snp_data: SnapshotData, table_name: str):
    if get_data(conn, snp_data, table_name) == []:
        insert_data(conn, snp_data, table_name)
    else:
        update_data(conn, snp_data, table_name)


def insert_data(conn, snp_data: SnapshotData, table_name: str):
    data_tuple = snp_data.ts, snp_data.user, \
        snp_data.ion_name, snp_data.ion_num, \
        snp_data.ion_mass, snp_data.ion_charge, snp_data.ion_charge1, \
        snp_data.beam_power, snp_data.beam_energy, snp_data.beam_dest, \
        snp_data.tags, snp_data.note, \
        snp_data.to_blob()
    cursor = conn.cursor()
    _insert_data(cursor, table_name, *data_tuple)
    conn.commit()


def update_data(conn, snp_data: SnapshotData, table_name: str):
    cursor = conn.cursor()
    query = f""" UPDATE {table_name} SET
    note = ?, tags = ? WHERE timestamp = ? """
    cursor.execute(query, (snp_data.note, snp_data.tags, snp_data.ts))
    conn.commit()
    cursor.close()


def get_data(conn, snp_data: SnapshotData, table_name: str) -> list[SnapshotData]:
    cursor = conn.cursor()
    ts = snp_data.ts
    r = cursor.execute(f" SELECT * FROM {table_name} WHERE timestamp = '{ts}' ")
    data = r.fetchall()
    cursor.close()
    return data


def _insert_data(cursor, table_name: str, *data):
    query = f''' INSERT INTO {table_name} (timestamp, user, ion_name, ion_number, ion_mass, ion_charge, ion_charge1, beam_power, beam_energy, beam_dest, tags, note, data) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?); '''
    try:
        cursor.execute(query, data)
    except sqlite3.Error as err:
        print(err)
    else:
        cursor.close()


def delete_data(conn, ts: str, table_name: str):
    cursor = conn.cursor()
    try:
        cursor.execute(f''' DELETE FROM {table_name} WHERE timestamp = '{ts}' ''')
    except sqlite3.Error as err:
        print(err)
    else:
        cursor.close()
        conn.commit()
