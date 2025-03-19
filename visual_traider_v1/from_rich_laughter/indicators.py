import pandas as pd
import numpy as np

def add_slice_df(df:pd.DataFrame,period=20):
    df_slice  = df.iloc[period+1:]
    df_slice = df_slice.reset_index(drop=True)
    return df_slice

def add_enter_price(df:pd.DataFrame,func):
    """add 'long_price','short_price','close_long_price','close_short_price'"""
    points = df.apply(lambda row: func(row),axis=1)
    points = np.stack(points.values)
    df['long_price'] = pd.Series(points[:,0])
    df['short_price'] = pd.Series(points[:,1])
    df['close_long_price'] = pd.Series(points[:,2])
    df['close_short_price'] = pd.Series(points[:,3])
    return df

def add_enter_price2close(df:pd.DataFrame):
    """add 'long_price','short_price','close_long_price','close_short_price'"""
    df['long_price'] = df['close']
    df['short_price'] = df['close']
    df['close_long_price'] = df['close']
    df['close_short_price'] = df['close']
    return df


def get_vodka_channel(row,df:pd.DataFrame,period=20):
    if row.name < period:
        return np.array([-1,-1,-1])
    df_short = df.iloc[row.name-period:row.name+1]
    max_hb = df_short['high'].median()
    min_hb = df_short['low'].median()
    avarage = (min_hb + max_hb)/2

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
    max_hb = df_short['high'].max()
    min_hb = df_short['low'].min()
    avarage = (min_hb + max_hb)/2

    return np.array([max_hb,min_hb,avarage])

def add_donchan_channel(df:pd.DataFrame,period=20):
    '''add max_hb, min_hb, avarege'''
    points = df.apply(lambda row: get_donchan_channel(row,df,period),axis=1)
    points = np.stack(points.values)
    df['max_hb'] = pd.Series(points[:,0])
    df['min_hb'] = pd.Series(points[:,1])
    df['avarege'] = pd.Series(points[:,2])
    return df

def get_donchan_middle(row,df:pd.DataFrame):
    middle_max,middle_min = -1,-1
    if row.name > 1:
        prev = df.loc[row.name-1]
        middle_min = (row['min_hb'] + prev['min_hb'])/2
        middle_max = (row['max_hb'] + prev['max_hb'])/2
    # if 'shape' in dir(middle_max):
    #     print(row['max_hb'])
    #     print(prev['max_hb'])
    return np.array([middle_max,middle_min])

def add_donchan_middle(df:pd.DataFrame):
    """add 'middle_max','middle_min'"""
    points = df.apply(lambda row: get_donchan_middle(row,df),axis=1)
    # for p in points:
    #     print(p.shape,p)
    points = np.stack(points.values)
    df['middle_max'] = pd.Series(points[:,0])
    df['middle_min'] = pd.Series(points[:,1])
    return df
def get_donchan_prev(row,df:pd.DataFrame,top='max_hb',bottom='min_hb'):
    prev_max,prev_min = -1,-1
    if row.name > 1:
        prev = df.loc[row.name-1]
        prev_min = prev[bottom]
        prev_max = prev[top]
    return np.array([prev_max,prev_min])

def add_donchan_prev(df:pd.DataFrame,top='max_hb',bottom='min_hb'):
    """add 'prev_max','prev_min'"""
    points = df.apply(lambda row: get_donchan_prev(row,df,top,bottom),axis=1)
    points = np.stack(points.values)
    df['prev_max'] = pd.Series(points[:,0])
    df['prev_min'] = pd.Series(points[:,1])
    return df

def add_vangerchik(df:pd.DataFrame):
    """add max_vg, min_vg"""
    df['max_vg'] = df.apply(lambda row: row['max_hb'] - (row['max_hb']-row['min_hb'])/10,axis=1)
    df['min_vg'] = df.apply(lambda row: row['min_hb'] + (row['max_hb']-row['min_hb'])/10,axis=1)
    return df

def get_sma(row,df:pd.DataFrame,period=20,kind='middle'):
    if row.name < period:
        return -1
    df_short = df.iloc[row.name-period:row.name+1]
    return df_short[kind].mean()

def add_sma(df:pd.DataFrame,period=20,kind='middle'):
    '''add sma'''
    df['sma'] = df.apply(lambda row: get_sma(row,df,period,kind),axis=1)
    return df

def get_bollinger(row,df:pd.DataFrame,period=20,kind='middle',multiplier=2):
    if row.name < period:
        return np.array([-1,-1,-1])
    df_short = df.iloc[row.name-period:row.name+1]
    std = df_short[kind].std()
    sma = df_short[kind].mean()
    bbu = sma + std*multiplier
    bbd = sma - std*multiplier

    return np.array([bbu,bbd,sma])

