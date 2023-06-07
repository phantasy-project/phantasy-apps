#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import pandas as pd
from datetime import datetime
from collections import OrderedDict

# default attr keys of snapshotdata
ATTR_KEYS = [
    "timestamp",
    "user",
    "ion_name",
    "ion_number",
    "ion_mass",
    "ion_charge",
    "ion_charge_state",
    "beam_power",
    "beam_energy",
    "beam_destination",
    "tags",
    "note",
]

ATTR_DICT = OrderedDict([(k, None) for k in ATTR_KEYS])

ISRC_INDEX_MAP = {
    'Live': 'live',
    'Artemis': 'ISRC1',
    'HP-ECR': 'ISRC2',
}


class SnapshotData:
    """Table node for snapshot data
    """

    def __init__(self, row_data: list):
        # row_data is a list of data for:
        # * timestamp: float
        # * user: str
        # * ion_name: str
        # * ion_number: int
        # * ion_mass: int
        # * ion_charge: int
        # * ion_charge1: int
        # * beam_power: float
        # * beam_energy: float
        # * beam_dest: str
        # * tags: str (sep ',')
        # * note: str
        # * data_dict: {device_type: dataframe (threshold data table)}
        self._row_data = row_data
        self.ts, self.user, self.ion_name, self.ion_num, self.ion_mass, self.ion_charge, \
          self.ion_charge1, self.beam_power, self.beam_energy, self.beam_dest, self.tags, \
          self.note, self.data_dict = row_data

        #
        self.__writer_map = {
            'xlsx': self.__write_to_excel,
        }
        #
        self.df_info = pd.DataFrame.from_dict(ATTR_DICT,
                                              orient='index',
                                              columns=['attribute']).T
        for k, v in zip(ATTR_KEYS, row_data):
            self.df_info.loc['attribute', k] = v

    def ts_as_str(self):
        """Return a string from timestamp.
        """
        return datetime.fromtimestamp(self.ts).strftime("%Y-%m-%dT%H:%M:%S")

    def get_column_data(self, i: int):
        if i == 0:  # timestamp as datetime string
            return self.ts_as_str()
        else:
            return self._row_data[i]

    def write(self, filepath, ftype='xlsx', **kws):
        """Write snapshot data into *filepath*.
        """
        self.__writer_map[ftype](filepath, **kws)

    def __write_to_excel(self, filepath, **kws):
        # xlsx
        df_info = self.df_info.copy(deep=True)
        with pd.ExcelWriter(filepath) as fp:
            df_info.T.to_excel(fp, sheet_name='info', header=False, **kws)
            for dtype, data in self.data_dict.items():
                data.to_excel(fp, sheet_name=dtype, index=False, **kws)

    def to_blob(self):
        # output self to a binary blob, see also write()
        s = io.BytesIO()
        self.write(s)
        return s.getvalue()

    @staticmethod
    def read_blob(dat: bytes):
        """Read the given bytes blob to a dict of dataframes.
        """
        return pd.read_excel(dat, sheet_name=None)

    def __repr__(self):
        return f"MPS {self.__class__.__name__}: [{self.ts_as_str()}] {self.ion_mass}{self.ion_name}{self.ion_charge}({self.ion_charge1})+"
