# test take_snapshot function.
# WIP: for the CLI tool.
#
from phantasy import MachinePortal
from phantasy_apps.settings_manager.app import get_snapshotdata
from phantasy_apps.settings_manager.utils import take_snapshot
import time

mp = MachinePortal("FRIB", "LINAC")

t0 = time.perf_counter()
ts = '2023-05-08T14:54:59'
uri = "/user/zhangt/development/tests/test-sm.db"
snp_template_data = get_snapshotdata(ts, uri)
print(f"Time elapsed for reading a template: {time.perf_counter() - t0:.3f}s")

t0 = time.perf_counter()
snp = take_snapshot('snapshot got from CLI', ['TEST', 'CLI'],
                   snp_template_data, 'Artemis', inst_mp=True,
                   with_machstate=True, verbose=0)
print(f"Time elapsed for None mp: {time.perf_counter() - t0:.3f}s")

t0 = time.perf_counter()
snp1 = take_snapshot('test snapshot', ['TEST'],
                    snp_template_data, mp=mp, with_machstate=True,
                    verbose=0)
print(f"Time elapsed for mp: {time.perf_counter() - t0:.3f}s")

snp.write('/tmp/snp.csv', ftype='csv')
snp1.write('/tmp/snp1.csv', ftype='csv')
