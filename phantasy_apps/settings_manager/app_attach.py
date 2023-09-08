#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import shutil
from functools import partial
from PyQt5.QtWidgets import (
        QDialog, QHeaderView,
        QMessageBox, QMenu, QAction, QWidgetAction,
        QStyledItemDelegate, QLabel, QGraphicsDropShadowEffect, QStyle,
        QWidget, QHBoxLayout, QSizePolicy
)
from PyQt5.QtGui import (
        QFontDatabase,
        QIcon,
        QPixmap,
        QDesktopServices
)
from PyQt5.QtCore import (
        pyqtSignal, pyqtSlot,
        QAbstractTableModel,
        QSortFilterProxyModel,
        QModelIndex, Qt, QPoint, QUrl
)
from phantasy_ui import get_open_filename
from phantasy_apps.settings_manager.data import AttachmentData
from phantasy_apps.settings_manager.db_utils import (
        insert_attach_data, update_attach_data, delete_attach_data,
        insert_snp_attach, delete_snp_attach, get_attachments
)
from .ui.ui_attach import Ui_Dialog


FTYP_COLOR_MAP = {
    'TXT': '#5988E6',
    'CSV': '#ED9800',
    'JSON': '#54ED00',
    'JPG': '#E8ED00',
    'LINK': '#ED1700',
}


