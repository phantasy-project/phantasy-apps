# -*- coding: utf-8 -*-#

"""App card widget.
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget

from .ui.ui_app_card import Ui_AppForm


class AppCard(QWidget, Ui_AppForm):

    def __init__(self, name, groups, fav_on=False, parent=None, **kws):
        super(AppCard, self).__init__(parent)

        self.setupUi(self)

        # fix width
        if kws.get('width', None) is not None:
            self.setFixedWidth(kws.get('width'));

        self.setName(name)
        self.setGroups(groups)
        self.setFavorite(fav_on)

        self.setMouseTracking(True)
        for o in (self.fav_btn, self.app_btn, self.info_btn):
            o.setMouseTracking(True)

    def setIcon(self, icon_path):
        self.app_btn.setIcon(QIcon(QPixmap(icon_path)))

    def name(self):
        """str : App name.
        """
        return self._name

    def setName(self, s):
        self._name = s
        self.app_name_lbl.setText(s)

    def groups(self):
        """list : App groups.
        """
        return self._groups

    def setGroups(self, groups):
        self._groups = groups
        self.app_group_lbl.setText(groups[0])

    def favorite(self):
        """bool: Is this app favorited?
        """
        return self._fav_on

    def setFavorite(self, on):
        self._fav_on = on
        self.fav_btn.setChecked(on)

    @pyqtSlot(bool)
    def on_toggle_fav(self, on):
        """Toggle fav on/off.
        """
        print("Fav on/off? ", on)

    @pyqtSlot(bool)
    def on_toggle_info(self, on):
        """Toggle info panel.
        """
        if on:
            self.setStyleSheet("""
            QWidget#AppForm {
                border: 2px solid #04B13B;
            }
            QWidget#AppForm:hover:!pressed {
                border: 2px solid #04B13B;
            }""")
        else:
            self.setStyleSheet("""
            QWidget#AppForm {
                border: 2px solid rgb(200, 200, 200);
            }
            QWidget#AppForm:hover:!pressed {
                border: 2px solid rgb(138, 138, 138);
            }""")

    def mouseMoveEvent(self, evt):
        change_cursor = False
        for o in (self.app_btn, self.fav_btn, self.info_btn):
            if o.rect().contains(o.mapFromGlobal(evt.globalPos())):
                change_cursor = True
        if change_cursor:
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.unsetCursor()

    def paintEvent(self, evt):
        from PyQt5.QtGui import QPainter
        from PyQt5.QtWidgets import QStyleOption, QStyle
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
