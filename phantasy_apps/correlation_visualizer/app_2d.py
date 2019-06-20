#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""2D params scan.

Tong Zhang <zhangt@frib.msu.edu>
2019-06-20 10:59:21 AM EDT
"""

from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QDialog

from phantasy_ui import BaseAppForm
from phantasy_ui.widgets import ElementWidget

from .app_elem_select import ElementSelectDialog
from .ui.ui_2dscan import Ui_MainWindow


class TwoParamsScanWindow(BaseAppForm, Ui_MainWindow):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self._p = parent

        self.setAppVersion(parent._version)
        app_title_p = parent.getAppTitle()
        self.setAppTitle("{}[{}]".format(app_title_p, '2D'))
        self.setWindowTitle("{}: {}".format(
            app_title_p, "Extend to Higher Dimension"))


        #
        self.select_alter_elem_btn.clicked.connect(self.on_select_elem)
        self._sel_elem_dialogs = {}
        self.elem_widgets_dict = {}

    def on_select_elem(self):
        """Select element via PV or high-level element for alter-vars and
        monitor-vars.
        """

        mode = "alter"
        dlg = self._sel_elem_dialogs.setdefault(mode, ElementSelectDialog(self, mode, mp=self._p._mp))
        r = dlg.exec_()
        self._p.elementsTreeChanged.connect(dlg.on_update_elem_tree)

        if r == QDialog.Accepted:
            # update element obj (CaField)
            sel_elem = dlg.sel_elem[0]  # CaField
            sel_elem_display = dlg.sel_elem_display[0]  # CaElement
            fname = dlg.sel_field[0]
            if fname is None:
                elem_btn_lbl = sel_elem_display.ename
            else:
                elem_btn_lbl = '{0} [{1}]'.format(sel_elem_display.name, fname)

            new_sel_key = ' '.join((sel_elem_display.ename, sel_elem.name, mode))
            # create elem_info widget, add into *elem_widgets_dict*
            self.elem_widgets_dict.setdefault(
                new_sel_key, ElementWidget(sel_elem_display, fields=fname))

            elem_btn = self._p._create_element_btn(elem_btn_lbl, new_sel_key,
                                                   self.elem_widgets_dict)
            self._p._place_element_btn(elem_btn, mode,
                                       target=self.alter_elem_lineEdit)

            """
            #
            self.scan_task.alter_element = sel_elem
            # initialize scan range
            x0 = self.scan_task.get_initial_setting()
            self.lower_limit_lineEdit.setText('{}'.format(x0))
            self.upper_limit_lineEdit.setText('{}'.format(x0))
            """

            # debug
            print("-" * 20)
            print(sel_elem)
            print("-" * 20)
            print(sel_elem_display)
            print("-" * 20)
            print(elem_btn_lbl)
            print("-" * 20)
            #

        elif r == QDialog.Rejected:
            # do not update alter element obj
            return
