#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import pandas as pd
from datetime import datetime

from PyQt5.QtWidgets import (
    QWidget,
    QMessageBox,
)

from PyQt5.QtCore import (
    pyqtSignal,
    pyqtSlot,
    QTimer,
    Qt,
    QModelIndex,
)

from PyQt5.QtGui import (
    QPixmap,
    QFontMetrics,
)

from phantasy_ui import delayed_exec
from phantasy_ui.widgets import SnapshotWidget as _SnapshotWidget

from phantasy_apps.threshold_manager.ui.ui_mps_diag import Ui_Form as MPSDiagWidgetForm
from phantasy_apps.threshold_manager._model import (
    MPSBeamLossDataModel,
    MPSBeamLossDataDelegateModel,
)
from phantasy_apps.threshold_manager.db.utils import ensure_connect_db
from phantasy_apps.threshold_manager.data import SnapshotData
from phantasy_apps.threshold_manager.tools import take_snapshot

DEVICE_TYPE_FULLNAME_MAP = {
    'ND': 'Neutron Detector',
    'IC': 'Ionization Chamber',
    'HMR': 'Halo Monitor Ring',
}


def read_dataframe(db_path: str, table_name: str):
    """ Read all data as a dataframe from a database file.
    """
    # t0 = time.perf_counter()
    # print("Reading database...")
    con = ensure_connect_db(db_path)
    query = f'''
        SELECT timestamp, datetime,
               isrc_name, ion_name, ion_number, ion_mass, ion_charge, ion_charge_state,
               user, beam_power, beam_energy, beam_bound, beam_dest, tags, note,
               data
               FROM {table_name} '''
    df = pd.read_sql(query, con).sort_values('timestamp', ascending=False)
    # generate date column:
    df['date'] = df['timestamp'].apply(
        lambda i: datetime.fromtimestamp(i).strftime("%Y-%m-%d %A"))
    # print(f"Reading database...done {time.perf_counter() - t0:.1f}s")
    return df, con, table_name


class SnapshotWidget(_SnapshotWidget):

    # index, info df, ref df
    ndDataLoaded = pyqtSignal(QModelIndex, pd.DataFrame, pd.DataFrame)
    icDataLoaded = pyqtSignal(QModelIndex, pd.DataFrame, pd.DataFrame)
    hmrDataLoaded = pyqtSignal(QModelIndex, pd.DataFrame, pd.DataFrame)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_admin_names(('zhangt', 'tong'))
        self.set_ctx_bit(COPY_DATA=False, MS=False)
        self.db_path_lineEdit.setVisible(False)
        self.db_path_lineEdit.setReadOnly(True)
        # close the top part (tag,ion filter buttons)
        self.vsplitter.setSizes([0, 100])

    def read_data(self):
        db_path = self.get_db_path()
        return read_dataframe(db_path, "mps_threshold")

    def onLoadData(self, idx: QModelIndex, dat: bytes):
        """Load the data blob
        """
        df_dict = SnapshotData.read_blob(dat)
        df_info = df_dict.get('info')
        df_nd = df_dict.get('ND')
        df_ic = df_dict.get('IC')
        df_hmr = df_dict.get('HMR')
        if df_nd is not None:
            self.ndDataLoaded.emit(idx, df_info, df_nd)
        if df_ic is not None:
            self.icDataLoaded.emit(idx, df_info, df_ic)
        if df_hmr is not None:
            self.hmrDataLoaded.emit(idx, df_info, df_hmr)


