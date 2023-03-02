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

LOG_DIR=$(dirname ${DIRPATH_CONF_FILE})/.pm-logs
[[ ! -e ${LOG_DIR} ]] && mkdir -p ${LOG_DIR}
rootlog="${LOG_DIR}/perm.log"

/bin/grep -v '^#' ${DIRPATH_CONF_FILE} | /bin/grep -v "^$" |
while read line; do
    dirpath=$(echo $line | awk -F';' '{print $1}')
    dirpath_=$(echo ${dirpath} | tr "/" "_")
    # if logfile is Refreshing..., continue
    logfile="${LOG_DIR}/${dirpath_}.log"

    [[ ! -f "${logfile}" ]] && echo "Initialized at $(date +%Y-%m-%dT%H:%M:%S_%Z)" > ${logfile}

    if [[ $(cat ${logfile}) != "Refreshing..." ]]; then
	#
	echo "[$(date +'%Y-%m-%dT%H:%M:%S %Z')] [$$] Proceeding with ${dirpath} ..." | tee -a ${rootlog}
	#
	echo "Refreshing..." > ${logfile}
        perm_s=$(echo $line | awk -F';' '{print $2}')
        _u=$(echo $perm_s | awk -F',' '{print $1}')
        _g=$(echo $perm_s | awk -F',' '{print $3}')
        _p=$(echo $perm_s | awk -F',' '{print $2}' | cut -c 3-)
        chgrp -R ${_g} ${dirpath}
        chmod -R ${_p} ${dirpath}
        find ${dirpath} -type f -a ! \( -name '*.sh' -o -name '*.py' \) -exec chmod -x {} \;
	echo "Refreshed at $(date +%Y-%m-%dT%H:%M:%S_%Z)" > ${logfile}
    fi
done
