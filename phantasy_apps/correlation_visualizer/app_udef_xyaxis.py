#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Hint window for user-defined xyaxis.
"""

from PyQt5.QtWidgets import QWidget

from phantasy_apps.correlation_visualizer.ui.ui_udef_xyaxis import Ui_Form


class UDFXYAxisWindow(QWidget, Ui_Form):

    def __init__(self, parent, html_text):
        super(UDFXYAxisWindow, self).__init__()
        self.parent = parent

        # UI
        self.setupUi(self)
        self.setWindowTitle("Write UDF for XY-Axis")

        self.body_textEdit.setHtml(html_text)
