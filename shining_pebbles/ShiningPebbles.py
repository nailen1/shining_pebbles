### version
### 2024-02-28-09:21
### 2024-05-31


import pandas as pd
import json
import os
import re
import time
import calendar
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import shutil


def test(func):
    start_time = time.time()  # 함수 실행 전 시간 측정
    result = func  # 함수 실행
    end_time = time.time()  # 함수 실행 후 시간 측정
    duration = end_time - start_time  # 실행 시간 계산
    print(f"Function execution took {duration:.9f} seconds.")  # 소수점 둘째자리까지 출력
    return result  # 함수의 결과 반환

### 날짜 관련 함수
def get_today(form="%Y-%m-%d"):
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

def get_date_n_days_ago(date, n, form='%Y-%m-%d'):
    date = date.replace('-', '')
    date_dt = datetime.strptime(date, '%Y%m%d')
    date_before_n_dt = date_dt - timedelta(days=n)
    date_before_n_str = date_before_n_dt.strftime(form)
    return date_before_n_str

def get_yesterday(form="%Y-%m-%d"):
    today = get_today(form)
    yesterday = get_date_n_days_ago(today, 1, form)
    return yesterday

def get_date_n_weeks_ago(date, n, form="%Y-%m-%d"):
    date = date.replace("-", "")
    date_dt = datetime.strptime(date, "%Y%m%d")
    date_before_n_dt = date_dt - timedelta(weeks=n)
    date_before_n_str = date_before_n_dt.strftime(form)
    return date_before_n_str

def is_the_last_date_of_month(date):
    if isinstance(date, str):
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    elif isinstance(date, datetime):
        date_obj = date
    else:
        raise ValueError("Input must be a string in 'YYYY-MM-DD' format or a datetime object")
    
    next_month = date_obj + relativedelta(months=1)
    last_day_of_month = next_month.replace(day=1) - relativedelta(days=1)
    
    # 주어진 날짜가 해당 월의 마지막 날짜인지 확인
    return date_obj.day == last_day_of_month.day

def get_date_n_month_ago(date, n, form="%Y-%m-%d"):
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


def get_last_day_of_month(year, month):
    year_input = int(year)
    month_input = int(month)
    # monthrange 함수로 해당 월의 일수를 가져옵니다
    _, last_day = calendar.monthrange(year_input, month_input)
    return f"{year_input}-{month_input:02d}-{last_day}"


def get_weekday(date, language='EN'):
    year = int(date.split('-')[0])
    month = int(date.split('-')[1])
    day = int(date.split('-')[2])

    # weekday 함수는 해당 날짜의 요일을 반환합니다 (0 = 월요일, 6 = 일요일).
    day_index = calendar.weekday(year, month, day)
    mapping = {
        'EN-full': ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        'EN': ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        'KR-full': ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"],
        'KR': ["월", "화", "수", "목", "금", "토", "일"],
    }
    weekday = mapping[language][day_index]
    return weekday


def calculate_prior_date_extended(base_date, days=0, months=0, years=0):
    """
    주어진 날짜로부터 n일/월/년 전의 날짜를 계산합니다.

    :param base_date: 기준 날짜 (문자열 형식: 'YYYY-MM-DD')
    :param kwargs: day, month, year 키워드 인자를 통해 이전으로 계산할 일/월/년 수
    :return: 계산된 이전 날짜 (문자열 형식: 'YYYY-MM-DD')
    """
    date_format = "%Y-%m-%d"
    base_date_obj = datetime.strptime(base_date, date_format)

    # years와 months를 처리하기 위해 relativedelta를 사용
    prior_date_obj = base_date_obj - relativedelta(
        days=days, months=months, years=years
    )
    return prior_date_obj.strftime(date_format)

def rename_key(d, old_key, new_key):
    if old_key in d:
        d[new_key] = d.pop(old_key)
    else:
        print(f"Key '{old_key}' not found in the dictionary.")


#  large scale file system control functions

def scan_files_including_regex(file_folder, regex, option="name"):
    with os.scandir(file_folder) as files:
        lst = [file.name for file in files if re.findall(regex, file.name)]

    mapping = {
        "name": lst,
        "path": [os.path.join(file_folder, file_name) for file_name in lst],
    }
    lst_ordered = sorted(mapping[option])
    return lst_ordered

def open_df_in_file_folder_by_regex(file_folder, regex, option="path", index_col=0):
    latest_file_path = scan_files_including_regex(file_folder, regex, option)[-1]
    df = pd.read_csv(latest_file_path, index_col=index_col)
    return df

