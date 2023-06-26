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


""" 
Program execution order:
1. display program info
2. check if Docker is already installed
4. check that system meets general requirements (RAM, os, etc)
5. get correct Docker installer from https://docs.docker.com/desktop/ based on OS
6. 
"""

# Define the checkpoint file path
CHECKPOINT_FILE = 'checkpoint.pkl'

# Save the relevant state information
def save_checkpoint(line_number):
    checkpoint_data = {'line_number': line_number}
    with open(CHECKPOINT_FILE, 'wb') as f:
        pickle.dump(checkpoint_data, f)

# Load the stored state
def load_checkpoint():
    with open(CHECKPOINT_FILE, 'rb') as f:
        checkpoint_data = pickle.load(f)
    return checkpoint_data['line_number']

def restart_computer():
    # Save the checkpoint before restarting
    save_checkpoint(42)

    # Get the path to the current executable
    script_path = sys.executable

    # Get the startup folder path
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')

    # Copy the executable to the startup folder
    shutil.copy2(script_path, startup_folder)

    # Restart the computer
    os.system('shutdown /r /t 0')

def remove_from_startup():
    # Get the path to the current executable
    script_path = sys.executable

    # Get the startup folder path
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')

    # Construct the full path of the executable in the startup folder
    startup_executable = os.path.join(startup_folder, os.path.basename(script_path))

    # Remove the executable from the startup folder if it exists
    if os.path.exists(startup_executable):
        os.remove(startup_executable)

# prints general info to terminal and requires user input before continuing with the rest of the program
def program_info():
    print("This program downloads the Docker Desktop Installer and runs the installer in unattended mode")
    user_input = input("Do you wish to continue (y/n): ")
    if (user_input == "y") | (user_input == "Y"):
        return 0
    # user does not wish to continue
    elif (user_input == "n") | (user_input == "N"):
        return 1
    # invalid input
    else:
        return 2

# check to see if Docker is already installed
def have_docker():
    docker_check = subprocess.Popen(["docker", "--version"], stdout=subprocess.DEVNULL)
    docker_check.communicate()
    rc = docker_check.returncode
    if rc == 0:
        return 3
    else:
        print("Docker is not installed on this machine")
        return 0

# first step in docker installation is determining OS
def install_docker():
    print("RAM:                        ",psutil.virtual_memory().total / (1024. **3))
    print("platform.system()           ", platform.system())
    print("sysconfig.get_platform()    ", sysconfig.get_platform())
    print("platform.machine()          ", platform.machine())
    print("platform.architecture()     ", platform.architecture())

    if platform.system() == "Windows":
        windows()
    elif platform.system() == "Linux":
        linux()
    elif platform.system() == "Darwin":
        darwin()
    else:
        return 4
    return 0

def windows():
    if platform.system() == "Windows":
        if psutil.virtual_memory().total / (1024. **3) >= 4:
            print("System meets requirements")
            url = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?_gl=1*zgulyg*_ga*MTcyMzIxMjkxMi4xNjg0ODEzMDYw*_ga_XJWPQMJYHQ*MTY4NzU1NTk3OC4yMy4wLjE2ODc1NTU5NzguNjAuMC4w"
            r = requests.get(url)

            with open("Docker Desktop Installer.exe", 'wb') as f:
                f.write(r.content)
        
            

            return_code = subprocess.call(["C:\\codebase\\docker_install_script\\Docker Desktop Installer.exe"], stdout=subprocess.DEVNULL)

        if return_code != 0:
            print("Installation failed")
    
    return

def linux():
    return

def darwin():
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
    time.sleep(3)
    exit()
        

def main():
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