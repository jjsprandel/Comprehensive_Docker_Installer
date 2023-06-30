import subprocess
import requests
import psutil
import sys
import os
from os_specific_scripts.windows_restart import restart_computer
from os_specific_scripts.windows_restart import remove_from_startup
import time

def windows_install():
    # checking if WSL is enabled
    output = subprocess.run(['wslconfig', '/l'], capture_output=True, text=True)

    # check the command's return code
    if output.returncode == 0:
        # in case return code can equal 0 but WSL is not installed, check stdout
        if output.stdout.replace('\x00', '').startswith('Windows Subsystem for Linux Distributions:') == True:
            print("WSL already enabled")
            time.sleep(1)
    else:
        # Print the error message
        print(output.stderr)
        
        print("\nenabling Windows Subsystem for Linux (WSL)")
        time.sleep(1)
        wsl_en = subprocess.call(
            [
                "powershell.exe", 
                "-noprofile", "-c",
                r"""
                Start-Process -Verb RunAs -Wait powershell.exe -Args "
                    dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
                    "
                """
            ]
        )
        

    time.sleep(1)

    # enable virtualization
    print("\nenabling virtualization")
    time.sleep(2)
    virt_en = subprocess.call(
        [
            "powershell.exe", 
            "-noprofile", "-c",
            r"""
            Start-Process -Verb RunAs -Wait powershell.exe -Args "
                dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
                "
            """
        ]
    )

    # restart machine
    current_file = os.path.abspath(__file__)
    line_number = 39
    
    print("\nYour machine must be restarted. Upon restart, the installation will automatically finish.")
    user_input = input("Do you wish to continue (y/n): ")
    if (user_input == "y") | (user_input == "Y"):
        restart_computer(current_file, line_number)
    # user does not wish to continue
    elif (user_input == "n") | (user_input == "N"):
        return 1
    # invalid input
    else:
        return 2


def windows_install_cont():
    # remove executable from startup folder
    remove_from_startup()
    
    # download the Linux kernel update package
    url = "https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi"
    r = requests.get(url)
    with open("wsl_update_x64.msi", 'wb') as f:
        f.write(r.content)
    
    # run the update package
    subprocess.call([os.getcwd()+"\\wsl_update_x64.msi"])

    time.sleep(2)

    return_code = subprocess.call(["powershell", "wsl --set-default-version 2"]) 

    if psutil.virtual_memory().total / (1024. **3) >= 4:
        print("System meets requirements")
        url = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
        r = requests.get(url)

        with open("Docker Desktop Installer.exe", 'wb') as f:
            f.write(r.content)

        return_code = subprocess.call(["C:\\codebase\\jjsprandel\\docker_install_script\\Docker Desktop Installer.exe"], stdout=subprocess.DEVNULL)

    if return_code != 0:
        print("Installation failed")
    
    return