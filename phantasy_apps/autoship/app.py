#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import toml
from functools import partial
from pathlib import Path

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QLabel, QCheckBox, QComboBox
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QSizePolicy, QGridLayout
from PyQt5.QtWidgets import QFrame

from phantasy_ui import BaseAppForm
from phantasy_ui import get_open_directory
from .ui.ui_app import Ui_MainWindow


REFRESH_INTERVAL = 5000 # ms

_HELP_TEXT = """
Hint...
"""


class _Path:
    # line: <file/dirpath>,r;tmin
    def __init__(self, line: str):
        _path_s, _t_wait_min = line.strip().split(";")
        self.t_wait_min = int(_t_wait_min)
        _path, self.is_remote_str = _path_s.split(",")
        self.fullpath = os.path.abspath(os.path.expanduser(_path))
        if self.is_remote_str == '':
            self.is_remote = False
        else:
            self.is_remote = True

    def __str__(self):
        return f"{self.fullpath},{self.is_remote_str};{self.t_wait_min}"


def read_config(configpath: str):
    _c = toml.load(configpath)
    _use_conf = _c[_c['default']['use']]

    conf_path = _use_conf['CONF_PATH']
    allowed_root_path = _use_conf['ALLOWED_ROOT_PATH']
    extra_allowed_root_path_list = _use_conf['EXTRA_ALLOWED_ROOT_PATH']

    path_list = []
    if not os.path.isfile(conf_path):
        with open(conf_path, "w") as fp:
            fp.write("# A list of directory path for AutoShip app.\n")
            fp.flush()
        os.chmod(conf_path, 0o664)
    else:
        for line in open(conf_path, "r"):
            if line.startswith("#"):
                continue
            _pth = os.path.abspath(os.path.expanduser(line.split(';')[0].strip()))
            if all(Path(p) not in Path(_pth).parents for p in extra_allowed_root_path_list + [allowed_root_path]):
                print(f"Skip {_pth} not in {allowed_root_path}")
                continue
            path_list.append(_Path(line))

    return path_list, conf_path, allowed_root_path, extra_allowed_root_path_list


