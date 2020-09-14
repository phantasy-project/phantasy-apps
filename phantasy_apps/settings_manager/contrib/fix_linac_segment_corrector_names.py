#!/usr/bin/python3

"""This script is to fix the names of LS(1,2) correctors, after the changes that
were made in phantasy-machines (commit: 39c94e5)
e.g. LS1_CA01:DCH_D1132 --> LS1_CA01:DCH1_D1132

Tong Zhang
2020-09-14 15:40
"""
import sys

csvfile = sys.argv[1]
outfile = sys.argv[2]

from phantasy import MachinePortal
mp = MachinePortal("FRIB", "LINAC")

fin = open(csvfile, 'r')
fout = open(outfile, 'w')

for line in fin:
    if line.startswith('#'):
        fout.write(line)
    else:
        name, leftover = line.split(',', 1)
        if 'DCH' in name or 'DCV' in name:
            a, b = name.rsplit('_', 1)
            elem = mp.get_elements(name=a + '*_' + b)[0]
            name1 = elem.name
            line = ','.join((name1, leftover))
        fout.write(line)

fin.close()
fout.close()

import os
os.utime(outfile, (os.path.getmtime(csvfile), os.path.getmtime(csvfile)))
