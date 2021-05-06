#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Machine state represented with hierachical key-value pairs.
"""
import time
import toml

import numpy as np
import pandas as pd

from collections import OrderedDict
from epics import caget_many

from phantasy_apps.utils import find_dconf
from phantasy_ui import printlog


DEFAULT_META_CONF_PATH = find_dconf("settings_manager", "metadata.toml")

def get_meta_conf_dict(filepath=None):
    """Return a dict of config for metadata, if *filepath* is not defined,
    use the default one.

    Parameters
    ----------
    filepath : str
        Filepath for the toml config file.

    Returns
    -------
    r : dict
        Dict of configuration.
    """
    if filepath is None:
        filepath = DEFAULT_META_CONF_PATH
    conf = toml.load(filepath)
    return conf


def fetch(confpath=None, verbose=False, rate=None, nshot=None):
    """Get machine state by fetching all PV readings defined in *confpath*.

    Parameters
    ----------
    confpath : str
        Filepath for the PV configuration file, .toml.
    verbose : bool
        Show log message if set.
    rate : float
        DAQ rate in Hz, if defined, override the one in config file.
    nshot : int
        Total number of shots for DAQ, if defined, override the one in config file.

    Returns
    -------
    r : DataFrame
        DataFrame of all PV reading with group and PV names as the index.
    """
    conf = get_meta_conf_dict(confpath)

    daq_conf = conf.pop('DAQ')
    daq_rate = daq_conf['rate']
    daq_nshot = daq_conf['nshot']

    if rate is not None and isinstance(rate, (float, int)):
        daq_rate = rate
    if nshot is not None and isinstance(nshot, int):
        daq_nshot = nshot

    pv_list = []
    grp_list = []
    for sect_name, sect_conf in conf.items():
        names = sect_conf['names']
        pv_list.extend(names)
        grp_list.extend([sect_name] * len(names))

    arr = np.zeros([daq_nshot, len(pv_list)])
    dt = 1.0 / daq_rate  # second
    for i in range(daq_nshot):
        t0 = time.time()
        arr[i, :] = caget_many(pv_list)
        t_elapsed = time.time() - t0
        if t_elapsed < dt:
            time.sleep(dt - t_elapsed)
        if verbose:
            printlog(f"Fetched data: shot {i + 1}.")
    df = pd.DataFrame(arr.transpose(), columns=[f'shot-{i}' for i in range(1, daq_nshot + 1)])
    df.set_index([pv_list, grp_list], inplace=True)
    df.index.names = ['PV', 'Group']
    df['avg'] = df.iloc[:, 0:daq_nshot].mean(axis=1)
    df['std'] = df.iloc[:, 0:daq_nshot].std(axis=1)

    return df

def _build_dataframe(arr_list, pv_list, grp_list):
    # build a dataframe from a list of pv readings:
    # -------------------------------------------------
    #             | shot-1 | shot-2 | ... | avg | std |
    # -------------------------------------------------
    # PV  | Group |
    # PV1 | g1    | ...
    # ...
    arr = np.asarray(arr_list).transpose()
    _, nshot = arr.shape
    df = pd.DataFrame(arr, columns=[f'shot-{i}' for i in range(1, nshot + 1)])
    df.set_index([pv_list, grp_list], inplace=True)
    df.index.names = ['PV', 'Group']
    df['avg'] = df.iloc[:, 0:nshot].mean(axis=1)
    df['std'] = df.iloc[:, 0:nshot].std(axis=1)
    return df


if __name__ == '__main__':
    print(fetch())
