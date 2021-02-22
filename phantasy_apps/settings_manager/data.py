# -*- coding: utf-8 -*-

import csv
import os
import re
import time
from collections import OrderedDict
from datetime import datetime
from getpass import getuser
from io import StringIO

from phantasy import Settings
from phantasy import get_random_name

CSV_HEADER = (
    'Name', 'Field', 'Type', 'Pos',
    'Setpoint', 'Readback', 'Last Setpoint',
    'Tolerance', 'Writable'
)

LIVE = os.environ.get('LIVE_MODE', True)
if isinstance(LIVE, str):
    LIVE = LIVE.capitalize() == 'True'

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

# default attr keys of snapshotdata
ATTR_KEYS = [
    "timestamp", "datetime", "name", "note", "user",
    "ion_name", "ion_number", "ion_mass", "ion_charge",
    "machine", "segment", "tags", "app", "version",
]

#
# key is old element name, value is the new name for loading.
#
ELEM_ALIAS_MAP = {
 'FE_ISRC1:HVP_D0679:V': 'FE_ISRC1:HVP_D0679',
 'FE_ISRC1:HVP_D0698:V': 'FE_ISRC1:HVP_D0698',
 'FE_ISRC1:PSEL_D0679:V': 'FE_ISRC1:PSEL_D0679',
 'FE_ISRC1:PSEL_D0698:V': 'FE_ISRC1:PSEL_D0698',
 'FE_ISRC1:PSX_D0679:V': 'FE_ISRC1:PSX_D0679',
 'FE_ISRC1:PSB_D0679:V': 'FE_ISRC1:PSB_D0679',
 'FE_ISRC1:PSE_D0686:V': 'FE_ISRC1:PSE_D0686',
 'FE_ISRC1:SOLR_D0690:I': 'FE_ISRC1:SOLR_D0690',
 'FE_ISRC1:DCH_D0695:I': 'FE_ISRC1:DCH_D0695',
 'FE_ISRC1:DCV_D0695:I': 'FE_ISRC1:DCV_D0695',
 'FE_ISRC1:PSOL_D0682:I': 'FE_ISRC1:SOLR_D0682',
 'FE_ISRC1:PSOL_D0685:I': 'FE_ISRC1:SOLR_D0685',
 'FE_RFQ:RFC_D1005:PHA': 'FE_RFQ:CAV_D1005',
 'FE_RFQ:RFC_D1005:E': 'FE_RFQ:CAV_D1005',
 'FE_ISRC1:BEAM:A_BOOK': 'FE_ISRC1:BEAM',
 'FE_ISRC1:BEAM:Q_BOOK': 'FE_ISRC1:BEAM',
 'FE_ISRC1:BEAM:Z_BOOK': 'FE_ISRC1:BEAM',
}

# field alias (RFQ, ION)
FIELD_ALIAS_MAP = {
 'E': 'AMP',
 'A_BOOK': 'A',
 'Q_BOOK': 'Q',
 'Z_BOOK': 'Z'
}


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
        if name in ELEM_ALIAS_MAP:
            name = ELEM_ALIAS_MAP[name]
        elem = lat[name]
        eng_fields = elem.get_eng_fields()
        phy_fields = elem.get_phy_fields()
        field = FIELD_ALIAS_MAP.get(field, field)
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


def read_data(data_source, data_type='csv'):
    """Read settings data with attribute values from data source.

    Supported data source: .csv file.
    To be supported data source: .sql file.
    Each .csv file is one snapshot, while each .sql may contain multiple.

    Parameters
    ----------
    data_source : str
        Path of the data source.
    data_type : str
        Data type, currently only 'csv' is supported.

    Returns
    -------
    (data, attr) : A tuple of settings list and attributes dict.
    """
    if data_type == 'csv':
        _path = os.path.abspath(os.path.expanduser(data_source))
        data_list, attr_dict = _read_csv_data(_path)
        # instantiate SnapshotData
        snp_data = SnapshotData(data_list, **attr_dict)
    else:
        raise RuntimeError(f"Load data source of type '{data_type}' is not implemented.")
    return snp_data


def _read_csv_data(data_source, delimiter=','):
    """Load data from .csv file to SnapshotData instance, initial attribute key: 'data_path'.

    Read CSV file with the lines starting with '#' as dict of comments,
    and the first line after comments section as header.
    """
    attr_dict = {'data_path': data_source}
    data_list = []
    with open(data_source, 'r') as fp:
        for line in fp:
            if line.startswith('#'):
                k, v = line.strip('# ,\n').split(':', 1)
                if k == 'timestamp':
                    attr_dict[k] = float(v.strip())
                else:
                    attr_dict[k] = v.strip()
            else:
                break
        ss = csv.reader(fp, delimiter=delimiter, skipinitialspace=True)
        header = [i.strip() for i in line.split(delimiter)]
        for ename, field, ftype, spos, sp, rd, last_sp, tol, writable in ss:
            data_list.append(
                (ename, field, ftype, spos,
                 float(sp), float(rd), float(last_sp),
                 float(tol), bool(writable)))
    return data_list, attr_dict


