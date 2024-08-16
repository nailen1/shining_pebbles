import pandas as pd
import json
import os
import re
import time
import calendar
import datetime
import shutil
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import List, Tuple

def measure_time(func):
    """
    A decorator that measures the execution time of a given function.

    Args:
        func (callable): The function to be measured.

    Returns:
        callable: The wrapped function with execution time measurement.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"Function '{func.__name__}' execution took {duration:.9f} seconds.")
        return result
    return wrapper

def get_today(form="%Y-%m-%d"):
    """
    Returns today's date in the specified format.

    Args:
        form (str): The date format.

    Returns:
        str or datetime: The current date in the specified format.
    """
    mapping = {
        "%Y%m%d": datetime.now().strftime("%Y%m%d"),
        "yyyymmdd": datetime.now().strftime("%Y%m%d"),
        "%Y-%m-%d": datetime.now().strftime("%Y-%m-%d"),
        "yyyy-mm-dd": datetime.now().strftime("%Y-%m-%d"),
        "datetime": datetime.now(),
        "%Y%m%d%H": datetime.now().strftime("%Y%m%d%H"),
        "%Y%m%d%H%M": datetime.now().strftime("%Y%m%d%H%M"),
        "%Y-%m-%d-%H-%M": datetime.now().strftime("%Y-%m-%d-%H-%M"),
        "%Y%m%d%H%M%S": datetime.now().strftime("%Y%m%d%H%M%S"),
        "%Y-%m-%d %H:%M:%S": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "save": datetime.now().strftime("%Y%m%d%H%M"),
    }
    today = mapping[form]
    return today

def get_date_n_days_ago(date, n, form=None):
    """
    Returns the date n days before the given date.

    Args:
        date (str or datetime): The reference date.
        n (int): The number of days before the reference date.
        form (str, optional): The output date format. If None, the input date format will be used.

    Returns:
        str or datetime: The date n days before the reference date in the specified format if input is str,
                         or as a datetime object if input is datetime.
    """
    if isinstance(date, str):
        if '-' in date:
            input_format = '%Y-%m-%d'
        elif len(date) == 8 and date.isdigit():
            input_format = '%Y%m%d'
        else:
            raise ValueError("Unsupported date format")
        
        date_dt = datetime.strptime(date, input_format)
        date_before_n_dt = date_dt - timedelta(days=n)
        output_format = form if form else input_format
        return date_before_n_dt.strftime(output_format)
    
    elif isinstance(date, datetime):
        date_before_n_dt = date - timedelta(days=n)
        return date_before_n_dt
    
    else:
        raise TypeError("Input date must be a string or a datetime object")

def get_yesterday(form="%Y-%m-%d"):
    """
    Returns yesterday's date in the specified format.

    Args:
        form (str): The date format.

    Returns:
        str: Yesterday's date in the specified format.
    """
    today = get_today(form)
    yesterday = get_date_n_days_ago(today, 1, form)
    return yesterday

def get_date_n_weeks_ago(date, n, form="%Y-%m-%d"):
    """
    Returns the date n weeks before the given date.

    Args:
        date (str): The reference date.
        n (int): The number of weeks before the reference date.
        form (str): The output date format.

    Returns:
        str: The date n weeks before the reference date in the specified format.
    """
    date = date.replace("-", "")
    date_dt = datetime.strptime(date, "%Y%m%d")
    date_before_n_dt = date_dt - timedelta(weeks=n)
    date_before_n_str = date_before_n_dt.strftime(form)
    return date_before_n_str

def is_the_last_date_of_month(date):
    """
    Checks if the given date is the last day of the month.

    Args:
        date (str or datetime): The date to check.

    Returns:
        bool: True if the date is the last day of the month, False otherwise.
    """
    if isinstance(date, str):
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    elif isinstance(date, datetime):
        date_obj = date
    else:
        raise ValueError("Input must be a string in 'YYYY-MM-DD' format or a datetime object")
    
    next_month = date_obj + relativedelta(months=1)
    last_day_of_month = next_month.replace(day=1) - relativedelta(days=1)
    
    return date_obj.day == last_day_of_month.day

def get_date_n_month_ago(date, n, form="%Y-%m-%d"):
    """
    Returns the date n months before the given date.

    Args:
        date (str or datetime): The reference date.
        n (int): The number of months before the reference date.
        form (str): The output date format.

    Returns:
        str: The date n months before the reference date in the specified format.
    """
    if isinstance(date, str):
        date_obj = datetime.strptime(date, form)
    elif isinstance(date, datetime):
        date_obj = date
    else:
        raise ValueError("Input must be a string in the specified format or a datetime object")
    
    if is_the_last_date_of_month(date_obj):
        previous_month = date_obj - relativedelta(months=n)
        next_month = previous_month + relativedelta(months=1)
        last_day_of_previous_month = next_month.replace(day=1) - relativedelta(days=1)
        result_date = last_day_of_previous_month
    else:
        result_date = date_obj - relativedelta(months=n)
    
    return result_date.strftime(form)

def detect_date_format(date_str):
    """
    Detects the date format of a given date string.

    Args:
        date_str (str): The date string to detect the format of. Expected formats are 'YYYY-MM-DD' or 'YYYYMMDD'.

    Returns:
        str: The detected date format ('%Y-%m-%d' or '%Y%m%d').
    """
    if '-' in date_str:
        return "%Y-%m-%d"
    else:
        return "%Y%m%d"


def get_month_end_dates(start_year_month: str, end_year_month: str, date_format: str = "%Y%m%d") -> List[str]:
    """
    Generates a list of month-end dates between two given year-months.

    Args:
        start_year_month (str): The start year-month in the format 'YYYYMM'.
        end_year_month (str): The end year-month in the format 'YYYYMM'.
        date_format (str): The format in which to return the dates (default is '%Y%m%d').

    Returns:
        list: A list of month-end dates in the specified format.

    Raises:
        ValueError: If the input date strings are not in the 'YYYYMM' format.
    """
    try:
        start_date = datetime.strptime(start_year_month, "%Y%m")
        end_date = datetime.strptime(end_year_month, "%Y%m")
    except ValueError:
        raise ValueError("The date strings must be in 'YYYYMM' format")

    month_end_dates = []
    current_date = start_date
    while current_date <= end_date:
        last_day = calendar.monthrange(current_date.year, current_date.month)[1]
        month_end_date = current_date.replace(day=last_day)
        month_end_dates.append(month_end_date.strftime(date_format))
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1, day=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1, day=1)
    
    return month_end_dates


def get_end_date_pairs(start_year_month: str, end_year_month: str, date_format: str = '%Y-%m-%d') -> List[Tuple[str, str]]:
    """
    Generates a list of tuples, where each tuple contains a pair of consecutive month-end dates between two given year-months.

    Args:
        start_year_month (str): The start year-month in the format 'YYYYMM'.
        end_year_month (str): The end year-month in the format 'YYYYMM'.
        date_format (str): The format in which to return the dates (default is '%Y-%m-%d').

    Returns:
        list: A list of tuples, each containing a pair of consecutive month-end dates in the specified format.

    Raises:
        ValueError: If the input date strings are not in the 'YYYYMM' format.
    """
    # Generate the list of month-end dates using the provided function
    end_dates = get_month_end_dates(start_year_month=start_year_month, end_year_month=end_year_month, date_format=date_format)
    
    # Create pairs of consecutive month-end dates
    dates_i = end_dates[:-1]
    dates_f = end_dates[1:]
    dates = list(zip(dates_i, dates_f))
    
    return dates


def generate_date_list(start_date_str):
    """
    Generates a list of date strings from a given start date to today.

    The function detects the format of the input date string and generates a list of dates in the same format
    from the start date up to the current date.

    Args:
        start_date_str (str): The start date string. Expected formats are 'YYYY-MM-DD' or 'YYYYMMDD'.

    Returns:
        list of str: A list of date strings from the start date to today in the same format as the input.
    """
    date_format = detect_date_format(start_date_str)
    start_date = datetime.strptime(start_date_str, date_format)
    today = datetime.today()

    date_list = []
    current_date = start_date
    while current_date <= today:
        date_list.append(current_date.strftime(date_format))
        current_date += timedelta(days=1)

    return date_list

def get_last_day_of_month(year, month):
    """
    Returns the last day of a given month.

    Args:
        year (int): The year.
        month (int): The month.

    Returns:
        str: The last day of the month in 'YYYY-MM-DD' format.
    """
    year_input = int(year)
    month_input = int(month)
    _, last_day = calendar.monthrange(year_input, month_input)
    return f"{year_input}-{month_input:02d}-{last_day}"

def get_weekday(date, language='EN'):
    """
    Returns the weekday of a given date.

    Args:
        date (str): The date string in 'YYYY-MM-DD' format.
        language (str): The language of the weekday ('EN', 'EN-full', 'KR', 'KR-full').

    Returns:
        str: The weekday name in the specified language.
    """
    year = int(date.split('-')[0])
    month = int(date.split('-')[1])
    day = int(date.split('-')[2])
    day_index = calendar.weekday(year, month, day)
    mapping = {
        'EN-full': ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        'EN': ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        'KR-full': ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"],
        'KR': ["월", "화", "수", "목", "금", "토", "일"],
    }
    weekday = mapping[language][day_index]
    return weekday

def get_dates_by_day_of_week(year):
    """
    Returns a dictionary of dates grouped by day of the week for a given year.

    Args:
        year (int): The year.

    Returns:
        dict: A dictionary with days of the week as keys and lists of date strings as values.
    """
    days_of_week = ['월', '화', '수', '목', '금', '토', '일']
    dates_by_day = {day: [] for day in days_of_week}
    date = datetime.date(year, 1, 1)
    while date.year == year:
        day_index = date.weekday()
        day_name = days_of_week[day_index]
        dates_by_day[day_name].append(date.isoformat())
        date += datetime.timedelta(days=1)
    
    return dates_by_day

def get_past_dates(date_str, n, form="%Y-%m-%d"):
    """
    Returns a list of past dates from a given date.

    Args:
        date_str (str): The reference date string.
        n (int): The number of past dates to return.
        form (str): The date format.

    Returns:
        list of str: A list of past date strings.
    """
    start_date = datetime.strptime(date_str, form)
    past_dates = [(start_date - timedelta(days=i)).strftime(form) for i in range(n)]
    return past_dates

def get_date_range(start_date_str, end_date_str, form="%Y-%m-%d"):
    """
    Returns a list of dates between a start date and an end date.

    Args:
        start_date_str (str): The start date string.
        end_date_str (str): The end date string.
        form (str): The date format.

    Returns:
        list of str: A list of date strings between the start and end dates.
    """
    start_date = datetime.strptime(start_date_str, form)
    end_date = datetime.strptime(end_date_str, form)
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date.strftime(form))
        current_date += timedelta(days=1)
    return date_list

def calculate_prior_date_extended(base_date, days=0, months=0, years=0):
    """
    Calculates a prior date from a given base date by a specified number of days, months, and years.

    Args:
        base_date (str): The base date string in 'YYYY-MM-DD' format.
        days (int): The number of days to subtract.
        months (int): The number of months to subtract.
        years (int): The number of years to subtract.

    Returns:
        str: The calculated prior date in 'YYYY-MM-DD' format.
    """
    date_format = "%Y-%m-%d"
    base_date_obj = datetime.strptime(base_date, date_format)
    prior_date_obj = base_date_obj - relativedelta(days=days, months=months, years=years)
    return prior_date_obj.strftime(date_format)


def convert_keys(data, key_mapping):
    """
    Converts the keys of dictionaries in a list according to a given key mapping.

    Parameters:
    data (list of dict): List of dictionaries with the original keys.
    key_mapping (dict): Dictionary with original keys as keys and new keys as values.

    Returns:
    list of dict: List of dictionaries with the converted keys.
    """
    return [{key_mapping.get(k, k): v for k, v in item.items()} for item in data]


def rename_key(dct, old_key, new_key):
    """
    Renames a key in a dictionary.

    Args:
        dct (dict): The dictionary.
        old_key (str): The old key to be renamed.
        new_key (str): The new key name.

    Returns:
        dict: The dictionary with the renamed key.
    """
    if old_key in dct:
        dct[new_key] = dct.pop(old_key)
    else:
        print(f"Key '{old_key}' not found in the dictionary.")
    
    return dct

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

def open_df_in_file_folder_by_regex(file_folder, regex, option="path", index_col=0):
    """
    Opens a DataFrame from the latest file in a folder matching a regex pattern.

    Args:
        file_folder (str): The folder to scan.
        regex (str): The regex pattern to match.
        option (str): Whether to match file names ('name') or file paths ('path').
        index_col (int): The column to use as the row labels of the DataFrame.

    Returns:
        pd.DataFrame: The DataFrame loaded from the file.
    """
    latest_file_path = scan_files_including_regex(file_folder, regex, option)[-1]
    df = pd.read_csv(latest_file_path, index_col=index_col)
    return df

def open_json_in_file_folder_by_regex(file_folder, regex, option="path", index=-1):
    """
    Opens a JSON object from a file in a folder matching a regex pattern.

    Args:
        file_folder (str): The folder to scan.
        regex (str): The regex pattern to match.
        option (str): Whether to match file names ('name') or file paths ('path').
        index (int): The index of the file in the matched list.

    Returns:
        dict: The JSON object loaded from the file.
    """
    latest_file_path = scan_files_including_regex(file_folder, regex, option)[index]
    with open(latest_file_path, 'r', encoding='utf-8') as file:
        dct = json.load(file)
    return dct

def get_last_key_and_value_in_json_file(dct):
    """
    Returns the last key and value in a JSON object.

    Args:
        dct (dict): The JSON object.

    Returns:
        tuple: The last key and value in the JSON object.
    """
    last_key = next(reversed(dct))
    last_value = dct[last_key]
    return last_key, last_value


def format_date_to_str(date_input, form='%Y-%m-%d'):
    """
    Formats a date input to a specified string format if it is a datetime object.
    
    Args:
        date_input (str or datetime): The input date which can be a string or a datetime object.
        output_format (str): The format to convert the datetime object to. Defaults to '%Y-%m-%d'.
    
    Returns:
        str: The formatted date string or the original string if the input is already a string.
    
    Raises:
        ValueError: If the input date is not a string or datetime object.
    """
    if isinstance(date_input, datetime):
        return date_input.strftime(form)
    elif isinstance(date_input, str):
        return date_input
    else:
        raise ValueError("Input date must be a string or datetime object.")


def convert_type_of_date_input(date, form):
    """
    Converts the input date based on its type.

    If the input date is a string, it converts it to a datetime object using the given format.
    If the input date is a datetime object, it converts it to a string using the given format.

    Args:
        date (str or datetime): The input date which can be a string or a datetime object.
        form (str): The format to use for conversion.

    Returns:
        datetime or str: The converted date in the specified format.

    Raises:
        ValueError: If the input date is not a string or datetime object.
    """
    if isinstance(date, str):
        date = datetime.strptime(date, form)
    elif isinstance(date, datetime):
        date = date.strftime(form)
    else:
        raise ValueError("Input date must be a string or datetime object.")
    
    return date


def save_dataset_of_subject_at(df, file_folder, subject, input_date):
    """
    Saves the dataset of a specific subject at a given date.

    Args:
        df (pandas.DataFrame): The DataFrame to save.
        file_folder (str): The folder where the file should be saved.
        subject (str): The subject of the dataset.
        input_date (str): The date for the dataset.

    Returns:
        pandas.DataFrame: The saved DataFrame.
    """
    check_folder_and_create_folder(file_folder)
    # Create file name with subject and input_date
    file_name = f'dataset-{subject}-at{input_date.replace("-","")}-save{get_today("%Y%m%d%H")}.csv'
    file_path = os.path.join(file_folder, file_name)
    # Save DataFrame to CSV
    df.to_csv(file_path, encoding='utf-8-sig')
    print(f'- save complete: {file_path}')
    return df


def save_dataset_of_subject_from_to(df, file_folder, subject, start_date=None, end_date=None):
    """
    Saves the dataset of a specific subject from a start date to an end date.

    Args:
        df (pandas.DataFrame): The DataFrame to save.
        file_folder (str): The folder where the file should be saved.
        subject (str): The subject of the dataset.
        start_date (str, optional): The start date for the dataset. If None, uses the first date in the DataFrame.
        end_date (str, optional): The end date for the dataset. If None, uses the last date in the DataFrame.

    Returns:
        pandas.DataFrame: The saved DataFrame.
    """
    dates = df.index.tolist()
    # Format start_date and end_date if not provided
    start_date = format_date_to_str(dates[0], form="%Y%m%d")
    end_date = format_date_to_str(dates[-1], form="%Y%m%d")
    check_folder_and_create_folder(file_folder)
    # Create file name with subject, start_date, and end_date
    file_name = f'dataset-{subject}-from{start_date.replace("-","")}-to{end_date.replace("-","")}-save{get_today("%Y%m%d%H")}.csv'
    file_path = os.path.join(file_folder, file_name)
    # Save DataFrame to CSV
    df.to_csv(file_path, encoding='utf-8-sig')
    print(f'- save complete: {file_path}')
    return df


def save_df_to_file(df, file_folder, file_name_var, file_extension=".csv", archive=False, file_folder_archive="./archive"):
    """
    Saves a DataFrame to a file, optionally archiving the previous file.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        file_folder (str): The folder to save the file in.
        file_name_var (str): The variable part of the file name.
        file_extension (str): The file extension.
        archive (bool): Whether to archive the previous file.
        file_folder_archive (str): The folder to save the archived file in.

    Returns:
        None
    """
    def get_today(form="%Y%m%d"):
        return datetime.now().strftime(form)
    try:
        save_time = get_today()
        file_name = f"dataset-{file_name_var}-save{save_time}{file_extension}"
        file_path = os.path.join(file_folder, file_name)
        if os.path.exists(file_path) and archive:
            df_archive = pd.read_csv(file_path)
            os.makedirs(file_folder_archive, exist_ok=True)
            archive_file_name = "archive-" + file_name
            archive_file_path = os.path.join(file_folder_archive, archive_file_name)
            df_archive.to_csv(archive_file_path, index=False)
            print(f"Archived: {archive_file_path}")
        df.to_csv(file_path, index=False)
        print(f"Saved: {file_path}")
    except Exception as e:
        print(f"Error: {e}")

def check_folder_and_create_folder(folder_name):
    """
    Checks if a folder exists, and creates it if it does not.

    Args:
        folder_name (str): The folder name.

    Returns:
        str: The folder name.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Created: {folder_name}")
    else:
        print(f"Already exists: {folder_name}")
    return folder_name


