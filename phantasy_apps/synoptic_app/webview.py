# -*- coding: utf-8 -*-

import logging

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtWebKitWidgets import QWebPage

from phantasy_ui import printlog


class LoggingWebPage(QWebPage):
    """Makes it possible to use a Python logger to print javascript console
    messages.
    """
    def __init__(self, logger=None, parent=None):
        super(self.__class__, self).__init__(parent)
        self.logger = logging if logger is None else logger

    def javaScriptConsoleMessage(self, msg, lineNumber, sourceID):
        self.logger.warn(
            "JsConsole(%s:%d):\n\t%s" % (sourceID, lineNumber, msg))
        printlog(
            "JsConsole(%s:%d):\n\t%s" % (sourceID, lineNumber, msg))


class MyWebView(QWebView):

    # zoom
    zooming_view = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        # Prevent the reload menu from opening. It will be useless anyway.
        self.setContextMenuPolicy(Qt.PreventContextMenu)

        #
        self.setPage(LoggingWebPage())

        #
        self.zoom_factor = self.zoomFactor() * 100
        self.zooming_view.connect(self.on_zooming_view)

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self.zoom_factor = self.zoom_factor * (1 + 0.05 * delta / 120)
        self.zooming_view.emit()

    @pyqtSlot()
    def on_zooming_view(self):
        self.setZoomFactor(self.zoom_factor / 100.0)

    def change_zoom_factor(self, x):
        self.zoom_factor += x
        self.zooming_view.emit()

    def contentsSizeChanged(self, event):
        printlog(event)
