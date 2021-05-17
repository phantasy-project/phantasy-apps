#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Machine state represented with hierachical key-value pairs.
"""
import time
import toml
import numpy as np
import pandas as pd
from collections import OrderedDict
from datetime import datetime
from epics import caget_many, caget
from phantasy_apps.utils import find_dconf
from phantasy_apps.msviz import TQDM_INSTALLED

TS_FMT = "%Y-%m-%dT%H:%M:%S.%f"
DEFAULT_META_CONF_PATH = find_dconf("msviz", "metadata.toml")


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


def merge_mach_conf(conf, rate=None, nshot=None):
    """Merge toml conf to a dict, override with valid arguments.

    Parameters
    ----------
    conf : dict
        Dict parsed from toml config file.
    rate : float
        DAQ rate in Hz, if defined, override the one in config file.
    nshot : int
        Total number of shots for DAQ, if defined, override the one in config file.

    Returns
    -------
    r : dict
        Dict for machine state config.
    """
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
    mach_state_conf = {'pv_list': pv_list, 'grp_list': grp_list,
                       'daq_rate': daq_rate, 'daq_nshot': daq_nshot}
    return mach_state_conf


def fetch(confpath=None, rate=None, nshot=None, verbose=1):
    """Get machine state by fetching all PV readings defined in *confpath*.

    Parameters
    ----------
    confpath : str
        Filepath for the PV configuration file, .toml.
    rate : float
        DAQ rate in Hz, if defined, override the one in config file.
    nshot : int
        Total number of shots for DAQ, if defined, override the one in config file.
    verbose : int
        Verbosity level of the log output, default is 0, no output, 1, output progress, 2 output
        progress with description.

    Returns
    -------
    r : DataFrame
        DataFrame of all PV reading with group and PV names as the index.
    """
    conf = get_meta_conf_dict(confpath)
    mach_state_conf = merge_mach_conf(conf, rate, nshot)
    return fetch_data(mach_state_conf, verbose=verbose)


def fetch_data(mach_state_conf, verbose=0):
    """Do data fetching based on configuration defined in *mach_state_conf*.

    Parameters
    ----------
    mach_state_conf : dict
        Dict configuration, key: 'pv_list', 'grp_list', 'daq_rate', 'daq_nshot'.
    verbose : int
        Verbosity level of the log output, default is 0, no output, 1, output progress, 2 output
        progress with description.

    Returns
    -------
    r : DataFrame
        DataFrame of all PV reading with group and PV names as the index.
    """
    daq_nshot = mach_state_conf['daq_nshot']
    daq_rate = mach_state_conf['daq_rate']
    pv_list = mach_state_conf['pv_list']
    grp_list = mach_state_conf['grp_list']
    n_pv = len(pv_list)

    if verbose != 0 and TQDM_INSTALLED:
        from phantasy_apps.msviz import tqdm
        pbar = tqdm(range(daq_nshot))
    else:
        pbar = range(daq_nshot)

    ts_list = [0] * daq_nshot
    arr = np.zeros([daq_nshot, len(pv_list)])
    dt = 1.0 / daq_rate  # second
    for i in pbar:
        t0 = time.time()
        arr[i, :] = caget_many(pv_list)
        t0_str = datetime.fromtimestamp(t0).strftime(TS_FMT)[:-3]
        desc = f"[{t0_str}] Fetched {n_pv} PVs data"
        ts_list[i] = t0_str
        t_elapsed = time.time() - t0
        t_sleep = dt - t_elapsed
        if t_sleep > 0:
            desc += f", waited {int(t_sleep * 1000)} ms"
            time.sleep(t_sleep)
        if verbose > 1:
            if TQDM_INSTALLED:
                pbar.set_description(desc)
            else:
                print(desc)

    df = pd.DataFrame(arr.transpose(), columns=ts_list)
    df.set_index([pv_list, grp_list], inplace=True)
    df.index.names = ['PV', 'Group']
    df['avg'] = df.iloc[:, 0:daq_nshot].mean(axis=1)
    df['std'] = df.iloc[:, 0:daq_nshot].std(axis=1)

    return df


def _daq_func(pv_list, delta_t):
    # pv_list : a list of PVs
    # delta_t : 1.0 / daq_rate in second
    #
    # work with DAQT (daq_func)
    #
    t0 = time.time()
    arr = [caget(i) for i in pv_list]
    t_elapsed = time.time() - t0
    t_wait = delta_t - t_elapsed
    if t_wait > 0:
        time.sleep(t_wait)
    return arr + [t0]


def _build_dataframe(arr_list, pv_list, grp_list):
    # build a dataframe from a list of pv readings:
    # -------------------------------------------------
    #             | ts-1 | ts-2 | ... | avg | std |
    # -------------------------------------------------
    # PV  | Group |
    # PV1 | g1    | ...
    # ...
    # the last column of arr_list is timestamps
    #
    # work with DAQT (resultsReady) only.
    #
    arr = np.asarray(arr_list).transpose()
    data = arr[:-1,:]
    ts_list = [datetime.fromtimestamp(i).strftime(TS_FMT)[:-3] for i in arr[-1]]
    _, nshot = data.shape
    df = pd.DataFrame(data, columns=ts_list)
    df.set_index([pv_list, grp_list], inplace=True)
    df.index.names = ['PV', 'Group']
    df['avg'] = df.iloc[:, 0:nshot].mean(axis=1)
    df['std'] = df.iloc[:, 0:nshot].std(axis=1)
    return df


if __name__ == '__main__':
    print(fetch())