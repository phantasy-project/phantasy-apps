#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QAction

from functools import partial

from phantasy_ui import BaseAppForm
from phantasy_ui.widgets import LatticeDataModelFull
from phantasy_ui.widgets import LatticeWidget
from phantasy_ui.widgets import ProbeWidget

from .ui.ui_app import Ui_MainWindow


class LatticeViewerWindow(BaseAppForm, Ui_MainWindow):

    def __init__(self, version):
        super(LatticeViewerWindow, self).__init__()

        # app version
        self._version = version

        # window title
        self.setWindowTitle("Lattice Viewer")

        # set app properties
        self.setAppTitle("Lattice Viewer")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Lattice Viewer</h4>
            <p>This app is created to visualize the FRIB accelerator
            structure, investigate devices, current version is {}.
            </p>
            <p>Copyright (C) 2018 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

        #
        self.post_init_ui()

    def post_init_ui(self):
        #
        self.__mp = None
        self._lattice_load_window = None
        # context menu
        self._copy_icon = QIcon(QPixmap(":/lv-icons/copy.png"))
        self._probe_icon = QIcon(QPixmap(":/lv-icons/probe.png"))
        self.set_context_menu()
        self._probe_widgets_dict = {}

    def set_context_menu(self):
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.on_custom_context_menu)

    @pyqtSlot(QPoint)
    def on_custom_context_menu(self, pos):
        m = self.treeView.model()
        if m is None:
            return
        idx = self.treeView.indexAt(pos)
        item = m.itemFromIndex(idx)
        text = item.text()

        #
        menu = QMenu(self)
        menu.setStyleSheet('QMenu {margin: 2px;}')

        #
        copy_action = QAction(self._copy_icon,
                              "Copy '{}'".format(text), menu)
        copy_action.triggered.connect(partial(self.on_copy_text, m, idx))
        menu.addAction(copy_action)

        #
        if hasattr(item, 'fobj'):
            ename = text
            elem = self.__lat[ename]
            fld = item.fobj
            probe_action = QAction(self._probe_icon,
                                   "Probe '{}'".format(ename), menu)
            probe_action.triggered.connect(
                    partial(self.on_probe_element, elem, fld.name))
            menu.addAction(probe_action)

        #
        menu.exec_(self.treeView.viewport().mapToGlobal(pos))

    @pyqtSlot()
    def on_copy_text(self, m, idx):
        text = m.data(idx)
        cb = QGuiApplication.clipboard()
        cb.setText(text)
        msg = '<html><head/><body><p><span style="color:#007BFF;">Copied text: </span><span style="color:#DC3545;">{}</span></p></body></html>'.format(text)
        self.statusInfoChanged.emit(msg)
        self._reset_status_info()

    @pyqtSlot()
    def on_probe_element(self, elem, fname):
        ename = elem.name
        if ename not in self._probe_widgets_dict:
            w = ProbeWidget(element=elem)
            [o.setEnabled(False) for o in (w.locate_btn, w.lattice_load_btn)]
            self._probe_widgets_dict[ename] = w
        w = self._probe_widgets_dict[ename]
        w.show()
        w.fields_cbb.setCurrentText(fname)

    def on_pressed_view(self, idx):
        m = self.treeView.model()
        if m is None:
            return
        if QGuiApplication.mouseButtons() == Qt.MiddleButton:
            cb = QGuiApplication.clipboard()
            if cb.supportsSelection():
                text = m.data(idx)
                cb.setText(text, cb.Selection)
                msg = '<html><head/><body><p><span style=" color:#007bff;">Selected text: </span><span style=" color:#dc3545;">{}</span><span style=" color:#007bff;">, paste with middle button.</span></p></body></html>'.format(text)
                self.statusInfoChanged.emit(msg)
                self._reset_status_info()

    @pyqtSlot()
    def on_load_lattice(self):
        """Load lattice.
        """
        if self._lattice_load_window is None:
            self._lattice_load_window = LatticeWidget()
            self._lattice_load_window.latticeChanged.connect(
                self.on_lattice_changed)
            self._lattice_load_window.latticeChanged.connect(self._lattice_load_window.close)
        self._lattice_load_window.show()

    @pyqtSlot(QVariant)
    def on_lattice_changed(self, o):
        """loaded lattice changed.
        """
        self.__mp = o
        self.__lat = o.combined_lattice()
        model = LatticeDataModelFull(self.treeView, o)
        model.set_model()
        # update meta info
        self.on_update_metainfo(o)
        # update layout drawing
        self.init_layout()

    def init_layout(self):
        # initial lattice layout view
        lat = self.__mp.work_lattice_conf
        layout = lat.layout
        ax = self.layout_plot.axes
        layout.draw(ax=ax, span=(1.05, 1.1))
        self.layout_plot.update_figure()

    def on_update_metainfo(self, o):
        """Update meta info of loaded lattice.
        """
        n_elem = len(o.work_lattice_conf)
        dtypes = o.get_all_types()
        sts_elem = [(f, len(o.get_elements(type=f))) for f in dtypes]
        sts_info = ' '.join(['{}({})'.format(f, n) for f, n in sts_elem])
        self.elem_num_lineEdit.setText('{0:d}'.format(n_elem))
        self.elem_sts_lineEdit.setText(sts_info)
        self.elem_types_lineEdit.setText(';'.join(dtypes))


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    w = LatticeViewerWindow(version="1.0")
    w.show()

    sys.exit(app.exec_())
