'''
Интерфейс для стратегий из RL с использованием внешних данных
'''
# import cv2
import numpy as np
import pandas as pd
from tas.BaseTA import BaseTA,Keys
from from_rich_laughter.download_moex import download_moex,create_df
# from utils.df_utils.indicators import add_rsi,add_slice_df,add_bollinger
# from utils.df_utils.draw_df import draw_rsi,draw_df_BB_polyline

# from dataclasses import dataclass

# @dataclass
# class KeysWRL1(Keys):
#     row:pd.Series  


class RLITA1(BaseTA):
    '''trader,period_bb=11,multiplier=2,period_si=11,threshold=30'''
    def __init__(self, trader,*args):
        super().__init__(trader,*args)
        self.
    def get_keys(self, img)-> None:
        return None

    def get_action(self, keys:None):
        df = download_moex(ticker,1,yesterday,board=board,market=market,engine=engine)
        df = create_df(df)

        
        # row = keys.row
        # nearest_long = keys.cur_price - row['high'] > row['low']  -  keys.cur_price
        # if row['low'] > row['bbd']:
        #     if nearest_long:
        #         if row['rsi'] < self.threshold:
        #             return 'long'
        # if row['high'] < row['bbu']:
        #     if row['rsi'] > 100-self.threshold:
        #         return 'short'