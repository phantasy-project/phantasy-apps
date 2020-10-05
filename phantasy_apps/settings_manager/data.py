# -*- coding: utf-8 -*-

import csv
import os
from collections import OrderedDict
import time
from datetime import datetime
from getpass import getuser
import pwd

from phantasy import Settings
from phantasy import get_random_name

CSV_HEADER = (
    'Name', 'Field', 'Type', 'Pos',
    'Setpoint', 'Readback', 'Last Setpoint',
    'Tolerance', 'Writable'
)

LIVE = True

if not LIVE:
    DEFAULT_MACHINE = "FRIB_VA"
    DEFAULT_SEGMENT = "LS1FS1"
else:
    DEFAULT_MACHINE = "FRIB"
    DEFAULT_SEGMENT = "LINAC"

#
ELEMT_PATH = os.path.join(os.path.dirname(__file__), 'config', 'elements.json')
DEFAULT_SETTINGS = Settings(ELEMT_PATH)
#

def make_physics_settings(csv_settings, lat):
    """Generate Settings (lattice settings) of *lat* from `TableSettings`
    instance defined by *csv_settings*.
    For lattice settings, all settings are physics field settings.

    Parameters
    ----------
    csv_settings : TableSettings
        TableSettings instance from CSV settings file.
    lat : Lattice
        High-level lattice object, or a list of CaElement(s).

    Returns
    -------
    r : Settings
        Physics settings.
    """
    s = Settings()  # physics settings
    for name, field, _, _, sp, rd, last_sp, _, _ in csv_settings:
        elem = lat[name]
        eng_fields = elem.get_eng_fields()
        phy_fields = elem.get_phy_fields()
        fld = elem.get_field(field)
        if name not in s:
            s[name] = OrderedDict()
        # generate PHY field from ENG field
        if fld.is_engineering_field():
            phy_field = phy_fields[eng_fields.index(field)]
            phy_sp = elem.convert(sp, field)
            phy_rd = elem.convert(rd, field)
            phy_last_sp = elem.convert(last_sp, field)
        else:
            phy_field = field
            phy_sp = sp
            phy_rd = rd
            phy_last_sp = last_sp
        s[name].update([(phy_field, phy_sp)])
    return s


class TableSettings(list):
    """List of device settings (read from CSV file from Settings Manager),
    each list element is a tuple of device name (ename), field name (fname),
    field set value (sp), field value (rd) and last field set value (last sp).

    Parameters
    ----------
    settings_path : str
        CSV settings data filepath.
    """

    def __init__(self, settings_path=None, **kws):
        # kws: delimiter
        # settings_path is csv file path.
        super(TableSettings, self).__init__()
        self.header = None
        delimiter = kws.pop('delimiter', ',')
        self.meta = kws
        if isinstance(settings_path, str):
            self.read(settings_path, delimiter)

    def read(self, path, delimiter=','):
        """Read CSV file with the lines starting with '#' as dict of comments,
        and the first line after comments section as header.
        """
        meta_str_list = []
        with open(path, 'r') as f:
            for line in f:
                if line.startswith('#'):
                    meta_str_list.append(line.strip('# ,\n'))
                else:
                    break
            ss = csv.reader(f, delimiter=delimiter, skipinitialspace=True)
            self.header = [i.strip() for i in line.split(',')]
            for ename, field, ftype, spos, sp, rd, last_sp, tol, writable in ss:
                self.append(
                    (ename, field, ftype, spos,
                     float(sp), float(rd), float(last_sp),
                     float(tol), bool(writable)))
        self.update_meta(meta_str_list)

    def update_meta(self, s_list):
        # update meta with a list of line startswith '#'
        meta_dict = {k: v.strip() for k, v in (i.split(':', 1) for i in s_list)}
        if 'timestamp' in meta_dict:
            meta_dict['timestamp'] = float(meta_dict['timestamp'])
        self.meta.update(meta_dict)

    def write(self, filepath, header=None, delimiter=','):
        """Write settings into *filepath*.
        """
        with open(filepath, 'w') as fp:
            for k, v in self.meta.items():
                fp.write(f"# {k}: {v}\n")
            ss = csv.writer(fp, delimiter=delimiter)
            if header is not None:
                ss.writerow(header)
            elif self.header is not None:
                ss.writerow(self.header)
            for ename, field, ftype, spos, sp, rd, old_sp, tol, writable in self:
                ss.writerow(
                    (ename, field, ftype, spos, sp, rd, old_sp, tol, writable))


def get_csv_settings(proxy_model):
    """Get settings data from *proxy_model* as TableSettings.
    """
    # new_sp (x2): current sp to save
    # new_rd (x1): rb at sp
    # old_sp (x0): last_sp
    m = proxy_model
    src_m = proxy_model.sourceModel()
    i_name, i_field, i_type, i_pos, i_new_sp, i_new_rd, i_old_sp, \
    i_tol, i_writable = \
        src_m.i_name, src_m.i_field, src_m.i_type, src_m.i_pos, \
        src_m.i_cset, src_m.i_rd, src_m.i_val0, src_m.i_tol, src_m.i_writable

    data = TableSettings()
    for irow in range(m.rowCount()):
        ename = m.data(m.index(irow, i_name))
        fname = m.data(m.index(irow, i_field))
        ftype = m.data(m.index(irow, i_type))
        spos = float(m.data(m.index(irow, i_pos)))
        f_new_sp = float(m.data(m.index(irow, i_new_sp)))
        f_old_sp = float(m.data(m.index(irow, i_old_sp)))
        f_new_rd = float(m.data(m.index(irow, i_new_rd)))
        f_tol = float(m.data(m.index(irow, i_tol)))
        f_writable = m.data(m.index(irow, i_writable))
        data.append((ename, fname, ftype, spos,
                     f_new_sp, f_new_rd, f_old_sp,
                     f_tol, f_writable))
    return data


