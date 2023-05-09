#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Creating a new snapshot.
"""

import time
from functools import partial
from datetime import timedelta

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QButtonGroup

from phantasy_ui import milli_sleep
from phantasy_ui.widgets import FlowLayout
from phantasy_ui.widgets import DataAcquisitionThread as DAQT

from .utils import TAG_BTN_STY
from .utils import take_snapshot
from .data import SnapshotData
from .ui.ui_post_snp import Ui_Dialog


DEFAULT_TAG_LIST = ["LINAC", "FSEE", "GOLDEN", "SCS1", "SCS2", "TEST"]

ISRC_NAME_MAP = {
    'ISRC1': 'Artemis',
    'ISRC2': 'HP-ECR'
}


class PostSnapshotDialog(QDialog, Ui_Dialog):
    """ The dialog to show after clicking 'Take Snapshot'.
    """

    def __init__(self, tag_fontsize: int, template_list: list, current_snpdata_originated: tuple, parent=None):
        super(self.__class__, self).__init__()
        self.parent = parent
        self._tag_fs = tag_fontsize
        # template list: [(name, tag_list, snpdata),...]
        self._template_list = template_list
        # current loaded snp originated template, (name, tag_list, snpdata)
        self._loaded_snp_name, self._loaded_snp_tag_list, \
                self._loaded_snp_data = current_snpdata_originated

        # UI
        self.setupUi(self)
        self.setWindowTitle("Settings Manager: Take Snapshot")

        #
        self._post_init()

    def _post_init(self):
        # hide pb
        self.pb.setVisible(False)
        self.pb_lbl.setVisible(False)
        # advanced ctrls.
        self.show_adv_ctls_btn.setChecked(False)
        #
        self.isrc_name_meta_cbb.setCurrentText('Live')
        #
        self._matched_px = QPixmap(":/sm-icons/done.png").scaled(64, 64, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self._not_matched_px = QPixmap(":/sm-icons/fail.png").scaled(64, 64, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # template area
        self._build_template_area()
        # build multi-select tag list
        tag_list = get_tag_list()
        self._selected_tag_list = []
        self._tag_btn_sts = {} # tag button dict: {tag-name: tag-btn-obj,...}
        self._build_tags_list(self.tags_area, tag_list)

        # check if current loaded snapshot matches beam operation
        milli_sleep(500)
        self.check_loaded_snp()

    @pyqtSlot('QString')
    def onIsrcNameMetaChanged(self, s: str):
        """The name of ISRC name for meta info is changed.
        Live, Artemis, HP-ECR.
        """
        self._isrc_name_meta = s

    def __set_isrc_name_meta_cbb(self, temp_name: str):
        # set the option from the given snapshot template name.
        if 'Artemis' in temp_name:
            self.isrc_name_meta_cbb.setCurrentText('Artemis')
        elif 'HP-ECR' in temp_name:
            self.isrc_name_meta_cbb.setCurrentText('HP-ECR')

    @pyqtSlot(bool)
    def onCheckOnLoaded(self, is_checked: bool):
        """Take snapshot on loaded one if enabled.
        """
        self.reset_tag_buttons()
        if is_checked:
            self._snp_temp_data = self._loaded_snp_data
            self._snp_temp_name = self._loaded_snp_name
            self.__set_isrc_name_meta_cbb(self._snp_temp_name)
        #
        self._snp_temp_tags = self._loaded_snp_tag_list
        for tag in self._loaded_snp_tag_list:
            self._tag_btn_sts[tag].setChecked(is_checked)

    @pyqtSlot(bool)
    def onCheckOnTemplate(self, is_checked: bool):
        """Take snapshot on a template if enabled.
        """
        self.reset_tag_buttons()
        if is_checked:
            print("Take a snapshot based on a template.")
        for w in self.template_area.findChildren(QToolButton):
            if w.isChecked():
                w.toggled.emit(True)
                break

    def reset_tag_buttons(self):
        """Uncheck all tag buttons.
        """
        [o.setChecked(False) for o in self._tag_btn_sts.values()]

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
            self._tag_btn_sts[tag] = o
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
            self._snp_temp_name = name
            self._snp_temp_data = data
            self._snp_temp_tags = tags
            self.__set_isrc_name_meta_cbb(name)
        for tag in tags:
            self._tag_btn_sts[tag].setChecked(is_checked)

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
        self.__take_snapshot()
        # self.close()
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

    def get_isrc_name_meta(self):
        # isrc name for capture metainfo of ion,A,Q,Z
        return self._isrc_name_meta

    def check_loaded_snp(self):
        """Check the originated template of the current loaded snapshot,
        to see if it matches beam operations. Auto-checked the template
        button if any matches current beam ops.
        """
        # get template snapshot name with beam ops
        isrc_name, bound_name, beam_dest = self.beamSpeciesDisplayWidget.get_bound_info()
        temp_name_in_op = f"{bound_name}_{ISRC_NAME_MAP[isrc_name]}"
        self._isrc_name_meta = isrc_name # isrc name for meta info capture.

        # check if loaded snapshot matches beam ops
        if self._loaded_snp_name == temp_name_in_op:
            self.is_match_lbl.setToolTip("The loaded snapshot MATCHES beam operations.")
            self.is_match_lbl.setPixmap(self._matched_px)
        else:
            self.is_match_lbl.setToolTip("The loaded snapshot does NOT MATCH beam operations!")
            self.is_match_lbl.setPixmap(self._not_matched_px)
            # check based on template option (default is baed on currently loaded)
            self.on_template_rbtn.setChecked(True)

        # check the temp button matches beam ops
        self.orig_template_lbl.setText(self._loaded_snp_name)
        for w in self.template_area.findChildren(QToolButton):
            if w.text() == temp_name_in_op:
                w.setChecked(True)
                break

    def get_snp_temp_data(self):
        """Return the snapshot data template for capturing a new snapshot.
        """
        return self._snp_temp_data

    def __take_snapshot(self):
        # meta snp
        note = self.get_note()
        tag_list = self.get_selected_tag_list()
        snp_temp_data = self.get_snp_temp_data()
        isrc_name_meta = self.get_isrc_name_meta()

        # mach state?
        with_machstate = self.snp_ms_chkbox.isChecked()

        #
        _t0 = time.time()
        def _on_update_time():
            t_elapsed = f"{str(timedelta(seconds=int(time.time() - _t0)))}"
            self.pb_lbl.setText(t_elapsed)

        ticker = QTimer(self)
        ticker.timeout.connect(_on_update_time)

        def _take(snp_data: SnapshotData):
            new_snp_data = take_snapshot(note, tag_list, snp_data, isrc_name_meta,
                                         mp=self.parent._mp, version=self.parent._version,
                                         with_machstate=with_machstate,
                                         machstate_conf=self.parent.get_ms_config())
            return new_snp_data

        def _take_started():
            self.pb.setVisible(True)
            self.pb_lbl.setVisible(True)
            _t0 = time.time()
            ticker.start(1000)
            print("Taking snapshot is started...")

        def _take_done():
            self.pb.setVisible(False)
            self.pb_lbl.setVisible(False)
            self.pb_lbl.setText("0:00:00")
            ticker.stop()
            print("Taking snapshot is done.")

        def _snp_ready(r: list):
            print(f"Took snapshot: {r[0].ts_as_str()}" )

        _t = DAQT(daq_func=_take, daq_seq=[snp_temp_data])
        _t.daqStarted.connect(_take_started)
        _t.resultsReady.connect(_snp_ready)
        _t.daqFinished.connect(_take_done)
        _t.start()


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
