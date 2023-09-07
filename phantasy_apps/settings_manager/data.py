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
from collections import namedtuple
from datetime import datetime
from getpass import getuser

from PyQt5.QtCore import Qt

from phantasy import Settings

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
    'Tolerance', 'Writable', 'Last Device State'
)

# For table_version of SnapshotData:
# CSV_HEADER: 9
# CSV_HEADER, LAST_DEVICE_STATUS: 10

# default attr keys of snapshotdata
ATTR_KEYS = [
    "timestamp", "datetime", "date", "note", "user",
    "ion_name", "ion_number", "ion_mass", "ion_charge",
    "machine", "segment", "tags", "app", "version", "data_format",
    "parent",
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
    r : tuple
        A tuple of ("Physics settings": Settings, "last device states" : dict),
        the keys of "last device states" are device names, and the states are strings,
        which should be correctly interpreted.
    """
    s = Settings()  # physics settings
    last_sts_dict = {}  # last device states dict
    for line in settings:
        name, field, _, _, sp, rd, last_sp, _, _, = line[0:9]
        try:
            last_sts = line[9]
        except IndexError:
            last_sts = "Non-existing"
        if name in ELEM_ALIAS_MAP:
            name = ELEM_ALIAS_MAP[name]
        elem = lat[name]
        if elem is None:
            s[name] = {field: sp}  # element is not existing any more
            continue
        last_sts_dict.setdefault(f"{name}-{field}", last_sts)
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
    return s, last_sts_dict


def get_settings_data(m, src_m):
    """Get settings data from *m* as a DataFrame.
    """
    # new_sp (x2): current sp to save
    # new_rd (x1): rb at sp
    # old_sp (x0): last_sp
    # new_sts (sts): current device state
    # WYIWYC?: proxy model, source model
    i_name, i_field, i_type, i_pos, i_new_sp, i_new_rd, i_old_sp, \
    i_tol, i_writable, i_sts = \
        src_m.i_name, src_m.i_field, src_m.i_type, src_m.i_pos, \
        src_m.i_cset, src_m.i_rd, src_m.i_val0, src_m.i_tol, src_m.i_writable, src_m.i_sts

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
        f_sts = m.data(m.index(irow, i_sts), Qt.ToolTipRole)
        data.append((ename, fname, ftype, spos,
                     f_new_sp, f_new_rd, f_old_sp,
                     f_tol, f_writable, f_sts))
    return pd.DataFrame(data, columns=CSV_HEADER_10)


def read_data(dataframe: pd.DataFrame):
    """Read settings data with attribute values from data source.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Data source to read as a SnapshotData

    Returns
    -------
    r : SnapshotData
    """
    try:
        r = SnapshotData.read(dataframe)
    except Exception as err:
        r = None
        print(f"Failed read_data(): {err}")
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
        _df_data = pd.read_excel(fp, sheet_name=SnapshotData.SETTINGS_SHEET_NAME)
        df_data = _df_data[~_df_data.Name.isna()]
        if SnapshotData.MACHSTATE_SHEET_NAME in fp.sheet_names:
            df_machstate = pd.read_excel(fp, sheet_name=SnapshotData.MACHSTATE_SHEET_NAME, index_col=[0, 1])
        else:
            df_machstate = None
    return df_data, _df.T, df_machstate


def read_sql(df):
    """Read a row of data into SnapshotData. The row of data is originated from a DataFrame
    from a sqlite database.
    """
    # extract blob: slow
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


def read_info(df):
    # return df_info part for SnapshotData, df <-- irow
    d = {'timestamp': df.timestamp, 'datetime': df.datetime, 'date': df.date,
         'note': df.note, 'user': df.user,
         'ion_name': df.ion_name, 'ion_number': df.ion_number,
         'ion_mass': df.ion_mass, 'ion_charge': df.ion_charge,
         'machine': df.machine, 'segment': df.segment,
         'app': df.app, 'version': df.version, 'tags': df.tags,
         'data_format': df.data_format, 'parent': df.parent}
    r = pd.DataFrame.from_dict(d, orient='index')
    r.rename(columns={0: 'attribute'}, inplace=True)
    return r.T


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
        'sql': read_sql, # extracted
        'info': read_info, # unextracted
    }
    def __init__(self, df_data, df_info=None, **kws):
        self.__writer_map = {
             'xlsx': self.__write_to_excel,
             'hdf': self.__write_to_hdf,
             'h5': self.__write_to_hdf,
             'csv': self.__write_to_csv,
        }
        #
        self.data = df_data
        self.info = df_info
        #
        # update the info table
        # (for creating new instance of SnapshotData)
        if kws:
            self.update_info(**kws)
        #
        # machine state data
        self.machstate = None
        # placeholder for df row (database)
        self._blob = None

    @property
    def machstate(self):
        return self._machstate

    @machstate.setter
    def machstate(self, df):
        """Set machine state with a dataframe.
        """
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

    def __getattr__(self, k: str):
        if k == 'tags':
            return SnapshotData.str2tags(self._df_info.loc['attribute'][k])
        if k in self._df_info:
            return self._df_info.loc['attribute'][k]
        if k == 'name': # snapshot name (unique)
            return self.ts_as_str()
        raise AttributeError(f"Invalid attribute '{k}'")

    def update_info(self, **kws):
        """Update info table with keyword arguments.
        """
        # timestamp
        ts = kws.pop("timestamp", time.time())
        self._df_info.loc["attribute"]["timestamp"] = ts
        self._df_info.loc["attribute"]["datetime"] = \
            datetime.fromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%S")
        self._df_info.loc["attribute"]["date"] = \
            datetime.fromtimestamp(ts).strftime("%Y-%m-%d %A")
        # user
        user = kws.pop("user", getuser())
        self._df_info.loc["attribute"]["user"] = user
        # app name
        app_name = kws.pop("app", "Settings Manager")
        self._df_info.loc["attribute"]["app"] = app_name
        # blob data format
        data_fmt = kws.pop("data_format", "xlsx")
        self._df_info.loc["attribute"]["data_format"] = data_fmt

        #
        for k, v in kws.items():
            self._df_info.loc['attribute'][k] = v

    def __dir__(self):
        return dir(__class__) + list(self.__dict__.keys()) \
                + self._df_info.keys().tolist()

    @staticmethod
    def str2tags(s: str):
        # get a list of sorted unique tags from input *s* (str).
        if s is None:
            tag_list = []
        else:
            s = s.strip(",; ")
            if s == "":
                tag_list = []
            else:
                # input: str separated by ',', ';', or white spaces, delete whitespace if any
                # ignore empty str '', e.g. ',,'.
                _tags = set(re.split(r"[,;\s+]", s))
                tag_list = [i.upper() for i in _tags]
        return sorted(tag_list)

    def ts_as_str(self):
        # datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%dT%H:%M:%S')
        return self.datetime

    def ts_as_fn(self):
        # filename: e.g. 20230823T093700
        return datetime.fromtimestamp(self.timestamp).strftime('%Y%m%dT%H%M%S')

    def ts_as_date(self):
        # datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %A')
        return self.date

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
        return f"{self.ion_mass}{self.ion_name}{self.ion_number}({self.ion_charge}+)"

    def tags_as_str(self):
        return ",".join(self.tags)

    def is_golden(self):
        return 'GOLDEN' in self.tags

    def archive(self):
        """Add 'ARCHIVE' into the tag list.
        """
        self.append_tag('ARCHIVE')

    def append_tag(self, tag: str):
        """Add a new tag to the tag list.
        """
        tag_list = self.tags
        _tag = tag.upper()
        if _tag not in tag_list:
            tag_list.append(_tag)
            self._df_info.loc['attribute']['tags'] = ','.join(tag_list)
        else:
            print(f"{_tag} exists, skip adding.")

    def set_timestamp(self, ts: float = None):
        """Update timestamp, along with datetime, date.
        """
        if ts is None:
            ts = time.time()
        self._df_info.loc["attribute"]["timestamp"] = ts
        self._df_info.loc["attribute"]["datetime"] = \
            datetime.fromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%S")
        self._df_info.loc["attribute"]["date"] = \
            datetime.fromtimestamp(ts).strftime("%Y-%m-%d %A")

#    def __str__(self):
#        # str(self.data)
#        sio = io.StringIO()
#        sio.write("\t".join(CSV_HEADER))
#        sio.write("\n")
#        for ename, fname, ftype, spos, sp, rd, old_sp, tol, writable in self.data:
#            sio.write(
#                f"{ename}\t{fname}\t{ftype}\t{spos}\t{sp}\t{rd}\t{old_sp}\t{tol}\t{writable}\n")
#        text = sio.getvalue()
#        sio.close()
#        return text

    def __write_to_excel(self, filepath, **kws):
        # xlsx
        df_info = self.info.copy(deep=True)
        df_info['tags'] = self.tags_as_str()

        parent_node = self.get_parent_node()
        if parent_node is not None:
            df_info['parent'] = parent_node

        with pd.ExcelWriter(filepath) as fp:
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
    def read(cls, df: pd.DataFrame, **kws):
        # read as a SnasphotData with info sheet only (metadata),
        # with _blob unextracted.
        df_info = cls._READER_MAP['info'](df, **kws)
        o = cls(None, df_info)
        o._blob = df
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

    def get_parent_node(self):
        """Return the parent node if available."""
        if 'parent' in self.info:
            return self.info['parent'].item()
        return None

    def extract_blob(self):
        # update .data and .machstate with _blob if _blob is not None
        # .info is managed in read_info()
        if self._blob is None: # already extracted
            return
        _df_data, _, _df_machstate = read_sql(self._blob)
        self.data = _df_data
        self.machstate = _df_machstate
        self._blob = None

    def clone(self):
        """Return a deepcopy.
        """
        _info = self.info.copy(deep=True)
        _info.loc['attribute']['parent'] = self.ts_as_str() # pass the datetime string as parent node
        _cp = SnapshotData(self.data.copy(deep=True), _info)
        if self.machstate is not None:
            _cp.machstate = self.machstate.copy(deep=True)
        return _cp

    def to_blob(self):
        # output self to a binary blob, see alo write()
        s = io.BytesIO()
        self.write(s)
        return s.getvalue()


AttachmentData = namedtuple('AttachmentData', ['name', 'uri', 'ftyp'])

class AttachmentData:

    _ATTR_MAP = {'name': 0, 'uri': 1, 'ftyp': 2, 'created': 3}

    def __init__(self, name, uri, ftyp, created):
        self._data = [name, uri, ftyp, created]
        self.created = created

    def __getitem__(self, index):
       if isinstance(index, str):
           return self._data[AttachmentData._ATTR_MAP[index]]
       else:
           return self._data[index]

    def __setitem__(self, index, value):
        if isinstance(index, str):
            self._data[AttachmentData._ATTR_MAP[index]] = value
        else:
            self._data[index] = value

    @property
    def name(self):
        return self._data[0]

    @name.setter
    def name(self, s):
        self._data[0] = s

    @property
    def uri(self):
        return self._data[1]

    @uri.setter
    def uri(self, s):
        self._data[1] = s

    @property
    def ftyp(self):
        return self._data[2]

    @ftyp.setter
    def ftyp(self, s):
        self._data[2] = s

    @property
    def created(self):
        return self._data[3]

    @created.setter
    def created(self, s):
        # with the format of "2023-09-07 16:09:43"
        if s is None:
            self._data[3] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self._data[3] = s

    def __repr__(self):
        return f"AttachmentData('{self.name}', '{self.uri}', '{self.ftyp}', '{self.created}')"
