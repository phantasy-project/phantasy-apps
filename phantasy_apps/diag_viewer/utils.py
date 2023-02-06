#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import partial

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QToolButton

from phantasy_apps.trajectory_viewer.ui import details_icon
from phantasy_apps.trajectory_viewer.utils import ElementListModel


class ElementListModelDV(ElementListModel):
    def __init__(self, parent, mp, enames, **kws):
        ElementListModel.__init__(self, parent, mp, enames, **kws)

    def set_columns(self):
        v = self._v
        for i, ename in enumerate(self._enames):
            # fields
            elem = self.name_elem_map[ename]
            cbb = QComboBox()
            cbb.addItems(elem.get_eng_fields())
            v.setIndexWidget(self.index(i, self.i_field), cbb)
            elem_item = self.item(i, self.i_name)
            cbb.currentTextChanged.connect(
                    partial(self.on_field_changed, elem_item))
            # info
            btn = QToolButton()
            btn.setIcon(QIcon(QPixmap(details_icon)))
            btn.setIconSize(QSize(24, 24))
            btn.setToolTip("Show details of {}.".format(ename))
            v.setIndexWidget(self.index(i, self.i_info), btn)
            btn.clicked.connect(partial(self.show_elem_info, elem))
        try:
            # emit list of element fields
            self.fieldsSelected.emit(elem.get_eng_fields())
        except:
            print("No selected fields.")
