#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QVariant
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from phantasy.library.settings import generate_settings
from phantasy_ui import get_open_filename

from .ui.ui_loadfrom import Ui_Dialog
from .utils import convert_settings


class LoadSettingsDialog(QDialog, Ui_Dialog):
    # signal: settings loaded, emit flat_settings and settings.
    settingsLoaded = pyqtSignal(QVariant, QVariant)

    def __init__(self, parent=None):
        super(LoadSettingsDialog, self).__init__()
        self.parent = parent

        # UI
        self.setupUi(self)
        self.setWindowTitle("Load Settings From File")

    @pyqtSlot()
    def on_open_snpfile(self):
        """open .snp file.
        """
        filepath, ext = get_open_filename(self,
                                          type_filter="SNP Files (*.snp);;CSV Files (*.csv)")
        if filepath is None:
            return
        self.filepath_lineEdit.setText(filepath)

    @pyqtSlot()
    def on_load(self):
        """Click OK to load settings.
        """
        mp = self.parent._mp
        if mp is None:
            QMessageBox.warning(self, "Load Settings",
                                "Please load lattice first.",
                                QMessageBox.Ok)
        else:
            snpfile = self.filepath_lineEdit.text()
            settings = generate_settings(snpfile=snpfile,
                                         lattice=mp.work_lattice_conf,
                                         only_physics=False)
            flat_settings = convert_settings(settings, mp)
            self.settingsLoaded.emit(flat_settings, settings)

            self.accept()
