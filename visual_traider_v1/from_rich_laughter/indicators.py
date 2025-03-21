import pandas as pd
import numpy as np
from scipy.stats import linregress

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

def add_vodka_channel(df:pd.DataFrame,period=20):
    '''add top_mean, bottom_mean, avarege_mean'''
    df['top_mean'] = df['high'].rolling(window=period).median()
    df['bottom_mean'] = df['low'].rolling(window=period).median()
    df['avarege_mean'] = (df['top_mean'] + df['bottom_mean']) / 2
    return df



def add_donchan_channel(df, period=20):
    """
    '''add max_hb, min_hb, avarege'''
    
    :param df: DataFrame с колонками 'high', 'low'
    :param period: Период для расчета канала Дончиана (по умолчанию 20)
    :return: DataFrame с добавленными колонками
    """
    # Верхняя полоса (максимум за последние N периодов)
    df['max_hb'] = df['high'].rolling(window=period).max()
    
    # Нижняя полоса (минимум за последние N периодов)
    df['min_hb'] = df['low'].rolling(window=period).min()
    
    # Средняя линия
    df['avarege'] = (df['max_hb'] + df['min_hb']) / 2
    
    return df




def add_vangerchik(df: pd.DataFrame):
    """
    Добавляет колонки 'max_vg' и 'min_vg' в DataFrame.
    Оптимизированная версия с использованием векторизованных операций.
    
    :param df: DataFrame с колонками 'max_hb', 'min_hb'
    :return: DataFrame с добавленными колонками 'max_vg', 'min_vg'
    """
    # Вычисляем разницу между 'max_hb' и 'min_hb'
    diff = df['max_hb'] - df['min_hb']
    
    # Вычисляем 'max_vg' и 'min_vg' с использованием векторизованных операций
    df['max_vg'] = df['max_hb'] - diff / 10
    df['min_vg'] = df['min_hb'] + diff / 10
    
    return df


def add_sma(df: pd.DataFrame, period=20, kind='close'):
    """
    Добавляет колонку 'sma' в DataFrame.
    Оптимизированная версия с использованием встроенных функций Pandas.
    
    :param df: DataFrame с колонками 'high', 'low', 'close'
    :param period: Период для SMA (по умолчанию 20)
    :param kind: Тип цены для расчета SMA ('middle', 'high', 'low', 'close')
    :return: DataFrame с добавленной колонкой 'sma'
    """
    # Выбираем колонку для расчета SMA
    if kind == 'middle':
        price = (df['high'] + df['low']) / 2
    elif kind == 'high':
        price = df['high']
    elif kind == 'low':
        price = df['low']
    elif kind == 'close':
        price = df['close']
    else:
        raise ValueError("Неподдерживаемый тип цены. Используйте 'middle', 'high', 'low' или 'close'.")
    
    # Вычисляем SMA с использованием встроенной функции rolling
    df['sma'] = price.rolling(window=period).mean()
    
    return df


def add_bollinger(df: pd.DataFrame, period=20, kind='close', multiplier=2):
    """
    Добавляет колонки 'bbu', 'bbd', 'sma' в DataFrame.
    Оптимизированная версия с использованием встроенных функций Pandas.
    
    :param df: DataFrame с колонками 'high', 'low', 'close'
    :param period: Период для расчета полос Боллинджера (по умолчанию 20)
    :param kind: Тип цены для расчета ('middle', 'high', 'low', 'close')
    :param multiplier: Множитель для стандартного отклонения (по умолчанию 2)
    :return: DataFrame с добавленными колонками 'bbu', 'bbd', 'sma'
    """
    # Выбираем колонку для расчета
    if kind == 'middle':
        price = (df['high'] + df['low']) / 2
    elif kind == 'high':
        price = df['high']
    elif kind == 'low':
        price = df['low']
    elif kind == 'close':
        price = df['close']
    else:
        raise ValueError("Неподдерживаемый тип цены. Используйте 'middle', 'high', 'low' или 'close'.")
    
    # Вычисляем SMA
    df['sma'] = price.rolling(window=period).mean()
    
    # Вычисляем стандартное отклонение
    std_dev = price.rolling(window=period).std()
    
    # Вычисляем верхнюю и нижнюю полосы Боллинджера
    df['bbu'] = df['sma'] + (multiplier * std_dev)
    df['bbd'] = df['sma'] - (multiplier * std_dev)
    
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
    df['sma_volume'] = df['volume'].rolling(period).mean()
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

