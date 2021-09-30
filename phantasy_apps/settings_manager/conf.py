# -*- coding: utf-8 -*-

"""App configurations.
"""

import toml
from itertools import cycle
from phantasy_apps.utils import find_dconf

# app config
# ~/.phantasy/settings_manager.toml or
# <app-dir>/config/settings_manager.toml
APP_CONF = toml.load(find_dconf("settings_manager", "settings_manager.toml"))

# data refresher
NPROC = APP_CONF['DATA_REFRESH']['NCORE']

# machine state capture
MS_CONF_PATH = APP_CONF['MACH_STATE']['CONFIG_PATH']
MS_ENABLED = APP_CONF['MACH_STATE']['ENABLED']

# data source and path
DATA_SOURCE_MODE = APP_CONF['DATA_SOURCE']['TYPE']
DB_ENGINE = APP_CONF['DATA_SOURCE']['DB_ENGINE']
DATA_URI = APP_CONF['DATA_SOURCE']['URI']

# pref
FIELD_INIT_MODE = APP_CONF['SETTINGS']['FIELD_INIT_MODE']
INIT_SETTINGS = APP_CONF['SETTINGS']['INIT_SETTINGS']
T_WAIT = APP_CONF['SETTINGS']['T_WAIT']
TOLERANCE = APP_CONF['SETTINGS']['TOLERANCE']
N_DIGIT = APP_CONF['SETTINGS']['PRECISION']
# for elements,settings,tolerance.json files
SUPPORT_CONFIG_PATH = APP_CONF['SETTINGS']['SUPPORT_CONFIG_PATH']

# others not controlled with config file
N_SNP_MAX = cycle([10, 20, 50, 100, 'All'])



