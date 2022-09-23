#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Finalize a new snapshot.
"""

from functools import partial

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget

from phantasy_ui.widgets import FlowLayout

from .utils import TAG_BTN_STY
from .ui.ui_post_snp import Ui_Dialog


DEFAULT_TAG_LIST = ["LINAC", "FSEE", "GOLDEN"]


class PostSnapshotDialog(QDialog, Ui_Dialog):

    def __init__(self, tag_fontsize: int, parent=None):
        super(self.__class__, self).__init__()
        self.parent = parent
        sef._tag_fs = tag_fontsize

        # UI
        self.setupUi(self)
        self.setWindowTitle("Finalize Snapshot")

        #
        self._post_init()

    def _post_init(self):
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
            o = QPushButton(tag, self)
            o.setStyleSheet(TAG_BTN_STY.format(fs=self._tag_fs))
            o.setCheckable(True)
            o.toggled.connect(partial(self.on_update_tags, tag))
            layout.addWidget(o)
        w.setLayout(layout)
        area.setWidget(w)

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
            QMessageBox.warning(self, "Finalize Snapshot",
                    "Tag and Note must be set for a new snapshot.",
                    QMessageBox.Ok, QMessageBox.Ok)
            return
        self.close()
        self.setResult(QDialog.Accepted)

    def get_selected_tag_list(self):
        return self._selected_tag_list

    def get_note(self):
        return self.note_textEdit.toPlainText().strip()


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