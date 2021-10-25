# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_bpmviz.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(2136, 847)
        MainWindow.setStyleSheet(
            "QTabBar::tab::disabled {width: 0; height: 0; margin: 0; padding: 0; border: none;}"
        )
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowNestedDocks
                                  | QtWidgets.QMainWindow.AllowTabbedDocks
                                  | QtWidgets.QMainWindow.GroupedDragging)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_6.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_6.setSpacing(4)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.widget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab1)
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.mplbase11 = MatplotlibBaseWidget(self.tab1)
        self.mplbase11.setFigureAutoScale(True)
        self.mplbase11.setProperty("figureToolbarToggle", False)
        self.mplbase11.setObjectName("mplbase11")
        self.gridLayout_2.addWidget(self.mplbase11, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab1, "")
        self.tab2 = QtWidgets.QWidget()
        self.tab2.setObjectName("tab2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab2)
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_3.setSpacing(2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.mplbase12 = MatplotlibBaseWidget(self.tab2)
        self.mplbase12.setFigureAutoScale(True)
        self.mplbase12.setProperty("figureToolbarToggle", False)
        self.mplbase12.setObjectName("mplbase12")
        self.gridLayout_3.addWidget(self.mplbase12, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab2, "")
        self.tab3 = QtWidgets.QWidget()
        self.tab3.setObjectName("tab3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab3)
        self.gridLayout_4.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_4.setSpacing(2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.mplbase21 = MatplotlibBaseWidget(self.tab3)
        self.mplbase21.setFigureAutoScale(True)
        self.mplbase21.setProperty("figureToolbarToggle", False)
        self.mplbase21.setObjectName("mplbase21")
        self.gridLayout_4.addWidget(self.mplbase21, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab3, "")
        self.tab4 = QtWidgets.QWidget()
        self.tab4.setObjectName("tab4")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab4)
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_5.setSpacing(2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.mplbase22 = MatplotlibBaseWidget(self.tab4)
        self.mplbase22.setFigureAutoScale(True)
        self.mplbase22.setProperty("figureToolbarToggle", False)
        self.mplbase22.setObjectName("mplbase22")
        self.gridLayout_5.addWidget(self.mplbase22, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab4, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.widget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 2136, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1),
                                  _translate("MainWindow", "Tab1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2),
                                  _translate("MainWindow", "Tab 2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab3),
                                  _translate("MainWindow", "Tab3"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab4),
                                  _translate("MainWindow", "Tab4"))


from mpl4qt.widgets.mplbasewidget import MatplotlibBaseWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
