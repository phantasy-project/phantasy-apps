#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
from datetime import datetime

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap

from phantasy_ui import delayed_exec
from phantasy_ui import get_open_filename
from phantasy_apps.settings_manager.ui.ui_mps_diag import Ui_Form
from phantasy_apps.settings_manager._mps_model import MPSBeamLossDataModel
from phantasy_apps.settings_manager._mps_model import MPSBeamLossDataDelegateModel

DEVICE_TYPE_FULLNAME_MAP = {
    'ND': 'Neutron Detector',
    'IC': 'Ionization Chamber',
    'HMR': 'Halo Monitor Ring',
}


class MPSDiagWidget(QWidget, Ui_Form):

    def __init__(self, device_type: str, outdata_dir: str, parent=None):
        super(self.__class__, self).__init__()
        self.parent = parent

        self.setupUi(self)
        self.device_type = device_type
        self.outdata_dir = outdata_dir
        self.setWindowTitle(
            f"MPS Configurtions: Beam Loss Threshold ({self.device_type})")

        self._post_init()

    def _post_init(self):
        self._dt_ms = int(1000.0 / self.refresh_rate_dsbox.value())
        self.dtype_lbl.setText(
            '<html><head/><body><p><span style=" font-size:20pt; font-weight:600; color:#0055ff;">{dtype}</span></p></body></html>'.format(
                dtype=DEVICE_TYPE_FULLNAME_MAP[self.device_type]))
        self.view.setItemDelegate(MPSBeamLossDataDelegateModel(self.view))
        self.set_data()
        self.hide_columns()
        delayed_exec(lambda: self.auto_resize_columns(), 2000)

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
        for _w in (self.refresh_rate_dsbox,):
            _w.setDisabled(is_checked)

    @pyqtSlot()
    def onDataRefreshStarted(self):
        pass
        # self.refresh_sts_lbl.setPixmap(QPixmap(":/sm-icons/inactive.png"))

    @pyqtSlot()
    def onDataRefreshStopped(self):
        self.refresh_sts_lbl.setPixmap(QPixmap(":/sm-icons/active.png"))
        delayed_exec(lambda:self.refresh_sts_lbl.setPixmap(QPixmap(":/sm-icons/inactive.png")), int(self._dt_ms * 0.6))

    def closeEvent(self, evt):
        self._r_tmr.stop()

    @pyqtSlot()
    def saveData(self):
        """Save data into a file.
        """
        _auto_filename = datetime.now().strftime("%Y%m%dT%H%M%S") + f"_{self.device_type}.csv"
        outfilepath = os.path.join(self.outdata_dir, _auto_filename)
        self.__model.get_dataframe().to_csv(outfilepath, index=False)
        QMessageBox.information(self, "MPS Diagnostics Threshold Configs", f"Saved data to {outfilepath}",
                                QMessageBox.Ok, QMessageBox.Ok)
    
    @pyqtSlot()
    def compareData(self):
        """Compare data, highlight the differences.
        """
        filepath, ext = get_open_filename(self, type_filter='CSV File (*.csv)')
        if filepath is None:
            return None
        ref_df = pd.read_csv(filepath)
        self.ref_datafilepath_lineEdit.setText(filepath)
        self.__model.highlight_diff(ref_df)
    
    @pyqtSlot()
    def clearDiff(self):
        """Clear diff.
        """
        self.ref_datafilepath_lineEdit.clear()
        self.__model.update_ref_dataframe(None)



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