def add_bollinger(df:pd.DataFrame,period=20,kind='middle',multiplier=2):
    '''add bbu, bbd, sma'''
    points = df.apply(lambda row: get_bollinger(row,df,period,kind,multiplier),axis=1)
    points = np.stack(points.values)
    df['bbu'] = pd.Series(points[:,0])
    df['bbd'] = pd.Series(points[:,1])
    df['sma'] = pd.Series(points[:,2])
    return df

def add_over_bb(df:pd.DataFrame):
    '''add over_bbu and over_bbd'''
    df['over_bbu'] = df.apply(lambda row: row['bbu'] < row['low'],axis=1)
    df['over_bbd'] = df.apply(lambda row: row['bbd'] > row['high'],axis=1)
    return df

def get_attached_bb(row,df:pd.DataFrame):
    bbu_attached = False
    bbd_attached = False
    if row.name > 1:
        prev = df.loc[row.name-1]
        if row['high'] > row['bbu'] or prev['high'] > prev['bbu']:
            bbu_attached = True
        if row['low'] < row['bbd'] or prev['low'] < prev['bbd']:
            bbd_attached = True
    return np.array([bbu_attached,bbd_attached])

def get_change_attached_bb(row,df:pd.DataFrame):
    attached_change = False
    if row.name > 1:
        prev = df.iloc[row.name-1]
        if row['bbu_attached'] != prev['bbu_attached']:
            attached_change = True
        if row['bbd_attached'] != prev['bbd_attached']:
            attached_change = True
    return attached_change
def add_attached_bb(df:pd.DataFrame):
    """add bbu_attached, bbd_attached, attached_change"""
    points = df.apply(lambda row: get_attached_bb(row,df),axis=1)
    points = np.stack(points.values)
    df['bbu_attached'] = pd.Series(points[:,0])
    df['bbd_attached'] = pd.Series(points[:,1])
    df['attached_change'] = df.apply(lambda row: get_change_attached_bb(row,df),axis=1)
    return df

def add_big_volume(df:pd.DataFrame,period=20,multiplier=1):
    """add sma_volume, is_big """
    df['sma_volume'] = df.apply(lambda row: get_sma(row,df,period,'volume'),axis=1)
    df['is_big'] = df.apply(lambda row: row['volume']*multiplier > row['sma_volume'],axis=1)
    return df

def add_dynamics_ma(df:pd.DataFrame,period=20,kind='sma'):
    """add dynamics_ma"""
    diff = df[kind].diff()
    df[kind+'_slope'] = diff * (1/diff.mean())
    df['dynamics_ma'] = np.degrees(np.arctan(df[kind+'_slope']))
    df['dynamics_ma'] = df['dynamics_ma'].rolling(period).mean()
    df = df.drop(kind+'_slope',axis=1)
    return df

def get_simple_diff_ma(row,df:pd.DataFrame,kind):
    diff = 0
    if row.name > 1:
        prev = df.iloc[row.name-1]
        if prev[kind] < row[kind]:
            diff = 1
        elif prev[kind] > row[kind]:
            diff = -1
    return diff

def add_simple_diff_ma(df:pd.DataFrame, kind='sma'):
    """add 'sdiff'"""
    df['sdiff'] = df.apply(lambda row: get_simple_diff_ma(row,df,kind),axis=1)
    return df

def get_sdm_ma(row,df:pd.DataFrame,period=20,kind='sdiff'):
    if row.name < period:
        return -1
    df_short = df.iloc[row.name-period:row.name+1]
    return df_short[kind].mean()

