# -*- coding: utf-8 -*-

import os
import random
import time
import toml

import epics
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMessageBox

from phantasy_apps.utils import find_dconf as _find_dconf

# https://getbootstrap.com/docs/4.0/utilities/colors/
COLOR_DANGER = QColor('#DC3545')
COLOR_INFO = QColor('#17A2B8')
COLOR_WARNING = QColor('#FFC107')
COLOR_PRIMARY = QColor('#007BFF')


def milli_sleep(qApp, msec):
    t0 = time.time()
    while (time.time() - t0) * 1000 < msec:
        qApp.processEvents()


def find_dconf(path=None, filename="correlation_visualizer.ini"):
    """Find parameter configuration for `correlation_visualizer` if `path` is None.
    searching the following locations:
    * ~/.phantasy/correlation_visualizer.ini
    * /etc/phantasy/correlation_visualizer.ini
    * package location: apps/correlation_visualizer/config/correlation_visualizer.ini
    """

    if path is not None:
        return os.path.abspath(path)
    return _find_dconf('correlation_visualizer', filename)


def get_config(path=None, filename="correlation_visualizer.ini"):
    path_conf = find_dconf(path, filename)
    conf = toml.load(path_conf)
    return conf
