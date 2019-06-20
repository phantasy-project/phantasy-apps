#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""2D params scan.

Tong Zhang <zhangt@frib.msu.edu>
2019-06-20 10:59:21 AM EDT
"""
import numpy as np

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QDialog

from phantasy_ui import BaseAppForm
from phantasy_ui.widgets import ElementWidget

from .app_elem_select import ElementSelectDialog
from .ui.ui_2dscan import Ui_MainWindow
from .scan import load_task
from phantasy_ui import random_string
from .scan import ScanTask
from .app_array_set import ArraySetDialog
from .utils import COLOR_DANGER
from .utils import delayed_exec


class TwoParamsScanWindow(BaseAppForm, Ui_MainWindow):

    # scan finish
    scanAllFinished = pyqtSignal()

    def __init__(self, parent=None):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self._p = parent

        self.setAppVersion(parent._version)
        app_title_p = parent.getAppTitle()
        self.setAppTitle("{}[{}]".format(app_title_p, '2D'))
        self.setWindowTitle("{}: {}".format(
            app_title_p, "Extend to Higher Dimension"))

        #
        self.select_alter_elem_btn.clicked.connect(self.on_select_elem)
        self._sel_elem_dialogs = {}
        self.elem_widgets_dict = {}

        # set alter array btn
        self.alter_array_btn.clicked.connect(self.on_set_alter_array)
        self._set_alter_array_dialogs = {}  # keys: alter element name

        # enable arbitary alter array input
        self.enable_arbitary_array_chkbox.toggled.connect(self.on_toggle_array)

        # outer loop step counter
        self.niter_spinBox.valueChanged.connect(self.on_update_niter)

        # outer_element settling time
        self.waitsec_dSpinBox.valueChanged.connect(self.on_update_waitsec)

        # start scan
        self.start_btn.clicked.connect(self.on_start_scan)

        # alter range
        self.lower_limit_lineEdit.textChanged.connect(self.set_alter_range)
        self.upper_limit_lineEdit.textChanged.connect(self.set_alter_range)

        # data
        self._p.data_updated.connect(self.on_data_updated)

        # scan finish
        self.scanAllFinished.connect(self.on_finish)

        # initial scan task
        self.init_scan_task()

    def init_scan_task(self):
        task_name = random_string(6)
        self.scan_task = ScanTask(task_name)

        # reset inner loop out data array
        self._p.scan_task.init_out_data()

        # init
        for o in (self.niter_spinBox, self.waitsec_dSpinBox):
            o.valueChanged.emit(o.value())

        self._i = 0

    @pyqtSlot()
    def on_set_alter_array(self):
        """Set alter array dialog.
        """
        dlg = self._set_alter_array_dialogs.setdefault(
            self.scan_task.name, ArraySetDialog(self))
        r = dlg.exec_()

        if r == QDialog.Accepted:
            arr = dlg.array
            self.scan_task.set_alter_array(arr)
            self.niter_spinBox.setValue(self.scan_task.alter_number)
            v1, v2 = self.scan_task.alter_start, self.scan_task.alter_stop
            self.lower_limit_lineEdit.setText(str(v1))
            self.upper_limit_lineEdit.setText(str(v2))
        elif r == QDialog.Rejected:
            print("No array set")
            return

    @pyqtSlot(bool)
    def on_toggle_array(self, ischecked):
        """If checked,

        1. disconnect textChanged of lower_limit_lineEdit, upper_limit_lineEdit
        2. disconnect valueChanged of niter_spinBox
        3. disable lower_limit_lineEdit, upper_limit_lineEdit, niter_spinBox
        if not checked, connect 1&2 and enable 3.
        """
        if ischecked:
            self.lower_limit_lineEdit.textChanged.disconnect()
            self.upper_limit_lineEdit.textChanged.disconnect()
            self.niter_spinBox.valueChanged.disconnect()
            self.lower_limit_lineEdit.setEnabled(False)
            self.upper_limit_lineEdit.setEnabled(False)
            self.niter_spinBox.setEnabled(False)
        else:
            self.lower_limit_lineEdit.textChanged.connect(self.set_alter_range)
            self.upper_limit_lineEdit.textChanged.connect(self.set_alter_range)
            self.niter_spinBox.valueChanged.connect(self.on_update_niter)
            self.lower_limit_lineEdit.setEnabled(True)
            self.upper_limit_lineEdit.setEnabled(True)
            self.niter_spinBox.setEnabled(True)

    @pyqtSlot(int)
    def on_update_niter(self, i):
        # total number of scan points
        shape = self._p.scan_task.scan_out_data.shape
        print("Inner out data shape is:", shape)
        self.scan_task.alter_number = i
        self.data = np.asarray(
                [np.ones(shape) * np.nan] * i)
        print("Whole data shape is:", self.data.shape)

    @pyqtSlot(float)
    def on_update_waitsec(self, x):
        # time wait after every scan data setup, in sec
        self.scan_task.t_wait = x
        self._dmsec = x * 1000

    @pyqtSlot()
    def set_alter_range(self):
        """Set scan alter vars range.
        """
        srange_val1_str = self.lower_limit_lineEdit.text()
        srange_val2_str = self.upper_limit_lineEdit.text()
        try:
            sval1, sval2 = float(srange_val1_str), float(srange_val2_str)
        except ValueError:
            self._p.scanlogTextColor.emit(COLOR_DANGER)
            self._p.scanlogUpdated.emit("Empty input of scan range is invalid")
        else:
            self.scan_task.alter_start = sval1
            self.scan_task.alter_stop = sval2

    @pyqtSlot()
    def on_select_elem(self):
        """Select element via PV or high-level element for alter-vars and
        monitor-vars.
        """
        mode = "alter"
        dlg = self._sel_elem_dialogs.setdefault(mode, ElementSelectDialog(self, mode, mp=self._p._mp))
        r = dlg.exec_()
        self._p.elementsTreeChanged.connect(dlg.on_update_elem_tree)

        if r == QDialog.Accepted:
            # update element obj (CaField)
            sel_elem = dlg.sel_elem[0]  # CaField
            sel_elem_display = dlg.sel_elem_display[0]  # CaElement
            fname = dlg.sel_field[0]
            if fname is None:
                elem_btn_lbl = sel_elem_display.ename
            else:
                elem_btn_lbl = '{0} [{1}]'.format(sel_elem_display.name, fname)

            new_sel_key = ' '.join((sel_elem_display.ename, sel_elem.name, mode))
            # create elem_info widget, add into *elem_widgets_dict*
            self.elem_widgets_dict.setdefault(
                new_sel_key, ElementWidget(sel_elem_display, fields=fname))

            elem_btn = self._p._create_element_btn(elem_btn_lbl, new_sel_key,
                                                   self.elem_widgets_dict)
            self._p._place_element_btn(elem_btn, mode,
                                       target=self.alter_elem_lineEdit)

            #
            self.scan_task.alter_element = sel_elem
            # initialize scan range
            x0 = self.scan_task.get_initial_setting()
            self.lower_limit_lineEdit.setText('{}'.format(x0))
            self.upper_limit_lineEdit.setText('{}'.format(x0))
        elif r == QDialog.Rejected:
            # do not update alter element obj
            return

    @pyqtSlot()
    def on_start_scan(self):
        """Start scan.
        """
        alter_array = self.scan_task.get_alter_array()
        # set outer element
        self.scan_task.alter_element.value = alter_array[self._i]
        # run inner loop
        delayed_exec(lambda: self._p.start_btn.clicked.emit(), self._dmsec)

    @pyqtSlot(QVariant)
    def on_data_updated(self, arr):
        # collect data
        self.data[self._i] = arr

        # next iter
        self._i += 1
        if self._i < self.scan_task.alter_number:
            self.start_btn.clicked.emit()
        else:
            self._i -= 1
            self.scanAllFinished.emit()

    @pyqtSlot()
    def on_finish(self):
        # all finish
        print("Scan is done.")
        print(self.data)
