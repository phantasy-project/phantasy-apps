#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QDialog

from .utils import X0
from .ui.ui_invalid_elemlist import Ui_Dialog


class InvalidElementListDialog(QDialog, Ui_Dialog):

    def __init__(self, elemlist, parent=None):
        super(InvalidElementListDialog, self).__init__()
        self.parent = parent

        # UI
        self.setupUi(self)
        self.setWindowTitle("Invalid Element List")

        self.set_model(elemlist)

    def set_model(self, elemlist):
        model = _Model(self.treeView, elemlist)
        model.set_model()


class _Model(QStandardItemModel):
    # elemlist: [(ename, {fname, value}]
    def __init__(self, parent, elemlist, **kws):
        super(self.__class__, self).__init__(parent)
        self._data = [(ename, _k, _v) for ename, v in elemlist for _k, _v in v.items()]
        self._tv = parent

        # header
        self.header = self.h_name, self.h_field, self.h_val0 \
                    = ("Device", "Field", f"Setpoint({X0})")
        self.ids = self.i_name, self.i_field, self.i_val0 \
                 = range(len(self.header))

    def set_data(self):
        for ename, fname, fval0 in self._data:
            item_ename = QStandardItem(ename)
            item_fname = QStandardItem(fname)
            item_val0 = QStandardItem(str(fval0))
            row = [item_ename, item_fname, item_val0]
            [i.setEditable(False) for i in row]
            self.appendRow(row)

    def set_model(self):
        # set data
        self.set_data()
        # set model
        self._tv.setModel(self)
        #
        self.__post_init_ui()

    def __post_init_ui(self):
        # set headers
        tv = self._tv
        for i, s in zip(self.ids, self.header):
            self.setHeaderData(i, Qt.Horizontal, s)
        tv.header().setStyleSheet("""
            QHeaderView {
                font-weight: bold;
            }""")
        #
        tv.setStyleSheet("""
            QTreeView {
                font-family: monospace;
                show-decoration-selected: 1;
                alternate-background-color: #D3D7CF;
            }

            QTreeView::item {
                /*color: black;*/
                border: 1px solid #D9D9D9;
                border-top-color: transparent;
                border-bottom-color: transparent;
            }

            QTreeView::item:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);
                border: 1px solid #bfcde4;
            }

            QTreeView::item:selected {
                border: 1px solid #567DBC;
                background-color: #D3D7CF;
            }

            QTreeView::item:selected:active{
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);
            }""")
        self.fit_view()

    def fit_view(self):
        tv = self._tv
        #tv.expandAll()
        for i in self.ids:
            tv.resizeColumnToContents(i)
        #tv.collapseAll()
