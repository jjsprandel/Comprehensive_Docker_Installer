import os
import shutil
import pickle
import sys
import requests
import subprocess
import psutil
import time
from os_specific_scripts.windows_restart import remove_from_startup

import subprocess

url = "https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi"
r = requests.get(url)
with open("wsl_update_x64.msi", 'wb') as f:
    f.write(r.content)

path = os.getcwd()
file = path + "\\wsl_update_x64.msi"
print(file)
# run the update package
subprocess.call([$file])
