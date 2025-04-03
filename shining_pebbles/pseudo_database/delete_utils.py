import os
from .file_scan_utils import scan_files_including_regex

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"deleted: {file_path}")
    except FileNotFoundError:
        print(f"file not found: {file_path}")
    except Exception as e:
        print(f"deletion failed: {file_path}, reason: {e}")

def get_file_names_to_delete(file_paths, keep=10):
    if len(file_paths) <= keep:
        return []    
    sorted_files = sorted(file_paths)
    return sorted_files[:-keep]

def delete_old_files(file_paths, keep=10):
    files_to_delete = get_file_names_to_delete(file_paths, keep)
    if not files_to_delete:
        print("No files to delete.")
        return None
    print(f"files to delete: {len(files_to_delete)} files")
    for file_path in files_to_delete:
        delete_file(file_path)
    return None

def delete_old_files_in_file_folder_by_regex(file_folder, regex, keep=10):
    file_paths = scan_files_including_regex(file_folder, regex, option="path")
    delete_old_files(file_paths=file_paths, keep=keep)
    return None
