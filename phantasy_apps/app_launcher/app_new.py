#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QWidget

from subprocess import Popen
from functools import partial
import os
import pwd

from phantasy_ui import BaseAppForm

from .ui.ui_app_cardview import Ui_MainWindow
from .app_add import AddLauncherDialog
from .utils import get_app_data
from .app_log import LogWidget
from .layout import FlowLayout
from .app_card import AppCard
from .app_card import AppCardInfoForm


class AppLauncherWindow(BaseAppForm, Ui_MainWindow):

    def __init__(self, version, **kws):
        super(AppLauncherWindow, self).__init__()

        # logfile
        self._logfile = kws.get('logfile', None)
        #print("logfile: ", self._logfile)
        self._logwidget = None

        # config filepath
        config_file = kws.get('config', None)
        self._app_data = get_app_data(config_file)

        # app version
        self._version = version

        # window title/version
        self.setWindowTitle("App Launcher")

        # set app properties
        self.setAppTitle("App Launcher")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Launcher App</h4>
            <p>This app features the access portal of the available
            physics apps for FRIB, current version is {}.
            </p>
            <p>Copyright (C) 2019 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

        # debug
        self._debug = False

        #
        self._margin = 20
        self._spacing = 40
        self._width = 300
        #
        # value: {name: AppCard}
        self._app_card_dict = { 'fav': {}, 'fav1': {}, 'all': {} }
        # value: {name: (info_form, on/off, sender, iidx)}
        self._info_form_dict = {'fav': {}, 'fav1': {}, 'all': {} }
        self._layout_dict = {'fav': None, 'fav1': None, 'all': None}
        self._area_dict = {'fav': self.fav_scrollArea,
                           'fav1': self.fav1_scrollArea,
                           'all': self.all_apps_scrollArea,
                           'grps': self.grps_scrollArea,}
        self._apps_tab_page = {0: 'all', 1: 'fav1', 2: 'grps'}

        # post init ui
        self.post_init_ui()

        #
        self.adjustSize()

    def on_launch_app(self, index, **kws):
        # slot
        item = self.v.model().item(index.row(), 0)
        if kws.get('detached', False):
            cmdline = "x-terminal-emulator -e " + item.cmd
        else:
            cmdline = item.cmd
        Popen(cmdline, shell=True)

    def on_custom_menu_request(self, pos):
        index = self.v.indexAt(pos)
        menu = QMenu(self)
        item00 = self.v.model().item(index.row(), 0)
        icon1 = item00.icon
        icon2 = item00.icon_console
        act1 = QAction(icon1, "Start App", menu)
        act2 = QAction(icon2, "Start App w/ Console", menu)
        menu.addAction(act1)
        menu.addAction(act2)
        menu.popup(self.v.viewport().mapToGlobal(pos))
        act1.triggered.connect(partial(self.on_launch_app, index))
        act2.triggered.connect(partial(self.on_launch_app, index, detached=True))

    @pyqtSlot(int)
    def on_current_changed(self, nested, i):
        self.clear_info_form(self._current_page)
        if not nested:
            if i == 0:
                page = 'fav'
            else:
                page = self._apps_tab_page[self.apps_tab.currentIndex()]
        else:
            page = self._apps_tab_page[i]
        self._current_page = page
        self.set_page(page)

    def clear_info_form(self, page):
        # TODO
        if page == 'grps':
            return
        #
        if page == -1:
            return
        # clear info forms.
        del_names = []
        for k, v in self._info_form_dict[page].items():
            info_form, show, _, iidx = v
            if show:
                layout = self._layout_dict[page]
                w = layout.itemAt(iidx).widget()
                layout.removeWidget(w)
                w.sig_close.emit()
                w.setParent(None)
                del_names.append(k)
        for i in del_names:
            self._info_form_dict[page].pop(i)

    def set_page(self, page):
        # TODO
        if page == 'grps':
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Group Page", "To be implemeneted",
                    QMessageBox.Ok)
            return
        #
        area = self._area_dict[page]
        w = area.takeWidget()
        w.setParent(None)
        w = QWidget(self)
        w.setContentsMargins(0, self._margin, 0, self._margin)
        layout = FlowLayout(spacing=self._spacing)
        self._layout_dict[page] = layout
        for name, app_item in self._app_data.items():
            groups = app_item.groups
            cmd = app_item.cmd
            desc = app_item.desc
            ver = app_item.ver
            fav_on = 'favorite' in groups
            if page in ['fav', 'fav1'] and not fav_on:
                continue
            card = AppCard(name, groups, cmd, fav_on, desc, ver, self, width=self._width)
            card.setIcon(app_item.icon_path)
            card.infoFormChanged.connect(partial(self.on_info_form_changed, page))
            card.favChanged.connect(self.on_fav_changed)
            self._app_card_dict[page][name] = card
            layout.addWidget(card)
        w.setLayout(layout)
        area.setWidget(w)

        # update cnt
        for i in range(self.apps_tab.count()):
            area = self._area_dict[self._apps_tab_page[i]]
            layout = area.findChildren(FlowLayout)
            if layout == []:
                continue
            self.apps_tab.setTabText(i, '{} ({})'.format(
                self.apps_tab.tabText(i).split(' ')[0], layout[0].count()))

    def sizeHint(self):
        return QSize(1600, 1200)

    def post_init_ui(self):
        # uid
        self.set_greetings()

        self._current_page = -1
        self.apps_tab.currentChanged.connect(partial(self.on_current_changed, True))
        self.main_tab.currentChanged.connect(partial(self.on_current_changed, False))
        self.main_tab.currentChanged.emit(self.main_tab.currentIndex())

        # log/debug
        for o in (self.show_log_btn, self.enable_debug_btn,):
            o.setVisible(False)
        self.search_btn.toggled.emit(self.search_btn.isChecked())

    @pyqtSlot(dict, bool)
    def on_info_form_changed(self, page, meta_info, show):
        name = meta_info['name']
        if name not in self._info_form_dict[page]:
            group = meta_info['groups'][0]
            fav_on = meta_info['fav']
            desc = meta_info['desc']
            info_form = AppCardInfoForm(name, group, fav_on, desc)
            card = self._app_card_dict[page][name]
            info_form.favChanged.connect(card.on_fav_changed)
            info_form.sig_close.connect(card.on_close_info)
            info_form.runAppInTerminal.connect(card.on_launch_app)
            card.favChanged.connect(info_form.on_fav_changed)
            self._info_form_dict[page][name] = [info_form, True, self.sender(), None]

        if show:
            for k, v in self._info_form_dict[page].items():
                if k == name: continue
                v[1] = False
        else:
            self._info_form_dict[page][name][1] = False

        self.place_info_form(page)

    def place_info_form(self, page):
        #
        area = self._area_dict[page]
        layout = self._layout_dict[page]
        #
        del_names = []
        for k, v in self._info_form_dict[page].items():
            info_form, show, sender, iidx = v
            n = self._get_row_item_count(area, self._spacing, self._width)

            if show:
                idx = layout.indexOf(sender)
                iidx = (1 + idx // n) * n
                iidx = min(iidx, layout.count())
                info_form.setFixedWidth(
                    n * (self._spacing + self._width) - self._spacing)
                layout.insertWidget(iidx, info_form)
                v[3] = iidx
            else:
                w = layout.itemAt(iidx).widget()
                layout.removeWidget(w)
                w.sig_close.emit()
                w.setParent(None)
                del_names.append(k)

        for i in del_names:
            self._info_form_dict[page].pop(i)

    def resizeEvent(self, evt):
        QMainWindow.resizeEvent(self, evt)
        self.place_info_form(self._current_page)

    @pyqtSlot()
    def on_add_launcher(self):
        """[VOID] Add new button as app launcher.
        """
        idx = self.horizontalLayout.count()
        self._dlg = AddLauncherDialog()
        r = self._dlg.exec_()
        if r == QDialog.Accepted and self._dlg.launcher is not None:
            launcher = self._dlg.launcher
            btn = launcher.button
            self.horizontalLayout.insertWidget(idx - 1, btn)

            btn.clicked.connect(partial(self.on_launch_app, launcher.cmd))
            btn.installEventFilter(self)
            MSG.update({launcher.name: (launcher.name, launcher.desc)})

        else:
            return

    @pyqtSlot(bool)
    def on_enable_debug(self, f):
        """Enable debug mode or not.
        """
        self._debug = f
        print("Debug is enabled?", self._debug)

    @pyqtSlot()
    def on_show_log(self):
        """Show log message under debug mode.
        """
        print("Show log message.")
        if self._logwidget is None:
            self._logwidget = LogWidget(self._logfile)
        self._logwidget.show()

    def closeEvent(self, e):
        QMainWindow.closeEvent(self, e)

    @staticmethod
    def _get_row_item_count(area, spacing, item_width):
        wd = area.viewport().width()
        xn = (wd + spacing) / (spacing + item_width)
        if xn - int(xn) >= 0.99:
            n = int(xn) + 1
        else:
            n = int(xn)
        return n

    def set_greetings(self):
        s = pwd.getpwuid(os.getuid())
        try:
            u = s[4].strip(',')
            assert u != ''
        except AssertionError:
            u = s[0]
        finally:
            self.greetings_lbl.setText("Welcome {}!".format(u.title()))

    @pyqtSlot(bool)
    def on_fav_changed(self, on):
        name = self.sender().name()
        if on:
            self._app_data[name].groups.append('favorite')
        else:
            self._app_data[name].groups.remove('favorite')

    @pyqtSlot('QString')
    def on_search_updated(self, s):
        print("searching: ", s)
