# -*- coding: utf-8 -*-

"""User-defined operation to change the device(s) setting(s) before each DAQ.

Here are some rules:
1. The function name is 'f';
2. The first argument is the new setting for selected alter element;
3. Available keyword arguments are:
   - 'alter_elem': current selected element to change;
   - 'tolerance': absolute discrenpancy between set and read;
   - 'timeout': timeout in second for 'ensure put';
   - 'extra_wait': additional wait time in second after 'ensure put';
"""
import inspect
import time
from phantasy import ensure_put
from phantasy_ui import printlog


def default_alter_action(goal, **kws):
    # set alter element, apply ensure put
    alter_elem = kws.get('alter_elem', None)
    tolerance = kws.get('tolerance', 0.01)
    timeout = kws.get('timeout', 0.01)
    extra_wait = kws.get('extra_wait', 0.0)
    if alter_elem is None:
        return
    ensure_put(alter_elem, goal=goal, tol=tolerance, timeout=timeout)
    printlog("{} RD: {} SP: {}".format(alter_elem.ename, alter_elem.value, goal))

    # extra wait
    time.sleep(extra_wait)
    printlog("Additionally, waited for {} seconds.".format(extra_wait))


DEFAULT_ALTER_ACTION = default_alter_action
DEFAULT_ALTER_ACTION_CODE = inspect.getsource(DEFAULT_ALTER_ACTION)
