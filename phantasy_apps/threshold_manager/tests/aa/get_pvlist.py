from phantasy_apps.threshold_manager._model import get_pv

import sys
sys.exit()


nd_pv = list(get_pv('ND'))
ic_pv = list(get_pv('IC'))
hmr_pv = list(get_pv('HMR'))

assert len(nd_pv) == len(set(nd_pv))
assert len(ic_pv) == len(set(ic_pv))
assert len(hmr_pv) == len(set(hmr_pv))

with open("nd_pv.txt", "w") as fp:
    fp.write("\n".join(nd_pv))

with open("ic_pv.txt", "w") as fp:
    fp.write("\n".join(ic_pv))

with open("hmr_pv.txt", "w") as fp:
    fp.write("\n".join(hmr_pv))

all_pv = nd_pv + ic_pv + hmr_pv
with open("allpv.txt", "w") as fp:
    fp.write("\n".join(all_pv))

