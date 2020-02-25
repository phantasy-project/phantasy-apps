from PyQt5.QtWidgets import QApplication
from phantasy_apps.settings_manager.app import SettingsManagerWindow
from phantasy_apps.settings_manager import __version__
from phantasy_apps.settings_manager import init_config_dir
from phantasy_apps.settings_manager.data import TableSettings
from phantasy_apps.settings_manager.data import make_physics_settings
import csv
from phantasy import MachinePortal

almost_equal_tolerance = 0.001

### LEBT to MEBT
#machine = "FRIB"
#segments = ["LEBT"]
#csvfile = "/user/zhangt/test_phantasy/tests/sm-data/20200204/LEBT_MEBT.csv"
#snpfile = "/user/zhangt/test_phantasy/tests/save_and_restore_snapshots/36Ar10_2020Jan28_203531.snp"

### LS1 to FS1A
machine = "FRIB"
segments = ["MEBT_FS1A"]
csvfile = "/user/zhangt/test_phantasy/tests/sm-data/20200204/LEBT_FS1A.csv"
snpfile = "/user/zhangt/test_phantasy/tests/save_and_restore_snapshots/40Ar9_20190926_180238.snp"


###
mp = MachinePortal(machine)
for segm in segments:
    mp.load_lattice(segm)
lat = mp.combined_lattice()

config_dir = init_config_dir()

app = QApplication([])
w = SettingsManagerWindow(__version__, config_dir)
w._lat = lat

lat1 = w.build_lattice()
table_settings = TableSettings(csvfile)
s = make_physics_settings(table_settings, lat1)
lat1.settings.update(s)

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
    sp_val = row[4]
    elem = lat1[ename]
    for f in elem.get_eng_fields():
        sp_pv_list = elem.pv(field=f, handle='setpoint')
        if sp_pv_list == []:
            print("Cannot find {} [{}] from snp file.".format(ename, f))
            continue
        sp_pv = sp_pv_list[0]
        if sp_pv in settings:
            snp_sp = settings[sp_pv]
            if abs(snp_sp - sp_val) > almost_equal_tolerance:
                new_row = list(row[:])
                new_row[4] = snp_sp
                table_settings[i] = tuple(new_row)
                print("{0} [{1}] is updated from {2:.3f} to {3:.3f}".format(
                    ename, f, sp_val, snp_sp))

# save as a new csv file from the snp settings.
new_csvfilename = snpfile.rsplit('.', 1)[0] + '.csv'
table_settings.write(new_csvfilename)
