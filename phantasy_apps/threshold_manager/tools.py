#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from getpass import getuser
import sqlite3
from phantasy_ui.widgets import BeamSpeciesDisplayWidget
from phantasy_apps.threshold_manager.data import (SnapshotData, ISRC_INDEX_MAP)
from phantasy_apps.threshold_manager.db.utils import insert_update_data

from ._model import _get_dataframe
from ._model import _get_dataframe_

TABLE_NAME = "mps_threshold"


def take_snapshot(dtypes: list[str],
                  note: str,
                  tags: list,
                  conn: sqlite3.Connection,
                  meta_isrc_name: str = 'Live'):
    """Take a snasphot based on *dtype* for the MPS threshold data.

    Parameters
    ----------
    dtypes : list
        A list of device types, a device type could be `ND`, `IC` or `HMR`.
    note : str
        A string of note.
    tags : list
        A list of strings as tags.
    conn : sqlite3.Connection
        Database connection object.
    meta_isrc_name : str
        Name of the ion source, could be `Live`, `Artemis` or `HP-ECR`.
    """
    ts = time.time()
    user = getuser()
    isrc_name, ion_name, ion_mass, ion_number, ion_charge, ion_charge_state, \
        beam_power, beam_energy, beam_bound, beam_dest = \
            BeamSpeciesDisplayWidget.get_species_meta_full(ISRC_INDEX_MAP[meta_isrc_name])
    data_dict = {_dtype: _get_dataframe(_dtype) for _dtype in dtypes}
    _row_data = (ts, user, isrc_name, ion_name, ion_number, ion_mass, ion_charge,
                 ion_charge_state, beam_power, beam_energy, beam_bound, beam_dest,
                 ','.join(tags), note, data_dict)
    snp_data = SnapshotData(_row_data)
    insert_update_data(conn, snp_data, TABLE_NAME)
    # print(f"Saved data {snp_data} to the database.")


def make_snapshot(dtypes: list[str],
                  data: dict,
                  note: str,
                  tags: list,
                  conn: sqlite3.Connection):
    """Make a snapshot from the given data, and add it to the database.
    
    Parameters
    ----------
    dtypes : list
        A list of device types, a device type could be `ND`, `IC` or `HMR`.
    data : dict
        A dict of data for the snasphot.
    note : str
        A string of note.
    tags : list
        A list of strings as tags.
    conn : sqlite3.Connection
        Database connection object.
    """
    ts = data['timestamp']
    user = data['user']
    isrc_name, ion_name, ion_mass, ion_number, ion_charge, ion_charge_state, \
        beam_power, beam_energy, beam_bound, beam_dest = data['isrc_name'], data['ion_name'], \
            data['ion_mass'], data['ion_number'], data['ion_charge'], data['ion_charge_state'], \
            data['power'], data['energy'], data['bound'], 'N/A'
    data_dict = {_dtype: _get_dataframe_(_dtype, data) for _dtype in dtypes}
    _row_data = (ts, user, isrc_name, ion_name, ion_number, ion_mass, ion_charge,
                 ion_charge_state, beam_power, beam_energy, beam_bound, beam_dest,
                 ','.join(tags), note, data_dict)
    snp_data = SnapshotData(_row_data)
    insert_update_data(conn, snp_data, TABLE_NAME)
