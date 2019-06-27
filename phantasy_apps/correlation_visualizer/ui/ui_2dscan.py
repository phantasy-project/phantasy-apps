# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_2dscan.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1440)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 0, 0, 1, 1)
        self.lower_limit_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lower_limit_lineEdit.setObjectName("lower_limit_lineEdit")
        self.gridLayout.addWidget(self.lower_limit_lineEdit, 1, 1, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setObjectName("label_17")
        self.gridLayout.addWidget(self.label_17, 1, 2, 1, 1)
        self.select_alter_elem_btn = QtWidgets.QPushButton(self.centralwidget)
        self.select_alter_elem_btn.setObjectName("select_alter_elem_btn")
        self.gridLayout.addWidget(self.select_alter_elem_btn, 0, 4, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 1, 0, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.enable_arbitary_array_chkbox = QtWidgets.QCheckBox(
            self.centralwidget)
        self.enable_arbitary_array_chkbox.setText("")
        self.enable_arbitary_array_chkbox.setObjectName(
            "enable_arbitary_array_chkbox")
        self.horizontalLayout_7.addWidget(self.enable_arbitary_array_chkbox)
        self.alter_array_btn = QtWidgets.QPushButton(self.centralwidget)
        self.alter_array_btn.setObjectName("alter_array_btn")
        self.horizontalLayout_7.addWidget(self.alter_array_btn)
        self.gridLayout.addLayout(self.horizontalLayout_7, 1, 4, 1, 1)
        self.upper_limit_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.upper_limit_lineEdit.setObjectName("upper_limit_lineEdit")
        self.gridLayout.addWidget(self.upper_limit_lineEdit, 1, 3, 1, 1)
        self.niter_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.niter_label.sizePolicy().hasHeightForWidth())
        self.niter_label.setSizePolicy(sizePolicy)
        self.niter_label.setObjectName("niter_label")
        self.gridLayout.addWidget(self.niter_label, 2, 0, 1, 1)
        self.alter_elem_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.alter_elem_lineEdit.setText("")
        self.alter_elem_lineEdit.setObjectName("alter_elem_lineEdit")
        self.gridLayout.addWidget(self.alter_elem_lineEdit, 0, 1, 1, 3)
        self.niter_spinBox = QtWidgets.QSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.niter_spinBox.sizePolicy().hasHeightForWidth())
        self.niter_spinBox.setSizePolicy(sizePolicy)
        self.niter_spinBox.setMinimum(1)
        self.niter_spinBox.setMaximum(9999)
        self.niter_spinBox.setProperty("value", 10)
        self.niter_spinBox.setObjectName("niter_spinBox")
        self.gridLayout.addWidget(self.niter_spinBox, 2, 1, 1, 3)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 4, 1, 1)
        self.waitsec_dSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.waitsec_dSpinBox.sizePolicy().hasHeightForWidth())
        self.waitsec_dSpinBox.setSizePolicy(sizePolicy)
        self.waitsec_dSpinBox.setSingleStep(0.5)
        self.waitsec_dSpinBox.setProperty("value", 2.0)
        self.waitsec_dSpinBox.setObjectName("waitsec_dSpinBox")
        self.gridLayout.addWidget(self.waitsec_dSpinBox, 3, 1, 1, 3)
        self.verticalLayout.addLayout(self.gridLayout)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.splitter = QtWidgets.QSplitter(self.groupBox)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.tabWidget_3 = QtWidgets.QTabWidget(self.splitter)
        self.tabWidget_3.setObjectName("tabWidget_3")
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tab1)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.avg_mplimagewidget = MatplotlibImageWidget(self.tab1)
        self.avg_mplimagewidget.setProperty("figureToolbarToggle", False)
        self.avg_mplimagewidget.setAutoColorLimit(True)
        self.avg_mplimagewidget.setObjectName("avg_mplimagewidget")
        self.horizontalLayout_4.addWidget(self.avg_mplimagewidget)
        self.tabWidget_3.addTab(self.tab1, "")
        self.tab2 = QtWidgets.QWidget()
        self.tab2.setObjectName("tab2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.std_mplimagewidget = MatplotlibImageWidget(self.tab2)
        self.std_mplimagewidget.setProperty("figureToolbarToggle", False)
        self.std_mplimagewidget.setAutoColorLimit(True)
        self.std_mplimagewidget.setObjectName("std_mplimagewidget")
        self.horizontalLayout_3.addWidget(self.std_mplimagewidget)
        self.tabWidget_3.addTab(self.tab2, "")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.splitter)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.curve_mplebwidget = MatplotlibErrorbarWidget(self.tab)
        self.curve_mplebwidget.setProperty("figureLegendToggle", True)
        self.curve_mplebwidget.setFigureAutoScale(True)
        self.curve_mplebwidget.setProperty("figureToolbarToggle", False)
        self.curve_mplebwidget.setObjectName("curve_mplebwidget")
        self.horizontalLayout_6.addWidget(self.curve_mplebwidget)
        self.tabWidget_2.addTab(self.tab, "")
        self.horizontalLayout_5.addWidget(self.splitter)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.alter_elem_val_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.alter_elem_val_lineEdit.setObjectName("alter_elem_val_lineEdit")
        self.horizontalLayout.addWidget(self.alter_elem_val_lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.moi_cbb = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.moi_cbb.sizePolicy().hasHeightForWidth())
        self.moi_cbb.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.moi_cbb.setFont(font)
        self.moi_cbb.setObjectName("moi_cbb")
        self.horizontalLayout_2.addWidget(self.moi_cbb)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/start.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.start_btn.setIcon(icon)
        self.start_btn.setIconSize(QtCore.QSize(32, 32))
        self.start_btn.setObjectName("start_btn")
        self.horizontalLayout_2.addWidget(self.start_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 32))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.tabWidget_3.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_15.setText(_translate("MainWindow", "Alter Element"))
        self.label_17.setText(_translate("MainWindow", "To"))
        self.select_alter_elem_btn.setText(_translate("MainWindow", "Select"))
        self.label_16.setText(_translate("MainWindow", "Alter Range"))
        self.alter_array_btn.setText(_translate("MainWindow", "Array"))
        self.niter_label.setText(_translate("MainWindow", "Iteration Number"))
        self.alter_elem_lineEdit.setPlaceholderText(
            _translate("MainWindow", "Click \'Select\' to set element"))
        self.niter_spinBox.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Total number of points to scan</p></body></html>"
            ))
        self.label_3.setText(_translate("MainWindow", "Additional Wait Time"))
        self.label_4.setText(_translate("MainWindow", "Second"))
        self.waitsec_dSpinBox.setToolTip(
            _translate(
                "MainWindow",
                "<html><head/><body><p>Additional wait time after set new scan point</p></body></html>"
            ))
        self.groupBox.setTitle(_translate("MainWindow", "Data Visualization"))
        self.avg_mplimagewidget.setFigureAspectRatio(
            _translate("MainWindow", "auto"))
        self.tabWidget_3.setTabText(
            self.tabWidget_3.indexOf(self.tab1),
            _translate("MainWindow", "Average"))
        self.std_mplimagewidget.setFigureAspectRatio(
            _translate("MainWindow", "auto"))
        self.tabWidget_3.setTabText(
            self.tabWidget_3.indexOf(self.tab2),
            _translate("MainWindow", "Standard Deviation"))
        self.tabWidget_2.setTabText(
            self.tabWidget_2.indexOf(self.tab),
            _translate("MainWindow", "Curve"))
        self.label.setText(_translate("MainWindow", "Current Settings"))
        self.label_2.setText(_translate("MainWindow", "Monitor of Interest"))
        self.start_btn.setText(_translate("MainWindow", "Start"))


from mpl4qt.widgets.mplerrorbarwidget import MatplotlibErrorbarWidget
from mpl4qt.widgets.mplimagewidget import MatplotlibImageWidget
from . import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
