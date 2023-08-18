# -*- coding: utf-8 -*-

"""App configurations.
"""

import os
import shutil
import toml
from phantasy_apps.utils import find_dconf

# default machine/segment
# (only being used in SnapshotData setter of machine/segment)
DEFAULT_MACHINE = "FRIB"
DEFAULT_SEGMENT = "LINAC"


def get_foi_dict(filepath: str):
    """Return a dict of field of interest per element type.
    """
    conf = toml.load(filepath)
    return {k: v['fields'] for k, v in conf.items()}


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
    print(f"Settings Manager: loading configurations from:\n'{config_file}'.")
    # app conf
    app_conf = toml.load(config_file)
    app_conf["_FILEPATH"] = os.path.abspath(config_file)

    # field-of-interest config, if not defined, use default one.
    try:
        foi_filepath = os.path.expanduser(app_conf['FIELD_OF_INTEREST']['FILEPATH'])
        if not os.path.isabs(foi_filepath):
            foi_filepath = os.path.abspath(
                    os.path.join(os.path.dirname(app_conf['_FILEPATH']), foi_filepath))
    except:
        foi_filepath = find_dconf("settings_manager", "fields.toml")
    finally:
        foi_conf = get_foi_dict(foi_filepath)
        app_conf['_FOI'] = foi_conf
    return app_conf


def reset_app_config():
    """Copy default app configuration file to user's home directory (~/.phantasy)
    """
    # distributed with app
    default_app_conf_path = find_dconf("settings_manager", "sm_default.toml")
    target_path = os.path.abspath(os.path.expanduser("~/.phantasy"))
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    fullpath = os.path.join(target_path, 'settings_manager.toml')
    shutil.copy2(default_app_conf_path, fullpath)
    return fullpath
