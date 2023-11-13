#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot

from .ui.ui_headinfo import Ui_Form


# map from <sys>_<subsys> to ion source name
ION_SOURCE_PHY_NAME_MAP = {'FE_SCS1': 'Artemis', 'FE_SCS2': 'HP-ECR'}

# map x or y to horizontal or vertical
_XOY_MAP = {'X': 'Horizontal', 'Y': 'Vertical'}


class HeadinfoForm(QWidget, Ui_Form):

    def __init__(self, parent, font_size: int):
        super(self.__class__, self).__init__()
        self.parent = parent
        self._fs = font_size

        self.setupUi(self)
        self._post_init()

    def _post_init(self):
        bw = 1
        self.device_name_lbl.setStyleSheet(f"""
            QLabel {{
                border-top: {bw}px solid gray;
                border-left: {bw + 2}px solid gray;
                border-right: {bw}px solid gray;
                border-bottom: {bw}px solid gray;
                font-family: monospace;
                font-size: {self._fs + 2}pt;
            }}""")
        self.isrc_name_lbl.setStyleSheet(f"""
            QLabel {{
                border-top: 0px solid gray;
                border-left: {bw + 2}px solid gray;
                border-bottom: {bw}px solid gray;
                font-family: monospace;
                font-size: {self._fs + 1}pt;
            }}""")
        self.xoy_name_lbl.setStyleSheet(f"""
            QLabel {{
                border-top: 0px solid gray;
                border-right: {bw}px solid gray;
                border-bottom: {bw}px solid gray;
                font-family: monospace;
                font-size: {self._fs + 1}pt;
            }}""")

    def _show(self):
        self.adjustSize()
        self.show()

    @pyqtSlot('QString')
    def onDeviceChanged(self, name: str):
        """EMS device name is changed.
        """
        self.device_name_lbl.setText(name)
        self.isrc_name_lbl.setText(ION_SOURCE_PHY_NAME_MAP[name[0:7]])

    @pyqtSlot('QString')
    def onOrientationChanged(self, xoy: str):
        """Orientation (X or Y) of EMS is changed.
        """
        self.xoy_name_lbl.setText(_XOY_MAP[xoy])

    @pyqtSlot(bool)
    def onOnlineModeChanged(self, is_checked: bool):
        """Online mode is changed.
        """
        # show read file button if online mode is False
        self.readfile_btn.setVisible(not is_checked)