class MPSDiagWidget(QWidget, MPSDiagWidgetForm):

    # data saved to database
    dataSaved = pyqtSignal()

    # str: timestamp of the loaded snapshot entry
    snapshotToLocate = pyqtSignal(str)

    def __init__(self, device_type: str, parent=None):
        super(self.__class__, self).__init__()
        self.parent = parent

        self.setupUi(self)
        self.device_type = device_type
        self.setWindowTitle(
            f"MPS Configurtions: Beam Loss Threshold ({self.device_type})")

        self._post_init()

    def set_snp_parent(self, w):
        # w: SnapshotWidget
        self.snp_parent = w

    def _post_init(self):
        self._auto_width_init_flag = False
        self.diff_help_btn.setVisible(False)
        self.snp_locate_btn.setVisible(False)
        self._dt_ms = int(1000.0 / self.refresh_rate_dsbox.value())
        self.dtype_lbl.setText(
            '<html><head/><body><p><span style=" font-size:18pt; font-weight:600; color:#0055ff;">{dtype}</span></p></body></html>'
            .format(dtype=DEVICE_TYPE_FULLNAME_MAP[self.device_type]))
        self.view.setItemDelegate(MPSBeamLossDataDelegateModel(self.view))
        self.set_data()
        self.hide_columns()
        # self.refresh_data()
        # the timestamp value for the loaded snpashot
        self._diff_snp_ts: float = None
        self._loadSnpIdx = None
        
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

    def refresh_data(self, auto=False, delay_ms=1000):
        # refresh data for one time.
        if not auto:
            delayed_exec(lambda: self.__model.refresh_data(), delay_ms)
        else:
            delayed_exec(lambda: self.refresh_btn.setChecked(True), delay_ms)

    @pyqtSlot()
    def auto_resize_columns(self):
        for c in range(self.view.model().columnCount()):
            self.view.resizeColumnToContents(c)
        # adjust row height
        if self.diff_help_btn.isVisible():
            self.view.itemDelegate().setRowHeight(58)
        else:
            self.view.itemDelegate().setRowHeight(36)

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
        take_snapshot([
            self.device_type,
        ],
                      note=f'Snapshot only for {self.device_type}',
                      tags=[self.device_type],
                      conn=self.snp_parent.get_db_conn())
        self.dataSaved.emit()

    @pyqtSlot(QModelIndex, pd.DataFrame, pd.DataFrame)
    def onDataLoaded(self, idx: QModelIndex, df_info: pd.DataFrame,
                     df_data: pd.DataFrame):
        # set new ref_df
        self._post_ref_snp_info(df_info)
        self.__model.highlight_diff(df_data)
        self.diff_help_btn.setVisible(True)
        self.snp_locate_btn.setVisible(True)
        self._loadSnpIdx = idx

    def _post_ref_snp_info(self, df: pd.DataFrame):
        # snapshot info data is loaded
        ts = df.columns[1]  # float timestamp
        self._diff_snp_ts = ts
        _datetime = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        _df = df.set_index('timestamp').T
        ion_name = _df.ion_name.to_list()[0]
        ion_mass = _df.ion_mass.to_list()[0]
        ion_charge = _df.ion_charge.to_list()[0]
        beam_dest = _df.beam_dest.to_list()[0]

        msg = f"[{_datetime}] {ion_mass}{ion_name}{ion_charge}+ ({beam_dest})"

        self.diff_type_lbl.setText(
            '<p><span style="font-weight:600;color:#007BFF;">[Snapshot]</span></p>'
        )
        _fulltext = f'''<p><span style="font-weight:600;color:#007BFF;">[Snapshot]</span> {msg}</p>'''
        _intext = QFontMetrics(self.ref_datafilepath_lbl.font()).elidedText(
            msg, Qt.ElideRight, self.ref_datafilepath_lbl.width())
        self.ref_datafilepath_lbl.setText(_intext)
        self.ref_datafilepath_lbl.setToolTip(_fulltext)

    @pyqtSlot()
    def clearDiff(self):
        """Clear diff.
        """
        self.ref_datafilepath_lbl.clear()
        self.diff_type_lbl.clear()
        self.__model.update_ref_dataframe(None)
        self.diff_help_btn.setVisible(False)
        self.snp_locate_btn.setVisible(False)
        self.auto_resize_columns()

    @pyqtSlot()
    def onHelpDiffMode(self):
        """Show the help message for diff mode.
        """
        _help_text = '''<html>
        <p>Diff mode is enabled: Colored cells indicate diff from the reference,
        reference could be loaded from the Snapshot Data Management window.</p>
        <p><span style="color:#28a745;">Green</span> color indicates the live
        reading is lower than the reference; <span style="color:#dc3545;">red</span>
        color is higher, hover on the cell gives the reference reading and the relative
        difference in percentage.</p></html>
        '''
        QMessageBox.information(self, "Diff Mode Help", _help_text,
                                QMessageBox.Ok, QMessageBox.Ok)

    @pyqtSlot()
    def onLocateSnp(self):
        """Find and highlight the snapshot.
        """
        if self._diff_snp_ts is not None:
            self.snapshotToLocate.emit(f"{self._diff_snp_ts:.6f}")


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    w1 = MPSDiagWidget('ND')
    # w2 = MPSDiagWidget('IC')
    # w3 = MPSDiagWidget('HMR')
    w1.show()
    # w2.show()
    # w3.show()

    sys.exit(app.exec_())