def add_rsi_tw(df, period=14, kind='close'):
    """
    Добавляет колонку 'rsi_tw' в DataFrame с данными о ценах.
    
    :param df: DataFrame с колонкой 'close' (цены закрытия)
    :param period: Период RSI (по умолчанию 14)
    :param kind: Название колонки с ценами (по умолчанию 'close')
    :return: DataFrame с добавленной колонкой 'RSI'
    """
    # Вычисляем изменение цены
    delta = df[kind].diff()
    
    # Разделяем на рост и падение
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # Вычисляем экспоненциальное скользящее среднее (EMA) для роста и падения
    avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()
    
    # Вычисляем относительную силу (RS)
    rs = avg_gain / avg_loss
    
    # Вычисляем RSI
    df['rsi_tw'] = 100 - (100 / (1 + rs))
    
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
    'adx'
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

def add_cci(df, period=20, kind='close'):
    """
    Добавляет колонку 'cci' в DataFrame с данными о ценах.
    
    :param df: DataFrame с колонкой 'close' (цены закрытия)
    :param period: Период CCI (по умолчанию 20)
    :param kind: Название колонки с ценами (по умолчанию 'close')
    :return: DataFrame с добавленной колонкой 'CCI'
    """
    # Вычисляем типичную цену (Typical Price)
    typical_price = (df['high'] + df['low'] + df[kind]) / 3
    
    # Вычисляем скользящее среднее типичной цены (SMA)
    sma = typical_price.rolling(window=period).mean()
    
    # Вычисляем среднее отклонение (Mean Deviation)
    mean_deviation = typical_price.rolling(window=period).apply(
        lambda x: np.abs(x - x.mean()).mean(), raw=True
    )
    
    # Вычисляем CCI
    df['cci'] = (typical_price - sma) / (0.015 * mean_deviation)
    
    return df

def add_williams_r(df, period=14, kind='close'):
    """
    Добавляет колонку 'williams_r' в DataFrame с данными о ценах.
    
    :param df: DataFrame с колонками 'high', 'low' и 'close'
    :param period: Период Williams %R (по умолчанию 14)
    :param kind: Название колонки с ценами закрытия (по умолчанию 'close')
    :return: DataFrame с добавленной колонкой 'williams_r'
    """
    # Вычисляем максимум и минимум за период
    highest_high = df['high'].rolling(window=period).max()
    lowest_low = df['low'].rolling(window=period).min()
    
    # Вычисляем Williams %R
    df['williams_r'] = -100 * (highest_high - df[kind]) / (highest_high - lowest_low)
    
    return df

def add_mfi(df, period=14):
    """
    Добавляет колонку 'mfi' в DataFrame с данными о ценах и объемах.
    
    :param df: DataFrame с колонками 'high', 'low', 'close' и 'volume'
    :param period: Период MFI (по умолчанию 14)
    :return: DataFrame с добавленной колонкой 'MFI'
    """
    # Вычисляем типичную цену (Typical Price)
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    
    # Вычисляем денежный поток (Money Flow)
    money_flow = typical_price * df['volume']
    
    # Определяем положительный и отрицательный денежный поток
    positive_flow = (typical_price > typical_price.shift(1)) * money_flow
    negative_flow = (typical_price < typical_price.shift(1)) * money_flow
    
    # Вычисляем сумму положительного и отрицательного денежного потока за период
    positive_flow_sum = positive_flow.rolling(window=period).sum()
    negative_flow_sum = negative_flow.rolling(window=period).sum()
    
    # Вычисляем Money Flow Ratio (MFR)
    money_flow_ratio = positive_flow_sum / negative_flow_sum
    
    # Вычисляем MFI
    df['mfi'] = 100 - (100 / (1 + money_flow_ratio))
    
    return df

def add_awesome_oscillator(df, short_period=5, long_period=34):
    """
    Добавляет колонку 'ao' в DataFrame с данными о ценах.
    
    :param df: DataFrame с колонкой 'close' (цены закрытия)
    :param short_period: Период короткой скользящей средней (по умолчанию 5)
    :param long_period: Период длинной скользящей средней (по умолчанию 34)
    :return: DataFrame с добавленной колонкой 'ao'
    """
    # Вычисляем типичную цену (Typical Price)
    typical_price = (df['high'] + df['low']) / 2
    
    # Вычисляем короткую и длинную скользящие средние (SMA)
    sma_short = typical_price.rolling(window=short_period).mean()
    sma_long = typical_price.rolling(window=long_period).mean()
    
    # Вычисляем Awesome Oscillator (AO)
    df['ao'] = sma_short - sma_long
    
    return df

