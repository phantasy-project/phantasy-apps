#!/bin/bash

#
# Keep folder permission matched as configured.
#
# Tong Zhang <zhangt@frib.msu.edu>
# 2023-02-28 17:06:54 EST
#
# The FTC app config is at: /files/shared/ap/HLA/permMgmt/pm-config.toml
# pm_dirpath.txt keeps track of the folder paths for permission management.
#

DIRPATH_CONF_FILE=/files/shared/ap/HLA/permMgmt/pm_dirpath.txt
# DIRPATH_CONF_FILE=/home/tong/pm_dirpath.txt
LOG_DIR=${DIRPATH_CONF_FILE}/../.pm-logs

[[ ! -e ${LOG_DIR} ]] && mkdir -p ${LOG_DIR}

/bin/grep -v '^#' ${DIRPATH_CONF_FILE} | /bin/grep -v "^$" |
while read line; do
    dirpath=$(echo $line | awk -F';' '{print $1}')
    is_updated_log=${LOG_DIR}/${dirpath}.log
    [[ -f ${is_updated_log} ]] && echo "" > ${is_updated_log}
    if [[ $(cat ${is_updated_log}) = "" ]]; then
        perm_s=$(echo $line | awk -F';' '{print $2}')
        _u=$(echo $perm_s | awk -F',' '{print $1}')
        _g=$(echo $perm_s | awk -F',' '{print $3}')
        _p=$(echo $perm_s | awk -F',' '{print $2}' | cut -c 3-)
        chgrp -R ${_g} ${dirpath}
        chmod -R ${_p} ${dirpath}
        find ${dirpath} -type f -a ! \( -name '*.sh' -o -name '*.py' \) -exec chmod -x {} \;
        echo "${dirpath} is refreshed at $(date)" > ${is_updated_log}
    fi
done
