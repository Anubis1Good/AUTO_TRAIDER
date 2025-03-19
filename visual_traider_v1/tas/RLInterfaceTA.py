'''
Интерфейс для стратегий из RL с использованием внешних данных
'''
# import cv2
from datetime import date, timedelta,datetime
import numpy as np
import pandas as pd
from tas.BaseTA import BaseTA,Keys
from from_rich_laughter.download_moex import download_moex,create_df,convert_chart1to5
from utils.name_decoder import decoder_name
from from_rich_laughter.id_ws import ids_wss
# from utils.df_utils.indicators import add_rsi,add_slice_df,add_bollinger
# from utils.df_utils.draw_df import draw_rsi,draw_df_BB_polyline

# from dataclasses import dataclass

# @dataclass
# class KeysWRL1(Keys):
#     row:pd.Series  


time_format = "%Y-%m-%d %H:%M:%S"
class RLITA1(BaseTA):
    "trader,convert1to5=False,id_strategy='0'"
    def __init__(self, trader,convert1to5=False,id_strategy='0',*args):
        super().__init__(trader,*args)
        self.convert1to5 = convert1to5
        self.ticker,self.board,self.market,self.engine = decoder_name(self.trader.name)
        today = date.today()
        self.yesterday = str(today - timedelta(days=2))
        self.ws = ids_wss[id_strategy]
    def get_keys(self, img)-> Keys:
        return Keys(-1)
    def convert_action(self,action):
        if action:
            if 'close_long' in action:
                return 'close_long'
            if 'close_short' in action:
                return 'close_short'
            if 'long' in action:
                return 'long'
            if 'short' in action:
                return 'short'
            if 'close_all' in action:
                return 'close_all'
    def get_action(self, keys:None):
        action = None
        try:
            df = download_moex(self.ticker,1,self.yesterday,board=self.board,market=self.market,engine=self.engine)
            df = create_df(df)
            if self.convert1to5:
                df = convert_chart1to5(df)
            row = self.ws.get_test_row(df)
            # print(row)
            t = datetime.now()
            delta= (t - datetime.strptime(str(row['ms']),time_format)).total_seconds()/60
            if delta < 7:
                action = self.convert_action(self.ws(row))
            else:
                print('RLITA1',self.ticker,'big deltatime',delta)
        except:
            print('RLITA1',self.ticker,'have some problems')
        # print(action)
        return action