class ToleranceSettings(Settings):
    """Settings for tolerance, keep tolerance element, field-wise
    e.g. {ename: {fname1: tol1, fname2: tol2}}
    """

    def __init__(self, settings_path=None):
        if settings_path is not None and os.path.isfile(settings_path):
            settingsPath = settings_path
        else:
            settingsPath = None
        super(self.__class__, self).__init__(settingsPath)
        self.settings_path = settings_path


class ElementPVConfig(Settings):
    """PV configurations for element from setpoint/readback PVs.
    e.g. {ename: {setpoint: sppv, readback: rdpv}}
    """

    def __init__(self, settings_path=None):
        if settings_path is not None and os.path.isfile(settings_path):
            settingsPath = settings_path
        else:
            settingsPath = None
        super(self.__class__, self).__init__(settingsPath)
        self.settings_path = settings_path
        self.update(DEFAULT_SETTINGS)


class SnapshotData:
    """Snapshot data.
    """
    def __init__(self, tablesettings, name=None, **kws):
        self.data = tablesettings
        self._ts = time.time()
        self._user = getuser()
        self.name = name
        self.wdir = kws.pop('wdir', '.')
        self.ion_name = kws.pop('ion_name', None)
        self.ion_number = kws.pop('ion_number', None) # Z (str)
        self.ion_mass = kws.pop('ion_mass', None) # A (str)
        self.ion_charge = kws.pop('ion_charge', None) # Q (str)
        self.machine = kws.pop('machine', DEFAULT_MACHINE)
        self.segment = kws.pop('segment', DEFAULT_SEGMENT)
        self.tags = kws.pop('tags', None) # list of string as tags
        note = ''
        for k, v in kws.items():
            if v == '':
                continue
            note += f'{k}: {v}, '
        self.note = note
        self._filepath = None

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, tags):
        if tags is None:
            self._tags = []
        else:
            if isinstance(tags, str):
                self._tags = [s.strip() for s in tags.split(',')]
            elif isinstance(tags, (list, tuple)):
                self._tags = tags

    def ts_as_str(self):
        return datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%dT%H:%M:%S')

    def ts_as_date(self):
        return datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %A')

    def ts_as_time(self):
        return datetime.fromtimestamp(self.timestamp).strftime('%H:%M:%S')

    def ion_as_str(self):
        if self._ion_name is None:
            return ""
        return f"{self._ion_mass}{self._ion_name}{self._ion_number}(+{self._ion_charge})"

    def tags_as_str(self):
        return ",".join(self._tags)

    @property
    def ion_name(self):
        return self._ion_name

    @ion_name.setter
    def ion_name(self, s):
        if s is None:
            self._ion_name = ''
        else:
            self._ion_name = s

    @property
    def ion_number(self):
        return self._ion_number

    @ion_number.setter
    def ion_number(self, i):
        if i is None:
            self.ion_number = ''
        else:
            self._ion_number = str(i)

    @property
    def ion_mass(self):
        return self._ion_mass

    @ion_mass.setter
    def ion_mass(self, i):
        if i is None:
            self._ion_mass = ''
        else:
            self._ion_mass = str(i)

    @property
    def ion_charge(self):
        return self._ion_charge

    @ion_charge.setter
    def ion_charge(self, i):
        if i is None:
            self._ion_charge = ''
        else:
            self._ion_charge = str(i)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, s):
        if s is None:
            self._name = get_random_name() + "_" + str(time.time())
        else:
            self._name = s

    @property
    def username(self):
        return self._user

    @username.setter
    def username(self, s):
        if s is None:
            self._user = getuser()
        else:
            self._user = s

    @property
    def timestamp(self):
        return self._ts

    @timestamp.setter
    def timestamp(self, x):
        if x is None:
            if self._filepath is not None:
                self._ts = os.path.getmtime(self._filepath)
                self._user = pwd.getpwuid(os.stat(self._filepath).st_uid).pw_name
            else:
                self._ts = time.time()
                self._user = getuser()
        else:
            self._ts = x

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, s):
        if s is None or s == '':
            self._note = 'Input note ...'
        else:
            self._note = s

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, s):
        self._filepath = s

    def update_meta(self):
        # update tablesettings meta
        self.data.meta = {
            'timestamp': self._ts,
            'datetime': self.ts_as_str(),
            'name': self._name,
            'note': self._note,
            'filepath': self._filepath,
            'user': self._user,
            'ion_name': self._ion_name,
            'ion_number': self._ion_number,
            'ion_mass': self._ion_mass,
            'ion_charge': self._ion_charge,
            'machine': self.machine,
            'segment': self.segment,
            'tags': ','.join(self.tags),
        }

    def update_properties(self):
        # update with tablesettings meta
        self.note = self.data.meta.get('note', None)
        self.timestamp = self.data.meta.get('timestamp', None)
        self.username = self.data.meta.get('user', None)
        self.ion_name = self.data.meta.get('ion_name', None)
        self.ion_number = self.data.meta.get('ion_number', None)
        self.ion_mass = self.data.meta.get('ion_mass', None)
        self.ion_charge = self.data.meta.get('ion_charge', None)
        self.machine = self.data.meta.get('machine', DEFAULT_MACHINE)
        self.segment = self.data.meta.get('segment', DEFAULT_SEGMENT)
        self.tags = self.data.meta.get('tags', None)

    def is_golden(self):
        return 'golden' in self.tags
