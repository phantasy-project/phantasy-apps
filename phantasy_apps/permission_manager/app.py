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
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QLabel, QCheckBox, QComboBox
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QSizePolicy, QGridLayout
from PyQt5.QtWidgets import QFrame

from phantasy_ui import BaseAppForm
from phantasy_ui import get_open_directory
from .ui.ui_app import Ui_MainWindow


REFRESH_INTERVAL = 5000 # ms

_HELP_TEXT = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body style=" font-family:'Cantarell'; font-size:12pt; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:14pt; font-style:italic;">Permission Manager</span><span style=" font-size:14pt;"> is created to provide a convenient way to configure and monitor folder permissions recursively.</span><span style=" font-size:14pt;"> </span></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:14pt;">The area of &quot;</span><span style=" font-size:14pt; font-weight:600;">Live</span><span style=" font-size:14pt;">&quot; is for showing the live permissions of the folders being managed.</span><span style=" font-size:14pt;"> </span></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:14pt;">The area of &quot;</span><span style=" font-size:14pt; font-weight:600;">Config</span><span style=" font-size:14pt;">&quot; is for configuring the desired folder permissions through user interactions.</span><span style=" font-size:14pt;"> </span></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:14pt;">If the live permission matches the configured one, a </span><span style=" font-size:14pt; font-weight:600; color:#00aa00;">green</span><span style=" font-size:14pt; color:#00aa00;"> </span><span style=" font-size:14pt;">check icon will be posted, otherwise, a </span><span style=" font-size:14pt; font-weight:600; color:#ff0000;">red</span><span style=" font-size:14pt;"> cross icon will be shown.</span><span style=" font-size:14pt;"> </span></p>
<ul style="margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;"><li style=" font-size:14pt;" style=" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">To add a new folder: click the <span style=" font-style:italic;">Browse</span> button, then click the <span style=" font-style:italic;">Add</span> button. </li>
<li style=" font-size:14pt;" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">​To remove a folder from the list: Copy or choose the folder path into the input box, then click the <span style=" font-style:italic;">Remove</span> button. </li>
<li style=" font-size:14pt;" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">To change the permissions: check/uncheck the permission checkboxes in the &quot;<span style=" font-weight:600;">Config&quot;</span> area for each folder path. </li>
<li style=" font-size:14pt;" style=" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">To change the group: select the wanted group name from the dropdown menu in the &quot;<span style=" font-weight:600;">Config</span>&quot; area for each folder path. </li></ul>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:14pt; font-weight:600;">Please note:</span><span style=" font-size:14pt;"> </span></p>
<ul style="margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;"><li style=" font-size:14pt;" style=" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">​</span>It will take up to at least <span style=" font-weight:600;">1</span> minute to see the updated live permissions. </li>
<li style=" font-size:14pt;" style=" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">​Read (R) and executable (X) usually come and go together, so do not just change a single one.</li></ul></body></html>
"""


class _Perm:
    # line: <dirpath>;user,775, group
    def __init__(self, line: str):
        _path, _perm_s = line.split(";")
        self.fullpath = os.path.abspath(os.path.expanduser(_path))
        self.user, self.group, self.u_perm, self.g_perm, self.o_perm, _ = \
                self._get_perm(self.fullpath, _perm_s)

    def _get_perm(self, fullpath: str, perm_s: str):
        """Get the config permissions of *fullpath* from *perm_s*, if perm_s is '', get the live perms.
        """
        if perm_s == '':
            return self.get_live_perms()
        else:
            # path;user,775,group
            _usr, perm_, _grp = perm_s.split(",")
            bin_list = list(bin(int(perm_, 8)))[2:]
            perm_u = [j if i == '1' else '-' for i, j in zip(bin_list[:3], list('rwx'))]
            perm_g = [j if i == '1' else '-' for i, j in zip(bin_list[3:6], list('rwx'))]
            perm_o = [j if i == '1' else '-' for i, j in zip(bin_list[6:], list('rwx'))]
            return _usr, _grp.strip(), perm_u, perm_g, perm_o, fullpath

    def is_set(self):
        """Return True if live perm matches config perm, otherwise return False.
        """
        _l = str(self.get_live_perms()).replace('s', 'x')
        _r = str(self.get_conf_perms()).replace('s', 'x')
        return _l == _r

    def __str__(self):
        perm_list = self.u_perm + self.g_perm + self.o_perm
        _s_bin = ''.join([{'r':'1','w':'1','x':'1','-':'0','s':'1'}.get(i) for i in perm_list])
        return f"{self.fullpath};{self.user},{oct(int(_s_bin, 2))},{self.group}"

    def get_live_perms(self):
        """Return a tuple of live folder permissions.
        """
        return get_perm(self.fullpath)

    def get_conf_perms(self):
        """Return a tuple of config folder permissions.
        """
        return self.user, self.group, self.u_perm, self.g_perm, self.o_perm, self.fullpath

    def change_conf_perm(self, i: str, j: str, enabled: bool):
        """Change the config permission for j bit of i, i could be 'u', 'g' or 'o',
        'j' could be 'r', 'w' or 'x'.
        """
        _perm = {'u': self.u_perm, 'g': self.g_perm, 'o': self.o_perm}.get(i)
        _perm[list('rwx').index(j)] = '-' if not enabled else j


def read_config(configpath: str):
    _c = toml.load(configpath)
    _use_conf = _c[_c['default']['use']]

    conf_path = _use_conf['CONF_PATH']
    allowed_root_path = _use_conf['ALLOWED_ROOT_PATH']
    additional_group_list = _use_conf['ADDITIONAL_GROUP_LIST']

    perm_list = []
    if not os.path.isfile(conf_path):
        with open(conf_path, "w") as fp:
            fp.write("# A list of directory path for Permission Manager.\n")
            fp.flush()
        os.chmod(conf_path, 0o664)
    else:
        for line in open(conf_path, "r"):
            if line.startswith("#"):
                continue
            _pth = os.path.abspath(os.path.expanduser(line.split(';')[0].strip()))
            if Path(allowed_root_path) not in Path(_pth).parents:
                print(f"Skip {_pth} not in {allowed_root_path}")
                continue
            perm_list.append(_Perm(line))

    return perm_list, conf_path, additional_group_list, allowed_root_path


class PermissionManagerWindow(BaseAppForm, Ui_MainWindow):

    # a list of dirpaths for permission management configs
    # each one is _Perm instance
    sigPermListChanged = pyqtSignal(list)

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

        # help
        self._hint_dlg = None
        #
        self.perm_list, self.conf_path, self.additional_group_list, self.allowed_root_path,= \
                read_config(configpath)
        # logdir
        self.logdirpath = Path(self.conf_path).parent.joinpath(".pm-logs")
        #
        self.allowed_root_path_lineEdit.setText(self.allowed_root_path)

        self.sigPermListChanged.connect(self.on_perm_list_changed)

        #
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_refresh)
        self.timer.start(REFRESH_INTERVAL)
        #
        self.sigPermListChanged.emit(self.perm_list)
        QTimer.singleShot(0, lambda:self.on_refresh())
        #

    @pyqtSlot()
    def onOpen(self):
        """Open a folder.
        """
        folderpath = get_open_directory(self, cdir=self.allowed_root_path)
        if Path(self.allowed_root_path) in Path(folderpath).parents:
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
        if folderpath in [i.fullpath for i in self.perm_list]:
            QMessageBox.warning(self, "Add Folderpath",
                    f"'{folderpath}' is already added and being managed.",
                    QMessageBox.Ok, QMessageBox.Ok)
        else:
            _perm = _Perm(f"{folderpath};")
            self.perm_list.append(_perm)
            with open(self.conf_path, "a") as fp:
                fp.write(str(_perm) + "\n")
                fp.flush()
            self.sigPermListChanged.emit(self.perm_list)
        self.dirpath_lineEdit.clear()

    @pyqtSlot()
    def onRemove(self):
        """Remove a folderpath.
        """
        folderpath = self._get_folderpath()
        if folderpath is None:
            return
        if folderpath not in [i.fullpath for i in self.perm_list]:
            QMessageBox.warning(self, "Remove Folderpath",
                    f"'{folderpath}' is not being managed.",
                    QMessageBox.Ok, QMessageBox.Ok)
        else:
            for i, o in enumerate(self.perm_list):
                if o.fullpath == folderpath:
                    self.perm_list.pop(i)
                    del o
            self.write_conf()
            self.sigPermListChanged.emit(self.perm_list)
        self.dirpath_lineEdit.clear()

    @pyqtSlot()
    def on_refresh(self):
        """Refresh the dirpath permissions.
        """
        self._layout_paths(self.perm_list, self.live_area, is_live=True)

    @pyqtSlot(list)
    def on_perm_list_changed(self, perm_list: list):
        """Post the dirpath permission info config, not live permissions.
        """
        self._layout_paths(perm_list, self.config_area, is_live=False,
                           groups=self.additional_group_list)

    def _layout_paths(self, perm_list, area, is_live=False, groups=None):
        """List all the dirpaths with config management rules, each folderpath one line.

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
            headers = ("", "Path", "Match?", "Last Refreshed", "User", "R", "W", "X", "Group", "R", "W", "X",
                       "|", "R", "W", "X")
        else:
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
        for i, d in enumerate(perm_list, 1):
            if is_live:
                _u, _g, _u_perm, _g_perm, _o_perm, _fullpath = d.get_live_perms()
            else:
                _u, _g, _u_perm, _g_perm, _o_perm, _fullpath = d.get_conf_perms()

            # dirpath
            _path_lbl = QLabel(_fullpath, self)
            _path_lbl.setTextInteractionFlags(
                    Qt.LinksAccessibleByMouse | Qt.TextSelectableByMouse)

            if is_live:
                # match?
                _match_lbl = QLabel(self)
                if d.is_set():
                    _match_lbl.setPixmap(QPixmap(":/_misc/match.png").scaled(32, 32))
                else:
                    _match_lbl.setPixmap(QPixmap(":/_misc/not-match.png").scaled(32, 32))
                # refreshing? or Refreshed
                _refresh_status = self.logdirpath.joinpath(
                        _fullpath.replace("/", "_") + '.log').read_text().strip()
                if _refresh_status.startswith("Refreshed"):
                    _refresh_date = _refresh_status.split()[-1][:-4]
                else:
                    _refresh_date = "Refreshing..."
                _sts_lbl = QLabel(self)
                _sts_lbl.setText(_refresh_date)
                _sts_lbl.setToolTip(_refresh_status)

            # user
            _u_lbl = QLabel(_u, self)
            # user, r,w,x
            _u_r = QCheckBox(self)
            _u_r.setChecked(_u_perm[0]=='r')
            _u_w = QCheckBox(self)
            _u_w.setChecked(_u_perm[1]=='w')
            _u_x = QCheckBox(self)
            _u_x.setChecked(_u_perm[2] in ('x', 's'))

            # group
            if groups is not None:
                _g_lbl = QComboBox(self)
                _g_lbl.addItems(groups)
                _g_lbl.addItem(_u)
                _g_lbl.setCurrentText(_g)
                _g_lbl.currentTextChanged.connect(partial(self.on_group_conf_changed, d))
            else:
                _g_lbl = QLabel(_g, self)

            # group, r,w,x
            _g_r = QCheckBox(self)
            _g_r.setChecked(_g_perm[0]=='r')
            _g_w = QCheckBox(self)
            _g_w.setChecked(_g_perm[1]=='w')
            _g_x = QCheckBox(self)
            _g_x.setChecked(_g_perm[2] in ('x', 's'))

            # vline before other perms.
            _v_line = QFrame(self)
            _v_line.setFrameShape(QFrame.VLine)
            _v_line.setFrameShadow(QFrame.Plain)

            # other, r,w,x
            _o_r = QCheckBox(self)
            _o_r.setChecked(_o_perm[0]=='r')
            _o_w = QCheckBox(self)
            _o_w.setChecked(_o_perm[1]=='w')
            _o_x = QCheckBox(self)
            _o_x.setChecked(_o_perm[2] in ('x', 's'))

            # config checkboxes
            for _o, _o_t in zip(
                    (_u_r, _u_w, _u_x,
                     _g_r, _g_w, _g_x,
                     _o_r, _o_w, _o_x),
                    (('u', 'r'), ('u', 'w'), ('u', 'x'),
                     ('g', 'r'), ('g', 'w'), ('g', 'x'),
                     ('o', 'r'), ('o', 'w'), ('o', 'x'))
                ):
                _o.setEnabled(enable_checkbox)
                if enable_checkbox: # support change perms
                    _o.stateChanged.connect(partial(self.on_perm_conf_changed, d, _o_t))

            # place a row for d
            if is_live:
                w_list = (QLabel(str(i), self),
                          _path_lbl,
                          _match_lbl, _sts_lbl,
                          _u_lbl, _u_r, _u_w, _u_x,
                          _g_lbl, _g_r, _g_w, _g_x, _v_line,
                          _o_r, _o_w, _o_x)
            else:
                w_list = (QLabel(str(i), self),
                          _path_lbl,
                          _u_lbl, _u_r, _u_w, _u_x,
                          _g_lbl, _g_r, _g_w, _g_x, _v_line,
                          _o_r, _o_w, _o_x)
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

    @pyqtSlot('QString')
    def on_group_conf_changed(self, perm: _Perm, group: str):
        """The group is changed.
        """
        perm.group = group
        self.write_conf()

    @pyqtSlot(int)
    def on_perm_conf_changed(self, perm: _Perm, perm_bit_tuple: tuple, state: int):
        """Change the config permission of *perm* for *perm_bit_tuple*,
        perm_bit_tuple is a tuple of e.g. ('i', 'j'), i could be 'u','g','o', j could be 'r','w','x'.
        """
        perm.change_conf_perm(*perm_bit_tuple, state==Qt.Checked)
        self.write_conf()

    def write_conf(self):
         # update file
        with open(self.conf_path, "w") as fp:
            fp.write("# A list of directory path for Permission Manager.\n")
            fp.writelines("\n".join((str(i) for i in self.perm_list)))
            fp.write("\n")
            fp.flush()

    @pyqtSlot()
    def onHint(self):
        """Show a brief text as the help.
        """
        if self._hint_dlg is None:
            self._hint_dlg = QTextEdit()
            self._hint_dlg.setHtml(_HELP_TEXT)
            self._hint_dlg.setReadOnly(True)
            self._hint_dlg.setWindowTitle("Permission Manager - Help")
            self._hint_dlg.setStyleSheet("""QTextEdit {
                border-top: 0px solid gray;
                border-bottom: 5px solid gray;
                border-right: 5px solid gray;
                border-left: 0px solid gray;}""")
        self._hint_dlg.show()
        self._hint_dlg.resize(880, 650)


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
