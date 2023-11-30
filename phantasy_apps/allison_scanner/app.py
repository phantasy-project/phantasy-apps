#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
from datetime import datetime
from epics import caget, caput
from functools import partial
from getpass import getuser
import numpy as np

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QEventLoop
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QSizePolicy

from numpy import ndarray
from numpy.testing import assert_almost_equal
from phantasy_ui.templates import BaseAppForm
from phantasy_ui.widgets import ElementWidget
from phantasy_ui import printlog

from phantasy import Configuration
from phantasy import establish_pvs
from phantasy import pass_arg
from phantasy_ui import delayed_exec
from phantasy_ui import uptime
from phantasy_ui import get_open_filename
from phantasy_ui import get_save_filename
from phantasy_apps.correlation_visualizer.data import JSONDataSheet
from .device import Device
from .ui.ui_app import Ui_MainWindow
from .utils import find_dconf
from .utils import get_all_devices
from .utils import is_integer
from .data import reading_params, mask_array
from .data import Data
from .model import Model
from .plot import PlotWidget
from .plot_final import PlotResults
from .save import SaveDataDialog
from .settings_view import SettingsView
from .app_layout import LayoutForm
from .app_headinfo import HeadinfoForm

CMAP_FAVLIST = ('flag', 'jet', 'nipy_spectral', 'gist_earth',
                'viridis', 'Greys')

POS_VOLT_NAME_MAP = {'pb': 'pos_begin', 'pe': 'pos_end', 'ps': 'pos_step',
                     'vb': 'volt_begin', 've': 'volt_end', 'vs': 'volt_step'}

# red
CNT_NOT_INT_STY = """
    QLabel {
        background-color: #DC3545;
        color: white;
        border-radius: 3px;
    }
"""

# green
CNT_IS_INT_STY = """
    QLabel {
        background-color: #28A745;
        color: white;
        border-radius: 3px;
    }
"""

PX_SIZE = 24

EMS_NAME_MAP = {
    'ISRC1': 'FE_SCS1:EMS_D0739',
    'ISRC2': 'FE_SCS2:EMS_D0718'
}

# map from <sys>_<subsys> to ion source id
ION_SOURCE_NAME_MAP = {'FE_SCS1': 'ISRC1', 'FE_SCS2': 'ISRC2'}

HV_MAP = {'ISRC1': 'FE_SCS1:BEAM:HV_BOOK',
          'ISRC2': 'FE_SCS2:BEAM:HV_BOOK'}

_USERGUIDE_FILE = os.path.join(os.path.dirname(__file__),
    'docs/AllisonScanner_UserGuide.pdf')

DEFAULT_DATA_SAVE_DIR = "/files/shared/phyapps-operations/data/allison_scanner"

#
POS_OUT_LIMIT_STR = "300" # 300 mm guarantees the pos reaches outlimit


