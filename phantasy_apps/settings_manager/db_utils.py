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
    query = ''' INSERT INTO attachment (name, uri, ftyp, created, note) VALUES (?, ?, ?, ?, ?); '''
    try:
        cursor.execute(query, (attach_data.name, attach_data.uri, attach_data.ftyp, attach_data.created, attach_data.note))
    except sqlite3.Error as err:
        print(err)
    else:
        cursor.close()
    conn.commit()

def update_attach_data(conn, attach_name: str, new_data: str,
                       edit_column: str):
    # edit_column: name, ftyp, note
    attach_id = get_attach_id(conn, attach_name)
    cursor = conn.cursor()
    query = f""" UPDATE attachment SET {edit_column} = ? WHERE id = ? """
    cursor.execute(query, (new_data, attach_id))
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


def get_attach_id(conn, attach_name: str):
    cursor = conn.cursor()
    r = cursor.execute(f" SELECT id FROM attachment WHERE name = '{attach_name}' ")
    data = r.fetchone()
    cursor.close()
    return data[0]


# snp <--> attach
def get_attachments(conn, snp_name: str):
    """Return a list of attachment data associated with the given snapshot data.
    """
    cursor = conn.cursor()
    r = cursor.execute(f"""
        SELECT attachment.id, attachment.name, attachment.uri, attachment.ftyp,
               attachment.created, attachment.note
        FROM attachment JOIN snp_attach ON snp_attach.attachment_id = attachment.id
        WHERE snp_attach.snapshot_name = '{snp_name}';""")
    data = r.fetchall()
    cursor.close()
    return [AttachmentData(*i[1:]) for i in data]


def get_attachments_cnt(conn, snp_name: str):
    """Return the total number of attached attachments with the given snapshot data.
    """
    try:
        with conn:
            r = conn.execute(f""" SELECT COUNT(attachment.id) FROM attachment
                    JOIN snp_attach ON snp_attach.attachment_id = attachment.id
                    WHERE snp_attach.snapshot_name = '{snp_name}';""")
            n = r.fetchone()[0]
    except Exception as err:
        print(f"Failed get_attachments_cnt() for '{snp_name}'\n{err}")
        n = 0
    finally:
        return n


def insert_snp_attach(conn, snp_name: str, attach_name: str):
    """Add attachment of *attach_name* to snapshot with *snp_name*.
    """
    attach_id = get_attach_id(conn, attach_name)
    new_attached = False
    with conn:
        try:
            conn.execute("""INSERT INTO snp_attach (snapshot_name, attachment_id)
            VALUES (?, ?)""", (snp_name, attach_id))
        except sqlite3.IntegrityError as err:
            print(f"Attaching attachment '{attach_id}' to snapshot '{snp_name}'\n{err}")
        else:
            print(f"Attached attachment '{attach_id}' to snapshot '{snp_name}'")
            new_attached = True
    return new_attached


def delete_snp_attach(conn, snp_name: str, attach_name: str):
    """Delete attachment of *attach_str* from snapshot with *snp_name*.
    """
    attach_id = get_attach_id(conn, attach_name)
    new_detached = False
    with conn:
        try:
            conn.execute(f"""DELETE FROM snp_attach WHERE snapshot_name = '{snp_name}'
            AND attachment_id = '{attach_id}';""")
        except Exception as err:
            print(f"Detaching attachment '{attach_id}' from snapshot '{snp_name}'\n{err}")
        else:
            print(f"Detached attachment '{attach_id}' from snapshot '{snp_name}'")
            new_detached = True
    return new_detached
