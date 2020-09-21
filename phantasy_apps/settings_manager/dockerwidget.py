from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtCore import pyqtSignal

class DockWidget(QDockWidget):
    closed = pyqtSignal()
    def __init__(self, parent):
        QDockWidget.__init__(self, parent)

    def closeEvent(self, e):
        self.closed.emit()
