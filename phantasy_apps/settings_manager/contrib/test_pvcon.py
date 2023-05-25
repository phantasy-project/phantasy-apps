import epics
from epics import get_pv
from functools import partial
import time
from queue import Queue, Empty


class PVsAreReady(Exception):
    def __init__(self, *args, **kws):
        super().__init__(*args, **kws)


def establish_pvs(pvs: list, timeout: float = 1.0, **kws):
    """Establish the connections for a given list of PVs within the defined time in seconds.

    Parameters
    ----------
    pvs : list
        A list of PV names.
    timeout : float
        Maximum wait time in seconds allowed before return.

    Keyword Arguments
    -----------------
    verbose : bool
        If set, output log messages.

    Returns
    -------
    r : list
        A list of PVs that are not ready, otherwise None.
    """
    #
    enable_log = kws.get('verbose', False)
    if enable_log:
        t0 = time.perf_counter()
    q = Queue()
    n_pv = len(pvs)
    con_sts = [False] * n_pv
    def _f(i, pvname, conn, **kws):
        if conn:
            con_sts[i] = True
            if all(con_sts):
                q.put(True)

    for i, pv in enumerate(pvs):
        get_pv(pv, connection_callback=partial(_f, i))

    while True:
        try:
            v = q.get(timeout=timeout)
            if v: raise PVsAreReady
        except Empty:
            not_connected_pvs = [i for i in pvs if not epics.get_pv(i).connected]
            if enable_log:
                print(f"{len(not_connected_pvs)} PVs are not established in {(time.perf_counter() - t0) * 1e3:.1f} ms.")
            return not_connected_pvs
        except PVsAreReady:
            if enable_log:
                print(f"Established {n_pv} PVs in {(time.perf_counter() - t0) * 1e3:.1f} ms.")
            return None


if __name__ == '__main__':
    pvs = [
     'FE_ISRC1:BEAM:ELMT_BOOK',
     'FE_ISRC1:BEAM:A_BOOK',
     'FE_ISRC1:BEAM:Z_BOOK',
     'FE_ISRC1:BEAM:Q_BOOK',
     'ACC_OPS:BEAM:Q_STRIP',
     'FE_ISRC2:BEAM:ELMT_BOOK',
     'FE_ISRC2:BEAM:A_BOOK',
     'FE_ISRC2:BEAM:Z_BOOK',
     'FE_ISRC2:BEAM:Q_BOOK',
     #'MYPV',
     'ACS_DIAG:DEST:ACTIVE_ION_SOURCE',
     'ACS_DIAG:DEST:FSEE_LINE_RD',
     'ACS_DIAG:DEST:BEAMDEST_RD',
    ]
    # with open("pvlist.txt", "r") as fp:
    #     pvs = fp.read().split()
    # print(establish_pvs(pvs, timeout=1, verbose=True))
    # print([epics.get_pv(i).value for i in pvs])

    from phantasy import MachinePortal
    mp = MachinePortal("FRIB", "LINAC")
    lat = mp.work_lattice_conf

    pvs = []
    for i in lat:
        pvs.extend(i.pv())

    all_pvs = set(pvs)
    print(f"Total # of PVs: {len(all_pvs)}")
    r = establish_pvs(all_pvs, timeout=5, verbose=True)
    if r is not None:
        print("Non-connected PVs are:")
        for i in sorted(r):
            print(i)
