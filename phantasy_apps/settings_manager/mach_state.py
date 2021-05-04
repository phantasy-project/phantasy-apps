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


def get_meta_conf_dict(filepath):
    """Return a dict of config for metadata.
    """
    conf = toml.load(filepath)
    return conf

DEFAULT_META_CONF_PATH = find_dconf("settings_manager", "metadata.toml")
DEFAULT_META_CONF_DICT = get_meta_conf_dict(DEFAULT_META_CONF_PATH)


def fetch(confpath=None, verbose=False):
    """Get machine state by fetching all PV readings defined in *confpath*.

    Parameters
    ----------
    confpath : str
        Filepath for the PV configuration file, .toml.
    verbose : bool
        Show log message if set.

    Returns
    -------
    r : DataFrame
        DataFrame of all PV reading with group and PV names as the index.
    """
    if confpath is None:
        conf = DEFAULT_META_CONF_DICT
    else:
        conf = get_meta_conf_dict(confpath)

    daq_conf = conf.pop('DAQ')
    daq_rate = daq_conf['rate']
    daq_nshot = daq_conf['nshot']

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


if __name__ == '__main__':
    print(fetch())
