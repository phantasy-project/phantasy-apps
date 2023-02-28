#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import toml

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QLabel, QCheckBox, QComboBox
from PyQt5.QtWidgets import QSizePolicy, QGridLayout
from PyQt5.QtWidgets import QFrame

from phantasy_ui import BaseAppForm
from phantasy_ui import get_open_filename
from phantasy_ui import get_open_directory
from .ui.ui_app import Ui_MainWindow


def read_config(configpath: str):
    _c = toml.load(configpath)
    _use_conf = _c[_c['default']['use']]

    conf_path = _use_conf['CONF_PATH']
    allowed_root_path = _use_conf['ALLOWED_ROOT_PATH']
    additional_group_list = _use_conf['ADDITIONAL_GROUP_LIST']

    dirpath_list = []
    if not os.path.isfile(conf_path):
        with open(conf_path, "w") as fp:
            fp.write("# A list of directory path for Permission Manager.\n")
        os.chmod(conf_path, 0o664)
    else:
        for line in open(conf_path, "r"):
            if line.startswith("#"):
                continue
            _pth = os.path.abspath(os.path.expanduser(line.strip()))
            if not _pth.startswith(allowed_root_path):
                print(f"Skip {_pth} not in {allowed_root_path}")
                continue
            dirpath_list.append(_pth)

    print( dirpath_list, conf_path, additional_group_list, allowed_root_path)
    return dirpath_list, conf_path, additional_group_list, allowed_root_path


