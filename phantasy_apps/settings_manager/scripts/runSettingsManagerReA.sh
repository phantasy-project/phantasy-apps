#!/usr/bin/env bash

#
# Start Settings Manager for ReA
#

export EPICS_CA_ADDR_LIST='controlgw1.nscl.msu.edu:6064 controlgw2.nscl.msu.edu:6064'
settings_manager
