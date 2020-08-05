# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_app_cardview.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 1080)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/app.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.tabWidget.setFont(font)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet(
            "QTabWidget::pane { \n"
            "    border-top: 1px solid #C2C7CB;\n"
            "}\n"
            "\n"
            "QTabWidget::tab-bar {\n"
            "    left: 0px;\n"
            "}\n"
            "\n"
            "/* Style the tab using the tab sub-control. Note that\n"
            "    it reads QTabBar _not_ QTabWidget */\n"
            "QTabBar::tab {\n"
            "    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
            "                                stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
            "    border: 1px solid #C4C4C3;\n"
            "    border-bottom-color: #C2C7CB; /* same as the pane color */\n"
            "    border-top-left-radius: 2px;\n"
            "    border-top-right-radius: 2px;\n"
            "    min-width: 8ex;\n"
            "    padding: 4px;\n"
            "}\n"
            "\n"
            "QTabBar::tab:selected, QTabBar::tab:hover {\n"
            "    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                stop: 0 #fafafa, stop: 0.4 #f4f4f4,\n"
            "                                stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);\n"
            "}\n"
            "\n"
            "QTabBar::tab:selected {\n"
            "    border-color: #9B9B9B;\n"
            "    border-bottom-color: #C2C7CB;\n"
            "}\n"
            "\n"
            "QTabBar::tab:!selected {\n"
            "    margin-top: 4px;\n"
            "}\n"
            "\n"
            "QScrollArea {\n"
            "    border: none;\n"
            "}")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(64, 64))
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setObjectName("tabWidget")
        self.home_page = QtWidgets.QWidget()
        self.home_page.setObjectName("home_page")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.home_page)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(self.home_page)
        self.label_3.setStyleSheet("QLabel {\n"
                                   "    padding: 10px 10px 10px 0px;\n"
                                   "    color: darkgreen;\n"
                                   "}")
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.greetings_lbl = QtWidgets.QLabel(self.home_page)
        self.greetings_lbl.setStyleSheet("QLabel {\n"
                                         "    padding: 10px 10px 10px 0px;\n"
                                         "    border-bottom: 1px solid gray;\n"
                                         "    border-radius: 2px;\n"
                                         "    font-size: 22pt;\n"
                                         "    font-weight: bold;\n"
                                         "}")
        self.greetings_lbl.setObjectName("greetings_lbl")
        self.gridLayout_2.addWidget(self.greetings_lbl, 0, 0, 1, 1)
        self.fav_scrollArea = QtWidgets.QScrollArea(self.home_page)
        self.fav_scrollArea.setWidgetResizable(True)
        self.fav_scrollArea.setObjectName("fav_scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(
            0, 0, 1406, 722))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.fav_scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.fav_scrollArea, 2, 0, 1, 1)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/home.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.tabWidget.addTab(self.home_page, icon1, "")
        self.apps_page = QtWidgets.QWidget()
        self.apps_page.setObjectName("apps_page")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.apps_page)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_4 = QtWidgets.QLabel(self.apps_page)
        self.label_4.setStyleSheet("QLabel {\n"
                                   "    padding: 10px 10px 10px 0px;\n"
                                   "    border-bottom: 1px solid gray;\n"
                                   "    border-radius: 2px;\n"
                                   "}")
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)
        self.tabWidget_2 = QtWidgets.QTabWidget(self.apps_page)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.tabWidget_2.setFont(font)
        self.tabWidget_2.setStyleSheet(
            "QTabWidget::tab-bar {\n"
            "   border: 1px solid gray;\n"
            "}\n"
            "\n"
            "QTabBar::tab {\n"
            "  background: #EFEFEF;\n"
            "  color: green;\n"
            "  padding: 16px;\n"
            " }\n"
            "\n"
            " QTabBar::tab:selected, QTabBar::tab::hover {\n"
            "    background: #EFEFEF;\n"
            "    color: darkgreen;\n"
            "    font-weight: bold;\n"
            "    /*border-bottom-color: #C2C7CB;*/\n"
            " }\n"
            "\n"
            "QTabWidget::pane { \n"
            "    border-top: 1px solid #C2C7CB;\n"
            "}")
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.all_apps_page = QtWidgets.QWidget()
        self.all_apps_page.setObjectName("all_apps_page")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.all_apps_page)
        self.gridLayout_4.setContentsMargins(0, 10, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.all_apps_scrollArea = QtWidgets.QScrollArea(self.all_apps_page)
        self.all_apps_scrollArea.setWidgetResizable(True)
        self.all_apps_scrollArea.setObjectName("all_apps_scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(
            QtCore.QRect(0, 0, 1406, 713))
        self.scrollAreaWidgetContents_2.setObjectName(
            "scrollAreaWidgetContents_2")
        self.all_apps_scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout_4.addWidget(self.all_apps_scrollArea, 0, 0, 1, 1)
        self.tabWidget_2.addTab(self.all_apps_page, "")
        self.fav_apps_page = QtWidgets.QWidget()
        self.fav_apps_page.setObjectName("fav_apps_page")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.fav_apps_page)
        self.gridLayout_5.setContentsMargins(0, 10, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.fav_scrollArea_alias = QtWidgets.QScrollArea(self.fav_apps_page)
        self.fav_scrollArea_alias.setWidgetResizable(True)
        self.fav_scrollArea_alias.setObjectName("fav_scrollArea_alias")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(
            QtCore.QRect(0, 0, 1406, 713))
        self.scrollAreaWidgetContents_3.setObjectName(
            "scrollAreaWidgetContents_3")
        self.fav_scrollArea_alias.setWidget(self.scrollAreaWidgetContents_3)
        self.gridLayout_5.addWidget(self.fav_scrollArea_alias, 0, 0, 1, 1)
        self.tabWidget_2.addTab(self.fav_apps_page, "")
        self.groups_apps_page = QtWidgets.QWidget()
        self.groups_apps_page.setObjectName("groups_apps_page")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groups_apps_page)
        self.gridLayout_6.setContentsMargins(0, 10, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.grps_scrollArea = QtWidgets.QScrollArea(self.groups_apps_page)
        self.grps_scrollArea.setWidgetResizable(True)
        self.grps_scrollArea.setObjectName("grps_scrollArea")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(
            QtCore.QRect(0, 0, 1406, 713))
        self.scrollAreaWidgetContents_4.setObjectName(
            "scrollAreaWidgetContents_4")
        self.grps_scrollArea.setWidget(self.scrollAreaWidgetContents_4)
        self.gridLayout_6.addWidget(self.grps_scrollArea, 0, 0, 1, 1)
        self.tabWidget_2.addTab(self.groups_apps_page, "")
        self.gridLayout_3.addWidget(self.tabWidget_2, 1, 0, 1, 1)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/apps.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.tabWidget.addTab(self.apps_page, icon2, "")
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)
        self.bottombar = QtWidgets.QWidget(self.centralwidget)
        self.bottombar.setStyleSheet("QWidget#bottombar {\n"
                                     "    border-top: 1px solid gray;\n"
                                     "    border-radius: 2px;\n"
                                     "}")
        self.bottombar.setObjectName("bottombar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.bottombar)
        self.horizontalLayout.setContentsMargins(-1, 1, -1, -1)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.about_btn = QtWidgets.QToolButton(self.bottombar)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/frib.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.about_btn.setIcon(icon3)
        self.about_btn.setIconSize(QtCore.QSize(64, 64))
        self.about_btn.setAutoRaise(True)
        self.about_btn.setObjectName("about_btn")
        self.horizontalLayout.addWidget(self.about_btn)
        self.label = QtWidgets.QLabel(self.bottombar)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.title_lbl = QtWidgets.QLabel(self.bottombar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.title_lbl.sizePolicy().hasHeightForWidth())
        self.title_lbl.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.title_lbl.setFont(font)
        self.title_lbl.setStyleSheet("QLabel {\n"
                                     "    font-weight: bold;\n"
                                     "    font-size: 20pt;\n"
                                     "    /*border: 0.5px solid gray;\n"
                                     "    border-radius: 3px;\n"
                                     "    padding: 5px 10px 5px 10px;\n"
                                     "    background-color: white;\n"
                                     "    color: blue;\n"
                                     "    */\n"
                                     "}")
        self.title_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.title_lbl.setObjectName("title_lbl")
        self.horizontalLayout.addWidget(self.title_lbl)
        self.toolButton = QtWidgets.QToolButton(self.bottombar)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/search.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton.setIcon(icon4)
        self.toolButton.setIconSize(QtCore.QSize(48, 48))
        self.toolButton.setAutoRaise(True)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.toolButton)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.show_log_btn = QtWidgets.QToolButton(self.bottombar)
        self.show_log_btn.setEnabled(False)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/show.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.show_log_btn.setIcon(icon5)
        self.show_log_btn.setIconSize(QtCore.QSize(20, 20))
        self.show_log_btn.setAutoRaise(True)
        self.show_log_btn.setObjectName("show_log_btn")
        self.verticalLayout.addWidget(self.show_log_btn)
        self.enable_debug_btn = QtWidgets.QToolButton(self.bottombar)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/log.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.enable_debug_btn.setIcon(icon6)
        self.enable_debug_btn.setIconSize(QtCore.QSize(20, 20))
        self.enable_debug_btn.setCheckable(True)
        self.enable_debug_btn.setAutoRaise(True)
        self.enable_debug_btn.setObjectName("enable_debug_btn")
        self.verticalLayout.addWidget(self.enable_debug_btn)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout.addWidget(self.bottombar, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        self.about_btn.clicked.connect(MainWindow.onAbout)
        self.enable_debug_btn.toggled['bool'].connect(
            MainWindow.on_enable_debug)
        self.show_log_btn.clicked.connect(MainWindow.on_show_log)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-size:20pt;\">Favorites</span></p></body></html>"
            ))
        self.greetings_lbl.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-size:22pt; font-weight:600;\">Welcome!</span></p></body></html>"
            ))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.home_page),
                                  _translate("MainWindow", "Home"))
        self.label_4.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-size:22pt; font-weight:600;\">Apps</span></p></body></html>"
            ))
        self.tabWidget_2.setTabText(
            self.tabWidget_2.indexOf(self.all_apps_page),
            _translate("MainWindow", "All"))
        self.tabWidget_2.setTabText(
            self.tabWidget_2.indexOf(self.fav_apps_page),
            _translate("MainWindow", "Favorites"))
        self.tabWidget_2.setTabText(
            self.tabWidget_2.indexOf(self.groups_apps_page),
            _translate("MainWindow", "Groups"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.apps_page),
                                  _translate("MainWindow", "Apps"))
        self.about_btn.setText(_translate("MainWindow", "..."))
        self.label.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" font-size:10pt;\">Facility for Rare Isotope Beams</span></p><p><span style=\" font-size:8pt;\">Michigan State University</span></p></body></html>"
            ))
        self.title_lbl.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt;\">High-level Physics Applications</span></p></body></html>"
            ))
        self.toolButton.setText(_translate("MainWindow", "Search"))
        self.show_log_btn.setToolTip(
            _translate("MainWindow", "Show log messages"))
        self.show_log_btn.setText(_translate("MainWindow", "Show Log"))
        self.enable_debug_btn.setToolTip(
            _translate("MainWindow", "Enable log messages capture"))
        self.enable_debug_btn.setText(_translate("MainWindow", "Debug"))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
