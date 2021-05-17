#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QDate
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QDialog

from phantasy_apps.settings_manager.ui.ui_date_range import Ui_Dialog


class DateRangeDialog(QDialog, Ui_Dialog):

    dateFromChanged = pyqtSignal(QDate)
    dateToChanged = pyqtSignal(QDate)

    def __init__(self, parent=None):
        super(self.__class__, self).__init__()
        self.parent = parent

        # UI
        self.setupUi(self)
        self.setWindowTitle("Select Date Range")

        #
        self.post_init_ui()

    def post_init_ui(self):
        self.dateTimeRangePicker.dateFromChanged.connect(self.dateFromChanged)
        self.dateTimeRangePicker.dateToChanged.connect(self.dateToChanged)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    w = DateRangeDialog()
    w.show()

    sys.exit(app.exec_())