class AllisonScannerWindow(BaseAppForm, Ui_MainWindow):

    image_data_changed = pyqtSignal(ndarray)
    data_changed = pyqtSignal(ndarray)
    xdata_changed = pyqtSignal(ndarray)
    ydata_changed = pyqtSignal(ndarray)
    xlabel_changed = pyqtSignal('QString')
    ylabel_changed = pyqtSignal('QString')
    results_changed = pyqtSignal(dict)
    size_factor_changed = pyqtSignal(float)
    finished = pyqtSignal()
    title_changed = pyqtSignal('QString')
    # device ready to scan signal
    sigReadyScanChanged = pyqtSignal(bool)
    # orientation changed
    sigOrientationChanged = pyqtSignal('QString')
    # ems device changed
    sigDeviceChanged = pyqtSignal('QString')
    # online mode change
    sigOnlineModeChanged = pyqtSignal(bool)
    # data filepath for offline mode
    sigDataFilepathChanged = pyqtSignal('QString')

    def __init__(self, version, mode="Live"):
        super(AllisonScannerWindow, self).__init__()

        # app version
        self._version = version

        # window title/version
        self.setWindowTitle("Allison Scanner")

        # set app properties
        self.setAppTitle("Allison Scanner")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Allison Scanner</h4>
            <p>This app is created for the operation of allison-scanner
            devices, including the DAQ and post data analysis,
            current version is {}.
            </p>
            <p>Copyright (C) 2019-2020 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)
        self.postInitUi()

        self.image_data_changed.connect(self.matplotlibimageWidget.update_image)
        self.xdata_changed.connect(self.matplotlibimageWidget.setXData)
        self.ydata_changed.connect(self.matplotlibimageWidget.setYData)
        self.xlabel_changed.connect(self.matplotlibimageWidget.setFigureXlabel)
        self.ylabel_changed.connect(self.matplotlibimageWidget.setFigureYlabel)
        self.title_changed.connect(self.matplotlibimageWidget.setFigureTitle)

        self._device_mode = mode.capitalize()
        self._post_init()

    def get_default_font_config(self):
        """Initial font config.
        """
        default_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        default_font_size = default_font.pointSize()
        return default_font, default_font_size

    def _set_headline_info(self):
        """Create widget for headline info.

        # online/offline headline info
        # +-------------------------------+
        # | EMS  Device Name | On/Offline |
        # +-----------+------+------------+
        # | ISRC Name |  X/Y | [readfile] |
        # +-----------+------+------------+
        """
        self._headinfo_widget = HeadinfoForm(self, self._default_font_size)
        self.toolBar.insertWidget(self.actiononline_mode, self._headinfo_widget)
        self.sigDeviceChanged.connect(self._headinfo_widget.onDeviceChanged)
        self.sigOrientationChanged.connect(self._headinfo_widget.onOrientationChanged)
        self.sigOnlineModeChanged.connect(self._headinfo_widget.onOnlineModeChanged)
        self.sigDataFilepathChanged.connect(self._headinfo_widget.onDataFilepathChanged)

    def _post_init(self):
        # schematic layout form
        self._layout_form = None

        # get system font info
        self._default_font, self._default_font_size = self.get_default_font_config()

        # device ready to scan?
        self.sigReadyScanChanged.connect(self.onReadyScanChanged)
        # right align Online/Offline Model tool
        _spacer = QWidget()
        _spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolBar.insertWidget(self.actiononline_mode, _spacer)

        # headline info widget.
        self._set_headline_info()

        # online/offline mode switching
        self.actiononline_mode.toggled.connect(self.on_online_mode_changed)
        self.actiononline_mode.toggled.emit(self.actiononline_mode.isChecked())
        #
        self._user_guide_mitem = QAction("User Guide", self)
        self.menu_Help.insertAction(self.actionAbout, self._user_guide_mitem)
        self._user_guide_mitem.triggered.connect(self.onShowUserGuide)

        #
        self._live_widgets = (self.retract_btn, self.abort_btn,
                              self.auto_fill_beam_params_btn,
                              self.reset_itlk_btn)
        self.on_auto_fill_beam_params(self._device_mode)
        # st
        self._active_px = QPixmap(":/icons/status-green.png").scaled(PX_SIZE, PX_SIZE,
                Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._inactive_px = QPixmap(":/icons/status-gray.png").scaled(PX_SIZE, PX_SIZE,
                Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._in_px = QPixmap(":/icons/status-orange.png").scaled(PX_SIZE, PX_SIZE,
                Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._outlimit_px = QPixmap(":/icons/status-red.png").scaled(PX_SIZE, PX_SIZE,
                Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._enable_px = QPixmap(":/icons/status-green.png").scaled(PX_SIZE, PX_SIZE,
                Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._not_enable_px = QPixmap(":/icons/status-red.png").scaled(PX_SIZE, PX_SIZE,
                Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._itlk_px = QPixmap(":/icons/status-green.png").scaled(PX_SIZE, PX_SIZE,
                Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._not_itlk_px = QPixmap(":/icons/status-red.png").scaled(PX_SIZE, PX_SIZE,
                Qt.KeepAspectRatio, Qt.SmoothTransformation)
        #
        self._fetch_red_px = QPixmap(":/icons/fetch_red.png").scaled(PX_SIZE, PX_SIZE,
                Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._fetch_px = QPixmap(":/icons/fetch.png").scaled(PX_SIZE, PX_SIZE,
                Qt.KeepAspectRatio, Qt.SmoothTransformation)
        #
        self.installed_px = QPixmap(":/icons/installed.png").scaled(PX_SIZE, PX_SIZE,
                Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.not_installed_px = QPixmap(":/icons/not-installed.png").scaled(PX_SIZE, PX_SIZE,
                Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # conf
        self._dconf = self.get_device_config()

        # bias voltage
        self.live_biasVolt_lineEdit.setValidator(QDoubleValidator())
        self.set_biasVolt_lineEdit.setValidator(QDoubleValidator())
        self.set_biasVolt_btn.clicked.connect(self.on_set_biasVolt)

        # motor pos
        self.live_pos_lineEdit.setValidator(QDoubleValidator())
        self.set_pos_lineEdit.setValidator(QDoubleValidator())

        self.set_pos_btn.clicked.connect(self.on_move_pos)
        self.retract_btn.clicked.connect(self.on_retract)
        #
        self.enable_btn.clicked.connect(self.on_enable)
        self.reset_itlk_btn.clicked.connect(self.on_reset_interlock)

        # check adv ctrl by default
        # main vertical splitter
        self.main_vsplitter.setStretchFactor(0, 0)
        self.main_vsplitter.setStretchFactor(1, 1)
        self.adv_ctrl_chkbox.toggled.emit(False)
        self.main_vsplitter.setSizes([10, 5000])
        self.adv_ctrl_chkbox.setChecked(True)
        self.adv_ctrl_chkbox.toggled.emit(self.adv_ctrl_chkbox.isChecked())

        # orientation
        self._ems_orientation = "X"
        self.ems_orientation_cbb.currentTextChanged.connect(self.on_update_orientation)

        # model
        for o in (self.ion_charge_lineEdit, self.ion_mass_lineEdit,
                  self.ion_energy_lineEdit, ):
            o.setValidator(QDoubleValidator(0, 99999999, 6))
            o.textChanged.connect(self.on_update_model)
        ve = self.voltage_lineEdit
        ve.setValidator(QDoubleValidator())
        ve.textChanged.connect(self.on_v2d)

        # data
        self._data = None
        # bkgd noise
        self._intensity_clean_bkgd = None
        self._auto_bkgd_noise_filter = False
        # noise cor
        for o in (self.bkgd_noise_nelem_sbox, self.bkgd_noise_threshold_sbox,
                  self.factor_dsbox, self.noise_threshold_sbox):
            o.valueChanged.emit(o.value())

        # pos,volt,dt...
        self._attr_names = [
                '{}_{}'.format(u, v)
                for u in ('pos', 'volt')
                      for v in ('begin', 'end', 'step', 'settling_time')
        ]

        for s in self._attr_names:
            o = getattr(self, s + '_dsbox')
            o.valueChanged.connect(partial(self.on_update_config, s))

        #
        for o in self.findChildren(QLineEdit):
            o.textChanged.connect(self.highlight_text)

        #
        self._plot_window = None
        # auto analysis?
        self._auto_analysis = True
        self._results = None
        # auto push?
        self._auto_push_results = True
        self.actionAuto_Push_Results_to_PVs.setChecked(True)
        # save dlg
        self._data_save_dlg = None
        # loading mode (open data from file)
        self._last_loading = False

        # fav cmap cbb/chkbox
        self.cmap_fav_cbb.addItems(CMAP_FAVLIST)
        self.cmap_fav_cbb.currentTextChanged.connect(self.on_update_fav_cmap)

        # detail info
        self.ems_detail_btn.clicked.connect(self.on_show_ems)
        self._device_widget = None

        # init model, ion info
        for o in (self.ion_charge_lineEdit, self.ion_mass_lineEdit,
                  self.ion_name_lineEdit):
            o.textChanged.emit(o.text())

        # initial EMS devices
        self._initial_devices()

        # default config btn, menu --> history settings
        self._init_revert_config_btn()
        self._init_scan_settings()

        # Re-emit the selected EMS device
        delayed_exec(lambda: self.ems_names_cbb.currentTextChanged.emit(
                                self.ems_names_cbb.currentText()), 2000)

    def _wire_device_signals(self, ems: Device):
        # connect signals of Device for controls and viz
        # status in
        ems.status_in_changed.connect(self.onUpdateStatusIn)
        # status out
        ems.status_out_changed.connect(self.onUpdateStatusOut)
        # interlock ok
        ems.status_itlk_ok_changed.connect(self.onUpdateStatusInterlockOK)
        # pos readback
        ems.pos_read_changed.connect(self.onUpdatePosRead)
        # pos setpoint
        ems.pos_set_changed.connect(self.onUpdatePosSet)
        # enable status
        ems.status_enabled_changed.connect(self.onUpdateStatusEnabled)
        # bias voltage on status
        ems.bias_volt_on_changed.connect(self.onUpdateBiasVoltOn)
        # bias voltage readback
        ems.bias_volt_read_changed.connect(self.onUpdateBiasVoltRead)
        # bias voltage setpoint
        ems.bias_volt_set_changed.connect(self.onUpdateBiasVoltSet)

        # pos/volt scan range configs
        for (ii, jj) in ((i, j) for i in ('p', 'v') for j in ('b', 'e', 's')):
            n = f"{ii}{jj}"
            sig = getattr(ems, f'{n}_changed')
            sig.connect(partial(self.on_update_pos_volt_conf, n))

    def _init_revert_config_btn(self):
        # main action: revert to default config
        # dropdown: pop-up a list of saved history settings
        m = QMenu(self)
        settings_act = QAction("Settings List", self)
        settings_act.triggered.connect(self.show_settings_list)
        m.addAction(settings_act)
        self.default_config_btn.setMenu(m)

    def __check_device_ready_scan(self):
        # Check if device is ready to scan.
        msg = []
        _is_ready = True
        if self._ems_device.elem.BIAS_VOLT > self._ems_device.bias_volt_threshold:
            msg.append(f"Bias voltage > {self._ems_device.bias_volt_threshold}.")
            _is_ready = False
        if self.is_enabled_lbl.toolTip() != "Device is enabled":
            msg.append("Device is not Enabled.")
            _is_ready = False
        if self.is_itlk_lbl.toolTip() != "Device interlock is OK":
            msg.append("Device interlock is not OK.")
            _is_ready = False
        if self.is_bias_on_lbl.toolTip() != "Bias voltage is on":
            msg.append("Bias voltage is OFF.")
            _is_ready = False
        self.sigReadyScanChanged.emit(_is_ready)
        # post the reason why not ready to scan
        if msg:
            msg_str = ''
            for i in msg:
                msg_str += \
                    f'''<p><span style="font-size:{self._default_font_size + 2}pt;">&#9888; </span>
                        <span style="font-size:{self._default_font_size + 2}pt;color:#ff0000;">{i}</span></p>'''
            self.scan_status_info_full_lbl.setText(msg_str)

    @pyqtSlot(bool)
    def on_online_mode_changed(self, is_checked: bool):
        """If the online/offline mode check tool changed checkstate.

        - Checked: Online mode.
        - Unchecked: Offline mode.
        """
        self.sigOnlineModeChanged.emit(is_checked)
        self._online_mode = is_checked
        #
        self.ctrl_gbox.setEnabled(is_checked)
        if is_checked: # online
            tt = "Online mode is enabled, for working with devices."
            text = "Online"
            # set the EMS device ready for work.
            self.ems_names_cbb.currentTextChanged.emit(self.ems_names_cbb.currentText())
            self.auto_fill_beam_params_btn.clicked.emit()
        else: # offline
            tt = "Offline mode is enabled, for working with data files."
            text = "Offline"
        self.actiononline_mode.setToolTip(tt)
        self.actiononline_mode.setIconText(text)

    @pyqtSlot()
    def onShowUserGuide(self):
        """Open and read user guide.
        """
        QDesktopServices.openUrl(QUrl(_USERGUIDE_FILE))

    def _init_scan_settings(self):
        self._scan_settings_list = []
        self._scan_settings_list.append(self.build_default_scan_settings())

    @pyqtSlot(bool)
    def on_auto_push_results(self, enabled):
        # Auto push results to PVs after data-processing?
        self._auto_push_results = enabled

    @pyqtSlot()
    def show_settings_list(self):
        if hasattr(self, '_slw'):
            self._slw.close()
        self._slw = SettingsView(self._scan_settings_list)
        self._slw.show()
        m = self._slw.treeView.model()
        m.remove_settings.connect(self.on_delete_settings)
        m.apply_settings.connect(self.on_apply_settings)
        #
        self.add_attached_widget(self._slw)

    @pyqtSlot('QString')
    def on_update_fav_cmap(self, s: str):
        """Update the image color map.
        """
        self.matplotlibimageWidget.setColorMap(s)

    @pyqtSlot(float)
    def on_update_config(self, attr: str, x: float):
        # update attr of ems (1), live config (2) and _dconf (3)
        """Every time when the scan range is changed:
        - (1) Update the attributes of EMS Device
        - (2) Update the live scan config
        - (3) Update the Configuration object
        """
        # (1), (3)
        setattr(self._ems_device, attr, x)
        # (2)
        getattr(self._ems_device, f'set_{attr}')()
        # (3)
        self._dconf = self._ems_device.dconf
        # Update steps once begin/end is changed
        for i in ('pos', 'volt'):
            if attr in [f'{i}_{v}' for v in ('begin', 'end')]:
                o = getattr(self, f'{i}_step_dsbox')
                o.valueChanged.emit(o.value())
                printlog("Updated {}".format(f'{i}_step_dsbox'))
        cnt_list = self.update_cnts()
        self.update_time_cost(cnt_list)

    @pyqtSlot(bool)
    def onReadyScanChanged(self, is_ready: bool):
        """ Device is ready to scan?
        """
        if is_ready:
            self.scan_status_info_lbl.setText(
                    '<p>&#9786; <span style="color:#00aa00;">Ready to Scan</span></p>')
            self.scan_status_info_full_lbl.setText(
                f'''<p><span style="font-size:{self._default_font_size + 2}pt;">&#9786; </span>
                    <span style="font-size:{self._default_font_size + 2}pt;color:#00aa00;">Ready to Scan</span></p>''')
        else:
            self.scan_status_info_lbl.setText(
                    '<p>&#9888; <span style="color:#ff0000;">Not Ready to Scan</span></p>')

        [w.setEnabled(is_ready) for w in (self.run_btn, )]

    def sizeHint(self):
        return QSize(1440, 1200)

    def resizeEvent(self, e):
        BaseAppForm.resizeEvent(self, e)

    def update_time_cost(self, cnt_list: list = None):
        # update required time cost to complete the scan.
        # TODO: update with the generated data.
        if None in cnt_list:
            return
        n_pos, n_volt = cnt_list
        pos_step = self.pos_step_dsbox.value()
        dt_pos = self.pos_settling_time_dsbox.value()
        dt_volt = self.volt_settling_time_dsbox.value()
        a, b, c = 0.0053, 0.028, 3.84 # only good for EMS1
        t_sec = ((dt_volt + a) * n_volt + pos_step * b + c + dt_pos) * n_pos
        self.time_cost_lbl.setText(uptime(t_sec))

    def update_cnts(self):
        # update steps counter, must be an integer
        cnt_list = []
        for p in ('pos', 'volt'):
            o_b = getattr(self, f'{p}_begin_dsbox')
            o_e = getattr(self, f'{p}_end_dsbox')
            o_s = getattr(self, f'{p}_step_dsbox')
            x1 = o_b.value()
            x2 = o_e.value()
            dx = o_s.value()
            # cnt label
            o = getattr(self, f'{p}_steps_lbl')
            try:
                cnt = (x2 - x1) / dx + 1
            except ZeroDivisionError:
                cnt_is_int = False
                o.setText('[INF]')
                tt = "Invalid step size."
                cnt = None
            else:
                cnt_is_int = is_integer(cnt)
                o.setText('[{0:03d}]'.format(int(cnt)))
                tt = "Total steps: {0:.1f}".format(cnt)
            finally:
                if not cnt_is_int:
                    o.setStyleSheet(CNT_NOT_INT_STY)
                else:
                    o.setStyleSheet(CNT_IS_INT_STY)
                o.setToolTip(tt)
            cnt_list.append(cnt)
        return cnt_list

    @pyqtSlot()
    def on_set_biasVolt(self):
        """Set bias voltage with the new setpoint.
        """
        try:
            new_volt = float(self.set_biasVolt_lineEdit.text())
        except:
            QMessageBox.warning(self, "Set Bias Voltage", "Invalid bias voltage setpoint!", QMessageBox.Ok)
        else:
            print(f"Set Bias Voltage to {new_volt}.")
            self._ems_device.elem.BIAS_VOLT = new_volt

    @pyqtSlot('QString')
    def on_update_orientation(self, s: str):
        """Update X or Y:
        - Update the EMS device attributes
        - Update the connections for the device control and viz part
        """
        # post the message to the status bar area.
        self.statusInfoChanged.emit(
                "Be sure do retraction and reset interlock before switching.")
        #
        self.sigOrientationChanged.emit(s)
        #
        self._ems_orientation = s
        self._ems_device.xoy = s
        self._oid = oid = self._ems_device._id

        # set up monitors for the new device and orientation
        for _name, _ems_device in self._ems_device_map.items():
            printlog(f"Unmonitoring... {_name}")
            _ems_device.unmonitor()
            printlog(f"Monitoring... {self._ems_device.name}")
        self._ems_device.monitor()
        # publish data
        self._ems_device._post_monitor()

        if self._online_mode:
            # sync config
            self.sync_config()
        # update xylabels (Data Figure)
        self._update_xylabels()
        # update result keys (Twiss Parameters)
        self._update_result_keys(s)

    def get_device_config(self, path=None):
        """Return device config from *path*.
        """
        path = find_dconf() if path is None else path
        dconf = Configuration(path)
        return dconf

    @pyqtSlot('QString')
    def on_device_changed(self, s: str):
        # Change device by selecting the EMS name from the combobox (self.ems_names_cbb).
        #
        # reset the widget for element investigation
        self.sigDeviceChanged.emit(s)
        self._device_widget = None
        # switch EMS device
        self._current_device_name = s
        self._current_device_elem = self._all_devices_dict[s]
        if self._online_mode:
            # switch ion source, set the beam info widget
            isrc_name = ION_SOURCE_NAME_MAP.get(s[:7], 'ISRC1')
            self.beamSpeciesDisplayWidget.set_ion_source(isrc_name)
        # update the EMS device
        self.on_update_device()
        self.statusInfoChanged.emit("Selected device: {}".format(s))
        # trigger v2d
        self.on_update_model()

    def on_update_device(self):
        # update the EMS device.
        dev_name = self._current_device_name
        if dev_name not in self._ems_device_map:
            ems = Device(self._current_device_elem, self._ems_orientation, self._dconf)
            self._ems_device_map[dev_name] = ems
        else:
            ems = self._ems_device_map[dev_name]
        # wire signals for only once
        _sig_wired = self._ems_device_sig_wired_map.get(dev_name, False)
        if not _sig_wired:
            self._wire_device_signals(ems)
            self._ems_device_sig_wired_map[dev_name] = True
        #
        self._ems_device = ems
        self.ems_orientation_cbb.currentTextChanged.emit(self.ems_orientation_cbb.currentText())
        #
        self.__set_device_info_label(ems.info)
        #
        self.show_device_config()

        # initial/update model
        ionc = float(self.ion_charge_lineEdit.text())
        ionm = float(self.ion_mass_lineEdit.text())
        ione = float(self.ion_energy_lineEdit.text())
        self._model = Model(device=ems,
                            ion_charge=ionc, ion_mass=ionm, ion_energy=ione)

    def show_device_config(self):
        """Show current device config, use device.sync_params() to refresh
        config with the live data.
        """
        self.__show_device_config_static(self._ems_device)
        self.__show_device_config_dynamic(self._ems_device)

    def __show_device_config_static(self, ems: Device):
        # static config: e.g. geometry specs.
        self._layout_form = LayoutForm(ems, self)

    def __show_device_config_dynamic(self, ems: Device):
        # dynamic: predefined scan range read from the config file.
        #
        # disconnect the scan spinboxes
        for attr in self._attr_names:
            dsbox = getattr(self, f'{attr}_dsbox')
            dsbox.valueChanged.disconnect()

        # predefined scan range for position
        self.pos_begin_dsbox.setValue(ems.pos_begin)
        self.pos_end_dsbox.setValue(ems.pos_end)
        self.pos_step_dsbox.setValue(ems.pos_step)
        self.pos_settling_time_dsbox.setValue(ems.pos_settling_time)
        # predefined scan range for voltage
        self.volt_begin_dsbox.setValue(ems.volt_begin)
        self.volt_end_dsbox.setValue(ems.volt_end)
        self.volt_step_dsbox.setValue(ems.volt_step)
        self.volt_settling_time_dsbox.setValue(ems.volt_settling_time)

        # calculate/valid the step counter for each dimension
        cnt_list = self.update_cnts()
        # post the estimated time required to finish the scan
        self.update_time_cost(cnt_list)

        # reconnect the scan spinboxes
        for attr in self._attr_names:
            dsbox = getattr(self, f'{attr}_dsbox')
            dsbox.valueChanged.connect(partial(self.on_update_config, attr))

        # just set the button status as synced.
        self.set_fetch_config_btn(0, 0)

    @pyqtSlot()
    def sync_config(self):
        """Pull current device configuration from controls network, update
        on the UI.
        """
        self.post_log("Read live scan configurations...")
        self._ems_device.sync_params()
        self.post_log("Set scan configurations...")
        self.__show_device_config_dynamic(self._ems_device)
        self.clear_log()

    @pyqtSlot()
    def on_loadfrom_config(self):
        """Load configuration from a file.
        """
        filepath, ext = get_open_filename(self,
                                          type_filter="INI Files (*.ini)")
        if filepath is None:
            return

        try:
            dconf_copy = Configuration(self._dconf.config_path)
            self._dconf = Configuration(filepath)
        except:
            self._dconf = dconf_copy
            QMessageBox.warning(self, "Load Configuration",
                                "Failed to load configuration file from {}.".format(filepath),
                                QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Load Configuration",
                                    "Loaded configuration file from {}.".format(filepath),
                                    QMessageBox.Ok)
        finally:
            self.on_update_device()

        printlog("Load config from {}".format(filepath))

    @pyqtSlot()
    def on_saveas_config(self):
        """Save configuration to a file.
        """
        filepath, ext = get_save_filename(self,
                                          type_filter="INI Files (*.ini)")
        if filepath is None:
            return
        self.__save_config_to_file(filepath)
        printlog("Save config as {}".format(filepath))

    @pyqtSlot()
    def on_save_config(self):
        """Save configuration.
        """
        filepath = self._dconf.config_path
        self.__save_config_to_file(filepath)
        printlog("Save config to {}".format(filepath))

    def __save_config_to_file(self, filepath):
        try:
            self._ems_device.save_dconf(filepath)
        except:
            QMessageBox.warning(self, "Save Configuration",
                                "Failed to save configuration file to {}".format(filepath),
                                QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Save Configuration",
                                    "Saved configuration file to {}".format(filepath),
                                    QMessageBox.Ok)

    @pyqtSlot()
    def on_reload_config(self):
        """Reload configuration.
        """
        filepath = self._dconf.config_path

        self._dconf = Configuration(self._dconf.config_path)
        self.on_update_device()
        QMessageBox.information(self, "Reload Configuration",
                                "Reloaded configuration file from {}.".format(filepath),
                                QMessageBox.Ok)

        printlog("Reload config from {}".format(filepath))

    @pyqtSlot()
    def on_locate_config(self):
        """Locate (find and open) device configuration file path.
        """
        path = self._dconf.config_path
        QDesktopServices.openUrl(QUrl(path))

    @pyqtSlot()
    def on_run(self):
        self.sync_config()
        self._abort = False
        self._run()

    def _run(self):
        if self._current_device_name[:7] == "FE_SCS1":
            if not self._validate_conflicts():
                return

        if not self._validate_device():
            return

        # test if ready to move
        if not self.is_ready_to_move():
            QMessageBox.warning(self, "Starting Device",
                    "Device is busy.",
                    QMessageBox.Ok)
            return
        self._pos_reached_begin = False # test if motor is at begin
        self._ems_device.init_run()
        self._init_elapsed_timer()
        self._ems_device.data_changed.connect(self.on_update)
        self._ems_device.finished.connect(self.on_finished)
        self.title_changed.emit("")
        self.post_log("Start the scan...")
        self._ems_device.move(wait=False)
        self.post_log("Waiting for data...")
        self._elapsed_timer.start(1000)
        # reset
        self._pos_reached_begin = False

    def _init_elapsed_timer(self):
        # initialize elapsed timer.
        self.time_elapsed_lbl.setText('00:00:00')
        self._elapsed_timer = QTimer(self)
        self._time_elapsed = 0 # sec
        self._elapsed_timer.timeout.connect(self.on_update_elapsed_time)

    def on_update_elapsed_time(self):
        self._time_elapsed += 1
        self.time_elapsed_lbl.setText(uptime(self._time_elapsed))

    @pyqtSlot()
    def on_abort(self):
        self._ems_device.abort()
        self._abort = True
        try:
            self._elapsed_timer.stop()
        except:
            pass

    @pyqtSlot()
    def on_retract(self):
        # retract the motor to the outlimit
        self.set_pos_lineEdit.setText(POS_OUT_LIMIT_STR)
        delayed_exec(lambda: self.set_pos_btn.clicked.emit(), 1000)

    @pyqtSlot()
    def on_move_pos(self):
        """Move the motor to the pos defined by set_pos_lineEdit.
        """
        try:
            new_pos = float(self.set_pos_lineEdit.text())
        except:
            QMessageBox.warning(self, "Invalid position setpoint!", QMessageBox.Ok)
        else:
            print(f"Move position to {new_pos}.")
            self._ems_device.retract(new_pos)

    def _validate_conflicts(self):
        # check if any conflicts with other devices.
        try:
            self.post_log("Checking any device conflicts...")
            assert caget('FE_SCS1:FC_D0739:LMPOS_LTCH_DRV') == 0
        except AssertionError:
            r = QMessageBox.warning(self, "Device Confilicts",
                    "Faraday Cup (D0738) should be pulled out.",
                    QMessageBox.Yes | QMessageBox.Cancel)
            msg = "<span style='color:#ff0000'>Device conflicts... Not OK</span>"
            is_ready = False
        else:
            msg = "<span style='color:#00aa00'>Device conflicts... OK</span>"
            is_ready = True
        finally:
            self.post_log(msg)
            return is_ready

    def _validate_device(self):
        """Validate device scan range.
        """
        # scan ranges
        x1 = self._ems_device.get_pos_begin()
        x2 = self._ems_device.get_pos_end()
        dx = self._ems_device.get_pos_step()
        try:
            assert int((x2 - x1) / dx) * dx == x2 - x1
        except AssertionError:
            QMessageBox.warning(self, "Scan Range Warning",
                "Input scan range for position indicates Non-Integer total steps.",
                QMessageBox.Ok)
            return False
        #
        y1 = self._ems_device.get_volt_begin()
        y2 = self._ems_device.get_volt_end()
        dy = self._ems_device.get_volt_step()
        try:
            assert int((y2 - y1) / dy) * dy == y2 - y1
        except AssertionError:
            QMessageBox.warning(self, "Scan Range Warning",
                "Input scan range for voltage indicates Non-Integer total steps.",
                QMessageBox.Ok)
            return False
        #
        self._xdim = int((x2 - x1) / dx) + 1
        self._ydim = int((y2 - y1) / dy) + 1

        return True

    def is_ready_to_move(self):
        # if ok to move or not.
        return self._ems_device.check_status() == "IDLE"

    def on_update(self, data):
        if not self._pos_reached_begin:
            if not self._ems_device.is_pos_at_begin():
                return
            self._pos_reached_begin = True
        self.post_log("Receiving data...")
        data_pvname = self._ems_device.get_data_pvname()
        data = mask_array(data)
        try:
            m = data.reshape(self._ydim, self._xdim)
        except ValueError as err:
            printlog(f"Ignore data, since '{err}'")
            return
        m = np.flipud(m)
        self._current_array = m
        self.image_data_changed.emit(m)

    @pyqtSlot()
    def on_finished(self):
        _title = self.on_title_with_ts(self._ems_device.get_data_pv().timestamp)
        self.on_update(self._ems_device.get_data())
        self.post_log("Scan is done.")
        self._elapsed_timer.stop()
        self._ems_device.append_timelog(self._time_elapsed)
        # initial data
        self.on_initial_data()
        self.on_plot_raw_data()
        #
        if self._auto_analysis:
            self.title_changed.emit(_title + "\n" + "Automatic data processing ...")
            delayed_exec(lambda: self.title_changed.emit(_title), 2000)
            self._auto_process()
        #
        # self.finished.emit()
        #
        self._ems_device.data_changed.disconnect()
        self._ems_device.finished.disconnect()
        self.clear_log()

    def closeEvent(self, e):
        r = QMessageBox.information(self, "Exit Application",
                "Do you want to save the data?",
                QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.Yes:
            self.on_save_data()
        BaseAppForm.closeEvent(self, e)

    @pyqtSlot()
    def on_update_results(self):
        """Calculate Twiss parameters and update UI.
        """
        try:
            inten = self.matplotlibimageWidget.get_data()
            res = self._data.calculate_beam_parameters(inten)
        except:
            pass
        else:
            self._results = res
            self.update_results_ui(res)
            self.results_changed.emit(res)

    def on_initial_data(self):
        self._data = Data(model=self._model, array=self._current_array)

    def on_plot_raw_data(self):
        # plot raw data, before processing.
        self.xdata_changed.emit(self._data.x_grid)
        xlbl = "${}\,\mathrm{{[mm]}}$".format(self._ems_orientation.lower())
        self.xlabel_changed.emit(xlbl)
        self.image_data_changed.emit(self._data.intensity)
        self.raw_view_chkbox.toggled.emit(self.raw_view_chkbox.isChecked())

    @pyqtSlot()
    def on_update_model(self):
        try:
            ionc = float(self.ion_charge_lineEdit.text())
            ionm = float(self.ion_mass_lineEdit.text())
            ione = float(self.ion_energy_lineEdit.text())
        except ValueError:
            printlog("Invalid input of Q, A, Ek...")
            return
        try:
            assert hasattr(self, '_model') == True
        except AssertionError:
            printlog("Model is not ready.")
            return
        self._model.ion_charge = ionc
        self._model.ion_mass = ionm
        self._model.ion_energy = ione
        self.on_v2d(self.voltage_lineEdit.text())
        self.charge_mass_ratio_lineEdit.setText("{0:.3f}".format(ionc/ionm))

        # update data
        if self._data is not None:
            self._data.model = self._model
            self.refresh_main_view()

    def refresh_main_view(self):
        """Refresh the image view on the main window.
        """
        o = self.raw_view_chkbox
        o.toggled.emit(o.isChecked())

    @pyqtSlot('QString')
    def on_v2d(self, s):
        try:
            v = float(s)
            d = self._model.voltage_to_divergence(v)[1] * 1000
            out = "{0:.3f}".format(d)
        except:
            out = ""
        finally:
            self.divergence_lineEdit.setText(out)

    @pyqtSlot()
    def on_open_data(self):
        # Open data from a JSON data file.
        filepath, ext = get_open_filename(self,
                                          cdir=DEFAULT_DATA_SAVE_DIR,
                                          type_filter="JSON Files (*.json)")
        if filepath is None:
            return

        # activate offline mode for working file only,
        # activate online mode to work with device online.
        self.actiononline_mode.setChecked(False)
        #
        self.on_add_current_config(show=False)
        try:
            # UI config
            # ion species and model
            ion_name, ion_charge, ion_mass, ion_energy, \
                bkgd_noise_nelem, bkgd_noise_nsigma, \
                ellipse_sf, noise_threshold, \
                xoy, pos_scan_conf, volt_scan_conf, \
                note, isrc_id = reading_params(filepath)
            #
            self._last_loading = True
            self._loading_note = note
            self._loading_filepath = filepath
            #
            self.ion_name_lineEdit.setText(ion_name)
            self.ion_charge_lineEdit.setText(ion_charge)
            self.ion_mass_lineEdit.setText(ion_mass)
            self.ion_energy_lineEdit.setText(ion_energy)

            # processing params
            self.bkgd_noise_nelem_sbox.setValue(int(bkgd_noise_nelem))
            self.bkgd_noise_threshold_sbox.setValue(int(bkgd_noise_nsigma))
            self.factor_dsbox.setValue(float(ellipse_sf))
            self.noise_threshold_sbox.setValue(float(noise_threshold))

            # set up device name and orientation
            self.ems_names_cbb.setCurrentText(EMS_NAME_MAP[isrc_id])
            self.ems_orientation_cbb.setCurrentText(xoy.upper())
            # post the read scan ranges read
            pb, pe, ps = pos_scan_conf['begin'], pos_scan_conf['end'], pos_scan_conf['step']
            vb, ve, vs = volt_scan_conf['begin'], volt_scan_conf['end'], volt_scan_conf['step']
            self.pos_begin_dsbox.setValue(pb)
            self.pos_end_dsbox.setValue(pe)
            self.pos_step_dsbox.setValue(ps)
            self.volt_begin_dsbox.setValue(vb)
            self.volt_end_dsbox.setValue(ve)
            self.volt_step_dsbox.setValue(vs)

            # data
            data = self._data = Data(self._model, file=filepath)
        except KeyError:
            QMessageBox.warning(self, "Open Data", "Failed to open data.",
                    QMessageBox.Ok)
            return
        else:
            # show raw_data
            self.on_plot_raw_data()
            #
            if self._auto_analysis:
                self._auto_process()

            # post the data file path
            self.sigDataFilepathChanged.emit(filepath)

    def _update_bkgd_noise(self):
        if self._data is None:
            return
        try:
            inten1, bkgd_noise = self._data.filter_initial_background_noise(
                               n_elements=self._bkgd_noise_nelem,
                               threshold=self._bkgd_noise_nsigma)
        except (IndexError, ValueError):
            pass
        else:
            inten1 = mask_array(inten1)
            self.plot_noise(self.bkgd_noise_plot, bkgd_noise,
                                 self._bkgd_noise_nsigma)
            if self._auto_bkgd_noise_filter:
                self.image_data_changed.emit(inten1)
                self.data_changed.emit(inten1)
            return inten1

    @pyqtSlot(int)
    def on_update_nsampling(self, i):
        # bkgd noise nelem.
        self._bkgd_noise_nelem = i
        self._intensity_clean_bkgd = self._update_bkgd_noise()

    @pyqtSlot(int)
    def on_update_threshold0(self, i):
        self._bkgd_noise_nsigma = i
        self._intensity_clean_bkgd = self._update_bkgd_noise()

    def plot_noise(self, o, m, n):
        m = mask_array(m)
        ax = o.axes
        ax.clear()
        m = m.flatten()
        avg = np.nanmean(m)
        std = np.nanstd(m)
        ax.plot(m, color='b')
        ax.axhline(avg, ls='--', color='r')
        ax.axhline(avg + n * std, ls='--', color='m')
        t = r'$\mathrm{{Average}}: {0:.3g}, \sigma: {1:.3g}, \mathrm{{threshold}}: {2:.3g}$'.format(
                avg, std, avg + n * std)
        ax.set_xlabel(t)
        o.update_figure()

    @pyqtSlot(bool)
    def on_enable_raw_view(self, f):
        if f: # show pos, volt, intensity
            try:
                self.ydata_changed.emit(self._data.volt_grid)
            except:
                printlog("volt data is not ready..")
            self.ylabel_changed.emit("$\mathrm{Voltage}\,\mathrm{[V]}$")
        else: # show pos, angle, intensity
            try:
                self.ydata_changed.emit(self._data.xp_grid)
            except:
                printlog("xp data is not ready..")
            self.ylabel_changed.emit("${}'\,\mathrm{{[mrad]}}$".format(
                                     self._ems_orientation.lower()))

    def update_results_ui(self, res):
        ks = ('x_cen', 'xp_cen', 'x_rms', 'xp_rms',
              'alpha_x', 'beta_x', 'gamma_x', 'emit_x', 'emitn_x', )
        u = self._ems_device.xoy.lower()
        for k in ks:
            o = getattr(self, k + '_lineEdit')
            v = res.get(k.replace('x', u))
            o.setText("{0:.4f}".format(v))

    def _update_result_keys(self, s):
        u = s.lower()
        o = (self.x_cen_lbl, self.xp_cen_lbl,
             self.x_rms_lbl, self.xp_rms_lbl,
             self.alpha_x_lbl, self.beta_x_lbl, self.gamma_x_lbl,
             self.emit_x_lbl, self.emitn_x_lbl)
        v = ["<html>{}<sub>{}</sub></html>".format(i, j) for (i, j) in
                zip((u, u + "'", '&sigma;', '&sigma;', '&alpha;',
                    '&beta;', '&gamma;', '&epsilon;', '&epsilon;'),
                    (0, 0, u, u + "'", u, u, u, u, u + '<sup>n</sup>',))]
        for (i, j) in zip(o, v):
            i.setText(j)

    def _initial_devices(self):
        # store all ems device: {name: Device, ...}
        self._ems_device_map = {}

        # have signals been wired for each EMS device?
        # establish Device signals for device controls for only once
        self._ems_device_sig_wired_map = {}
        #
        all_devices_dict = get_all_devices("FRIB", "EMS", "EMS")
        self._all_devices_dict = all_devices_dict
        self.ems_names_cbb.addItems(all_devices_dict)
        self.ems_names_cbb.currentTextChanged.connect(self.on_device_changed)
        #
        self.ems_names_cbb.currentTextChanged.emit(
                self.ems_names_cbb.currentText())
        #
        self.ems_orientation_cbb.currentTextChanged.emit(
                self.ems_orientation_cbb.currentText())

    @pyqtSlot(bool)
    def on_enable_auto_filter_bkgd_noise(self, f):
        self._auto_bkgd_noise_filter = f
        if f:
            inten = self._update_bkgd_noise()
            if inten is None:
                self.sender().setChecked(False)
                return
            else:
                self._intensity_clean_bkgd = inten
                self.image_data_changed.emit(self._intensity_clean_bkgd)
                self.data_changed.emit(self._intensity_clean_bkgd)

    @pyqtSlot()
    def on_plot_region(self):
        # tag noise/signal pts.
        m = self.matplotlibimageWidget.get_data()
        if self._plot_window is None:
            self._plot_window = PlotWidget(self)
            self.data_changed.connect(self._plot_window.data_changed)
            self._plot_window.auto_boundary_chkbox.toggled.emit(
                    self._plot_window.auto_boundary_chkbox.isChecked())
            self._plot_window.setWindowTitle("ROI for Noise Correction")
        self._plot_window.plot()
        self._plot_window.show()
        #
        self.add_attached_widget(self._plot_window)

    @pyqtSlot()
    def on_apply_noise_correction(self):
        m, _ = self._data.noise_correction(self._noise_signal_arr,
                threshold_sigma=self._noise_threshold)
        self.image_data_changed.emit(m)

    @pyqtSlot(float)
    def on_update_noise_threshold(self, x):
        self._noise_threshold = x
        if self._data is None:
            return
        try:
            _, noise_arr = self._data.noise_correction(self._noise_signal_arr,
                threshold_sigma=x)
        except:
            QMessageBox.warning(self, "", "Noise estimation is not ready.",
                    QMessageBox.Ok)
            return
        else:
            self.plot_noise(self.noise_plot, noise_arr, x)

    @pyqtSlot(float)
    def on_update_ellipse_size_factor(self, x):
        self._ellipse_sf = x
        self.size_factor_changed.emit(x)
        # noise th
        o = self.noise_threshold_sbox
        o.valueChanged.emit(o.value())

    @pyqtSlot()
    def on_finalize_results(self):
        # show Twiss parameters as figure.
        if self._data is None:
            return
        if hasattr(self, '_plot_results_window'):
            self._plot_results_window.close()
        self._plot_results_window = PlotResults(self._ems_device.elem,
                                                self._auto_push_results,
                                                self._last_loading, self)
        self._plot_results_window.results = self._results
        try:
            self._plot_results_window.plot_data()
            self._plot_results_window.show()
            self._plot_results_window.setWindowTitle("Finalize Twiss Parameters")
            #
            self.add_attached_widget(self._plot_results_window)
        except:
            pass

    def on_title_with_ts(self, ts: float):
        """Title with human readable timestamp of the current data.
        """
        fmtedts = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        title = "Data generated at {}".format(fmtedts)
        self.title_changed.emit(title)
        return title

    @pyqtSlot()
    def on_sync_data(self):
        """Pull and analyze (if auto process is enabled) the live data.
        """
        auto_push = self._auto_push_results
        self.actionAuto_Push_Results_to_PVs.setChecked(False)
        if self._validate_device() is False:
            return
        self.on_add_current_config(show=False)
        arr = self._ems_device.get_data()
        try:
            self.check_data_size(arr)
        except DataSizeZeroError:
            QMessageBox.warning(self, "Fetch Last Measured Data",
                    "Last measured data is empty.", QMessageBox.Ok)
            return
        except DataSizeNotMatchError:
            QMessageBox.warning(self, "Fetch Last Measured Data",
                    f"Last measured data size ({arr.size}) mismatches the current scan settings ({self._ydim}x{self._xdim}).",
                    QMessageBox.Ok)
            return
        _title = self.on_title_with_ts(self._ems_device.get_data_pv().timestamp)
        # sync data only, bypass pos at begin check.
        self._pos_reached_begin = True
        #
        self.on_update(arr)
        self.on_initial_data()
        self.on_plot_raw_data()

        if self._auto_analysis:
            self.title_changed.emit(_title + "\n" + "Automatic data processing ...")
            delayed_exec(lambda: self.title_changed.emit(_title), 2000)
            self._auto_process()

        #
        self._last_loading = False
        #
        self.actionAuto_Push_Results_to_PVs.setChecked(auto_push)
        # reset
        self._pos_reached_begin = True

    def check_data_size(self, data):
        if data.size == 0:
            raise DataSizeZeroError
        if data.size != self._xdim * self._ydim:
            raise DataSizeNotMatchError

    def _auto_process(self):
        self.post_log("Processing data...")
        self.auto_update_image_chkbox.setChecked(True)
        self.plot_region_btn.clicked.emit()
        self._update_bkgd_noise()
        self.on_update_results()
        self.factor_dsbox.valueChanged.emit(self.factor_dsbox.value())
        self.apply_noise_correction_btn.clicked.emit()
        self.on_update_results()
        self.show_results_btn.clicked.emit()
        self.clear_log()

    @pyqtSlot(bool)
    def on_enable_auto_analysis(self, f):
        self._auto_analysis = f

    @pyqtSlot()
    def on_save_data(self):
        if self._data_save_dlg is None:
            self._data_save_dlg = SaveDataDialog(DEFAULT_DATA_SAVE_DIR, self)
        if self._last_loading:
            self._data_save_dlg.filepath_lineEdit.setText(self._loading_filepath)
            self._data_save_dlg.note_plainTextEdit.setPlainText(self._loading_note)
            self._last_loading = False
        self._data_save_dlg.exec_()

    def _save_results_as_image(self, filepath):
        """Save results as a image file.
        """
        if not hasattr(self, '_plot_results_window'):
            self.show_results_btn.clicked.emit()
            delayed_exec(lambda: self._plot_results_window.grab().save(filepath), 2000)
        self._plot_results_window.grab().save(filepath)

    def _save_data_to_file(self, filepath, **kws):
        ems = self._ems_device
        xoy = ems.xoy.lower()
        pos_begin = ems.pos_begin
        pos_end = ems.pos_end
        pos_step = ems.pos_step
        volt_begin = ems.volt_begin
        volt_end = ems.volt_end
        volt_step = ems.volt_step
        pos_size = int((pos_end - pos_begin) / pos_step) + 1
        volt_size = int((volt_end - volt_begin) / volt_step) + 1
        data = np.flipud(self._data.intensity)
        ds = JSONDataSheet()
        r = []
        r.append(('xoy', xoy))
        r.append(('position', {
            'begin': pos_begin, 'end': pos_end, 'step': pos_step,
            'unit': 'mm'}))
        r.append(('voltage', {
            'begin': volt_begin, 'end': volt_end, 'step': volt_step,
            'unit': 'V'}))
        r.append(('data', {
            'shape': (volt_size, pos_size),
            'array': data.tolist()}))
        ds.update(r)
        # ion species
        n, q, a, ek = self._get_ion_info("as-is") # grab ion info as-is.
        ds.update({
            "Beam Source": {
                '_id': self._headinfo_widget.getIonSourceId(),
                'Ion Name': n,
                'Q': q,
                'A': a,
                'Ek': {'value': ek, 'unit': 'eV'}}})
        # data-processing params
        bkgd_noise_nelem = '{0:d}'.format(self.bkgd_noise_nelem_sbox.value())
        bkgd_noise_nsigma = '{0:d}'.format(self.bkgd_noise_threshold_sbox.value())
        ellipse_sf = '{0:.1f}'.format(self.factor_dsbox.value())
        noise_threshold = '{0:.1f}'.format(self.noise_threshold_sbox.value())
        ds.update({
            'analysis parameters':
            {
                'background noise corner sampling points': bkgd_noise_nelem,
                'background noise corner sampling threshold': bkgd_noise_nsigma,
                'ellipse size factor': ellipse_sf,
                'noise threshold': noise_threshold,
            }
        })
        # results
        if self._results is not None:
            ds.update({'results': {k: '{0:.6g}'.format(v) for k,v in self._results.items()}})
        ds.update({'info':
                    {'user': getuser(),
                     'app': self.getAppTitle(),
                     'version': self.getAppVersion()}})
        # note
        ds.update({'note':
                    kws.get('note')})
        ds.write(filepath)

    @pyqtSlot()
    def on_auto_fill_beam_params(self, mode="Live"):
        # mode: Live
        n, q, a, ek = self._get_ion_info(mode)
        ws = (self.ion_name_lineEdit,
              self.ion_charge_lineEdit,
              self.ion_mass_lineEdit)
        for v, w in zip((n, q, a), ws):
            w.setText(str(v))
        self.ion_energy_lineEdit.setText("{0:.6g}".format(ek))
        try:
            self.on_update_model()
        except:
            pass

    def _get_ion_info(self, mode="Live"):
        # ion name, Q, A, Ek [eV]
        # Q, A, Ek
        # mode:
        #  - Live, pull from PVs
        #  - Simulation, load from UI or roll back with default ones
        if mode == "Live":
            n, a, _, q = self.beamSpeciesDisplayWidget.get_species()
            pv_hv_book = HV_MAP.get(self.beamSpeciesDisplayWidget.get_ion_source())
            kv = caget(pv_hv_book)
            ek = kv * 1000.0 * q / a
        else: # Simulation
            # get from UI
            n = self.ion_name_lineEdit.text()
            q = int(self.ion_charge_lineEdit.text())
            a = int(self.ion_mass_lineEdit.text())
            ek = float(self.ion_energy_lineEdit.text())
            # n, q, a, kv = 'Ar', 9, 40, 53.333
        return (n, q, a, ek)

    @pyqtSlot()
    def on_reset_interlock(self):
        self._ems_device.reset_interlock()

    @pyqtSlot()
    def on_enable(self):
        """Enable the device.
        """
        self._ems_device.enable_device()

    @pyqtSlot(bool)
    def on_enable_advctrl(self, is_enabled: bool):
        """Visibility control for advanced device controls.
        """
        [w.setVisible(is_enabled) for w in (
            self.adv_ctrl_widget, self.adv_ctrl_hline,
            self.scan_status_info_full_lbl)]
        [w.setVisible(not is_enabled) for w in (
            self.scan_status_info_lbl, self.status_lbl)]

    def _beat_on(self, dt):
        self.status_lbl.setPixmap(self._active_px)
        QTimer.singleShot(dt,
                lambda:self.status_lbl.setPixmap(self._inactive_px))

    def _update_xylabels(self):
        # update xylabels.
        xlbl = "${}\,\mathrm{{[mm]}}$".format(self._ems_orientation.lower())
        self.xlabel_changed.emit(xlbl)
        self.raw_view_chkbox.toggled.emit(self.raw_view_chkbox.isChecked())

    @pyqtSlot()
    def on_show_ems(self):
        """Show EMS element detail info.
        """
        if self._device_widget is None:
            self._device_widget = ElementWidget(self._ems_device.elem)
        self._device_widget.show()

    @pyqtSlot()
    def onRunXnY(self):
        """Run X and Y in a sequence.
        """
        self.actionAuto_Analysis.setChecked(False)

        def on_finished():
            ori = self.ems_orientation_cbb.currentText()
            if ori == 'Y':
                self.retract_btn.clicked.emit()
                loop.quit()
            else:
                self.ems_orientation_cbb.setCurrentText('Y')
                self.run_btn.clicked.emit()

        self.ems_orientation_cbb.setCurrentText('X')
        self.run_btn.clicked.emit()

        loop = QEventLoop()
        self.finished.connect(on_finished)
        loop.exec_()

        self.actionAuto_Analysis.setChecked(True)

    @pyqtSlot()
    def on_add_current_config(self, show=True):
        """Add current device scan settings into settings list.
        """
        is_synced = self.fetch_config_btn.property('is_synced')
        if not is_synced:
            self.statusInfoChanged.emit(
                     "Device settings is not consistent between GUI and IOC.")
            # QMessageBox.warning(self, "Add Current Settings",
            #         "Device settings is not consistent between GUI and IOC.",
            #         QMessageBox.Ok)
            return
        self._scan_settings_list.append(self.build_current_scan_settings())
        if show:
            self.show_settings_list()

    def build_current_scan_settings(self):
        """Return a dict of current scan settings.
        """
        pb = self.pos_begin_dsbox.value()
        pe = self.pos_end_dsbox.value()
        ps = self.pos_step_dsbox.value()
        vb = self.volt_begin_dsbox.value()
        ve = self.volt_end_dsbox.value()
        vs = self.volt_step_dsbox.value()
        name = self._ems_device.name
        xoy = self._ems_orientation
        return build_scan_settings_dict(name, xoy, pb, pe, ps, vb, ve, vs)

    def build_default_scan_settings(self):
        """Return a dict of default scan settings.
        """
        dconf = Configuration(self._dconf.config_path)
        xoy = self._ems_orientation
        name = self._ems_device.name
        return get_scan_settings_from_config(xoy, name, dconf)

    @pyqtSlot()
    def on_load_default_config(self):
        """Load default scan ranges to device.
        """
        # reload default configuration file
        # push scan ranges shown in the panel
        self.on_add_current_config()
        self.actionReload.triggered.emit()
        for s in self._attr_names:
            o = getattr(self, s + '_dsbox')
            o.valueChanged.emit(o.value())

    @pyqtSlot(float)
    def on_update_pos_volt_conf(self, name: str, v: float):
        """Update the position/voltage scan range configurations.
        - Do not apply live update
        - Notify via button status if live value is changed.
        """
        w_name = '{}_dsbox'.format(POS_VOLT_NAME_MAP[name])
        w_value = getattr(self, w_name).value()
        self.set_fetch_config_btn(w_value, v)

    def set_fetch_config_btn(self, x: float, y: float):
        # set fetch config btn icon to reflect if the scan ranges match the device settings.
        # the scan ranges might be changed by other programs, e.g. through OPI.
        # this app does not auto keep up these values all the time, but provides this way to
        # notify the user, who can decide to catch up by clicking the button or not.
        try:
            assert_almost_equal(x, y)
        except AssertionError:
            px = self._fetch_red_px
            tt = "Scan range configurations are outdated, click to catch up."
            is_synced = False
        else:
            px = self._fetch_px
            tt = "Scan range configurations are updated."
            is_synced = True
        finally:
            self.fetch_config_btn.setIcon(QIcon(px))
            self.fetch_config_btn.setToolTip(tt)
            self.fetch_config_btn.setProperty("is_synced", is_synced)

    @pyqtSlot(float)
    def on_delete_settings(self, ts):
        """Delete settings by timestamp *ts*.
        """
        printlog("delete ", ts)
        for i, d in enumerate(self._scan_settings_list):
            if d['timestamp'] == ts:
                self._scan_settings_list.pop(i)
        self.show_settings_list()

    @pyqtSlot(float)
    def on_apply_settings(self, ts):
        """Apply settings by timestamp *ts*.
        """
        printlog("apply ", ts)
        for i, d in enumerate(self._scan_settings_list):
            if d['timestamp'] == ts:
                self.set_scan_settings(d)

    def set_scan_settings(self, d):
        """Apply scan settings from dict *d*.
        """
        self.pos_begin_dsbox.setValue(d['pos_begin'])
        self.pos_end_dsbox.setValue(d['pos_end'])
        self.pos_step_dsbox.setValue(d['pos_step'])
        self.volt_begin_dsbox.setValue(d['volt_begin'])
        self.volt_end_dsbox.setValue(d['volt_end'])
        self.volt_step_dsbox.setValue(d['volt_step'])

    @pyqtSlot()
    def onShowSchematic(self):
        """Show pop-up window for the schematic layout.
        """
        if self._layout_form is not None:
            self._layout_form = LayoutForm(self._ems_device)
        self._layout_form._show()

    def __set_device_info_label(self, info: str):
        # set up device info, installed or not.
        if info == "Installed":
            px = self.installed_px
            tt = "Device is ready to use"
        else:
            px = self.not_installed_px
            tt = "Device is not ready to use"
        self.info_lbl.setPixmap(px)
        self.info_lbl.setToolTip(tt)

    @pyqtSlot(bool)
    def onUpdateStatusIn(self, is_in: bool):
        # motor fork (pos) in status
        printlog(f"{self._ems_device.name}[{self._ems_orientation}] STATUS IN: {is_in}")
        if is_in:
            px = self._in_px
            tt = "Device is at IN"
        else:
            px = self._inactive_px
            tt = "Device is not IN"
        self.is_in_lbl.setPixmap(px)
        self.is_in_lbl.setToolTip(tt)

    @pyqtSlot(bool)
    def onUpdateStatusOut(self, is_out: bool):
        # motor fork (pos) out status
        printlog(f"{self._ems_device.name}[{self._ems_orientation}] STATUS OUT: {is_out}")
        if is_out:
            px = self._outlimit_px
            tt = "Device is at outlimit"
        else:
            px = self._inactive_px
            tt = "Device is not at outlimit"
        self.is_outlimit_lbl.setPixmap(px)
        self.is_outlimit_lbl.setToolTip(tt)

    @pyqtSlot(bool)
    def onUpdateStatusInterlockOK(self, is_ok: bool):
        # motor fork interlock ok statusa
        printlog(f"{self._ems_device.name}[{self._ems_orientation}] ITLK OK: {is_ok}")
        if is_ok:
            px = self._itlk_px
            tt = "Device interlock is OK"
        else:
            px = self._not_itlk_px
            tt = "Device interlock is not OK"
        self.is_itlk_lbl.setPixmap(px)
        self.is_itlk_lbl.setToolTip(tt)
        self.__check_device_ready_scan()

    @pyqtSlot(bool)
    def onUpdateStatusEnabled(self, is_enabled: bool):
        # enable status
        printlog(f"{self._ems_device.name}[{self._ems_orientation}] Enabled: {is_enabled}")
        if is_enabled:
            px = self._enable_px
            tt = "Device is enabled"
        else:
            px = self._not_enable_px
            tt = "Device is not enabled"
        self.is_enabled_lbl.setPixmap(px)
        self.is_enabled_lbl.setToolTip(tt)
        self.__check_device_ready_scan()

    @pyqtSlot(bool)
    def onUpdateBiasVoltOn(self, is_on: bool):
        # bias voltage on status
        printlog(f"{self._ems_device.name}[{self._ems_orientation}] BiasVolt ON: {is_on}")
        if is_on:
            px = self._enable_px
            tt = "Bias voltage is on"
        else:
            px = self._not_enable_px
            tt = "Bias voltage is off"
        self.is_bias_on_lbl.setPixmap(px)
        self.is_bias_on_lbl.setToolTip(tt)
        self.__check_device_ready_scan()

    @pyqtSlot(float)
    def onUpdateBiasVoltRead(self, x: float):
        # bias voltage readback
        self.live_biasVolt_lineEdit.setText(f'{x:.1f}')
        self.__check_device_ready_scan()
        # pass
        # self._ems_device.bias_volt_threshold = x
       #  self._ems_device.set_bias_voltage(0.1)
        # self._dconf = self._ems_device.dconf

    @pyqtSlot(float)
    def onUpdateBiasVoltSet(self, x: float):
        # bias voltage setpoint
        self.set_biasVolt_lineEdit.setText(f'{x:.0f}')

    @pyqtSlot(float)
    def onUpdatePosRead(self, x: float):
        # motor position readback
        self.live_pos_lineEdit.setText('{0:.2f}'.format(x))
        self._beat_on(500)

    @pyqtSlot(float)
    def onUpdatePosSet(self, x: float):
        # motor position setpoint
        self.set_pos_lineEdit.setText('{0:.2f}'.format(x))

    def post_log(self, msg: str):
        self.log_lbl.setVisible(True)
        self.log_lbl.setText(msg)

    def clear_log(self):
        self.log_lbl.setVisible(False)
        self.log_lbl.setText("")


class DataSizeNotMatchError(Exception):
    def __init__(self, *args, **kws):
        super(self.__class__, self).__init__(*args, **kws)


class DataSizeZeroError(Exception):
    def __init__(self, *args, **kws):
        super(self.__class__, self).__init__(*args, **kws)


def build_scan_settings_dict(name, xoy, pb, pe, ps, vb, ve, vs):
    return {
        'name': name, 'xoy': xoy,
        'timestamp': time.time(),
        'pos_begin': pb, 'pos_end': pe, 'pos_step': ps,
        'volt_begin': vb, 'volt_end': ve, 'volt_step': vs,
    }


def get_scan_settings_from_config(xoy, name, dconf):
    # xoy: 'X' or 'Y'
    # name: device name
    # default pos/volt alter ranges, [mm], [V], settling time: [sec]
    kxoy = kxoy = "{}.{}".format(name, xoy)
    pos_begin = float(dconf.get(kxoy, 'pos_begin'))
    pos_end = float(dconf.get(kxoy, 'pos_end'))
    pos_step = float(dconf.get(kxoy, 'pos_step'))
    pos_settling_time = float(dconf.get(kxoy, 'pos_settling_time'))
    volt_begin = float(dconf.get(kxoy, 'volt_begin'))
    volt_end = float(dconf.get(kxoy, 'volt_end'))
    volt_step = float(dconf.get(kxoy, 'volt_step'))
    volt_settling_time = float(dconf.get(kxoy, 'volt_settling_time'))
    return build_scan_settings_dict(
                name, xoy,
                pos_begin, pos_end, pos_step,
                volt_begin, volt_end, volt_step)


