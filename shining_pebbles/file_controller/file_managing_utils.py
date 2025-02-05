import os
import shutil

def archive_a_file(file_path, file_folder_archive):
    """
    Move a file to a specific folder.

    Parameters:
        file_path (str): The path of the file to move.
        file_folder_archive (str): The folder where the file will be moved.

    Returns:
        bool: True if the file was moved successfully, False otherwise.
    """
    try:
        # Ensure the destination folder exists
        os.makedirs(file_folder_archive, exist_ok=True)

        # Move the file
        shutil.move(file_path, file_folder_archive)
        print(f"File moved to {file_folder_archive}")
        return True
    except FileNotFoundError:
        print("Error: The file does not exist.")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def delete_a_file(file_path):
    """
    Delete a specific file.

    Parameters:
        file_path (str): The path of the file to delete.

    Returns:
        bool: True if the file was deleted successfully, False otherwise.
    """
    try:
        os.remove(file_path)
        print(f"File {file_path} deleted.")
        return True
    except FileNotFoundError:
        print("Error: The file does not exist.")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