def quarter_string_to_date(quarter_string):
    """
    Converts a quarter string to a datetime object representing the first day of the quarter.

    Args:
        quarter_string (str): The quarter string, formatted as 'YYYY QX'.

    Returns:
        datetime: The datetime object representing the first day of the quarter.
    """
    year, q = quarter_string.split(' ')
    year = int(year)
    quarter = int(q.replace('Q', '').strip())
    quarter_to_month = {1: 1, 2: 4, 3: 7, 4: 10}
    month = quarter_to_month[quarter]
    return pd.Timestamp(year=year, month=month, day=1)

def year_string_to_date(year_string):
    """
    Converts a year string to a datetime object representing the first day of the year.

    Args:
        year_string (str): The year string, formatted as 'YYYY'.

    Returns:
        datetime: The datetime object representing the first day of the year.
    """
    year = f'{year_string}-01-01'
    return pd.Timestamp(year=year, month=1, day=1)

def fill_all_dates_from_start_to_end(start_date, end_date):
    """
    Generates a list of all dates between a start date and an end date.

    Args:
        start_date (str): The start date string.
        end_date (str): The end date string.

    Returns:
        list of str: A list of all date strings between the start and end dates.
    """
    date_range = pd.date_range(start=start_date, end=end_date)
    return date_range.strftime("%Y-%m-%d").tolist()

