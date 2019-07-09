#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""2D params scan.

Tong Zhang <zhangt@frib.msu.edu>
2019-06-20 10:59:21 AM EDT
"""
import numpy as np
import pickle
from datetime import datetime
from numpy import ndarray
import os

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox

from phantasy import CaField
from phantasy_ui import BaseAppForm
from phantasy_ui import random_string
from phantasy_ui.widgets import ElementWidget

from .app_array_set import ArraySetDialog
from .app_elem_select import ElementSelectDialog
from .data import ScanDataModel
from .scan import ScanTask
from .scan import load_task
from .ui.ui_2dscan import Ui_MainWindow
from .utils import COLOR_DANGER, COLOR_INFO
from .utils import delayed_exec


class TwoParamsScanWindow(BaseAppForm, Ui_MainWindow):

    # scan finish
    scanAllFinished = pyqtSignal()

    # image
    image_title_changed = pyqtSignal('QString')
    image_avg_data_changed = pyqtSignal(ndarray)
    image_std_data_changed = pyqtSignal(ndarray)
    xdata_changed = pyqtSignal(ndarray)
    ydata_changed = pyqtSignal(ndarray)
    ylabel_changed = pyqtSignal('QString')

    # curve
    curve_data_changed = pyqtSignal(QVariant, QVariant, QVariant, QVariant)
    curve_ylabel_changed = pyqtSignal('QString')
    line_id_changed = pyqtSignal(int)

    # curve & image
    xlabel_changed = pyqtSignal('QString')

    def __init__(self, parent=None):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self._p = parent

        self.setAppVersion(parent._version)
        app_title_p = parent.getAppTitle()
        self.setAppTitle("{}[{}]".format(app_title_p, '2D'))
        self.setWindowTitle("{}: {}".format(
            app_title_p, "Extend to Higher Dimensions"))

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

        # lattice --> _sel_elem_dialogs {}
        self._p.segments_updated.connect(self.on_lattice_updated)

        # inner loop out data
        for o in (self._p.niter_spinBox, self._p.nshot_spinBox):
            o.valueChanged.connect(self.init_out_data)

        self._p.extraMonitorsNumberChanged.connect(self.on_extra_moni_changes)

        # 3d data (avg, std)
        self._avg_img_widget = self.avg_mplimagewidget
        self._std_img_widget = self.std_mplimagewidget

        self.image_avg_data_changed.connect(self._avg_img_widget.update_image)
        self.image_std_data_changed.connect(self._std_img_widget.update_image)
        for o in (self._avg_img_widget, self._std_img_widget):
            self.xdata_changed.connect(o.setXData)
            self.ydata_changed.connect(o.setYData)
            self.xlabel_changed.connect(o.setFigureXlabel)
            self.ylabel_changed.connect(o.setFigureYlabel)
            self.image_title_changed.connect(o.setFigureTitle)

        # data (curve w/ eb)
        self._curve_widget = self.curve_mplebwidget
        self.curve_data_changed.connect(self._curve_widget.update_curve)
        self.xlabel_changed.connect(self._curve_widget.setFigureXlabel)
        self.curve_ylabel_changed.connect(self._curve_widget.setFigureYlabel)
        self.line_id_changed.connect(self._curve_widget.setLineID)
        self.line_id_changed.connect(self._curve_widget.setEbLineID)

        # moi
        self.moi_cbb.currentIndexChanged.connect(self.on_update_moi)

        # scan finish
        self.scanAllFinished.connect(self.on_finish)
        self.scanAllFinished.connect(self.reset_alter_element)

        # initial scan task
        self.init_scan_task()

        # post init
        self.post_init()

    def post_init(self):
        # clear dataviz widgets
        for o in (self.avg_mplimagewidget, self.std_mplimagewidget,
                  self.curve_mplebwidget, ):
            o.clear_data()
        # reset the line/mk style of curve w/ eb
        o = self.curve_mplebwidget
        c = QColor("#FF0000")
        o.setLineColor(c)
        o.setMkEdgeColor(c)
        o.setMkFaceColor(c)
        o.setEbMkEdgeColor(c)
        o.setEbMkFaceColor(c)
        o.setEbLineColor(c)

    def on_extra_moni_changes(self, i):
        # workaround to ensure the extra moni counter is updated.
        delayed_exec(lambda: self.init_out_data(), 10)

    def init_out_data(self, *args):
        # reset inner loop out data array
        self._p.scan_task.init_out_data()

        # debug
        shape = self._p.scan_task.scan_out_data.shape
        print("Inner out data shape is:", shape)
        #
        self.data = np.asarray(
                [np.ones(shape) * np.nan] * self.scan_task.alter_number)
        print("Whole data shape is:", self.data.shape)

    def init_moi(self):
        """Initial monitor-of-interest cbb list.
        """
        self._idx = 0

        monitors = [self._p.scan_task.monitor_element, ] + \
                    self._p.scan_task.get_extra_monitors()

        flds = []
        for o in monitors:
            if isinstance(o, CaField):
                fld = '{0} [{1}]'.format(o.ename, o.name)
            else:
                fld = o.ename
            flds.append(fld)

        o = self.moi_cbb
        o.currentIndexChanged.disconnect()
        o.clear()
        o.addItems(flds)
        o.currentIndexChanged.connect(self.on_update_moi)
        # initial
        o.currentIndexChanged.emit(0)
        self.image_title_changed.emit(o.currentText())

    def _get_lbl(self, mode):
        # get xlabel or ylabel
        if mode == 'inner':
            o = self._p.scan_task.alter_element
        else:
            o = self.scan_task.alter_element
        if isinstance(o, CaField):
            lbl = '{0} [{1}]'.format(o.ename, o.name)
        else:
            lbl = o.ename
        return lbl

    @pyqtSlot(int)
    def on_update_moi(self, idx):
        # the index of moi changed.
        setattr(self, '_idy', idx + 1)
        self.on_update_moi_labels()
        self.on_update_data()

    def on_update_data(self):
        """Update image and curve data (live), when switching monitors.

        For image data, should refresh all the data, including the data
        already acquired, only allowed when task is done.
        """
        data = self.data
        idx, idy = self._idx, self._idy
        # l: niter of outer loop
        # n,m,k: niter,nshot, nmoni of inner loop
        l, n, m, k = data.shape
        # update image data
        if not self._run:
            for i in range(l):
                sm = ScanDataModel(data[i, :])
                self.avg_data[i] = sm.get_yavg(ind=idy)
                self.std_data[i] = sm.get_yerr(ind=idy)
            self.image_avg_data_changed.emit(self.avg_data)
            self.image_std_data_changed.emit(self.std_data)

        if np.all(np.isnan(self.data)):
            return
        # update curve data
        nn = self._iiter if self._run else l
        for i in range(nn):
            sm = ScanDataModel(data[i, :])
            x, xerr = sm.get_xavg(ind=idx), sm.get_xerr(ind=idx)
            y, yerr = sm.get_yavg(ind=idy), sm.get_yerr(ind=idy)
            self.line_id_changed.emit(i)
            self.curve_data_changed.emit(x, y, xerr, yerr)


    def on_update_moi_labels(self):
        """Update ylabel of curve widget and title of image widget.
        """
        lbl = self.moi_cbb.currentText()
        if not self._run:
            self.image_title_changed.emit(lbl)
        self.curve_ylabel_changed.emit(lbl)

    def init_scan_task(self):
        task_name = random_string(6)
        self.scan_task = ScanTask(task_name)

        # init out data
        for o in (self.niter_spinBox, self.waitsec_dSpinBox):
            o.valueChanged.emit(o.value())
        # reset
        self.reset_flags()

    def reset_flags(self):
        # init alter point
        self._iiter = 0
        # initialized?
        self._initialized = False
        # task status
        self._run = False

    def init_dataviz(self):
        """Dataviz initialization.
        """
        # image
        inner_alter_array = self._p.scan_task.get_alter_array()
        outer_alter_array = self.scan_task.get_alter_array()
        xx, yy = np.meshgrid(inner_alter_array, outer_alter_array)
        avg_data = np.ones(xx.shape) * np.nan
        std_data = np.ones(xx.shape) * np.nan
        self.xdata_changed.emit(xx)
        self.ydata_changed.emit(yy)
        inner_lbl = self._get_lbl('inner')
        outer_lbl = self._get_lbl('outer')
        self.xlabel_changed.emit(inner_lbl)
        self.ylabel_changed.emit(outer_lbl)
        self.image_avg_data_changed.emit(avg_data)
        self.image_std_data_changed.emit(std_data)
        self.avg_data = avg_data
        self.std_data = std_data
        # curve
        o = self._curve_widget

        # clear curves (tmp solutiono)
        for i, l in enumerate(o.get_all_curves()):
            self.line_id_changed.emit(i)
            o.setLineLabel("_line{}".format(i))
            o.clear_data()

        o.setFigureTitle("v: {}".format(outer_lbl))
        for i, v in enumerate(outer_alter_array):
            if len(o.get_all_curves()) < i + 1:
                # add new curve
                o.add_curve(None, None, None, None)
            # reset curve
            self.line_id_changed.emit(i)
            o.setLineLabel("$v={0:.3g}$".format(v))

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
        self.scan_task.alter_number = i
        # self.init_out_data()

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
            self._p.scanlogUpdated.emit("[M] Empty input of scan range is invalid")
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
        # debug
        print("Alter array: ", alter_array)
        print("Current setting: ", alter_array[self._iiter])
        #
        # set outer element
        self.scan_task.alter_element.value = alter_array[self._iiter]

        if not self._run:
            self._run = True

        if not self._initialized:
            self._connect_signals()
            # preset out data
            self.init_out_data()
            # monitor-of-interest
            self.init_moi()
            # image data
            self.init_dataviz()
            self._initialized = True

        # run inner loop
        delayed_exec(lambda: self._p.start_btn.clicked.emit(), self._dmsec)

    @pyqtSlot(QVariant)
    def on_data_updated(self, arr):
        # collect data
        self.data[self._iiter] = arr

        # updata dataviz
        self._update_dataviz()

        # next iter
        self._iiter += 1
        if self._iiter < self.scan_task.alter_number:
            self.start_btn.clicked.emit()
        else:
            self._iiter -= 1
            self.scanAllFinished.emit()

    @pyqtSlot()
    def on_finish(self):
        # all finish
        print("Scan is done.")
        # dump data
        self._dump_data(self.data)
        # reset flags
        self.reset_flags()
        #
        self._disconnect_signals()

    def _dump_data(self, data, filepath=None):
        # dump *data* to filepath.
        if filepath is None:
            filepath = "CV_2D_{}.pkl".format(
                    datetime.now().strftime("%Y%m%dT%H%M%S"))
        try:
            with open(filepath, 'wb') as f:
                pickle.dump(data, f)
        except:
            QMessageBox.warning(self, "Save Data", "Failed to dump data.",
                    QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Save Data",
                    "Saved data to {}".format(os.path.abspath(filepath)),
                    QMessageBox.Ok)

    @pyqtSlot()
    def reset_alter_element(self):
        x0 = self.scan_task.get_initial_setting()
        # restore alter elem
        self._p.scanlogTextColor.emit(COLOR_INFO)
        self._p.scanlogUpdated.emit(
            "[M] Scan task is done, reset alter element...")
        self._p.scanlogUpdated.emit(
            "[M] Setting alter element to {0:.3f}...".format(x0))
        self.scan_task.alter_element.value = x0
        self._p.scanlogUpdated.emit(
            "[M] Alter element reaches {0:.3f}".format(x0))

    @pyqtSlot(list)
    def on_lattice_updated(self, l):
        self._sel_elem_dialogs = {}

    def update_progress(self):
        self.alter_elem_val_lineEdit.setText("Value: {}, IITER: {}".format(
            self.scan_task.alter_element.value,
            self._iiter))

    def _update_dataviz(self):
        # update curve and image dataviz
        idx, idy = self._idx, self._idy

        data = self.data
        #
        sm = ScanDataModel(data[self._iiter, :])
        # curve w/ eb
        x, xerr = sm.get_xavg(ind=idx), sm.get_xerr(ind=idx)
        y, yerr = sm.get_yavg(ind=idy), sm.get_yerr(ind=idy)
        self.line_id_changed.emit(self._iiter)
        self.curve_data_changed.emit(x, y, xerr, yerr)

        # image, avg & std
        self.avg_data[self._iiter] = sm.get_yavg(ind=idy)
        self.std_data[self._iiter] = sm.get_yerr(ind=idy)
        self.image_avg_data_changed.emit(self.avg_data)
        self.image_std_data_changed.emit(self.std_data)

    def _disconnect_signals(self):
        # disconnect signals
        self._p.start_btn.clicked.disconnect(self.update_progress)
        self._p.data_updated.disconnect(self.on_data_updated)

    def _connect_signals(self):
        # reconnect signals
        self._p.start_btn.clicked.connect(self.update_progress)
        self._p.data_updated.connect(self.on_data_updated)
