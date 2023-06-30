import os
import sys
import platform
import sysconfig
import psutil
import requests
import subprocess
import shutil
import pickle
import time
from misc_scripts.have_docker import have_docker
from os_specific_scripts.windows_install import windows_install
from os_specific_scripts.windows_install import windows_install_cont
from os_specific_scripts.darwin_install import darwin_install
from os_specific_scripts.windows_restart import load_checkpoint
from os_specific_scripts.windows_restart import remove_from_startup

""" 
PROGRAM EXECUTION ORDER:
1. display program info
2. check if Docker is already installed
3. determine OS

For Windows:
    1. enable Windows Subsystem for Linux
    2. check requirements for running WSL 2
    3. enable virtualization
    4. restart the machine
    5. download the Linux kernel update package
    6. run the update package
    7. set WSL2 as default version
    8. check Windows version for requirements to install Docker
    9. download Docker installer
    10. run Docker

For macOS (ARM):
    1. install Rosetta 2
    2. download the Docker installer
    3. run the installer
    4. run Docker

For macOS (Intel):
    1. check macOS version for requirements
    2. check system requirements (RAM)
    3. check VirtualBox version
    4. download the Docker installer
    4. run the installer
    5. run Docker

For Linux:
    ** OS not added **
"""

CHECKPOINT_FILE = 'checkpoint.pkl'

# prints general info to terminal and requires user input before continuing with the rest of the program
def program_info():
    
    print("\nThis is a platform-independent Docker Desktop Installer. All requirements/features will be installed and enabled for your OS.")
    user_input = input("Do you wish to continue (y/n): ")
    if (user_input == "y") | (user_input == "Y"):
        return 0
    # user does not wish to continue
    elif (user_input == "n") | (user_input == "N"):
        return 1
    # invalid input
    else:
        return 2

# first step in docker installation is determining OS
def install_docker():
    if platform.system() == "Windows":
        return_code = windows_install()
        if return_code != 0:
            return return_code
    elif platform.system() == "Linux":
        linux()
    elif platform.system() == "Darwin":
        darwin_install()
    else:
        return 4
    return 0

def linux():
    return

def error_handling(error_code):
    # default error, no message
    if error_code == 1:
        None
    elif error_code == 2:
        print("Invalid input")
    elif error_code == 3:
        docker_version = subprocess.check_output(["docker", "--version"], text=True)
        print (docker_version[0:21], "is already installed on this machine")
    elif error_code == 4:
        print("This OS is not currently supported")
    
    print("exiting............................................................................")
    time.sleep(2)
    exit()
        

def main():
    # if checkpoint file exists, continue program from where it left off
    if os.path.exists(CHECKPOINT_FILE):
        remove_from_startup()
        file_path, line_to_resume = load_checkpoint()
        windows_install_cont()
    
    else:
        error_code = program_info()
        if error_code != 0:
            error_handling(error_code)

        error_code = have_docker()
        if error_code != 0:
            error_handling(error_code)

        install_docker()
        if error_code != 0:
            error_handling(error_code)

if __name__ == '__main__':
    main()
