#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QMainWindow

from functools import partial
from collections import OrderedDict
import numpy as np

from phantasy_ui.templates import BaseAppForm
from phantasy.apps.trajectory_viewer.utils import ElementListModel
from phantasy.apps.utils import get_save_filename
from phantasy.apps.utils import get_open_filename

from .ui.ui_app import Ui_MainWindow
from .utils import OrmWorker
from .utils import ORMDataSheet
from .utils import load_orm_sheet


OP_MODE_MAP = {
    'Simulation': 'model',
    'Live': 'control',
}


class OrbitResponseMatrixWindow(BaseAppForm, Ui_MainWindow):
    """Orbit reponse matrix measurement, visualization and data management.

    Parameters
    ----------
    parent :
        Paranet QObject.
    version : str
        Version number string.

    Keyword Arguments
    -----------------
    cors : dict
        Dict of correctors, key: element name, value: list of fields.
    bpms : dict
        Dict of monitors, key: element name, value: list of fields.
    name_map : dict
        Dict of element name (key) and element object (value) mapping.
    mp :
        MachinePortal object.
    """

    def __init__(self, parent, version, **kws):
        super(OrbitResponseMatrixWindow, self).__init__()
        self.parent = parent

        # name map
        self._name_map = kws.get('name_map', {})

        # mp
        self.__mp = kws.get('mp', None)

        # orm
        self._orm = None

        # bpms dict
        self._bpms_dict = sort_dict(kws.get('bpms', OrderedDict()))

        # cors dict
        self._cors_dict = sort_dict(kws.get('cors', OrderedDict()))

        # app version
        self._version = version

        # window title
        self.setWindowTitle("Orbit Response Matrix")

        # set app properties
        self.setAppTitle("Orbit Response Matrix")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Orbit Response Matrix</h4>
            <p>This app is created to measure, manage and visualize
            the orbit response matrices for central trajectory correction,
            current version is {}.
            </p>
            <p>Copyright (C) 2018 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

        #
        self.post_init()

    def post_init(self):
        # refresh element list models
        self.refresh_models_btn.clicked.connect(self.on_refresh_models)

        # set up models for BPMs and CORs
        self.refresh_models_btn.clicked.emit()

        #
        self.measure_pb.setVisible(False)
        self.cor_apply_pb.setVisible(False)

        # element selection for BPMs/CORs treeview
        self.select_all_bpms_btn.clicked.connect(
                partial(self.on_select_all_elems, "bpm"))
        self.inverse_bpm_selection_btn.clicked.connect(
                partial(self.on_inverse_current_elem_selection, "bpm"))
        self.select_all_cors_btn.clicked.connect(
                partial(self.on_select_all_elems, "cor"))
        self.inverse_cor_selection_btn.clicked.connect(
                partial(self.on_inverse_current_elem_selection, "cor"))

    @pyqtSlot()
    def on_refresh_models(self):
        # refresh 'bpm' and 'cor' model.
        for mode in ('bpm', 'cor'):
            v = getattr(self, '_{}s_dict'.format(mode))
            tv = getattr(self, '{}s_treeView'.format(mode))
            enames = list(v.keys())
            model = ElementListModel(tv, self.__mp, enames)
            model.set_model()

        try:
            self.bpms_treeView.model().nElementSelected.connect(
                    lambda i:self.nelem_selected_bpms_lineEdit.setText(str(i)))
            self.cors_treeView.model().nElementSelected.connect(
                    lambda i:self.nelem_selected_cors_lineEdit.setText(str(i)))
        except:
            pass

    @pyqtSlot(dict)
    def on_update_elements(self, mode, elems_dict):
        """Update monitor view with *elems_dict* for *mode*, 'bpm' or 'cor'.
        """
        print("[ORM]-{}: {}".format(mode, elems_dict))
        e_dict = sort_dict(elems_dict)
        setattr(self, '_{}s_dict'.format(mode), e_dict)

    @pyqtSlot()
    def on_measure_orm(self):
        """Measure ORM.
        """
        params = self.__prepare_inputs_for_orm_measurement()

        self.thread = QThread()
        self.orm_runner = OrmWorker(params)
        self.orm_runner.moveToThread(self.thread)
        self.orm_runner.started.connect(partial(self.orm_worker_started, self.measure_pb, self.run_btn))
        self.orm_runner.resultsReady.connect(partial(self.on_results_ready, 'measure'))
        self.orm_runner.update_progress.connect(partial(self.update_pb, self.measure_pb))
        self.orm_runner.finished.connect(partial(self.orm_worker_completed, self.measure_pb, self.run_btn))
        self.orm_runner.finished.connect(self.thread.quit)
        self.orm_runner.finished.connect(self.orm_runner.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.orm_runner.run)
        self.thread.start()

    @pyqtSlot(float, 'QString')
    def update_pb(self, pb, x, s):
        pb.setValue(x)
        pb.setFormat("%p%")
        self.log_textEdit.append(s)

    @pyqtSlot()
    def orm_worker_started(self, pb, sender_obj):
        print("ORM worker is about to start.")
        sender_obj.setEnabled(False)
        pb.setVisible(True)

    @pyqtSlot()
    def orm_worker_completed(self, pb, sender_obj):
        print("ORM worker is done.")
        sender_obj.setEnabled(True)
        pb.setVisible(False)

    @pyqtSlot(QVariant)
    def on_results_ready(self, mode, m):
        if mode == 'measure':
            self._orm = m
            print("ORM is ready")
        else:
            pass

    def __prepare_inputs_for_orm_measurement(self):
        source = OP_MODE_MAP[self.operation_mode_cbb.currentText()]
        x1 = float(self.alter_start_lineEdit.text())
        x2 = float(self.alter_stop_lineEdit.text())
        n = int(self.alter_steps_lineEdit.text())
        srange = np.linspace(x1, x2, n)

        cor_field = list(self._cors_dict.values())[0][0]

        bpm_fields = self.monitor_fields_cbb.currentText()
        if bpm_fields== 'X&Y':
            xoy = 'xy'
        else:
            xoy = bpm_fields.lower()
        wait = self.wait_time_dspinbox.value()

        bpms = [self._name_map[e] for e in self._bpms_dict]
        cors = [self._name_map[e] for e in self._cors_dict]
        self._bpms = bpms
        self._cors = cors
        self._xoy = xoy

        print("source:", source)
        print("srange:", srange)
        print("cor_field:", cor_field)
        print("xoy:", xoy)
        print("wait:", wait)

        return (bpms, cors), (source, srange, cor_field, xoy, wait)

    @pyqtSlot()
    def on_apply_orm(self):
        """Apply ORM to correct orbit.
        """
        dfac = self.cor_damping_fac_dspinbox.value()
        niter = self.cor_niter_spinbox.value()
        t_wait = self.cor_wait_time_dspinbox.value()
        print(dfac, niter, t_wait)

        #
        bpm_fields = self.monitor_fields_cbb.currentText()
        if bpm_fields== 'X&Y':
            xoy = 'xy'
        else:
            xoy = bpm_fields.lower()

        bpms = [self._name_map[e] for e in self._bpms_dict]
        cors = [self._name_map[e] for e in self._cors_dict]
        self._bpms = bpms
        self._cors = cors
        self._xoy = xoy
        #

        lat = self.__mp.work_lattice_conf
        lat.orm = self._orm
        #
        params = (lat,), (self._bpms, self._cors), (self._xoy, dfac, niter, t_wait)

        self.thread1 = QThread()
        self.orm_consumer = OrmWorker(params, mode='apply')
        self.orm_consumer.moveToThread(self.thread1)
        self.orm_consumer.started.connect(partial(self.orm_worker_started, self.cor_apply_pb, self.cor_apply_btn))
        self.orm_consumer.resultsReady.connect(partial(self.on_results_ready, 'apply'))
        self.orm_consumer.update_progress.connect(partial(self.update_pb, self.cor_apply_pb))
        self.orm_consumer.finished.connect(partial(self.orm_worker_completed, self.cor_apply_pb, self.cor_apply_btn))
        self.orm_consumer.finished.connect(self.thread1.quit)
        self.orm_consumer.finished.connect(self.orm_consumer.deleteLater)
        self.thread1.finished.connect(self.thread1.deleteLater)
        self.thread1.started.connect(self.orm_consumer.run)
        self.thread1.start()

    @pyqtSlot()
    def on_open_orm(self):
        filepath, ext = get_open_filename(self,
                filter="JSON Files (*.json)")
        if filepath is None:
            return

        mp, name_map, bpms_dict, cors_dict, orm = load_orm_sheet(filepath)
        self.__mp = mp
        self._name_map = name_map
        self._bpms_dict = bpms_dict
        self._cors_dict = cors_dict
        self._orm = orm
        self.refresh_models_btn.clicked.emit()

    @pyqtSlot()
    def on_save_orm(self):
        filepath, ext = get_save_filename(self,
                cdir='.',
                filter="JSON Files (*.json)")
        if filepath is None:
            return

        machine, segment = self.__mp.last_machine_name, self.__mp.last_lattice_name
        bpms_dict = sort_dict(self.bpms_treeView.model()._selected_elements)
        cors_dict = sort_dict(self.cors_treeView.model()._selected_elements)

        orm = self._orm.tolist()
        data_sheet = ORMDataSheet()
        data_sheet['monitors'] = bpms_dict
        data_sheet['correctors'] = cors_dict
        data_sheet['machine'] = machine
        data_sheet['segment'] = segment
        data_sheet['orm'] = orm

        data_sheet.write(filepath)

    @pyqtSlot()
    def on_select_all_elems(self, mode):
        """Select all BPMs/CORs in *mode*s_treeView.
        """
        try:
            print("Select All {}s".format(mode.upper()))
            model = getattr(self, '{}s_treeView'.format(mode)).model()
            model.select_all_items()
        except AttributeError:
            QMessageBox.warning(self, "Element Selection",
                    "Selection error, Choose elements first.",
                    QMessageBox.Ok)

    @pyqtSlot()
    def on_inverse_current_elem_selection(self, mode):
        """Inverse current BPM/COR selection in *mode*s_treeView.
        """
        try:
            print("Inverse {} selection".format(mode.upper()))
            model = getattr(self, '{}s_treeView'.format(mode)).model()
            model.inverse_current_selection()
        except AttributeError:
            QMessageBox.warning(self, "Element Selection",
                    "Selection error, Choose elements first.",
                    QMessageBox.Ok)


def sort_dict(d):
    return OrderedDict([(k, d[k]) for k in sorted(d, key=lambda i:(i[-4:], i))])
