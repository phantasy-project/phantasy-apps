#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from collections import OrderedDict
from functools import partial

import numpy as np
from PyQt5.QtCore import QEventLoop
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
from phantasy_ui import BaseAppForm
from phantasy_ui.widgets import DataAcquisitionThread as DAQT
from phantasy_ui.widgets import ElementSelectionWidget
from phantasy_ui.widgets import LatticeWidget

from .app_device_selection import DeviceSelectionWidget
from .app_save import SaveDataDialog
from .ui.ui_app import Ui_MainWindow
from .utils import ElementListModelDV as ElementListModel

DTYPE_LIST = ("BCM", "ND", "HMR", )

DEFAULT_MACHINE = 'FRIB'
DEFAULT_SEGMENT = 'LINAC'


class DeviceViewerWindow(BaseAppForm, Ui_MainWindow):

    # update
    data_updated = pyqtSignal(QVariant, QVariant, QVariant)
    # init
    data_initialized = pyqtSignal(QVariant, QVariant, QVariant)
    ## selected devices and fields, k: ename, v: list of fields
    #devicesChanged = pyqtSignal(dict)

    # segments updated, list of loaded segments
    segments_updated = pyqtSignal(list)

    xtklbls_changed = pyqtSignal(list)
    xtks_changed = pyqtSignal(list)

    def __init__(self, version):
        super(DeviceViewerWindow, self).__init__()

        # app version
        self._version = version

        # window title
        self.setWindowTitle("Devices Viewer")

        # set app properties
        self.setAppTitle("Devices Viewer")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Devices Viewer</h4>
            <p>This app is created to visualize the device readings of FRIB
            accelerator, including the diagnostic devices and optics settings,
            current version is {}.
            </p>
            <p>Copyright (C) 2019 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)
        self.postInitUi()

        #
        self._post_init()

        #
        self.show()
        self.preload_lattice(DEFAULT_MACHINE, DEFAULT_SEGMENT)

    def _post_init(self,):
        # bpms from TV
        self._bpms_dict = None
        self._icon_refresh = QIcon(QPixmap(":/icons/refresh.png"))
        self._icon_refresh_new = QIcon(QPixmap(":/icons/refresh1.png"))
        self.refresh_bpm_btn.setVisible(False)
        # lattice load window
        self._lattice_load_window = None
        # elem selection widget
        self._elem_sel_widget = None
        # pv elems sel widget
        self._pv_elem_sel_widget = None

        # lattice viewer
        self._enable_widgets(False)
        self._lv = None
        self.lv_view_btn.clicked.connect(self.on_show_latinfo)
        self.reload_lattice_btn.clicked.connect(self.on_reload_lattice)

        #
        # list of field names of selected elements
        self.__mp = None
        self._field_list = []
        # list of selected elems
        self._elems_list = []
        # data save
        self._data_save_dlg = None
        #
        self.data_updated.connect(self.matplotlibbarWidget.update_curve)
        self.data_initialized.connect(self.matplotlibbarWidget.reset_data)
        self.set_widgets_status("WAIT")

        # DAQ freq
        self._daq_stop = False
        self._daq_nshot = 1
        self._daqfreq = 1.0
        self.daqfreq_dSpinbox.valueChanged[float].connect(self.update_daqfreq)
        self.daq_nshot_sbox.valueChanged[int].connect(self.update_daq_nshot)
        self._viz_active_px = QPixmap(":/icons/active.png")
        self._viz_inactive_px = QPixmap(":/icons/inactive.png")
        self.daq_pb.setVisible(False)

        self.reset_figure_btn.clicked.disconnect(self.on_init_dataviz)
        # xdata opt
        self.id_as_x_rbtn.setChecked(False)
        self.pos_as_x_rbtn.setChecked(True)
        self._xdata_gauge = 'pos'

        # show with D#### or device name
        self._xtklbls_dnum = []   # init by reset
        self._xtklbls_dname = []  # init by reset
        self._xtks = []
        self._auto_rotate_deg_dname = 40
        self._auto_rotate_deg_dnum = 30
        self._auto_rotate_xtks = self.auto_rotate_chkbox.isChecked()
        self.auto_rotate_chkbox.toggled.connect(self.on_auto_rotate_xtks)

        self.xtks_changed.connect(self.matplotlibbarWidget.set_xticks)
        self.xtklbls_changed.connect(self.matplotlibbarWidget.set_xticklabels)

        # xylabels
        self._auto_lbls = self.auto_lbls_chkbox.isChecked()
        self.auto_lbls_chkbox.toggled.connect(self.on_auto_lbls)

        # annote
        self._show_annote = self.annote_height_chkbox.isChecked()

        # device selection
        self.choose_elems_btn.clicked.connect(self.on_choose_devices)
        self.choose_elems_pv_btn.clicked.connect(self.on_choose_devices_pv)
        self.select_all_elems_btn.clicked.connect(self.on_select_all_elems)
        self.inverse_selection_btn.clicked.connect(self.on_inverse_current_elem_selection)

        # field cbb
        self.field_cbb.currentTextChanged.connect(self.on_elem_field_changed)

        # reset figure
        # does not work with matlotlib 2.0.0
        # self.on_init_dataviz()
        self.reset_figure_btn.clicked.connect(self.on_init_dataviz)

    @pyqtSlot()
    def on_select_all_elems(self):
        try:
            model = self.devices_treeView.model()
            model.select_all_items()
        except AttributeError:
            QMessageBox.warning(self, "Element Selection",
                    "Selection error, Choose elements first.",
                    QMessageBox.Ok)

    @pyqtSlot()
    def on_inverse_current_elem_selection(self):
        try:
            model = self.devices_treeView.model()
            model.inverse_current_selection()
        except AttributeError:
            QMessageBox.warning(self, "Element Selection",
                    "Selection error, Choose elements first.",
                    QMessageBox.Ok)

    @pyqtSlot(float)
    def update_daqfreq(self, f):
        self._daqfreq = f

    @pyqtSlot(int)
    def update_daq_nshot(self, i):
        self._daq_nshot = i

    @pyqtSlot()
    def on_daq_start(self):
        """Start DAQ.
        """
        if self._elems_list == [] :
            QMessageBox.warning(self, "DAQ Warning",
                    "Cannot find loaded devices.", QMessageBox.Ok)
            return

        if self._daq_stop:
            self.set_widgets_status("STOP")
            return

        self._delt = 1.0 / self._daqfreq
        self.daq_th = DAQT(daq_func=self.daq_single, daq_seq=range(self._daq_nshot))
        self.daq_th.started.connect(partial(self.set_widgets_status, "START"))
        self.daq_th.progressUpdated.connect(self.on_update_daq_status)
        self.daq_th.resultsReady.connect(self.on_daq_results_ready)
        self.daq_th.finished.connect(self.on_daq_start)

        self.daq_th.start()

    @pyqtSlot()
    def on_daq_stop(self):
        """Stop DAQ.
        """
        self._daq_stop = True

    def __refresh_data(self):
        h = [getattr(e, f) for e, f in zip(self._elems_list, self._field_list)]
        if self._xdata_gauge == 'pos':
            s = [e.sb for e in self._elems_list]
        else: # ID as x
            s = list(range(len(h)))
        herr = [0] * len(h)
        self._xtks = s
        # only work with D####
        self._xtklbls_dnum = [e.name[-5:] for e in self._elems_list]
        self._xtklbls_dname = [e.name for e in self._elems_list]
        return s, h, herr

    @pyqtSlot()
    def on_init_dataviz(self):
        # initial plot (reset figure btn)
        s, h, herr = self.__refresh_data()
        if len(np.unique(s)) != len(s):
            self.pos_as_x_rbtn.setEnabled(False)
        self.data_initialized.emit(s, h, herr)
        # reset daq bit
        self._daq_stop = False
        # reset xtklbl
        self.reset_xtklbls()
        # viz cnt
        self._viz_cnt = 0
        self.viz_cnt_lbl.setText('0')
        if self._daq_nshot > 1:
            # daq pb
            self.daq_pb.setValue(0)
            self.daq_pb.setVisible(True)
        else:
            self.daq_pb.setVisible(False)

        # tmp solution
        from mpl4qt.widgets.mplconfig import MatplotlibConfigBarPanel
        MatplotlibConfigBarPanel(self.matplotlibbarWidget)
        self.annote_height_chkbox.toggled.emit(self.annote_height_chkbox.isChecked())
        self.on_auto_lbls(self._auto_lbls)
        #

    @pyqtSlot(bool)
    def on_apply_id_as_xdata(self, f):
        if f:
            self._xdata_gauge = 'id'
            self.reset_figure_btn.clicked.emit()

    @pyqtSlot(bool)
    def on_apply_pos_as_xdata(self, f):
        if f:
            self._xdata_gauge = 'pos'
            self.reset_figure_btn.clicked.emit()

    def set_widgets_status(self, status):
        olist1 = (self.reset_figure_btn, self.start_btn,
                  self.id_as_x_rbtn, self.pos_as_x_rbtn,
                  self.devices_treeView, self.capture_btn, )
        olist2 = (self.stop_btn, )
        if status != "START":
            [o.setEnabled(True) for o in olist1]
            [o.setEnabled(False) for o in olist2]
        else:
            [o.setEnabled(False) for o in olist1]
            [o.setEnabled(True) for o in olist2]

    @pyqtSlot(bool)
    def on_annote_height(self, f):
        o = self.matplotlibbarWidget
        self._show_annote = f
        if f:
            # annote height on top/bottom of bar
            o.on_annote_config_changed()
        else:
            if o._all_annotes is None:
                return
            # hide annotes
            [i.set_visible(False) for i in o._all_annotes]
        o.update_figure()

    @pyqtSlot()
    def onLoadLatticeAction(self):
        """Load lattice.
        """
        if self._lattice_load_window is None:
            self._lattice_load_window = LatticeWidget()
            self._lattice_load_window.latticeChanged.connect(self.update_lattice)
            self._lattice_load_window.latticeChanged.connect(self._lattice_load_window.close)
        self._lattice_load_window.show()
        # reset element selection widgets
        self._elem_sel_widget = None

    def preload_lattice(self, mach, segm):
        return self.__load_lattice(mach, segm)

    def __load_lattice(self, mach, segm):
        self.actionLoad_Lattice.triggered.emit()
        self._lattice_load_window.mach_cbb.setCurrentText(mach)
        self._lattice_load_window.seg_cbb.setCurrentText(segm)
        self._lattice_load_window.auto_monitor_chkbox.setChecked(False)
        loop = QEventLoop()
        self._lattice_load_window.latticeChanged.connect(loop.exit)
        self._lattice_load_window.load_btn.clicked.emit()
        loop.exec_()

    @pyqtSlot(QVariant)
    def update_lattice(self, o):
        self.__mp = o
        self.segments_updated.emit(self.__mp.lattice_names)
        self.update_lattice_info_lbls(o.last_machine_name, o.last_lattice_name)

    @pyqtSlot()
    def on_choose_devices_pv(self):
        # elements from PVs
        if self._pv_elem_sel_widget is None:
            self._pv_elem_sel_widget = DeviceSelectionWidget(self)
            self._pv_elem_sel_widget.pv_elems_selected.connect(self.on_update_elem_objs)
        self._pv_elem_sel_widget.show()

    @pyqtSlot()
    def on_choose_devices(self):
        if self.__mp is None:
            QMessageBox.warning(self, "Device Selection",
                    "Cannot find loaded lattice, try to load first, either by clicking Tools > Load Lattice or Ctrl+Shift+L.",
                    QMessageBox.Ok)
            return
        w = self._elem_sel_widget = ElementSelectionWidget(self,
                self.__mp, dtypes=DTYPE_LIST)
        w.elementsSelected.connect(self.on_update_elems)
        w.show()

    @pyqtSlot(list)
    def on_update_elem_objs(self, elem_objs):
        # CaElement objs from PVs
        tv = self.devices_treeView

        enames = [i.name for i in elem_objs]
        model = ElementListModel(tv, None, enames, elem_objs_list=elem_objs)
        # list of fields of selected element type
        model.fieldsSelected.connect(self.on_selected_fields_updated)
        model.set_model()

        m = tv.model()
        m.elementSelected.connect(self.on_elem_selection_updated)
        model.select_all_items()

    @pyqtSlot(list)
    def on_update_elems(self, enames):
        """Selected element names list updated.
        """
        tv = self.devices_treeView
        model = ElementListModel(tv, self.__mp, enames)
        # list of fields of selected element type
        model.fieldsSelected.connect(self.on_selected_fields_updated)
        model.set_model()

        m = tv.model()
        m.elementSelected.connect(self.on_elem_selection_updated)
        model.select_all_items()

    @pyqtSlot()
    def on_refresh_model(self):
        # refresh element list, DV from TV.
        if self._bpms_dict is None:
            return
        self.on_update_elems(self._bpms_dict)
        self.refresh_bpm_btn.setIcon(self._icon_refresh)


    @pyqtSlot(dict)
    def on_update_selected_items(self, elems_dict):
        # DV launched from TV, when device (BPM) selection is updated.
        self._bpms_dict = elems_dict
        self.refresh_bpm_btn.setIcon(self._icon_refresh_new)

    @pyqtSlot(OrderedDict)
    def on_elem_selection_updated(self, d):
        print("selected elems:", d)
        self._field_list = [f[0] for _, f in d.items()]
        self._elems_list = self.devices_treeView.model().get_elements("selected")
        #model = self.devices_treeView.model()
        #self.devicesChanged.emit(model._selected_elements)

    @pyqtSlot(list)
    def on_selected_fields_updated(self, fields):
        o = self.field_cbb
        o.clear()
        o.addItems(fields)
        if 'X' in fields:
            # BPM
            o.setCurrentText('X')
        elif 'TYP' in fields:
            # BCM
            o.setCurrentText('TYP')

    @pyqtSlot('QString')
    def on_elem_field_changed(self, s):
        try:
            model = self.devices_treeView.model()
            model.change_field(s)
        except AttributeError:
            QMessageBox.warning(self, "Change Field",
                    "Failed to change field.", QMessageBox.Ok)

    @pyqtSlot(QVariant)
    def on_daq_results_ready(self, res):
        #print("DAQ Results: ", res)
        self.data = data = np.array(res)
        h, herr = data.mean(axis=0), data.std(axis=0)

        if self._xdata_gauge == 'pos': # s-pos as x
            s = [e.sb for e in self._elems_list]
        else: # ID as x
            s = list(range(len(h)))

        self.data_updated.emit(s, h, herr)

        self.matplotlibbarWidget.clear_annote()
        self.annote_height_chkbox.toggled.emit(self._show_annote)

    def daq_single(self, iiter):
        # fetch data from all devices
        # daq_seq is range(shot number)
        x = np.zeros(len(self._elems_list))
        for i, (e, f) in enumerate(zip(self._elems_list, self._field_list)):
            x[i] = getattr(e, f)
        time.sleep(self._delt)
        return x

    def on_update_daq_status(self, f, s):
        # beat DAQ viz status
        if f == 1.0:
            px = self._viz_active_px
            self._viz_cnt += 1
            self.viz_cnt_lbl.setText(str(self._viz_cnt))
        else:
            px = self._viz_inactive_px
        self.daq_status_lbl.setPixmap(px)
        QTimer.singleShot(200,
                lambda:self.daq_status_lbl.setPixmap(self._viz_inactive_px))
        if self._daq_nshot > 1:
            self.daq_pb.setValue(f * 100)

    @pyqtSlot()
    def on_single_viz_update(self):
        # single viz update.
        if self._elems_list == [] :
            QMessageBox.warning(self, "DAQ Warning",
                    "Cannot find loaded devices.", QMessageBox.Ok)
            return

        self._delt = 1.0 / self._daqfreq
        self.daq_th = DAQT(daq_func=self.daq_single, daq_seq=range(self._daq_nshot))
        self.daq_th.started.connect(partial(self.set_widgets_status, "START"))
        self.daq_th.progressUpdated.connect(self.on_update_daq_status)
        self.daq_th.resultsReady.connect(self.on_daq_results_ready)
        self.daq_th.finished.connect(partial(self.set_widgets_status, "STOP"))
        self.daq_th.start()

    @pyqtSlot()
    def on_save_data(self):
        # save current vized data into file.
        if self._data_save_dlg is None:
            self._data_save_dlg = SaveDataDialog(self)
        self.segments_updated.connect(self._data_save_dlg.on_segments_updated)
        self._data_save_dlg.show()

    def get_mp(self):
        # get MachinePortal instance
        return self.__mp

    @pyqtSlot(bool)
    def on_show_dnum(self, f):
        if not f:
            return
        self.xtklbls_changed.emit(self._xtklbls_dnum)
        if self._xtks != []:
            self.xtks_changed.emit(self._xtks)
        self.on_auto_rotate_xtks(self._auto_rotate_xtks)
        self.on_auto_lbls(self._auto_lbls)

    @pyqtSlot(bool)
    def on_show_dname(self, f):
        if not f:
            return
        self.xtklbls_changed.emit(self._xtklbls_dname)
        if self._xtks != []:
            self.xtks_changed.emit(self._xtks)
        self.on_auto_rotate_xtks(self._auto_rotate_xtks)
        self.on_auto_lbls(self._auto_lbls)

    def reset_xtklbls(self):
        [o.toggled.emit(o.isChecked()) for o in
                (self.show_dnum_rbtn, self.show_dname_rbtn)]

    @pyqtSlot(bool)
    def on_auto_rotate_xtks(self, f):
        self._auto_rotate_xtks = f
        if f:
            if self.show_dnum_rbtn.isChecked():
                self.on_rotate_xtks(self._auto_rotate_deg_dnum)
            elif self.show_dname_rbtn.isChecked():
                self.on_rotate_xtks(self._auto_rotate_deg_dname)
            self.auto_rotate_dsbox.setValue(self.matplotlibbarWidget.getFigureXTicksAngle())

    @pyqtSlot(bool)
    def on_auto_lbls(self, f):
        self._auto_lbls = f
        if f:
            self._auto_xlbl()
            self._auto_ylbl()

    def _auto_xlbl(self):
        if self.show_dnum_rbtn.isChecked() or self.show_dname_rbtn.isChecked():
            xlbl = ''
        else:
            xlbl = 's [m]'
        self.matplotlibbarWidget.setFigureXlabel(xlbl)

    def _auto_ylbl(self):
        fld = self._field_list[0]
        ename = self._elems_list[0]
        ylbl = "Device readings for '{}' ({})".format(ename.family, fld)
        self.matplotlibbarWidget.setFigureYlabel(ylbl)

    @pyqtSlot(float)
    def on_rotate_xtks(self, deg):
        self.matplotlibbarWidget.setFigureXTicksAngle(deg)
        if self.show_dnum_rbtn.isChecked():
            self._auto_rotate_deg_dnum = deg
        elif self.show_dname_rbtn.isChecked():
            self._auto_rotate_deg_dname = deg

    def _enable_widgets(self, enabled):
        for w in (self.lv_lbl, self.lv_mach_lbl, self.lv_segm_lbl,
                  self.lv_view_btn, self.reload_lattice_btn):
            w.setEnabled(enabled)

    def update_lattice_info_lbls(self, mach, segm):
        self._enable_widgets(True)
        self.lv_mach_lbl.setText(mach)
        self.lv_segm_lbl.setText(segm)

    @pyqtSlot()
    def on_show_latinfo(self):
        machine = self.lv_mach_lbl.text()
        lattice = self.lv_segm_lbl.text()
        if machine == '' or lattice == '':
            return

        from phantasy_apps.lattice_viewer import LatticeViewerWindow
        from phantasy_apps.lattice_viewer import __version__
        from phantasy_apps.lattice_viewer import __title__

        if self._lv is None:
            self._lv = LatticeViewerWindow(__version__)
            self._lv.setWindowTitle("{} ({})".format(__title__,
                                                     self.getAppTitle()))
            self._lv._initialize_lattice_widget()
        lw = self._lv._lattice_load_window
        lw.mach_cbb.setCurrentText(machine)
        lw.seg_cbb.setCurrentText(lattice)
        lw.load_btn.clicked.emit()
        self._lv.show()

    @pyqtSlot()
    def on_reload_lattice(self):
        """Reload lattice.
        """
        self.actionLoad_Lattice.triggered.emit()
        self._lattice_load_window.load_btn.clicked.emit()

