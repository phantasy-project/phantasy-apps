# coding: utf-8

import xlrd
from phantasy import MachinePortal
from phantasy import disable_warnings
from phantasy_apps.settings_manager.contrib import SettingsRow

disable_warnings()

# parameters
machine = "FRIB_VA"
segments = ["MEBT", "LS1FS1"]

xlsx_filepath = "20190212_phase_scan_setting_list_maruta.xlsx"
sheet_name = "magnets"
row_start = 4
column_start = 4
settings_rootpath = "extracted_settings"

#
wkbk = xlrd.open_workbook(xlsx_filepath)
if sheet_name not in wkbk.sheet_names():
    raise RuntimeError("Cannot find sheet {} from given xlsx file.".format(sheet_name))

magnets_settings = wkbk.sheet_by_name(sheet_name)
head_row = magnets_settings.row(1)

mp = MachinePortal(machine, segments[0]);
for segm in segments[1:]:
    mp.load_lattice(segm);
lat = mp.combined_lattice()

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

list_settings_row = []
last_settings_row = None
for ridx in range(row_start - 1, magnets_settings.nrows):
    row = magnets_settings.row(ridx)
    current_settings_row = SettingsRow(row, index_elem_list, last_settings_row)
    last_settings_row = current_settings_row
    current_settings_row.write(rootpath=settings_rootpath, row_id=ridx + 1)
