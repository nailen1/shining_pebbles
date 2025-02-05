from .menu2205_loader import open_df_menu2205_snapshot, open_df_menu2205
from .menu2205_cleanser import *
from .menu2205_consts import ASSET_CATEGORIES
from .menu2205_exceptions import MAPPING_NAMES_TO_CORPNAMES_FOR_EXCEPTIONS

def get_preprocessed_df_menu2205_snapshot(date_ref=None, data_source='local'):
    return preprocess_menu2205(open_df_menu2205_snapshot(date_ref=date_ref, data_source=data_source))

def get_df_menu2205(fund_code, date_ref=None, from_local=True):
    return preprocess_menu2205(open_df_menu2205(fund_code=fund_code, date_ref=date_ref, from_local=from_local))

def get_df_asset_menu2205_snapshot(date_ref=None, data_source='local'):
    menu2205 = get_preprocessed_df_menu2205_snapshot(date_ref=date_ref, data_source=data_source)
    df = {category: menu2205[menu2205['자산']==category] for category in ASSET_CATEGORIES}
    return df

def get_df_asset_menu2205(fund_code, date_ref=None):
    menu2205 = get_df_menu2205(fund_code=fund_code, date_ref=date_ref)
    df = {category: menu2205[menu2205['자산']==category] for category in ASSET_CATEGORIES}
    return df

def get_df_stock_snapshot(date_ref=None):
    df = get_df_asset_menu2205_snapshot(date_ref=date_ref)[ASSET_CATEGORIES[0]]
    df = df.reset_index(drop=True)
    return df

def get_df_stock(fund_code, date_ref=None):
    df = get_df_asset_menu2205(fund_code=fund_code, date_ref=date_ref)
    df = df.reset_index(drop=True)
    return df


def get_mapping_tickers_to_names():
    stocks = get_df_stock_snapshot().iloc[:-1]
    stocks['ticker'] = stocks['종목'].apply(lambda x: x[3:-3])
    cols_to_keep = ['ticker', '종목명']
    stocks = stocks[cols_to_keep].rename(columns={'종목명': 'name'})
    mapping_tickers_to_names = stocks.set_index('ticker').to_dict()['name']
    return mapping_tickers_to_names

def get_mapping_names_to_corpnames():
    stocks = get_df_stock_snapshot().iloc[:-1]
    cols_to_keep = ['종목명', '종목정보: 발행기관',]
    stocks = stocks[cols_to_keep].rename(columns={'종목명': 'name', '종목정보: 발행기관': 'corpname'})
    mapping_names_to_corpnames = stocks.set_index('name').to_dict()['corpname']
    return mapping_names_to_corpnames

def get_df_ticker_name_corpname(date_ref=None, exceptions=True):
    df = get_df_stock_snapshot(date_ref=date_ref).iloc[:-1]
    df['ticker'] = df['종목'].apply(lambda x: x[3:-3])
    cols_to_keep = ['ticker', '종목명', '종목정보: 발행기관']
    df = df[cols_to_keep].rename(columns={'종목명': 'name', '종목정보: 발행기관': 'corpname'})
    if exceptions:
        df = apply_exceptions_to_df_ticker_name_corpname(df)
    return df

def apply_exceptions_to_df_ticker_name_corpname(df):
    for name, corpname in MAPPING_NAMES_TO_CORPNAMES_FOR_EXCEPTIONS.items():
        df.loc[df['name']==name, 'hotfix'] = corpname
    return df