def fill_all_first_days_of_months(start_date, end_date):
    """
    Generates a list of the first day of each month between a start date and an end date.

    Args:
        start_date (str): The start date string.
        end_date (str): The end date string.

    Returns:
        list of str: A list of the first day of each month between the start and end dates.
    """
    date_range = pd.date_range(start=start_date, end=end_date)
    first_days = [date for date in date_range if date.day == 1]
    return [date.strftime("%Y-%m-%d") for date in first_days]

def get_last_day_of_previous_month(input_date_str):
    """
    Returns the last day of the previous month from a given date.

    Args:
        input_date_str (str): The input date string in 'YYYY-MM-DD' format.

    Returns:
        str: The last day of the previous month in 'YYYY-MM-DD' format.
    """
    input_date = datetime.strptime(input_date_str, '%Y-%m-%d')
    first_day_of_current_month = input_date.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    return last_day_of_previous_month.strftime('%Y-%m-%d')

def get_quarters(start_year, end_year):
    """
    Returns a list of quarter strings from a start year to an end year.

    Args:
        start_year (int): The start year.
        end_year (int): The end year.

    Returns:
        list of str: A list of quarter strings.
    """
    quarters = []
    for year in range(start_year, end_year - 1, -1):
        for quarter in ['4Q', '3Q', '2Q', '1Q']:
            quarters.append(f'{year} {quarter}')
    return quarters

