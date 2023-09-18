#!/usr/bin/bash

#
# Fetch archived data for accumulated dose calculation.
#
#
# 2023-07-11T19:37:00.00-04:00 
# 2023-07-11T20:05:00.00-04:00
#

FROM_TS=2023-07-11T19:37:00.00-04:00 
TO_TS=2023-07-11T20:37:00.00-04:00

# ND
echo "Fetching data for ND from ${FROM_TS} to ${TO_TS}"
pyarchappl-get --pv-file ../nd_pv.txt -vv \
    --from ${FROM_TS} --to ${TO_TS} \
    --output data_nd_1s.csv \
    --resample 1S

sleep 2

# IC
echo "Fetching data for IC from ${FROM_TS} to ${TO_TS}"
pyarchappl-get --pv-file ../ic_pv.txt -vv \
    --from ${FROM_TS} --to ${TO_TS} \
    --output data_ic_1s.csv \
    --resample 1S

sleep 2

# HMR
echo "Fetching data for HMR from ${FROM_TS} to ${TO_TS}"
pyarchappl-get --pv-file ../hmr_pv.txt -vv \
    --from ${FROM_TS} --to ${TO_TS} \
    --output data_hmr_1s.csv \
    --resample 1S
