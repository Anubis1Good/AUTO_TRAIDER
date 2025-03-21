from from_rich_laughter.indicators import *

class BaseTABitget:
    def __init__(self,symbol="BTCUSDT",granularity="1m",productType="usdt-futures",n_parts=1,period=20):
        self.symbol = symbol
        self.granularity = granularity
        self.productType = productType
        self.n_parts = n_parts
        self.period = period

    def preprocessing(self,df):
        df = add_slice_df(df,period=self.period)
        return df
    
    def get_test_df(self,df):
        df = self.preprocessing(df)
        return df
    
    def get_test_row(self,df):
        df = self.preprocessing(df)
        return df.iloc[-1]
    
    # def get_row(self):
    #     limit = self.period*3
    #     df = get_df(self.symbol,self.granularity,self.productType,limit)
    #     df = self.preprocessing(df)
    #     return df.iloc[-1]
    
    # def get_middle_price(self,row):
    #     return row['middle']
    
    def __call__(self,row, *args, **kwds):
        return None

class PTA4_WDDCr(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_rsi(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] == row['min_hb']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if row['high'] == row['max_hb']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'
            
class PTA4_WDVCr(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_vodka_channel(df,self.period)
        df = add_enter_price2close(df)
        df = add_rsi(df,self.period)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['bottom_mean']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if row['high'] > row['top_mean']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'
            
class PTA4_WLISICA(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,divider=1,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
        self.divider = divider
    def preprocessing(self, df):
        df = add_vodka_channel(df,self.period)
        df = add_buffer_add(df,'top_mean','bottom_mean',self.divider)
        df = add_enter_price2close(df)
        df = add_rsi(df,self.period)
        df = add_slice_df(df,self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['bottom_buff']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if row['high'] > row['top_buff']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'

class PTA4_WDDCrVG(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_vangerchik(df)
        df = add_enter_price2close(df)
        df = add_rsi(df,self.period)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['min_vg']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if row['high'] > row['max_vg']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'

class PTA4_WDDCrE(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_donchan_channel(df,self.period)
        df = add_rsi(df,self.period)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] == row['min_hb']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
                else:
                    return 'close_short_pw'
        if row['high'] == row['max_hb']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'
            else:
                return 'close_long_pw'

class PTA8_WDOBBY_FREEr(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,multiplier=2,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
        self.multiplier = multiplier
    def preprocessing(self, df):
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_enter_price2close(df)
        df = add_rsi(df,self.period)
        df = add_slice_df(df,period=self.period)
        return df
    def __call__(self, row, *args, **kwds):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] < row['bbd']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long_pw'
        if row['high'] > row['bbu']:
            if row['rsi'] > 100-self.threshold:
                return 'short_pw'
            
class OGTA4_DOG(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=14,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_CDV(df)
        df = add_rsi(df,self.period,'cdv')
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        # df['signal'] = add_signal(df) # поиск какого-то сигнала
        return df

    def __call__(self, row, *args, **kwds):
        if row['rsi'] < self.threshold:  
            return 'long_pw'
        if row['rsi'] > 100-self.threshold:  
            return 'short_pw'
        
class LTA_OKROSHKA(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=15,period_chop=10):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period_chop = period_chop
    def preprocessing(self, df):
        df = add_rsi(df,self.period)
        df = add_chop(df,self.period_chop)
        df = add_enter_price2close(df)  
        period = max(self.period,self.period_chop)
        df = add_slice_df(df, period) 
        # df['signal'] = add_signal(df) # поиск какого-то сигнала
        return df

    def __call__(self, row, *args, **kwds):
        threshold = 30
        if 60 > row['chop'] > 45:
            threshold = 30
        elif row['chop'] > 60:
            threshold = 25
        elif 45 > row['chop'] > 30:
            threshold = 20
        else:
            threshold = 10
        if row['rsi'] < threshold:  
            return 'long_pw'
        if row['rsi'] > 100-threshold:  
            return 'short_pw'
        
class LTA_KROSH(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=15,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_rsi(df,self.period)

        df = add_enter_price2close(df)  

        df = add_slice_df(df, self.period) 
        # df['signal'] = add_signal(df) # поиск какого-то сигнала
        return df

    def __call__(self, row, *args, **kwds):
        if row['rsi'] < self.threshold:  
            return 'long_pw'
        if row['rsi'] > 100-self.threshold:  
            return 'short_pw'
        
class PTA10_WIZARD(BaseTABitget):
    'period=26, period2=12, period3=9,threshold=20,threshold_adx=20'
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=26, period2=12, period3=9,threshold=20,threshold_adx=20):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
        self.period3 = period3
        self.threshold = threshold
        self.threshold_adx = threshold_adx
    def preprocessing(self, df):
        df = add_macd(df,self.period2,self.period,self.period3)
        df = add_adx(df,self.period2)
        df = add_rsi_tw(df,self.period2)
        df = add_enter_price2close(df)
        df = add_slice_df(df,period=self.period)
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа
        df.loc[df['macd'] > df['signal_line'], 'signal'] = 1  # Покупка
        df.loc[df['macd'] < df['signal_line'], 'signal'] = -1  # Продажа
        return df
    def __call__(self, row, *args, **kwds):
        if row['adx'] > self.threshold_adx:
            if row['signal'] == 1 and row['rsi_tw'] < 100-self.threshold:
                return 'long_pw'
            if row['signal'] == -1 and row['rsi_tw'] > self.threshold:
                return 'short_pw'
        if row['rsi_tw'] < self.threshold:
            return 'close_short_pw'
        if row['rsi_tw'] > 100-self.threshold:
            return 'close_long_pw'
        
class LTA_SAVUNIA(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=15,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_williams_r(df,self.period)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['williams_r'] < -100+self.threshold:  
            return 'long_pw'
        if row['williams_r'] > 0-self.threshold:  
            return 'short_pw'
        
class LTA_KOPATYCH(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=15,threshold=40):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_ultimate_oscillator(df,self.period//3,self.period//2,self.period)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['ultimate_oscillator'] < self.threshold:  
            return 'long_pw'
        if row['ultimate_oscillator'] > 100-self.threshold:  
            return 'short_pw'
        
class LTA_PIN(BaseTABitget):
    'period=15,period2=3,threshold=30,solution = 5'
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=15,period2=3,threshold=30,solution = 5):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.period2 = period2
        self.threshold = threshold
        self.solution = solution
    def preprocessing(self, df):
        df = add_rsi(df,self.period)
        df = add_rsi_tw(df,self.period)
        df = add_williams_r(df,self.period)
        df = add_mfi(df,self.period)
        df = add_ultimate_oscillator(df,self.period//3,self.period//2,self.period)
        df = add_cmo(df,self.period)
        df = add_cci(df,self.period)
        df = add_stochastic(df,self.period,self.period2)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        pins_solution = 0
        if row['rsi'] < self.threshold:  
            pins_solution += 1
        if row['rsi_tw'] < self.threshold:  
            pins_solution += 1
        if row['williams_r'] < -100+self.threshold:  
            pins_solution += 1
        if row['mfi'] < self.threshold:  
            pins_solution += 1
        if row['ultimate_oscillator'] < self.threshold+10:  
            pins_solution += 1
        if row['cmo'] < -100+self.threshold+10:  
            pins_solution += 1
        if row['cci'] < -200+self.threshold:  
            pins_solution += 1
        if row['%k'] > row['%d'] < self.threshold:  
            pins_solution += 1
        if row['rsi'] > 100-self.threshold:  
            pins_solution -= 1
        if row['rsi_tw'] > 100-self.threshold:  
            pins_solution -= 1
        if row['williams_r'] > 0-self.threshold:  
            pins_solution -= 1
        if row['mfi'] > 100-self.threshold:  
            pins_solution -= 1
        if row['ultimate_oscillator'] > 100-self.threshold-10:  
            pins_solution -= 1
        if row['cmo'] > 100-self.threshold-10:  
            pins_solution -= 1
        if row['cci'] > 200-self.threshold:  
            pins_solution -= 1
        if row['%k'] < row['%d'] > 100-self.threshold:  
            pins_solution -= 1
        if pins_solution > self.solution:
            return 'long_pw'
        if pins_solution < -self.solution:
            return 'short_pw'
        
class LTA_NUSHA(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=15,threshold=30):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_mfi(df,self.period)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['mfi'] < self.threshold:  
            return 'long_pw'
        if row['mfi'] > 100-self.threshold:  
            return 'short_pw'
        
class LTA_LOSYASH(BaseTABitget):
    def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=15,threshold=40):
        super().__init__(symbol, granularity, productType, n_parts, period)
        self.threshold = threshold
    def preprocessing(self, df):
        df = add_cmo(df,self.period)
        df = add_enter_price2close(df)  
        df = add_slice_df(df, self.period) 
        return df

    def __call__(self, row, *args, **kwds):
        if row['cmo'] < -100+self.threshold:  
            return 'long_pw'
        if row['cmo'] > 100-self.threshold:  
            return 'short_pw'