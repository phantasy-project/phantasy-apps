# -*- coding: utf-8 -*-#

"""App card widget.
"""

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QEvent
from PyQt5.QtCore import QFile
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QStyleOption
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

from subprocess import Popen
import shutil

from .utils import _new_dir

from .ui.ui_app_card import Ui_AppForm
from .ui.ui_app_info import Ui_InfoForm

DEFAULT_LOG_ROOTDIR = "/tmp/app-launcher"

class AppCard(QWidget, Ui_AppForm):

    favChanged = pyqtSignal(bool)
    infoFormChanged = pyqtSignal(dict, bool)

    def __init__(self, name, groups, cmd=None, fav_on=False, desc=None,
                 version=None, helpdoc=None, contact=None, changelog=None,
                 parent=None, **kws):
        super(AppCard, self).__init__(parent)

        #
        self.setupUi(self)

        # fixed width
        if kws.get('width', None) is not None:
            self.setFixedWidth(kws.get('width'))

        # root dir for app logs
        self._log_rootdir = kws.get('log_rootdir', DEFAULT_LOG_ROOTDIR)

        self.app_btn_widget.installEventFilter(self)
        self.app_btn_widget.setToolTip(f"Click to run {name}")

        self.setName(name)
        self.setGroups(groups)
        self.setFavorite(fav_on)
        self.setCommand(cmd)
        self.setDescription(desc)
        self.setVersion(version)
        self.setHelpdoc(helpdoc)
        self.setContact(contact)
        self.setChangelog(changelog)

    def get_meta_info(self):
        return {'name': self.name(), 'groups': self.groups(),
                'fav': self.favorite(), 'desc': self.description(),
                'helpdoc': self.helpdoc(), 'contact': self.contact(),
                'changelog': self.changelog(),
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
    def on_fav_changed(self, on: bool):
        self.fav_btn.setChecked(on)

    def setIcon(self, icon_path):
        self.app_btn.setIcon(QIcon(QPixmap(icon_path)))

    def setToolTip(self, s):
        self.app_btn.setToolTip(s)

    def description(self):
        """str : Description.
        """
        return self._desc

    def setDescription(self, s: str):
        self._desc = s

    def version(self):
        """str : App version.
        """
        return self._version

    def setVersion(self, s: str):
        self._version = s
        self.app_ver_lbl.setText(s)

    def helpdoc(self):
        """str : Url/path for help doc.
        """
        return self._helpdoc

    def setHelpdoc(self, s: str):
        self._helpdoc = s

    def changelog(self):
        """str : Url/path for changelog.
        """
        return self._changelog

    def setChangelog(self, s: str):
        self._changelog = s

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

    def setCommand(self, cmd: str):
        self._cmd = cmd
        self.app_btn.clicked.connect(lambda:self.on_launch_app(False))
        # if cmd is a single word, try to get the full path
        if len(cmd.split()) == 1:
            self._cmd = shutil.which(cmd)

    def name(self):
        """str : App name.
        """
        return self._name

    def setName(self, s: str):
        self._name = s
        self.app_name_lbl.setText(s)
        # initialize the filename for log messages
        self._log_app_dirpath = os.path.join(self._log_rootdir, s.lower().replace(" ", "_"))
        if not os.path.exists(self._log_app_dirpath):
            _new_dir(self._log_app_dirpath)
        self._log_filename = s.lower().replace(" ", "_") + ".log"
        self._log_filepath = os.path.join(self._log_app_dirpath, self._log_filename)

    def groups(self):
        """list : App groups.
        """
        return self._groups

    def setGroups(self, groups: list):
        self._groups = groups
        self.app_group_lbl.setText(groups[0])

    def favorite(self):
        """bool: Is this app favorited?
        """
        return self._fav_on

    def setFavorite(self, on: bool):
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
        for o in (self.fav_btn, self.info_btn, self.app_btn_widget):
            if o.rect().contains(o.mapFromGlobal(evt.globalPos())):
                change_cursor = True
        if change_cursor:
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.unsetCursor()

    def eventFilter(self, obj, evt):
        if evt.type() == QEvent.MouseButtonPress:
            self.app_btn.clicked.emit()
            return True
        else:
            return False

    def paintEvent(self, evt):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

    @pyqtSlot(bool)
    def on_launch_app(self, console: bool):
        if not console:
            cmdline = self._cmd
        else:
            # cmdline = "gnome-terminal -- " + self._cmd
            cmdline = "gnome-terminal -- " + "bash -c " + '"' \
                    + self._cmd + " 2>&1 | tee -a " + f"{self._log_filepath}" + '"'
        Popen(cmdline, shell=True)


class AppCardInfoForm(QWidget, Ui_InfoForm):

    favChanged = pyqtSignal(bool)
    runAppInTerminal = pyqtSignal(bool)
    sig_close = pyqtSignal()

    def __init__(self, name, group, fav_on=False, desc=None, ver=None,
                 helpdoc=None, contact=None, changelog=None,
                 parent=None, **kws):
        super(AppCardInfoForm, self).__init__(parent)

        self.setupUi(self)
        self.app_name.setText(name)
        self.app_main_group.setText(group)
        self.app_version = ver
        self.desc_plainTextEdit.setPlainText(desc)
        self.on_fav_changed(fav_on)
        self.config_helpdoc(helpdoc)
        self.config_contact(contact)
        self.config_changelog(changelog)

        #
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5)
        shadow.setOffset(2)
        self.desc_plainTextEdit.setGraphicsEffect(shadow)

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
            self.fav_btn.setText("Remove from Favorites")
        else:
            self.fav_btn.setText("Add to Favorites")

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

    def config_changelog(self, doc):
        url = QUrl.fromUserInput(doc)
        if url.isLocalFile():
            if QFile(url.path()).exists():
                self.changelog_btn.setVisible(True)
                self.changelog_btn.clicked.connect(lambda:QDesktopServices.openUrl(url))
            else:
                self.changelog_btn.setVisible(False)
        else: # url?
            self.changelog_btn.setVisible(False)

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
