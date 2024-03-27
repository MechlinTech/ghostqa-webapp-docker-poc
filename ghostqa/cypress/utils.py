import os
import subprocess
import psutil
import re
from colorama import init, Fore

# Initialize colorama to work on Windows as well
init()

def parse_color_logs(log):
    # Define a regular expression to match ANSI escape codes for colors
    color_pattern = re.compile(r'\033\[(\d+)(;\d+)*m')

    # Split the log into segments based on color codes
    segments = color_pattern.split(log)

    # Process each segment and print with appropriate color
    for segment in segments:
        if segment.startswith('\033['):
            # Extract color code and apply the corresponding color
            color_code = int(segment[2:-1].split(';')[0])
            print_color(segment, color_code)
        else:
            # No color code, print as is
            print(segment, end='')

def print_color(text, color_code):
    # Map color codes to colorama Fore constants
    color_mapping = {
        30: Fore.BLACK,
        31: Fore.RED,
        32: Fore.GREEN,
        33: Fore.YELLOW,
        34: Fore.BLUE,
        35: Fore.MAGENTA,
        36: Fore.CYAN,
        37: Fore.WHITE,
    }

    # Print text with the corresponding color
    color = color_mapping.get(color_code, Fore.RESET)
    print(f"{color}{text}{Fore.RESET}", end='')

# Example usage
def create_directory(directory_path):
    """
    Check if a directory exists, and create it if it doesn't.
    
    Parameters:
    - directory_path (str): The path of the directory to be checked/created.
    
    Returns:
    - None
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created.")
    else:
        print(f"Directory '{directory_path}' already exists.")

def get_full_path(file_or_directory):
    """
    Get the full path of a file or directory.
    
    Parameters:
    - file_or_directory (str): The file or directory for which to find the full path.
    
    Returns:
    - str: The full path of the file or directory.
    """
    full_path = os.path.abspath(file_or_directory)
    return full_path

def convert_to_unix_path(file_path):
    return os.path.normpath(file_path).replace(os.sep, '/')


def list_files_in_directory(directory_path):
    """
    List all files in a directory and return a list of their full paths.
    
    Parameters:
    - directory_path (str): The path of the directory to list files from.
    
    Returns:
    - list: A list of full paths of files in the directory.
    """
    files_list = []
    
    # Ensure the given path is a directory
    if os.path.isdir(directory_path):
        # Get the list of files in the directory
        files = os.listdir(directory_path)
        
        # Create full paths for each file in the directory
        files_list = [convert_to_unix_path(os.path.join(directory_path, file)) for file in files if os.path.isfile(os.path.join(directory_path, file))]
    
    return files_list


def list_recurssive_files_in_directory(directory_path):
    """
    Recursively list all files in a directory and return a list of their full paths.
    
    Parameters:
    - directory_path (str): The path of the directory to list files from.
    
    Returns:
    - list: A list of full paths of files in the directory and its subdirectories.
    """
    files_list = []
    
    # Ensure the given path is a directory
    if os.path.isdir(directory_path):
        # Get the list of files and directories in the directory
        for root, dirs, files in os.walk(directory_path):
            # Iterate through files in the current directory
            for file in files:
                # Create full paths for each file
                file_path = os.path.join(root, file)
                # Append only if it's a file
                if os.path.isfile(file_path):
                    files_list.append(convert_to_unix_path(file_path))
    
    return files_list

def directory_exists(directory_path):
    """
    Check if a directory exists.

    Parameters:
    - directory_path (str): The path of the directory to check.

    Returns:
    - bool: True if the directory exists, False otherwise.
    """
    return os.path.exists(directory_path) and os.path.isdir(directory_path)




def poll_process(pid):
    try:
        process = psutil.Process(pid)
        while process.is_running():
            # Do something while the process is running
            return "Process is still running."
        return process.returncode
    except psutil.NoSuchProcess:
        return f"No process found with PID: {pid}"


def check_container_status(container_name):
    try:
        # Run the "docker inspect" command to get information about the container
        result = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Status}}", container_name],
            capture_output=True,
            text=True,
            check=True,
        )

        # Extract the container status from the output
        container_status = result.stdout.strip()

        # Check if the container has exited
        if container_status == "exited":
            return True
        else:
            return False

    except subprocess.CalledProcessError as e:
        # Handle the error (e.g., container not found)
        print(f"Error: {e}")
        return None

import os
import shutil

def copy_files_and_folders(source_dir, destination_dir):
    """
    Copy all files and folders from the source directory to the destination directory.

    Parameters:
    - source_dir (str): The path to the source directory.
    - destination_dir (str): The path to the destination directory.
    """

    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Walk through the source directory and copy files and folders
    for root, dirs, files in os.walk(source_dir):
        # Create the corresponding directories in the destination
        for dir_name in dirs:
            source_path = os.path.join(root, dir_name)
            destination_path = os.path.join(destination_dir, os.path.relpath(source_path, source_dir))
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)

        # Copy files to the destination
        for file_name in files:
            source_path = os.path.join(root, file_name)
            destination_path = os.path.join(destination_dir, os.path.relpath(source_path, source_dir))
            shutil.copy2(source_path, destination_path)    

import jsbeautifier

def format_javascript(input_code):
    try:
        # Use jsbeautifier to format the code
        formatted_code = jsbeautifier.beautify(input_code)

        # Return the formatted code
        return formatted_code

    except Exception as e:
        # Handle errors, if any
        print(f"Error while formatting JavaScript code: {e}")
        return input_code
# def check_container_status_and_exit_code(container_name):
#     try:
#         # Run the "docker ps -a" command to list all containers, including those that have exited
#         result = subprocess.run(['docker', 'ps', '-a', '--filter', f'name={container_name}', '--format', '{{.Status}} {{.ExitCode}}'], capture_output=True, text=True, check=True)

#         # Extract the container status and exit code from the output
#         output_lines = result.stdout.strip().split()

#         if len(output_lines) == 2:
#             container_status, exit_code = output_lines
#             return container_status, int(exit_code)
#         else:
#             return None, None


#     except subprocess.CalledProcessError as e:
#         # Print the error message and return None for both status and exit code
#         print(f"Error: {e}")
#         return None, None