class AttachDialog(QDialog, Ui_Dialog):

    sigDataModelShown = pyqtSignal()
    sigAttachmentUpdated = pyqtSignal()

    def __init__(self, snp_name: str, snp_longname: str, conn: sqlite3.Connection,
                 data_dir: str, parent):
        super(self.__class__, self).__init__()
        self.parent = parent
        self.conn = conn
        self.data_dir = data_dir
        self.snp_name = snp_name
        self.snp_longname = snp_longname

        self.setupUi(self)
        self.setWindowTitle("Attachments")

        self._post_init()

    def exec_query(self):
        q_str = self.search_lineEdit.text()
        if q_str == '' or q_str == '*':
            q_cond = ''
        else:
            q_cond = f"WHERE name like '%{q_str}%'"
        try:
            with self.conn:
                r = self.conn.execute(f"SELECT name, uri, ftyp, created, note FROM attachment {q_cond}")
                data = [AttachmentData(*i) for i in r.fetchall()]
        except Exception as err:
            print(err)
            data = []
        finally:
            return data

    def _post_init(self):
        # set title line
        self.snp_name_lbl.setText(self.snp_longname)
        # context menu
        self._attach_icon = QIcon(QPixmap(":/sm-icons/attach.png"))
        self._detach_icon = QIcon(QPixmap(":/sm-icons/detach.png"))
        self._delete_icon = QIcon(QPixmap(":/sm-icons/delete.png"))
        self._open_icon = QIcon(QPixmap(":/sm-icons/open.png"))
        self.attach_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.attach_view.customContextMenuRequested.connect(self.on_request_context_menu)
        #
        self.uri_type = 'FILE'
        self.uri_path = ''
        self.uri_name = ''
        self.ftype = ''  # file type, ext, or 'LINK' for uri_type of 'URL'
        # signals and slots
        self.dataModelShown = False
        self.attach_btn.clicked.connect(self.on_click_attach)
        self.browse_btn.clicked.connect(self.on_click_browse)
        self.upload_btn.clicked.connect(self.on_click_upload)
        self.search_btn.clicked.connect(self.on_click_search)
        self.show_checked_btn.clicked.connect(self.on_filter_checked_items)
        self.show_all_btn.clicked.connect(self.on_show_all_items)
        self.uri_type_cbb.currentTextChanged.connect(self.on_uri_type_changed)
        self.sigDataModelShown.connect(self.on_dataModelShown)
        self.sigAttachmentUpdated.connect(self.on_attachmentUpdated)
        # initial signals
        self.uri_type_cbb.currentTextChanged.emit('File')
        #
        self.attach_view.setItemDelegate(AttachDataDelegateModel(self.attach_view))
        # pull db
        self.search_btn.click()

    @pyqtSlot()
    def on_dataModelShown(self):
        self.dataModelShown = True
        if self.m.get_checked_items():
            self.show_checked_btn.clicked.emit()
        else:
            self.show_all_btn.clicked.emit()

    @pyqtSlot()
    def on_attachmentUpdated(self):
        """Add or delete an attachment.
        """
        self.search_btn.clicked.emit()

    @pyqtSlot()
    def on_show_all_items(self):
        """Show all items for attach view.
        """
        self.search_btn.clicked.emit()

    @pyqtSlot()
    def on_filter_checked_items(self):
        """Show only checked items for attach view.
        """
        proxy_model = AttachDataProxyModel(self.m)
        self.attach_view.setModel(proxy_model)
        #
        self.attach_view.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)

    @pyqtSlot(QPoint)
    def on_request_context_menu(self, pos: QPoint):
        m = self.attach_view.model()
        if m is None:
            return
        idx = self.attach_view.indexAt(pos)
        if isinstance(m, AttachDataProxyModel):
            idx = m.mapToSource(idx)
            m = m.sourceModel()
        if idx.column() == m.ColumnName:
            menu = self.__build_menu(idx, m)
            menu.exec_(self.attach_view.viewport().mapToGlobal(pos))

    def __build_menu(self, idx, m):
        # only for 1st col (name).
        menu = QMenu(self)
        menu.setStyleSheet("QMenu {margin: 1px;}")
        # title
        title_w = QLabel(f"Attachment:\n{m.data(idx)}")
        title_w.setStyleSheet("""
        QLabel {
            background: #C8E6C9;
            font-weight: bold;
            padding: 2px 2px 2px 2px;}""")
        title_act = QWidgetAction(self)
        title_act.setDefaultWidget(title_w)
        # open attachment
        open_act = QAction(self._open_icon, "Open", menu)
        open_act.triggered.connect(partial(self.on_open, idx, m))
        # attach
        attach_act = QAction(self._attach_icon, "Attach", menu)
        attach_act.triggered.connect(partial(self.on_attach, idx, m))
        # detach
        detach_act = QAction(self._detach_icon, "Detach", menu)
        detach_act.triggered.connect(partial(self.on_detach, idx, m))
        # delete attachment
        delete_act = QAction(self._delete_icon, "Delete", menu)
        delete_act.triggered.connect(partial(self.on_delete, idx, m))
        #
        menu.addAction(title_act)
        menu.addAction(attach_act)
        menu.addAction(detach_act)
        menu.addSeparator()
        menu.addAction(open_act)
        menu.addAction(delete_act)
        return menu

    @pyqtSlot()
    def on_open(self, idx, m):
        """Open attachment.
        """
        row = idx.row()
        ftype = m.data(m.index(row, AttachDataModel.ColumnFtype))
        uri = m.data(m.index(row, AttachDataModel.ColumnUri))
        if ftype == 'LINK':
            r = QMessageBox.warning(self, "Open an Attachment", "Does not support LINK, but try to open it...",
                    QMessageBox.Ok, QMessageBox.Ok)
            if r == QMessageBox.Ok:
                QDesktopServices.openUrl(QUrl(uri))
        else:
            QDesktopServices.openUrl(QUrl(uri))

    @pyqtSlot()
    def on_attach(self, idx, m):
        name = m.data(idx)
        m.setData(idx, Qt.Checked, Qt.CheckStateRole)
        new_attached = insert_snp_attach(self.conn, self.snp_name, name)
        if new_attached:
            QMessageBox.information(self, "Attach an Attachment",
                    f"Attached '{name}' to '{self.snp_name}'",
                    QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "Attach an Attachment",
                    "Attachment '{name} has already been attached to '{self.snp_name}'",
                    QMessageBox.Ok, QMessageBox.Ok)

    @pyqtSlot()
    def on_detach(self, idx, m):
        name = m.data(idx)
        m.setData(idx, Qt.Unchecked, Qt.CheckStateRole)
        new_detached = delete_snp_attach(self.conn, self.snp_name, name)
        if new_detached:
            QMessageBox.information(self, "Detach an Attachment",
                    f"Detached '{name}' from '{self.snp_name}'",
                    QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "Detach an Attachment",
                    "Attachment '{name} has already been detached from '{self.snp_name}'",
                    QMessageBox.Ok, QMessageBox.Ok)

    @pyqtSlot()
    def on_delete(self, idx, m):
        """Delete the attachment.
        """
        delete_attach_data(self.conn, m.data(idx))
        self.sigAttachmentUpdated.emit()

    @pyqtSlot()
    def on_click_search(self):
        """Search database and present the results.
        """
        # current attachments
        self.current_attach_list = get_attachments(self.conn, self.snp_name)
        self.current_attach_namelist = [i.name for i in self.current_attach_list]
        #
        attach_list = self.exec_query()
        self.m = AttachDataModel(attach_list, self.current_attach_namelist, self.data_dir)
        self.m.dataChanged.connect(self.on_attachment_dataChanged)
        self.attach_view.setModel(self.m)
        self.attach_view.resizeColumnsToContents()
        if not self.dataModelShown:
            self.sigDataModelShown.emit()
        #
        self.attach_view.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)

    def on_attachment_dataChanged(self, tl: QModelIndex, br: QModelIndex, roles: list):
        if Qt.CheckStateRole in roles:
            return
        m = self.attach_view.model()
        if isinstance(m, AttachDataProxyModel):
            m = m.sourceModel()
        row, column = tl.row(), tl.column()
        new_data = m.data(tl, Qt.EditRole)
        col_name = AttachDataModel.editColumnNameMap[column]
        name = m.data(m.index(row, AttachDataModel.ColumnName))
        print(f"Editted {col_name} for {name} -> {new_data} @ ({row}, {column})")
        update_attach_data(self.conn, name, new_data, col_name)

    @pyqtSlot()
    def on_click_attach(self):
        """Attach the checked attachments.
        """
        attach_list = self.m.get_checked_items()
        newly_attached_list = []
        for i in attach_list:
            is_new_attached = insert_snp_attach(self.conn, self.snp_name, i.name)
            if is_new_attached:
                newly_attached_list.append(i.name)
        if newly_attached_list:
            newly_attached_str = '\n'.join(newly_attached_list)
            QMessageBox.information(self, "Attachments Updated",
                    f"Newly Attached:\n{newly_attached_str}",
                    QMessageBox.Ok, QMessageBox.Ok)

    @pyqtSlot()
    def on_click_browse(self):
        """Choose the file.
        """
        filepath, ext = get_open_filename(self, type_filter='Other Files (*.*)')
        if filepath is None:
            return
        filename = os.path.basename(filepath)
        ext = filename.rsplit('.', 1)[-1]
        self.ftype = ext.upper()
        self.uri_name = filename
        self.uri_path = filepath
        self.uri_path_lineEdit.setText(filepath)
        self.uri_name_lineEdit.setText(filename)

    @pyqtSlot()
    def on_click_upload(self):
        """Upload the file to attachment database.
        """
        #
        # - check the file basename, if collides, suggest rename the original one
        # - copy the file to the root directory for attachments
        # - insert to database
        # - re-run search
        #
        if self.uri_path_lineEdit.text() == '':
            return
        print(f"Uploading {self.uri_path} ...")
        if self.uri_type == "URL":
            link_name = self.uri_name_lineEdit.text()
            link_url = self.uri_path_lineEdit.text()
            self.ftype = 'LINK'
            attach_data = AttachmentData(link_name, link_url, self.ftype, None, '')
        else:
            _src_filepath = self.uri_path
            _dst_filename = self.uri_name_lineEdit.text()
            _dst_filepath = os.path.join(self.data_dir, _dst_filename)
            _dst_dirpath = os.path.dirname(_dst_filepath)
            try:
                if not os.path.exists(_dst_dirpath):
                    os.makedirs(_dst_dirpath)
                shutil.copy2(_src_filepath, _dst_filepath)
            except Exception as err:
                QMessageBox.critical(self, "Upload Attachment", f"Failed uploading.\n{err}",
                        QMessageBox.Ok, QMessageBox.Ok)
                return
            attach_data = AttachmentData(_dst_filename, _dst_filename, self.ftype, None, '')
        insert_attach_data(self.conn, attach_data)
        print(f"Uploading {self.uri_path}...done")
        self.sigAttachmentUpdated.emit()

    @pyqtSlot('QString')
    def on_uri_type_changed(self, s: str):
        """URI type is changed, FILE or URL.
        """
        self.uri_type = s.upper()
        if self.uri_type == 'URL':
            self.uri_path_lineEdit.setEnabled(True)
            self.uri_name_lineEdit.setText('mylink')
            self.ftype = 'LINK'
        else: # FILE
            self.uri_path_lineEdit.setEnabled(False)
            self.uri_name_lineEdit.setText(self.uri_name)


