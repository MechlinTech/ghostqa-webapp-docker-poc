import os

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