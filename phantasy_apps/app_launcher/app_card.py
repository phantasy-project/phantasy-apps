# -*- coding: utf-8 -*-#

"""App card widget.
"""

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QFile
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QStyleOption
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QWidget

from subprocess import Popen

from .ui.ui_app_card import Ui_AppForm
from .ui.ui_app_info import Ui_InfoForm


class AppCard(QWidget, Ui_AppForm):

    favChanged = pyqtSignal(bool)
    infoFormChanged = pyqtSignal(dict, bool)

    def __init__(self, name, groups, cmd=None, fav_on=False, desc=None,
                 version=None, helpdoc=None, contact=None, parent=None, **kws):
        super(AppCard, self).__init__(parent)

        #
        self.setupUi(self)

        # fix width
        if kws.get('width', None) is not None:
            self.setFixedWidth(kws.get('width'))

        self.setName(name)
        self.setGroups(groups)
        self.setFavorite(fav_on)
        self.setCommand(cmd)
        self.setDescription(desc)
        self.setVersion(version)
        self.setHelpdoc(helpdoc)
        self.setContact(contact)

        self.setMouseTracking(True)
        for o in (self.fav_btn, self.app_btn, self.info_btn):
            o.setMouseTracking(True)

        self.setToolTip(f"Click to run {name}")

    def get_meta_info(self):
        return {'name': self.name(), 'groups': self.groups(),
                'fav': self.favorite(), 'desc': self.description(),
                'helpdoc': self.helpdoc(), 'contact': self.contact(),
                'ver': self.version(),}

    @pyqtSlot()
    def on_close_info(self):
        self.info_btn.toggled.disconnect()
        self.info_btn.setChecked(False)
        self.setStyleSheet("""
        QWidget#AppForm {
            border: 2px solid rgb(200, 200, 200);
        }
        QWidget#AppForm:hover:!pressed {
            border: 2px solid rgb(138, 138, 138);
        }""")
        self.info_btn.toggled.connect(self.on_toggle_info)

    @pyqtSlot(bool)
    def on_fav_changed(self, on):
        self.fav_btn.setChecked(on)

    def setIcon(self, icon_path):
        self.app_btn.setIcon(QIcon(QPixmap(icon_path)))

    def setToolTip(self, s):
        self.app_btn.setToolTip(s)

    def description(self):
        """str : Description.
        """
        return self._desc

    def setDescription(self, s):
        self._desc = s

    def version(self):
        """str : App version.
        """
        return self._version

    def setVersion(self, s):
        self._version = s
        self.app_ver_lbl.setText(s)

    def helpdoc(self):
        """str : Url/path for help doc.
        """
        return self._helpdoc

    def setHelpdoc(self, s):
        self._helpdoc = s

    def contact(self):
        """People : People to contact.
        """
        return self._contact

    def setContact(self, o):
        self._contact = o

    def command(self):
        """str : Callback command.
        """
        return self._cmd

    def setCommand(self, cmd):
        self._cmd = cmd
        self.app_btn.clicked.connect(lambda:self.on_launch_app(False))

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
        self.favChanged.emit(on)

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
            self.infoFormChanged.emit(self.get_meta_info(), True)
        else:
            self.setStyleSheet("""
            QWidget#AppForm {
                border: 2px solid rgb(200, 200, 200);
            }
            QWidget#AppForm:hover:!pressed {
                border: 2px solid rgb(138, 138, 138);
            }""")
            self.infoFormChanged.emit(self.get_meta_info(), False)

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
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

    @pyqtSlot(bool)
    def on_launch_app(self, console):
        if not console:
            cmdline = self._cmd
        else:
            cmdline = "x-terminal-emulator -e " + self._cmd
        Popen(cmdline, shell=True)


class AppCardInfoForm(QWidget, Ui_InfoForm):

    favChanged = pyqtSignal(bool)
    runAppInTerminal = pyqtSignal(bool)
    sig_close = pyqtSignal()

    def __init__(self, name, group, fav_on=False, desc=None, ver=None, helpdoc=None, contact=None,
                 parent=None, **kws):
        super(AppCardInfoForm, self).__init__(parent)

        self.setupUi(self)
        self.desc_plainTextEdit.setStyleSheet("""
            QPlainTextEdit {
                font-size: 16pt;
                font-family: monospace;}""")
        self.app_name.setText(name)
        self.app_main_group.setText(group)
        self.app_version = ver
        self.desc_plainTextEdit.setPlainText(desc)
        self.on_fav_changed(fav_on)
        self.config_helpdoc(helpdoc)
        self.config_contact(contact)

    @pyqtSlot(bool)
    def on_fav_changed(self, on):
        self.fav_btn.setChecked(on)

    @pyqtSlot()
    def on_run_app(self):
        self.runAppInTerminal.emit(False)

    @pyqtSlot()
    def on_run_app_in_terminal(self):
        self.runAppInTerminal.emit(True)

    @pyqtSlot(bool)
    def on_toggle_fav(self, on):
        self.favChanged.emit(on)
        if on:
            self.fav_on_lbl.setText("Remove from Favorites")
        else:
            self.fav_on_lbl.setText("Add to Favorites")

    @pyqtSlot()
    def on_close(self):
        self.sig_close.emit()
        self.close()

    def closeEvent(self, evt):
        self.sig_close.emit()
        QWidget.closeEvent(self, evt)

    def paintEvent(self, evt):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

    def config_helpdoc(self, doc):
        url = QUrl.fromUserInput(doc)
        if url.isLocalFile():
            if QFile(url.path()).exists():
                self.helpdoc_btn.setVisible(True)
                self.helpdoc_btn.clicked.connect(lambda:QDesktopServices.openUrl(url))
            else:
                self.helpdoc_btn.setVisible(False)
        else: # url?
            self.helpdoc_btn.setVisible(False)

    def config_contact(self, contact):
        if contact.name == '':
            [o.setVisible(False) for o in (self.contact_lbl, self.contact_name_lbl,
                                           self.contact_phone_lbl, self.contact_email_lbl)]
        else:
            self.contact_name_lbl.setText(contact.name)
            self.contact_phone_lbl.setText(contact.phone)
            s = f'<a href="mailto:{contact.email}?subject=Questions about {self.app_name.text()} v{self.app_version}">{contact.email}</a>'
            self.contact_email_lbl.setOpenExternalLinks(True)
            self.contact_email_lbl.setText(s)
