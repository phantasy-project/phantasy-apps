## Set up the development environment in CTS network

The working machine is `csstudio` (Debian 11), from where, the PV write permission is granted.

Debian 12: work-cts-r4300-01

### Support IOC
CTS provides all the PVs, but lacks some logic.
- Start the IOC on csstudio.cts machine.

### Python Environment
- virtualenv: "phantasy-env" in develop-vmphy0-v11:~/Desktop
  - virtualenv phantasy-env
  - source phantasy-env/bin/activate
  - pip install -r requirements-phantasy.txt
- rsync -av phantasy-env/ zhangt@csstudio-cts:~/phantasy-env
- [csstudio] edit path:
  - ~/phantasy-env/bin/activate: VIRTUAL_ENV
  - ~/phantasy-env/bin/<exec>: #!
- Run the app on csstudio:
  - source ~/phantasy-env/bin/activate
  - ./run_asapp.py

### Qt Issue
Could not load the Qt platform plugin "xcb":
- apt download libxcb-cursor0 libxcb-render-util0 libxcb-icccm4 libxcb-xinerama0 \
               libxcb-image0 libxcb-xkb1 libxcb-keysyms1 libxkbcommon-x11-0 \
               libpython3.9 # for flame-code
- for i in *.deb; do dpkg -x $i .; done
- move all .so libs to a folder, add it to LD_LIBRARY_PATH

### Shell Environment
Set up .bashrc:
# for cothread installed via pip install
export EPICS_BASE=/usr/lib/epics
# phantasy
export PYTHONPATH=$HOME/mpl4qt:$HOME/unicorn:$HOME/phantasy:$HOME/phantasy-apps:$HOME/phantasy-ui:$PYTHONPATH
export PHANTASY_CONFIG_DIR=$HOME/phantasy-machines
export LD_LIBRARY_PATH=$HOME/libs:$LD_LIBRARY_PATH