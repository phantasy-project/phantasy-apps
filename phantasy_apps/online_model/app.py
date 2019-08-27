#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Template Python module generated based on 'app_template', 'phantasy-ui'
is required to make it executable as a PyQt5 app.
"""

import os
import time
from functools import partial
from numpy import ndarray

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox

from phantasy_ui import BaseAppForm
from phantasy_ui import get_open_filename
from phantasy_ui import get_save_filename
from phantasy_ui.widgets import LatticeWidget
from phantasy_ui.widgets import DataAcquisitionThread as DAQT

from phantasy_apps.correlation_visualizer.utils import delayed_exec
from phantasy_apps.utils import apply_mplcurve_settings

from flame import Machine
from flame_utils import ModelFlame
from flame_utils import generate_source

from .ui.ui_app import Ui_MainWindow


class MyAppWindow(BaseAppForm, Ui_MainWindow):

    stop_signal = pyqtSignal(bool)
    traj_lineChanged = pyqtSignal(int)
    traj_xdataChanged = pyqtSignal(QVariant)
    traj_ydataChanged = pyqtSignal(QVariant)
    env_lineChanged = pyqtSignal(int)
    env_xdataChanged = pyqtSignal(QVariant)
    env_ydataChanged = pyqtSignal(QVariant)
    data_updated = pyqtSignal(ndarray, ndarray, ndarray, ndarray, ndarray)
    xmin_changed = pyqtSignal(float)
    xmax_changed = pyqtSignal(float)
    ymin_changed = pyqtSignal(float)
    ymax_changed = pyqtSignal(float)

    def __init__(self, version, **kws):
        super(self.__class__, self).__init__()

        # app version, title
        self.setAppVersion(version)
        self.setAppTitle("Online Model")

        # app info in about dialog
        self.app_about_info = """
            <html>
            <h4>About Physics Online Model</h4>
            <p>This app is created for the live modeling of accelerator.
            </p>
            <p>Copyright (c) 2019 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self.getAppVersion())

        # UI
        self.setupUi(self)
        self.postInitUi()

        #
        self._post_init()

    def _post_init(self):
        #
        self.lattice_load_window = None
        self._stop = False
        self.stop_signal.connect(self.on_set_stop_signal)

        # start/stop btns
        self.start_btn.clicked.connect(self.on_start)
        self.stop_btn.clicked.connect(self.on_stop)

        # export latfile
        self.export_btn.clicked.connect(self.on_export)

        # load latfile for reading initial condition
        self._beam_state_conf = None
        self.browse_btn.clicked.connect(self.on_open_latfile)
        self.latpath_lineEdit.returnPressed.connect(self.on_update_beamstate)

        # beam ellipse btn
        self.show_twiss_btn.clicked.connect(self.on_show_beam_ellipse)

        #
        self._init_data_viz()
        # xylimts
        for o in (self.envelope_plot, self.trajectory_plot, self.layout_plot):
            self.xmin_changed.connect(o.setXLimitMin)
            self.xmax_changed.connect(o.setXLimitMax)

        self.ymin_changed.connect(self.layout_plot.setYLimitMin)
        self.ymax_changed.connect(self.layout_plot.setYLimitMax)

        for s in ('xmin', 'xmax', 'ymin', 'ymax'):
            o = getattr(self, '{}_lineEdit'.format(s))
            o.setValidator(QDoubleValidator())
            o.textChanged.connect(partial(self.on_limit_changed, s))

        # beam init state
        self.beamstate_from_file_rbtn.setChecked(True)
        self.beamstate_from_config_rbtn.toggled.emit(False)

    @pyqtSlot('QString')
    def on_limit_changed(self, s, sv):
        v = float(self.sender().text())
        getattr(self, '{}_changed'.format(s)).emit(v)

    def _init_data_viz(self):
        # init data viz
        o1, o2 = self.trajectory_plot, self.envelope_plot
        self.traj_lineChanged.connect(o1.setLineID)
        self.traj_xdataChanged.connect(o1.setXData)
        self.traj_ydataChanged.connect(o1.setYData)
        self.env_lineChanged.connect(o2.setLineID)
        self.env_xdataChanged.connect(o2.setXData)
        self.env_ydataChanged.connect(o2.setYData)

        self.data_updated.connect(self.on_data_updated)

        self.trajectory_plot.add_curve()
        self.envelope_plot.add_curve()

        for s in ('traj', 'env'):
            for i in range(2):
                getattr(self, '{}_lineChanged'.format(s)).emit(i)
                getattr(self, '{}_xdataChanged'.format(s)).emit([])
                getattr(self, '{}_ydataChanged'.format(s)).emit([])

        # mpl settings
        apply_mplcurve_settings(o1, 'online_model',
                                filename='om_mpl_settings_traj.json')
        apply_mplcurve_settings(o2, 'online_model',
                                filename='om_mpl_settings_env.json')

    @pyqtSlot()
    def on_start(self):
        """Start modeling.
        """
        if self._stop:
            self.set_widgets_status("STOP")

            return

        self._settling_sec = self.dtsec_dsbox.value()
        self.mth = DAQT(daq_func=self.model_single, daq_seq=range(1))
        self.mth.daqStarted.connect(partial(self.set_widgets_status, "START"))
        self.mth.resultsReady.connect(self.on_results_ready)
        self.mth.finished.connect(self.on_start)
        self.mth.start()

    def on_data_updated(self, s, x, y, rx, ry):
        self.traj_lineChanged.emit(0)
        self.traj_xdataChanged.emit(s)
        self.traj_ydataChanged.emit(x)
        self.traj_lineChanged.emit(1)
        self.traj_xdataChanged.emit(s)
        self.traj_ydataChanged.emit(y)

        self.env_lineChanged.emit(0)
        self.env_xdataChanged.emit(s)
        self.env_ydataChanged.emit(rx)
        self.env_lineChanged.emit(1)
        self.env_xdataChanged.emit(s)
        self.env_ydataChanged.emit(ry)

    def model_single(self, iiter):
        # model with live settings.
        t0 = time.time()
        print("-- Sync live settings...")
        self._lat.sync_settings()
        print("-- Sync live settings...done: {0:.3f} s".format(time.time() - t0))
        print("-- Run physics model...")
        _, fm = self._lat.run()
        if self._beam_state_conf is not None:
            fm.configure(econf=self._beam_state_conf)
        r, s = fm.run(monitor='all')
        self._fm = fm
        data = fm.collect_data(r, pos=True, x0=True, y0=True,
                               xrms=True, yrms=True)
        s = data['pos'] + self._pos_offset
        traj_x, traj_y = data['x0'], data['y0']
        env_x, env_y = data['xrms'], data['yrms']
        self.data_updated.emit(s, traj_x, traj_y, env_x, env_y)
        dt = self._settling_sec - (time.time() - t0)
        print("-- Run physics model...done: {0:.3f} s".format(dt))
        if dt >= 0:
            time.sleep(dt)

    def on_results_ready(self, r):
        print(r)

    def set_widgets_status(self, status):
        olist1 = (self.start_btn, )
        olist2 = (self.stop_btn, )
        if status != "START":
            [o.setEnabled(True) for o in olist1]
            [o.setEnabled(False) for o in olist2]
        else:
            [o.setEnabled(False) for o in olist1]
            [o.setEnabled(True) for o in olist2]

    @pyqtSlot()
    def on_stop(self):
        """Stop modeling.
        """
        self.stop_signal.emit(True)
        delayed_exec(lambda:self.stop_signal.emit(False),
                     self._settling_sec * 1000)

    @pyqtSlot()
    def on_open_latfile(self):
        """Open lattice file to reading initial beam conditions.
        """
        filepath, ext = get_open_filename(self,
                type_filter="FLAME Lattice Files (*.lat)")
        if filepath is None:
            return
        self.latpath_lineEdit.setText(filepath)
        self.on_update_beamstate()

    @pyqtSlot()
    def on_update_beamstate(self):
        """Update initial beam conditions.
        """
        latfile = self.latpath_lineEdit.text()
        if not os.path.isfile(latfile):
            QMessageBox.warning(self, "Read Beam States",
                    "Invalid lattice file.", QMessageBox.Ok)
            return
        #
        fm = ModelFlame(lat_file=latfile)
        bs = fm.bmstate
        # additional process
        drf_lat = {'sim_type': 'MomentMatrix',
                   'elements': [{
                       'name': 'drift01',
                       'type': 'drift',
                       'L': 1.49541187}]
        }
        drf_m = Machine(drf_lat)
        drf_m.propagate(bs.state)
        s0 = generate_source(state=bs)
        print(s0)
        self._beam_state_conf = s0

    @pyqtSlot()
    def onLoadLatticeAction(self):
        """Load machine/segment configurations.
        """
        if self.lattice_load_window is None:
            self.lattice_load_window = LatticeWidget()
        self.lattice_load_window.show()
        self.lattice_load_window.latticeChanged.connect(self.update_mp)

    def update_mp(self, o):
        self._mp = o
        self._lat = o.work_lattice_conf
        self._pos_offset = self._lat.s_begin
        mach, segm = o.last_machine_name, o.last_lattice_name
        self.machine_lineEdit.setText(mach)
        self.segment_lineEdit.setText(segm)
        self.init_latinfo()
        self.init_layout()

    def init_latinfo(self):
        # initial lattice info view
        self._lv = None
        self.lattice_info_btn.clicked.connect(self.on_show_latinfo)

    def init_layout(self):
        # initial lattice layout view
        layout = self._lat.layout
        ax = self.layout_plot.axes
        layout.draw(ax=ax, span=(1.05, 1.05))
        self.layout_plot.update_figure()

    @pyqtSlot(bool)
    def on_set_stop_signal(self, f):
        self._stop = f

    @pyqtSlot()
    def on_export(self):
        """Export lattice file for current modeling.
        """
        filepath, ext = get_save_filename(self,
                type_filter="FLAME Lattice Files (*.lat)")
        if filepath is None:
            return
        self._fm.generate_latfile(latfile=filepath)

    @pyqtSlot()
    def on_show_latinfo(self):
        machine = self.machine_lineEdit.text()
        lattice = self.segment_lineEdit.text()
        if machine == '' or lattice == '':
            return

        from phantasy_apps.lattice_viewer import LatticeViewerWindow
        from phantasy_apps.lattice_viewer import __version__
        from phantasy_apps.lattice_viewer import __title__

        if self._lv is None:
            self._lv = LatticeViewerWindow(__version__)
            self._lv.setWindowTitle("{} ({})".format(__title__, self.getAppTitle()))
        lw = self._lv.latticeWidget
        lw.mach_cbb.setCurrentText(machine)
        lw.seg_cbb.setCurrentText(lattice)
        lw.load_btn.clicked.emit()
        lw.setEnabled(False)
        self._lv.show()

    @pyqtSlot()
    def onSnapshotAction(self):
        """Show results in a popup window.
        """
        QMessageBox.warning(self, "", "To be implemented.", QMessageBox.Ok)
        #from flame_utils import hplot
        #hplot('xcen', 'ycen', 'xrms', 'yrms', machine=self._fm)

    @pyqtSlot()
    def on_show_beam_ellipse(self):
        """Show beam ellipse based on twiss parameters.
        """
        QMessageBox.warning(self, "", "To be implemented.", QMessageBox.Ok)
        # if self._ellipse_widget is None:
        #    self._ellipse_widget = EllipseWindow(self)
        # self._ellipse_widget.show()



if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    version = 0.1
    app = QApplication(sys.argv)
    w = MyAppWindow(version)
    w.show()
    w.setWindowTitle("This is an app from template")
    sys.exit(app.exec_())
