#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def insert_data(conn, snp_data):
    data_tuple = snp_data.timestamp, snp_data.datetime, snp_data.name, \
         snp_data.note, \
         snp_data.user, snp_data.ion_name, \
         int(snp_data.ion_number), int(snp_data.ion_mass), \
         int(snp_data.ion_charge), snp_data.machine, \
         snp_data.segment, snp_data.tags_as_str(), \
         snp_data.app, snp_data.version, 'xlsx', snp_data.to_blob()
    cursor = conn.cursor()
    _insert_data(cursor, *data_tuple)
    conn.commit()


def _insert_data(cursor, *data):
    cmd = ''' INSERT INTO snapshot (timestamp, datetime, name, note, user, ion_name, ion_number, ion_mass, ion_charge, machine, segment, tags, app, version, data_format, data) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?); '''
    cursor.execute(cmd, data)
    cursor.close()