class PermissionManagerWindow(BaseAppForm, Ui_MainWindow):

    sigDirPathListChanged = pyqtSignal(list)

    def __init__(self, version: str, configpath: str):
        super(PermissionManagerWindow, self).__init__()
        self._version = version
        self.setWindowTitle("Permission Manager")
        self.setAppTitle("Permission Manager")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Permission Manager</h4>
            <p>This app is created to manage the AP file/folder permissions, current version is {}.
            </p>
            <p>Copyright (C) 2023 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)
        self.postInitUi()

        #
        self.dirpath_list, self.conf_path, self.additional_group_list, self.allowed_root_path,= \
                read_config(configpath)

        self.sigDirPathListChanged.connect(self.on_dirpath_list_changed)

        #
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_refresh)
        self.timer.start(5000)
        #
        self.sigDirPathListChanged.emit(self.dirpath_list)
        QTimer.singleShot(0, lambda:self.on_refresh())
        #

    @pyqtSlot()
    def onOpen(self):
        """Open a folder.
        """
        folderpath = get_open_directory(self)
        if folderpath.startswith(self.allowed_root_path):
            self.dirpath_lineEdit.setText(folderpath)
        else:
            QMessageBox.warning(self, "Choose a Folder",
                                f"Please choose a folder under: '{allowed_root_path}'",
                                QMessageBox.Ok, QMessageBox.Ok)
            return

    def _get_folderpath(self):
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
        """Add a folderpath.
        """
        folderpath = self._get_folderpath()
        if folderpath is None:
            return
        if folderpath in self.dirpath_list:
            QMessageBox.warning(self, "Add Folderpath",
                    f"'{folderpath}' is already added and being managed.",
                    QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.dirpath_list.append(folderpath)
            with open(self.conf_path, "a") as fp:
                fp.write(folderpath)
                fp.write("\n")
            self.sigDirPathListChanged.emit(self.dirpath_list)

    @pyqtSlot()
    def onRemove(self):
        """Remove a folderpath.
        """
        folderpath = self._get_folderpath()
        if folderpath is None:
            return
        if folderpath not in self.dirpath_list:
            QMessageBox.warning(self, "Remove Folderpath",
                    f"'{folderpath}' is not being managed.",
                    QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.dirpath_list.remove(folderpath)
            self.sigDirPathListChanged.emit(self.dirpath_list)
            with open(self.conf_path, "w") as fp:
                fp.write("# A list of directory path for Permission Manager.\n")
                fp.writelines("\n".join(self.dirpath_list))

    @pyqtSlot()
    def on_refresh(self):
        """Refresh the dirpath permissions.
        """
        print("Refresh...")
        self._layout_paths(self.dirpath_list, self.live_area, enable_checkbox=False)

    @pyqtSlot(list)
    def on_dirpath_list_changed(self, dirpath_list: list):
        """Post the dirpath permission info config.
        """
        self._layout_paths(dirpath_list, self.config_area, enable_checkbox=True,
                           groups=self.additional_group_list)

    def _layout_paths(self, dirpath_list, area, enable_checkbox, groups=None):
        w = area.takeWidget()
        w.setParent(None)

        w = QWidget(self)
        w.setContentsMargins(0, 6, 0, 0)
        l = QGridLayout()
        # headers
        headers = ("", "Path", "User", "R", "W", "X", "Group", "R", "W", "X",
                   "|", "R", "W", "X")
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
        for i, d in enumerate(dirpath_list, 1):
            _u, _g, _u_perm, _g_perm, _o_perm, _fullpath = get_perm(d)
            # print(_fullpath, _u, _g, _u_perm, _g_perm, _o_perm)

            _path_lbl = QLabel(_fullpath, self)
            _path_lbl.setTextInteractionFlags(
                    Qt.LinksAccessibleByMouse | Qt.TextSelectableByMouse)

            _u_lbl = QLabel(_u, self)
            _u_r = QCheckBox(self)
            _u_r.setChecked(_u_perm[0]=='r')
            _u_r.setEnabled(enable_checkbox)
            _u_w = QCheckBox(self)
            _u_w.setChecked(_u_perm[1]=='w')
            _u_w.setEnabled(enable_checkbox)
            _u_x = QCheckBox(self)
            _u_x.setChecked(_u_perm[2]=='x')
            _u_x.setEnabled(enable_checkbox)

            if groups is not None:
                if _g not in groups:
                    groups.insert(0, _g)
                _g_lbl = QComboBox(self)
                _g_lbl.addItems(groups)
                _g_lbl.setCurrentText(_g)
            else:
                _g_lbl = QLabel(_g, self)

            _g_r = QCheckBox(self)
            _g_r.setChecked(_g_perm[0]=='r')
            _g_r.setEnabled(enable_checkbox)
            _g_w = QCheckBox(self)
            _g_w.setChecked(_g_perm[1]=='w')
            _g_w.setEnabled(enable_checkbox)
            _g_x = QCheckBox(self)
            _g_x.setChecked(_g_perm[2]=='x')
            _g_x.setEnabled(enable_checkbox)

            _o_r = QCheckBox(self)
            _o_r.setChecked(_o_perm[0]=='r')
            _o_r.setEnabled(enable_checkbox)
            _o_w = QCheckBox(self)
            _o_w.setChecked(_o_perm[1]=='w')
            _o_w.setEnabled(enable_checkbox)
            _o_x = QCheckBox(self)
            _o_x.setChecked(_o_perm[2]=='x')
            _o_x.setEnabled(enable_checkbox)

            _o_line = QFrame(self)
            _o_line.setFrameShape(QFrame.VLine)
            _o_line.setFrameShadow(QFrame.Plain)
            for j, _w in enumerate((QLabel(str(i), self),
                                    _path_lbl,
                                    _u_lbl, _u_r, _u_w, _u_x,
                                    _g_lbl, _g_r, _g_w, _g_x,
                                    _o_line, _o_r, _o_w, _o_x)):
                if j == 0:
                    _w.setStyleSheet("""
                    QLabel {
                        border-top: 0px solid gray;
                        border-right: 5px solid gray;
                    }
                    """)
                l.addWidget(_w, i, j)
        #
        _vspacer = QWidget()
        _vspacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        l.addWidget(_vspacer, i + 1, 1)
        w.setLayout(l)
        area.setWidget(w)


def get_perm(d: str):
    r = subprocess.run(["ls", "-ld", os.path.expanduser(d)],
                       capture_output=True)
    s = r.stdout.strip().decode()
    _perm = s.split()[0][1:]
    _u = s.split()[2]
    _u_perm = list(_perm[:3])
    _g = s.split()[3]
    _g_perm = list(_perm[3:6])
    _o_perm = list(_perm[6:])
    _filepath = s.split()[-1]
    return _u, _g, _u_perm, _g_perm, _o_perm, _filepath

