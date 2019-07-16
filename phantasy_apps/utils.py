# -*- coding: utf-8 -*-
import os


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


def find_dconf(app_name, app_ini_file):
    """Find parameter configuration file, searching the following locations:
    * ~/.phantasy/<app_ini_file>
    * /etc/phantasy/<app_ini_file>
    * package location: <app>/config/<app_ini_file>

    Parameters
    ----------
    app_name : str
        Name of app sub-package.
    app_ini_file : str
        Name of app ini config file.

    Returns
    -------
    r : str
        App config path or None.
    """
    home_conf = os.path.expanduser("~/.phantasy/{}".format(app_ini_file))
    sys_conf = "/etc/phantasy/{}".format(app_ini_file)
    if os.path.isfile(home_conf):
        return home_conf
    elif os.path.isfile(sys_conf):
        return sys_conf
    else:
        basedir = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(basedir, '{}/config/{}'.format(
            app_name, app_ini_file))
        try:
            assert os.path.isfile(path)
        except AssertionError:
            return None
        else:
            return path


if __name__ == '__main__':
    t = 12345
    assert uptime(t) == "03:25:45"

    t = 123455
    assert uptime(t) == "1 day, 10:17:35"

    t = 1234555
    assert uptime(t) == "14 days, 06:55:55"
