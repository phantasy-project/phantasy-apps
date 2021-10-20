# -*- coding: utf-8 -*-

import csv
import hashlib
import io
import os
import pathlib
import re
import tempfile
import time
import pandas as pd
from collections import OrderedDict
from datetime import datetime
from getpass import getuser

from PyQt5.QtCore import Qt

from phantasy import Settings

from .conf import DEFAULT_MACHINE, DEFAULT_SEGMENT

# default data format to save
DEFAULT_DATA_FMT = "xlsx"

# support file types
SUPPORT_FTYPES = ("xlsx", "csv", "h5", "sql")

CSV_HEADER = (
    'Name', 'Field', 'Type', 'Pos',
    'Setpoint', 'Readback', 'Last Setpoint',
    'Tolerance', 'Writable'
)

CSV_HEADER_9 = CSV_HEADER

CSV_HEADER_10 = (
    'Name', 'Field', 'Type', 'Pos',
    'Setpoint', 'Readback', 'Last Setpoint',
    'Tolerance', 'Writable', 'Last Power State'
)

# For table_version of SnapshotData:
# CSV_HEADER: 9
# CSV_HEADER, LAST_POWER_STATUS: 10

#
ELEMT_PATH = os.path.join(os.path.dirname(__file__), 'config', 'elements.json')
DEFAULT_SETTINGS = Settings(ELEMT_PATH)
#

# default attr keys of snapshotdata
ATTR_KEYS = [
    "timestamp", "datetime", "name", "note", "user",
    "ion_name", "ion_number", "ion_mass", "ion_charge",
    "machine", "segment", "tags", "app", "version",
    "table_version",
]

ATTR_DICT = OrderedDict([(k, None) for k in ATTR_KEYS])

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
 'FE_SCS1:STPC01_D0736:SLR.VAL': 'FE_SCS1:SLT_D0736',
 'FE_SCS1:STPC01_D0736:SLL.VAL': 'FE_SCS1:SLT_D0736',
 'FE_SCS1:STPC01_D0736:SLT.VAL': 'FE_SCS1:SLT_D0736',
 'FE_SCS1:STPC01_D0736:SLB.VAL': 'FE_SCS1:SLT_D0736',
 'FE_ISRC1:DRV_D0686:POS': 'FE_ISRC1:DRV_D0686',
 'FS1_BBS:CSEL_D2405:L': 'FS1_BBS:SLH_D2405',
 'FS1_BBS:CSEL_D2405:R': 'FS1_BBS:SLH_D2405',
 'FS1_BBS:CSEL_D2405:CTR_MTR.RBV': 'FS1_BBS:SLH_D2405',
 'FS1_STRS:STPC03_D2237:DRV1': 'FS1_CSS:STRIP_D2249',
 'FS1_STRS:STPC03_D2237:DRV2': 'FS1_CSS:STRIP_D2249',
}

# field alias (RFQ, ION)
FIELD_ALIAS_MAP = {
 'E': 'AMP',
 'A_BOOK': 'A',
 'Q_BOOK': 'Q',
 'Z_BOOK': 'Z',
 'SLR.VAL': 'RIGHT',
 'SLL.VAL': 'LEFT',
 'SLT.VAL': 'TOP',
 'SLB.VAL': 'BOTTOM',
 'L': 'LEFT',
 'R': 'RIGHT',
 'CTR_MTR.RBV': 'CENTER',
 'DRV1': 'POS',
 'DRV2': 'ANGLE',
}


def make_physics_settings(settings, lat):
    """Generate Settings (lattice settings) of *lat* from a list of
    field settings, defined by *settings*.
    For lattice settings, all settings are physics field settings.

    Parameters
    ----------
    settings : sequence
        An array of list settings, each list contains settings for one field.
    lat : Lattice
        High-level lattice object, or a list of CaElement(s).

    Returns
    -------
    r : Settings
        Physics settings.
    """
    s = Settings()  # physics settings
    for line in settings:
        name, field, _, _, sp, rd, last_sp, _, _ = line[0:9]
        if name in ELEM_ALIAS_MAP:
            name = ELEM_ALIAS_MAP[name]
        elem = lat[name]
        if elem is None:
            s[name] = {field: sp}  # element is not existing any more
            continue
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


