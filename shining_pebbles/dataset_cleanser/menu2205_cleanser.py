from .office_system_dataset_cleanser import preprocess_multi_columned_df

def preprocess_menu2205(df):
    df = preprocess_multi_columned_df(df)
    return df