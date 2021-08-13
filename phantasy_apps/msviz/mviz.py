#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Widget for machine state visualization.
"""

from PyQt5.QtWidgets import QWidget

from .ui.ui_mviz import Ui_Form


class MVizWidget(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__()
        self.parent = parent

        # UI
        self.setupUi(self)

        
