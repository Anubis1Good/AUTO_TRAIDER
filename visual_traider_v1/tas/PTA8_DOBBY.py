'''
бот на основе BB
'''
import cv2
import numpy as np
import pandas as pd
from tas.BaseTA import BaseTA,Keys
from utils.df_utils.indicators import add_rsi,add_slice_df,add_bollinger
from utils.df_utils.draw_df import draw_rsi,draw_df_BB_polyline

from dataclasses import dataclass

@dataclass
class KeysWRL1(Keys):
    row:pd.Series  


class PTA8_WDOBBYFrRL(BaseTA):
    '''trader,period_bb=11,multiplier=2,period_si=11,threshold=30'''
    def __init__(self, trader,period_bb=11,multiplier=2,period_si=11,threshold=30,*args):
        super().__init__(trader,*args)
        self.period_bb = period_bb
        self.multiplier = multiplier
        self.period_si = period_si
        self.threshold = threshold
    def get_keys(self, img)-> KeysWRL1:
        region = self.trader.chart_region
        chart = self.trader._get_chart(img,region)
        df = self.trader._get_df(chart)
        df = add_bollinger(df,self.period_bb,multiplier=self.multiplier)
        df = add_rsi(df,self.period_si)
        max_period = max(self.period_bb,self.period_si)
        df = add_slice_df(df,max_period)
        cur_price = self.trader._get_current_price(chart)

        if self.trader.mode in (2,3):
            draw_df_BB_polyline(df,chart)
            draw_rsi(df,chart)

        return KeysWRL1(
            cur_price=cur_price[1],
            row=df.iloc[-1]
        )

    def get_action(self, keys:KeysWRL1):
        row = keys.row
        nearest_long = keys.cur_price - row['high'] > row['low']  -  keys.cur_price
        if row['low'] > row['bbd']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long'
        if row['high'] < row['bbu']:
            if row['rsi'] > 100-self.threshold:
                return 'short'