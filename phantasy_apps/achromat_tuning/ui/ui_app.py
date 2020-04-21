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
        MainWindow.resize(1300, 975)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(6, 12, 6, 6)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.bend_tune_tab = QtWidgets.QWidget()
        self.bend_tune_tab.setObjectName("bend_tune_tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.bend_tune_tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.bend_tuning_plot = MatplotlibErrorbarWidget(self.bend_tune_tab)
        font = QtGui.QFont()
        font.setFamily("sans-serif")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.bend_tuning_plot.setFigureXYlabelFont(font)
        font = QtGui.QFont()
        font.setFamily("sans-serif")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.bend_tuning_plot.setFigureTitleFont(font)
        font = QtGui.QFont()
        font.setFamily("sans-serif")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.bend_tuning_plot.setFigureXYticksFont(font)
        self.bend_tuning_plot.setFigureAutoScale(False)
        self.bend_tuning_plot.setObjectName("bend_tuning_plot")
        self.gridLayout_2.addWidget(self.bend_tuning_plot, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.open_in_cv_btn = QtWidgets.QPushButton(self.bend_tune_tab)
        self.open_in_cv_btn.setObjectName("open_in_cv_btn")
        self.horizontalLayout.addWidget(self.open_in_cv_btn)
        self.label = QtWidgets.QLabel(self.bend_tune_tab)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.bpm_goal_lineEdit = QtWidgets.QLineEdit(self.bend_tune_tab)
        self.bpm_goal_lineEdit.setObjectName("bpm_goal_lineEdit")
        self.horizontalLayout.addWidget(self.bpm_goal_lineEdit)
        self.label_3 = QtWidgets.QLabel(self.bend_tune_tab)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.bend_goal_lineEdit = QtWidgets.QLineEdit(self.bend_tune_tab)
        self.bend_goal_lineEdit.setObjectName("bend_goal_lineEdit")
        self.horizontalLayout.addWidget(self.bend_goal_lineEdit)
        self.set_bend_goal_btn = QtWidgets.QPushButton(self.bend_tune_tab)
        self.set_bend_goal_btn.setObjectName("set_bend_goal_btn")
        self.horizontalLayout.addWidget(self.set_bend_goal_btn)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.tabWidget.addTab(self.bend_tune_tab, "")
        self.quad_tune_tab = QtWidgets.QWidget()
        self.quad_tune_tab.setObjectName("quad_tune_tab")
        self.tabWidget.addTab(self.quad_tune_tab, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1300, 22))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menumenu = QtWidgets.QMenu(self.menubar)
        self.menumenu.setObjectName("menumenu")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_About = QtWidgets.QAction(MainWindow)
        self.action_About.setObjectName("action_About")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        self.actionE_xit.setObjectName("actionE_xit")
        self.actionContents = QtWidgets.QAction(MainWindow)
        self.actionContents.setObjectName("actionContents")
        self.actionload_data = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/at-icons/load_data.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionload_data.setIcon(icon)
        self.actionload_data.setObjectName("actionload_data")
        self.menu_Help.addAction(self.actionContents)
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.action_About)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.menubar.addAction(self.menumenu.menuAction())
        self.toolBar.addAction(self.actionload_data)
        self.toolBar.addAction(self.actionE_xit)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt)
        self.actionE_xit.triggered.connect(MainWindow.close)
        self.action_About.triggered.connect(MainWindow.onAbout)
        self.actionload_data.triggered.connect(MainWindow.on_load_data)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.open_in_cv_btn.setText(
            _translate("MainWindow", "Open in Correlation Visualizer"))
        self.label.setText(
            _translate("MainWindow",
                       "Evaluate bend strength at BPM readings of"))
        self.bpm_goal_lineEdit.setText(_translate("MainWindow", "0.0"))
        self.label_3.setText(
            _translate("MainWindow",
                       "<html><head/><body><p>&rarr;</p></body></html>"))
        self.set_bend_goal_btn.setToolTip(
            _translate("MainWindow",
                       "Set the bend with the left textbox value."))
        self.set_bend_goal_btn.setText(_translate("MainWindow", "Set"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.bend_tune_tab),
                                  _translate("MainWindow", "Bend Tuning"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.quad_tune_tab),
                                  _translate("MainWindow", "Quad Tuning"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.menumenu.setTitle(_translate("MainWindow", "menu"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action_About.setText(_translate("MainWindow", "&About"))
        self.action_About.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))
        self.actionE_xit.setText(_translate("MainWindow", "E&xit"))
        self.actionE_xit.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionContents.setText(_translate("MainWindow", "Contents"))
        self.actionContents.setShortcut(_translate("MainWindow", "F1"))
        self.actionload_data.setText(_translate("MainWindow", "Load Data"))
        self.actionload_data.setToolTip(
            _translate("MainWindow", "Load data from file."))


from mpl4qt.widgets.mplerrorbarwidget import MatplotlibErrorbarWidget
from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
