from .file_scan_utils import scan_files_including_regex
import os
import json
import pandas as pd
from pathlib import Path
from typing import List, Optional

def load_csv_in_file_folder_by_regex(file_folder, regex, index_col=0):
    file_name = scan_files_including_regex(file_folder, regex)[-1]
    file_path = os.path.join(file_folder, file_name)
    df = pd.read_csv(file_path, index_col=index_col)
    return df

def load_json_in_file_folder_by_regex(file_folder, regex, index=-1):
    file_name = scan_files_including_regex(file_folder, regex)[index]
    file_path = os.path.join(file_folder, file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        dct = json.load(file)
    return dct

def load_xlsx_in_file_folder_by_regex(file_folder, regex):
    file_name = scan_files_including_regex(file_folder, regex)[-1]
    file_path = os.path.join(file_folder, file_name)
    df = pd.read_excel(file_path)
    return df

def load_single_file(file_path: str, file_type: Optional[str] = None) -> pd.DataFrame:
    path = Path(file_path)
    suffix = path.suffix.lower()
    
    if file_type or suffix == '':
        ft = file_type or '.csv'
    else:
        ft = suffix
    
    loaders = {
        '.csv': lambda p: pd.read_csv(p),
        '.xlsx': lambda p: pd.read_excel(p),
        '.xls': lambda p: pd.read_excel(p),
        '.json': lambda p: pd.read_json(p),
        '.parquet': lambda p: pd.read_parquet(p),
        '.pkl': lambda p: pd.read_pickle(p)
    }
    
    loader = loaders.get(ft, lambda p: pd.read_csv(p))
    return loader(file_path)

def load_files_to_dataframes(
    file_paths: List[str],
    file_type: Optional[str] = None
) -> List[pd.DataFrame]:
    return list(map(
        lambda path: load_single_file(path, file_type),
        file_paths
    ))

def load_file_to_dataframe(
    file_path: str,
    file_type: Optional[str] = None
) -> pd.DataFrame:
    return load_single_file(file_path, file_type)
