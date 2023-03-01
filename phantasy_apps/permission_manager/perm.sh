#!/bin/bash

#
# Keep folder permission matched as configured.
#
# Tong Zhang <zhangt@frib.msu.edu>
# 2023-02-28 17:06:54 EST
#

DIRPATH_CONF_FILE=/home/tong/pm_dirpath.txt

/bin/grep -v '^#' ${DIRPATH_CONF_FILE} | /bin/grep -v "^$" |
while read line; do
    dirpath=$(echo $line | awk -F';' '{print $1}')
    perm_s=$(echo $line | awk -F';' '{print $2}')
    _u=$(echo $perm_s | awk -F',' '{print $1}')
    _g=$(echo $perm_s | awk -F',' '{print $3}')
    _p=$(echo $perm_s | awk -F',' '{print $2}' | cut -c 3-)
    chgrp -R ${_g} ${dirpath}
    chmod -R ${_p} ${dirpath}
    find ${dirpath} -type f -a ! \( -name '*.sh' -o -name '*.py' \) -exec chmod -x {} \;
done
