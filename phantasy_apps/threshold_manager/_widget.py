#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sqlite3
import os
import pandas as pd
from datetime import datetime
from getpass import getuser
from functools import partial
from typing import Literal

from PyQt5.QtWidgets import (
    QWidget,
    QMessageBox,
    QLayout,
    QScrollArea,
    QToolButton,
)

from PyQt5.QtCore import (
    pyqtSignal,
    pyqtSlot,
    QTimer,
    Qt,
    QDate,
    QDateTime,
    QModelIndex,
)

from PyQt5.QtGui import (
    QFont,
    QFontDatabase,
    QPixmap,
    QFontMetrics,
)

from phantasy_ui import (
    delayed_exec,
    get_open_filename,
)
from phantasy_ui.widgets import BeamSpeciesDisplayWidget
from phantasy_ui.widgets import DataAcquisitionThread as DAQT

from phantasy_apps.threshold_manager.ui.ui_mps_diag import Ui_Form as MPSDiagWidgetForm
from phantasy_apps.threshold_manager._model import (
    MPSBeamLossDataModel,
    MPSBeamLossDataDelegateModel,
)
from phantasy_apps.threshold_manager.db.utils import (
    ensure_connect_db,
    insert_update_data
)
from phantasy_apps.threshold_manager.data import SnapshotData

DEVICE_TYPE_FULLNAME_MAP = {
    'ND': 'Neutron Detector',
    'IC': 'Ionization Chamber',
    'HMR': 'Halo Monitor Ring',
}

ISRC_INDEX_MAP = {
    'Live': 'live',
    'Artemis': 'ISRC1',
    'HP-ECR': 'ISRC2',
}


