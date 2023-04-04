#!/bin/bash

#
# Manage the path list for AutoShip
#
# Tong Zhang <zhangt@frib.msu.edu>
# 2023-04-04 13:34:26 EDT
#
# The FTC app config is at: /files/shared/ap/HLA/autoShip/ah-config.toml
# ah_filelist.txt keeps track of the folder paths for AutoShip.
#

# DIRPATH_CONF_FILE=/files/shared/ap/HLA/autoShip/ah_filelist.txt
DIRPATH_CONF_FILE=/home/tong/test/ah_filelist.txt

# DST=/files/shared/outbound-to-office-network/zhangt/FTC-AP
DST=/tmp/autoship-test

LOG_DIR=$(dirname ${DIRPATH_CONF_FILE})/.ah-logs
[[ ! -e ${LOG_DIR} ]] && mkdir -p ${LOG_DIR}
rootlog="${LOG_DIR}/autoship.log"

/bin/grep -v '^#' ${DIRPATH_CONF_FILE} | /bin/grep -v "^$" |
while read line; do
    _dirpath_remote=$(echo $line | awk -F';' '{print $1}')
    dirpath=$(echo ${_dirpath_remote} | awk -F',' '{print $1}')
    pathtype=$(echo ${_dirpath_remote} | awk -F',' '{print $2}') # '' or 'not-empty-string'

    if [[ $pathtype == "" ]]; then
        exec_cmd="cp"
    else
        exec_cmd="scp"
        dirpath="zhangt@phyapps-ioc:"$dirpath
    fi

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
        _tmin=$(echo $line | awk -F';' '{print $2}')
        ${exec_cmd} -r $dirpath $DST/
        echo "$(date +%Y-%m-%dT%H:%M:%S)" > ${logfile2}
        echo "[$(date +'%Y-%m-%dT%H:%M:%S %Z')] [$$] Proceeding with ${dirpath} ... done" | tee -a ${rootlog}
        echo "waiting" > ${logfile1}
        if [[ _tmin -gt 0 ]]; then
            echo "[$(date +'%Y-%m-%dT%H:%M:%S %Z')] [$$] Waiting ${_tmin} mins before next run for ${dirpath} ..." | tee -a ${rootlog}
            sleep ${_tmin}m
            echo "[$(date +'%Y-%m-%dT%H:%M:%S %Z')] [$$] Waiting ${_tmin} mins before next run for ${dirpath} ... done" | tee -a ${rootlog}
        fi
        echo "idle" > ${logfile1}
    fi
done
