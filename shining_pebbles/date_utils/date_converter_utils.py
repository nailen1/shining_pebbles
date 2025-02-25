def transform_date_str_to_date_str_dashed(date):
    date_dashed = f'{date[:4]}-{date[4:6]}-{date[6:8]}'
    return date_dashed

def transform_date_str_dashed_to_date_str(date):
    return date.replace('-', '')