def pick_something_in_string(string, something):
    """
    Finds a substring in a string using a regex pattern.

    Args:
        string (str): The input string.
        something (str): The regex pattern to match.

    Returns:
        str: The matched substring.
    """
    return re.search(pattern=something, string=string).group()

def pick_n_characters_followed_by_something_in_string(string, something, n):
    """
    Finds a substring followed by n characters in a string using a regex pattern.

    Args:
        string (str): The input string.
        something (str): The substring to find.
        n (int): The number of characters to match after the substring.

    Returns:
        str: The matched substring.
    """
    regex = re.escape(something) + fr'(\w{{{n}}})'
    match = re.search(pattern=regex, string=string)
    if match:
        return match.group(1)
    else:
        return None

def pick_menu_code_in_file_name(file_name):
    """
    Finds the menu code in a file name.

    Args:
        file_name (str): The file name.

    Returns:
        str: The menu code.
    """
    return pick_n_characters_followed_by_something_in_string(file_name, something='menu', n=4)

def pick_code_in_file_name(file_name):
    """
    Finds the code in a file name.

    Args:
        file_name (str): The file name.

    Returns:
        str: The code.
    """
    return pick_n_characters_followed_by_something_in_string(file_name, something='code', n=6)

def pick_input_date_in_file_name(file_name):
    """
    Finds the input date in a file name.

    Args:
        file_name (str): The file name.

    Returns:
        str: The input date.
    """
    return pick_n_characters_followed_by_something_in_string(file_name, something='at', n=8)