def open_json_in_file_folder_by_regex(file_folder, regex, option="path", index=-1):
    latest_file_path = scan_files_including_regex(file_folder, regex, option)[index]
    with open(latest_file_path, 'r', encoding='utf-8') as file:
        dct = json.load(file)
    return dct

def get_last_key_and_value_in_json_file(dct):
    last_key = next(reversed(dct))
    last_value = dct[last_key]
    return last_key, last_value

def format_date(date, form="yyyymmdd"):
    date = date.replace("-", "")
    date_dashed = datetime.strptime(date, "%Y%m%d").strftime("%Y-%m-%d")
    mapping = {"yyyymmdd": date, "yyyy-mm-dd": date_dashed}
    return mapping.get(form, date_dashed)


def save_df_to_file(
    df,
    file_folder,
    file_name_var,
    file_extension=".csv",
    archive=False,
    file_folder_archive="./archive",
):
    def get_today(form="%Y%m%d"):
        return datetime.now().strftime(form)

    try:
        save_time = get_today()
        file_name = f"dataset-{file_name_var}-save{save_time}"+file_extension
        file_path = os.path.join(file_folder, file_name)
        if os.path.exists(file_path) and archive:
            df_archive = pd.read_csv(file_path)
            os.makedirs(file_folder_archive, exist_ok=True)
            archive_file_name = "archive-" + file_name
            archive_file_path = os.path.join(file_folder_archive, archive_file_name)
            df_archive.to_csv(archive_file_path, index=False)
            print(f"Archived: {archive_file_path}")
        df.to_csv(file_path, index=False)
        print(f"- Saved: {file_path}")
    except Exception as e:
        print(f"- Error: {e}")

def check_folder_and_create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"- create: {folder_name}")
    else:
        print(f"- already exist: {folder_name}")
    return folder_name

def save_dataset_as_csv(df, file_folder, file_name_description):
    file_folder = file_folder
    file_name = file_name_description + ".csv"
    file_path = os.path.join(file_folder, file_name)
    df.to_csv(file_path)

def quarter_string_to_date(quarter_string):
    """
    Convert a quarter string (e.g., '2021 Q1') to a datetime object representing
    the first day of the corresponding quarter.

    Parameters:
    quarter_string (str): A string representing a quarter, formatted as 'YYYY QX'.

    Returns:
    datetime: A datetime object representing the first day of the quarter.
    """
    year, q = quarter_string.split(' ')
    year = int(year)
    quarter = int(q.replace('Q', '').strip())
    
    # 분기와 해당 분기의 첫 달을 매핑하는 딕셔너리
    quarter_to_month = {1: 1, 2: 4, 3: 7, 4: 10}
    
    # 딕셔너리를 사용하여 분기에 해당하는 월 결정
    month = quarter_to_month[quarter]
    
    # 해당 분기의 첫 날짜로 datetime 객체 생성
    return pd.Timestamp(year=year, month=month, day=1)

def year_string_to_date(year_string):
    """
    Convert a quarter string (e.g., '2021 Q1') to a datetime object representing
    the first day of the corresponding quarter.

    Parameters:
    quarter_string (str): A string representing a quarter, formatted as 'YYYY QX'.

    Returns:
    datetime: A datetime object representing the first day of the quarter.
    """
    year = f'{year_string}-01-01'    
    
    # 해당 분기의 첫 날짜로 datetime 객체 생성
    return pd.Timestamp(year=year, month=1, day=15)


def fill_all_dates_from_start_to_end(start_date, end_date):
    """
    start_date와 end_date 사이의 모든 날짜를 포함하는 날짜 범위를 생성합니다.

    :param start_date: 시작 날짜 (문자열 형식: 'YYYY-MM-DD')
    :param end_date: 끝 날짜 (문자열 형식: 'YYYY-MM-DD')
    :return: 시작 날짜와 끝 날짜 사이의 모든 날짜를 포함하는 리스트
    """
    date_range = pd.date_range(start=start_date, end=end_date)
    return date_range.strftime("%Y-%m-%d").tolist()


def fill_all_first_days_of_months(start_date, end_date):
    """
    start_date와 end_date 사이의 각 달의 첫째 날만 포함하는 날짜 범위를 생성합니다.

    :param start_date: 시작 날짜 (문자열 형식: 'YYYY-MM-DD')
    :param end_date: 끝 날짜 (문자열 형식: 'YYYY-MM-DD')
    :return: 시작 날짜와 끝 날짜 사이의 각 달의 첫째 날만을 포함하는 리스트
    """
    date_range = pd.date_range(start=start_date, end=end_date)
    first_days = [date for date in date_range if date.day == 1]
    # 각 Timestamp 객체를 문자열로 변환
    return [date.strftime("%Y-%m-%d") for date in first_days]


