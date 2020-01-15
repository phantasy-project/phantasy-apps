#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""2D params scan.

Tong Zhang <zhangt@frib.msu.edu>
2019-06-20 10:59:21 AM EDT
"""
import numpy as np
import pickle
from datetime import datetime
from functools import partial
from getpass import getuser
from numpy import ndarray
import os

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox

from phantasy import CaField
from phantasy import ensure_put
from phantasy_ui.widgets import printlog
from phantasy_ui import BaseAppForm
from phantasy_ui import get_open_filename
from phantasy_ui import get_save_filename
from phantasy_ui import random_string
from phantasy_ui.widgets import ElementWidget

from .app_array_set import ArraySetDialog
from .app_elem_select import ElementSelectDialog
from .app_plot3d import Plot3dData
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

    # nested task loaded, i.e. 1d task
    nested_task_loaded = pyqtSignal(ScanTask)

    def __init__(self, parent=None):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self._p = parent

        self.setAppVersion(parent._version)
        app_title_p = parent.getAppTitle()
        self.setAppTitle(app_title_p)
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

        # outer alter element rd/set tolerance
        self.tol_dSpinBox.valueChanged.connect(self.on_update_tol)

        # outer_element settling time
        self.waitsec_dSpinBox.valueChanged.connect(self.on_update_waitsec)

        # start scan
        self.start_btn.clicked.connect(self.on_start_scan)

        # stop scan
        self.stop_btn.clicked.connect(self.on_stop_scan)

        # set start/stop btns status after scan is started
        self._p.start_btn.clicked.connect(partial(self.set_btn_status, 'start'))

        # init btn status
        self.set_btn_status('init')

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

        # connections to main window
        self.nested_task_loaded.connect(self._p.init_ui_with_scan_task)

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
        printlog("Inner out data shape is: {}".format(shape))
        #
        self.data = np.asarray(
                [np.ones(shape) * np.nan] * self.scan_task.alter_number)
        self.scan_task.scan_out_data = self.data
        printlog("Whole data shape is: {}".format(self.data.shape))

    def init_all_elements(self):
        """Initial all the elemetns (alter elements and all the monitors) for
        final 3D data visualization.
        """
        elems = [self.scan_task.alter_element, \
                 self._p.scan_task.alter_element, ] + \
                [self._p.scan_task.monitor_element, ] + \
                 self._p.scan_task.get_extra_monitors()
        flds = []
        for o in elems:
            if isinstance(o, CaField):
                fld = '{0} [{1}]'.format(o.ename, o.name)
            else:
                fld = o.fname
            flds.append(fld)

        cbbs = (self.ydata_cbb, self.xdata_cbb, self.zdata_cbb,)
        for i, icbb in enumerate(cbbs):
            icbb.clear()
            icbb.addItems(flds)
            icbb.setCurrentIndex(i)
        # interp init
        self.interp_nx_sbox.setValue(self._p.niter_spinBox.value())
        self.interp_ny_sbox.setValue(self.niter_spinBox.value())
        #
        self._plot3d_window = None

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
        try:
            self.on_update_data()
        except: # if not data to update, then just do nothing.
            pass

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
        # task_name = random_string(6)
        task_name = self._p.scan_task.name
        self.scan_task = ScanTask(task_name, mode="2D")
        self.scan_task.set_nested_task(self._p.scan_task)

        # init out data
        for o in (self.niter_spinBox, self.waitsec_dSpinBox,
                  self._p.niter_spinBox, self._p.nshot_spinBox,
                  self.tol_dSpinBox):
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
        printlog("Initialize 3D data visualization.")
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

    @pyqtSlot(float)
    def on_update_tol(self, x):
        # tolerance of delta(rd, set)
        self.scan_task.tolerance = x

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

    @pyqtSlot(tuple)
    def on_selection_changed(self, selections):
        self._elem_selections = selections

    @pyqtSlot()
    def on_select_elem(self):
        """Select element via PV or high-level element for alter-vars and
        monitor-vars.
        """
        mode = "alter"
        if mode not in self._sel_elem_dialogs:
            dlg = ElementSelectDialog(self, mode, mp=self._p._mp)
            dlg.selection_changed.connect(self.on_selection_changed)
            self._sel_elem_dialogs[mode] = dlg
            self._p.elementsTreeChanged.connect(dlg.on_update_elem_tree)
        else:
            dlg = self._sel_elem_dialogs[mode]

        r = dlg.exec_()
        if r == QDialog.Accepted:
            sel_elems, sel_elems_display, sel_fields = self._elem_selections
            # update element obj (CaField)
            sel_elem = sel_elems[0]  # CaField
            sel_elem_display = sel_elems_display[0]  # CaElement
            fname = sel_fields[0]
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
        # self.scan_task.alter_element.value = alter_array[self._iiter]
        elem = self.scan_task.alter_element
        x = alter_array[self._iiter]
        tol, wait_sec = self.scan_task.tolerance, self.scan_task.t_wait
        ensure_put(elem, goal=x, tol=tol, timeout=wait_sec)
        printlog("{} RD: {} SP: {}".format(elem.ename, elem.value, x))
        #
        if not self._run:
            self._run = True

        if not self._initialized:
            self._connect_signals()
            # scan task info
            self.init_task_info()
            # preset out data
            self.init_out_data()
            # monitor-of-interest
            self.init_moi()
            # elements for final data visualization
            self.init_all_elements()
            # image data
            self.init_dataviz()
            self._initialized = True

        # run inner loop
        self._dmsec = 0
        delayed_exec(lambda: self._p.start_btn.clicked.emit(), self._dmsec)

    def set_btn_status(self, mode='start'):
        if mode == 'start':
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.enable_post_processing_ctrls(False)
        elif mode == 'stop':
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.enable_post_processing_ctrls(True)
        elif mode == 'init':
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)

    def init_task_info(self):
        """Update scan task config.
        """
        self.scan_task.name = self._p.scan_task.name + '-2D'

    @pyqtSlot()
    def on_stop_scan(self):
        """Stop scan.
        """
        print("[2D] Stop scan...")
        self._p.stop_btn.clicked.emit()
        delayed_exec(lambda: self.scanAllFinished.emit(), 1000)

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
        # self._dump_data(self.data)
        # reset flags
        self.reset_flags()
        #
        self._disconnect_signals()
        #
        self.set_btn_status("stop")

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
    def on_save_task(self):
        """Save task configuration.
        """
        print("[2D] Save task configuration...")

        filename, ext = get_save_filename(self,
                caption="Save Scan Task (2D) to file",
                type_filter="JSON Files (*.json)")

        if filename is None:
            return

        self.init_task_info()
        data_sheet = self.scan_task.to_datasheet()
        data_sheet['data'].update({'filepath': filename})

        # info
        data_sheet.update({'info': {}})
        data_sheet['info'].update({'user': getuser(),
                                   'app': self.getAppTitle(),
                                   'version': self.getAppVersion(),})
        data_sheet['task'].update(
            {'array_mode': self.enable_arbitary_array_chkbox.isChecked()})
        if self._p._mp is not None:
            mp_conf = {'machine': self._p._mp.last_machine_name,
                       'segment': self._p._mp.last_lattice_name}
            data_sheet['task'].update(mp_conf)

        # 1D task configs
        fn, ext = filename.rsplit('.', 1)
        filepath_inner_loop = "{}.{}".format(fn + '_1d', ext)
        self._p._save_data_as_json(filepath_inner_loop)

        data_sheet['task']['nested_task'] = {'filepath': filepath_inner_loop}

        # save
        data_sheet.write(filename)
        #
        QMessageBox.information(self, "",
                                "Save 2D scan task config to {}".format(filename))

    @pyqtSlot()
    def on_load_task(self):
        """Load task configuration.
        """
        print("[2D] Load task configuration...")
        filepath, ext = get_open_filename(self,
                type_filter="JSON Files (*.json)")
        if filepath is None:
            return
        self._load_task(filepath)

    def _load_task(self, filepath):
        # set task, i.e. outer loop
        scan_task = load_task(filepath, self._p._mp)
        if hasattr(scan_task, '_lattice'):
            self._p._mp = scan_task._lattice
        try:
            assert scan_task.mode == "2D"
        except AssertionError:
            QMessageBox.warning(self, "Load 2D Task",
                    "The task trying to load is not 2D task, please select correct one or load 1D task in the main window of Correlation Visualizer.",
                    QMessageBox.Ok)
            return
        # set nested task, i.e. inner loop
        scan_task_1d = scan_task.get_nested_task()
        self.nested_task_loaded.emit(scan_task_1d)
        # ensure inner loop setup is done (tmp workaround)
        delayed_exec(lambda: self.init_ui_with_scan_task(scan_task), 1000)

    def init_ui_with_scan_task(self, scan_task):
        self.scan_task = scan_task
        # ui
        # alter element
        self._p._setup_element_btn_from_scan_task(
                scan_task, 'alter', widgets_dict=self.elem_widgets_dict,
                target=self.alter_elem_lineEdit)
        # scan range
        self.lower_limit_lineEdit.setText(str(scan_task.alter_start))
        self.upper_limit_lineEdit.setText(str(scan_task.alter_stop))
        # nite, t_wait
        self.niter_spinBox.setValue(scan_task.alter_number)
        self.waitsec_dSpinBox.setValue(scan_task.t_wait)
        self.tol_dSpinBox.setValue(scan_task.tolerance)

        # array mode
        self._set_alter_array_dialogs = {}
        self.enable_arbitary_array_chkbox.setChecked(scan_task.array_mode)

        # init data
        self.init_dataviz()
        # set data
        self.data = self.scan_task.scan_out_data
        # init moi
        self.init_moi()
        # elements for final data visualization
        self.init_all_elements()
        # show data
        printlog("Show 3D data on image widgets.")
        for i in range(self.scan_task.alter_number):
            self._iiter = i
            self._update_dataviz()
        self._iiter = 0

    @pyqtSlot()
    def on_save_data(self):
        """Save data after scan.
        """
        print("[2D] Save data...")

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
        self.alter_elem_val_lineEdit.setText("Value: {0:.6g}, ITER: {1}/{2}".format(
            self.scan_task.alter_element.value,
            self._iiter + 1, self.scan_task.alter_number))

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

    def make_data(self):
        """Make data for 3D plot.
        """
        idy = self.ydata_cbb.currentIndex() # outer y: 0
        idx = self.xdata_cbb.currentIndex() # inner x: 1 --> 0 (ScanDataModel)
        idz = self.zdata_cbb.currentIndex() # inner z,... 2... --> 1...
        data = {idx: [], idy: [], idz: []}

        outdata = self.scan_task.scan_out_data
        l, n, m, k = outdata.shape

        for iid in (idx, idy, idz):
            if iid == 0: # outer iterator
                x2 = self.scan_task.get_alter_array()
                data[iid] = [v for v in x2 for _ in range(n)]
            elif iid == 1: # inner iterator
                x1 = self._p.scan_task.get_alter_array()
                data[iid] = [v for _ in range(l) for v in x1]
                # for i in range(l):
                #     sm = ScanDataModel(outdata[i, :])
                #     data[iid].extend(sm.get_xavg(ind=0))
            else:
                for i in range(l):
                    sm = ScanDataModel(outdata[i, :])
                    data[iid].extend(sm.get_yavg(ind=iid - 1))

        return map(np.asarray, (data[idx], data[idy], data[idz]))

    @pyqtSlot()
    def on_plot_data(self):
        """Visulize final 3D data, based on selected X, Y and Z.
        """
        xdata, ydata, zdata = self.make_data()
        if self._plot3d_window is None:
            self._plot3d_window = Plot3dData(self)
        o = self._plot3d_window
        m = self.interp_method_cbb.currentText()
        nx = self.interp_nx_sbox.value()
        ny = self.interp_ny_sbox.value()
        o.set_interp(m, nx, ny)
        o.set_xdata(xdata)
        o.set_ydata(ydata)
        o.set_zdata(zdata)
        o.plot_data()
        o.show()
        self.add_attached_widget(o)

    def enable_post_processing_ctrls(self, enable):
        """Enable/disable widgets for post processing.
        """
        self.analysis_gbox.setEnabled(enable)