DECO_PX_DICT = {}
PX_SIZE = 24

def get_px_file():
    return DECO_PX_DICT.setdefault('file',
            QPixmap(":/sm-icons/file.png").scaled(
                PX_SIZE, PX_SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation))


def get_px_link():
    return DECO_PX_DICT.setdefault('link',
            QPixmap(":/sm-icons/hyperlink.png").scaled(
                PX_SIZE, PX_SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation))


def get_px_note():
    return DECO_PX_DICT.setdefault('note',
            QPixmap(":/sm-icons/comment.png").scaled(
                PX_SIZE, PX_SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation))


class AttachDataModel(QAbstractTableModel):

    ColumnName, ColumnUri, ColumnFtype, ColumnNote, ColumnCreated, ColumnCount = range(6)

    # map column int to header name
    columnNameMap = {
        ColumnName: "Name",
        ColumnUri: "URI",
        ColumnFtype: "Type",
        ColumnNote: "Note",
        ColumnCreated: "Uploaded", # "Created"
    }

    # map column int to table column name
    editColumnNameMap = {
        ColumnFtype: 'ftyp',
        ColumnNote: 'note'
    }

    # map column int to list index in AttachmentData
    columnListIndexMap = {
        ColumnName: 0,
        ColumnUri: 1,
        ColumnFtype: 2,
        ColumnNote: 4,
        ColumnCreated: 3
    }

    def __init__(self, data: list[AttachmentData], attached_namelist: list[str],
                 data_dir: str, parent=None):
        super(self.__class__, self).__init__(parent)
        # root directory for all the datafiles
        self._data_dir = data_dir
        # data: a list of AttachmentData
        self._data = data
        # prefix data_dir to URI
        for i in self._data:
            if i.ftyp == 'LINK':
                continue
            i.uri = os.path.join(data_dir, i.uri)
        # initial checkstate
        self._checkstate_list = [i.name in attached_namelist for i in self._data]

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
        v = self._data[row][AttachDataModel.columnListIndexMap[column]]
        if role == Qt.DisplayRole:
            if column == AttachDataModel.ColumnFtype:
                return ' ' * (len(v) + 2)
            else:
                return v
        if role == Qt.UserRole:
            if column == AttachDataModel.ColumnFtype:
                return v
        if role == Qt.DecorationRole:
            if column == AttachDataModel.ColumnUri:
                if self._data[row][AttachDataModel.columnListIndexMap[
                                    AttachDataModel.ColumnFtype]] == 'LINK':
                    return get_px_link()
                else:
                    return get_px_file()
            elif column == AttachDataModel.ColumnNote:
                return get_px_note()
        if role == Qt.EditRole:
            return v
        if column == 0 and role == Qt.CheckStateRole:
            return Qt.Checked if self._checkstate_list[row] else Qt.Unchecked
        if role == Qt.ToolTipRole:
            return v
        return None

    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole):
        if not index.isValid() or not role in (Qt.CheckStateRole, Qt.EditRole):
            return False
        row, column = index.row(), index.column()
        if role == Qt.EditRole:
            o_val = self._data[row][AttachDataModel.columnListIndexMap[column]]
            if value != o_val:
                self._data[row][AttachDataModel.columnListIndexMap[column]] = value
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
        if index.column() in (self.ColumnFtype, self.ColumnNote):
            return Qt.ItemIsEditable | QAbstractTableModel.flags(self, index)
        return QAbstractTableModel.flags(self, index)

    def get_checked_items(self):
        return [idata for idata, is_checked in zip(self._data, self._checkstate_list) if is_checked]


