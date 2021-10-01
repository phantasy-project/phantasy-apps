#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

from phantasy_ui import get_open_directory
from phantasy_ui import get_save_filename

from .ui.ui_dbmgmt import Ui_Dialog


class DBManagerDialog(QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        super(DBManagerDialog, self).__init__()
        self.parent = parent

        # UI
        self.setupUi(self)
        self.setWindowTitle("Manage Database")

    @pyqtSlot()
    def on_select_init_db_file(self):
        """Choose filepath for init db file.
        """
        filepath, ext = get_save_filename(self, caption="Select a database file",
                                          type_filter='SQLite File (*.db);;Other Files (*.*)')
        if filepath is None:
            return
        self.init_db_path_lineEdit.setText(filepath)

    @pyqtSlot()
    def on_init_db(self):
        """Initialize database.
        """
        from phantasy_apps.settings_manager.contrib.db.db_utils import init_db
        try:
            filepath = self.init_db_path_lineEdit.text()
            init_db(filepath)
        except:
            QMessageBox.warning(self, "Init Database",
                                f"Failed to initialize database at {filepath}.",
                                QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Init Database",
                                    f"Initialized database at {filepath}.",
                                    QMessageBox.Ok)

    @pyqtSlot()
    def on_select_snpdir(self):
        """Choose directory for snapshot files.
        """
        d = get_open_directory(self)
        if not os.access(d, os.W_OK):
            return
        self.snpdirpath_lineEdit.setText(d)

    @pyqtSlot()
    def on_select_db_file(self):
        """Choose filepath for generated records, update existing one or
        create a new one.
        """
        filepath, ext = get_save_filename(self, caption="Select a database file",
                                          type_filter='SQLite File (*.db);;Other Files (*.*)')
        if filepath is None:
            return
        self.db_path_lineEdit.setText(filepath)

    @pyqtSlot()
    def on_file2db(self):
        """Convert files to db records.
        """
        from phantasy_apps.settings_manager.contrib.db.db_utils import file2db
        try:
            dbpath = self.db_path_lineEdit.text()
            smpath = self.snpdirpath_lineEdit.text()
            cnt = file2db(dbpath, smpath)
        except:
            QMessageBox.warning(self, "Generate Database",
                                f"Failed to add data to database at {dbpath}.",
                                QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Generate Database",
                                    f"Added {cnt} records to database at {dbpath}.",
                                    QMessageBox.Ok)
