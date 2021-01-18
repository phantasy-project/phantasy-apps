#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test snapshot data structure.
"""

import os
import time
from getpass import getuser
import pytest

from phantasy_apps.settings_manager.data import read_data
from phantasy_apps.settings_manager.data import SnapshotData
from phantasy_apps.settings_manager.data import DEFAULT_MACHINE
from phantasy_apps.settings_manager.data import DEFAULT_SEGMENT


curdir = os.path.abspath(os.path.dirname(__file__))
datadir = os.path.join(curdir, 'data')
csv_fn_example1 = '40Ar+9_20200929T104317.csv'
data_fn_example1 = '40Ar+9_20200929T104317_data.csv'


@pytest.fixture
def get_snpdata_example1():
    """Return SnapshotData object from example1 csv data file.
    """
    filepath = os.path.join(datadir, csv_fn_example1)
    return read_data(filepath, data_type='csv')


@pytest.fixture
def get_data_example1():
    """Return a single string from the settings data of example1 csv data.
    """
    filepath = os.path.join(datadir, data_fn_example1)
    with open(filepath, 'r') as fp:
        all_str = '\n'.join(fp.read().split('\n')[1:]).strip()
    return all_str


def test_read_data1(get_snpdata_example1, get_data_example1):
    snp_data = get_snpdata_example1
    data_list_as_string = get_data_example1

    assert snp_data.timestamp == 1601390597.1267834
    assert snp_data.datetime ==  '2020-09-29T10:43:17'
    assert snp_data.name == 'dazzling_information'
    assert snp_data.note == 'LS1 95% correction'
    assert snp_data.user == 'tong'
    assert snp_data.ion_name == 'Ar'
    assert snp_data.ion_number == '18'
    assert snp_data.ion_mass == '36'
    assert snp_data.ion_charge == '9'
    assert snp_data.machine == 'FRIB_VA'
    assert snp_data.segment == 'LS1FS1'
    assert snp_data.tags == ['test1']
    assert snp_data.app == 'Settings Manager'
    assert snp_data.version == '5.2'
    assert data_list_to_string(snp_data.data) == data_list_as_string

    snp_data.tags = 'test1,test2'
    assert snp_data.tags == ['test1', 'test2']
    snp_data.tags = ' test1, test2, test 3 '
    assert snp_data.tags == ['test1', 'test2', 'test3']
    snp_data.tags = ' ,test1, test2, '
    assert snp_data.tags == ['test1', 'test2']
    snp_data.tags = ''
    assert snp_data.tags == []


def test_create_new_snapshot(get_snpdata_example1):
    snp_data = get_snpdata_example1
    data_list = snp_data.data
    t0 = time.time()
    new_snp_data = SnapshotData(data_list)
    assert new_snp_data.note == 'Input note ...'
    assert new_snp_data.user == getuser()
    assert new_snp_data.ion_name == ''
    assert new_snp_data.ion_number == ''
    assert new_snp_data.ion_mass == ''
    assert new_snp_data.ion_charge == ''
    assert new_snp_data.machine == DEFAULT_MACHINE
    assert new_snp_data.segment == DEFAULT_SEGMENT
    assert new_snp_data.tags == []
    assert new_snp_data.app == 'Settings Manager'
    assert new_snp_data.version == 'undefined'
    assert new_snp_data.timestamp - t0 < 1e-3


def data_list_to_string(data_list):
    return '\n'.join([','.join([str(j) for j in i]) for i in data_list])
