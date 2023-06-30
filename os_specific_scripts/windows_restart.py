import pickle
import shutil
import os
import sys

# define the checkpoint file path
CHECKPOINT_FILE = 'checkpoint.pkl'

# save the relevant state information
def save_checkpoint(file_path, line_number):
    checkpoint_data = {'file_path': file_path, 'line_number': line_number}
    with open(CHECKPOINT_FILE, 'wb') as f:
        pickle.dump(checkpoint_data, f)

# load the stored state
def load_checkpoint():
    with open(CHECKPOINT_FILE, 'rb') as f:
        checkpoint_data = pickle.load(f)
    return checkpoint_data['file_path'], checkpoint_data['line_number']

def restart_computer(current_file, line_number):
    # Save the checkpoint before restarting
    save_checkpoint(current_file, line_number)
    
    # Get the path to the current executable
    script_path = sys.executable

    # Get the startup folder path
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')

    # Copy the executable to the startup folder
    shutil.copy2(script_path, startup_folder)
    
    # Restart the computer (replace with your restart logic)
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


