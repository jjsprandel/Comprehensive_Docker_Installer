import subprocess

# check to see if Docker is already installed
def have_docker():
    docker_check = subprocess.Popen(["docker", "--version"], stdout=subprocess.DEVNULL)
    docker_check.communicate()
    rc = docker_check.returncode
    if rc == 0:
        return 0
    else:
        print("Docker is not installed on this machine.")
        return 0