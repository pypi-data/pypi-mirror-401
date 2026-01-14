from simba.utils.read_write import fetch_pip_data
from simba.utils.enums import OS
from simba.utils.printing import stdout_information

def check_for_updates():
    _, latest_simba_version = fetch_pip_data(pip_url=r'https://pypi.org/pypi/simba-uw-tf-dev/json')
    env_simba_version = OS.SIMBA_VERSION.value
    if latest_simba_version == env_simba_version:
        msg = f'UP-TO-DATE. \nYou have the latest SimBA version ({env_simba_version}).'
    else:
        msg = (f'NEW VERSION AVAILABLE. \nYou have SimBA version {env_simba_version}. \nThe latest version is {latest_simba_version}. '
               f'\nYou can update using "pip install simba-uw-tf-dev --upgrade"')
    stdout_information(msg=msg, source=check_for_updates.__name__)


check_for_updates()


import h5py
print("HDF5 library version:", h5py.version.hdf5_version)
print("h5py version:", h5py.__version__)

PATH = r"E:\h5_read\20251208_TS1_Gr3_T1.h5"

f = h5py.File(PATH, "r")
print(list(f.keys()))