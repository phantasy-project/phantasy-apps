#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog

from .ui.ui_ormviz import Ui_Dialog


class MVizDialog(QDialog, Ui_Dialog):

    def __init__(self, parent=None, matrix=None, **kws):
        super(self.__class__, self).__init__()
        self.parent = parent
        self._matrix = matrix

        self.setupUi(self)
        self.setWindowTitle("Response Matrix")

        #
        self._post_init()

    def _post_init(self):
        self._o = self.matplotlibimageWidget
        self._o.setFigureYlabel("BPM ID")
        self._o.setFigureXlabel("Corrector ID")

    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, m):
        self._matrix = m

    def plot(self):
        # self._o.setXData()
        # self._o.setYData()
        self._o.update_image(self._matrix)




