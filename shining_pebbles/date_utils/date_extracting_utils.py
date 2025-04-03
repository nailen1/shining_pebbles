from functools import partial
from shining_pebbles.file_scan_utils import scan_files_including_regex
from .date_converter_utils import transform_date_str_to_date_str_dashed

def parse_date(file_name, pattern, option_dashed=True):
    date = file_name.split(pattern)[-1].split("-")[0]
    return transform_date_str_to_date_str_dashed(date) if option_dashed else date

def parse_date_pair(file_name, start_pattern, end_pattern, option_dashed=True):
    start_date = parse_date(file_name, start_pattern, option_dashed)
    end_date = parse_date(file_name, end_pattern, option_dashed)
    return start_date, end_date

extract_date_ref = partial(parse_date, pattern="-at")

extract_timeseries_date_pair = partial(
    parse_date_pair, 
    start_pattern="-from", 
    end_pattern="-to"
)

extract_period_date_pair = partial(
    parse_date_pair, 
    start_pattern="-between", 
    end_pattern="-and"
)

def extract_from_files(file_folder, regex, extractor, **kwargs):
    file_names = scan_files_including_regex(file_folder=file_folder, regex=regex)
    return [extractor(file_name=file_name, **kwargs) for file_name in file_names]

def extract_dates_ref_in_file_folder_by_regex(file_folder, regex, option_dashed=True):
    return extract_from_files(
        file_folder=file_folder, 
        regex=regex, 
        extractor=extract_date_ref, 
        option_dashed=option_dashed
    )

def extract_timeseries_date_pairs_in_file_folder_by_regex(file_folder, regex, option_dashed=True):
    return extract_from_files(
        file_folder=file_folder, 
        regex=regex, 
        extractor=extract_timeseries_date_pair, 
        option_dashed=option_dashed
    )

def extract_period_date_pairs_in_file_folder_by_regex(file_folder, regex, option_dashed=True):
    return extract_from_files(
        file_folder=file_folder, 
        regex=regex, 
        extractor=extract_period_date_pair, 
        option_dashed=option_dashed
    )