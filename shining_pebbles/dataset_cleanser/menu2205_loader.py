from .path_director import file_folder
from shining_pebbles import open_df_in_file_folder_by_regex
from aws_s3_controller import open_df_in_bucket_by_regex

def open_df_menu2205_snapshot(date_ref=None, data_source='local'):
    regex = f'menu2205-code000000-at{date_ref.replace("-", "")}' if date_ref else 'menu2205-code000000-at'
    if data_source == 'local':
        df = open_df_in_file_folder_by_regex(file_folder=file_folder['menu2205-snapshot'], regex=regex).reset_index().rename(columns={'index': 'Unnamed: 0'})
    elif data_source in ['aws', 's3', 'bucket']:
        df = open_df_in_bucket_by_regex(bucket='dataset-system', bucket_prefix='dataset-menu2205-snapshot', regex=regex)
    return df

def open_df_menu2205(fund_code, date_ref=None, from_local=True):
    regex = f'menu2205-code{fund_code}-at{date_ref.replace("-", "")}' if date_ref else f'menu2205-code{fund_code}-at'
    if from_local:
        df = open_df_in_file_folder_by_regex(file_folder=file_folder['menu2205'], regex=regex)
    else:
        df = open_df_in_bucket_by_regex(bucket='dataset-system', bucket_prefix='dataset-menu2205', regex=regex)
    return df