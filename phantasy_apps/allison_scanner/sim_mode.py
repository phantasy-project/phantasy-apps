# -*- coding: utf-8 -*-

from subprocess import Popen
from PyQt5.QtWidgets import QWidget

from .ui.ui_sim_mode import Ui_Form


class SimModeWidget(QWidget, Ui_Form):

    def __init__(self, parent):
        super(SimModeWidget, self).__init__()
        self.parent = parent

        # UI
        self.setupUi(self)
        self.setWindowTitle("Simulation Mode")

        #
        self._post_init()

    def _post_init(self):
        pass

    def on_start(self):
        cmd = "docker run --rm -it --name myIOCAppAS tonyzhang/ioc-app-for-allison:dev"
        Popen(cmd.split())

    def on_stop(self):
        cmd = "docker container stop myIOCAppAS"
        Popen(cmd.split())

    def on_refresh(self):
        self.parent._post_init()
