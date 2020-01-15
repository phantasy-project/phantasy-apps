# -*- coding: utf-8 -*-

import random
import time

import epics
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMessageBox

# https://getbootstrap.com/docs/4.0/utilities/colors/
COLOR_DANGER = QColor('#DC3545')
COLOR_INFO = QColor('#17A2B8')
COLOR_WARNING = QColor('#FFC107')
COLOR_PRIMARY = QColor('#007BFF')


def delayed_exec(f, delay, *args, **kws):
    """Execute *f* after *delay* msecm `*args` and `**kws` is for *f*.
    """

    def func():
        return f(*args, **kws)

    QTimer.singleShot(delay, func)


def milli_sleep(qApp, msec):
    t0 = time.time()
    while (time.time() - t0) * 1000 < msec:
        qApp.processEvents()
