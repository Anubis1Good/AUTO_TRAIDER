import os
from time import time
import requests
import apimoex
import pandas as pd

def download_moex(ticker,interval,start,end=None,board: str = "TQBR",market:str="shares", engine:str = "stock"):
    """K-line particle size
        1 - 1 минута
        10 - 10 минут
        60 - 1 час
        24 - 1 день
        7 - 1 неделя
        31 - 1 месяц
        4 - 1 квартал
    """
    with requests.Session() as session:
        data = apimoex.get_board_candles(session, ticker,interval,start,end,board=board,market=market,engine=engine)
        df = pd.DataFrame(data)

        return df
    
def create_df(df:pd.DataFrame):
    df = df.rename(columns={'value':"vol_coin",'begin':'ms'})
    df['direction'] = df.apply(lambda row: 1 if row['open'] < row['close'] else -1, axis=1)
    df['middle'] = df.apply(lambda row: (row['high']+row['low'])/2,axis=1)
    df = df.reset_index()
    df['x'] = df.index
    df = df.drop(['index'],axis=1)
    return df

def save_df(ticker,interval,start,end=None,board: str = "TQBR",market:str="shares", engine:str = "stock"):
    """K-line particle size
        1 - 1 минута
        10 - 10 минут
        60 - 1 час
        24 - 1 день
        7 - 1 неделя
        31 - 1 месяц
        4 - 1 квартал
    """
    df = download_moex(ticker,interval,start,end,board,market,engine)
    df = create_df(df)
    path = os.path.join('DataForTests/DataFromMOEX',ticker+"_"+str(interval)+'_'+str(time()).split(".")[0]+'.csv')
    df.to_csv(path)

def convert_chart1to5(df):
    # Преобразуем столбец 'ms' в datetime
    df['ms'] = pd.to_datetime(df['ms'])

    # Устанавливаем 'ms' в качестве индекса
    df.set_index('ms', inplace=True)

    # Агрегируем данные по пятиминутным интервалам
    df_5min = df.resample('5min').agg({
        'open': 'first',        # Первое значение 'open' в интервале
        'close': 'last',        # Последнее значение 'close' в интервале
        'high': 'max',          # Максимальное значение 'high' в интервале
        'low': 'min',           # Минимальное значение 'low' в интервале
        'vol_coin': 'sum',      # Сумма 'vol_coin' в интервале
        'volume': 'sum',        # Сумма 'volume' в интервале
        'direction': 'last',    # Последнее значение 'direction' в интервале
        'middle': 'last',       # Последнее значение 'middle' в интервале
        'x': 'last'             # Последнее значение 'x' в интервале
    }).dropna()
    df_5min['direction'] = (df_5min['open'] - df_5min['close']).apply(lambda x: 1 if x <= 0 else -1)
    df_5min['middle'] = (df_5min['high'] + df_5min['low']) / 2
    # Сбрасываем индекс, чтобы 'ms' снова стал столбцом
    df_5min.reset_index(inplace=True)
    df_5min['x'] = df_5min.index
    return df_5min

