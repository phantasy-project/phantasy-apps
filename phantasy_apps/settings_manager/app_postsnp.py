#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Creating a new snapshot.
"""

from functools import partial

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QButtonGroup

from phantasy_ui.widgets import FlowLayout

from .utils import TAG_BTN_STY
from .data import SnapshotData
from .ui.ui_post_snp import Ui_Dialog


DEFAULT_TAG_LIST = ["LINAC", "FSEE", "GOLDEN", "SCS1", "SCS2", "TEST"]


class PostSnapshotDialog(QDialog, Ui_Dialog):
    """ The dialog to show after clicking 'Take Snapshot'.
    """

    # originated template info of the loaded snapshot
    # tuple of temp name, temp tag list, temp SnapshotData
    origTemplateSnapshot = pyqtSignal(tuple)

    def __init__(self, tag_fontsize: int, template_list: list, parent=None):
        super(self.__class__, self).__init__()
        self.parent = parent
        self._tag_fs = tag_fontsize
        # template list: [(name, tag_list, snpdata),...]
        self._template_list = template_list

        # UI
        self.setupUi(self)
        self.setWindowTitle("Settings Manager: Take Snapshot")

        #
        self._post_init()

    def _post_init(self):
        #
        self.origTemplateSnapshot.connect(self.onOrigTemplateChanged)
        # template area
        self._build_template_area()
        # build multi-select tag list
        tag_list = get_tag_list()
        self._selected_tag_list = []
        self._build_tags_list(self.tags_area, tag_list)

    def _build_tags_list(self, area, tags):
        # build a flow list of checkable toolbuttons for tag selection.
        w = area.takeWidget()
        w.setParent(None)
        w = QWidget(self)
        w.setContentsMargins(2, 4, 0, 0)
        layout = FlowLayout()
        _tags = sorted(list(tags))
        for tag in _tags:
            o = QToolButton(self)
            o.setText(tag)
            o.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            o.setStyleSheet(TAG_BTN_STY.format(fs=self._tag_fs))
            o.setCheckable(True)
            o.toggled.connect(partial(self.on_update_tags, tag))
            layout.addWidget(o)
        w.setLayout(layout)
        area.setWidget(w)

    def _build_template_area(self):
        # build buttons for templates, checked the one matches current
        # beam operation.
        area = self.template_area
        w = area.takeWidget()
        w.setParent(None)
        w = QWidget(self)
        w.setContentsMargins(2, 4, 0, 0)
        layout = FlowLayout()
        btn_grp = QButtonGroup(self)
        for _name, _tag_list, _snpdata in self._template_list:
            o = QToolButton(self)
            o.setText(_name)
            o.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            # o.setStyleSheet(TAG_BTN_STY.format(fs=self._tag_fs))
            o.setCheckable(True)
            o.toggled.connect(partial(self.on_checked_template,
                              _name, _tag_list, _snpdata))
            layout.addWidget(o)
            btn_grp.addButton(o)
        w.setLayout(layout)
        area.setWidget(w)

    def on_checked_template(self, name: str, tags: list, data: SnapshotData,
                            is_checked: bool):
        """Update checked template snapshot info.
        """
        if is_checked:
            print(name, tags)


    def on_update_tags(self, tag: str, is_checked: bool):
        """Update tag string.
        """
        if is_checked:
            self._selected_tag_list.append(tag)
        else:
            self._selected_tag_list.remove(tag)
        self._selected_tag_str = ','.join(sorted(self._selected_tag_list))
        self.selected_tags.setText(self._selected_tag_str)

    @pyqtSlot()
    def on_click_ok(self):
        if not self.get_note() or not self.get_selected_tag_list():
            QMessageBox.warning(self, "Create a Snapshot",
                    "Tag and Note must be set for the new snapshot.",
                    QMessageBox.Ok, QMessageBox.Ok)
            return
        self.close()
        self.setResult(QDialog.Accepted)

    @pyqtSlot()
    def on_click_cancel(self):
        self.close()
        self.setResult(QDialog.Rejected)

    def get_selected_tag_list(self):
        return self._selected_tag_list

    def get_selected_tag_str(self):
        return self._selected_tag_str

    def get_note(self):
        return self.note_textEdit.toPlainText().strip()

    @pyqtSlot(tuple)
    def onOrigTemplateChanged(self, t: tuple):
        """The originated template info of the currently loaded snapshot
        is changed.
        """
        _temp_name, _temp_tag_list, _temp_snpdata = t
        self.orig_template_lbl.setText(_temp_name)
        for w in self.template_area.findChildren(QToolButton):
            if w.text() == _temp_name:
                w.setChecked(True)
                break
        print("Originated tag list: ", _temp_tag_list)


def get_tag_list():
    """Return a list of tags.
    """
    return DEFAULT_TAG_LIST


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    w = PostSnapshotDialog()
    r = w.exec_()
    if r == QDialog.Accepted:
        print(w.selected_tag_list)

    sys.exit(app.exec_())
