#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox

from phantasy_ui.widgets import DataAcquisitionThread as DAQT
from .contrib.db.db_utils import ensure_connect_db

from .data import read_data
from .db_utils import insert_update_data

from .ui.ui_import import Ui_Dialog


class ImportSNPDialog(QDialog, Ui_Dialog):
    # refresh the database
    sigRefreshDatabase = pyqtSignal()

    def __init__(self, parent=None):
        super(ImportSNPDialog, self).__init__()
        self.parent = parent

        # UI
        self.setupUi(self)
        self.setWindowTitle("Import Snapshots from Files")

        #
        self.filepath_list = []
        self.import_pb.setVisible(False)

    @pyqtSlot()
    def onClearFiles(self):
        """Clear selected filepaths.
        """
        self.filepaths_textEdit.clear()
        self.filepath_list.clear()

    @pyqtSlot()
    def onOpenFiles(self):
        """open .csv, .xlsx files.
        """
        filepaths, _ = QFileDialog.getOpenFileNames(
                        self, "Select one or more files",
                        "",
                        "Snapshots (*.csv *.xlsx)");
        if filepaths == []:
            return
        for _f in filepaths:
            if _f not in self.filepath_list:
                self.filepath_list.append(_f)
                self.filepaths_textEdit.appendPlainText(_f)

    @pyqtSlot()
    def onImportSnapshots(self):
        """Click OK to load settings.
        """
        def _import_file(filepath):
            conn = ensure_connect_db(self.parent.data_uri)
            snp_data = read_data(filepath)
            snp_data.extract_blob()
            for _tag in tag_list:
                if _tag not in snp_data.tags:
                    snp_data.tags.append(_tag)
            insert_update_data(conn, snp_data)
            return filepath

        def _import_started():
            self.import_pb.setVisible(True)

        def _import_progressed(p: float, s: str):
            self.import_pb.setValue(int(p * 100))

        def _import_done(r):
            filepaths = "\n".join(f"{i+1:d}: {f}" for i,f in enumerate(r))
            self.sigRefreshDatabase.emit()
            self.import_pb.setVisible(False)
            QMessageBox.information(self, "Import Snapshots",
                    f"Imported {len(r)} files:\n{filepaths}", QMessageBox.Ok, QMessageBox.Ok)
            self.accept()

        tag_str = self.tags_lineEdit.text()
        if tag_str != '':
            tag_list = [i.strip() for i in tag_str.split(",")]
        else:
            tag_list = []

        th = DAQT(daq_func=_import_file, daq_seq=self.filepath_list)
        th.daqStarted.connect(_import_started)
        th.progressUpdated.connect(_import_progressed)
        th.resultsReady.connect(_import_done)
        th.start()

