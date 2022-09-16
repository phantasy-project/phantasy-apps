#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Finalize a new snapshot.
"""

from functools import partial

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QWidgetAction

# from .ui.ui_postsnp import Ui_Dialog
from phantasy_apps.settings_manager.ui.ui_post_snp import Ui_Dialog


DEFAULT_TAG_LIST = ["LINAC", "FSEE", "GOLDEN"]


class PostSnapshotDialog(QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__()
        self.parent = parent

        # UI
        self.setupUi(self)
        self.setWindowTitle("Finalize Snapshot")

        #
        self._post_init()

    def _post_init(self):
        # build multi-select tag list
        tag_list = get_tag_list()
        self.selected_tag_list = None
        self._build_tags_list(self.tags_hbox, tag_list)

    def _build_tags_list(self, container, tags):
        # dropdown menu with checkable tag names
        # tags: a list of predefined tags.
        #
        child = container.takeAt(0)
        while child:
            w = child.widget()
            if w is not None:
                w.setParent(None)
            del w
            del child
            child = container.takeAt(0)
        #
        _d = {i: False for i in tags}
        #
        def _on_update_tag_selection(k, btn, is_toggled):
            if k == 'All':  # update checkstates for other actions
                for obj in self.sender().parent().findChildren(QCheckBox):
                    obj.setChecked(is_toggled)
            else:
                _d[k] = is_toggled
                obj = self.sender().parent().findChild(QCheckBox, "sel_tag_act")
                obj.toggled.disconnect()
                obj.setChecked(all(_d.values()))
                obj.toggled.connect(
                    partial(_on_update_tag_selection, 'All', btn))

            #
            self.selected_tag_list = [k for k, v in _d.items() if v]
            btn.setToolTip("Selected tags: {}".format(
                ','.join(self.selected_tag_list)))
            self.selected_tags.setText(','.join(self.selected_tag_list))

        def _create_widgetaction(text, parent):
            _chkbox = QCheckBox(text, parent)
            _chkbox.setChecked(False)
            _wa = QWidgetAction(parent)
            _wa.setDefaultWidget(_chkbox)
            _chkbox.setStyleSheet("""QCheckBox{padding-left:10px;}""")
            return _chkbox, _wa

        def _build_actions(btn):
            menu = QMenu(self)
            for i in tags:
                _chkbox, _wa = _create_widgetaction(i, menu)
                _chkbox.toggled.connect(
                    partial(_on_update_tag_selection, i, btn))
                menu.addAction(_wa)
            menu.addSeparator()
            _chkbox_all, _wa_all = _create_widgetaction('All', menu)
            _chkbox_all.setObjectName("sel_tag_act")
            _chkbox_all.toggled.connect(
                partial(_on_update_tag_selection, 'All', btn))
            menu.addAction(_wa_all)
            btn.setMenu(menu)

        #
        _btn = QToolButton(self)
        _btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        _btn.setText("Select Tags")
        _btn.setToolTip("Select tags for the snapshot")
        _btn.setPopupMode(QToolButton.MenuButtonPopup)
        #
        container.addWidget(_btn)
        _build_actions(_btn)

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
        return self.selected_tag_list

    def get_note(self):
        return self.note_textEdit.toPlainText()


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
