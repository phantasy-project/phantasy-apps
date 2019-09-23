# -*- coding: utf-8 -*-

import os

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel

from phantasy_apps.utils import find_dconf as _find_dconf

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser

DEFAULT_ICON_PATH = "/usr/share/phantasy/assets/icons/default.png"


def find_dconf(path=None):
    """Find parameter configuration for `app_launcher` if `path` is None.
    searching the following locations:
    * ~/.phantasy/app_launcher.ini
    * /etc/phantasy/app_launcher.ini
    * package location: apps/app_launcher/config/app_launcher.ini
    """
    if path is not None:
        return os.path.abspath(path)
    return _find_dconf('app_launcher', 'app_launcher.ini')


class AppDataModel(QStandardItemModel):
    """App data model.

    """
    def __init__(self, parent, app_items, **kws):
        # app_items: list of AppItem instances.
        super(self.__class__, self).__init__(parent)
        self._v = parent
        self._app_items = app_items

        # header
        self.header = self.h_name, self.h_cat, self.h_desc, self.h_ver = \
                ('Name', '', 'Description', 'Version')
        self.ids = self.i_name, self.i_cat, self.i_desc, self.i_ver = \
                range(len(self.header))

        #
        self.px_catpub = QPixmap(":/icons/public.png")
        self.px_catlim = QPixmap(":/icons/limited.png")
        self.px_console = QPixmap(":/icons/console.png")

    def set_header(self):
        for i, s in zip(self.ids, self.header):
            self.setHeaderData(i, Qt.Horizontal, s)

    def set_data(self):
        for app in self._app_items:
            item_name = QStandardItem(app.name)
            item_name.cmd = app.cmd
            item_name.icon = icon = QIcon(QPixmap(app.icon_path))
            item_name.icon_console = QIcon(self.px_console)
            item_name.setIcon(icon)

            item_cat = QStandardItem(app.category)
            text = item_cat.text()
            if text == 'Public':
                px = self.px_catpub
                tp = "App access is public"
            elif text == 'Limited':
                px = self.px_catlim
                tp = "App access is limited"
            item_cat.setText('')
            item_cat.setToolTip(tp)
            item_cat.setTextAlignment(Qt.AlignCenter)
            item_cat.setData(px.scaled(32, 32), Qt.DecorationRole)

            item_desc = QStandardItem(app.desc)
            item_ver = QStandardItem(app.ver)
            #
            row = (item_name, item_cat, item_desc, item_ver)
            [i.setEditable(False) for i in row]
            self.appendRow(row)

    def set_model(self):
        self.set_data()
        self.set_header()
        self._v.setModel(self)
        self.__post_init_ui(self._v)

    def __post_init_ui(self, v):
        # view properties
        #v.setStyleSheet("font-family: monospace;")
        v.setIconSize(QSize(24, 24))
        v.setAlternatingRowColors(True)
        try:
            # tree
            v.header().setStretchLastSection(True)
        except:
            # table
            v.horizontalHeader().setStretchLastSection(True)
        v.setSortingEnabled(True)
        self.sort(self.i_name, Qt.AscendingOrder)
        for i in self.ids:
            v.resizeColumnToContents(i)
        for i in range(self.rowCount()):
            v.resizeRowToContents(i)
        #v.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #v.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


class AppItem(object):
    def __init__(self, name, desc, cmd, icon_path, category=None, version=None):
        # name : app name
        # desc : app descriptiono
        # cmd : command to start up app
        # icon_path : icon path for app icon
        # category : category of app, default is 'Limited'
        super(self.__class__, self).__init__()
        self.name = name
        self.desc = desc
        self.cmd = cmd
        self.icon_path = icon_path
        self.category = "Limited" if category is None else category
        if version is None:
            try:
                self.ver = get_app_version(name)
            except RuntimeError:
                self.ver = "0"
        else:
            self.ver = version


def get_app_version(name):
    if name == 'Correlation Visualizer':
        from phantasy_apps.correlation_visualizer import __version__ as ver
    elif name == 'Quad Scan App':
        from phantasy_apps.quad_scan import __version__ as ver
    elif name == 'Wire Scanner App':
        from phantasy_apps.wire_scanner import __version__ as ver
    elif name == 'Allison Scanner App':
        from phantasy_apps.allison_scanner import __version__ as ver
    elif name == 'Virtual Accelerator Launcher':
        from phantasy_apps.va import __version__ as ver
    elif name == 'Trajectory Viewer':
        from phantasy_apps.trajectory_viewer import __version__ as ver
    elif name == 'Trajectory Correction':
        from phantasy_apps.orm import __version__ as ver
    elif name == 'Unicorn App':
        from phantasy_apps.unicorn import __version__ as ver
    elif name == 'Lattice Viewer':
        from phantasy_apps.lattice_viewer import __version__ as ver
    elif name == 'Device Viewer':
        from phantasy_apps.diag_viewer import __version__ as ver
    elif name == 'PM Viewer':
        from phantasy_apps.pm_viewer import __version__ as ver
    elif name == 'Online Model':
        from phantasy_apps.online_model import __version__ as ver
    else:
        raise RuntimeError
    return ver


def get_app_data(path=None):
    """Return a list of app data.
    """

    # app conf
    path_conf = find_dconf(path)
    conf = ConfigParser()
    conf.read(path_conf)

    data = []
    for k,v in conf.items():
        if k == 'DEFAULT':
            continue
        icon_path = v.get('icon', DEFAULT_ICON_PATH)
        if not os.path.isfile(icon_path):
            icon_path = DEFAULT_ICON_PATH
        category = v.get('category', None)
        version = v.get('version', None)
        app_item = AppItem(k, v.get('desc'), v.get('exec'), icon_path,
                           category, version)
        data.append(app_item)

    return data


if __name__ == '__main__':
    from PyQt5.QtWidgets import QWidget, QTableView, QTextEdit, QVBoxLayout
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QSize
    import sys
    from subprocess import Popen

    data = get_app_data()

    class MyApp(QWidget):
        def __init__(self):
            super(self.__class__, self).__init__()

            v = QTableView(self)
            self.v = v
            model = AppDataModel(v, data)
            model.set_model()

            text_edit = QTextEdit(self)

            vbox = QVBoxLayout()
            vbox.addWidget(v, 1)
            vbox.addWidget(text_edit, 0)
            self.setLayout(vbox)

            # events
            self.v.doubleClicked.connect(self.on_launch_app)

        def on_launch_app(self, index):
            item = self.v.model().item(index.row(), 0)
            Popen(item.cmd, shell=True)

        def sizeHint(self):
            return QSize(800, 600)

    app = QApplication(sys.argv)
    w = MyApp()
    w.show()
    w.adjustSize()

    sys.exit(app.exec_())