def pick_start_date_in_file_name(file_name):
    """
    Finds the start date in a file name.

    Args:
        file_name (str): The file name.

    Returns:
        str: The start date.
    """
    return pick_n_characters_followed_by_something_in_string(file_name, something='from', n=8)

def pick_end_date_in_file_name(file_name):
    """
    Finds the end date in a file name.

    Args:
        file_name (str): The file name.

    Returns:
        str: The end date.
    """
    return pick_n_characters_followed_by_something_in_string(file_name, something='to', n=8)

def pick_save_date_in_file_name(file_name):
    """
    Finds the save date in a file name.

    Args:
        file_name (str): The file name.

    Returns:
        str: The save date.
    """
    return pick_n_characters_followed_by_something_in_string(file_name, something='save', n=8)

def get_fund_codes_in_file_folder(dataset_file_folder):
    """
    Returns a list of fund codes in a file folder.

    Args:
        dataset_file_folder (str): The dataset file folder.

    Returns:
        list of str: A list of fund codes.
    """
    if re.match(r'-\d{4}', dataset_file_folder):
        menu_code = pick_something_in_string(dataset_file_folder, something=r'\d{4}')
    else:
        menu_code = r'\d{4}'
    file_names = scan_files_including_regex(dataset_file_folder, regex=f'menu{menu_code}-code')
    fund_codes = [pick_something_in_string(file_name, something=r'-code.{6}')[5:] for file_name in file_names]
    return fund_codes

