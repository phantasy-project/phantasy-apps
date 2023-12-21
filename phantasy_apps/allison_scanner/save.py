#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QDesktopServices
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
        try:
            self.auto_fill_filepath()
        except Exception as err:
            QMessageBox.critical(self, "Save Data", f"Failed: {err}", QMessageBox.Ok)

    @pyqtSlot()
    def on_locate_dir(self):
        """Reveal the root data directory in File Exeplorer.
        """
        dirpath = self.dirpath_lineEdit.text()
        QDesktopServices.openUrl(QUrl(dirpath))

    def auto_fill_filepath(self):
        """Auto fill filepath with timestamp.

        fullpath: <root-dirpath>/ISRC1/20231113T161310_36Ar_X.[json|png]
        """
        # ISRC{i} as the subdirectory
        isrc_id = self.parent._headinfo_widget.getIonSourceId()
        self.subdir = isrc_id
        # X or Y as the suffix
        xoy = self.parent._headinfo_widget.getOrientation()
        # ion name and mass
        ion_name = self.parent.ion_name_lineEdit.text()
        ion_mass = int(self.parent.ion_mass_lineEdit.text())
        #
        ctime = epoch2human(time.time(), fmt=TS_FMT)
        data_fn = f"{ctime}_{ion_mass}{ion_name}_{xoy}"
        self.filepath_lineEdit.setText(f"{data_fn}.json")
        _parent_dirpath = os.path.abspath(os.path.join(self.cdir, f"{self.subdir}"))
        self.dirpath_lineEdit.setText(_parent_dirpath)
        self.filepath_lineEdit.setToolTip(os.path.join(_parent_dirpath, data_fn, ".json"))
        #
        if not os.path.exists(_parent_dirpath):
            os.makedirs(_parent_dirpath)

    @pyqtSlot()
    def on_save_data(self):
        note = self.note_plainTextEdit.toPlainText()
        self._save_data(note=note)
        if self.save_image_chkbox.isChecked():
            self._save_image()

    def _save_image(self):
        # save image.
        _filepath = self.filepath_lineEdit.text()
        filepath = os.path.abspath(os.path.join(self.cdir, self.subdir, _filepath))
        png_filepath = filepath.rsplit(".", 1)[0] + ".png"
        if os.path.exists(png_filepath):
            r = QMessageBox.warning(self, "Save Image", f"Overwriting the existing '{png_filepath}'?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if r == QMessageBox.No:
                return
        self.parent._save_results_as_image(png_filepath)

    def _save_data(self, **kws):
        # save data.
        try:
            _filepath = self.filepath_lineEdit.text()
            filepath = os.path.abspath(os.path.join(self.cdir, self.subdir, _filepath))
            if os.path.exists(filepath):
                r = QMessageBox.warning(self, "Save Data", f"Overwriting the existing '{filepath}'?" \
                                        + "\n" + "Hint: clicking the 'Auto' button to update the filename.",
                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if r == QMessageBox.No:
                    return
            self.parent._save_data_to_file(filepath, **kws)
        except Exception as err:
            mbox = QMessageBox(QMessageBox.Critical, "Save Data", 
                    f"Failed to save data to {filepath}.\n{err}",
                    QMessageBox.Ok, self)
            mbox.move(self.parent.geometry().center() - QPoint(int(self.geometry().width() / 2), 0))
            mbox.exec_()
        else:
            mbox = QMessageBox(QMessageBox.Information, "Save Data",
                    f"Saved data to {filepath}.",
                    QMessageBox.Ok, self)
            mbox.move(self.parent.geometry().center() - QPoint(int(self.geometry().width() / 2), 0))
            mbox.exec_()
            self.close()