def add_roc(df, period=12, kind='close'):
    """
    Добавляет колонку 'roc' в DataFrame с данными о ценах.
    
    :param df: DataFrame с колонкой 'close' (цены закрытия)
    :param period: Период ROC (по умолчанию 12)
    :param kind: Название колонки с ценами (по умолчанию 'close')
    :return: DataFrame с добавленной колонкой 'ROC'
    """
    # Вычисляем ROC
    df['roc'] = ((df[kind] - df[kind].shift(period)) / df[kind].shift(period)) * 100
    
    return df

def add_ultimate_oscillator(df, short_period=7, medium_period=14, long_period=28):
    """
    Добавляет колонку 'ultimate_oscillator' в DataFrame с данными о ценах.
    
    :param df: DataFrame с колонками 'high', 'low', 'close'
    :param short_period: Короткий период (по умолчанию 7)
    :param medium_period: Средний период (по умолчанию 14)
    :param long_period: Длинный период (по умолчанию 28)
    :return: DataFrame с добавленной колонкой 'ultimate_oscillator'
    """
    # Вычисляем типичную цену (Typical Price)
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    
    # Вычисляем денежный поток (Money Flow)
    money_flow = typical_price * df['volume']
    
    # Определяем давление покупок и продаж
    buying_pressure = typical_price - df[['low', 'close']].min(axis=1)
    true_range = df[['high', 'close']].max(axis=1) - df[['low', 'close']].min(axis=1)
    
    # Вычисляем средние значения для каждого периода
    avg_buying_pressure_short = buying_pressure.rolling(window=short_period).sum()
    avg_true_range_short = true_range.rolling(window=short_period).sum()
    
    avg_buying_pressure_medium = buying_pressure.rolling(window=medium_period).sum()
    avg_true_range_medium = true_range.rolling(window=medium_period).sum()
    
    avg_buying_pressure_long = buying_pressure.rolling(window=long_period).sum()
    avg_true_range_long = true_range.rolling(window=long_period).sum()
    
    # Вычисляем компоненты осциллятора
    short_component = avg_buying_pressure_short / avg_true_range_short
    medium_component = avg_buying_pressure_medium / avg_true_range_medium
    long_component = avg_buying_pressure_long / avg_true_range_long
    
    # Вычисляем Ultimate Oscillator
    df['ultimate_oscillator'] = (4 * short_component + 2 * medium_component + long_component) / 7 * 100
    
    return df

def add_cmo(df, period=14, kind='close'):
    """
    Добавляет колонку 'cmo' в DataFrame с данными о ценах.
    
    :param df: DataFrame с колонкой 'close' (цены закрытия)
    :param period: Период CMO (по умолчанию 14)
    :param kind: Название колонки с ценами (по умолчанию 'close')
    :return: DataFrame с добавленной колонкой 'CMO'
    """
    # Вычисляем изменение цены
    delta = df[kind].diff()
    
    # Разделяем на рост и падение
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # Вычисляем сумму роста и падения за период
    sum_gain = gain.rolling(window=period).sum()
    sum_loss = loss.rolling(window=period).sum()
    
    # Вычисляем CMO
    df['cmo'] = ((sum_gain - sum_loss) / (sum_gain + sum_loss)) * 100
    
    return df


def add_keltner_channel(df, period=20, multiplier=2):
    """
    Добавляет колонки 'keltner_upper', 'keltner_middle', 'keltner_lower' в DataFrame.
    
    :param df: DataFrame с колонками 'high', 'low', 'close'
    :param period: Период для EMA и ATR (по умолчанию 20)
    :param multiplier: Множитель для ATR (по умолчанию 2)
    :return: DataFrame с добавленными колонками
    """
    # Вычисляем EMA (центральная линия)
    df['keltner_middle'] = df['close'].ewm(span=period, adjust=False).mean()
    
    # Вычисляем ATR (средний истинный диапазон)
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift()).abs()
    low_close = (df['low'] - df['close'].shift()).abs()
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window=period).mean()
    
    # Вычисляем верхнюю и нижнюю полосы
    df['keltner_upper'] = df['keltner_middle'] + (multiplier * atr)
    df['keltner_lower'] = df['keltner_middle'] - (multiplier * atr)
    
    return df

def add_ma_envelope(df, period=20, deviation=0.05):
    """
    Добавляет колонки 'envelope_upper', 'envelope_lower' в DataFrame.
    
    :param df: DataFrame с колонкой 'close'
    :param period: Период для SMA (по умолчанию 20)
    :param deviation: Процент отклонения (по умолчанию 0.05)
    :return: DataFrame с добавленными колонками
    """
    df['sma'] = df['close'].rolling(window=period).mean()
    df['envelope_upper'] = df['sma'] * (1 + deviation)
    df['envelope_lower'] = df['sma'] * (1 - deviation)
    return df

