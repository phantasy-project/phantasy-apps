#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox

from phantasy import epoch2human
from phantasy_ui import get_save_filename

from .ui.ui_save import Ui_Dialog

TS_FMT = "%Y%m%dT%H%M%S"


class SaveDataDialog(QDialog, Ui_Dialog):

    def __init__(self, cdir: str, parent):
        super(SaveDataDialog, self).__init__()
        self.cdir = cdir
        self.parent = parent

        # UI
        self.setupUi(self)
        self.setWindowTitle("Save Data to Files")

        #
        self._post_init()

    def _post_init(self):
        self.dirpath_lineEdit.setText(self.cdir)
        self.auto_fill_filepath()

    def auto_fill_filepath(self):
        """Auto fill filepath with timestamp.

        fullpath: <root-dirpath>/ISRC1/20231113T161310_X.[json|png]
        """
        # ISRC{i} as the subdirectory
        isrc_id = self.parent._headinfo_widget.getIonSourceId()
        self.subdir = isrc_id
        # X or Y as the suffix
        xoy = self.parent._headinfo_widget.getOrientation()
        #
        ctime = epoch2human(time.time(), fmt=TS_FMT)
        data_fn = f"{ctime}_{xoy}"
        self.filepath_lineEdit.setText(f"{data_fn}.json")
        _parent_dirpath = os.path.abspath(os.path.join(self.cdir, f"{self.subdir}"))
        self.filepath_lineEdit.setToolTip(os.path.join(_parent_dirpath, data_fn, ".json"))
        #
        if not os.path.exists(_parent_dirpath):
            os.makedirs(_parent_dirpath)

    @pyqtSlot()
    def on_save_data(self):
        print("SaveDataDialog: Save Data")
        note = self.note_plainTextEdit.toPlainText()
        self._save_data(note=note)
        if self.save_image_chkbox.isChecked():
            self._save_image()

    def _save_image(self):
        # save image.
        _filepath = self.filepath_lineEdit.text()
        filepath = os.path.abspath(os.path.join(self.cdir, self.subdir, _filepath))
        png_filepath = filepath.rsplit(".", 1)[0] + ".png"
        print(f"Save image to {png_filepath}")
        self.parent._save_results_as_image(png_filepath)

    def _save_data(self, **kws):
        # save data.
        try:
            _filepath = self.filepath_lineEdit.text()
            filepath = os.path.abspath(os.path.join(self.cdir, self.subdir, _filepath))
            self.parent._save_data_to_file(filepath, **kws)
        except:
            QMessageBox.warning(self, "Save Data",
                    "Failed to save data to {}.".format(filepath),
                    QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Save Data",
                    "Saved data to {}.".format(filepath),
                    QMessageBox.Ok)
        finally:
            self.close()
