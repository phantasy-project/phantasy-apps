# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_app.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/frib_va.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(
            "QGroupBox {\n"
            "    /*background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #E0E0E0, stop: 1 #E0E0E0);\n"
            "   */\n"
            "    border: 2px solid gray;\n"
            "    border-radius: 5px;\n"
            "    margin-top: 1.5ex; /* leave space at the top for the title */\n"
            "    margin-bottom: 0.5ex;\n"
            "}\n"
            "\n"
            "QGroupBox::title {\n"
            "    subcontrol-origin: margin;\n"
            "    subcontrol-position: top center; /* position at the top center */\n"
            "    padding: 0 3px;\n"
            "    /*background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                      stop: 0 #EDECEB, stop: 1 #FFFFFF);\n"
            "    */\n"
            "}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(6, 12, 6, 6)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.va_listWidget = QtWidgets.QListWidget(self.widget)
        self.va_listWidget.setMinimumSize(QtCore.QSize(300, 0))
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.va_listWidget.setFont(font)
        self.va_listWidget.setViewMode(QtWidgets.QListView.ListMode)
        self.va_listWidget.setObjectName("va_listWidget")
        self.verticalLayout.addWidget(self.va_listWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.toolButton = QtWidgets.QToolButton(self.widget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/clear.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.toolButton.setIcon(icon1)
        self.toolButton.setIconSize(QtCore.QSize(24, 24))
        self.toolButton.setAutoRaise(True)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.toolButton)
        self.delete_btn = QtWidgets.QToolButton(self.widget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/delete.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_btn.setIcon(icon2)
        self.delete_btn.setIconSize(QtCore.QSize(24, 24))
        self.delete_btn.setAutoRaise(True)
        self.delete_btn.setObjectName("delete_btn")
        self.horizontalLayout.addWidget(self.delete_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.va_tab = QtWidgets.QTabWidget(self.splitter)
        self.va_tab.setElideMode(QtCore.Qt.ElideNone)
        self.va_tab.setDocumentMode(False)
        self.va_tab.setTabsClosable(False)
        self.va_tab.setMovable(False)
        self.va_tab.setTabBarAutoHide(False)
        self.va_tab.setObjectName("va_tab")
        self.last_page = QtWidgets.QWidget()
        self.last_page.setObjectName("last_page")
        self.va_tab.addTab(self.last_page, "")
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 31))
        self.menubar.setObjectName("menubar")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        MainWindow.setMenuBar(self.menubar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/info.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon3)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/qt.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.actionAbout_Qt.setIcon(icon4)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionContents = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/help.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.actionContents.setIcon(icon5)
        self.actionContents.setObjectName("actionContents")
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/exit.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.actionE_xit.setIcon(icon6)
        self.actionE_xit.setObjectName("actionE_xit")
        self.nb_tool = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/notebook_run.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nb_tool.setIcon(icon7)
        self.nb_tool.setObjectName("nb_tool")
        self.va_info_tool = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/system-task.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.va_info_tool.setIcon(icon8)
        self.va_info_tool.setObjectName("va_info_tool")
        self.va_run_tool = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/start.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.va_run_tool.setIcon(icon9)
        self.va_run_tool.setObjectName("va_run_tool")
        self.va_stop_tool = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/stop.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.va_stop_tool.setIcon(icon10)
        self.va_stop_tool.setObjectName("va_stop_tool")
        self.menu_Help.addAction(self.actionContents)
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menu_File.addAction(self.actionE_xit)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        self.va_tab.setCurrentIndex(0)
        self.actionAbout.triggered.connect(MainWindow.onAbout)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.actionE_xit.triggered.connect(MainWindow.close)
        self.va_tab.tabBarClicked['int'].connect(MainWindow.on_clicked_tabbar)
        self.delete_btn.clicked.connect(MainWindow.on_delete_current_page)
        self.toolButton.clicked.connect(self.va_listWidget.clearSelection)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolButton.setToolTip(_translate("MainWindow",
                                              "Clear selection."))
        self.toolButton.setText(_translate("MainWindow", "Clear Selection"))
        self.delete_btn.setToolTip(
            _translate("MainWindow", "Delete selected VA page."))
        self.delete_btn.setText(_translate("MainWindow", "Delete"))
        self.va_tab.setTabText(self.va_tab.indexOf(self.last_page),
                               _translate("MainWindow", "+"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))
        self.actionContents.setText(_translate("MainWindow", "Contents"))
        self.actionContents.setShortcut(_translate("MainWindow", "F1"))
        self.actionE_xit.setText(_translate("MainWindow", "E&xit"))
        self.actionE_xit.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.nb_tool.setText(_translate("MainWindow", "RUN-NB"))
        self.va_info_tool.setText(_translate("MainWindow", "VA Info"))
        self.va_run_tool.setText(_translate("MainWindow", "RUN VA"))
        self.va_stop_tool.setText(_translate("MainWindow", "STOP VA"))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