def get_settings_data(proxy_model):
    """Get settings data from *proxy_model* as a DataFrame.
    """
    # new_sp (x2): current sp to save
    # new_rd (x1): rb at sp
    # old_sp (x0): last_sp
    # new_ps (ps): current power/lock(CAV) status
    m = proxy_model
    src_m = proxy_model.sourceModel()
    i_name, i_field, i_type, i_pos, i_new_sp, i_new_rd, i_old_sp, \
    i_tol, i_writable, i_pwr = \
        src_m.i_name, src_m.i_field, src_m.i_type, src_m.i_pos, \
        src_m.i_cset, src_m.i_rd, src_m.i_val0, src_m.i_tol, src_m.i_writable, src_m.i_pwr

    data = []
    for irow in range(m.rowCount()):
        ename = m.data(m.index(irow, i_name))
        fname = m.data(m.index(irow, i_field))
        ftype = m.data(m.index(irow, i_type))
        spos = float(m.data(m.index(irow, i_pos)))

        try:
            f_new_sp = float(m.data(m.index(irow, i_new_sp)))
        except ValueError:
            f_new_sp = None
        try:
            f_old_sp = float(m.data(m.index(irow, i_old_sp)))
        except ValueError:
            f_old_sp = None
        try:
            f_new_rd = float(m.data(m.index(irow, i_new_rd)))
        except ValueError:
            f_new_rd = None

        f_tol = float(m.data(m.index(irow, i_tol)))
        f_writable = m.data(m.index(irow, i_writable))
        f_pwr = m.data(m.index(irow, i_pwr), Qt.ToolTipRole)
        data.append((ename, fname, ftype, spos,
                     f_new_sp, f_new_rd, f_old_sp,
                     f_tol, f_writable, f_pwr))
    return pd.DataFrame(data, columns=CSV_HEADER_10)


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


def read_data(data_path, file_type=None):
    """Read settings data with attribute values from data source.

    Supported data source: .csv, .xls, .h5 files.

    Parameters
    ----------
    data_path : Path
        Path of the data source, or dataframe for 'sql' file_type.
    file_type : str
        File type.

    Returns
    -------
    r : SnapshotData
    """
    if isinstance(data_path, (pathlib.Path, str)):
        # filepath
        data_path = pathlib.Path(data_path)
        if file_type is None:
            file_type = data_path.suffix.lower()[1:]
        if file_type not in SUPPORT_FTYPES:
            print(f"Non-support file type: {file_type}.")
            return None
        data_src = data_path.resolve()
    else:
        # DATABASE, --> _sql, df
        file_type = '_sql'
        data_src = data_path

    try:
        r = SnapshotData.read(data_src, ftype=file_type)
    except:
        r = None
    finally:
        return r


def read_hdf(filepath, **kws):
    """Read data from an HDF5 data file (e.g. h5).

    Parameters
    ----------
    filepath : str
        File path.

    Returns
    -------
    r : tuple
        Tuple of (df_data, df_info, df_state), df_data: physics settings,
        df_info: meta info for physics settings, df_state: machine state.
    """
    with pd.HDFStore(filepath, **kws) as store:
        df_data = store.get(SnapshotData.SETTINGS_SHEET_NAME)
        attr_dict = getattr(store.get_storer(SnapshotData.SETTINGS_SHEET_NAME).attrs,
                            SnapshotData.INFO_SHEET_NAME)
        # attr_dict['data_path'] = os.path.abspath(filepath)
        # attr_dict.move_to_end('data_path', last=False)
        df_info = pd.DataFrame.from_dict(attr_dict, orient='index', columns=["attribute"]).T
        if f"/{SnapshotData.MACHSTATE_SHEET_NAME}" in store.keys():
            df_machstate = store.get(SnapshotData.MACHSTATE_SHEET_NAME)
        else:
            df_machstate = None
    return df_data, df_info, df_machstate