class AttachDataProxyModel(QSortFilterProxyModel):

    def __init__(self, model):
        super(AttachDataProxyModel, self).__init__()
        self.setSourceModel(model)

    def filterAcceptsRow(self, src_row, src_parent):
        index = self.sourceModel().index(src_row, AttachDataModel.ColumnName)
        check_state = self.sourceModel().data(index, Qt.CheckStateRole)
        return check_state == Qt.Checked


class AttachDataDelegateModel(QStyledItemDelegate):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__()
        self.default_font_size = QFontDatabase.systemFont(
            QFontDatabase.FixedFont).pointSize()

    def sizeHint(self, option, index):
        return QStyledItemDelegate.sizeHint(self, option, index)

    def paint(self, painter, option, index):
        if index.column() == AttachDataModel.ColumnFtype:
            ftyp = index.model().data(index, Qt.UserRole).strip()
            if ftyp == '':
                QStyledItemDelegate.paint(self, painter, option, index)
            else:
                if option.state & QStyle.State_Selected or option.state & QStyle.State_MouseOver:
                    QStyledItemDelegate.paint(self, painter, option, index)

                w = QWidget()
                layout = QHBoxLayout()
                layout.setContentsMargins(4, 4, 4, 4)
                layout.setSpacing(2)

                shadow = QGraphicsDropShadowEffect()
                shadow.setBlurRadius(10)
                shadow.setOffset(2)
                lbl = QLabel(ftyp)
                lbl.setGraphicsEffect(shadow)
                lbl.setSizePolicy(QSizePolicy.Preferred,
                                  QSizePolicy.Preferred)
                bkgd_color = FTYP_COLOR_MAP.get(ftyp, '#EEEEEC')
                lbl.setStyleSheet(f'''
                QLabel {{
                    font-size: {self.default_font_size}pt;
                    border: 1px solid #AEAEAE;
                    border-radius: 5px;
                    margin: 1px;
                    background-color: {bkgd_color};
                }}''')
                layout.addWidget(lbl)
                w.setLayout(layout)
                w.setStyleSheet(
                    """QWidget { background-color: transparent; }""")
                rect = option.rect.adjusted(2, 2, -2, -2)
                painter.drawPixmap(rect.x(), rect.y(), w.grab())
        else:
            QStyledItemDelegate.paint(self, painter, option, index)
