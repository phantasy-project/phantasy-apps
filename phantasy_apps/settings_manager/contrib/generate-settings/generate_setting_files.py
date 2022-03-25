#!/usr/bin/env python
# coding: utf-8

#
# ### Extract device settings as CSV files for `Settings Manager` from an XLSX file prepared for the beam envelope controling during the cavity phase scan tuning.
# Run in FTC.

import xlrd
from getpass import getuser
from phantasy import MachinePortal
from phantasy import disable_warnings
from phantasy_apps.settings_manager.contrib import SettingsRow

disable_warnings()
ion_info_idx = False

# input parameters for beam study (ARR07) (2022-01-17)
machine = "ARIS"
segments = ["ARIS"]

xlsx_filepath = "ARR07_settings.xlsx"  # file path of the xlsx file
sheet_name = "ARR07"  # sheet name of the data
row_start = 3  # the row number (counts from 1) where the settings data begins, put one settings each row after
column_start = 10  # the column number (counts from 1) where the device settings data begins
settings_rootpath = "ARR07_20220119-1"  # the directory name to put the generated snapshot files, each row will be generated as one file

snp_tags = "GENERATED,ARIS,ARR07"  # Tag the generated file,the cell values in Tag columns are not used
snp_machine = "ARIS"  # the machine to load
snp_segment = "ARIS"  # the segment to load
snp_ion_name = 4  # column id, indicated in row 2, will be used as ion name
snp_ion_mass = 6  # column id, indicated in row 2, will be used as ion mass
snp_ion_charge = 7  # column id, indicated in row 2, will be used as ion charge
snp_ion_number = 5  # column id, indicated in row 2, will be used as ion number
snp_note = 8  # column id, indicated in row 2 will be used as the note string
ion_info_idx = True  # always set True
snp_user = getuser()  # user name
snp_app_name = "Settings Manager"
snp_app_version = "9.7"

# ### Generate snapshot files

# In[4]:

wkbk = xlrd.open_workbook(xlsx_filepath)
if sheet_name not in wkbk.sheet_names():
    raise RuntimeError(
        "Cannot find sheet {} from given xlsx file.".format(sheet_name))
magnets_settings = wkbk.sheet_by_name(sheet_name)
head_row = magnets_settings.row(1)
head_row

# In[5]:

mp = MachinePortal(machine, segments[0])
for segm in segments[1:]:
    mp.load_lattice(segm)
lat = mp.combined_lattice()
lat

# In[6]:

# get a list of column index of element name and element object.
# [(cell index, CaElement)]
index_elem_list = []
col_idx0 = column_start - 1
for i, cell in enumerate(head_row[col_idx0:], col_idx0):
    if cell.value == 'STOP':
        break
    elem = lat.get_elements(name="*{}*".format(cell.value))
    if elem:
        index_elem_list.append((i, elem[0]))

# In[7]:

import time
list_settings_row = []
last_settings_row = None
for ridx in range(row_start - 1, magnets_settings.nrows):
    row = magnets_settings.row(ridx)
    current_settings_row = SettingsRow(
        row,
        index_elem_list,
        last_settings_row,
        ion_name=snp_ion_name,
        ion_number=snp_ion_number,
        ion_mass=snp_ion_mass,
        ion_charge=snp_ion_charge,
        note=snp_note,
        machine=snp_machine,
        segment=snp_segment,
        tags=snp_tags,
        app=snp_app_name,
        version=snp_app_version,
        user=snp_user,
        ion_info_idx=ion_info_idx,
    )
    if not current_settings_row == last_settings_row:
        current_settings_row.write(rootpath=settings_rootpath, row_id=ridx + 1)
    last_settings_row = current_settings_row
    time.sleep(1)

# In[ ]:
