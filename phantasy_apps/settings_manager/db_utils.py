#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from .data import SnapshotData
from .data import AttachmentData


# Snapshot data

def insert_update_data(conn, snp_data: SnapshotData):
    if get_data(conn, snp_data) == []:
        insert_data(conn, snp_data)
    else:
        update_data(conn, snp_data)


def insert_data(conn, snp_data: SnapshotData):
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


def update_data(conn, snp_data: SnapshotData):
    cursor = conn.cursor()
    query = """ UPDATE snapshot SET
    note = ?, tags = ? WHERE datetime = ? """
    cursor.execute(query, (snp_data.note, snp_data.tags_as_str(), snp_data.datetime))
    conn.commit()
    cursor.close()


def get_data(conn, snp_data: SnapshotData):
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
    except sqlite3.Error as err:
        print(err)
    else:
        cursor.close()


def delete_data(conn, snp_data: SnapshotData):
    cursor = conn.cursor()
    datetime = snp_data.datetime
    try:
        cursor.execute(f''' DELETE FROM snapshot WHERE datetime = '{datetime}' ''')
    except sqlite3.Error as err:
        print(err)
    else:
        cursor.close()
        conn.commit()


# attachment data
def insert_attach_data(conn, attach_data: AttachmentData):
    cursor = conn.cursor()
    query = ''' INSERT INTO attachment (name, uri, ftyp) VALUES (?, ?, ?); '''
    try:
        cursor.execute(query, (attach_data.name, attach_data.uri, attach_data.ftyp))
    except sqlite3.Error as err:
        print(err)
    else:
        cursor.close()
    conn.commit()

def update_attach_data(conn, attach_name: str, new_attach_ftyp: str):
    cursor = conn.cursor()
    query = """ UPDATE attachment SET ftyp = ? WHERE name = ? """
    cursor.execute(query, (new_attach_ftyp, attach_name))
    conn.commit()
    cursor.close()


def delete_attach_data(conn, attach_name: str):
    cursor = conn.cursor()
    try:
        cursor.execute(f''' DELETE FROM attachment WHERE name = '{attach_name}' ''')
    except sqlite3.Error as err:
        print(err)
    else:
        cursor.close()
        conn.commit()


def get_attach_data(conn, attach_data: AttachmentData):
    cursor = conn.cursor()
    name = attach_data.name
    r = cursor.execute(f" SELECT * FROM attachment WHERE name = '{name}' ")
    data = r.fetchall()
    cursor.close()
    return data


# snp <--> attach
def get_attachments(conn, snp_name: str):
    """Return a list of attachment data associated with the given snapshot data.
    """
    cursor = conn.cursor()
    r = cursor.execute(f"""
        SELECT attachment.name, attachment.uri, attachment.ftyp FROM attachment
        JOIN snp_attach ON snp_attach.attachment_name = attachment.name
        WHERE snp_attach.snapshot_name = '{snp_name}';""")
    data = r.fetchall()
    cursor.close()
    return [AttachmentData(*i) for i in data]


def insert_snp_attach(conn, snp_name: str, attach_name: str):
    """Add attachment of *attach_name* to snapshot with *snp_name*.
    """
    new_attached = False
    with conn:
        try:
            conn.execute("""INSERT INTO snp_attach (snapshot_name, attachment_name)
            VALUES (?, ?)""", (snp_name, attach_name))
        except sqlite3.IntegrityError as err:
            print(f"Attaching '{attach_name}' to '{snp_name}'\n{err}")
        else:
            print(f"Attached '{attach_name}' to '{snp_name}'")
            new_attached = True
    return new_attached


def delete_snp_attach(conn, snp_name: str, attach_name: str):
    """Delete attachment of *attach_name* from snapshot with *snp_name*.
    """
    new_detached = False
    with conn:
        try:
            conn.execute(f"""DELETE FROM snp_attach WHERE snapshot_name = '{snp_name}'
            AND attachment_name = '{attach_name}';""")
        except Exception as err:
            print(f"Detaching '{attach_name}' from '{snp_name}'\n{err}")
        else:
            print(f"Detached '{attach_name}' from '{snp_name}'")
            new_detached = True
    return new_detached