def add_std_dev_channel(df, period=20, multiplier=2):
    """
    Добавляет колонки 'std_upper', 'std_lower' в DataFrame.
    
    :param df: DataFrame с колонкой 'close'
    :param period: Период для SMA и стандартного отклонения (по умолчанию 20)
    :param multiplier: Множитель для стандартного отклонения (по умолчанию 2)
    :return: DataFrame с добавленными колонками
    """
    df['sma'] = df['close'].rolling(window=period).mean()
    std_dev = df['close'].rolling(window=period).std()
    df['std_upper'] = df['sma'] + (multiplier * std_dev)
    df['std_lower'] = df['sma'] - (multiplier * std_dev)
    return df




def add_linear_regression_channel(df, period=20, multiplier=2):
    """
    Добавляет колонки 'regression_upper', 'regression_lower','regression_middle' в DataFrame.
    
    :param df: DataFrame с колонкой 'close'
    :param period: Период для линейной регрессии (по умолчанию 20)
    :param multiplier: Множитель для стандартного отклонения (по умолчанию 2)
    :return: DataFrame с добавленными колонками
    """
    def calculate_regression(values):
        x = range(len(values))  # Создаем массив индексов
        slope, intercept, _, _, _ = linregress(x, values)
        return slope * x[-1] + intercept  # Возвращаем значение на последней точке
    
    # Применяем линейную регрессию к скользящему окну
    df['regression_middle'] = df['close'].rolling(window=period).apply(calculate_regression, raw=True)
    
    # Вычисляем стандартное отклонение
    std_dev = df['close'].rolling(window=period).std()
    
    # Вычисляем верхнюю и нижнюю полосы
    df['regression_upper'] = df['regression_middle'] + (multiplier * std_dev)
    df['regression_lower'] = df['regression_middle'] - (multiplier * std_dev)
    
    return df

def add_lrchl(df, period=20):
    """
    Добавляет колонки 'regression_upper', 'regression_lower' в DataFrame.
    
    :param df: DataFrame с колонкой 'close'
    :param period: Период для линейной регрессии (по умолчанию 20)
    :param multiplier: Множитель для стандартного отклонения (по умолчанию 2)
    :return: DataFrame с добавленными колонками
    """
    def calculate_regression(values):
        x = range(len(values))  # Создаем массив индексов
        slope, intercept, _, _, _ = linregress(x, values)
        return slope * x[-1] + intercept  # Возвращаем значение на последней точке
    
    # Применяем линейную регрессию к скользящему окну
    df['regression_upper'] = df['high'].rolling(window=period).apply(calculate_regression, raw=True)
    df['regression_lower'] = df['low'].rolling(window=period).apply(calculate_regression, raw=True)

    
    return df

def add_atr_channel(df, period=20, multiplier=2):
    """
    Добавляет колонки 'atr_upper', 'atr_lower' в DataFrame.
    
    :param df: DataFrame с колонками 'high', 'low', 'close'
    :param period: Период для ATR (по умолчанию 20)
    :param multiplier: Множитель для ATR (по умолчанию 2)
    :return: DataFrame с добавленными колонками
    """
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift()).abs()
    low_close = (df['low'] - df['close'].shift()).abs()
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window=period).mean()
    
    df['atr_upper'] = df['close'] + (multiplier * atr)
    df['atr_lower'] = df['close'] - (multiplier * atr)
    return df

def add_volatility_bands(df, period=20, multiplier=2):
    """
    Добавляет колонки 'volatility_upper', 'volatility_lower' в DataFrame.
    
    :param df: DataFrame с колонкой 'close'
    :param period: Период для SMA и стандартного отклонения (по умолчанию 20)
    :param multiplier: Множитель для стандартного отклонения (по умолчанию 2)
    :return: DataFrame с добавленными колонками
    """
    df['sma'] = df['close'].rolling(window=period).mean()
    std_dev = df['close'].rolling(window=period).std()
    df['volatility_upper'] = df['sma'] + (multiplier * std_dev)
    df['volatility_lower'] = df['sma'] - (multiplier * std_dev)
    return df

