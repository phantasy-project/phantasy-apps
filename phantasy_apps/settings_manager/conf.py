# -*- coding: utf-8 -*-

"""App configurations.
"""

import os
import shutil
import toml
from itertools import cycle
from phantasy_apps.utils import find_dconf

def read_app_config(config_file: str = None):
    """Read the app configuration from *config_file*, if it is None,
    follow the search rules defined in *find_dconf*.

    Returns
    -------
    r : dict
        A dict as the app configurations.
    """
    # all keys startwith _ will not be persistent
    if config_file is None:
        config_file = find_dconf("settings_manager", "settings_manager.toml")
    print(f"Settings Manager: loading configurations from '{config_file}'.")
    # app conf
    app_conf = toml.load(config_file)
    app_conf['_FILEPATH'] = os.path.abspath(config_file)
    return app_conf




# user configurations
USER_APP_CONF_DIR = "~/.phantasy"

# distributed with app
DEFAULT_APP_CONF_PATH = find_dconf("settings_manager", "sm_default.toml")

# APP_CONF = toml.load(APP_CONF_PATH)

# data refresher
# NPROC = APP_CONF['DATA_REFRESH']['NCORE']

# machine state capture
# MS_CONF_PATH = APP_CONF['MACH_STATE']['CONFIG_PATH']
# MS_ENABLED = APP_CONF['MACH_STATE']['ENABLED']
# MS_DAQ_RATE = APP_CONF['MACH_STATE']['DAQ_RATE']
# MS_DAQ_NSHOT = APP_CONF['MACH_STATE']['DAQ_NSHOT']

# data source and path
# DATA_SOURCE_MODE = APP_CONF['DATA_SOURCE']['TYPE']
# DB_ENGINE = APP_CONF['DATA_SOURCE']['DB_ENGINE']
# DATA_URI = os.path.expanduser(APP_CONF['DATA_SOURCE']['URI'])

# pref
# FIELD_INIT_MODE = APP_CONF['SETTINGS']['FIELD_INIT_MODE']
# INIT_SETTINGS = APP_CONF['SETTINGS']['INIT_SETTINGS']
# T_WAIT = APP_CONF['SETTINGS']['T_WAIT']
# N_DIGIT = APP_CONF['SETTINGS']['PRECISION']

# default machine/segment
DEFAULT_MACHINE = "FRIB"
DEFAULT_SEGMENT = "LINAC"

# others not controlled with config file
N_SNP_MAX = cycle([50, 100, 500, 'All'])


def init_user_config():
    """Test if user app configuration file exists, if not, reset.
    """
    user_config_dir = os.path.abspath(os.path.expanduser(USER_APP_CONF_DIR))
    user_config_path = os.path.join(user_config_dir, 'settings_manager.toml')
    if not os.path.isfile(user_config_path):
        reset_app_config()
    return user_config_path


def reset_app_config():
    """Copy default app configuration file to *target_path*.
    """
    target_path = os.path.abspath(os.path.expanduser(USER_APP_CONF_DIR))
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    fullpath = os.path.join(target_path, 'settings_manager.toml')
    shutil.copy2(DEFAULT_APP_CONF_PATH, fullpath)
