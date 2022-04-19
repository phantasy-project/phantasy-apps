#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import time
from functools import partial
from getpass import getuser

import epics
import numpy as np
import pathlib
from PyQt5.QtCore import QEventLoop
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QWidget
from phantasy import CaField
from phantasy_ui import BaseAppForm
from phantasy_ui import random_string
from phantasy_ui import uptime
from phantasy_ui import delayed_exec
from phantasy_ui import get_open_filename
from phantasy_ui import get_save_filename
from phantasy_ui import printlog
from phantasy_ui.widgets import ElementWidget
from phantasy_ui.widgets import LatticeWidget
from phantasy_ui.widgets import ElementSelectDialog
from phantasy_apps.utils import apply_mplcurve_settings
from phantasy_apps.utils import current_datetime

from .app_array_set import ArraySetDialog
from .app_help import HelpDialog
from .app_monitors_view import MonitorsViewWidget
from .app_mps_config import MpsConfigWidget
from .app_points_view import PointsViewWidget
from .app_save import SaveDataDialog
from .app_udef_action import UserDefinedActionDialog
from .app_2d import TwoParamsScanWindow
from .app_plot_all import PlotAllWidget
from .data import ScanDataModel
from .scan import ScanTask
from .scan import ScanWorker
from .scan import load_task
from .ui.ui_app import Ui_MainWindow
from .utils import COLOR_DANGER, COLOR_INFO, COLOR_WARNING, COLOR_PRIMARY
from .utils import get_config

BOTTOM_TBTN_ICON_SIZE = 32
SMALL_TBTN_ICON_SIZE = 20

BOTTOM_TBTN_ICON_QSIZE = QSize(BOTTOM_TBTN_ICON_SIZE, BOTTOM_TBTN_ICON_SIZE)
SMALL_TBTN_ICON_QSIZE = QSize(SMALL_TBTN_ICON_SIZE, SMALL_TBTN_ICON_SIZE)

# MPS status
MPS_STATUS = ["Fault", "Disable", "Monitor", "Enable"]
MPS_ENABLE_STATUS = "Enable"
MPS_DISABLE_STATUS = "Disable"

# default MPS pv name
MPS_PV_DEFAULT = 'MPS_FPS:MSTR_N0001:MpsStatus'  # FRIB MPS
# MPS_PV_DEFAULT = 'VA:SVR:MpsStatus' # VA MPS

# machine/segment for preloading
MACH, SEGM = 'FRIB', 'LINAC'


