# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_app.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1316, 873)
        MainWindow.setStyleSheet(
            "QCheckBox::indicator {\n"
            "    width: 16px;\n"
            "    height: 16px;\n"
            "}\n"
            "QCheckBox::indicator::unchecked {\n"
            "    image: url(:/_misc/uncheck-square.png);\n"
            "}\n"
            "QCheckBox::indicator::checked {\n"
            "    image: url(:/_misc/check-square-fill.png);\n"
            "}\n"
            "QAbstractItemView::indicator::unchecked {\n"
            "    image: url(:/_misc/uncheck-square.png);\n"
            "}\n"
            "QAbstractItemView::indicator::checked {\n"
            "    image: url(:/_misc/check-square-fill.png);\n"
            "}\n"
            "\n"
            "/*Splitter*/\n"
            "QSplitter::handle {\n"
            "    height: 6px;\n"
            "    width: 6px;\n"
            "}\n"
            "QSplitter::handle:horizontal {\n"
            "    image: url(:/_misc/separator-v.png);\n"
            "}\n"
            "QSplitter::handle:horizontal:pressed, QSplitter::handle:horizontal:hover {\n"
            "    image: url(:/_misc/separator-v-pressed.png);\n"
            "}\n"
            "QSplitter::handle:vertical {\n"
            "    image: url(:/_misc/separator-h.png);\n"
            "}\n"
            "QSplitter::handle:vertical:pressed, QSplitter::handle:vertical:hover {\n"
            "    image: url(:/_misc/separator-h-pressed.png);\n"
            "}\n"
            "\n"
            "QMainWindow::separator {\n"
            "    width: 6px;\n"
            "    height: 6px;\n"
            "}\n"
            "QMainWindow::separator:horizontal {\n"
            "    image: url(:/_misc/separator-h.png);\n"
            "}\n"
            "QMainWindow::separator:horizontal:hover, QMainWindow::separator:horizontal:pressed {\n"
            "    image: url(:/_misc/separator-h-pressed.png);\n"
            "}\n"
            "QMainWindow::separator:vertical {\n"
            "    image: url(:/_misc/separator-v.png);\n"
            "}\n"
            "QMainWindow::separator:vertical:hover, QMainWindow::separator:vertical:pressed {\n"
            "    image: url(:/_misc/separator-v-pressed.png);\n"
            "}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(4, 10, 4, 4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 4, -1, 4)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.allowed_root_path_lineEdit = QtWidgets.QLineEdit(
            self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.allowed_root_path_lineEdit.sizePolicy().hasHeightForWidth())
        self.allowed_root_path_lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setItalic(True)
        self.allowed_root_path_lineEdit.setFont(font)
        self.allowed_root_path_lineEdit.setReadOnly(True)
        self.allowed_root_path_lineEdit.setObjectName(
            "allowed_root_path_lineEdit")
        self.horizontalLayout_2.addWidget(self.allowed_root_path_lineEdit)
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/_misc/help.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QtCore.QSize(32, 32))
        self.toolButton.setAutoRaise(True)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_2.addWidget(self.toolButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.live_groupBox = QtWidgets.QGroupBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.live_groupBox.sizePolicy().hasHeightForWidth())
        self.live_groupBox.setSizePolicy(sizePolicy)
        self.live_groupBox.setStyleSheet(
            "QLabel {\n"
            "    font-family: monospace;\n"
            "}\n"
            "QScrollArea {\n"
            "    border-top: 0px solid gray;\n"
            "    border-bottom: 5px solid gray;\n"
            "    border-right: 5px solid gray;\n"
            "       border-left: 0px solid gray;\n"
            "}")
        self.live_groupBox.setObjectName("live_groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.live_groupBox)
        self.gridLayout.setContentsMargins(0, 8, 0, 0)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.live_area = QtWidgets.QScrollArea(self.live_groupBox)
        self.live_area.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.live_area.sizePolicy().hasHeightForWidth())
        self.live_area.setSizePolicy(sizePolicy)
        self.live_area.setStyleSheet("")
        self.live_area.setWidgetResizable(True)
        self.live_area.setObjectName("live_area")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(
            0, 0, 1292, 521))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.live_area.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.live_area, 0, 0, 1, 1)
        self.config_groupBox = QtWidgets.QGroupBox(self.splitter)
        self.config_groupBox.setStyleSheet(
            "QLabel {\n"
            "    font-family: monospace;\n"
            "}\n"
            "QScrollArea {\n"
            "    border-top: 0px solid gray;\n"
            "    border-bottom: 5px solid gray;\n"
            "    border-right: 5px solid gray;\n"
            "       border-left: 0px solid gray;\n"
            "}")
        self.config_groupBox.setCheckable(True)
        self.config_groupBox.setChecked(False)
        self.config_groupBox.setObjectName("config_groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.config_groupBox)
        self.gridLayout_2.setContentsMargins(0, 8, 0, 0)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.config_area = QtWidgets.QScrollArea(self.config_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.config_area.sizePolicy().hasHeightForWidth())
        self.config_area.setSizePolicy(sizePolicy)
        self.config_area.setStyleSheet("")
        self.config_area.setWidgetResizable(True)
        self.config_area.setObjectName("config_area")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(
            QtCore.QRect(0, 0, 1292, 89))
        self.scrollAreaWidgetContents_2.setObjectName(
            "scrollAreaWidgetContents_2")
        self.config_area.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout_2.addWidget(self.config_area, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.splitter)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 4, -1, 4)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse
                                           | QtCore.Qt.TextSelectableByMouse)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.dirpath_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.dirpath_lineEdit.sizePolicy().hasHeightForWidth())
        self.dirpath_lineEdit.setSizePolicy(sizePolicy)
        self.dirpath_lineEdit.setReadOnly(False)
        self.dirpath_lineEdit.setObjectName("dirpath_lineEdit")
        self.horizontalLayout.addWidget(self.dirpath_lineEdit)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/_misc/open.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/_misc/add.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushButton.setIcon(icon2)
        self.pushButton.setIconSize(QtCore.QSize(32, 32))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/_misc/remove.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon3)
        self.pushButton_3.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1316, 32))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.action_About = QtWidgets.QAction(MainWindow)
        self.action_About.setObjectName("action_About")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.menu_Help.addAction(self.action_About)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        self.actionAbout_Qt.triggered.connect(
            MainWindow.onAboutQt)  # type: ignore
        self.action_About.triggered.connect(MainWindow.onAbout)  # type: ignore
        self.pushButton_2.clicked.connect(MainWindow.onOpen)  # type: ignore
        self.pushButton.clicked.connect(MainWindow.onAdd)  # type: ignore
        self.pushButton_3.clicked.connect(MainWindow.onRemove)  # type: ignore
        self.toolButton.clicked.connect(MainWindow.onHint)  # type: ignore
        self.config_groupBox.toggled['bool'].connect(
            self.config_area.setEnabled)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(
            _translate("MainWindow", "Autoship the files recursively in"))
        self.allowed_root_path_lineEdit.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Manage the folder permissions under pointed directory.</p></body></html>"
            ))
        self.toolButton.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Click for the help info of this app.</p></body></html>"
            ))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.live_groupBox.setTitle(_translate("MainWindow", "Live"))
        self.config_groupBox.setTitle(_translate("MainWindow", "Config"))
        self.label.setText(_translate("MainWindow", "Select a directory"))
        self.pushButton_2.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Choose a folder to be managed.</p></body></html>"
            ))
        self.pushButton_2.setText(_translate("MainWindow", "Browse"))
        self.pushButton.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Add the selected folder to the list of folders being managed.</p></body></html>"
            ))
        self.pushButton.setText(_translate("MainWindow", "Add"))
        self.pushButton_3.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Remove the folder from the list of folders being managed.</p></body></html>"
            ))
        self.pushButton_3.setText(_translate("MainWindow", "Remove"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.action_About.setText(_translate("MainWindow", "&About"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))


from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())