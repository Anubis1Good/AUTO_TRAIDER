 # Работа с QUIK из Python через LUA скрипты QuikSharp
import pandas as pd
import mplfinance as mpf

col_names = ['Date','Open','High','Low','Close','Volume']
df = pd.DataFrame(columns=col_names)
del col_names

#  0   Date    30 non-null     object
#  1   Open    30 non-null     float64
#  2   High    30 non-null     float64
#  3   Low     30 non-null     float64
#  4   Close   30 non-null     float64
#  5   Volume
def change_data(data):
    dt = data['datetime']
    new_data = {
        'Date': f"{str(dt['day']).zfill(2)}.{str(dt['month']).zfill(2)}.{dt['year']} {str(dt['hour']).zfill(2)}:{str(dt['min']).zfill(2)}",
        'Open':data['open'],
        'High':data['high'],
        'Low':data['low'],
        'Close':data['close'],
        'Volume':data['volume']
    }
    return new_data
sample = {
    'datetime': {'day': 7, 'hour': 16, 'year': 2024, 'count': 1, 'week_day': 5, 'month': 6, 'min': 50, 'sec': 0, 'ms': 0},
    'sec': 'SBER',
    'volume': 4011.0,
    'interval': 1, 
    'low': 319.35,
    'class': 'TQBR', 
    'high': 319.38, 
    'open': 319.35, 
    'close': 319.38}

# 19.06.2012 00:00
from datetime import datetime
import time  # Подписка на события по времени
from QuikPy import QuikPy  # Работа с QUIK из Python через LUA скрипты QuikSharp


def print_callback(data):
    """Пользовательский обработчик событий:
    - Изменение стакана котировок
    - Получение обезличенной сделки
    - Получение новой свечки
    """
    print(data["data"])
    global df
    df.loc[len(df)] = change_data(data["data"])
    # print(f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")} - {data["data"]}')  # Печатаем полученные данные




if __name__ == '__main__':  # Точка входа при запуске этого скрипта
    qp_provider = QuikPy()  # Подключение к локальному запущенному терминалу QUIK

    class_code = 'TQBR'  # Класс тикера
    sec_code = 'SBER'  # Тикер  


    # Новые свечки. При первой подписке получим все свечки с начала прошлой сессии
    # TODO В QUIK 9.2.13.15 перестала работать повторная подписка на минутные бары. Остальные работают
    #  Перед повторной подпиской нужно перезапустить скрипт QuikSharp.lua Подписка станет первой, все заработает
    qp_provider.OnNewCandle = print_callback  # Обработчик получения новой свечки
    for interval in (1,):  # (1, 60, 1440) = Минутки, часовки, дневки
        print(f'Подписка на интервал {interval}:', qp_provider.SubscribeToCandles(class_code, sec_code, interval)['data'])
        print(f'Статус подписки на интервал {interval}:', qp_provider.IsSubscribed(class_code, sec_code, interval)['data'])
    input('Enter - отмена\n')
    for interval in (1,):  # (1, 60, 1440) = Минутки, часовки, дневки
        print(f'Отмена подписки на интервал {interval}', qp_provider.UnsubscribeFromCandles(class_code, sec_code, interval)['data'])
        print(f'Статус подписки на интервал {interval}:', qp_provider.IsSubscribed(class_code, sec_code, interval)['data'])

    # Выход
    try:
        df = df.iloc[1:]
        df.index = pd.DatetimeIndex(df['Date'])
        print(df.head(10))
        df.info()
        mpf.plot(df,volume=True)
    finally:
        qp_provider.CloseConnectionAndThread()
      # Перед выходом закрываем соединение и поток QuikPy