class CorrelationVisualizerWindow(BaseAppForm, Ui_MainWindow):
    # scan log
    scanlogUpdated = pyqtSignal('QString')
    scanlogTextColor = pyqtSignal(QColor)

    # scan pb
    scanProgressUpdated = pyqtSignal(float)

    # scan plot curve w/ errorbar
    curveUpdated = pyqtSignal(QVariant, QVariant, QVariant, QVariant)

    # loaded lattice elements
    elementsTreeChanged = pyqtSignal(QVariant)

    # number of extra monitors
    extraMonitorsNumberChanged = pyqtSignal(int)

    # MPS connection is changed, only when MPS guardian is enabled.
    mpsConnectionChanged = pyqtSignal(bool)

    # MPS status is changed
    mpsStatusChanged = pyqtSignal('QString')

    # signal to trig PAUSE action
    pauseScan = pyqtSignal(bool)

    # segments updated, list of loaded segments
    segments_updated = pyqtSignal(list)

    # out data from scan task updated
    data_updated = pyqtSignal(QVariant)

    def __init__(self, version: str, machine: str, segment: str, config: str):
        super(CorrelationVisualizerWindow, self).__init__()

        # app version
        self._version = version

        # window title/icon
        self.setWindowTitle("Correlation Visualizer")

        # set app properties
        self.setAppTitle("Correlation Visualizer")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Correlation Visualizer</h4>
            <p>This app is created to visualize the correlation between
            selected parameters, current version is {}.
            </p>
            <p>Copyright (C) 2018 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        self._machine = "FRIB" if machine is None else machine
        self._segment = "LINAC" if segment is None else segment

        # UI
        self.setupUi(self)
        self.postInitUi()

        # update task buttons/groups from configuration file.
        self.init_task_pool(get_config(config))

        # daq ctrl btns
        self.start_btn.clicked.connect(self.on_click_start_btn)
        self.stop_btn.clicked.connect(self.on_click_stop_btn)
        self.retake_btn.clicked.connect(self.on_click_retake_btn)
        self.pause_btn.clicked.connect(self.on_click_pause_btn)

        # events
        self.niter_spinBox.valueChanged.connect(self.on_update_niter)
        self.nshot_spinBox.valueChanged.connect(self.on_update_nshot)
        self.waitsec_dSpinBox.valueChanged.connect(self.on_update_waitsec)
        self.t_wait_extra_dSpinBox.valueChanged.connect(self.on_update_extra_wait)
        self.scanrate_dSpinBox.valueChanged.connect(self.on_update_daqrate)
        self.tol_dSpinBox.valueChanged.connect(self.on_update_tol)
        # output scan data
        self.save_data_tbtn.clicked.connect(self.save_data)
        # auto xylabels
        self.auto_labels_tbtn.clicked.connect(self.on_auto_labels)
        # auto title
        self.auto_title_tbtn.clicked.connect(self.on_auto_title)
        # move to peak/valley
        self.moveto_tbtn.clicked.connect(self.on_moveto)
        # set btn: set alter_elem with the value vline pointing to
        self.set_tbtn.clicked.connect(self.on_set)
        # clear log btn
        self.clear_log_tbtn.clicked.connect(self.scan_log_textEdit.clear)
        # fs +
        self.inc_fontsize_tbtn.clicked.connect(lambda: self.update_logfontsize(mode="+"))
        # fs -
        self.dec_fontsize_tbtn.clicked.connect(lambda: self.update_logfontsize(mode="-"))

        # view selected points btn
        self.view_selected_pts_tbtn.clicked.connect(self.on_view_selected_points)

        # set alter array btn
        self.alter_array_btn.clicked.connect(self.on_set_alter_array)
        self._set_alter_array_dialogs = {}  # keys: alter element name

        # enable arbitary alter array input
        self.enable_arbitary_array_chkbox.toggled.connect(self.on_toggle_array)

        # signals & slots
        self.scanlogUpdated.connect(self.on_update_log)
        self.scanlogTextColor.connect(self.scan_log_textEdit.setTextColor)
        self.scanProgressUpdated.connect(self.on_update_pb)
        self.scan_pb.valueChanged.connect(self.pb_changed)
        self.curveUpdated.connect(self.scan_plot_widget.update_curve)
        # point selector
        self.scan_plot_widget.selectedIndicesUpdated.connect(self.on_select_points)

        # (new) unified button for setting alter element
        self.select_alter_elem_btn.clicked.connect(
            partial(self.on_select_elem, 'alter'))
        self._sel_elem_dialogs = {}  # keys: 'alter', 'monitor'

        # (new) main monitor
        self.select_monitor_elem_btn.clicked.connect(
            partial(self.on_select_elem, 'monitor'))

        # additional monitors
        self.select_more_monitor_elems_btn.clicked.connect(
            self.on_select_extra_elem)
        # list of tuple of 'ename fname, mode',
        # ElementWidget keeps in self.elem_widgets_dict by indexing
        self._extra_monitors = []
        self.show_extra_monitors_btn.clicked.connect(
            self.on_show_extra_monitors)
        # widget for monitors view
        self.init_attached_widget('monitors_viewer')

        # alter range
        self.lower_limit_lineEdit.textChanged.connect(self.set_alter_range)
        self.upper_limit_lineEdit.textChanged.connect(self.set_alter_range)

        # extra monitors counter
        self.extraMonitorsNumberChanged[int].connect(self.on_extra_monitors_number_changed)

        # inventory for selected elements
        # key: (ename, fname, mode), value: ElementWidget
        self.elem_widgets_dict = {}

        self._2d_mode = False

        # UI post_init
        self._post_init_ui()

        # scan worker
        self.scan_worker = None

        # index array for retake
        self._indices_for_retake = []
        # (x, y) coords when seleted
        self._indices_for_retake_points = []

        # init scan config
        self.init_scan_config()

        # q-scan window
        self.qs_window = None

        # achromat tuning window
        self.at_window = None

        # lattice viewer
        for w in (self.lv_lbl, self.lv_mach, self.lv_segm, self.lv_view):
            w.setVisible(False)
        self._lv = None
        self.lv_view.clicked.connect(self.on_show_latinfo)

        # 2dscan window
        self._2dscan_window = None

        # lattice-load window
        self.init_attached_widget('lattice_load_window')
        self._mp = None
        # preload machine/segment
        #self.pre_load_lattice(MACH, SEGM)

        # moveto flag, set True when moveto some point.
        self._moveto_flag = False

        # points selected viewer
        self.init_attached_widget('pts_viewer')

        # plot all widget
        self.init_attached_widget('plot_all_widget')

        # mps config widget
        self.mps_config_widget = None
        self._mps_pvname = MPS_PV_DEFAULT
        self.mps_pv = epics.PV(self._mps_pvname)
        # enable MPS guardian by default
        delayed_exec(lambda: self.actionMPS_guardian.setChecked(True), 1000.0)
        # self.actionMPS_guardian.setChecked(True)
        #
        self.pauseScan[bool].connect(self.on_pause_scan)

        # set alter action as default
        self.regular_alter_action_rbtn.setChecked(True)

        self.setAcceptDrops(True)

        # mpl settings
        delayed_exec(lambda: self.init_mpl_settings(), 500)

    @pyqtSlot(bool)
    def on_pause_scan(self, f):
        if f and self.pause_btn.isEnabled():
            self.pause_btn.setText('Resume')
            # pause action
            self.scanlogTextColor.emit(COLOR_DANGER)
            self.scanlogUpdated.emit("Scan is paused by MPS")
            self.scanlogTextColor.emit(COLOR_WARNING)
            self.scanlogUpdated.emit("Scan task is paused, click 'Resume' to continue")
            self.scan_worker.pause()
            QMessageBox.warning(self, "MPS Guardian Says",
                                "Scan is paused by MPS, click 'Resume' button to continue.",
                                QMessageBox.Ok)

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

    @pyqtSlot(QVariant, QVariant)
    def on_select_points(self, ind, pts):
        """*ind*: list of index numbers, *pts*: list of (x, y) coords.
        e.g. the orignal xarray is [5 4 3 2 1], selected ind is [1 2 4],
        then pts is [(xi,yi)], xi is x[1], x[2], x[4], i.e. 4, 3, 1, yi is
        the value at xi.
        """
        self.add_retake_indices(ind, pts)
        self.on_view_selected_points()

    def add_retake_indices(self, ind, pts):
        """Make index array for retake, if ind[i] is already selected,
        skip, if not add it into.
        """
        for i, idx in enumerate(ind):
            if idx in self._indices_for_retake:
                continue
            else:
                self._indices_for_retake.append(idx)
                self._indices_for_retake_points.append(pts[i])

    @pyqtSlot(int)
    def update_retake_indices_view(self, idx):
        """Update retake indices array, idx and points, and update points view.
        """
        self.remove_idx_from_retake_indices(idx)
        self.on_view_selected_points()

    def remove_idx_from_retake_indices(self, idx):
        """Remove *idx* from retake index array.
        """
        index_of_idx = self._indices_for_retake.index(idx)
        self._indices_for_retake.pop(index_of_idx)
        self._indices_for_retake_points.pop(index_of_idx)

    def clear_retake_indices(self):
        """Clear selected points for RETAKE to be empty list.
        """
        self._indices_for_retake = []
        self._indices_for_retake_points = []
        self.on_view_selected_points()

    @pyqtSlot(tuple)
    def on_selection_changed(self, selections):
        self._elem_selections = selections

    @pyqtSlot()
    def on_select_elem(self, mode='alter'):
        """Select element via PV or high-level element for alter-vars and
        monitor-vars.
        """
        if mode not in self._sel_elem_dialogs:
            dlg = ElementSelectDialog(self, mode, mp=self._mp)
            dlg.selection_changed.connect(self.on_selection_changed)
            self._sel_elem_dialogs[mode] = dlg
            self.elementsTreeChanged.connect(dlg.on_update_elem_tree)
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

            elem_btn = self._create_element_btn(elem_btn_lbl, new_sel_key)
            self._place_element_btn(elem_btn, mode)

            if mode == 'alter':
                self.scan_task.alter_element = sel_elem
                # initialize scan range
                x0 = self.scan_task.get_initial_setting()
                self.lower_limit_lineEdit.setText('{}'.format(x0))
                self.upper_limit_lineEdit.setText('{}'.format(x0))
            elif mode == 'monitor':
                self.scan_task.monitor_element = sel_elem

            # debug
            print("-" * 20)
            print(sel_elem, sel_elem_display)
            print(elem_btn_lbl)
            print("-" * 20)
            #

        elif r == QDialog.Rejected:
            # do not update alter element obj
            return

    @pyqtSlot()
    def on_select_extra_elem(self):
        """Select element as extra monitor(s).
        """
        dlg = ElementSelectDialog(self, 'extra', mp=self._mp)
        dlg.selection_changed.connect(self.on_selection_changed)
        r = dlg.exec_()
        if r == QDialog.Accepted:
            sel_elems, sel_elems_display, sel_fields = self._elem_selections
            new_monis = self._setup_extra_monitors(sel_elems_display, sel_elems)
            for moni in new_monis:
                self.scan_task.add_extra_monitor(moni)

            # show afterward by default
            if self.auto_show_extra_chkbox.isChecked():
                self.on_show_extra_monitors()

        elif r == QDialog.Rejected:
            return

    @pyqtSlot(int)
    def on_extra_monitors_number_changed(self, n):
        """Update the counter of total number of extra monitors.
        """
        self.extra_monitors_counter_lbl.setText("Monitors ({})".format(n))

    @pyqtSlot()
    def on_show_extra_monitors(self):
        """Show extra monitors.
        """
        # show all extra monitors of scan task
        data = [(name, self.elem_widgets_dict[name]) for name in self._extra_monitors]
        if self.monitors_viewer is None:
            self.monitors_viewer = MonitorsViewWidget(self, data)
        else:
            self.monitors_viewer.set_data(data)
        self.monitors_viewer.show()
        self.monitors_viewer.adjustSize()

    @pyqtSlot('QString')
    def update_extra_monitors(self, name):
        """Update extra monitors, after deletion.

        1. remove name from _extra_monitors
        2. remove item with the key of name from elem_widgets_dict
        3. remove item from scan_task
        4. update view
        """
        idx = self._extra_monitors.index(name)
        self._extra_monitors.remove(name)
        self.scan_task.del_extra_monitor(idx)
        self.elem_widgets_dict.pop(name)
        self.extraMonitorsNumberChanged.emit(len(self._extra_monitors))
        self.on_show_extra_monitors()

    @pyqtSlot()
    def on_show_elem_info(self, name, container):
        """Show element obj info in a popup elementWidget.

        Parameters
        ----------
        name : str
            Name key of Element.
        container : dict
            Dict of element widgets.
        """
        w = container[name]
        w.show()
        self.add_attached_widget(w)

    @pyqtSlot()
    def save_data(self):
        """save data.
        """
        if self.scan_plot_widget.get_all_data()[0].size == 0:
            return

        filename, ext = get_save_filename(self,
                caption="Save data to file",
                type_filter="JSON Files (*.json);;CSV Files (*.csv)")

        if filename is None:
            return
        self._save_data(filename, ext)

    def _save_data(self, filename, ext):
        if ext.upper() == 'JSON':
            self._save_data_as_json(filename)
        elif ext.upper() == 'CSV':
            self._save_data_as_array(filename)
        elif ext.upper() == 'H5':
            QMessageBox.warning(self, "", "TBI", QMessageBox.Ok)
            return
        QMessageBox.information(self, "", "Save data to {}".format(filename))

    def _save_data_as_json(self, filename):
        """Save scan data as json datasheet.
        """
        data_sheet = self.scan_task.to_datasheet()

        data_sheet['data'].update({'filepath': filename})
        # info
        data_sheet.update({'info': {}})
        data_sheet['info'].update({'user': getuser(),
                                   'app': self.getAppTitle(),
                                   'version': self.getAppVersion()})
        data_sheet['task'].update(
            {'array_mode': self.enable_arbitary_array_chkbox.isChecked()})
        if self._mp is not None:
            mp_conf = {'machine': self._mp.last_machine_name,
                       'segment': self._mp.last_lattice_name}
            data_sheet['task'].update(mp_conf)
        # save
        data_sheet.write(filename)
        # return flag to indicate success or fail.

    def _save_data_as_array(self, filename):
        """csv/txt"""
        sm = ScanDataModel(self.scan_task.scan_out_data)
        ynerr = []  # [yi, yi_err, ...], y0:x, y1:y
        for i in range(0, sm.shape[-1]):
            ynerr.append(sm.get_avg()[:, i])
            ynerr.append(sm.get_err()[:, i])

        header = 'App: Correlation Visualizer {}\n'.format(self._version)
        header += 'Data table saved on {}\n'.format(current_datetime())
        header += 'Scan job is done on {}\n'.format(current_datetime(self.scan_task.ts_stop))
        header += 'Columns ({}) definitions: standard error comes after average reading\n'.format(2 * sm.shape[-1])
        header += '<x> x_std <y> y_std <y1> y1_std ...\n'
        header += 'x: {}\ny: {}\n'.format(
            self.scan_task.alter_element.readback[0],
            self.scan_task.monitor_element.readback[0])
        header += 'yi is the i-th extra monitor\n'
        for i, elem in enumerate(self.scan_task.get_extra_monitors()):
            header += 'Extra monitor {}: {}\n'.format(i + 1, elem.readback[0])
        np.savetxt(filename, np.vstack(ynerr).T, header=header,
                   delimiter='\t')

    def init_mpl_settings(self):
        apply_mplcurve_settings(self.scan_plot_widget, 'correlation_visualizer',
                                filename='mpl_settings.json')

    def _post_init_ui(self):
        """post init ui
        """
        # hide File -> Save
        self.actionSave.setVisible(False)

        # toolbtns
        # save data
        self.save_data_tbtn.setIconSize(BOTTOM_TBTN_ICON_QSIZE)
        self.save_data_tbtn.setToolTip("Save data to file.")
        # auto labels
        self.auto_labels_tbtn.setIconSize(BOTTOM_TBTN_ICON_QSIZE)
        self.auto_labels_tbtn.setToolTip("Auto set X/Y labels.")
        # auto title
        self.auto_title_tbtn.setIconSize(BOTTOM_TBTN_ICON_QSIZE)
        self.auto_title_tbtn.setToolTip("Auto set figure title.")
        # move to
        self.moveto_tbtn.setIconSize(BOTTOM_TBTN_ICON_QSIZE)
        self.moveto_tbtn.setToolTip("Move cross-ruler to...")

        # auto scale toggle button
        self.autoscale_tbtn.setIconSize(BOTTOM_TBTN_ICON_QSIZE)
        self.autoscale_tbtn.setToolTip("Auto X/Y Scale.")
        self.autoscale_tbtn.setChecked(self.scan_plot_widget.getFigureAutoScale())

        #### deprecated moveto button
        menu = QMenu(self)
        # to peak
        peak_action = QAction('Peak', self)
        peak_action.triggered.connect(lambda: self.on_moveto(pos='peak'))

        # to valley
        valley_action = QAction('Valley', self)
        valley_action.triggered.connect(lambda: self.on_moveto(pos='valley'))

        # hide cross-ruler
        hide_action = QAction('Hide', self)
        hide_action.triggered.connect(lambda: self.on_moveto(pos='hide'))

        # set up menu
        menu.addAction(peak_action)
        menu.addAction(valley_action)
        menu.addSeparator()
        menu.addAction(hide_action)
        self.moveto_tbtn.setMenu(menu)
        # hide moveto btn
        self.moveto_tbtn.setVisible(False)
        ####

        # scan event log textedit
        # clear log btn
        self.clear_log_tbtn.setIconSize(SMALL_TBTN_ICON_QSIZE)
        self.clear_log_tbtn.setToolTip("Clear scan event log.")

        # fontsize + btn
        self.inc_fontsize_tbtn.setIconSize(SMALL_TBTN_ICON_QSIZE)
        self.inc_fontsize_tbtn.setToolTip("Increase Fontsize.")
        # fontsize - btn
        self.dec_fontsize_tbtn.setIconSize(SMALL_TBTN_ICON_QSIZE)
        self.dec_fontsize_tbtn.setToolTip("Decrease Fontsize.")

        # set btn
        self.set_tbtn.setIconSize(BOTTOM_TBTN_ICON_QSIZE)
        self.set_tbtn.setToolTip("Set with value cross-ruler pointed.")

        # view retake points btn
        self.view_selected_pts_tbtn.setIconSize(BOTTOM_TBTN_ICON_QSIZE)
        self.view_selected_pts_tbtn.setToolTip("Show selected points to retake.")

        menu_pts = QMenu(self)
        # show all selected points
        show_pts_act = QAction('Show', self)
        show_pts_act.triggered.connect(self.on_view_selected_points)
        # clear all points
        clear_pts_act = QAction('Clear', self)
        clear_pts_act.triggered.connect(self.clear_retake_indices)
        # set up menu_pts
        menu_pts.addAction(show_pts_act)
        menu_pts.addAction(clear_pts_act)
        self.view_selected_pts_tbtn.setMenu(menu_pts)

        # validators
        self.lower_limit_lineEdit.setValidator(QDoubleValidator())
        self.upper_limit_lineEdit.setValidator(QDoubleValidator())

        # btn's status
        self.set_btn_status(mode='init')

        # clear init curve data
        empty_arr = np.asarray([])
        self.curveUpdated.emit(empty_arr, empty_arr, empty_arr, empty_arr)

        # MPS guardian status
        mps_skipped_icon = QIcon(QPixmap(":/icons/mps_skipped.png"))
        mps_normal_icon = QIcon(QPixmap(":/icons/mps_normal.png"))
        mps_fault_icon = QIcon(QPixmap(":/icons/mps_fault.png"))
        mps_disable_icon = QIcon(QPixmap(":/icons/mps_disable.png"))
        mps_disconnected_icon = QIcon(QPixmap(":/icons/mps_disconnected.png"))
        mps_connected_icon = QIcon(QPixmap(":/icons/mps_connected.png"))
        self._mps_status_icons = {
            'skipped': mps_skipped_icon,
            'disconnected': mps_disconnected_icon,
            'connected': mps_connected_icon,
            'normal': mps_normal_icon,
            'fault': mps_fault_icon,
            'disable': mps_disable_icon,
        }

        # data save dlg
        self._data_save_dlg = None
        #

        # current acquired data
        self._current_arr = None

        # x-data & y-data cbbs
        self._idx, self._idy = 0, 1
        self.xdata_cbb.currentIndexChanged.connect(
            partial(self.on_update_data_index, 'x'))
        self.ydata_cbb.currentIndexChanged.connect(
            partial(self.on_update_data_index, 'y'))

        # xyaxis data expression
        self.xaxis_fn_chkbox.toggled.connect(
                lambda: self.on_update_data_index('x', self.xdata_cbb.currentIndex()))
        self.yaxis_fn_chkbox.toggled.connect(
                lambda: self.on_update_data_index('y', self.ydata_cbb.currentIndex()))
        self.xaxis_fn_lineEdit.textChanged.connect(
                lambda: self.on_update_data_index('x', self.xdata_cbb.currentIndex()))
        self.yaxis_fn_lineEdit.textChanged.connect(
                lambda: self.on_update_data_index('y', self.ydata_cbb.currentIndex()))
        # expanded udf expression
        self._xyaxis_fn_expanded_dict = {}
        # hint button
        self.xyaxis_fn_hint_btn.clicked.connect(self.on_xyaxis_fn_hint)

        #
        self.scan_pb.setVisible(False)

        # virtual diag?
        self.actionVirtual_diag.setChecked(True)

        # alter action, regular/advanced
        self._adv_alter_action_dlg = None
        self.regular_alter_action_rbtn.toggled.connect(
                partial(self.on_toggle_alter_action_rbtn, 'regular'))
        self.advanced_alter_action_rbtn.toggled.connect(
                partial(self.on_toggle_alter_action_rbtn, 'advanced'))
        self.advanced_alter_action_btn.clicked.connect(
                self.on_click_adv_alter_action_btn)

    def is_virtual_mode(self):
        # if enabled, treat devices virtually, e.g. VA.
        return self._enable_virtual_diag

    @pyqtSlot(int)
    def on_update_data_index(self, xoy, idx):
        setattr(self, '_id{}'.format(xoy), idx)
        # update xy labels
        self.on_auto_labels()
        # update data
        self.update_curve(self._current_arr)

    @pyqtSlot()
    def set_alter_range(self):
        """Set scan alter vars range.
        """
        srange_val1_str = self.lower_limit_lineEdit.text()
        srange_val2_str = self.upper_limit_lineEdit.text()
        try:
            sval1, sval2 = float(srange_val1_str), float(srange_val2_str)
        except ValueError:
            self.scanlogTextColor.emit(COLOR_DANGER)
            self.scanlogUpdated.emit("Empty input of scan range is invalid")
        else:
            self.scan_task.alter_start = sval1
            self.scan_task.alter_stop = sval2

    def init_scan_config(self):
        """Initialize scan configurations, including:
        1. Scan vars: the vars to be altered and
           the ones used as monitoring purpose.
        2. Scan range
        3. DAQ settings
        4. Scan data out settings
        """
        task_name = random_string(6)
        self.scan_task = ScanTask(task_name)
        # initialize ScanTask
        # daq
        self.set_scan_daq()
        # scan range
        self.set_alter_range()

    @pyqtSlot()
    def on_click_start_btn(self):
        """Start a new scan routine, initialize everything.
        """
        self.scan_pb.setVisible(True)
        self.scan_pb.setValue(0)
        # initialize configuration for scan routine
        # initialize scan out data
        self.scan_task.init_out_data()

        # check scan config
        if not self.scan_task.is_valid():
            QMessageBox.warning(self, "Scan Task Warning",
                                "Scan Task is not valid", QMessageBox.Ok)
            return

        # init x[y]data cbbs
        self.init_xydata_cbbs()

        #
        self.scanlogTextColor.emit(COLOR_PRIMARY)
        self.scanlogUpdated.emit("[START] button is pushed")
        self.scanlogTextColor.emit(COLOR_INFO)
        self.scanlogUpdated.emit(
            "Starting scan task: {}".format(self.scan_task.name))

        # set alter element to start point
        x_start = self.scan_task.alter_start
        self.scanlogUpdated.emit(
            "Setting alter element to {0:.3f}...".format(x_start))
        self.scan_task.alter_element.value = x_start
        self.scanlogUpdated.emit(
            "Alter element reaches {0:.3f}".format(x_start))

        # reset scan_plot_widget

        # start scan thread
        self.__start_scan_thread()

    def __retake_scan(self):
        """Retake at selected points.
        """
        self.scanlogTextColor.emit(COLOR_INFO)
        self.scanlogUpdated.emit("Retake is activated...")
        self.__start_scan_thread(index_array=self._indices_for_retake)

    def __resume_scan(self):
        """Start scan at where paused.
        """
        self.scanlogTextColor.emit(COLOR_INFO)
        self.scanlogUpdated.emit(
            "Resuming scan task: {}".format(self.scan_task.name))
        self.__start_scan_thread(self.scan_starting_index)

    def __start_scan_thread(self, starting_index=0, index_array=None):
        # scan worker thread
        self.thread = QThread()
        self.scan_worker = ScanWorker(self.scan_task,
                                      starting_index=starting_index,
                                      index_array=index_array, parent=self)
        self.scan_worker.moveToThread(self.thread)
        self.scan_worker.scanOneIterFinished.connect(self.on_one_iter_finished)
        self.scan_worker.scanAllDataReady.connect(self.on_scan_data_ready)
        self.scan_worker.scanFinished.connect(self.reset_alter_element)
        self.scan_worker.scanFinished.connect(lambda: self.set_btn_status(mode='stop'))
        self.scan_worker.scanFinished.connect(lambda: self.set_timestamp(type='stop'))
        self.scan_worker.scanFinished.connect(self.on_auto_title)
        self.scan_worker.scanFinished.connect(self.on_scan_finished)

        # scan is stopped by STOP btn
        self.scan_worker.scanStopped.connect(self.scan_worker.scanFinished)

        # scan is paused by PAUSE btn
        self.scan_worker.scanPaused.connect(lambda: self.set_btn_status(mode='pause'))
        self.scan_worker.scanPausedAtIndex.connect(self.on_keep_scan_index)
        #
        self.scan_worker.scanPaused.connect(self.thread.quit)

        # test
        self.scan_worker.scanFinished.connect(self.test_scan_finished)

        self.scan_worker.scanFinished.connect(partial(self.set_scan_ctrl_status, 'stop'))

        self.scan_worker.scanFinished.connect(self.thread.quit)
        self.scan_worker.scanFinished.connect(self.scan_worker.deleteLater)

        self.thread.finished.connect(self.thread.deleteLater)

        # test
        self.thread.started.connect(self.test_scan_started)

        self.thread.started.connect(lambda: self.set_btn_status(mode='start'))
        self.thread.started.connect(self.on_auto_labels)
        self.thread.started.connect(lambda: self.set_timestamp(type='start'))
        self.thread.started.connect(partial(self.set_scan_ctrl_status, 'start'))

        self.thread.started.connect(self.scan_worker.run)
        self.thread.start()

    @pyqtSlot()
    def on_scan_finished(self):
        if self._2d_mode:
            return
        QMessageBox.information(self, "Job is done",
                f"Scan task is done at {current_datetime(fmt='%Y-%m-%dT%H:%M:%S')}, it is good to save data now.",
                QMessageBox.Ok)

    @pyqtSlot(int, float, QVariant)
    def on_one_iter_finished(self, idx, x, arr):
        """Every one iteration finished, push event log
        """
        # current acquired data
        self._current_arr = arr

        niter = self.scan_task.alter_number
        self.scanlogTextColor.emit(COLOR_INFO)
        msg = 'Step:{0:>3d}/{1:d} is done at value: {2:>9.3g}'.format(
            idx + 1, niter, x)
        self.scanlogUpdated.emit(msg)
        self.scanProgressUpdated.emit((idx + 1.0) / niter)
        # update scan plot figure
        self.update_curve(arr)

    @pyqtSlot(QVariant)
    def on_scan_data_ready(self, arr):
        """Scan out data is ready.
        """
        self.data_updated.emit(arr)
        # print(arr)

    @pyqtSlot()
    def on_click_stop_btn(self):
        """Stop scan routine, can only start again.
        """
        def on_stop_at_index(index, value):
            QMessageBox.information(self, "Job is stopped",
                    f"Scan task is stopped at {value:g}, {index}th iteration, however data still could be saved and loaded.",
                    QMessageBox.Ok)

        if self.scan_worker is None:
            return
        if self.scan_worker.is_running():
            self.scanlogTextColor.emit(COLOR_PRIMARY)
            self.scanlogUpdated.emit("[STOP] button is pushed")
            self.scan_worker.stop()
            loop = QEventLoop()
            self.scan_worker.scanStoppedAt.connect(on_stop_at_index)
            self.scan_worker.scanStopped.connect(loop.exit)
            loop.exec_()
            self.scanlogTextColor.emit(COLOR_WARNING)
            self.scanlogUpdated.emit("Scan task is stopped.")
            self.scan_pb.setValue(100)

    @pyqtSlot()
    def set_btn_status(self, mode='start'):
        """Set control btns status for 'start' and 'stop'.
        """
        if mode == 'start':  # after push start button to start scan
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.pause_btn.setEnabled(True)
            self.retake_btn.setEnabled(True)
        elif mode == 'stop':  # scan is finished or stopped
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.pause_btn.setEnabled(False)
            self.retake_btn.setEnabled(True)
        elif mode == 'pause':  # scan is paused
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.retake_btn.setEnabled(False)
        elif mode == 'init':  # when app is started up
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.pause_btn.setEnabled(False)
            self.retake_btn.setEnabled(False)

    @pyqtSlot()
    def set_scan_ctrl_status(self, mode='start'):
        ctrls = (self.niter_spinBox, self.nshot_spinBox,
                 self.waitsec_dSpinBox, self.scanrate_dSpinBox,
                 self.tol_dSpinBox, self.t_wait_extra_dSpinBox)
        if mode=='start':
            # disable ctrls
            [o.setEnabled(False) for o in ctrls]
        else:
            # enable ctrls
            [o.setEnabled(True) for o in ctrls]

    @pyqtSlot()
    def on_click_pause_btn(self):
        """Pause scan routine.
        """
        if self.sender().text() == 'Pause':
            self.pause_btn.setText('Resume')
            # pause action
            self.scanlogTextColor.emit(COLOR_PRIMARY)
            self.scanlogUpdated.emit("[PAUSE] button is pushed")
            self.scanlogTextColor.emit(COLOR_WARNING)
            self.scanlogUpdated.emit("Scan task is paused, click 'Resume' to continue")
            self.scan_worker.pause()
        else:
            self.pause_btn.setText('Pause')
            self.scanlogTextColor.emit(COLOR_PRIMARY)
            self.scanlogUpdated.emit("[RESUME] button is pushed")
            # resume action
            self.__resume_scan()

    @pyqtSlot(int)
    def on_keep_scan_index(self, idx):
        """Keep the index at current scan value.
        """
        self.scan_starting_index = idx

    @pyqtSlot()
    def on_click_retake_btn(self):
        """Re-scan with selected points.
        """
        self.scanlogTextColor.emit(COLOR_PRIMARY)
        self.scanlogUpdated.emit("[RETAKE] button is pushed")
        self.__retake_scan()

    @pyqtSlot(int)
    def on_update_niter(self, i):
        # total number of scan points
        self.scan_task.alter_number = i

    @pyqtSlot(float)
    def on_update_waitsec(self, x):
        # max wait time in second (timeout) for each alter element ensure set.
        self.scan_task.t_wait = x

    @pyqtSlot(float)
    def on_update_extra_wait(self, x):
        # extra wait time in second after each alter element ensure set up.
        self.scan_task.t_wait_extra = x

    @pyqtSlot(int)
    def on_update_nshot(self, i):
        # total shot number for each scan iteration
        self.scan_task.shotnum = self.nshot_spinBox.value()

    @pyqtSlot(float)
    def on_update_daqrate(self, x):
        # scan DAQ rate, in Hz
        self.scan_task.daq_rate = x

    @pyqtSlot(float)
    def on_update_tol(self, x):
        # tolerance of delta(rd, set)
        self.scan_task.tolerance = x

    def set_scan_daq(self):
        for o in (self.niter_spinBox, self.nshot_spinBox,
                  self.waitsec_dSpinBox, self.scanrate_dSpinBox,
                  self.tol_dSpinBox):
            o.valueChanged.emit(o.value())

    def update_curve(self, arr):
        """Update scan plot with fresh data.
        """
        if arr is None:
            return
        sm = ScanDataModel(arr)
        idx, idy = self._idx, self._idy
        x, xerr = sm.get_xavg(ind=idx), sm.get_xerr(ind=idx)
        y, yerr = sm.get_yavg(ind=idy), sm.get_yerr(ind=idy)

        # check if xy arithmetic enabled
        if self.xaxis_fn_chkbox.isChecked() or self.yaxis_fn_chkbox.isChecked():
            xexp = self.xaxis_fn_lineEdit.text()
            yexp = self.yaxis_fn_lineEdit.text()
            _r = re.findall(r"([x,y])(\d+)", xexp + " " + yexp)
            if _r: # not empty list, [('x', '1'), ('y', '2'), ...]
                for xoy, i in _r:
                    k = f"{xoy}{i}"
                    idx = int(i) - 1
                    if xoy == 'x':
                        setattr(self, k, sm.get_xavg(ind=idx))
                        self._xyaxis_fn_expanded_dict[k] = self.xdata_cbb.itemText(idx).split('-')[-1]
                    else:
                        setattr(self, k, sm.get_yavg(ind=idx))
                        self._xyaxis_fn_expanded_dict[k] = self.ydata_cbb.itemText(idx).split('-')[-1]

        if self.xaxis_fn_chkbox.isChecked():
            sx = re.sub(r"([x,y])(\d+)", r"self.\1\2", self.xaxis_fn_lineEdit.text())
            try:
                _x = eval(sx)
            except:
                pass
            else:
                x = _x
                xlbl = re.sub(r"([x,y])(\d+)",
                        lambda m: self._xyaxis_fn_expanded_dict.get(m.group()),
                        self.xaxis_fn_lineEdit.text())
                self.scan_plot_widget.setFigureXlabel(xlbl)
        if self.yaxis_fn_chkbox.isChecked():
            sy = re.sub(r"([x,y])(\d+)", r"self.\1\2", self.yaxis_fn_lineEdit.text())
            try:
                _y = eval(sy)
            except:
                pass
            else:
                y = _y
                ylbl = re.sub(r"([x,y])(\d+)",
                        lambda m: self._xyaxis_fn_expanded_dict.get(m.group()),
                        self.yaxis_fn_lineEdit.text())
                self.scan_plot_widget.setFigureYlabel(ylbl)
        #
        self.curveUpdated.emit(x, y, xerr, yerr)

        # update all if plot_all button is checked
        if self.plot_all_widget is not None and self.plot_all_widget.is_show():
            self.plot_all_widget.update_curve(self._get_all_data())

    @pyqtSlot()
    def on_xyaxis_fn_hint(self):
        """Show the hint for udf of xyaxis.
        """
        text_list = ["<p>Available list of variable and its corresponding full name:</p>"]
        for i in range(self.xdata_cbb.count()):
            text_list.append(f'''<p><span style=" font-style:italic; color:#0055ff;">x{i+1}</span> : <span style=" color:#ff0000;">{self.xdata_cbb.itemText(i).split('-')[-1]}</span></p>''')
        text_list.append('<hr>')
        for i in range(self.ydata_cbb.count()):
            text_list.append(f'''<p><span style=" font-style:italic; color:#0055ff;">y{i+1}</span> : <span style=" color:#ff0000;">{self.ydata_cbb.itemText(i).split('-')[-1]}</span></p>''')
        text = ''.join(text_list)

        from .app_udef_xyaxis import UDFXYAxisWindow
        self._w_udf_xyaxis = UDFXYAxisWindow(self, text)
        self._w_udf_xyaxis.show()

    @pyqtSlot()
    def onQuadScanAction(self):
        """Show Quad scan data analysis app.
        """
        from phantasy_apps.quad_scan import QuadScanWindow
        from phantasy_apps.quad_scan import __version__

        if self.qs_window is None:
            try:
                self.qs_window = QuadScanWindow(__version__,
                                                self.scan_task.to_datasheet())
            except (AttributeError, TypeError):
                QMessageBox.warning(self, "",
                                    "Scan task is not complete, please try again later.",
                                    QMessageBox.Ok)
                return
        self.qs_window.show()

    @pyqtSlot()
    def onAchromatAnalysisAction(self):
        """Show achromat data analysis app.
        """
        from phantasy_apps.achromat_tuning import MyAppWindow
        from phantasy_apps.achromat_tuning import __version__
        from phantasy import create_tempfile

        tmpfile = create_tempfile(prefix="cv4at", suffix=".json")
        self._save_data_as_json(tmpfile)
        if self.at_window is None:
            self.at_window = MyAppWindow(version=__version__)
        self.at_window.load_file(tmpfile, "json")
        self.at_window.show()

    @pyqtSlot()
    def onLoadLatticeAction(self):
        """Load lattice.
        """
        if self.lattice_load_window is None:
            self.lattice_load_window = LatticeWidget()
            self.lattice_load_window.latticeChanged.connect(self.update_mp)
            self.lattice_load_window.latticeChanged.connect(
                    self.lattice_load_window.close)
        self.lattice_load_window.show()

    @pyqtSlot(QVariant)
    def update_mp(self, o):
        """Update MachinePortal instance, after reload lattice.
        """
        # reset sel_elem_dialogs
        self._sel_elem_dialogs = {}
        #
        self._mp = o
        self.elementsTreeChanged.emit(o)
        self.segments_updated.emit(o.lattice_names)
        #
        self.update_lattice_info_lbls(o.last_machine_name, o.last_lattice_name)

    def update_lattice_info_lbls(self, mach, segm):
        for w in (self.lv_lbl, self.lv_mach, self.lv_segm, self.lv_view):
            w.setVisible(True)
        self.lv_mach.setText(mach)
        self.lv_segm.setText(segm)

    @pyqtSlot(bool)
    def onEnableVirtualDiag(self, f):
        printlog("Enable Virtual Diag? {}".format(f))
        self._enable_virtual_diag = f

    @pyqtSlot(bool)
    def onEnableMPSGuardian(self, f):
        """Enable MPS guardian or not.
        """
        btn = self.mps_status_btn

        def on_mps_connected(pvname=None, conn=None, **kws):
            # MPS connection is changed
            self.mpsConnectionChanged.emit(conn)

        def on_mps_changed(**kws):
            # MPS status is changed
            v = kws.get('char_value')
            self.mpsStatusChanged.emit(v)

        if f:  # enable MPS guardian
            self.mps_pv.connection_callbacks = [on_mps_connected]
            self.mps_pv.add_callback(on_mps_changed)
            self.mpsConnectionChanged.connect(
                partial(self.on_update_mps_status, reason='conn'))
            self.mpsStatusChanged.connect(
                partial(self.on_update_mps_status, reason='val'))
            # if connected, set
            if self.mps_pv.connected:
                self.mpsConnectionChanged.emit(True)
                self.mpsStatusChanged.emit(self.mps_pv.get(as_string=True))
            else:
                self.mpsConnectionChanged.emit(False)
        else:  # not enable MPS guardian, MPS may be still running
            self.mpsConnectionChanged.disconnect()
            self.mpsStatusChanged.disconnect()
            btn.setIcon(self._mps_status_icons['skipped'])
            btn.setToolTip("MPS guardian is not enabled.")

    @pyqtSlot()
    def on2DScanAction(self):
        """Start up app with 2D scan feature.
        """
        msg = "Two-dimensional parameters scan is enabled."
        self.scanlogTextColor.emit(COLOR_DANGER)
        self.scanlogUpdated.emit(msg)
        self._2d_mode = True
        if self._2dscan_window is None:
            self._2dscan_window = TwoParamsScanWindow(self)
        self._2dscan_window.show()
        self.add_attached_widget(self._2dscan_window)

    @pyqtSlot()
    def onConfigDeviceProcessor(self):
        """Customize processing routine for device operation.
        """
        QMessageBox.warning(self, "Customize Device Processor",
                "To be implemented.", QMessageBox.Ok)

    @pyqtSlot()
    def on_update_mps_status(self, change, reason='conn'):
        """Update MPS status button icon when MPS guardian is enabled.
        *change* is bool when *reason* is 'conn', while str when
        *reason* is 'val'.
        """
        btn = self.mps_status_btn
        if reason == 'conn':
            if change:  # MPS is connected
                # print("set btn to connected icon")
                btn.setIcon(self._mps_status_icons['connected'])
                btn.setToolTip("MPS guardian is enabled, connection is established.")
            else:  # MPS is disconnected
                # print("set btn to disconnected icon")
                btn.setIcon(self._mps_status_icons['disconnected'])
                btn.setToolTip("MPS guardian is enabled, connection is lost.")
        else:  # val
            self._set_mps_status_btn(change)

    def _set_mps_status_btn(self, v):
        """Check MPS status readings, and set indicators.
        """
        btn = self.mps_status_btn
        if v == MPS_DISABLE_STATUS:
            btn.setIcon(self._mps_status_icons['disable'])
        elif v != MPS_ENABLE_STATUS:
            # print("set btn to fault icon")
            btn.setIcon(self._mps_status_icons['fault'])
            # pause scan
            self.pauseScan.emit(True)
        else:
            # print("set btn to normal icon")
            btn.setIcon(self._mps_status_icons['normal'])
        btn.setToolTip("MPS guardian is enabled, status is {}.".format(v))

    @pyqtSlot()
    def on_config_mps(self):
        """Config MPS: PV for the status.
        """
        if self.mps_config_widget is None:
            self.mps_config_widget = MpsConfigWidget(self)
        r = self.mps_config_widget.exec_()
        if r == QDialog.Accepted:
            self._mps_pvname = self.mps_config_widget.pvname
            self.mps_pv = epics.PV(self._mps_pvname)
            # re-check MPS guardian
            if self.actionMPS_guardian.isChecked():
                self.actionMPS_guardian.setChecked(False)
                delayed_exec(
                    lambda: self.actionMPS_guardian.setChecked(True), 2000.0)
        #                self.actionMPS_guardian.toggled.emit(True)
        else:
            pass

    @pyqtSlot()
    def onHelp(self):
        d = HelpDialog(self)
        d.resize(800, 600)
        d.exec_()

    @pyqtSlot()
    def on_auto_labels(self):
        """Auto fill out the xy labels of figure.
        """
        xlabel = self.get_auto_label('x')
        ylabel = self.get_auto_label('y')
        self.scan_plot_widget.setFigureXlabel(xlabel)
        self.scan_plot_widget.setFigureYlabel(ylabel)

    @pyqtSlot()
    def on_auto_title(self):
        """Auto fill out the title of figure.
        """
        if self.scan_worker is None:
            return

        if self.scan_worker.is_running():
            QMessageBox.warning(self, "",
                                "Scan task is not finished.",
                                QMessageBox.Ok)
            return

        ts_start = self.scan_task.ts_start
        ts_stop = self.scan_task.ts_stop
        title = "Completed at {ts}\nTime Elapsed: {t}".format(
            ts=current_datetime(ts_stop, fmt="%Y-%m-%dT%H:%M:%S"),
            t=uptime(ts_stop - ts_start))
        self.scan_plot_widget.setFigureTitle(title)

    @pyqtSlot()
    def on_moveto(self, pos='peak'):
        """Move cross-ruler to the `xm` where y reaches max.
        *Pos*: 'peak' (default), 'valley', 'hide'.
        """

        if pos == 'hide':  # hide cross-ruler
            self.scan_plot_widget.set_visible_hvlines(False)
            self._moveto_flag = False
            return

        if self.scan_plot_widget.get_all_data()[0].size == 0:
            return
        # if self.scan_worker is None or self.scan_worker.is_running():
        #     # scan is not completed, do nothing
        #     return

        sm = ScanDataModel(self.scan_task.scan_out_data)
        y = sm.get_yavg()
        y_min, y_max = y.min(), y.max()

        alter_array = self.scan_task.get_alter_array()
        if pos == 'peak':  # peak
            xm = alter_array[np.where(y == y_max)][0]
            ym = y_max
        elif pos == 'valley':  # valley
            xm = alter_array[np.where(y == y_min)][0]
            ym = y_min

        # draw/update cross-ruler
        # mc: mpl4qt.utils.COLOR_CYCLE[0]
        self.scan_plot_widget.draw_hvlines(xm, ym, pos, mc="#1F77B4")
        self.scan_plot_widget.set_visible_hvlines(True)
        # set moveto_flag
        self._moveto_flag = True

    @pyqtSlot()
    def on_set(self):
        """Set alter_elem where cross-ruler pointing to
        """
        mk_dict = self.scan_plot_widget._markers
        if not mk_dict:
            QMessageBox.warning(self, "",
                                "No value to set, use 'CTRL + M' to " +
                                "add a marker on the canvas, if multiple markers are added, " +
                                "the most recent one will be used to set the device.",
                                QMessageBox.Ok)
        else:
            mk_name = list(mk_dict.keys())[-1]
            _, _, _, _, (x0, y0) = mk_dict[mk_name]
            self.scanlogTextColor.emit(COLOR_INFO)
            self.scanlogUpdated.emit(f"Setting alter element to {x0:.3f}...")
            self.scan_task.alter_element.value = x0
            self.scanlogUpdated.emit(f"Alter element reaches {x0:.3f}.")
            QMessageBox.information(self, "",
                                    f"Set alter element to {x0:.3f} which is marked by {mk_name}.",
                                    QMessageBox.Ok)

    def reset_alter_element(self):
        x0 = self.scan_task.get_initial_setting()
        # restore alter elem
        self.scanlogTextColor.emit(COLOR_INFO)
        self.scanlogUpdated.emit(
            "Scan task is done, reset alter element...")
        self.scanlogUpdated.emit(
            "Setting alter element to {0:.3f}...".format(x0))
        # self.scan_task.alter_element.value = x0
        tol = self.scan_task.tolerance
        timeout = self.scan_task.t_wait
        extra_wait = self.scan_task.t_wait_extra
        print(f"--- reset element: value: {x0}, tol: {tol}, timeout: {timeout}, extra_wait: {extra_wait}")
        # crash set None issue // debug
        if x0 is not None:
            self.scan_task.alter_action(x0, alter_elem=self.scan_task.alter_element,
                                        tolerance=tol, timeout=timeout, extra_wait=extra_wait)
            self.scanlogUpdated.emit(
                "Alter element reaches {0:.3f}".format(x0))
        else:
            self.scanlogUpdated.emit(
                "Skip reset alter element to None.")
        # in case it is 'resume' while scan is done
        self.pause_btn.setText('Pause')

    @pyqtSlot()
    def set_timestamp(self, type='start'):
        """Update start timestamp of scan task.
        """
        printlog("Set timestamp for '{}'...".format(type))
        if type == 'start':
            self.scan_task.ts_start = time.time()
        elif type == 'stop':
            self.scan_task.ts_stop = time.time()

    @pyqtSlot('QString')
    def on_update_log(self, s):
        """Update scan event log.
        """
        msg = '[{0}] {1}'.format(current_datetime(fmt="%H:%M:%S"), s)
        self.scan_log_textEdit.append(msg)

    @pyqtSlot(float)
    def on_update_pb(self, x):
        self.scan_pb.setValue(x * 100)

    def pb_changed(self, i):
        if i == 100:
            QTimer.singleShot(500, lambda: self.scan_pb.setVisible(False))

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

    @pyqtSlot()
    def on_view_selected_points(self):
        """Show selected points to retake.
        """
        alter_array = self.scan_task.get_alter_array()
        sm = ScanDataModel(self.scan_task.scan_out_data)
        x_rd, y_rd, sy_rd = sm.get_xavg(), sm.get_yavg(), sm.get_yerr()

        data = []
        for idx, pts in zip(self._indices_for_retake, self._indices_for_retake_points):
            # index, alter_value, selected_point_x_pos, selected_point_y_pos, current_y_pos
            # current_y_pos is updated when clicking this button, if after retaking, this value should be updated)
            data.append((idx, alter_array[idx], pts[0], pts[1], (y_rd[idx], sy_rd[idx])))

        if self.pts_viewer is None:
            self.pts_viewer = PointsViewWidget(self, data)
        else:
            self.pts_viewer.set_data(data)
        self.pts_viewer.show()
        self.pts_viewer.adjustSize()

    @pyqtSlot()
    def update_logfontsize(self, mode="+"):
        """Grow/shrink scan eventlog fontsize.
        """
        font = self.scan_log_textEdit.currentFont()
        ps = font.pointSize()
        new_ps = ps + 1 if mode == '+' else ps - 1
        font.setPointSize(new_ps)
        self.scan_log_textEdit.setCurrentFont(font)

    @pyqtSlot()
    def on_save_data(self):
        # save current vized data into file.
        if self._data_save_dlg is None:
            self._data_save_dlg = SaveDataDialog(self)
        self.segments_updated.connect(self._data_save_dlg.on_segments_updated)
        self._data_save_dlg.show()

    def get_mp(self):
        # get MachinePortal instance
        return self._mp

    def init_xydata_cbbs(self):
        # initial x[y]data_cbb with selected elements.
        monitors = [self.scan_task.alter_element,
                    self.scan_task.monitor_element, ] + \
                   self.scan_task.get_extra_monitors()
        flds = [] # each element is a tuple of (id, fname)
        for _id, o in enumerate(monitors, 1):
            if isinstance(o, CaField):
                fld = '{0} [{1}]'.format(o.ename, o.name)
            else:
                fld = o.fname
            flds.append(f"{_id}-{fld}")

        for i, o in zip(('x', 'y'), (self.xdata_cbb, self.ydata_cbb)):
            o.currentIndexChanged.disconnect()
            o.clear()
            o.addItems(flds)
            o.currentIndexChanged.connect(
                partial(self.on_update_data_index, i))
        # inital
        self.xdata_cbb.setCurrentIndex(0)
        self.ydata_cbb.setCurrentIndex(1)
        self.xdata_cbb.currentIndexChanged.emit(0)
        self.ydata_cbb.currentIndexChanged.emit(1)

    def get_auto_label(self, xoy):
        # Return labels for xdata/ydata.
        current_text = getattr(self, '{}data_cbb'.format(xoy)).currentText()
        return current_text.split('-')[-1]

    @pyqtSlot()
    def on_save_task(self):
        # save scan task into file, even scan is done.
        filename, ext = get_save_filename(self,
                caption="Save Scan Task to file",
                type_filter="JSON Files (*.json)")

        if filename is None:
            return
        self._save_data(filename, 'JSON')

    @pyqtSlot()
    def on_load_task(self):
        # load scan task.
        filepath, ext = get_open_filename(self,
                type_filter="JSON Files (*.json)")
        self.load_task_from_file(filepath)

    def _clear_containers(self):
        #
        # Clear the mem space for different kinds of objs.
        #
        for d in (self.elem_widgets_dict, self._set_alter_array_dialogs, self._sel_elem_dialogs, ):
            d.clear()
        for l in (self._extra_monitors, self._indices_for_retake_points, self._indices_for_retake, ):
            l.clear()

    def load_task_from_file(self, filepath):
        if filepath is None:
            return
        # clear vars
        self._clear_containers()
        #
        #
        printlog("Loading task from {}.".format(filepath))
        scan_task = load_task(filepath, self._mp, self._machine, self._segment)
        if hasattr(scan_task, '_lattice'):
            self._mp = scan_task._lattice
        printlog("Loading task is done.")

        if scan_task.mode == '2D':
            printlog("Task to load is a 2D task.")
            self.load_2D_task(filepath)
            printlog("Loaded 2D configurations.")
        else:
            # initial UI widgets with loaded scan_task
            self.init_ui_with_scan_task(scan_task)

        # reset plot_all widget
        if self.plot_all_widget is not None:
            self.plot_all_widget.reset()

    def init_ui_with_scan_task(self, scan_task):
        # initial UI widgets with *scan_task*.
        #
        printlog("Starting to restore UI configurations.")

        # update scan_task obj
        self.scan_task = scan_task
        # print(scan_task)

        # set UI only
        self.enable_arbitary_array_chkbox.setChecked(True)

        # alter and monitor element
        self._setup_element_btn_from_scan_task(scan_task, 'alter')
        self._setup_element_btn_from_scan_task(scan_task, 'monitor')

        # alter action
        alter_mode = self.scan_task._alter_action_mode
        for o in (self.regular_alter_action_rbtn,
                  self.advanced_alter_action_rbtn):
            o.toggled.disconnect()
        self.advanced_alter_action_btn.setDisabled(alter_mode == 'regular')
        if alter_mode == 'regular':
            self.regular_alter_action_rbtn.setChecked(True)
        else:
            self.advanced_alter_action_rbtn.setChecked(True)
            self._adv_alter_action_dlg = UserDefinedActionDialog(self)
            self._adv_alter_action_dlg.alter_action_changed.connect(
                    self.on_update_alter_action)
            self._adv_alter_action_dlg.plainTextEdit.setPlainText(
                    self.scan_task.alter_action_code)
        self.regular_alter_action_rbtn.toggled.connect(
                partial(self.on_toggle_alter_action_rbtn, 'regular'))
        self.advanced_alter_action_rbtn.toggled.connect(
                partial(self.on_toggle_alter_action_rbtn, 'advanced'))

        # extra monitors
        extra_monis = scan_task.get_extra_monitors()
        extra_monis_dis = scan_task._extra_moni_display
        self._setup_extra_monitors(extra_monis_dis, extra_monis)

        # mp
        mp = scan_task.lattice
        if mp is not None:
            self.update_mp(mp)
        else:
            self._sel_elem_dialogs = {}

        # alter begin, end
        self.lower_limit_lineEdit.setText(str(scan_task.alter_start))
        self.upper_limit_lineEdit.setText(str(scan_task.alter_stop))
        # niter
        self.niter_spinBox.setValue(scan_task.alter_number)
        # nshot
        self.nshot_spinBox.setValue(scan_task.shotnum)
        # t_wait (timeout)
        self.waitsec_dSpinBox.setValue(scan_task.t_wait)
        # t_wait_extra
        self.t_wait_extra_dSpinBox.setValue(scan_task.t_wait_extra)
        # daq_rate
        self.scanrate_dSpinBox.setValue(scan_task.daq_rate)
        # tolerance
        self.tol_dSpinBox.setValue(scan_task.tolerance)

        # reset set array mode
        self._set_alter_array_dialogs = {}
        # array mode
        self.enable_arbitary_array_chkbox.setChecked(scan_task.array_mode)

        # init data plot
        printlog("Show 2D data visualization on curve widget.")
        self._current_arr = scan_task.scan_out_data
        self.init_xydata_cbbs()

        #
        printlog("UI restoration is done.")

    def _create_element_btn(self, btn_lbl, sel_key, widgets_dict=None):
        # create push button from selected element.
        # btn_lbl: label on the button
        # sel_key: string for indexing ElementWidget
        if widgets_dict is None:
            widgets_dict = self.elem_widgets_dict
        elem_btn = QPushButton(btn_lbl)
        elem_btn.setAutoDefault(True)
        elem_btn.clicked.connect(
            partial(self.on_show_elem_info, sel_key, widgets_dict))
        elem_btn.setCursor(Qt.PointingHandCursor)
        printlog("- Created element button with the label of '{}'.".format(btn_lbl))
        return elem_btn

    def _place_element_btn(self, elem_btn, mode, target=None):
        # place pushbutton for element widget
        # mode: alter, monitor
        if target is None:
            target = getattr(self, '{}_elem_lineEdit'.format(mode))
        hbox0 = target.findChild(QHBoxLayout)
        if hbox0 is None:
            hbox = QHBoxLayout()
            hbox.addWidget(elem_btn)
            hbox.setContentsMargins(0, 0, 0, 0)
            target.setLayout(hbox)
        else:
            hbox0.itemAt(0).widget().setParent(None)
            hbox0.addWidget(elem_btn)
            hbox0.update()
        tp = "Element to {}, click to see details.".format(mode)
        elem_btn.setToolTip(tp)
        printlog("- Placed element button with the label of '{}'.".format(elem_btn.text()))

    def _setup_element_btn_from_scan_task(self, scan_task, mode,
                                          widgets_dict=None, target=None):
        # set up element buttons for alter/monitor element(s)
        # with info from *scan_task*.
        elem = getattr(scan_task, '{}_element'.format(mode))
        elem_dis = getattr(scan_task, '_{}_element_display'.format(mode))
        elem_lbl = scan_task.print_element(elem)
        printlog("Setting up {} element...".format(mode.upper()))
        printlog("- {} Field: {}".format(mode.capitalize(), elem.ename))
        printlog("- Element: {}".format(elem_dis.ename))
        printlog("- Field Label: {}".format(elem_lbl))
        printlog("- Field Name: {}".format(elem.name))
        sel_key = ' '.join((elem_dis.ename, elem.name, mode))
        if widgets_dict is None:
            widgets_dict = self.elem_widgets_dict
        widgets_dict.setdefault(
            sel_key, ElementWidget(elem_dis, fields=elem.name))
        elem_btn = self._create_element_btn(elem_lbl, sel_key, widgets_dict)
        self._place_element_btn(elem_btn, mode, target)

    def _setup_extra_monitors(self, elems, flds):
        # elems: element for display
        # flds: element for scan task
        # return: list of fld objs to be added to scan task as extra monis.
        # note: add extra monis does not apply to load_task case.
        printlog("Setting up extra monitors...")

        sel_keys = []
        for elem, fld in zip(elems, flds):
            sel_keys.append(' '.join((elem.name, fld.name, 'extra')))

        new_monis = []
        for k, elem, fld in zip(sel_keys, elems, flds):
            if k not in self.elem_widgets_dict:
                printlog("- Add '{}' to element widget dict as key: '{}'.".format(
                         elem.name, k))
                self.elem_widgets_dict[k] = ElementWidget(elem, fields=fld.name)
            if k not in self._extra_monitors:
                printlog("- Add '{}' to extra monitors list.".format(k))
                self._extra_monitors.append(k)
                new_monis.append(fld)

        # update the counter for the total number of extra monitors
        self.extraMonitorsNumberChanged.emit(len(self._extra_monitors))

        return new_monis

    def load_2D_task(self, filepath):
        """Initial 2D scan task window with task file from *filepath*.

        Parameters
        ----------
        filepath : str
            Filepath of 2D task.
        """
        self.actionEnable_2D_Scan.triggered.emit()
        self._2dscan_window._load_task(filepath)

    def pre_load_lattice(self, mach, segm):
        """Preload machine and segment (timing issue?)
        """
        self.actionLoad_Lattice.triggered.emit()
        self.lattice_load_window.mach_cbb.setCurrentText(mach)
        self.lattice_load_window.seg_cbb.setCurrentText(segm)
        self.lattice_load_window.load_btn.clicked.emit()
        self.lattice_load_window.close()

    @pyqtSlot()
    def on_show_latinfo(self):
        machine = self.lv_mach.text()
        lattice = self.lv_segm.text()
        if machine == '' or lattice == '':
            return

        from phantasy_apps.lattice_viewer import LatticeViewerWindow
        from phantasy_apps.lattice_viewer import __version__
        from phantasy_apps.lattice_viewer import __title__

        if self._lv is None:
            self._lv = LatticeViewerWindow(__version__)
            self._lv.setWindowTitle("{} ({})".format(__title__, self.getAppTitle()))
            self._lv._initialize_lattice_widget()
        lw = self._lv._lattice_load_window
        lw.mach_cbb.setCurrentText(machine)
        lw.seg_cbb.setCurrentText(lattice)
        lw.load_btn.clicked.emit()
        self._lv.show()

    @pyqtSlot(bool)
    def on_toggle_alter_action_rbtn(self, mode, f):
        """Toggle alter action mode, 'regular' or 'advanced'.
        """
        if f and mode == 'regular':
            # reset alter action with the default one.
            self.scan_task.alter_action = None
            self.advanced_alter_action_btn.setEnabled(False)

        if f and mode == 'advanced':  # mode is advanced
            self.advanced_alter_action_btn.setEnabled(True)
            self.advanced_alter_action_btn.clicked.emit()

    @pyqtSlot(QVariant, 'QString')
    def on_update_alter_action(self, func_obj, func_str):
        """Update the function for setting alter element.
        """
        self.scan_task.alter_action = func_obj
        self.scan_task.alter_action_code = func_str

    @pyqtSlot()
    def on_click_adv_alter_action_btn(self):
        """User-defined alter action.
        """
        if self._adv_alter_action_dlg is None:
            self._adv_alter_action_dlg = UserDefinedActionDialog(self)
            self._adv_alter_action_dlg.alter_action_changed.connect(
                    self.on_update_alter_action)
        self._adv_alter_action_dlg.exec_()

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        path = e.mimeData().urls()[0].toLocalFile()
        self.load_task_from_file(path)

    # test slots
    def test_scan_started(self):
        printlog("Scan is started.")
        return
        print(self.scan_task)
        print("-" * 20)
        print("alter start : ", self.scan_task.alter_start)
        print("alter stop  : ", self.scan_task.alter_stop)
        print("alter number: ", self.scan_task.alter_number)
        print("shot number : ", self.scan_task.shotnum)
        print("alter array : ", self.scan_task.get_alter_array())
        print("alter elem  : ", self.scan_task.alter_element)
        print("monitor elem: ", self.scan_task.monitor_element)
        print("out data    : ", self.scan_task.scan_out_data)
        print("initial set : ", self.scan_task.get_initial_setting())
        print("ts_start    : ", self.scan_task.ts_start)
        print("ts_stop     : ", self.scan_task.ts_stop)
        print("-" * 20)
        print("\n")

    def test_scan_finished(self):
        printlog("Scan is done.")
        return
        print(self.scan_task)
        print("-" * 20)
        print("alter start : ", self.scan_task.alter_start)
        print("alter stop  : ", self.scan_task.alter_stop)
        print("alter number: ", self.scan_task.alter_number)
        print("shot number : ", self.scan_task.shotnum)
        print("alter array : ", self.scan_task.get_alter_array())
        print("alter elem  : ", self.scan_task.alter_element)
        print("monitor elem: ", self.scan_task.monitor_element)
        print("out data    : ", self.scan_task.scan_out_data)
        print("initial set : ", self.scan_task.get_initial_setting())
        print("ts_start    : ", self.scan_task.ts_start)
        print("ts_stop     : ", self.scan_task.ts_stop)
        print("-" * 20)
        print("\n")
        print("thread is running?", self.thread.isRunning())

    def init_task_pool(self, conf):
        # init ui controls for task pool from toml config obj.
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolBar.addWidget(spacer)
        for _, v in conf['TASK_BUTTONS'].items():
            btn_name = v.get('NAME', None)
            if btn_name is None:
                continue
            btn_tt = v.get('DESC', btn_name)
            btn = QToolButton()
            btn.setIcon(QIcon(QPixmap(":/icons/task-btn.png")))
            btn.setText(btn_name)
            btn.setToolTip(btn_tt)
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            btn.clicked.connect(partial(self.load_task_from_file, v['FILEPATH']))
            self.toolBar.addWidget(btn)
        for _, v in conf['TASK_GROUPS'].items():
            grp_name = v.get('NAME', None)
            if grp_name is None:
                continue
            grp_tt = v.get('DESC', grp_name)
            grp_dir = v.get('DIRPATH')
            btn = QToolButton()
            menu = QMenu()
            for f in pathlib.Path(grp_dir).glob("**/*.json"):
                act = QAction(QIcon(QPixmap(":/icons/task-btn.png")), f.stem, menu)
                act.triggered.connect(partial(self.load_task_from_file, f.as_posix()))
                menu.addAction(act)
            btn.setMenu(menu)
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            btn.setToolTip(grp_tt)
            btn.setText(grp_name)
            btn.setPopupMode(QToolButton.MenuButtonPopup)
            btn.setIcon(QIcon(QPixmap(":/icons/task-group.png")))
            self.toolBar.addWidget(btn)

    @pyqtSlot()
    def on_plot_all(self):
        """Plot and update all curves in one figure if *is_checked*.
        """
        data = self._get_all_data()
        if self.plot_all_widget is None:
            self.plot_all_widget = PlotAllWidget(self, data)
        else:
            self.plot_all_widget.update_curve(data)
        self.plot_all_widget.show()
        self.plot_all_widget._show_flag = True

    def _get_all_data(self):
        # prepare data array
        sm = ScanDataModel(self._current_arr)
        xlbl = self.xdata_cbb.itemText(self._idx)
        x, xerr = sm.get_xavg(ind=self._idx), sm.get_xerr(ind=self._idx)
        ynlines = [(xlbl, x, xerr)]
        # [(lbl, yi, yi_err), ...], y0:x, y1:y
        for i in range(0, sm.shape[-1]):
            lbl = self.xdata_cbb.itemText(i)
            if lbl == xlbl:
                continue
            ynlines.append((lbl, sm.get_avg()[:, i], sm.get_err()[:, i]))
        return ynlines
