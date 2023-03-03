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
# DIRPATH_CONF_FILE=/home/tong/test/pm_dirpath.txt

LOG_DIR=$(dirname ${DIRPATH_CONF_FILE})/.pm-logs
[[ ! -e ${LOG_DIR} ]] && mkdir -p ${LOG_DIR}
rootlog="${LOG_DIR}/perm.log"

/bin/grep -v '^#' ${DIRPATH_CONF_FILE} | /bin/grep -v "^$" |
while read line; do
    dirpath=$(echo $line | awk -F';' '{print $1}')
    dirpath_=$(echo ${dirpath} | tr "/" "_")
    # is running: idle, running, waiting
    logfile1="${LOG_DIR}/${dirpath_}_1.log"
    # last updated
    logfile2="${LOG_DIR}/${dirpath_}_2.log"

    [[ ! -f "${logfile1}" ]] && echo "idle" > ${logfile1}
    [[ ! -f "${logfile2}" ]] && echo "" > ${logfile2}

    if [[ $(cat ${logfile1}) = "idle" ]]; then
        #
        echo "[$(date +'%Y-%m-%dT%H:%M:%S %Z')] [$$] Proceeding with ${dirpath} ..." | tee -a ${rootlog}
        #
        echo "running" > ${logfile1}
        perm_s=$(echo $line | awk -F';' '{print $2}')
        _u=$(echo $perm_s | awk -F',' '{print $1}')
        _g=$(echo $perm_s | awk -F',' '{print $3}')
        _p=$(echo $perm_s | awk -F',' '{print $2}' | cut -c 3-)
        _tmin=$(echo $line | awk -F';' '{print $3}')
        chgrp -R ${_g} ${dirpath}
        chmod -R ${_p} ${dirpath}
        find ${dirpath} -type f -a ! \( -name '*.sh' -o -name '*.py' \) -exec chmod -x {} \;
        echo "$(date +%Y-%m-%dT%H:%M:%S)" > ${logfile2}
        echo "[$(date +'%Y-%m-%dT%H:%M:%S %Z')] [$$] Proceeding with ${dirpath} ... done" | tee -a ${rootlog}
        echo "waiting" > ${logfile1}
        if [[ _tmin -gt 0 ]]; then
            echo "[$(date +'%Y-%m-%dT%H:%M:%S %Z')] [$$] Waiting before next run for ${dirpath} ..." | tee -a ${rootlog}
            sleep ${_tmin}m
            echo "[$(date +'%Y-%m-%dT%H:%M:%S %Z')] [$$] Waiting before next run for ${dirpath} ... done" | tee -a ${rootlog}
        fi
        echo "idle" > ${logfile1}
    fi
done
