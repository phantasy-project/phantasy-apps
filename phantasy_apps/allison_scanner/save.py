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
        print(self.cdir)
        self.parent = parent

        # UI
        self.setupUi(self)
        self.setWindowTitle("Save Data to File")

        #
        self._post_init()

    def _post_init(self):
        self.auto_fill_filepath()

    @pyqtSlot()
    def on_get_filepath(self):
        cdir = os.path.abspath(
                os.path.dirname(self.filepath_lineEdit.text()))
        filepath, ext = get_save_filename(self,
                cdir=self.cdir,
                type_filter="JSON Files (*.json)")
        if filepath is None:
            return
        self.filepath_lineEdit.setText(filepath)

    def auto_fill_filepath(self):
        """Auto fill filepath with timestamp.
        """
        ctime = epoch2human(time.time(), fmt=TS_FMT)
        fn = "allison_scanner_data_{}.json".format(ctime)
        # dirname = os.path.dirname(self.filepath_lineEdit.text())
        self.filepath_lineEdit.setText(
                os.path.abspath(os.path.join(self.cdir, fn)))

    @pyqtSlot()
    def on_save_data(self):
        print("SaveDataDialog: Save Data")
        note = self.note_plainTextEdit.toPlainText()
        print(note)
        self._save_data(note=note)

    def _save_data(self, **kws):
        # save data.
        try:
            filepath = self.filepath_lineEdit.text()
            ext = filepath.rsplit('.', 1)[-1]
            self.parent._save_data_to_file(filepath, ftype=ext, **kws)
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
