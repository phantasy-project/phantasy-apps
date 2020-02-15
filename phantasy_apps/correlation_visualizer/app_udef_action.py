#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox

from phantasy_ui import get_open_filename
from phantasy_ui import get_save_filename
from phantasy_ui.widgets import PythonHighlighter
from phantasy_ui.widgets import format_code
from phantasy_ui.widgets import str2func

from phantasy_apps.correlation_visualizer.ui.ui_udef_action import Ui_Dialog


class UserDefinedActionDialog(QDialog, Ui_Dialog):

    # function changed
    alter_action_changed = pyqtSignal(QVariant)

    # function name changed
    func_name_changed = pyqtSignal('QString')

    # file loaded
    file_loaded = pyqtSignal('QString')

    def __init__(self, parent=None):
        super(UserDefinedActionDialog, self).__init__()
        self.parent = parent

        # UI
        self.setupUi(self)
        self._title = "Set Alter Action by User-defined Function"
        self.setWindowTitle(self._title)

        self.hl = PythonHighlighter(self.plainTextEdit.document())
        self.func_name_changed.connect(self.func_name_lineEdit.setText)
        self.file_loaded.connect(self.on_file_loaded)

    @pyqtSlot('QString')
    def on_file_loaded(self, filepath):
        self.filepath_lineEdit.setText(filepath)
        self.save_btn.setEnabled(True)
        self.saveas_btn.setEnabled(True)

    @pyqtSlot()
    def on_text_changed(self):
        # try to extra function name
        s = self.plainTextEdit.toPlainText()
        r = re.search(r'def\s+(.*)\(.*', s, re.MULTILINE)
        try:
            func_name = r.group(1)
        except AttributeError:
            pass
        else:
            self.func_name_changed.emit(func_name)

    @pyqtSlot()
    def on_open_file(self):
        """Load script from a file.
        """
        filepath, ext = get_open_filename(self,
            type_filter="Python Files (*.py)")
        if filepath is None:
            return
        with open(filepath, 'r') as fp:
            text = fp.read()
            try:
                code_formatted = format_code(text)
            except RuntimeError:
                QMessageBox.critical(self, "Load User-defined Function",
                        "The code is not right formatted.",
                        QMessageBox.Ok)
                return
            else:
                self.plainTextEdit.setPlainText(code_formatted)
                self.file_loaded.emit(filepath)

    @pyqtSlot()
    def on_click_ok(self):
        text = self.plainTextEdit.toPlainText()
        func = str2func(text, func_name=self.func_name_lineEdit.text())
        if func is not None:
            self.close()
            self.setResult(QDialog.Accepted)
            self.alter_action_changed.emit(func)
        else:
            QMessageBox.warning(self, self._title,
                    "The code is not right formatted.",
                    QMessageBox.Ok)
            return

    @pyqtSlot()
    def on_click_cancel(self):
        self.close()
        self.setResult(QDialog.Rejected)

    def _save_data(self, filepath=None):
        try:
            code_formatted = format_code(self.plainTextEdit.toPlainText())
        except RuntimeError:
            QMessageBox.critical(self, "Checking User-defined Function",
                    "The code is not right formatted.",
                    QMessageBox.Ok)
            return
        else:
            self.plainTextEdit.setPlainText(code_formatted)

        if filepath is None:
            filepath = self.filepath_lineEdit.text()

        try:
            with open(filepath, 'w') as fp:
                fp.write(self.plainTextEdit.toPlainText())
        except:
            QMessageBox.warning(self, "Save Data to a File",
                    "Failed to save data to {}.".format(filepath),
                    QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Save Data to a File",
                    "Saved data to {}.".format(filepath),
                    QMessageBox.Ok)

    @pyqtSlot()
    def on_save(self):
        """Save current text to a file if loaded from a file.
        """
        self._save_data()

    @pyqtSlot()
    def on_save_as(self):
        """Save current text to a file.
        """
        filename, ext = get_save_filename(self,
                caption="Save Data to a file",
                type_filter="Python Files (*.py)")

        if filename is None:
            return
        self._save_data(filename)
        self.file_loaded.emit(filename)