def pick_dates_in_file_folder(file_folder, regex, form="%Y%m%d"):
    """
    Picks the dates in a file folder based on the file names.

    Args:
        file_folder (str): The file folder.
        regex (str): The regex pattern to match.
        form (str): The date format.

    Returns:
        list of str: The dates in the file folder.
    """
    file_names = scan_files_including_regex(file_folder=file_folder, regex=regex)
    dates = [pick_input_date_in_file_name(file_name) for file_name in file_names]
    if form == "%Y%m%d":
        pass
    elif form == "%Y-%m-%d":
        dates = [f'{date[:4]}-{date[4:6]}-{date[6:]}' for date in dates]
    return dates

def pick_latest_date_in_file_folder(file_folder, regex, form="%Y%m%d"):
    """
    Picks the latest date in a file folder based on the file names.

    Args:
        file_folder (str): The file folder.
        regex (str): The regex pattern to match.
        form (str): The date format.

    Returns:
        str: The latest date in the file folder.
    """
    dates = pick_dates_in_file_folder(file_folder, regex, form)
    latest_date = dates[-1]
    return latest_date


def move_files(regex, folder_from, folder_to, option='copy'):
    """
    Moves or copies files matching a regex pattern from one folder to another.

    Args:
        regex (str): The regex pattern to match.
        folder_from (str): The source folder.
        folder_to (str): The destination folder.
        option (str): The operation to perform ('copy' or 'move').

    Returns:
        None
    """
    check_folder_and_create_folder(folder_to)
    filenames = scan_files_including_regex(file_folder=folder_from, regex=regex)
    for filename in filenames:
        file_path_from = os.path.join(folder_from, filename)
        file_path_to = os.path.join(folder_to, filename)
        if option == 'copy':
            shutil.copy(file_path_from, file_path_to)
            print(f"Copied: [{file_path_from}] -> [{file_path_to}]")
        elif option == 'move':
            shutil.move(file_path_from, file_path_to)
            print(f"Moved: [{file_path_from}] -> [{file_path_to}]")
        else:
            print("Invalid option. Please choose 'copy' or 'move'.")
            return


def change_to_numeric(x):
    if isinstance(x, str):
        if x == '-':
            return np.nan
        else:
            return float(x.replace(',', ''))
    else:
        return x


def compare_dataframes(df1, df2, key):
    """
    Compare two dataframes and return two dataframes:
    1. Rows where the key is duplicated in both df1 and df2.
    2. Rows where the key is only in df2 and not in df1.

    Args:
    df1 (pd.DataFrame): The first dataframe.
    df2 (pd.DataFrame): The second dataframe.
    key (str): The column name to compare.

    Returns:
    pd.DataFrame: DataFrame with duplicated rows based on the key.
    pd.DataFrame: DataFrame with rows only in df2 and not in df1.
    """
    # Merge df1 and df2 on the key column to find duplicates
    merged_df = pd.merge(df1, df2, on=key, how='inner')
    
    # Find rows in df2 that are not in df1
    unique_to_df2 = df2[~df2[key].isin(df1[key])]
    
    return merged_df, unique_to_df2



