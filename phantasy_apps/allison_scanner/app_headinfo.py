#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import stat
import shutil
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

from .ui.ui_headinfo import Ui_Form

# map from <sys>_<subsys> to ion source name
ION_SOURCE_PHY_NAME_MAP = {'FE_SCS1': 'Artemis', 'FE_SCS2': 'HP-ECR'}
ION_SOURCE_ID_NAME_MAP = {'FE_SCS1': 'ISRC1', 'FE_SCS2': 'ISRC2'}

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
        # current open data filepath
        self._data_filepath = None
        #
        self.mainFrame.setStyleSheet("""
            QFrame#mainFrame {
                border: 1px solid gray;
        }""")
        self.device_name_lbl.setStyleSheet(f"""
            QLabel {{
                border-top: 0px solid gray;
                border-bottom: 1px solid gray;
                font-family: monospace;
                font-size: {self._fs + 3}pt;
            }}""")
        self.isrc_name_lbl.setStyleSheet(f"""
            QLabel {{
                color: #17A2B8;
                font-family: monospace;
                font-size: {self._fs + 1}pt;
            }}""")
        self.xoy_name_lbl.setStyleSheet(f"""
            QLabel {{
                font-family: monospace;
                font-size: {self._fs + 1}pt;
            }}""")
        self.readfile_btn.clicked.connect(self.onReadDatafile)
        self.saveto_btn.clicked.connect(self.onSaveTo)

    def _show(self):
        self.adjustSize()
        self.show()

    @pyqtSlot('QString')
    def onDeviceChanged(self, name: str):
        """EMS device name is changed.
        """
        self._device_name = name
        self.device_name_lbl.setText(name)
        self._isrc_name = ION_SOURCE_PHY_NAME_MAP[name[0:7]]
        self._isrc_id = ION_SOURCE_ID_NAME_MAP[name[0:7]]
        self.isrc_name_lbl.setText(self._isrc_name)

    @pyqtSlot('QString')
    def onOrientationChanged(self, xoy: str):
        """Orientation (X or Y) of EMS is changed.
        """
        self._xoy = xoy
        self._xoy_name = _XOY_MAP[xoy]
        if xoy == "X":
            color = "#007BFF" # blue
        else:
            color = "#DC3545" # red
        self.xoy_name_lbl.setText(
            f"<span style='color:{color};'>{self._xoy_name}</span>")

    @pyqtSlot(bool)
    def onOnlineModeChanged(self, is_checked: bool):
        """Online mode is changed.
        """
        # show read file button if online mode is False
        self.readfile_btn.setVisible(not is_checked)

    @pyqtSlot('QString')
    def onDataFilepathChanged(self, filepath: str):
        """Current opened data filepath is changed (offline mode).
        """
        self._data_filepath = filepath
        self.readfile_btn.setToolTip(
            "Click to open and read the data from \n'{}'.".format(filepath))

    @pyqtSlot()
    def onReadDatafile(self):
        """Read the opened data file (offline mode only).
        """
        if self._data_filepath is None:
            return
        QDesktopServices.openUrl(QUrl(self._data_filepath))

    @pyqtSlot()
    def onSaveTo(self):
        """Save the data file/image to user-defined location.
        """
        if self._data_filepath is None:
            return
        user_dstdir = QFileDialog.getExistingDirectory(self, "Choose the directory",
                                                    "", QFileDialog.ShowDirsOnly)
        json_file = self._data_filepath
        png_file = json_file.replace("json", "png")
        _copy_file(json_file, user_dstdir)
        if os.path.isfile(png_file):
            _copy_file(png_file, user_dstdir)        
        QMessageBox.information(self, "Save Files",
                                "Saved the following files to {}\n:{}".format(
                                    user_dstdir, '\n'.join([json_file, png_file])),
                                QMessageBox.Ok, QMessageBox.Ok)

    def getIonSourceId(self):
        """Return the ion source id name.
        ISRC1, ISRC2, ...
        """
        return self._isrc_id

    def getOrientation(self):
        """Return X or Y as the orientation.
        """
        return self._xoy

def _copy_file(src_filepath: str, dst_filepath: str):
    shutil.copy2(src_filepath, dst_filepath)
    os.chmod(dst_filepath, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)