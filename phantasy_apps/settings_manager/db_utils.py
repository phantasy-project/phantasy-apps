#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlite3 import Error


def insert_update_data(conn, snp_data):
    if get_data(conn, snp_data) == []:
        insert_data(conn, snp_data)
    else:
        update_data(conn, snp_data)


def insert_data(conn, snp_data):
    data_tuple = snp_data.timestamp, snp_data.datetime, \
         snp_data.note, snp_data.user, snp_data.ion_name, \
         snp_data.ion_number, snp_data.ion_mass, \
         snp_data.ion_charge, snp_data.machine, \
         snp_data.segment, snp_data.tags_as_str(), \
         snp_data.app, snp_data.version, \
         snp_data.data_format, snp_data.to_blob(), \
         snp_data.date, snp_data.parent
    cursor = conn.cursor()
    _insert_data(cursor, *data_tuple)
    conn.commit()


def update_data(conn, snp_data):
    cursor = conn.cursor()
    query = """ UPDATE snapshot SET
    note = ?, tags = ? WHERE datetime = ? """
    cursor.execute(query, (snp_data.note, snp_data.tags_as_str(), snp_data.datetime))
    conn.commit()
    cursor.close()


def get_data(conn, snp_data):
    cursor = conn.cursor()
    datetime = snp_data.name
    r = cursor.execute(f" SELECT * FROM snapshot WHERE datetime = '{datetime}' ")
    data = r.fetchall()
    cursor.close()
    return data


def _insert_data(cursor, *data):
    query = ''' INSERT INTO snapshot (timestamp, datetime, note, user, ion_name, ion_number, ion_mass, ion_charge, machine, segment, tags, app, version, data_format, data, date, parent) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?); '''
    try:
        cursor.execute(query, data)
    except Error as err:
        print(err)
    else:
        cursor.close()


def delete_data(conn, snp_data):
    cursor = conn.cursor()
    datetime = snp_data.datetime
    try:
        cursor.execute(f''' DELETE FROM snapshot WHERE datetime = '{datetime}' ''')
    except Error as err:
        print(err)
    else:
        cursor.close()
        conn.commit()
