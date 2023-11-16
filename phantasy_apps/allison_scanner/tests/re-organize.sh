#!/bin/bash

#
# Re-organize the Allison scanner data files.
#

# recursively search allison*.json files.
ORIG_DIR=${1:-/files/shared/ap/beam_study}

# new place for renamed .json files.
NEW_DIR="/files/shared/phyapps-operations/data/allison_scanner"

_process() {
  orig_filepath="$1"
  # get the original timestamp when created
  orig_ts=$(date -d @$(stat -c %Y ${orig_filepath}) +%Y%m%dT%H%M%S)
  # get the ion source id string
  [[ -z $(grep '_id' ${orig_filepath}) ]] && _isrc_id="ISRC1" || \
    _isrc_id=$(grep '_id' ${orig_filepath} | awk -F':' '{print $NF}' | cut -c3-7)
  # X or Y?
  xoy=$(grep 'xoy' ${orig_filepath} | awk -F':' '{print $2}' | cut -c3 | tr 'a-z' 'A-Z')
  # new filepath
  new_filepath="${NEW_DIR}/${_isrc_id}/${orig_ts}_${xoy}.json"
  suffix_i=1
  while [ -e ${new_filepath} ]; do
    new_filepath=${new_filepath%%.*}.${suffix_i}.json
    suffix_i=$((suffix_i+1))
  done
  #
  echo ${orig_filepath} "->" ${new_filepath}
  [ ! -e $(dirname ${new_filepath}) ] && mkdir -p $(dirname ${new_filepath})
  cp -av ${orig_filepath} ${new_filepath}
  # insert original filepath to the note field
  sed -i "s|\(.*note.*\): \"\(.*\)\"|\1: \"\2 ${orig_filepath}\"|" ${new_filepath}
  # chmod 644
  chmod 644 ${new_filepath}
}

find ${ORIG_DIR} -iname 'allison*.json' | while read -r fn; do
    _process ${fn}
done

