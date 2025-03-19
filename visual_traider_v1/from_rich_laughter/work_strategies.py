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