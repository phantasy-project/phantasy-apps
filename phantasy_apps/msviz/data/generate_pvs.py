#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from phantasy import MachinePortal

mach, segm = "FRIB_VA", "LS1FS1"
mach, segm = "FRIB", "LINAC"

mp = MachinePortal(mach, segm)

# generate BPM PVs for X, Y, PHA, ENG

bpms = mp.get_elements(type='BPM')

pv_list_x = []
pv_list_y = []
pv_list_pha = []
pv_list_eng = []
for i in bpms:
    pv_list_x.append(i.pv(field='X')[0])
    pv_list_y.append(i.pv(field='Y')[0])
    pv_list_pha.append(i.pv(field='PHA')[0])
    # VA only
    # pv_list_eng.append(i.pv(field='ENG')[0])
    pv_list_eng.append(i.pv(field='MAG')[0])


for i in pv_list_x:
    print(f"'{i}',")

for i in pv_list_y:
    print(f"'{i}',")

for i in pv_list_pha:
    print(f"'{i}',")

for i in pv_list_eng:
    print(f"'{i}',")
