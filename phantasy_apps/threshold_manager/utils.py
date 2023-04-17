#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import (QDate, QDateTime, Qt, QSize, QRect)
from PyQt5.QtGui import (QPixmap, QColor, QPainter, QPen)

ROW_HEIGHT = 48
PX_SIZE = 24

# all ions with icon resources
AVAILABLE_IONS = ('He', 'Ne', 'Ar', 'Kr', 'Xe', 'U', 'Se', 'Ca', 'Pb', 'O',
                  'Bi', 'Zn', 'Tm', 'Pt')
# pixmaps for decorationRole (!= ion_name column)
DECO_PIXMAP_DICT = {}
# pixmaps for decorationRole, (== ion_name column)
ELMT_PIXMAP_ON_DICT = {}
ELMT_PIXMAP_OFF_DICT = {}


def get_pixmap_note():
    return DECO_PIXMAP_DICT.setdefault(
        'note',
        QPixmap(":/tm-icons/comment.png").scaled(
            PX_SIZE, PX_SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation))


def get_pixmap_user():
    return DECO_PIXMAP_DICT.setdefault(
        'user',
        QPixmap(":/tm-icons/person.png").scaled(
            PX_SIZE, PX_SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation))


def get_pixmap_default():
    return QPixmap()


def get_pixmap_element(ion_name: str, state: str = 'on'):
    # pixmaps for decorationRole, (== ion_name column)
    px_size = int(ROW_HEIGHT * 0.98)
    if ion_name in AVAILABLE_IONS:
        if state == 'on':
            return ELMT_PIXMAP_ON_DICT.setdefault(
                ion_name,
                QPixmap(
                    f":/elements/elements/{ion_name}.png").scaledToHeight(
                        px_size, Qt.SmoothTransformation))
        else:  # off
            return ELMT_PIXMAP_OFF_DICT.setdefault(
                ion_name,
                QPixmap(f":/elements/elements/{ion_name}-off.png").
                scaledToHeight(px_size, Qt.SmoothTransformation))
    else:
        px = QPixmap(QSize(px_size, px_size))
        px.fill(QColor(240, 240, 240, 0))
        pt = QPainter(px)
        pt.drawText(QRect(0, 0, px_size, px_size), Qt.AlignCenter, ion_name)
        pt.setPen(QPen(Qt.gray, 2))
        pt.drawRect(QRect(0, 0, px_size, px_size))
        pt.end()
        if state == 'on':
            return ELMT_PIXMAP_ON_DICT.setdefault(ion_name, px)
        else:
            return ELMT_PIXMAP_OFF_DICT.setdefault(ion_name, px)
