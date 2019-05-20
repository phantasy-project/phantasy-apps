#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time

import numpy as np
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from phantasy import epoch2human
from phantasy.recipes import save_all_settings

from phantasy_apps.utils import get_save_filename
from .ui.ui_save import Ui_Dialog

TS_FMT = "%Y-%m-%d %H:%M:%S"


class SaveDataDialog(QDialog, Ui_Dialog):

    def __init__(self, parent):
        super(SaveDataDialog, self).__init__()
        self.parent = parent

        # UI
        self.setupUi(self)
        self.setWindowTitle("Save Data To File(s)")

        #
        self._post_init()

    def _post_init(self):
        # check figure and settings options
        self.save_figure_chkbox.setChecked(True)
        self.save_settings_chkbox.setChecked(True)

        # list and check all loaded all segs
        mp = self.parent.get_mp()
        if mp is not None:
            self.on_segments_updated(mp.lattice_names)

        # figure format
        self.figure_format_cbb.currentTextChanged.connect(
                self.on_update_figure_filepath)

    @pyqtSlot(list)
    def on_segments_updated(self, segs):
        # list of segs updated
        cnt = self.segs_hbox.count()
        if cnt > 1:
            self._clear_segs()
        seg_chkbox_list = []
        for seg in segs:
            seg_chkbox = QCheckBox(seg, self)
            self.segs_hbox.addWidget(seg_chkbox)
            seg_chkbox_list.append(seg_chkbox)
        self._selected_segs = []
        for o in seg_chkbox_list:
            o.toggled.connect(self.on_update_segs)
            o.setChecked(True)

    def _clear_segs(self):
        item = self.segs_hbox.takeAt(1)
        while item:
            w = item.widget()
            if w: w.deleteLater()
            item = self.segs_hbox.takeAt(1)

    @pyqtSlot('QString')
    def on_update_figure_filepath(self, fmt):
        filepath_name = self.figure_filepath_lineEdit.text().rsplit('.', 1)[0]
        filepath = '{}.{}'.format(filepath_name, fmt)
        self.figure_filepath_lineEdit.setText(filepath)

    @pyqtSlot(bool)
    def on_update_segs(self, checked):
        s = self.sender().text()
        if checked:
            self._selected_segs.append(s)
        else:
            self._selected_segs.remove(s)

    @pyqtSlot()
    def on_save_data(self):
        print("SaveDataDialog: Save Data")
        ctime = epoch2human(time.time(), fmt=TS_FMT)
        self._save_data(captured=ctime)

        if self.save_figure_chkbox.isChecked():
                self._save_figure()

        if self.save_settings_chkbox.isChecked():
            self._save_settings(captured=ctime)

    def _save_data(self, **kws):
        # save data.
        try:
            filepath = self.filepath_lineEdit.text()
            data = self.parent.data
            header = ','.join(i.name for i in self.parent._elems_list)
            comments = "# "
            for k, v in kws.items():
                comments += "{}: {}".format(k.capitalize(), v)
            comments += "\n"
            np.savetxt(filepath, data, delimiter=",", header=header, comments=comments)
        except:
            QMessageBox.warning(self, "Save Data Warning",
                    "Failed to save data to {}.".format(filepath), QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Save Data",
                    "Saved data to {}.".format(filepath), QMessageBox.Ok)

    def _save_figure(self):
        # save figure
        try:
            o = self.parent.matplotlibbarWidget
            filepath = self.figure_filepath_lineEdit.text()
            opt = {}
            opt.update({'dpi': o.getFigureDpi()})
            o.figure.savefig(filepath, **opt)
        except:
            QMessageBox.warning(self, "Save Figure Warning",
                    "Failed to save figure to {}.".format(filepath), QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Save Figure",
                    "Saved figure to {}.".format(filepath), QMessageBox.Ok)

    def _save_settings(self, **kws):
        # save settings
        try:
            filepath = self.settings_filepath_lineEdit.text()
            save_all_settings(filepath, segments=self._selected_segs,
                              mp=self.parent.get_mp())
        except:
            QMessageBox.warning(self, "Save Settings Warning",
                    "Failed to save settings to {}.".format(filepath), QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Save Settings",
                    "Saved settings to {}.".format(filepath), QMessageBox.Ok)

    @pyqtSlot()
    def on_get_filepath(self):
        print("SaveDataDialog: Get filepath")
        cdir = os.path.dirname(self.filepath_lineEdit.text())
        filepath, ext = get_save_filename(self,
                cdir=cdir,
                filter="CSV Files (*.csv)")
        if filepath is None:
            return
        self.filepath_lineEdit.setText(filepath)
        self.on_update_filepaths()

    @pyqtSlot()
    def on_update_filepaths(self):
        # update all filepaths.
        try:
            fname, ext = self.filepath_lineEdit.text().rsplit('.', 1)
        except ValueError:
            return

        # fig
        fig_fmt = self.figure_format_cbb.currentText()
        figure_filepath = '{}-figure.{}'.format(fname, fig_fmt)
        self.figure_filepath_lineEdit.setText(figure_filepath)

        # settings
        settings_filepath = fname + '-settings' + '.json'
        self.settings_filepath_lineEdit.setText(settings_filepath)
