import datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
from typing import List, Tuple


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

