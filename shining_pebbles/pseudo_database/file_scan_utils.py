import os
import re

def scan_files_including_regex(file_folder, regex, option="name"):
    """
    Scans a folder for files matching a given regex pattern.

    Args:
        file_folder (str): The folder to scan.
        regex (str): The regex pattern to match.
        option (str): Whether to return file names ('name') or file paths ('path').

    Returns:
        list: A sorted list of matching file names or paths.
    """
    with os.scandir(file_folder) as files:
        lst = [file.name for file in files if re.findall(regex, file.name)]
    mapping = {
        "name": lst,
        "path": [os.path.join(file_folder, file_name) for file_name in lst],
    }
    lst_ordered = sorted(mapping[option])
    return lst_ordered

# function refactoring

from pathlib import Path
import re
from typing import List, Callable, Dict, Literal

def scan_folder(
    file_folder: str, 
    regex: str, 
    option_format: Literal["file_name", "file_path"] = "file_name"
) -> List[str]:
    path = Path(file_folder)
    
    # Filter files using regex pattern
    matches = filter(
        lambda f: re.search(regex, f.name) is not None,
        path.iterdir()
    )
    
    # Transform to either name or full path based on option
    mapping_output: Dict[str, Callable[[Path], str]] = {
        "file_name": lambda f: f.name,
        "file_path": lambda f: str(f.absolute())
    }
    
    # Apply transformation and sort
    return sorted(map(
        mapping_output[option_format], 
        matches
    ))