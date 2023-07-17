#!/usr/bin/bash

#
# Fetch archived data for accumulated dose calculation.
#
pyarchappl-get --pv-file pvlist.txt -vv \
    --from 2023-04-27T00:00:00.00-04:00 \
    --to 2023-07-10T00:00:00.00-04:00 \
    --output data_1S.csv --resample 1S
