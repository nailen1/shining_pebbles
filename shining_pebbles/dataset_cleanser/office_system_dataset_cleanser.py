import pandas as pd

def eliminate_unnamed_in_col(col):
    col = col if 'Unnamed' not in col else None
    return col

def combine_col_prefix_suffix(row, conjunction=None):
    conjunction = ':' if conjunction is None else conjunction
    return f"{row['col_prefix']}{conjunction} {row['col_suffix']}" if row['col_prefix'] is not None else row['col_suffix']

def get_df_col_preprocessed(df):
    cols_raw = df.columns
    cols_in_row1 = df.iloc[0].tolist()
    dct = {
        'col_raw': cols_raw,
        'col_in_row1': cols_in_row1
    }
    df_cols = pd.DataFrame(dct)
    df_cols['col_prefix'] = df_cols['col_raw'].map(eliminate_unnamed_in_col).ffill()
    df_cols['col_suffix'] = df_cols['col_in_row1']
    df_cols['col_preprocessed'] = df_cols.apply(lambda row: combine_col_prefix_suffix(row), axis=1)
    return df_cols

def preprocess_columns_in_multi_columned_df(df):
    df_cols = get_df_col_preprocessed(df)
    cols_preprocessed = [col for col in df_cols['col_preprocessed'].tolist() if col is not None]
    return cols_preprocessed

def classify_category_in_multi_columned_df(df):
    df_cols = get_df_col_preprocessed(df)
    cols_category = df_cols['col_prefix'].unique().tolist()
    return cols_category

def preprocess_multi_columned_df(df):
    df = df.copy()
    cols_preprocessed = preprocess_columns_in_multi_columned_df(df)
    df.columns = cols_preprocessed
    df = df.drop([0])
    return df