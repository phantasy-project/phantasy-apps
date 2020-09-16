# -*- coding: utf-8 -*-

import os
import time
from phantasy import epoch2human
from mpl4qt.widgets.utils import MatplotlibCurveWidgetSettings
from PyQt5.QtCore import QLibraryInfo
from PyQt5.QtCore import QProcess
from subprocess import Popen

TS_FMT = "%Y-%m-%dT%H:%M:%S.%f"


def find_dconf(app_name, conf_file):
    """Find app configuration file, searching the following locations:
    * ~/.phantasy/<conf_file>
    * /etc/phantasy/<conf_file>
    * package location: <app_name>/config/<conf_file>

    Parameters
    ----------
    app_name : str
        Name of app sub-package.
    conf_file : str
        Name of app config file, e.g. .ini or .json (for mpl widgets).

    Returns
    -------
    r : str
        App config path or None.
    """
    home_conf = os.path.expanduser("~/.phantasy/{}".format(conf_file))
    sys_conf = "/etc/phantasy/{}".format(conf_file)
    if os.path.isfile(home_conf):
        return home_conf
    elif os.path.isfile(sys_conf):
        return sys_conf
    else:
        basedir = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(basedir, '{}/config/{}'.format(
            app_name, conf_file))
        try:
            assert os.path.isfile(path)
        except AssertionError:
            return None
        else:
            return path


def apply_mplcurve_settings(widget, app_name, json_path=None, filename=None):
    """Apply JSON settings read from *json_path* to *widget*.

    Parameters
    ----------
    widget : MatplotlibCurveWidget
        Instance of MatplotlibCurveWidget.
    app_name : str
        Name of app sub-package.
    json_path : str
        Path of JSON settings file.
    """
    if json_path is None:
        json_path = find_dconf(app_name, filename)
    s = MatplotlibCurveWidgetSettings(json_path)
    widget.apply_mpl_settings(s)


def current_datetime(ctime=None, fmt=None):
    """Return the human readable datetime string from epoch time ticks.

    See Also
    --------
    :func:`~phantasy.library.misc.epoch2human`
    """
    t = time.time() if ctime is None else ctime
    f = TS_FMT if fmt is None else fmt
    return epoch2human(t, fmt=f)


class Assistant(object):

    def __init__(self, path=None):
        self.qhc_path = path
        self.exec_path = os.path.join(
            QLibraryInfo.location(QLibraryInfo.BinariesPath), 'assistant')

    def start(self):
        cmdline = self.exec_path + " -collectionFile " + self.qhc_path
        Popen(cmdline, shell=True)


def launch_assistant(path):
    assistant = Assistant(path=path)
    assistant.start()


if __name__ == '__main__':
    path = "/home/tong/Dropbox/phantasy-project/documentation/sm-doc/qhc/settings_manager.qhc"
    launch_assistant(path)
