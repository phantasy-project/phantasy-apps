#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import Qt
from phantasy_apps.settings_manager.data import AttachmentData
from phantasy_ui import get_open_filename
from phantasy_apps.settings_manager.db_utils import insert_update_attach

from .ui.ui_attach import Ui_Dialog


class AttachDialog(QDialog, Ui_Dialog):

    def __init__(self, conn, parent):
        super(self.__class__, self).__init__()
        self.parent = parent
        self.conn = conn

        self.setupUi(self)
        self.setWindowTitle("Attachments")

        self._post_init()

    def _post_init(self):
        #
        self.filepath = ''
        self.filetype = ''
        self.filename = ''
        # signals and slots
        self.attach_btn.clicked.connect(self.on_click_attach)
        self.browse_btn.clicked.connect(self.on_click_browse)
        self.upload_btn.clicked.connect(self.on_click_upload)
        self.uritype_cbb.currentTextChanged.connect(self.on_uri_type_changed)
        # initial signals
        self.uritype_cbb.currentTextChanged.emit('File')
        #

        attach_list = [
                AttachmentData('n1', '/tmp/test1.csv', 'csv'),
                AttachmentData('n3', '/tmp/test3.xlsx', 'xlsx'),
                AttachmentData('n2', '/tmp/test2.txt', 'txt'),
        ]
        self.m = AttachDataModel(attach_list)
        self.attach_view.setModel(self.m)
        self.attach_view.resizeColumnsToContents()

    @pyqtSlot()
    def on_click_attach(self):
        """Attach the checked attachments.
        """
        print(self.m.get_checked_items())

    @pyqtSlot()
    def on_click_browse(self):
        """Choose the file.
        """
        filepath, ext = get_open_filename(self, type_filter='Other Files (*.*)')
        if filepath is None:
            return
        filename = os.path.basename(filepath)
        ext = filename.rsplit('.', 1)[-1]
        self.filetype = ext.upper()
        self.filename = filename
        self.filepath = filepath
        print(f"Selected {filepath}[{ext}]")
        self.filepath_lineEdit.setText(self.filepath)
        self.filetype_lineEdit.setText(self.filetype)
        self.filename_lineEdit.setText(self.filename)

    @pyqtSlot()
    def on_click_upload(self):
        """Upload the file to attachment database.
        """
        if self.filepath == '':
            return
        print(f"Uploading {self.filepath}...")
        attach_data = AttachmentData(self.filename, self.filepath, self.filetype)
        insert_update_attach(self.conn, attach_data)
        print(f"Uploading {self.filepath}...done")

    @pyqtSlot('QString')
    def on_uri_type_changed(self, s: str):
        """URI type is changed.
        """
        self.filepath_lineEdit.setEnabled(s=='URL')
        self.filetype_lineEdit.setDisabled(s=='URL')
        if s == 'URL':
            self.filetype_lineEdit.setText('hyperlink')
            self.filename_lineEdit.setText('link')
        else:
            self.filetype_lineEdit.setText(self.filetype)
            self.filename_lineEdit.setText(self.filename)


class AttachDataModel(QAbstractTableModel):

    ColumnName, ColumnUri, ColumnFtype, ColumnCount = range(4)

    columnNameMap = {
        ColumnName: "Name",
        ColumnUri: "URI",
        ColumnFtype: "Type",
    }

    def __init__(self, data: list, parent=None):
        super(self.__class__, self).__init__(parent)
        # data: a list of AttachmentData
        self._data = data
        # initial checkstate
        self._checkstate_list = [False] * len(self._data)

    def __post_init(self):
        pass

    def columnCount(self, parent=None):
        return self.ColumnCount

    def rowCount(self, parent=QModelIndex):
        if parent.isValid():
            return 0
        return len(self._data)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None
        row, column = index.row(), index.column()
        if role == Qt.DisplayRole:
            return self._data[row][column]
        if role == Qt.EditRole:
            return self._data[row][column]
        if column == 0 and role == Qt.CheckStateRole:
            return Qt.Checked if self._checkstate_list[row] else Qt.Unchecked
        return None

    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole):
        if not index.isValid() or not role in (Qt.CheckStateRole, Qt.EditRole):
            return False
        row, column = index.row(), index.column()
        if role == Qt.EditRole:
            o_val = self._data[row][column]
            if value != o_val:
                self._data[row][column] = value
                self.dataChanged.emit(index, index, (Qt.DisplayRole, Qt.EditRole))
                return True
        if role == Qt.CheckStateRole and column == 0:
            self._checkstate_list[row] = value == Qt.Checked
            self.dataChanged.emit(index, index, [Qt.CheckStateRole])
            return True
        return False

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if orientation != Qt.Horizontal:
            return None
        if role != Qt.DisplayRole:
            return None
        return self.columnNameMap.get(section)

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return Qt.NoItemFlags
        if index.column() == self.ColumnName:
            return Qt.ItemIsUserCheckable | QAbstractTableModel.flags(self, index)
        if index.column() in (self.ColumnUri, self.ColumnFtype):
            return Qt.ItemIsEditable | QAbstractTableModel.flags(self, index)
        return QAbstractTableModel.flags(self, index)

    def get_checked_items(self):
        return [idata for idata, is_checked in zip(self._data, self._checkstate_list) if is_checked]