class MPSDiagWidget(QWidget, MPSDiagWidgetForm):

    def __init__(self, device_type: str, outdata_dir: str, parent=None):
        super(self.__class__, self).__init__()
        self.parent = parent

        self.setupUi(self)
        self.device_type = device_type
        self.outdata_dir = outdata_dir
        self.setWindowTitle(
            f"MPS Configurtions: Beam Loss Threshold ({self.device_type})")

        self._post_init()

    def set_snp_parent(self, w):
        # w: SnapshotWidget
        self.snp_parent = w

    def set_db_con(self, con):
        self.__db_con = con

    def _post_init(self):
        self._auto_width_init_flag = False
        self.diff_help_btn.setVisible(False)
        self._dt_ms = int(1000.0 / self.refresh_rate_dsbox.value())
        self.dtype_lbl.setText(
            '<html><head/><body><p><span style=" font-size:18pt; font-weight:600; color:#0055ff;">{dtype}</span></p></body></html>'
            .format(dtype=DEVICE_TYPE_FULLNAME_MAP[self.device_type]))
        self.view.setItemDelegate(MPSBeamLossDataDelegateModel(self.view))
        self.set_data()
        self.hide_columns()
        # delayed_exec(lambda: self.refresh_btn.setChecked(True), 2000)

    def hide_columns(self):
        """Hide columns.
        """
        for i in self.__model.get_hidden_columns():
            self.view.setColumnHidden(i, True)

    def set_data(self):
        self.__model = MPSBeamLossDataModel(self.device_type)
        self.view.setModel(self.__model)
        self.__model.dataRefreshStarted.connect(self.onDataRefreshStarted)
        self.__model.dataRefreshStopped.connect(self.onDataRefreshStopped)
        self._r_tmr = QTimer(self)
        self._r_tmr.timeout.connect(self.__model.refresh_data)

    @pyqtSlot()
    def auto_resize_columns(self):
        for c in range(self.view.model().columnCount()):
            self.view.resizeColumnToContents(c)

    @pyqtSlot(bool)
    def refreshData(self, is_checked: bool):
        """Refresh the data model.
        """
        if is_checked:
            self._dt_ms = int(1000.0 / self.refresh_rate_dsbox.value())
            self._r_tmr.start(self._dt_ms)
        else:
            self._r_tmr.stop()
        for _w in (self.refresh_rate_dsbox, ):
            _w.setDisabled(is_checked)

    @pyqtSlot()
    def onDataRefreshStarted(self):
        pass

    @pyqtSlot()
    def onDataRefreshStopped(self):
        self.refresh_sts_lbl.setPixmap(QPixmap(":/tm-icons/active.png"))
        delayed_exec(
            lambda: self.refresh_sts_lbl.setPixmap(
                QPixmap(":/tm-icons/inactive.png")), int(self._dt_ms * 0.6))

        if not self._auto_width_init_flag:
            self.auto_resize_columns()
            self._auto_width_init_flag = True

    def closeEvent(self, evt):
        self._r_tmr.stop()

    @pyqtSlot()
    def saveData(self):
        """Save data into a file.
        """
        _auto_filename = datetime.now().strftime(
            "%Y%m%dT%H%M%S") + f"_{self.device_type}.csv"
        outfilepath = os.path.join(self.outdata_dir, _auto_filename)
        self.__model.get_dataframe().to_csv(outfilepath, index=False)
        QMessageBox.information(self, "MPS Diagnostics Threshold Configs",
                                f"Saved data to {outfilepath}", QMessageBox.Ok,
                                QMessageBox.Ok)
        self.saveToDatabase('testing', ['test1', 'test2'])

    def saveToDatabase(self, note: str, tags: list, meta_isrc_name: str = 'Live', conn: sqlite3.Connection = None):
        # save data to the database.
        ts = time.time()
        user = getuser()
        ion_name, ion_num, ion_mass, ion_charge, ion_charge1, \
            beam_power, beam_energy, beam_dest = BeamSpeciesDisplayWidget.get_species_meta_full(
                ISRC_INDEX_MAP[meta_isrc_name])
        data = self.__model.get_dataframe()
        _row_data = (ts, user, ion_name, ion_num, ion_mass, ion_charge, ion_charge1,
                     beam_power, beam_energy, beam_dest, ','.join(tags), note, data)
        print(_row_data[:-1])
        snp_data = SnapshotData(_row_data)
        if conn is None:
            conn = self.snp_parent.get_db_con()
        table_name = TABLE_NAME_MAP[self.device_type]
        insert_update_data(conn, snp_data, table_name)
        print(f"Saved data {snp_data} to the databse.")

    @pyqtSlot()
    def compareData(self):
        """Compare data, highlight the differences.
        """
        filepath, ext = get_open_filename(self, type_filter='CSV File (*.csv)')
        if filepath is None:
            return None
        ref_df = pd.read_csv(filepath)

        self.diff_type_lbl.setText(
            '<p><span style="font-weight:600;color:#007BFF;">[FILE]</span></p>'
        )
        _fulltext = f'''<p><span style="font-weight:600;color:#007BFF;">[FILE]</span> {filepath}</p>'''
        _intext = QFontMetrics(self.ref_datafilepath_lbl.font()).elidedText(
            filepath, Qt.ElideRight, self.ref_datafilepath_lbl.width())
        self.ref_datafilepath_lbl.setText(_intext)
        self.ref_datafilepath_lbl.setToolTip(_fulltext)
        self.__model.highlight_diff(ref_df)
        self.diff_help_btn.setVisible(True)

    @pyqtSlot()
    def clearDiff(self):
        """Clear diff.
        """
        self.ref_datafilepath_lbl.clear()
        self.diff_type_lbl.clear()
        self.__model.update_ref_dataframe(None)
        self.diff_help_btn.setVisible(False)

    @pyqtSlot()
    def takeDiff(self):
        """Take a snapshot of current live readings for diff.
        """
        auto_name = datetime.now().strftime(
            "%Y%m%dT%H%M%S") + f"_{self.device_type}"
        self.__model.highlight_diff(self.__model.get_dataframe())
        self.diff_type_lbl.setText(
            '<p><span style="font-weight:600;color:#DC3545;">[MEM]</span></p>')
        _fulltext = f'''<p><span style="font-weight:600;color:#DC3545;">[MEM]</span> {auto_name}</p>'''
        _intext = QFontMetrics(self.ref_datafilepath_lbl.font()).elidedText(
            auto_name, Qt.ElideRight, self.ref_datafilepath_lbl.width())
        self.ref_datafilepath_lbl.setText(_intext)
        self.ref_datafilepath_lbl.setToolTip(_fulltext)
        self.diff_help_btn.setVisible(True)

    @pyqtSlot()
    def onHelpDiffMode(self):
        """Show the help message for diff mode.
        """
        _help_text = '''<html>
        <p>Diff mode is enabled: Colored cells indicate diff from the reference,
        reference could be loaded from saved data ("Load-Diff") or set through
        "Take-Diff".</p>
        <p><span style="color:#28a745;">Green</span> color indicates the live
        reading is lower than the reference; <span style="color:#dc3545;">red</span>
        color is higher, hover on the cell gives the reference reading and the relative
        difference in percentage.</p></html>
        '''
        QMessageBox.information(self, "Diff Mode Help", _help_text,
                                QMessageBox.Ok, QMessageBox.Ok)


TABLE_NAME_MAP = {
    'ND': 'mps_threshold_nd',
    'IC': 'mps_threshold_ic',
    'HMR': 'mps_threshold_hmr',
}


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    w1 = MPSDiagWidget('ND', '/tmp/')
    # w2 = MPSDiagWidget('IC')
    # w3 = MPSDiagWidget('HMR')
    w1.show()
    # w2.show()
    # w3.show()

    sys.exit(app.exec_())
