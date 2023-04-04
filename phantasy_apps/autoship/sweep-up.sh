#!/bin/bash

#
# Clean up folder paths that are not being auto-shipped.
#
#

DST=/files/shared/outbound-to-office-network/zhangt/FTC-AP
filelistpath=/files/shared/ap/HLA/autoShip/ah_filelist.txt

ls -l $DST | awk '{print $NF}' | sed 1d | sort > .list1.txt
/bin/grep -v "^#" $filelistpath | /bin/grep -v "^$" | awk -F',' '{print $1}' | awk -F'/' '{print $NF}' | sort > .list2.txt

# dirpath exist in .list1.txt but not .list2.txt
comm -23 .list1.txt .list2.txt | xargs -I {} rm -rf "$DST/{}"
rm .list1.txt .list2.txt