def read_excel(filepath, **kws):
    """Read data from an Excel data file (e.g. xlsx).

    Parameters
    ----------
    filepath : str
        File path

    Returns
    -------
    r : tuple
        Tuple of (df_data, df_info, df_state), df_data: physics settings,
        df_info: meta info for physics settings, df_state: machine state.
    """
    with pd.ExcelFile(filepath, **kws) as fp:
        _df = pd.read_excel(fp, sheet_name=SnapshotData.INFO_SHEET_NAME, header=None, index_col=0)
        _df.rename(columns={1: 'attribute'}, inplace=True)
        _df.index.name = None
#        if _df.T.tags[0] == ['nan']:  # reset tags to []
#            _df.loc['attribute', 'tags'] = []
        #df_info = _df.T
        #df_info.insert(0, "data_path", os.path.abspath(filepath))
        df_data = pd.read_excel(fp, sheet_name=SnapshotData.SETTINGS_SHEET_NAME)
        if SnapshotData.MACHSTATE_SHEET_NAME in fp.sheet_names:
            df_machstate = pd.read_excel(fp, sheet_name=SnapshotData.MACHSTATE_SHEET_NAME, index_col=[0, 1])
        else:
            df_machstate = None
    return df_data, _df.T, df_machstate


def read_sql(df):
    """Read a row of data into SnapshotData. The row of data is originated from a DataFrame
    from a sqlite database.
    """
    data_format = df.data_format
    if data_format == 'xlsx':
        return read_excel(io.BytesIO(df.data))
    elif data_format == 'csv':
        return read_csv(io.BytesIO(df.data))
    elif data_format in ('h5', 'hdf5'):
        _, mfile = tempfile.mkstemp(".h5")
        with open(mfile, "wb") as fp:
            fp.write(df.data)
            r = read_hdf(mfile)
        os.remove(mfile)
        return r


def _read_sql(df):
    def _df_info_from_df(df):
        # return df_info part for SnapshotData, df <-- irow
        d = {'timestamp': df.timestamp, 'datetime': df.datetime,
             'name': df['name'], 'note': df.note, 'user': df.user,
             'ion_name': df.ion_name, 'ion_number': df.ion_number, 'ion_mass': df.ion_mass,
             'ion_charge': df.ion_charge, 'machine': df.machine, 'segment': df.segment,
             'app': df.app, 'version': df.version, 'tags': df.tags}
        r = pd.DataFrame.from_dict(d, orient='index')
        r.rename(columns={0: 'attribute'}, inplace=True)
        return r.T
    return None, _df_info_from_df(df), df


def read_csv(filepath, delimiter=','):
    """Load data from a csv file to SnapshotData instance, initial attribute key: 'data_path'.

    Read CSV file with the lines starting with '#' as dict of comments,
    and the first line after comments section as header, the rest as settings data.

    Returns
    -------
    r : tuple
        A tuple of two dataframes, the first is physics settings table, the other is the metadata
        describing the settings, the third is None (for machine state)
    """
    attr_dict = OrderedDict()
    stream_type = None
    if isinstance(filepath, (str, pathlib.Path)): # path
        stream_type = 'file'
        fp = open(filepath, 'r')
    else:
        stream_type = 'bytes'
        fp = filepath # BytesIO
    for line in fp:
        if stream_type == 'bytes':
            line = line.decode()
        if line.startswith('#'):
            k, v = line.strip('# ,\n').split(':', 1)
            if k == 'timestamp':
                attr_dict[k] = float(v.strip())
            else:
                attr_dict[k] = v.strip()
        else:
            break
    header = [i.strip() for i in line.split(delimiter)]
    df_info = pd.DataFrame.from_dict(attr_dict, orient='index', columns=['attribute']).T
    df_data = pd.read_csv(fp, names=header)
    if stream_type == 'file':
        fp.close()
    return df_data, df_info, None