class AutoShipWindow(BaseAppForm, Ui_MainWindow):

    # a list of dirpaths for AutoShip configs
    # each one is a _Path instance
    sigPathListChanged = pyqtSignal(list)

    def __init__(self, version: str, configpath: str):
        super(AutoShipWindow, self).__init__()
        self._version = version
        self.setWindowTitle("AutoShip")
        self.setAppTitle("AutoShip")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About AutoShip</h4>
            <p>This app is created to auto-ship files in AP directory to outbound, current version is {}.
            </p>
            <p>Copyright (C) 2023 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)
        self.postInitUi()

        # help
        self._hint_dlg = None
        #
        self.path_list, self.conf_path, self.allowed_root_path, self.extra_allowed_root_path_list = \
                read_config(configpath)
        # logdir
        self.logdirpath = Path(self.conf_path).parent.joinpath(".ah-logs")
        #
        self.allowed_root_path_lineEdit.setText(self.allowed_root_path)

        self.sigPathListChanged.connect(self.on_path_list_changed)

        #
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_refresh)
        self.timer.start(REFRESH_INTERVAL)
        #
        self.sigPathListChanged.emit(self.path_list)
        QTimer.singleShot(0, lambda:self.on_refresh())
        #

    @pyqtSlot()
    def onOpen(self):
        """Open a folder.
        """
        folderpath = get_open_directory(self, cdir=self.allowed_root_path)
        if any(Path(p) in Path(folderpath).parents for p in self.extra_allowed_root_path_list + [self.allowed_root_path]):
            self.dirpath_lineEdit.setText(folderpath)
        else:
            QMessageBox.warning(self, "Choose a Folder",
                                f"Please choose a folder under: '{self.allowed_root_path}'",
                                QMessageBox.Ok, QMessageBox.Ok)
            return

    def _get_folderpath(self):
        if self.dirpath_lineEdit.text() == '':
            return None
        folderpath = os.path.abspath(os.path.expanduser(
                self.dirpath_lineEdit.text().strip()))
        if os.path.isdir(folderpath):
            return folderpath
        else:
            QMessageBox.warning(self, "Folderpath",
                    f"Invalid folder path!",
                    QMessageBox.Ok, QMessageBox.Ok)
            return None

    @pyqtSlot()
    def onAdd(self):
        """Add a folderpath with live perms into the conf dirpath file.
        """
        folderpath = self._get_folderpath()
        if folderpath is None:
            return
        if folderpath in [i.fullpath for i in self.path_list]:
            QMessageBox.warning(self, "Add Folderpath",
                    f"'{folderpath}' is already added and being managed.",
                    QMessageBox.Ok, QMessageBox.Ok)
        else:
            _path = _Path(f"{folderpath},;60")
            self.path_list.append(_path)
            with open(self.conf_path, "a") as fp:
                fp.write(str(_path) + "\n")
                fp.flush()
            self.sigPathListChanged.emit(self.path_list)
        self.dirpath_lineEdit.clear()

    @pyqtSlot()
    def onRemove(self):
        """Remove a folderpath.
        """
        folderpath = self._get_folderpath()
        if folderpath is None:
            return
        if folderpath not in [i.fullpath for i in self.path_list]:
            QMessageBox.warning(self, "Remove Folderpath",
                    f"'{folderpath}' is not being managed.",
                    QMessageBox.Ok, QMessageBox.Ok)
        else:
            for i, o in enumerate(self.path_list):
                if o.fullpath == folderpath:
                    self.path_list.pop(i)
                    del o
            self.write_conf()
            self.sigPathListChanged.emit(self.path_list)
        self.dirpath_lineEdit.clear()

    @pyqtSlot()
    def on_refresh(self):
        """Refresh the dirpath permissions.
        """
        self._layout_paths(self.path_list, self.live_area, is_live=True)

    @pyqtSlot(list)
    def on_path_list_changed(self, path_list: list):
        """Post the file path info config.
        """
        self._layout_paths(path_list, self.config_area, is_live=False)

    def _layout_paths(self, path_list, area, is_live=False):
        """List all the dirpaths with config management rules, one folderpath per line.

        # config_area: for configurations
        # live_area: for live permissions
        """
        if is_live:
            enable_checkbox = False
        else:
            enable_checkbox = True # support change checkbox for permission
        #
        w = area.takeWidget()
        w.setParent(None)

        w = QWidget(self)
        w.setContentsMargins(0, 6, 0, 0)
        l = QGridLayout()
        # headers
        if is_live:
            headers = ("", "Path", "", "Last Shipped")
        else:
            headers = ("", "Path", "Interval", "", "Remote?")

        for j, s in enumerate(headers):
            if s == "|":
                _w = QFrame(self)
                _w.setFrameShape(QFrame.VLine)
                _w.setFrameShadow(QFrame.Plain)
            else:
                _w = QLabel(s, self)
                _w.setStyleSheet("QLabel { font-weight: bold; }")
            l.addWidget(_w, 0, j)

        i = 1
        for i, d in enumerate(path_list, 1):
            _fullpath = d.fullpath
            # dirpath
            _path_lbl = QLabel(_fullpath, self)
            _path_lbl.setTextInteractionFlags(
                    Qt.LinksAccessibleByMouse | Qt.TextSelectableByMouse)

            if is_live:
                # shipping or shipped?
                _log1 = self.logdirpath.joinpath(_fullpath.replace("/", "_") + '_1.log')
                if _log1.is_file():
                    _refresh_status = _log1.read_text().strip()
                else:
                    _refresh_status = "idle"
                _refreshed_lbl = QLabel(self)
                if _refresh_status == "running":
                    _refreshed_lbl.setPixmap(QPixmap(":/_misc/pending.png").scaled(32, 32))

                # last shipped date
                _log2 = self.logdirpath.joinpath(_fullpath.replace("/", "_") + '_2.log')
                if _log2.is_file():
                    _last_refreshed_date = _log2.read_text().strip()
                else:
                    _last_refreshed_date = ""
                _last_refreshed_lbl = QLabel(self)
                _last_refreshed_lbl.setText(_last_refreshed_date)
                _last_refreshed_lbl.setToolTip(f"{_fullpath} was shipped at {_last_refreshed_date}\nNow is {_refresh_status}")

            # place a row for d
            if is_live:
                w_list = (
                    QLabel(str(i), self),
                    _path_lbl,
                    _refreshed_lbl,
                    _last_refreshed_lbl,
                )
            else:
                _t_min_sbox = QSpinBox(self)
                _t_min_sbox.setRange(0, 9999)
                _t_min_sbox.setSingleStep(1)
                _t_min_sbox.setSuffix(" m")
                _t_min_sbox.setValue(d.t_wait_min)
                _t_min_btn = QToolButton(self)
                _t_min_btn.setIcon(QIcon(QPixmap(":/_misc/apply.png")))
                _t_min_btn.setIconSize(QSize(28, 28))
                _t_min_btn.setToolTip("Click to change time interval.")
                _t_min_btn.clicked.connect(partial(self.on_t_wait_changed, d, _t_min_sbox))
                _is_remote_chkbox = QCheckBox("Remote", self)
                _is_remote_chkbox.setChecked(d.is_remote)
                _is_remote_chkbox.toggled.connect(partial(self.on_toggle_remote, d))
                _is_remote_chkbox.setEnabled(False)
                _is_remote_chkbox.setToolTip("Not Support Yet")
                w_list = (QLabel(str(i), self),
                          _path_lbl, _t_min_sbox, _t_min_btn,
                          _is_remote_chkbox)
            for j, _w in enumerate(w_list):
                if j == 0:
                    _w.setStyleSheet("""
                    QLabel {
                        font-family: monospace;
                        border-top: 0px solid gray;
                        border-right: 5px solid gray;
                    }""")
                l.addWidget(_w, i, j)
        #
        _vspacer = QWidget()
        _vspacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        l.addWidget(_vspacer, i + 1, 1)
        w.setLayout(l)
        area.setWidget(w)

    @pyqtSlot()
    def on_t_wait_changed(self, _p: _Path, _o: QSpinBox):
        """Time interval for perm scan.
        """
        new_t_min = _o.value()
        if _p.t_wait_min != new_t_min:
            _p.t_wait_min = new_t_min
            self.write_conf()

    def write_conf(self):
         # update file
        with open(self.conf_path, "w") as fp:
            fp.write("# A list of directory path for AutoShip app.\n")
            fp.writelines("\n".join((str(i) for i in self.path_list)))
            fp.write("\n")
            fp.flush()

    @pyqtSlot(bool)
    def on_toggle_remote(self, _p: _Path, is_checked: bool):
        if _p.is_remote == is_checked:
            return
        if is_checked:
            _p.is_remote = True
            _p.is_remote_str = "r"
        else:
            _p.is_remote = False
            _p.is_remote_str = ""
        self.write_conf()

    @pyqtSlot()
    def onHint(self):
        """Show a brief text as the help.
        """
        if self._hint_dlg is None:
            self._hint_dlg = QTextEdit()
            self._hint_dlg.setHtml(_HELP_TEXT)
            self._hint_dlg.setReadOnly(True)
            self._hint_dlg.setWindowTitle("AutoShip - Help")
            self._hint_dlg.setStyleSheet("""QTextEdit {
                border-top: 0px solid gray;
                border-bottom: 5px solid gray;
                border-right: 5px solid gray;
                border-left: 0px solid gray;}""")
        self._hint_dlg.show()
        self._hint_dlg.resize(880, 650)
