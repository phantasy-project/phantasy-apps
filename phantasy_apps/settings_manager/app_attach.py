#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, stat
import sqlite3
import shutil
from subprocess import Popen
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
        QDesktopServices,
        QGuiApplication
)
from PyQt5.QtCore import (
        pyqtSignal, pyqtSlot,
        QAbstractTableModel,
        QSortFilterProxyModel,
        QModelIndex, Qt, QPoint, QUrl,
        QMimeDatabase
)
from phantasy_ui import get_open_filename
from phantasy_apps.settings_manager.data import AttachmentData
from phantasy_apps.settings_manager.db_utils import (
        insert_attach_data, update_attach_data, delete_attach_data,
        insert_snp_attach, delete_snp_attach, get_attachments
)
from .ui.ui_attach import Ui_Dialog


FTYP_COLOR_MAP = {
    'TXT': '#EED405',
    'JSON': '#4B7F6C',
    'PY': '#306998',

    'LINK': '#F72D69',

    'PNG': '#F4B1AE',
    'BMP': '#F4B1AE',
    'JPEG': '#F4B1AE',
    'JPG': '#F4B1AE',
    'TIFF': '#F4B1AE',

    'PDF': '#AD0B00',

    'ODT': '#1D96E2',
    'DOC': '#1D96E2',
    'DOCX': '#1D96E2',

    'ODP': '#C65914',
    'PPT': '#C65914',
    'PPTX': '#C65914',

    'ODS': '#4EC84E',
    'CSV': '#4EC84E',
    'XLS': '#4EC84E',
    'XLSX': '#4EC84E',
}


