#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

from phantasy_ui import get_open_directory

from .ui.ui_fix_names import Ui_Dialog


class FixNamesDialog(QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        super(FixNamesDialog, self).__init__()
        self.parent = parent

        # UI
        self.setupUi(self)
        self.setWindowTitle("Fix Names")

        #
        self.filelist = []
        self.fix_btn.setEnabled(False)

    @pyqtSlot()
    def on_open_files(self):
        """open csv files
        """
        filelist, _  = QFileDialog.getOpenFileNames(self,
                "Select one or more files to open",
                ".",
                "CSV Files (*.csv)")
        if filelist != []:
            self.fix_btn.setEnabled(True)
        else:
            self.fix_btn.setEnabled(False)
            return
        self.csvfilelist_textEdit.setHtml(
                '\n'.join([f'<ul><h4>{i:2d}: {os.path.basename(f)}</h4><p>{f}</p></ul>' for i, f in enumerate(filelist)]))
        self.filelist = filelist

    @pyqtSlot()
    def on_set_export_dir(self):
        # set export dir, otherwise override loaded one.
        d = get_open_directory(self)
        if not os.access(d, os.W_OK):
            return
        self.export_dir_lineEdit.setText(d)

    @pyqtSlot()
    def on_fix(self):
        # see also: settings_manager/contrib/fix_linac_segment_corrector_names.py
        target_dir = self.export_dir_lineEdit.text()
        if target_dir == '':
            overwrite = True
            target_dir = '/tmp'
        else:
            overwrite = False

        from phantasy import MachinePortal
        from phantasy_ui import printlog
        import shutil
        mp = MachinePortal("FRIB", "LINAC")

        i = 0
        for file in self.filelist:
            printlog(f"Fixing {file}...")
            fname = os.path.basename(file)
            outfile = os.path.join(target_dir, fname)

            fin = open(file, 'r')
            fout = open(outfile, 'w')

            for line in fin:
                if line.startswith('#'):
                    fout.write(line)
                else:
                    name, leftover = line.split(',', 1)
                    if 'DCH' in name or 'DCV' in name:
                        a, b = name.rsplit('_', 1)
                        elems = mp.get_elements(name=a + '*_' + b)
                        if elems != []:
                            name1 = elems[0].name
                            line = ','.join((name1, leftover))
                    fout.write(line)
            fin.close()
            fout.close()
            os.utime(outfile, (os.path.getmtime(file), os.path.getmtime(file)))
            if overwrite:
                shutil.copy2(outfile, file)
            printlog(f"Fixed {file}.")
            i += 1
        QMessageBox.information(self, "Fix Names", f"Fixed corrector names in {i} CSV files.",
                                QMessageBox.Ok)
