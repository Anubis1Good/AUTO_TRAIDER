from from_rich_laughter.indicators import add_donchan_channel,add_slice_df,add_big_volume,add_dynamics_ma,add_bollinger,add_over_bb,add_enter_price,add_donchan_middle,add_donchan_prev,add_buffer_add,add_buffer_sub,add_vangerchik,add_simple_dynamics_ma,add_vodka_channel,add_rsi,add_enter_price2close,add_macd

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