def get_last_day_of_previous_month(input_date_str):
    input_date = datetime.strptime(input_date_str, '%Y-%m-%d')    
    first_day_of_current_month = input_date.replace(day=1)    
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)    
    return last_day_of_previous_month.strftime('%Y-%m-%d')


def get_quarters(start_year, end_year):
    quarters = []
    for year in range(start_year, end_year - 1, -1):
        for quarter in ['4Q', '3Q', '2Q', '1Q']:
            quarters.append(f'{year} {quarter}')
    return quarters


def pick_something_in_string(string, something):
    return re.search(pattern=something, string=string).group()


def pick_n_characters_followed_by_something_in_string(string, something, n):
    # regex pattern to find 'something' followed by n word characters
    regex = re.escape(something) + fr'(\w{{{n}}})'
    print(f'input regex: {regex}')
    match = re.search(pattern=regex, string=string)
    if match:
        return match.group(1)
    else:
        return None

def pick_menu_code_in_file_name(file_name):
    return pick_n_characters_followed_by_something_in_string(file_name, something='menu', n=4)

def pick_code_in_file_name(file_name):
    return pick_n_characters_followed_by_something_in_string(file_name, something='code', n=6)

def pick_input_date_in_file_name(file_name):
    return pick_n_characters_followed_by_something_in_string(file_name, something='at', n=8)

def pick_start_date_in_file_name(file_name):
    return pick_n_characters_followed_by_something_in_string(file_name, something='from', n=8)

def pick_end_date_in_file_name(file_name):
    return pick_n_characters_followed_by_something_in_string(file_name, something='to', n=8)

def pick_save_date_in_file_name(file_name):
    return pick_n_characters_followed_by_something_in_string(file_name, something='save', n=8)

def get_fund_codes_in_file_folder(dataset_file_folder):
    if re.match(r'-\d{4}', dataset_file_folder):
        menu_code = pick_something_in_string(dataset_file_folder, something=r'\d{4}')
    else:
        menu_code = r'\d{4}'
    file_names = scan_files_including_regex(dataset_file_folder, regex=f'menu{menu_code}-code')
    fund_codes = [pick_something_in_string(file_name, something=r'-code.{6}')[5:] for file_name in file_names]
    return fund_codes

def move_files(regex, folder_from, folder_to, option='copy'):
    check_folder_and_create_folder(folder_to)
    filenames = scan_files_including_regex(file_folder=folder_from, regex=regex)
    for filename in filenames:
        file_path_from = os.path.join(folder_from, filename)
        file_path_to = os.path.join(folder_to, filename)
        if option == 'copy':
            shutil.copy(file_path_from, file_path_to)
            print(f"- Copied: [{file_path_from}] -> [{file_path_to}]")
        elif option == 'move':
            shutil.move(file_path_from, file_path_to)
            print(f"- Moved: [{file_path_from}] -> [{file_path_to}]")
        else:
            print("Invalid option. Please choose 'copy' or 'move'.")
            return
        
# move this to DownloadAutomation.py
def update_df_time_series(df_old, df_new):
    """
    두 시계열 데이터프레임을 통합하는 개선된 함수입니다.
    
    Args:
    - df_old (pd.DataFrame): 과거 데이터가 담긴 데이터프레임.
    - df_new (pd.DataFrame): 현재 또는 미래 데이터가 담긴 데이터프레임.
    
    Returns:
    - pd.DataFrame: 통합된 시계열 데이터프레임.
    """
    df_old.index = pd.to_datetime(df_old.index)
    df_new.index = pd.to_datetime(df_new.index)
    common_index = df_old.index.intersection(df_new.index)
    unique_to_old = df_old.index.difference(df_new.index)
    unique_to_new = df_new.index.difference(df_old.index)    
    if not unique_to_old.empty and not pd.isna(unique_to_old).any():
        print(f"- Unique dates in df_old not in df_new: {unique_to_old[0].strftime('%Y-%m-%d')} ~ {unique_to_old[-1].strftime('%Y-%m-%d')} (Total: {len(unique_to_old)} days)")
    if not unique_to_new.empty and not pd.isna(unique_to_new).any():
        print(f"- Unique dates in df_new not in df_old: {unique_to_new[0].strftime('%Y-%m-%d')} ~ {unique_to_new[-1].strftime('%Y-%m-%d')} (Total: {len(unique_to_new)} days)")    

    if set(common_index) == set(df_new.index):
        print("- No update is needed. The new data is already included in the old data.")
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

