# -*- coding: utf-8 -*-

import logging

from PyQt5.QtCore import Qt
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

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        # Prevent the reload menu from opening. It will be useless anyway.
        self.setContextMenuPolicy(Qt.PreventContextMenu)

        #
        self.setPage(LoggingWebPage())

    def wheelEvent(self, event):
        frame = self.page().mainFrame()
        delta = event.angleDelta().y()
        scale = 1 + 0.1 * delta / 240
        frame.setZoomFactor(frame.zoomFactor() * scale)

    def contentsSizeChanged(self, event):
        printlog(event)