class AttachDialog(QDialog, Ui_Dialog):

    sigDataModelShown = pyqtSignal()
    sigAttachmentUpdated = pyqtSignal()
    sigViewUpdated = pyqtSignal()

    def __init__(self, snp_name: str, snp_longname: str, conn: sqlite3.Connection,
                 data_dir: str, file_exec: dict, attach_after_upload: bool, parent):
        super(self.__class__, self).__init__()
        self.parent = parent
        self.conn = conn
        self.data_dir = data_dir
        self.file_exec = file_exec
        self.attach_after_upload = attach_after_upload
        self.snp_name = snp_name
        self.snp_longname = snp_longname

        self.setupUi(self)
        self.setWindowTitle("Attachments")

        self._post_init()

    def exec_query(self):
        # return a tuple of list[AttachmentData], list[int] (for nsnp)
        q_str = self.search_lineEdit.text()
        if q_str == '' or q_str == '*':
            q_cond = ''
        else:
            q_cond = f"WHERE name like '%{q_str}%' OR uri like '%{q_str}%' OR note like '%{q_str}%'"

        attach_list = []
        nsnp_list = []
        try:
            with self.conn:
                r = self.conn.execute(f"""
        SELECT attachment.id, attachment.name, attachment.uri, attachment.ftyp,
               attachment.created, attachment.note, COUNT(snp_attach.attachment_id)
        FROM attachment
        LEFT JOIN snp_attach
        ON snp_attach.attachment_id = attachment.id
        {q_cond}
        GROUP BY attachment.id""")
            for i in r.fetchall():
                attach_list.append(AttachmentData(*i[1:-1]))
                nsnp_list.append(i[-1])
        except Exception as err:
            print(err)
        finally:
            return attach_list, nsnp_list

    @pyqtSlot(bool)
    def on_toggle_attach_after_upload(self, is_checked: bool):
        self.attach_after_upload = is_checked
        if is_checked:
            tt = "Attach the new uploaded attachment to the snapshot."
        else:
            tt = "Do not attach the new uploaded attachment to the snapshot."
        self.attach_after_upload_chkbox.setToolTip(tt)

    def _post_init(self):
        # attach after upload?
        self.attach_after_upload_chkbox.setChecked(self.attach_after_upload)
        self.attach_after_upload_chkbox.toggled.connect(self.on_toggle_attach_after_upload)
        self.attach_after_upload_chkbox.toggled.emit(self.attach_after_upload)
        #
        self.default_font_size = QFontDatabase.systemFont(
            QFontDatabase.FixedFont).pointSize()
        #
        self.uri_name_lbl.setToolTip(
                f"""Set the relative path under '{self.data_dir}' as the destination filepath.\ne.g.:'f1/f2/file.txt' uploads the source file to '{self.data_dir}/f1/f2/file.txt'.""")
        self.uri_name_lineEdit.textChanged.connect(self.on_uri_name_textChanged)
        # set title line
        self.snp_name_lbl.setText(self.snp_longname)
        self.snp_name_lbl.setStyleSheet(f"""
        QLabel {{
            color: #1E88E5;
            font-family: monospace;
            font-size: {int(self.default_font_size * 1.2)}pt;
            font-weight: bold;
            border-top: 0px solid gray;
            border-bottom: 3px solid gray;}}""")
        # context menu
        self._attach_icon = QIcon(QPixmap(":/sm-icons/attach.png"))
        self._detach_icon = QIcon(QPixmap(":/sm-icons/detach.png"))
        self._delete_icon = QIcon(QPixmap(":/sm-icons/delete.png"))
        self._open_icon = QIcon(QPixmap(":/sm-icons/open.png"))
        self._copy_icon = QIcon(QPixmap(":/sm-icons/copy_text.png"))
        self._reveal_icon = QIcon(QPixmap(":/sm-icons/openfolder.png"))
        #
        self.attach_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.attach_view.customContextMenuRequested.connect(self.on_request_context_menu)
        #
        self.uri_type = 'FILE'
        self.uri_path = ''
        self.uri_name = ''
        self.ftype = ''  # file type, ext, or 'LINK' for uri_type of 'URL'
        # signals and slots
        self.dataModelShown = False
        #
        self.browse_btn.clicked.connect(self.on_click_browse)
        self.upload_btn.clicked.connect(self.on_click_upload)
        self.search_btn.clicked.connect(self.on_click_search)
        self.show_checked_btn.clicked.connect(self.on_filter_checked_items)
        self.show_all_btn.clicked.connect(self.on_show_all_items)
        self.uri_type_cbb.currentTextChanged.connect(self.on_uri_type_changed)
        self.sigDataModelShown.connect(self.on_dataModelShown)
        self.sigAttachmentUpdated.connect(self.on_attachmentUpdated)
        self.sigViewUpdated.connect(self.on_viewUpdated)
        self.sigViewUpdated.connect(self.on_post_nitem)
        # initial signals
        self.uri_type_cbb.currentTextChanged.emit('File')
        #
        self.attach_view.setItemDelegate(AttachDataDelegateModel(self.attach_view))
        # pull db
        self.search_btn.click()

    @pyqtSlot('QString')
    def on_uri_name_textChanged(self, s: str):
        """URI name is changed, update the tooltip, test dest path name collision.
        """
        style_template = """
            QLineEdit {{
                border: 2px solid {c};
                padding: 1 5px;
                border-radius: 2px;
                background-color: {b};
            }}
        """
        _style0 = style_template.format(c='gray', b='white')
        _style1 = style_template.format(c='red', b='#FFFDE7')
        destpath = os.path.join(self.data_dir, s)
        if os.path.exists(destpath):
            self.upload_btn.setDisabled(True)
            tt = "The destination path exists, rename it or delete the existing one."
            self.uri_name_lineEdit.setStyleSheet(_style1)
        else:
            self.upload_btn.setDisabled(False)
            tt = f"Click Upload button to upload source filepath to '{destpath}'."
            self.uri_name_lineEdit.setStyleSheet(_style0)
        self.uri_name_lineEdit.setToolTip(tt)


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
        self.attach_view.resizeColumnsToContents()
        #
        self.sigViewUpdated.emit()

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
        # copy filepath
        copy_uri_act = QAction(self._copy_icon, "Copy URI", menu)
        copy_uri_act.triggered.connect(partial(self.on_copy_uri, idx, m))
        # reveal
        reveal_act = QAction(self._reveal_icon, "Show in File Explorer", menu)
        reveal_act.triggered.connect(partial(self.on_reveal_uri, idx, m))
        # delete attachment
        delete_act = QAction(self._delete_icon, "Delete", menu)
        delete_act.triggered.connect(partial(self.on_delete, idx, m))
        #
        menu.addAction(title_act)
        if m.data(idx, Qt.CheckStateRole) == Qt.Checked:
            menu.addAction(detach_act)
        else:
            menu.addAction(attach_act)
        menu.addSeparator()
        menu.addAction(open_act)
        menu.addAction(reveal_act)
        menu.addAction(copy_uri_act)
        menu.addAction(delete_act)
        return menu

    @pyqtSlot()
    def on_reveal_uri(self, idx, m):
        """Reveal file in File Explorer.
        """
        # !! requires nautilus / caja !!
        uri = m.data(m.index(idx.row(), AttachDataModel.ColumnUri))
        try:
            Popen(["nautilus", "-s", uri])
        except Exception as err:
            try:
                Popen(["caja", "-s", uri])
            except:
                pass
            else:
                print(f"Revealed {uri} in caja.")
                return
            print(f"Failed revealing {uri}\n{err}")
        else:
            print(f"Revealed {uri} in nautilus.")

    @pyqtSlot()
    def on_copy_uri(self, idx, m):
        """Copy the URI.
        """
        uri = m.data(m.index(idx.row(), AttachDataModel.ColumnUri))
        QGuiApplication.clipboard().setText(uri)

    @pyqtSlot()
    def on_open(self, idx, m):
        """Open attachment.
        """
        row = idx.row()
        ftype = m.data(m.index(row, AttachDataModel.ColumnFtype), Qt.UserRole)
        uri = m.data(m.index(row, AttachDataModel.ColumnUri))
        _exec = self.file_exec.get(ftype, None)
        if _exec is not None:
            Popen(f"{_exec} {uri}", shell=True)
        else:
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
        m._checkstate_list[idx.row()] = True
        m._nsnp[idx.row()] += 1
        new_attached = insert_snp_attach(self.conn, self.snp_name, name)
        if new_attached:
            QMessageBox.information(self, "Attach an Attachment",
                    f"Attached attachment '{name}' to snasphot '{self.snp_name}'.",
                    QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "Attach an Attachment",
                    f"Attachment '{name} has already been attached to snapshot '{self.snp_name}'.",
                    QMessageBox.Ok, QMessageBox.Ok)
        self.sigViewUpdated.emit()

    @pyqtSlot()
    def on_detach(self, idx, m):
        name = m.data(idx)
        m._checkstate_list[idx.row()] = False
        m._nsnp[idx.row()] -= 1
        new_detached = delete_snp_attach(self.conn, self.snp_name, name)
        if new_detached:
            QMessageBox.information(self, "Detach an Attachment",
                    f"Detached '{name}' from '{self.snp_name}'",
                    QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "Detach an Attachment",
                    f"Attachment '{name} has already been detached from '{self.snp_name}'",
                    QMessageBox.Ok, QMessageBox.Ok)
        self.sigViewUpdated.emit()

    @pyqtSlot()
    def on_delete(self, idx, m):
        """Delete the attachment.
        """
        nsnp = m.data(m.index(idx.row(), AttachDataModel.ColumnNSnp), Qt.UserRole)
        uri = m.data(m.index(idx.row(), AttachDataModel.ColumnUri))
        if nsnp > 0:
            r = QMessageBox.warning(self, "Delete an Attachment",
                    f"Are you sure to delete this attachment? It will be detached from all ({nsnp}) the attached snapshots.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if r == QMessageBox.No:
                return
        deleted = delete_attach_data(self.conn, m.data(idx))
        if deleted:
            # delete attachment
            try:
                os.remove(uri)
            except FileNotFoundError:
                print(f"{uri} not found.")
            else:
                print(f"Deleted {uri}.")
        self.sigAttachmentUpdated.emit()

    @pyqtSlot()
    def on_click_search(self):
        """Search database and present the results.
        """
        # current attachments
        self.current_attach_list = get_attachments(self.conn, self.snp_name)
        self.current_attach_namelist = [i.name for i in self.current_attach_list]
        #
        attach_list, nsnp_list = self.exec_query()
        self.m = AttachDataModel(attach_list, nsnp_list, self.current_attach_namelist, self.data_dir)
        self.m.dataChanged.connect(self.on_attachment_dataChanged)
        self.m.dataChanged.connect(self.on_post_nitem)
        self.attach_view.setModel(self.m)
        self.attach_view.resizeColumnsToContents()
        if not self.dataModelShown:
            self.sigDataModelShown.emit()
        #
        self.sigViewUpdated.emit()

    def on_viewUpdated(self):
        self.attach_view.horizontalHeader().setSectionResizeMode(
                AttachDataModel.ColumnNote, QHeaderView.Stretch)

    def on_post_nitem(self):
        self.nitem_lbl.setText(f"{self.attach_view.model().rowCount()}")

    def on_attachment_dataChanged(self, tl: QModelIndex, br: QModelIndex, roles: list):
        if Qt.CheckStateRole in roles:
            return
        m = self.attach_view.model()
        if isinstance(m, AttachDataProxyModel):
            m = m.sourceModel()
        row, column = tl.row(), tl.column()
        new_data = m.data(tl, Qt.EditRole)
        col_name = AttachDataModel.editColumnNameMap[column]
        if column == AttachDataModel.ColumnName:
            name = m._name_map[new_data]
        else:
            name = m.data(m.index(row, AttachDataModel.ColumnName))
        print(f"Editted {col_name} for {name} -> {new_data} @ ({row}, {column})")
        updated = update_attach_data(self.conn, name, new_data, col_name)
        if not updated:
            QMessageBox.critical(self, "Update an Attachment",
                    f"Failed to update the attachment with '{new_data}'.",
                    QMessageBox.Ok, QMessageBox.Ok)
        self.sigAttachmentUpdated.emit()

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
                os.chmod(_dst_filepath, stat.S_IWUSR | stat.S_IRUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH)
            except Exception as err:
                QMessageBox.critical(self, "Upload an Attachment", f"Failed uploading '{attach_data.name}'.\n{err}",
                        QMessageBox.Ok, QMessageBox.Ok)
                return
            attach_data = AttachmentData(_dst_filename, _dst_filename, self.ftype, None, '')
        inserted = insert_attach_data(self.conn, attach_data)
        if not inserted:
            QMessageBox.critical(self, "Upload an Attachment",
                    f"Failed to add the data to the database, try to change the 'Destination Filepath' input.", QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Upload an Attachment",
                    f"Uploaded attachment '{attach_data.name}'.", QMessageBox.Ok, QMessageBox.Ok)
            # attach the new attachment?
            if self.attach_after_upload:
                insert_snp_attach(self.conn, self.snp_name, attach_data.name)
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


PX_SIZE = 32
DECO_PX_DICT = {}
def get_px_note():
    return DECO_PX_DICT.setdefault('note',
            QPixmap(":/sm-icons/comment.png").scaled(
                PX_SIZE, PX_SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation))


def get_px(filepath: str, is_link: bool):
    iname = QMimeDatabase().mimeTypeForUrl(QUrl(filepath)).genericIconName()
    if QIcon.hasThemeIcon(iname):
        return DECO_PX_DICT.setdefault(iname, QIcon.fromTheme(iname).pixmap(PX_SIZE, PX_SIZE))
    else:
        if is_link:
            return DECO_PX_DICT.setdefault('link', QPixmap(":/sm-icons/hyperlink.png").scaled(
                PX_SIZE, PX_SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            return DECO_PX_DICT.setdefault('file', QPixmap(":/sm-icons/file.png").scaled(
                PX_SIZE, PX_SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation))


class AttachDataModel(QAbstractTableModel):

    ColumnName, ColumnNSnp, ColumnUri, ColumnFtype, ColumnNote, ColumnCreated, \
        ColumnCount = range(7)

    # map column int to header name
    columnNameMap = {
        ColumnName: "Name",
        ColumnNSnp: "#", # total number of snapshots that attached to this attachment
        ColumnUri: "URI",
        ColumnFtype: "Type",
        ColumnNote: "Note",
        ColumnCreated: "Uploaded", # "Created"
    }

    # map column int to table column name
    editColumnNameMap = {
        ColumnName: 'name',
        ColumnFtype: 'ftyp',
        ColumnNote: 'note'
    }

    # map column int to list index in AttachmentData
    columnListIndexMap = {
        ColumnName: 0,
        ColumnUri: 1,
        ColumnFtype: 2,
        ColumnCreated: 3,
        ColumnNote: 4,
    }

    def __init__(self, data: list[AttachmentData], nsnp: list[int], attached_namelist: list[str],
                 data_dir: str, parent=None):
        super(self.__class__, self).__init__(parent)
        # root directory for all the datafiles
        self._data_dir = data_dir
        # data: a list of AttachmentData
        # nsnp: a list of number of snapshots attached to the attachment
        self._data, self._nsnp = data, nsnp
        # prefix data_dir to URI
        for i in self._data:
            if i.ftyp == 'LINK':
                continue
            i.uri = os.path.join(data_dir, i.uri)
        # initial checkstate
        self._checkstate_list = [i.name in attached_namelist for i in self._data]
        # new name -> old name
        self._name_map = {}

    def columnCount(self, parent=None):
        return self.ColumnCount

    def rowCount(self, parent: QModelIndex = QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._data)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None
        row, column = index.row(), index.column()
        if column == self.ColumnNSnp:
            v = self._nsnp[row]
        else:
            v = self._data[row][self.columnListIndexMap[column]]
        if role == Qt.DisplayRole:
            if column == self.ColumnFtype:
                return ' ' * (len(v) + 2)
            elif column == self.ColumnNSnp:
                return ' ' * (len(str(v)) + 2)
            else:
                return v
        if role == Qt.UserRole:
            if column in (self.ColumnFtype, self.ColumnNSnp):
                return v
        if role == Qt.DecorationRole:
            if column == self.ColumnUri:
                is_link = self._data[row][
                        self.columnListIndexMap[self.ColumnFtype]] == 'LINK'
                return get_px(v, is_link)
            elif column == self.ColumnNote:
                return get_px_note()
        if role == Qt.EditRole:
            return v
        if column == self.ColumnName and role == Qt.CheckStateRole:
            return Qt.Checked if self._checkstate_list[row] else Qt.Unchecked
        if role == Qt.ToolTipRole:
            if column == self.ColumnNSnp:
                return f"# of Snapshots attached: {v}."
            else:
                return v
        return None

    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole):
        if not index.isValid() or not role in (Qt.CheckStateRole, Qt.EditRole):
            return False
        row, column = index.row(), index.column()
        if role == Qt.EditRole:
            if column == self.ColumnFtype:
                value = value.upper()
            o_val = self._data[row][self.columnListIndexMap[column]]
            if value != o_val:
                self._data[row][self.columnListIndexMap[column]] = value
                self._name_map[value] = o_val
                self.dataChanged.emit(index, index, (Qt.DisplayRole, Qt.EditRole))
                return True
        if role == Qt.CheckStateRole and column == 0:
            self._checkstate_list[row] = value == Qt.Checked
            self.dataChanged.emit(index, index, [Qt.CheckStateRole])
            return True
        return False

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.columnNameMap.get(section)
            else:
                return None
        return None

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return Qt.NoItemFlags
        if index.column() in (self.ColumnName, self.ColumnFtype, self.ColumnNote):
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
                    font-size: {self.default_font_size - 1}pt;
                    font-family: monospace;
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
        elif index.column() == AttachDataModel.ColumnNSnp:
            nsnp = str(index.model().data(index, Qt.UserRole))
            if nsnp == '':
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
                lbl = QLabel(nsnp)
                lbl.setGraphicsEffect(shadow)
                lbl.setSizePolicy(QSizePolicy.Preferred,
                                  QSizePolicy.Preferred)
                if nsnp == '0':
                    bkgd_color = '#F8BBD0'
                else:
                    bkgd_color = '#BBDEFB'
                lbl.setStyleSheet(f'''
                QLabel {{
                    font-size: {self.default_font_size - 1}pt;
                    font-family: monospace;
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
