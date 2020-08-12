#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QVBoxLayout
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
        self._app_data = dict(sorted(get_app_data(config_file).items()))

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
        self._app_card_dict = { 'fav': {}, 'fav1': {}, 'all': {},
                                'search_apps': {}, 'search_fav': {}}
        # value: {name: (info_form, on/off, sender, iidx)}
        self._info_form_dict = {'fav': {}, 'fav1': {}, 'all': {},
                                'search_fav': {}, 'search_apps': {}}
        self._layout_dict = {'fav': None, 'fav1': None, 'all': None,
                             'search_fav': None, 'search_apps': None}
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
            cmdline = "gnome-terminal -- " + item.cmd
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
        self._nested = nested
        self._current_index = i
        self.clear_info_form(self._current_page)
        if not nested:
            if i == 0:
                page = 'fav'
            else:
                # quick fix for nest bit and page index
                self._nested = True
                self._current_index = self.apps_tab.currentIndex()
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
            helpdoc = app_item.helpdoc
            contact = app_item.contact
            if page in ['fav', 'fav1'] and not fav_on:
                continue
            card = AppCard(name, groups, cmd, fav_on, desc, ver, helpdoc, contact, self, width=self._width)
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

        self.search_btn.toggled.connect(partial(self.on_enable_search, True))
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
            ver = meta_info['ver']
            helpdoc = meta_info['helpdoc']
            contact = meta_info['contact']
            info_form = AppCardInfoForm(name, group, fav_on, desc, ver, helpdoc, contact)
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
                print(iidx, layout.count())
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
        matched_fav_items = []
        matched_other_items = []
        for name, item in self._app_data.items():
            if s in item:
                if 'favorite' in item.groups:
                    matched_fav_items.append(item)
                else:
                    matched_other_items.append(item)
        self.show_search_results(s, matched_fav_items, matched_other_items)

    def show_search_results(self, s, fav_items, other_items):
        if s == '':
            self.on_enable_search(False, False)
            return


        total_items = len(fav_items) + len(other_items)
        if self.main_tab.widget(2) is None:
            w = QWidget()
            self.main_tab.addTab(w, QIcon(QPixmap(":/icons/view_list.png")), 'Search')

            headtext_lbl = QLabel(w)
            headtext_lbl.setObjectName('headtext_lbl')
            headtext_lbl.setStyleSheet(
                    "QLabel {\n"
                    "    padding: 10px 10px 10px 0px;\n"
                    "    border-bottom: 1px solid gray;\n"
                    "    border-radius: 2px;\n"
                    "    font-size: 22pt;\n"
                    "    font-weight: bold;\n"
                    "}")
            headtext_lbl.setText("Search Results: '{}' ({})".format(s, total_items))
            layout = QVBoxLayout()
            layout.addWidget(headtext_lbl)

            # 404
            notfound_lbl = QLabel(w)
            notfound_lbl.setObjectName('notfound_lbl')
            notfound_lbl.setStyleSheet(
                    "QLabel {\n"
                    "    padding: 10px 10px 10px 0px;\n"
                    "    font-size: 22pt;\n"
                    "    color: gray;\n"
                    "}")
            notfound_lbl.setText("No items match your search.")
            layout.addWidget(notfound_lbl, stretch=1, alignment=Qt.AlignCenter)
            notfound_lbl.setVisible(False)

            # fav group
            fav_lbl = QLabel(w)
            fav_lbl.setText("Favorites")
            fav_lbl.setObjectName('fav_group_lbl')
            fav_lbl.setStyleSheet(
                    "QLabel {\n"
                    "    padding: 10px 10px 10px 0px;\n"
                    "    color: darkgreen;\n"
                    "    font-size: 20pt;\n"
                    "}")
            layout.addWidget(fav_lbl)
            fav_area = QScrollArea(w)
            fav_area.setObjectName('fav_area')
            fav_area.setWidgetResizable(True)
            layout.addWidget(fav_area, stretch=1)

            # apps group
            apps_lbl = QLabel(w)
            apps_lbl.setText("Apps")
            apps_lbl.setObjectName('apps_group_lbl')
            apps_lbl.setStyleSheet(
                    "QLabel {\n"
                    "    padding: 10px 10px 10px 0px;\n"
                    "    color: darkgreen;\n"
                    "    font-size: 20pt;\n"
                    "}")
            layout.addWidget(apps_lbl)
            apps_area = QScrollArea(w)
            apps_area.setObjectName('apps_area')
            apps_area.setWidgetResizable(True)
            layout.addWidget(apps_area, stretch=1)

            #
            layout.addStretch(0)
            w.setLayout(layout)
        else:
            w = self.main_tab.widget(2)
            w.findChild(QLabel, 'headtext_lbl').setText("Search Results: '{}' ({})".format(s, total_items))

        self.main_tab.currentChanged.disconnect()
        self.main_tab.setCurrentIndex(2)
        self.main_tab.currentChanged.connect(partial(self.on_current_changed, False))

        # show filtered items, group by Favorites and Apps
        fav_area = w.findChild(QScrollArea, 'fav_area')
        self._area_dict.update({'search_fav': fav_area})
        w1 = fav_area.takeWidget()
        if w1 is not None:
            w1.setParent(None)
        w1 = QWidget(w)
        w1.setContentsMargins(0, self._margin, 0, self._margin)
        layout = FlowLayout(spacing=self._spacing)
        self._layout_dict['search_fav'] = layout
        for app_item in fav_items:
            groups = app_item.groups
            cmd = app_item.cmd
            desc = app_item.desc
            ver = app_item.ver
            name = app_item.name
            helpdoc = app_item.helpdoc
            contact = app_item.contact
            card = AppCard(name, groups, cmd, True, desc, ver, helpdoc, contact, self, width=self._width)
            card.setIcon(app_item.icon_path)
            card.infoFormChanged.connect(partial(self.on_info_form_changed, 'search_fav'))
            card.favChanged.connect(self.on_fav_changed)
            self._app_card_dict['search_fav'][name] = card
            layout.addWidget(card)
        w1.setLayout(layout)
        fav_area.setWidget(w1)

        apps_area = w.findChild(QScrollArea, 'apps_area')
        self._area_dict.update({'search_apps': apps_area})
        w2 = apps_area.takeWidget()
        if w2 is not None:
            w2.setParent(None)
        w2 = QWidget(w)
        w2.setContentsMargins(0, self._margin, 0, self._margin)
        layout = FlowLayout(spacing=self._spacing)
        self._layout_dict['search_apps'] = layout
        for app_item in other_items:
            groups = app_item.groups
            cmd = app_item.cmd
            desc = app_item.desc
            ver = app_item.ver
            name = app_item.name
            helpdoc = app_item.helpdoc
            contact = app_item.contact
            card = AppCard(name, groups, cmd, False, desc, ver, helpdoc, contact, self, width=self._width)
            card.setIcon(app_item.icon_path)
            card.infoFormChanged.connect(partial(self.on_info_form_changed, 'search_apps'))
            card.favChanged.connect(self.on_fav_changed)
            self._app_card_dict['search_apps'][name] = card
            layout.addWidget(card)
        w2.setLayout(layout)
        apps_area.setWidget(w2)

        #
        w.findChild(QLabel, 'fav_group_lbl').setVisible(not fav_items==[])
        w.findChild(QLabel, 'apps_group_lbl').setVisible(not other_items==[])
        w.findChild(QLabel, 'notfound_lbl').setVisible(other_items==[] and fav_items==[])
        apps_area.setVisible(not other_items==[])
        fav_area.setVisible(not fav_items==[])

    @pyqtSlot(bool)
    def on_enable_search(self, auto_collapse, enabled):
        if not enabled and self.main_tab.currentIndex() == 2:
            # switch back to last page
            if self._nested:
                self.main_tab.setCurrentIndex(1)
                self.apps_tab.setCurrentIndex(self._current_index)
            else:
                self.main_tab.setCurrentIndex(self._current_index)
            # clean search page
            self.main_tab.removeTab(2)

        if auto_collapse:
            # collapse input box
            self.search_lineEdit.setVisible(enabled)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape and self.search_btn.isChecked():
            self.search_btn.setChecked(False)
