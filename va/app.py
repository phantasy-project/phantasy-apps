#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QProcess
from PyQt5.QtCore import QProcessEnvironment
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QAction
import epics
import time
import os

from phantasy_ui.templates import BaseAppForm
from phantasy.apps.utils import uptime

from .ui.ui_app import Ui_MainWindow
from .app_vainfo import VAProcessInfoWidget
from .icons import va_icon
from .icons import run_icon
from .icons import stop_icon
from .icons import nb_run_icon
from .icons import nb_stop_icon
from .icons import info_icon

CURDIR = os.path.dirname(__file__)

MACHINE_DICT = {
    'VA_LEBT': ('LEBT',),
    'VA_MEBT': ('MEBT',),
    #'VA_LS1FS1': ('LINAC', 'LS1', 'FS1',),
    'VA_LS1FS1': ('LINAC',),
}

MACHINE_LIST = sorted(list(MACHINE_DICT.keys()))


class VALauncherWindow(BaseAppForm, Ui_MainWindow):
    # va status changed, message to set, color of the string
    vaStatusChanged = pyqtSignal('QString', QColor)

    def __init__(self, version):
        super(VALauncherWindow, self).__init__()

        # app version
        self._version = version

        # window title/icon
        self.setWindowTitle("Virtual Accelerator Launcher")
        self.setWindowIcon(QIcon(QPixmap(va_icon)))

        # set app properties
        self.setAppTitle("VA Launcher")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Virtual Accelerator Launcher</h4>
            <p>Start virtual accelerators of FRIB for app development,
            current version is {}.
            </p>
            <p>Copyright (C) 2018 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

        # initialize va_process
        self.va_process = None

        # va process info widget
        self._va_info_widget = None

        # noise pv
        self.noise_pv = None
        self._noise_pv_name = 'VA:SVR:NOISE'

        # pv prefix
        self._prefix = None

        # CA local only
        self._ca_local_only = False

        # events
        # va status
        self.vaStatusChanged.connect(self.on_va_status_changed)
        # 0.001 * i -> 0.1% * i
        self.noise_slider.valueChanged.connect(
                lambda i:self.noise_label.setText("{:.1f}%".format(i*0.1)))
        self.noise_slider.valueChanged.connect(self.on_change_noise)

        # timer for uptime
        self.uptimer = QTimer(self)
        self.uptimer.timeout.connect(self.on_update_uptime)

        # post ui init
        self._post_ui_init()

    def _post_ui_init(self):
        # fill out mach/segm combobox
        self.mach_comboBox.clear()
        self.mach_comboBox.addItems(MACHINE_LIST)
        self.mach_comboBox.setCurrentText(MACHINE_LIST[0])
        self.mach_comboBox.currentTextChanged.emit(MACHINE_LIST[0])

        # run&stop tbtn: run
        self._setup_toolbar()

        # uptime label
        self.uptime_label.setText("00:00:00")

        # initialization, va config
        self.on_machine_changed(self.mach_comboBox.currentText())
        self.on_engine_changed(self.engine_comboBox.currentText())

        # disable all other tools
        self.enable_all_tools(False)

    def _setup_toolbar(self):
        # va run tool
        self.va_run_tool.setIcon(QIcon(QPixmap(run_icon)))
        self.va_run_tool.setToolTip("RUN VA")

        # va stop tool
        self.va_stop_tool.setIcon(QIcon(QPixmap(stop_icon)))
        self.va_stop_tool.setToolTip("STOP VA")

        # notebook tool
        self.nb_tool.setIcon(QIcon(QPixmap(nb_run_icon)))
        self.nb_tool.setToolTip("Launch Jupyter-notebook")

        # va info tool
        self.va_info_tool.setIcon(QIcon(QPixmap(info_icon)))
        self.va_info_tool.setToolTip("Show VA running status")

        # initial visibility
        self.va_run_tool.setEnabled(True)
        self.va_stop_tool.setEnabled(False)

    @pyqtSlot()
    def on_update_uptime(self):
        """Update uptime box.
        """
        up_secs = time.time() - self.start_time
        self.uptime_label.setText(uptime(up_secs))

    @pyqtSlot()
    def on_run_va(self):
        """Run VA.
        """
        env = QProcessEnvironment.systemEnvironment()
        k = 'PHANTASY_CONFIG_DIR'
        if k not in env.keys():
            env.insert(k, '/usr/lib/phantasy-machines')
        mach = self._mach
        segm = self._segm
        run_cmd = self._run_cmd
        prefix = self._prefix
        va = QProcess()
        va.setProcessEnvironment(env)
        self.va_process = va
        arguments = [run_cmd, '--mach', mach, '--subm', segm]
        if prefix is not None and prefix not in ('', 'NONE'):
            arguments.extend(['--pv-prefix', prefix])
            self._noise_pv_name = "{}:SVR:NOISE".format(prefix)
        if self._ca_local_only:
            arguments.append("-l")
        va.start('phytool', arguments)

        # start va
        va.started.connect(self.on_va_started)
        #va.errorOccurred.connect(self.on_error_occurred)

    def on_error_occurred(self, err):
        print("Error (code: {}) occurred...".format(err))

    @pyqtSlot('QString', QColor)
    def on_va_status_changed(self, s, color):
        self.va_status_label.setText(s)
        self.va_status_label.setStyleSheet(
                """QLabel {{
                    background-color:{c};
                    color: white;
                    border: 1px solid {c};
                    border-radius: 5px;
                    padding: 2px;
                }}""".format(c=color.name()))

    @pyqtSlot()
    def on_va_started(self):
        """VA is started.
        """
        self.start_time = time.time()
        self.uptimer.start(1000)
        self.vaStatusChanged.emit("Running", QColor("#4E9A06"))
        self.update_widgets_visibility(status="STARTED")
        self.va_name_label.setText(
            "{}/{}, PV prefixed with {}".format(
                self._mach, self._segm, self._prefix))
        if self._prefix == 'NONE' or self._prefix is None:
            self.va_name_label.setToolTip(
                "PV prefixed with default one, e.g. 'VA'")
        else:
            self.va_name_label.setToolTip('')
        # reset VAProcessInfoWidget
        self._va_info_widget = None
        # noise pv
        self.noise_pv = epics.PV(self._noise_pv_name,
                                 connection_callback=self.__on_connection_changed,
                                 callback=self.__on_value_changed)

    def update_widgets_visibility(self, status="STARTED"):
        """Enable/Disable widgets when VA is STARTED or STOPPED.
        """
        if status == 'STARTED':
            # enable tool buttons panel
            # enable VA STOP, disable VA START
            # disable VA configuration panel
            self.enable_all_tools()
            self.va_run_tool.setEnabled(False)
            self.va_stop_tool.setEnabled(True)
            self.config_groupBox.setEnabled(False)
        elif status == 'STOPPED':
            # disable tool buttons panel
            # disable VA STOP, enable VA START
            # enable VA configuration panel
            self.enable_all_tools(False)
            self.va_run_tool.setEnabled(True)
            self.va_stop_tool.setEnabled(False)
            self.config_groupBox.setEnabled(True)

    @pyqtSlot()
    def on_stop_va(self):
        """Stop VA.
        """
        pid = self.va_process.processId()
        self.va_process.kill()
        print("VA ({}) is stopped...".format(pid))
        self.vaStatusChanged.emit("Stopped", QColor("#EF2929"))
        self.uptimer.stop()
        self.update_widgets_visibility(status="STOPPED")

    @pyqtSlot('QString')
    def on_machine_changed(self, s):
        """Machine is changed, update segm_combob items.
        """
        self._mach = s
        self.segm_comboBox.currentTextChanged.disconnect()
        self.segm_comboBox.clear()
        self.segm_comboBox.currentTextChanged.connect(self.on_segment_changed)
        seg_names = MACHINE_DICT[s]
        self.segm_comboBox.addItems(seg_names)
        self.segm_comboBox.setCurrentText(seg_names[0])

    @pyqtSlot('QString')
    def on_segment_changed(self, s):
        """Segment is changed.
        """
        self._segm = s

    @pyqtSlot('QString')
    def on_pvprefix_changed(self, s):
        """PV string prefix is changed.
        """
        self._prefix = s.upper()

    @pyqtSlot('QString')
    def on_engine_changed(self, s):
        self._engine = s
        self._run_cmd = '{}-vastart'.format(s.lower())

    @pyqtSlot()
    def on_view_va_info(self):
        """VA info tool button: view va process information.
        """
        if self.va_process is None:
            return

        if self._va_info_widget is None:
            w = VAProcessInfoWidget(self.va_process.processId())
            self._va_info_widget = w
        self._va_info_widget.show_widget()

    @pyqtSlot()
    def on_launch_notebook(self):
        """Notebook tool button: launch jupyter notebook with predefined
        python environment.
        """
        obj = self.sender()
        def on_nb_started():
            obj.setText("STOP-NB")
            obj.setIcon(QIcon(QPixmap(nb_stop_icon)))
            obj.setToolTip("Stop Jupyter-notebook")

        if obj.text() == "RUN-NB":
            mach = self._mach
            self.nb_p = p = QProcess(self)
            cmd = "jupyter-notebook"
            nbfile = os.path.join(CURDIR, 'nb', "{}.ipynb".format(self._mach))
            args = []
            if os.path.isfile(nbfile):
                args.append(nbfile)
            p.start(cmd, args)
            p.started.connect(on_nb_started)
        elif obj.text() == "STOP-NB":
            self.nb_p.kill()
            obj.setText("RUN-NB")
            obj.setIcon(QIcon(QPixmap(nb_run_icon)))
            obj.setToolTip("Launch Jupyter-notebook")

    def enable_all_tools(self, enable=True):
        """Enable/disable all tools, except RUN/STOP VA tools.
        """
        [t.setEnabled(enable) for t in (self.nb_tool, self.va_info_tool)]

    def closeEvent(self, e):
        try:
            self.on_stop_va()
            self.va_process.waitForFinished()
        except:
            pass
        BaseAppForm.closeEvent(self, e)

    @pyqtSlot(int)
    def on_change_noise(self, i):
        """Update VA noise level.
        """
        if self.noise_pv is not None and self.noise_pv.connected:
            v = i * 0.001
            self.noise_pv.put(v, wait=True)

    @pyqtSlot(bool)
    def on_localonly(self, f):
        """CA localhost only or not.
        """
        self._ca_local_only = f

    def __on_connection_changed(self, pvname=None, conn=None, **kws):
        if conn:
            self.enable_noise_controls()
        else:
            self.enable_noise_controls(False)

    def __on_value_changed(self, pvname=None, value=None, host=None, **kws):
        v = int(value / 0.001)
        self.noise_slider.setValue(v)

    def enable_noise_controls(self, enable=True):
        """Enable controls for noise or not.
        """
        for o in (self.noise_slider, self.noise_label):
            o.setEnabled(enable)