def add_parabolic_sar(df, acceleration=0.02, maximum=0.2):
    """
    Добавляет колонку 'parabolic_sar' в DataFrame.
    
    :param df: DataFrame с колонками 'high', 'low'
    :param acceleration: Начальное ускорение (по умолчанию 0.02)
    :param maximum: Максимальное ускорение (по умолчанию 0.2)
    :return: DataFrame с добавленной колонкой
    """
    sar = []
    trend = 1  # 1 для восходящего тренда, -1 для нисходящего
    ep = df['high'].iloc[0]  # Экстремальная точка
    af = acceleration  # Фактор ускорения
    
    for i in range(len(df)):
        if i == 0:
            sar.append(df['low'].iloc[0])
            continue
        
        if trend == 1:
            sar.append(sar[-1] + af * (ep - sar[-1]))
        else:
            sar.append(sar[-1] + af * (ep - sar[-1]))
        
        if trend == 1:
            if df['high'].iloc[i] > ep:
                ep = df['high'].iloc[i]
                af = min(af + acceleration, maximum)
            if df['low'].iloc[i] < sar[-1]:
                trend = -1
                sar[-1] = ep
                ep = df['low'].iloc[i]
                af = acceleration
        else:
            if df['low'].iloc[i] < ep:
                ep = df['low'].iloc[i]
                af = min(af + acceleration, maximum)
            if df['high'].iloc[i] > sar[-1]:
                trend = 1
                sar[-1] = ep
                ep = df['high'].iloc[i]
                af = acceleration
    
    df['parabolic_sar'] = sar
    return df

def add_volume_profile(df, period=14):
    """
    Добавляет Volume Profile в DataFrame.
    
    :param df: DataFrame с колонками 'high', 'low', 'close', 'volume'
    :param period: Период для расчета Volume Profile (по умолчанию 14)
    :return: DataFrame с добавленными колонками 'poc', 'value_area_high', 'value_area_low'
    """
    # Создаем пустые колонки для результатов
    df['poc'] = np.nan
    df['value_area_high'] = np.nan
    df['value_area_low'] = np.nan
    
    for i in range(period, len(df)):
        # Выбираем данные за последние `period` дней
        window = df.iloc[i-period:i]
        
        # Создаем гистограмму объема по ценам
        price_bins = np.linspace(window['low'].min(), window['high'].max(), num=100)
        volume_profile = np.zeros_like(price_bins)
        
        for j in range(len(window)):
            low = window.iloc[j]['low']
            high = window.iloc[j]['high']
            close = window.iloc[j]['close']
            volume = window.iloc[j]['volume']
            
            # Распределяем объем по ценам
            mask = (price_bins >= low) & (price_bins <= high)
            volume_profile[mask] += volume
        
        # Находим POC (цена с максимальным объемом)
        poc_index = np.argmax(volume_profile)
        poc = price_bins[poc_index]
        
        # Находим Value Area (70% объема)
        total_volume = np.sum(volume_profile)
        sorted_volume_indices = np.argsort(volume_profile)[::-1]
        cumulative_volume = 0
        value_area_indices = []
        
        for idx in sorted_volume_indices:
            cumulative_volume += volume_profile[idx]
            value_area_indices.append(idx)
            if cumulative_volume >= 0.7 * total_volume:
                break
        
        value_area_prices = price_bins[value_area_indices]
        value_area_high = np.max(value_area_prices)
        value_area_low = np.min(value_area_prices)
        
        # Записываем результаты
        df.at[df.index[i], 'poc'] = poc
        df.at[df.index[i], 'value_area_high'] = value_area_high
        df.at[df.index[i], 'value_area_low'] = value_area_low
    
    return df

def add_rvi(df, period=14):
    """
    Добавляет колонку 'rvi' в DataFrame с данными о ценах.
    
    :param df: DataFrame с колонкой 'close'
    :param period: Период для RVI (по умолчанию 14)
    :return: DataFrame с добавленной колонкой 'RVI'
    """
    # Вычисляем стандартное отклонение цен закрытия
    std_dev = df['close'].rolling(window=period).std()
    
    # Сглаживаем стандартное отклонение с помощью EMA
    smoothed_std_dev = std_dev.ewm(span=period, adjust=False).mean()
    
    # Вычисляем среднее значение сглаженного стандартного отклонения
    mean_smoothed_std_dev = smoothed_std_dev.rolling(window=period).mean()
    
    # Вычисляем RVI
    df['rvi'] = (smoothed_std_dev / mean_smoothed_std_dev) * 100
    
    return df

def help_delta(row):
    if row['close'] > row['open']:  # Бычья свеча
        return row['volume']
    elif row['close'] < row['open']:  # Медвежья свеча
        return -row['volume']
    return 0

def add_CDV(df:pd.DataFrame):
    'add "cdv"'
    df['delta'] = df.apply(help_delta,axis=1)
    df['cdv'] = df['delta'].cumsum()  # Кумулятивная сумма
    return df