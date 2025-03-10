import pandas as pd
import numpy as np
def _help_donchan_channel(row,period,df,point):
    if point == 1:
        if row.name < period:
            return -1
        return int(df.iloc[row.name-period:row.name+1]['yh'].min())
    if point == -1:
        if row.name < period:
            return -1
        return int(df.iloc[row.name-period:row.name+1]['yl'].max())
    

def get_df_donchan_channel(df:pd.DataFrame,period:int=20):
    df['up_dc'] = df.apply(lambda row: _help_donchan_channel(row,period,df,1),axis=1)
    df['down_dc'] = df.apply(lambda row: _help_donchan_channel(row,period,df,-1),axis=1)
    # df.info()
    df['middle_dc'] = df.apply(lambda row: (row['up_dc']+row['down_dc'])//2,axis=1)
    return df

def add_slice_df(df:pd.DataFrame,period=20):
    df_slice  = df.iloc[period+1:]
    df_slice = df_slice.reset_index(drop=True)
    return df_slice

def get_vodka_channel(row,df:pd.DataFrame,period=20):
    if row.name < period:
        return np.array([-1,-1,-1])
    df_short = df.iloc[row.name-period:row.name+1]
    max_hb = int(df_short['high'].median())
    min_hb = int(df_short['low'].median())
    avarage = (min_hb + max_hb)//2

    return np.array([max_hb,min_hb,avarage])

def add_vodka_channel(df:pd.DataFrame,period=20):
    '''add top_mean, bottom_mean, avarege_mean'''
    points = df.apply(lambda row: get_vodka_channel(row,df,period),axis=1)
    points = np.stack(points.values)
    df['top_mean'] = pd.Series(points[:,0])
    df['bottom_mean'] = pd.Series(points[:,1])
    df['avarege_mean'] = pd.Series(points[:,2])
    return df

def get_donchan_channel(row,df:pd.DataFrame,period=20):
    if row.name < period:
        return np.array([-1,-1,-1])
    df_short = df.iloc[row.name-period:row.name+1]
    max_hb = df_short['high'].min()
    min_hb = df_short['low'].max()
    avarage = (min_hb + max_hb)//2

    return np.array([max_hb,min_hb,avarage])

def add_donchan_channel(df:pd.DataFrame,period=20):
    '''add max_hb, min_hb, avarege'''
    points = df.apply(lambda row: get_donchan_channel(row,df,period),axis=1)
    points = np.stack(points.values)
    df['max_hb'] = pd.Series(points[:,0])
    df['min_hb'] = pd.Series(points[:,1])
    df['avarege'] = pd.Series(points[:,2])
    return df

def add_rsi(df, period=14,kind='middle'):
    """
    add 'rsi'\n
    Вычисляет RSI для DataFrame с данными о ценах.
    
    :param data: DataFrame с колонкой 'Close' (цены закрытия)
    :param period: Период RSI (по умолчанию 14)
    :return: DataFrame с добавленной колонкой 'RSI'
    """
    # Вычисляем изменение цены
    delta = df[kind].diff()
    
    # Разделяем на рост и падение
    gain = (delta.where(delta < 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta > 0, 0)).rolling(window=period).mean()
    
    # Вычисляем относительную силу (RS)
    rs = gain / loss
    
    # Вычисляем RSI
    df['rsi'] = 100 - (100 / (1 + rs))
    df['rsi'] = df['rsi'].apply(lambda v: int(v) if not pd.isnull(v) else -1)
    
    return df

def get_bollinger(row,df:pd.DataFrame,period=20,kind='middle',multiplier=2):
    if row.name < period:
        return np.array([-1,-1,-1])
    df_short = df.iloc[row.name-period:row.name+1]
    std = int(df_short[kind].std())
    sma = int(df_short[kind].mean())
    bbu = sma - std*multiplier
    bbd = sma + std*multiplier

    return np.array([bbu,bbd,sma])

def add_bollinger(df:pd.DataFrame,period=20,kind='middle',multiplier=2):
    '''add bbu, bbd, sma'''
    points = df.apply(lambda row: get_bollinger(row,df,period,kind,multiplier),axis=1)
    points = np.stack(points.values)
    df['bbu'] = pd.Series(points[:,0])
    df['bbd'] = pd.Series(points[:,1])
    df['sma'] = pd.Series(points[:,2])
    return df