def update_df_time_series(df_old, df_new):
    """
    Merges two time series DataFrames.

    Args:
        df_old (pd.DataFrame): The old DataFrame.
        df_new (pd.DataFrame): The new DataFrame.

    Returns:
        pd.DataFrame: The merged DataFrame.
    """
    df_old.index = pd.to_datetime(df_old.index)
    df_new.index = pd.to_datetime(df_new.index)
    common_index = df_old.index.intersection(df_new.index)
    unique_to_old = df_old.index.difference(df_new.index)
    unique_to_new = df_new.index.difference(df_old.index)
    if not unique_to_old.empty and not pd.isna(unique_to_old).any():
        print(f"Unique dates in df_old not in df_new: {unique_to_old[0].strftime('%Y-%m-%d')} ~ {unique_to_old[-1].strftime('%Y-%m-%d')} (Total: {len(unique_to_old)} days)")
    if not unique_to_new.empty and not pd.isna(unique_to_new).any():
        print(f"Unique dates in df_new not in df_old: {unique_to_new[0].strftime('%Y-%m-%d')} ~ {unique_to_new[-1].strftime('%Y-%m-%d')} (Total: {len(unique_to_new)} days)")
    if set(common_index) == set(df_new.index):
        print("No update is needed. The new data is already included in the old data.")
        return df_new
    elif not common_index.empty:
        split_date = common_index.min()
        before_split = df_old[df_old.index < split_date]
        after_split = df_new[df_new.index >= split_date]
        df_merge = pd.concat([before_split, after_split])
    else:
        df_merge = pd.concat([df_old, df_new])
        df_merge = df_merge.sort_index()
    return df_merge

def update_timeseries_dataset_from_old_and_new_in_file_folder(file_folder, fund_code, menu_code=None, save=True):
    """
    Updates a time series dataset in a file folder by merging old and new data.

    Args:
        file_folder (str): The folder containing the datasets.
        fund_code (str): The fund code.
        menu_code (str, optional): The menu code. Defaults to None.
        save (bool): Whether to save the updated dataset. Defaults to True.

    Returns:
        pd.DataFrame: The updated dataset.
    """
    menu_code = pick_something_in_string(file_folder, something=r"\d{4}") if menu_code is None else menu_code
    file_paths = scan_files_including_regex(file_folder=f'dataset-{menu_code}', regex=fr'menu2160-code{fund_code}-to\d{{8}}', option='path')
    if len(file_paths) < 2:
        print("There is no old dataset to update.")
        return
    file_name_old = file_paths[-2]
    file_name_new = file_paths[-1]
    df_old = pd.read_csv(file_name_old, index_col=0)
    df_new = pd.read_csv(file_name_new, index_col=0)
    print(f"Compare two datasets:")
    print(f"old dataset: {file_name_old}")
    print(f"new dataset: {file_name_new}")
    df_update = update_df_time_series(df_old, df_new)
    if save:
        end_date = df_update.index[-1].strftime("%Y%m%d")
        file_folder = f'dataset-{menu_code}'
        file_name = f'menu{menu_code}-code{fund_code}-to{end_date}-save{get_today("%Y%m%d")}-updated.csv'
        file_path = os.path.join(file_folder, file_name)
        df_update.to_csv(file_path)
        print(f"Updated dataset saved: {file_name}")
    return df_update

def update_all_timeseries_datasets_in_file_folder(dataset_file_folder):
    """
    Updates all time series datasets in a file folder.

    Args:
        dataset_file_folder (str): The dataset file folder.

    Returns:
        None
    """
    for code in get_fund_codes_in_file_folder(dataset_file_folder):
        update_timeseries_dataset_from_old_and_new_in_file_folder(file_folder=dataset_file_folder, fund_code=code)
    return None

def find_new_elements(data_old, data_new):
    """
    Finds new or updated elements in two lists of dictionaries.

    Args:
        data_old (list): The old list of dictionaries.
        data_new (list): The new list of dictionaries.

    Returns:
        list: A list of new or updated dictionaries.
    """
    new_elements = []
    for datum_new in data_new:
        is_new_or_updated = True
        for datum_old in data_old:
            if all(datum_new.get(key) == datum_old.get(key) for key in set(datum_new.keys()) | set(datum_old.keys())):
                is_new_or_updated = False
                break
        if is_new_or_updated:
            new_elements.append(datum_new)
    return new_elements

def get_dct_from_a_row(df, index):
    """
    Returns a dictionary from a DataFrame row.

    Args:
        df (pd.DataFrame): The DataFrame.
        index (int): The row index.

    Returns:
        dict: A dictionary representing the row.
    """
    dct_from_row = df.iloc[index].to_dict()
    return dct_from_row

def export_json_from_dct(dct, file_folder, file_name):
    """
    Exports a dictionary to a JSON file.

    Args:
        dct (dict): The dictionary to export.
        file_folder (str): The folder to save the file in.
        file_name (str): The file name.

    Returns:
        None
    """
    file_path = os.path.join(file_folder, file_name)
    with open(file_path, 'w') as f:
        json.dump(dct, f, ensure_ascii=False)

