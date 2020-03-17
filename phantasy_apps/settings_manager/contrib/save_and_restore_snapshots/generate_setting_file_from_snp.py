# -*- coding: utf-8 -*-
"""Extract settings from SNP file, generate a new CSV file for app 'Settings Manager',

Tong Zhang <zhangt@frib.msu.edu>
2020-02-24 17:21:25 PM EST
"""

from PyQt5.QtWidgets import QApplication
from phantasy_apps.settings_manager.app import SettingsManagerWindow
from phantasy_apps.settings_manager import __version__
from phantasy_apps.settings_manager.utils import init_config_dir
from phantasy_apps.settings_manager.data import TableSettings
from phantasy_apps.settings_manager.data import make_physics_settings
import csv
from phantasy import MachinePortal
import re

almost_equal_tolerance = 0.001

type_map = {'PSQ': 'Q', 'PSC2': 'DCH', 'PSC1': 'DCV', 'PSD': 'DH',
            'PSOL': 'SOLR'}

### LEBT to MEBT
machine = "FRIB"
segments = ["LEBT", "MEBT"]
csvfile = "/user/zhangt/test_phantasy/tests/save_and_restore_snapshots/LEBT_MEBT_template.csv"
snpfile = "/user/zhangt/test_phantasy/tests/save_and_restore_snapshots/36Ar10_2020Jan28_203531.snp"

### LS1 to FS1A
#machine = "FRIB"
#segments = ["LEBT", "MEBT_FS1A"]
#csvfile = "/user/zhangt/test_phantasy/tests/sm-data/20200204/LEBT_FS1A.csv"
#snpfile = "/user/zhangt/test_phantasy/tests/save_and_restore_snapshots/40Ar9_20190926_180238.snp"

### LEBT to FS1A
machine = "FRIB"
segments = ["LEBT", "MEBT_FS1A"]
csvfile = "/user/zhangt/test_phantasy/tests/save_and_restore_snapshots/LEBT_FS1A_template.csv"
snpfile = "/user/zhangt/test_phantasy/tests/save_and_restore_snapshots/40Ar9_50euA_20190215.snp"


new_csvfilename = snpfile.rsplit('.', 1)[0] + '.csv'

###
mp = MachinePortal(machine)
for segm in segments:
    mp.load_lattice(segm)
lat = mp.combined_lattice()

config_dir = "~/.phantasy-apps/settings-manager"

app = QApplication([])
w = SettingsManagerWindow(__version__, config_dir)

lat1 = w.build_lattice() + lat
table_settings = TableSettings(csvfile)
#s = make_physics_settings(table_settings, lat1)
#lat1.settings.update(s)

###
settings = {}
with open(snpfile, "r") as f:
    ss = csv.reader(f, delimiter=",", skipinitialspace=True)
    ts = next(ss)
    header = next(ss)
    sp_pv_idx = header.index('PV')
    rd_pv_idx = header.index('READBACK')
    sp_val_idx = header.index('VALUE')
    rd_val_idx = header.index('READBACK_VALUE')
    tol_idx = header.index('DELTA')
#     print('SP PV: {sp_pv_idx}, RD PV: {rd_pv_idx}, SP VAL: {sp_val_idx}, RD VAL: {rd_val_idx}, TOL: {tol_idx}'.format(
#        sp_pv_idx=sp_pv_idx, rd_pv_idx=rd_pv_idx,
#        sp_val_idx=sp_val_idx, rd_val_idx=rd_val_idx,
#        tol_idx=tol_idx))
    for line in ss:
        if line == []:
            break
        settings.update({line[sp_pv_idx]: float(line[sp_val_idx])})

#
for i, row in enumerate(table_settings):
    ename = row[0]
    fname = row[1]
    sp_val = row[4]
    elem = lat1[ename]

    if elem is None:
        print("{} is not found from lattice.".format(ename))
        continue

    sp_pv = elem.pv(field=fname, handle='setpoint')[0]

    try:
        if sp_pv in settings:
            snp_sp = settings[sp_pv]
        else:
            r = re.match("(.*):(.*)_D(.*):(.*)", sp_pv)
            map_sp_pv = "{}:{}_D{}:{}".format(
                r.group(1), type_map.get(r.group(2), r.group(2)), r.group(3), r.group(4))
            if map_sp_pv not in settings:
                if elem.family in ('QUAD', 'EQUAD'):
                    map_sp_pv = "{}:QE_D{}:{}".format(r.group(1), r.group(3), r.group(4))
                elif elem.family in ('EBEND',):
                    map_sp_pv = "{}:{}".format(elem.name, r.group(4))
            snp_sp = settings[map_sp_pv]
    except:
        print("Cannot find {} [{}] from snp file.".format(ename, fname))
        continue

    if abs(snp_sp - sp_val) > almost_equal_tolerance:
        new_row = list(row[:])
        new_row[4] = snp_sp
        table_settings[i] = tuple(new_row)
        print("{0} [{1}] is updated from {2:.3f} to {3:.3f}".format(
            ename, fname, sp_val, snp_sp))

# save as a new csv file from the snp settings.
table_settings.write(new_csvfilename)
