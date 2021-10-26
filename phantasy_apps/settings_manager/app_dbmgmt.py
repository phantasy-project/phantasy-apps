#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

from phantasy_ui import get_open_directory
from phantasy_ui import get_save_filename
from phantasy_ui import get_open_filename

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

    @pyqtSlot()
    def on_select_db1_path(self):
        """Choose filepath for source database.
        """
        filepath, ext = get_open_filename(self, caption="Select a database file",
                                          type_filter='SQLite File (*.db);;Other Files (*.*)')
        if filepath is None:
            return
        self.db1_path_lineEdit.setText(filepath)

    @pyqtSlot()
    def on_select_db2_path(self):
        """Choose filepath for target database.
        """
        filepath, ext = get_open_filename(self, caption="Select a database file",
                                          type_filter='SQLite File (*.db);;Other Files (*.*)')
        if filepath is None:
            return
        self.db2_path_lineEdit.setText(filepath)

    @pyqtSlot()
    def on_merge(self):
        """Merge source db to target db.
        """
        from phantasy_apps.settings_manager.contrib.db.db_utils import ensure_connect_db, insert_data
        db1_path = self.db1_path_lineEdit.text()
        db2_path = self.db2_path_lineEdit.text()
        try:
            conn1 = ensure_connect_db(db1_path)
            conn2 = ensure_connect_db(db2_path)
            cursor1 = conn1.cursor()
            cursor2 = conn2.cursor()
            r = cursor1.execute("SELECT * FROM snapshot")
            cnt = 0
            for i in r.fetchall():
                insert_data(cursor2, *i[1:])
                cnt += 1
        except sqlite3.Error as err:
            QMessageBox.warning(self, "Merge Database",
                                err, QMessageBox.Ok)
        else:
            conn2.commit()
            QMessageBox.information(self, "Merge Database",
                                    f"Merged {cnt} records from {db1_path} to {db2_path}.",
                                    QMessageBox.Ok)
        finally:
            cursor2.close()
            conn2.close()
            cursor1.close()
            conn1.close()

    @pyqtSlot()
    def on_select_backdb_path(self):
        """Choose filepath for backup db file.
        """
        filepath, ext = get_save_filename(self, caption="Select a database file",
                                          type_filter='SQLite File (*.db);;Other Files (*.*)')
        if filepath is None:
            return
        self.backdb_path_lineEdit.setText(filepath)

    @pyqtSlot()
    def on_back_up(self):
        """Back up db.
        """
        from phantasy_apps.settings_manager.contrib.db.db_utils import create_connection, ensure_connect_db, insert_data
        backdb_path = self.backdb_path_lineEdit.text()
        db_path = self.parent.data_uri_lineEdit.text()

        try:
            conn = create_connection(db_path)
            conn_bk = ensure_connect_db(backdb_path)
            cursor = conn.cursor()
            cursor_bk = conn_bk.cursor()
            for i in cursor.execute("SELECT * FROM snapshot").fetchall():
                insert_data(cursor_bk, *i[1:])
            conn_bk.commit()
        except:
            QMessageBox.warning(self, "Back up Database",
                                f"Failed to create a backup of {db_path}.",
                                QMessageBox.Ok)
        else:
            cursor_bk.close()
            conn_bk.close()
            cursor.close()
            conn.close()
            QMessageBox.information(self, "Back up Database",
                                    f"Create a backup of {db_path} at {backdb_path}.",
                                    QMessageBox.Ok)
