# -*- coding: utf-8 -*-

import os
import time
from phantasy import epoch2human
from mpl4qt.widgets.utils import MatplotlibCurveWidgetSettings

TS_FMT = "%Y-%m-%dT%H:%M:%S.%f"


def uptime(t):
    """Convert *t* in second to uptime with the tuple of days, hours,
    minutes, and seconds, and return string of uptime.

    Examples
    --------
    >>> assert uptime(12345) == "03:25:45"
    >>> assert uptime(123455) == "1 day, 10:17:35"
    >>> assert uptime(1234555) == "14 days, 06:55:55"
    """
    MINUTE = 60
    HOUR = MINUTE * 60
    DAY = HOUR * 24

    days = int(t / DAY)
    hours = int((t % DAY) / HOUR)
    minutes = int((t % HOUR) / MINUTE)
    seconds = int(t % MINUTE)

    s = ''
    if days > 0:
        s += str(days) + " " + (days == 1 and "day" or "days") + ", "
    s += '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
    return s


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


if __name__ == '__main__':
    t = 12345
    assert uptime(t) == "03:25:45"

    t = 123455
    assert uptime(t) == "1 day, 10:17:35"

    t = 1234555
    assert uptime(t) == "14 days, 06:55:55"