class SnapshotData:
    """Snapshot data object, instantiated from settings data with attributes passed by keyword
    arguments.

    Parameters
    ----------
    df_data : DataFrame
        Physics settings.
    df_info : DataFrame
        Meta info for physics settings.

    Keyword Arguments
    -----------------
    other meta info key-value pairs add/update to *df_info*, key should be in ATTR_KEYS.
    """
    INFO_SHEET_NAME = "info"
    SETTINGS_SHEET_NAME = "settings"
    MACHSTATE_SHEET_NAME = "machine_state"
    _READER_MAP = {
        'xlsx': read_excel,
        'hdf': read_hdf,
        'h5': read_hdf,
        'csv': read_csv,
        'sql': read_sql,
        '_sql': _read_sql,
    }
    def __init__(self, df_data, df_info=None, **kws):
        # setter dict: default/special values
        from phantasy_apps.settings_manager import __version__
        self.__setter_map = {
            'name': lambda v: get_sha1()[0] if v is None else v,
            'user': lambda v: getuser() if v is None else v,
            'timestamp': lambda v: time.time() if v is None else v,
            'note': lambda v: 'Input note ...' if v is None else v,
            'machine': lambda v: DEFAULT_MACHINE if v is None else v,
            'segment': lambda v: DEFAULT_SEGMENT if v is None else v,
            'ion_name': lambda v: '' if v is None else str(v),
            'ion_mass': lambda v: '' if v is None else str(v),
            'ion_charge': lambda v: '' if v is None else str(v),
            'ion_number': lambda v: '' if v is None else str(v),
            'table_version': lambda v: 9 if v is None else v,
            'version': lambda v: __version__ if v is None else v,
            'app': lambda v: 'Settings Manager' if v is None else v,
            'tags': self.__get_tags,
        }
        self.__writer_map = {
             'xlsx': self.__write_to_excel,
             'hdf': self.__write_to_hdf,
             'h5': self.__write_to_hdf,
             'csv': self.__write_to_csv,
        }
        #
        self.data = df_data
        self.info = df_info
        self.__update_info(**kws)
        # update tags : str -> list
        self.__update_tags()
        # by default data_path is None, only be updated when saving/loading to/from file.
        self.data_path = None
        # machine state data
        self.machstate = None
        # placeholder for df row (DB)
        self._blob = None

    @property
    def data_path(self):
        return self._data_path

    @data_path.setter
    def data_path(self, s):
        self._data_path = s

    @property
    def machstate(self):
        return self._machstate

    @machstate.setter
    def machstate(self, df):
        """Set machine state with a dataframe.
        """
        if df is None:
            self._machstate = None
        else:
            self._machstate = df

    @property
    def info(self):
        """DataFrame : Column-wised attributes table.
        """
        return self._df_info

    @info.setter
    def info(self, df=None):
        if df is None:
            self._df_info = pd.DataFrame.from_dict(ATTR_DICT, orient='index', columns=['attribute']).T
        else:
            self._df_info = df

    def __setattr__(self, k, v):
        if k in ATTR_KEYS:
            if k == 'datetime':
                # alias attribute for timestamp, cannot be set
                raise AttributeError(f"Readonly attribute cannot be changed")
            else:
                v = self.__setter_map.get(k, lambda v:v)(v)
            self._df_info.loc['attribute', k] = v
            if k == 'timestamp':
                self._df_info['datetime'] = self.ts_as_str()
        else:
            super(SnapshotData, self).__setattr__(k, v)

    def __getattr__(self, k):
        if k in self._df_info:
            return self._df_info[k][0]
        else:
            raise AttributeError(f"Invalid attribute '{k}'")

    def __update_tags(self):
        tags = self.info['tags'][0]
        # update tags to list from str (after read from data file)
        self.info.loc['attribute', 'tags'] = self.__get_tags(tags)

    def __update_info(self, **kws):
        """Initial and update (with keyword arguments) info table.
        """
        d = self._df_info.T['attribute'].to_dict()
        d.update(kws)
        for k, v in d.items():
            if k == 'datetime':
                continue  # present timestamp in another way
            setattr(self, k, v)

    def __dir__(self):
        return dir(__class__) + list(self.__dict__.keys()) \
                + self._df_info.keys().tolist()

    def __get_tags(self, v):
        # get a list of tags from input *v* (str)  to set .tags attribute
        if v is None:
            v = []
        else:
            # input: str separated by ',', delete whitespace if any, or list of strings.
            # ignore empty str ''.
            if isinstance(v, str):
                _tags = v.split(',')
            elif isinstance(v, (list, tuple)):
                _tags = v
            else:
                _tags = [str(v),]
            v = [i for i in [re.sub(r'\s+', '', s) for s in _tags] if i not in ('', 'nan')]
        return v

    def ts_as_str(self):
        # string
        return datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%dT%H:%M:%S')

    def ts_as_fn(self):
        # filename
        return datetime.fromtimestamp(self.timestamp).strftime('%Y%m%dT%H%M%S')

    def ts_as_date(self):
        # datetime str
        return datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %A')

    def ts_as_datetime(self):
        # datetime object
        s = datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d')
        return datetime.strptime(s, "%Y-%m-%d")

    def ts_as_time(self):
        # hour:min:sec str
        return datetime.fromtimestamp(self.timestamp).strftime('%H:%M:%S')

    def ion_as_str(self):
        if self.ion_name == '':
            return ""
        return f"{self.ion_mass}{self.ion_name}{self.ion_number}(+{self.ion_charge})"

    def tags_as_str(self):
        return ",".join(self.tags)

    def get_default_data_path(self, working_directory=None, data_type=None):
        """Return full data path for saving by naming convention,
        the data directory by default is ., e.g. ./40Ar+9_20200929T104317.csv.
        """
        if working_directory is None:
            wdir = '.'
        else:
            wdir = os.path.expanduser(working_directory)
        ftype = DEFAULT_DATA_FMT if data_type is None else data_type
        fn = f"{self.ion_mass}{self.ion_name}+{self.ion_charge}_{self.ts_as_fn()}.{ftype}"
        return os.path.abspath(os.path.join(wdir, fn))

    def update_name(self):
        """Update timestamp with current time, update name and datetime as well.
        """
        self.name, self.timestamp = get_sha1()

    def is_golden(self):
        return 'golden' in self.tags

    def __str__(self):
        # str(self.data)
        sio = io.StringIO()
        sio.write("\t".join(CSV_HEADER))
        sio.write("\n")
        for ename, fname, ftype, spos, sp, rd, old_sp, tol, writable in self.data:
            sio.write(
                f"{ename}\t{fname}\t{ftype}\t{spos}\t{sp}\t{rd}\t{old_sp}\t{tol}\t{writable}\n")
        text = sio.getvalue()
        sio.close()
        return text

    def __write_to_excel(self, filepath, **kws):
        # xlsx
        df_info = self.info.copy(deep=True)
        df_info['tags'] = self.tags_as_str()
        with pd.ExcelWriter(filepath) as fp:
            # df_info.drop(columns=['data_path']).T.to_excel(fp,
            #         sheet_name=SnapshotData.INFO_SHEET_NAME, header=False, **kws)
            df_info.T.to_excel(fp,
                    sheet_name=SnapshotData.INFO_SHEET_NAME, header=False, **kws)
            self.data.to_excel(fp, sheet_name=SnapshotData.SETTINGS_SHEET_NAME, index=False, **kws)
            if self.machstate is not None:
                self.machstate.to_excel(fp, sheet_name=SnapshotData.MACHSTATE_SHEET_NAME, **kws)

    def __write_to_hdf(self, filepath, **kws):
        # hdf
        df_info = self.info.copy(deep=True)
        df_info['tags'] = self.tags_as_str()
        complevel = kws.pop("complevel", 9)
        complib = kws.pop("complib", "blosc")
        format = kws.pop("format", "table")
        with pd.HDFStore(filepath, "w") as store:
            store.put(SnapshotData.SETTINGS_SHEET_NAME, self.data, index=False, format=format,
                      complevel=complevel, complib=complib, **kws)
            storer = store.get_storer(SnapshotData.SETTINGS_SHEET_NAME)
            attr_dict = []
            for k, v in df_info.items():
                #if k == 'data_path':
                #    continue
                attr_dict.append((k, v[0]))
            attr_dict = OrderedDict(attr_dict)
            storer.attrs.info = str(attr_dict)
            setattr(storer.attrs, SnapshotData.INFO_SHEET_NAME, attr_dict)
            if self.machstate is not None:
                store.put(SnapshotData.MACHSTATE_SHEET_NAME, self.machstate, format=format,
                        complevel=complevel, complib=complib, **kws)

    def __write_to_csv(self, filepath, **kws):
        # csv: only save info and data,
        # save machstate (if any) to another csv file, with filename-ms.csv as filepath.
        df_info = self.info.copy(deep=True)
        df_info['tags'] = self.tags_as_str()
        with open(filepath, "w") as fp:
            for k, v in df_info.items():
                fp.writelines(f"# {k}: {v[0]}\n")
            self.data.to_csv(fp, index=False)
        if self.machstate is not None:
            filename = os.path.basename(filepath).rsplit(".csv")[0] + "_ms.csv"
            _filepath = os.path.join(os.path.dirname(filepath), filename)
            self.machstate.to_csv(_filepath)

    def write(self, filepath, ftype='xlsx', **kws):
        """Write snapshot data into *filepath*.
        """
        self.__writer_map[ftype](filepath, **kws)

    @classmethod
    def read(cls, filepath, ftype='xlsx', **kws):
        # filepath: full path of data file
        # for ftype 'sql', filepath argument should be dataframe.
        if ftype not in cls._READER_MAP:
            print(f"Data source of type '{ftype}' is not supported.")
            return None
        df_data, df_info, df_machstate = cls._READER_MAP[ftype](filepath, **kws)
        o = cls(df_data, df_info)
        o.machstate = df_machstate
        if ftype == '_sql':
            o._blob = df_machstate
        if isinstance(filepath, (pathlib.Path, str)):
            o.data_path = str(filepath)
        return o

    @staticmethod
    def export_machine_state(machstate, filepath, ftype="xlsx", **kws):
        if machstate is None:
            return None
        if ftype == 'xlsx':
            machstate.to_excel(filepath, sheet_name=SnapshotData.MACHSTATE_SHEET_NAME, **kws)
        elif ftype == 'h5':
            machstate.to_hdf(filepath, SnapshotData.MACHSTATE_SHEET_NAME, format="table", **kws)
        elif ftype == 'csv':
            machstate.to_csv(filepath, **kws)
        return True

    def extract_blob(self):
        # update .data and .machstate with _blob if _blob is not None
        # only needed when work with DB
        if self._blob is None: # already extracted
            return
        _df_data, _df_info, _df_machstate = read_sql(self._blob)
        self.data = _df_data
        self.machstate = _df_machstate
        self._blob = None

    def to_blob(self):
        # output self to a binary blob, see alo write()
        s = io.BytesIO()
        self.write(s)
        return s.getvalue()

    #def __eq__(self, other):
    #    return all(self.info.drop(columns=["data_path"]) == other.info.drop(columns=["data_path"])) \
    #            and all(self.data == other.data)


def get_sha1():
    t0 = time.time()
    s = str(t0).encode('utf-8')
    return hashlib.sha1(s).hexdigest(), t0