# move this to DownloadAutomation.py
def update_timeseries_dataset_from_old_and_new_in_file_folder(file_folder, fund_code, menu_code=None, save=True):
    menu_code = pick_something_in_string(file_folder, something=r"\d{4}") if menu_code is None else menu_code
    file_paths = scan_files_including_regex(file_folder=f'dataset-{menu_code}', regex=fr'menu2160-code{fund_code}-to\d{{8}}', option='path')
    print(file_paths)
    if len(file_paths) < 2:
        print("- There is no old dataset to update.")
        return
    file_name_old = file_paths[-2]
    file_name_new = file_paths[-1]
    df_old = pd.read_csv(file_name_old, index_col=0)
    df_new = pd.read_csv(file_name_new, index_col=0)
    print(f"- Compare two datasets:")
    print(f"-- old dataset: {file_name_old}")
    print(f"-- new dataset: {file_name_new}")
    df_update = update_df_time_series(df_old, df_new)
    if save:
        end_date = df_update.index[-1].strftime("%Y%m%d")
        file_folder = f'dataset-{menu_code}'
        file_name = f'menu{menu_code}-code{fund_code}-to{end_date}-save{get_today("%Y%m%d")}-updated.csv'
        file_path = os.path.join(file_folder, file_name)
        df_update.to_csv(file_path)
        print(f"- updated dataset saved: {file_name}")
    return df_update

def update_all_timeseries_datasets_in_file_folder(dataset_file_folder):
    for code in get_fund_codes_in_file_folder(dataset_file_folder):
        update_timeseries_dataset_from_old_and_new_in_file_folder(file_folder=dataset_file_folder, fund_code=code)
    return None


def find_new_elements(data_old, data_new):
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


### JSON Functions

def export_json_from_dct(dct, file_folder, file_name):
    file_path = os.path.join(file_folder, file_name)
    with open(file_path, 'w') as f:
        json.dump(dct, f, ensure_ascii=False)


### TIMESERIES FUNCTIONS
### GENERATE A STANDARD TIMESERIES DATASET 
def preprocess_timeseries(df, time_col_from, value_col_from, time_col_to, value_col_to):
    print('-step 1: drop NaN')
    df = df[[time_col_from, value_col_from]].dropna()
    print('-step 2: rename columns to date and price')
    df = df.rename(columns={time_col_from: time_col_to, value_col_from: value_col_to})
    print('-step 3: reset index')
    df = df.reset_index(drop=True)
    df = df.copy()
    try:
        print('-step 4: convert value to float type')
        df[value_col_to] = df[value_col_to].str.replace(',', '').astype(float)
    except Exception as e:
        print(e)
    return df


def preprocess_timeseries_for_single_column(df, date_col_name, price_col_name):
    df = preprocess_timeseries(df=df, time_col_from=date_col_name, value_col_from=price_col_name, time_col_to='date', value_col_to='price')
    return df


def preprocess_timeseries_for_multi_columns(df, time_col_from, value_cols_from, time_col_to, value_cols_to):
    print('-step 1: drop NaN')
    df = df[[time_col_from, *value_cols_from]].dropna()
    print('-step 2: rename columns to date and price')
    df.columns = [time_col_to, *value_cols_to]
    print('-step 3: reset index')
    df = df.reset_index(drop=True)
    df = df.copy()
    try:
        print('-step 4: convert value to float type')
        for col in value_cols_to:
            df[col] = df[col].str.replace(',', '').astype(float)
    except Exception as e:
        print(e)
    return df


## APPLICATION: FOR KB FUND SYSTEM>MOS>2160 FUND DATASETS 
def preprocess_to_extract_timeseries_price_in_menu2160(df_menu2160):
    df = preprocess_timeseries_for_single_column(df=df_menu2160, date_col_name='일자', price_col_name='수정\n기준가')
    return df

def preprocess_to_extract_timeseries_price_in_menu2160(df_menu2160):
    df = preprocess_timeseries(df_menu2160, time_col_from='일자', value_col_from='순자산총액', time_col_to='date', value_col_to='asset')
    return df

def preprocess_timeseries_of_menu2160_for_multi_columns(df_menu2160):
    df = preprocess_timeseries_for_multi_columns(df_menu2160, time_col_from='일자', value_cols_from=['수정\n기준가', '순자산총액'], time_col_to='date', value_cols_to=['price', 'asset'])
    return df


