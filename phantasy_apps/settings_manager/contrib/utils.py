# -*- coding: utf-8 -*-

import csv
import os
import xlrd
import time
from datetime import datetime


class SettingsRow(object):

    """Extract each row of xlsx (see local file) and parse it to settings,
    *write* method can export a CSV file for `Settings Manager`.
    """

    def __init__(self, row, index_elem_list, last_settings_row=None, **kws):
        # cryo module name
        self.name = self._cell_to_string(row[0])
        if self.name is None:
            self.name = last_settings_row.name
        self.name = self.name.replace(' ', '_')
        # cavity id
        self.cid = self._cell_to_cid(row[1])
        # energy, MeV/u
        self.ek = self._cell_to_float(row[2])
        if self.ek is None:
            self.ek = last_settings_row.ek
        #
        self.settings_header = ('Name', 'Field', 'Type', 'Pos',
                                'Setpoint', 'Readback', 'Last Setpoint',
                                'Tolerance', 'Writable')
        settings_table = []
        for i, elem in index_elem_list:
            # i: column index in xlsx
            # i -3: index in SettingsRow.settings list
            new_sp = self._cell_to_float(row[i])
            if new_sp is None:
                try:
                    settings_row = last_settings_row.settings[i - 3]
                except:
                    continue
            else:
                fname = 'I'
                fld = elem.get_field(fname)
                settings_row = (
                    elem.name, fname, elem.family, elem.sb,
                    new_sp, fld.value, fld.current_setting(),
                    0.1, fld.write_access)
            settings_table.append(settings_row)
        self.settings = settings_table
        self.ion_info_idx = kws.pop('ion_info_idx', False)
        self.meta = kws
        if self.ion_info_idx: # ion info is from column defined by index
            for k in ('ion_name', 'ion_number', 'ion_charge', 'ion_mass'):
                if k != 'ion_name':
                    self.meta[k] = int(self._cell_to_float(row[self.meta[k]]))
                else:
                    self.meta[k] = self._cell_to_string(row[self.meta[k]])

    def __eq__(self, other):
        if other is None:
            return False
        if len(self.settings) != len(other.settings):
            return False
        for l, r in zip(self.settings, other.settings):
            # only compare ename, fname, family, spos and set value
            for i in (0, 1, 2, 3, 4):
                if l[i] != r[i]:
                    return False
        return True

    @staticmethod
    def _cell_to_cid(cell):
        if cell.ctype == xlrd.XL_CELL_EMPTY:
            return 0
        elif cell.ctype == xlrd.XL_CELL_TEXT:
            return int(cell.value.split('#')[-1])

    @staticmethod
    def _cell_to_string(cell):
        if cell.ctype == xlrd.XL_CELL_TEXT:
            value = cell.value.strip()
            if len(value) > 0:
                return value
            return None

    @staticmethod
    def _cell_to_float(cell):
        if cell.ctype == xlrd.XL_CELL_TEXT:
            try:
                return float(cell.value)
            except:
                pass
        elif cell.ctype == xlrd.XL_CELL_NUMBER:
            return cell.value
        return None

    def write(self, rootpath=".", filename=None, row_id=None):
        """Write settings into a CSV file for Settings Manager.

        Parameters
        ----------
        rootpath : str
            Parent directory of *filename*.
        filename : str
            File name for CSV settings file, if not defined, use
            <name>-<cid>-<ek>.csv with *name_prefix* as prefix string.
        row_id : int
            Row id if given as name prefix.
        """
        if row_id is None:
            prefix = ''
        else:
            prefix = "{0:03d}".format(row_id)
        if filename is None:
            filename = "{prefix}-{name}-{cid}-{ek:.3f}.csv".format(
                prefix=prefix, name=self.name, cid=self.cid, ek=self.ek)
        filename = filename.replace('#', '_')
        filepath = os.path.abspath(
                os.path.expanduser(os.path.join(rootpath, filename)))
        if not os.path.exists(os.path.dirname(filepath)):
            os.mkdir(os.path.dirname(filepath))
        #
        ts = time.time()
        name = "{prefix}-{name}-{cid}-{ek:.3f}_{ts}".format(
                prefix=prefix, name=self.name, cid=self.cid, ek=self.ek, ts=ts)
        ts_as_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.meta.update({'name': name,
                          'timestamp': ts, 'datetime': ts_as_str, })
        if 'note' not in self.meta:
            note = "Row {prefix}, {ek:.3f} MeV, {name}-#{cid}".format(
                    prefix=prefix, name=self.name, cid=self.cid, ek=self.ek)
            self.meta.update({'note': note})
        #
        with open(filepath, 'w') as fp:
            #
            for k, v in self.meta.items():
                fp.write(f"# {k}: {v}\n")
            #
            ss = csv.writer(fp, delimiter=',')
            ss.writerow(self.settings_header)
            for row in self.settings:
                ss.writerow(row)
        print("Write settings file {}".format(filename))