def add_simple_dynamics_ma(df:pd.DataFrame,period=20,kind='sma',divider_period=1):
    """add 'sdm'"""
    df = add_simple_diff_ma(df,kind)
    df['sdm'] = df.apply(lambda row: get_sdm_ma(row,df,period//divider_period),axis=1)
    return df

def add_sc_and_buffer(df:pd.DataFrame,top='max_hb',bottom='min_hb',divider=10):
    """add 'spred_channel','buffer'"""
    df['spred_channel'] = df[top] - df[bottom]
    df['buffer'] = df['spred_channel']/divider
    return df

def add_buffer_add(df:pd.DataFrame,top='max_hb',bottom='min_hb',divider=10):
    '''add top_buff, bottom_buff\n
    append outside butter
    '''
    df = add_sc_and_buffer(df,top,bottom,divider)
    df['top_buff'] = df[top]+df['buffer']
    df['bottom_buff'] = df[bottom]-df['buffer']
    return df

def add_buffer_sub(df:pd.DataFrame,top='max_hb',bottom='min_hb',divider=10):
    '''add top_buff, bottom_buff\n
    'append inside butter'
    '''
    df = add_sc_and_buffer(df,top,bottom,divider)
    df['top_buff'] = df[top]-df['buffer']
    df['bottom_buff'] = df[bottom]+df['buffer']
    return df

def add_delta_2v(df:pd.DataFrame,top='max_hb',bottom='min_hb'):
    """add 'delta_2v' """
    df['delta_2v'] = df[top] - df[bottom]
    return df

def add_fractals(df, period=5):
    """
    add 'fractal_up','fractal_down'\n
    Добавляет фракталы Билла Вильямса в DataFrame с данными свечей.
    
    :param df: DataFrame с колонками 'High' и 'Low'
    :param period: Количество свечей для поиска фракталов (по умолчанию 5)
    :return: DataFrame с добавленными колонками 'Fractal_Up' и 'Fractal_Down'
    """
    # Вычисляем смещение для сравнения свечей
    shift = (period - 1) // 2  # Для периода 5 это будет 2
    
    # Фрактал вверх (верхний фрактал)
    fractal_up_condition = True
    for i in range(1, shift + 1):
        fractal_up_condition &= (df['high'] > df['high'].shift(i))
        fractal_up_condition &= (df['high'] > df['high'].shift(-i))
    df['fractal_up'] = fractal_up_condition
    
    # Фрактал вниз (нижний фрактал)
    fractal_down_condition = True
    for i in range(1, shift + 1):
        fractal_down_condition &= (df['low'] < df['low'].shift(i))
        fractal_down_condition &= (df['low'] < df['low'].shift(-i))
    df['fractal_down'] = fractal_down_condition
    
    return df

def add_rsi(df, period=14,kind='close'):
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
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    # Вычисляем относительную силу (RS)
    rs = gain / loss
    
    # Вычисляем RSI
    df['rsi'] = 100 - (100 / (1 + rs))
    
    return df

def add_ema(df, period=20, kind='close'):
    """
    add 'ema'\n
    Вычисляет EMA для DataFrame с данными о ценах.
    
    :param data: DataFrame с колонкой 'Close' (цены закрытия)
    :param period: Период EMA (по умолчанию 20)
    :param column: Название колонки с ценами (по умолчанию 'Close')
    :return: DataFrame с добавленной колонкой 'EMA'
    """
    # Вычисляем коэффициент сглаживания
    alpha = 2 / (period + 1)
    
    # Вычисляем SMA для первой точки
    df['ema'] = df[kind].rolling(window=period).mean()
    
    # Вычисляем EMA для остальных точек
    for i in range(period, len(df)):
        df.loc[df.index[i], 'ema'] = (df[kind].iloc[i] * alpha) + (df['ema'].iloc[i - 1] * (1 - alpha))
    
    return df

def add_stochastic(df, k_period=14, d_period=3,kind='close'):
    """add 'lowest_so','highest_so','%k','%d' """
    df['lowest_so'] = df[kind].rolling(window=k_period).min()
    df['highest_so'] = df[kind].rolling(window=k_period).max()
    df['%k'] = 100 * ((df[kind] - df['lowest_so']) / (df['highest_so'] - df['lowest_so']))
    df['%d'] = df['%k'].rolling(window=d_period).mean()
    return df

def add_atr(df, period=5,kind='close'):
    df['high_low'] = df['high'] - df['low']
    df['high_close'] = np.abs(df['high'] - df[kind].shift(1))
    df['low_close'] = np.abs(df['low'] - df[kind].shift(1))
    df['tr'] = df[['high_low', 'high_close', 'low_close']].max(axis=1)
    df['atr'] = df['tr'].rolling(window=period).mean()
    return df

def add_local_extrema(df, window=5):
    df['local_max'] = df['close'].rolling(window=window).max()
    df['local_min'] = df['close'].rolling(window=window).min()
    return df
# что-то не то
def add_supertrend(df, period=10, multiplier=3):
    """
    Рассчитывает индикатор SuperTrend.
    """
    # Вычисляем ATR (Average True Range)
    df = add_atr(df,period)
    
    # Рассчитываем базовые линии (верхнюю и нижнюю)
    df['upper_band'] = (df['high'] + df['low']) / 2 + multiplier * df['atr']
    df['lower_band'] = (df['high'] + df['low']) / 2 - multiplier * df['atr']
    
    # Инициализируем колонку для SuperTrend
    df['supertrend'] = 0.0
    df['in_uptrend'] = True  # Флаг для определения текущего тренда
    
    # Расчет SuperTrend
    for i in range(1, len(df)):
        if df['close'].iloc[i] > df['upper_band'].iloc[i - 1]:
            df.loc[df.index[i], 'in_uptrend'] = True
        elif df['close'].iloc[i] < df['lower_band'].iloc[i - 1]:
            df.loc[df.index[i], 'in_uptrend'] = False
        
        # Устанавливаем значение SuperTrend
        if df['in_uptrend'].iloc[i]:
            df.loc[df.index[i], 'supertrend'] = df['lower_band'].iloc[i]
        else:
            df.loc[df.index[i], 'supertrend'] = df['upper_band'].iloc[i]
    
    return df

def add_macd(data, short_window=12, long_window=26, signal_window=9):
    """add 'ema_1','ema_2','macd','signal_line'"""
    data['ema_1'] = data['close'].ewm(span=short_window, adjust=False).mean()
    data['ema_2'] = data['close'].ewm(span=long_window, adjust=False).mean()
    data['macd'] = data['ema_1'] - data['ema_2']
    data['signal_line'] = data['macd'].ewm(span=signal_window, adjust=False).mean()
    return data

def add_adx(df,adx_period=14):
    """
    Расчет индикатора ADX (Average Directional Index).
    :param df: DataFrame с данными
    :return: DataFrame с добавленным столбцом ADX
    """
    # Расчет True Range (TR)
    df['tr'] = np.maximum(
        df['high'] - df['low'],
        np.maximum(
            abs(df['high'] - df['close'].shift(1)),
            abs(df['low'] - df['close'].shift(1))
        )
    )

    # Расчет Positive Directional Movement (+DM) и Negative Directional Movement (-DM)
    df['plus_dm'] = np.where(
        (df['high'] - df['high'].shift(1)) > (df['low'].shift(1) - df['low']),
        np.maximum(df['high'] - df['high'].shift(1), 0),
        0
    )
    df['minus_dm'] = np.where(
        (df['low'].shift(1) - df['low']) > (df['high'] - df['high'].shift(1)),
        np.maximum(df['low'].shift(1) - df['low'], 0),
        0
    )

    # Сглаживание TR, +DM, -DM
    df['tr_smooth'] = df['tr'].rolling(window=adx_period, min_periods=adx_period).sum()
    df['plus_dm_smooth'] = df['plus_dm'].rolling(window=adx_period, min_periods=adx_period).sum()
    df['minus_dm_smooth'] = df['minus_dm'].rolling(window=adx_period, min_periods=adx_period).sum()

    # Расчет +DI и -DI
    df['plus_di'] = (df['plus_dm_smooth'] / df['tr_smooth']) * 100
    df['minus_di'] = (df['minus_dm_smooth'] / df['tr_smooth']) * 100

    # Расчет ADX
    df['dx'] = (abs(df['plus_di'] - df['minus_di']) / (df['plus_di'] + df['minus_di'])) * 100
    df['adx'] = df['dx'].rolling(window=adx_period, min_periods=adx_period).mean()

    return df

def add_kama(df, period=30,fast_ema=2,slow_ema=30):
    """
    Расчет индикатора KAMA (Kaufman Adaptive Moving Average).
    :param df: DataFrame с данными
    :param period: Период для расчета KAMA
    :return: DataFrame с добавленным столбцом KAMA
    """
    change = abs(df['close'] - df['close'].shift(period))
    volatility = df['close'].diff().abs().rolling(window=period).sum()
    efficiency_ratio = change / volatility

    fast_sc = 2 / (fast_ema + 1)
    slow_sc = 2 / (slow_ema + 1)
    smooth_constant = (efficiency_ratio * (fast_sc - slow_sc) + slow_sc) ** 2

    df[f'kama_{period}'] = 0.0
    for i in range(period, len(df)):
        df.loc[df.index[i], f'kama_{period}'] = (
            df.loc[df.index[i - 1], f'kama_{period}'] +
            smooth_constant[i] * (df.loc[df.index[i], 'close'] - df.loc[df.index[i - 1], f'kama_{period}'])
        )
    return df

def add_chop(df,chop_period=14):
    """
    'chop'
    Расчет индикатора CHOP (Choppiness Index).
    :param df: DataFrame с данными
    :return: DataFrame с добавленным столбцом CHOP
    """
    # Расчет True Range (TR)
    df['tr'] = np.maximum(
        df['high'] - df['low'],
        np.maximum(
            abs(df['high'] - df['close'].shift(1)),
            abs(df['low'] - df['close'].shift(1))
        )
    )

    # Сумма TR за период
    df['tr_sum'] = df['tr'].rolling(window=chop_period).sum()

    # Максимальная и минимальная цена за период
    df['high_max'] = df['high'].rolling(window=chop_period).max()
    df['low_min'] = df['low'].rolling(window=chop_period).min()

    # Расчет CHOP
    df['chop'] = 100 * np.log10(df['tr_sum'] / (df['high_max'] - df['low_min'])) / np.log10(chop_period)
    return df