# -*- coding: utf-8 -*-

import importlib
import os
import toml
from collections import OrderedDict

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QFile
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel

from phantasy_apps.utils import find_dconf as _find_dconf


def find_dconf(path=None, filename='app_launcher.ini'):
    """Find parameter configuration for `app_launcher` if `path` is None.
    searching the following locations:
    * ~/.phantasy/app_launcher.ini
    * /etc/phantasy/app_launcher.ini
    * package location: apps/app_launcher/config/app_launcher.ini
    """
    if path is not None:
        return os.path.abspath(path)
    return _find_dconf('app_launcher', filename)


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
        for app in self._app_items.values():
            item_name = QStandardItem(app.name)
            item_name.cmd = app.cmd
            item_name.icon = icon = QIcon(QPixmap(app.icon_path))
            item_name.icon_console = QIcon(self.px_console)
            item_name.setIcon(icon)

            item_cat = QStandardItem(app.groups[0])
            text = item_cat.text()
            if text == 'stable':
                px = self.px_catpub
                tp = "App access is public"
            elif text == 'devel':
                px = self.px_catlim
                tp = "App access is limited"
            item_cat.setText('')
            item_cat.setToolTip(tp)
            item_cat.setTextAlignment(Qt.AlignCenter)
            item_cat.setData(px.scaled(24, 24), Qt.DecorationRole)

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
    def __init__(self, name, desc, cmd, icon_path, groups, version, helpdoc):
        # name : app name
        # desc : app descriptiono
        # cmd : command to start up app (exec)
        # icon_path : icon path for app icon (icon)
        # groups : a list of affiliated groups
        # helpdoc : path for help doc
        super(self.__class__, self).__init__()
        self.name = name
        self.desc = desc
        self.cmd = cmd
        self.icon_path = icon_path
        self.groups = groups
        self.ver = version
        self.helpdoc = helpdoc

    def __contains__(self, item):
        item = item.lower()
        if item in self.name.lower() or item.lower() in self.desc.lower() \
           or item in self.cmd.lower() or item in self.ver.lower() \
           or item in ' '.join(self.groups).lower():
               return True
        else:
            return False

    def __repr__(self):
        return f"AppItem({self.name}, {self.desc[:10]}..., {self.cmd[:10]}..., {self.icon_path[:10]}..., {self.groups}, {self.ver})"


def get_app_version(pkg_path):
    if isinstance(pkg_path, list):
        pkg_path = '.'.join(pkg_path)
    try:
        module = importlib.import_module(pkg_path)
    except ImportError:
        ver = "Unknown"
    else:
        ver = module.__version__
    finally:
        return ver


def get_app_data(path=None, filename='app_launcher.ini'):
    """Return a dict of app data, key: name, value: AppItem
    """
    # app conf
    path_conf = find_dconf(path, filename)
    conf = toml.load(path_conf)

    title = conf.pop('title')
    imp_path_conf = conf.pop('CONFIG_PATH')
    app_default_conf = conf.pop('APP-DEFAULT')
    default_icon_path = app_default_conf['icon']
    default_groups = app_default_conf['groups']

    data = OrderedDict()
    for k, v in conf.items():
        icon_path = v.get('icon', default_icon_path)
        icon_path = config_icon_path(icon_path, os.path.dirname(path_conf))
        groups = v.get('groups', default_groups[:])
        version = v.get('version', get_app_version(imp_path_conf.get(k, 'undefined')))
        helpdoc = v.get('helpdoc', '')
        app_item = AppItem(v.get('name'), v.get('desc'), v.get('exec'), icon_path,
                           groups, version, helpdoc)
        data.update([(app_item.name, app_item)])

    return data

def config_icon_path(icon_path, conf_path):
    # 1. if in conf_path/icons
    # 2. if in <app_name>/config/icons
    icon_path0 = os.path.join(conf_path, 'icons', icon_path)
    if os.path.isfile(icon_path0):
        return icon_path0
    else:
        basedir = os.path.abspath(os.path.dirname(__file__))
        icon_path1 = os.path.join(basedir, "config", "icons", icon_path)
        if os.path.isfile(icon_path1):
            return icon_path1
        else:
            return os.path.join(basedir, "config", "icons", "default.png")


if __name__ == '__main__':
    from PyQt5.QtWidgets import QWidget, QTableView, QTextEdit, QVBoxLayout
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QSize
    import sys
    from subprocess import Popen

    data = get_app_data(filename='app_launcher.ini')

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