def preprocess_timeseries(df, time_col_from, value_col_from, time_col_to, value_col_to):
    """
    Preprocesses a DataFrame for time series analysis.

    Args:
        df (pd.DataFrame): The DataFrame to preprocess.
        time_col_from (str): The original time column name.
        value_col_from (str): The original value column name.
        time_col_to (str): The new time column name.
        value_col_to (str): The new value column name.

    Returns:
        pd.DataFrame: The preprocessed DataFrame.
    """
    print('step 1: drop NaN')
    df = df[[time_col_from, value_col_from]].dropna()
    print('step 2: rename columns to date and price')
    df = df.rename(columns={time_col_from: time_col_to, value_col_from: value_col_to})
    print('step 3: reset index')
    df = df.reset_index(drop=True)
    df = df.copy()
    try:
        print('step 4: convert value to float type')
        df[value_col_to] = df[value_col_to].str.replace(',', '').astype(float)
    except Exception as e:
        print(e)
    return df

def preprocess_timeseries_for_single_column(df, date_col_name, price_col_name):
    """
    Preprocesses a DataFrame for time series analysis with a single value column.

    Args:
        df (pd.DataFrame): The DataFrame to preprocess.
        date_col_name (str): The original date column name.
        price_col_name (str): The original price column name.

    Returns:
        pd.DataFrame: The preprocessed DataFrame.
    """
    df = preprocess_timeseries(df=df, time_col_from=date_col_name, value_col_from=price_col_name, time_col_to='date', value_col_to='price')
    return df

def preprocess_timeseries_for_multi_columns(df, time_col_from, value_cols_from, time_col_to, value_cols_to):
    """
    Preprocesses a DataFrame for time series analysis with multiple value columns.

    Args:
        df (pd.DataFrame): The DataFrame to preprocess.
        time_col_from (str): The original time column name.
        value_cols_from (list): The original value column names.
        time_col_to (str): The new time column name.
        value_cols_to (list): The new value column names.

    Returns:
        pd.DataFrame: The preprocessed DataFrame.
    """
    print('step 1: drop NaN')
    df = df[[time_col_from, *value_cols_from]].dropna()
    print('step 2: rename columns to date and price')
    df.columns = [time_col_to, *value_cols_to]
    print('step 3: reset index')
    df = df.reset_index(drop=True)
    df = df.copy()
    try:
        print('step 4: convert value to float type')
        for col in value_cols_to:
            df[col] = df[col].str.replace(',', '').astype(float)
    except Exception as e:
        print(e)
    return df

def preprocess_to_extract_timeseries_price_in_menu2160(df_menu2160):
    """
    Preprocesses a DataFrame to extract time series price data from menu 2160.

    Args:
        df_menu2160 (pd.DataFrame): The original DataFrame.

    Returns:
        pd.DataFrame: The preprocessed DataFrame with date and price columns.
    """
    df = preprocess_timeseries_for_single_column(df=df_menu2160, date_col_name='일자', price_col_name='수정\n기준가')
    return df

def preprocess_to_extract_timeseries_price_in_menu2160(df_menu2160):
    """
    Preprocesses a DataFrame to extract time series asset data from menu 2160.

    Args:
        df_menu2160 (pd.DataFrame): The original DataFrame.

    Returns:
        pd.DataFrame: The preprocessed DataFrame with date and asset columns.
    """
    df = preprocess_timeseries(df_menu2160, time_col_from='일자', value_col_from='순자산총액', time_col_to='date', value_col_to='asset')
    return df

def preprocess_timeseries_of_menu2160_for_multi_columns(df_menu2160):
    """
    Preprocesses a DataFrame to extract multiple time series data columns from menu 2160.

    Args:
        df_menu2160 (pd.DataFrame): The original DataFrame.

    Returns:
        pd.DataFrame: The preprocessed DataFrame with date, price, and asset columns.
    """
    df = preprocess_timeseries_for_multi_columns(df_menu2160, time_col_from='일자', value_cols_from=['수정\n기준가', '순자산총액'], time_col_to='date', value_cols_to=['price', 'asset'])
    return df

def print_tree(startpath, indent=""):
    """
    Prints the directory tree starting from a given path.

    Args:
        startpath (str): The starting path.
        indent (str): The indentation string.

    Returns:
        None
    """
    for item in os.listdir(startpath):
        path = os.path.join(startpath, item)
        if os.path.isdir(path):
            print(indent + "├── " + item + "/")
            print_tree(path, indent + "│   ")
        else:
            print(indent + "├── " + item)


def save_dataset_of_subject_at(df, file_folder, subject, input_date):
    file_name = f'dataset-{subject}-at{input_date.replace("-","")}-save{get_today("%Y%m%d%H")}.csv'
    file_path = os.path.join(file_folder, file_name)
    df.to_csv(file_path)
    print(f'- save complete: {file_path}')
    return df

def save_dataset_of_subject_from_to(df, file_folder, subject, start_date, end_date):
    file_name = f'dataset-{subject}-from{start_date.replace("-","")}-to{end_date.replace("-","")}-save{get_today("%Y%m%d%H")}.csv'
    file_path = os.path.join(file_folder, file_name)
    df.to_csv(file_path)
    print(f'- save complete: {file_path}')
    return df