class SnapshotData:
    """Snapshot data object, instantiated from settings data with attributes.

    Parameters
    ----------
    data_list : list
        A list of settings tuple.
    """
    def __init__(self, data_list, **kws):
        self.data = data_list
        self.init_attr()
        self.init_attr_dict(**kws)
        self.meta_keys = ATTR_KEYS[:]
        for k in kws:
            if k == 'data_path' or k in self.meta_keys:
                continue
            self.meta_keys.append(k)

    def init_attr(self):
        self._ts = None
        self._datetime = None
        self._name = None
        self._note = None
        self._user = None
        self._ion_name = None
        self._ion_number = None
        self._ion_mass = None
        self._ion_charge = None
        self._machine = None
        self._segment = None
        self._tags = None
        self.data_path = None

    def init_attr_dict(self, **kws):
        d = {k: None for k in ATTR_KEYS}
        d.update(kws)
        for k, v in d.items():
            if k == 'datetime':
                continue  # present timestamp in another way
            elif k == 'app' and v is None: # app name
                v = 'Settings Manager'
            elif k == 'version' and v is None: # app version
                v = 'undefined'
            setattr(self, k, v)

    @property
    def tags(self):
        """List of strings.
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        # input: str separated by ',', delete whitespace if any, or list of strings.
        # ignore empty str ''.
        if tags is None:
            self._tags = []
        else:
            if isinstance(tags, str):
                _tags = tags.split(',')
            elif isinstance(tags, (list, tuple)):
                _tags = tags
            self._tags = [i for i in [re.sub(r'\s+', '', s) for s in _tags] if i != '']

    def ts_as_str(self):
        return datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%dT%H:%M:%S')

    def ts_as_fn(self):
        return datetime.fromtimestamp(self.timestamp).strftime('%Y%m%dT%H%M%S')

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

    def get_default_data_path(self, working_directory=None, data_type='csv'):
        """Return full data path for saving by naming convention,
        the data directory by default is ., e.g. ./40Ar+9_20200929T104317.csv.
        """
        if working_directory is None:
            wdir = '.'
        else:
            wdir = os.path.expanduser(working_directory)
        fn = f"{self.ion_mass}{self.ion_name}+{self.ion_charge}_{self.ts_as_fn()}.csv"
        return os.path.abspath(os.path.join(wdir, fn))

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
            self._name = get_random_name() + "_" + str(time.time_ns())
        else:
            self._name = s

    @property
    def machine(self):
        return self._machine

    @machine.setter
    def machine(self, s):
        if s is None:
            self._machine = DEFAULT_MACHINE
        else:
            self._machine = s

    @property
    def segment(self):
        return self._segment

    @segment.setter
    def segment(self, s):
        if s is None:
            self._segment = DEFAULT_SEGMENT
        else:
            self._segment = s

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, s):
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
            self._ts = time.time()
        else:
            self._ts = x
        self._datetime = self.ts_as_str()

    @property
    def datetime(self):
        return self._datetime

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, s):
        if s is None or s == '':
            self._note = 'Input note ...'
        else:
            self._note = s

    def is_golden(self):
        return 'golden' in self.tags

    def __str__(self):
        sio = StringIO()
        sio.write("\t".join(CSV_HEADER))
        sio.write("\n")
        for ename, fname, ftype, spos, sp, rd, old_sp, tol, writable in self.data:
            sio.write(
                f"{ename}\t{fname}\t{ftype}\t{spos}\t{sp}\t{rd}\t{old_sp}\t{tol}\t{writable}\n")
        text = sio.getvalue()
        sio.close()
        return text

    def write(self, filepath, delimiter=','):
        """Write settings into *filepath*.
        """
        with open(filepath, 'w') as fp:
            for k in self.meta_keys:
                v = getattr(self, k)
                if k == 'tags':
                    v = self.tags_as_str()
                fp.write(f"# {k}: {v}\n")
            ss = csv.writer(fp, delimiter=delimiter)
            ss.writerow(CSV_HEADER)
            for ename, fname, ftype, spos, sp, rd, old_sp, tol, writable in self.data:
                ss.writerow(
                    (ename, fname, ftype, spos, sp, rd, old_sp, tol, writable))

