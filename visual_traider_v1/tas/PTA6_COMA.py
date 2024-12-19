'''
Пересечение скальзяшек
'''

import cv2
import numpy as np
from tas.BaseTA import BaseTA,Keys
from utils.chart_utils.indicators import get_bollinger_bands,get_donchan_channel,get_bull_power_index, get_SMA
from utils.test_utils.test_draws_funcs import draw_dhbs,draw_bollinger,draw_rsi
from dataclasses import dataclass

@dataclass
class KeysW(Keys):
    sma_f:int
    sma_s:int



class PTA6_COMA(BaseTA):
    def __init__(self, trader,fast_period:int=15,slow_period:int=30,*args):
        super().__init__(trader,*args)
        self.fast_period = fast_period
        self.slow_period = slow_period
    def get_keys(self, img)-> KeysW:
        region = self.trader.chart_region
        chart = self.trader._get_chart(img,region)
        dhbs = self.trader._get_dir_half_bars(chart)
        cur_price = self.trader._get_current_price(chart)
        # bpi = get_bull_power_index(dhbs,14)
        mpts = np.array(list(map(lambda x: x.mpt,dhbs)))
        sma_f = get_SMA(mpts,self.fast_period)
        sma_s = get_SMA(mpts,self.slow_period)
        # sma_sm,bbu_sm,bbd_sm = get_bollinger_bands(np.array(mpts),step=60)
        # ups,downs,middle = get_donchan_channel(dhbs,20)
        if self.trader.mode in (2,0):
            0
            # draw_dhbs(chart,dhbs)
            # draw_rsi(chart,bpi,dhbs,30)
            # draw_bollinger(chart,sma_sm,bbu_sm,bbd_sm)
            # draw_bollinger(chart,ups,downs,middle,(0,200,0))
            # cv2.circle(chart,stop_long,1,(0,255,255),1)
            # cv2.circle(chart,take_long,1,(0,255,255),2)
            # cv2.circle(chart,stop_short,1,(255,0,255),1)
            # cv2.circle(chart,take_short,1,(255,0,255),2)
            cv2.polylines(chart,[sma_f],False,(255,0,200),1)
            cv2.polylines(chart,[sma_s],False,(255,200,200),1)
            # cv2.polylines(chart,[downs],False,(55,200,250),2)
            # cv2.polylines(chart,[middle],False,(155,100,250),2)
            # cv2.polylines(chart,[siu],False,(255,0,200),2)
            # cv2.polylines(chart,[sid],False,(55,200,250),2)

        return KeysW(
            cur_price=cur_price[1],
            sma_f=sma_f[-1][1],
            sma_s=sma_s[-1][1]
        )

    def get_action(self, keys:KeysW):
        if keys.sma_s > keys.sma_f:
            return 'long'
        if keys.sma_s < keys.sma_f:
            return 'short'
        # if keys.short_pattern:
        #     return 'short'
        # if keys.long_pattern:
        #     return 'long'
        # if self.trader.have_pos_l:
        #     if keys.cur_price < keys.take_long or keys.cur_price > keys.stop_long:
        #         return 'close_long'
        # if self.trader.have_pos_s:
        #     if keys.cur_price > keys.take_short or keys.cur_price < keys.stop_short:
        #         return 'close_short'

