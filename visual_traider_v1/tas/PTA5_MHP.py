'''
Майкл Харрис паттерн
'''

import cv2
import numpy as np
from tas.BaseTA import BaseTA,Keys
from utils.chart_utils.indicators import check_michael_harris_pattern,get_SMA
from dataclasses import dataclass

@dataclass
class KeysW(Keys):
    long_pattern:bool
    short_pattern:bool
    stop_long:int
    stop_short:int
    take_long:int
    take_short:int



class PTA5_MHP(BaseTA):
    def __init__(self, trader,*args):
        super().__init__(trader,*args)
    def get_keys(self, img)-> KeysW:
        region = self.trader.chart_region
        chart = self.trader._get_chart(img,region)
        candle_mask = self.trader._get_candle_mask(chart)
        volume_mask = self.trader._get_volume_mask(chart)
        candle_cords = self.trader._get_cords_on_mask(candle_mask)
        volume_cords = self.trader._get_cords_on_mask(volume_mask)
        half_bars = self.trader._get_half_bars(candle_mask,candle_cords,volume_cords)
        cur_price = self.trader._get_current_price(chart)
        long_pattern = check_michael_harris_pattern(half_bars)
        short_pattern = check_michael_harris_pattern(half_bars,False)

        volatility = list(map(lambda x: x.spred_pt,half_bars))
        volatility = get_SMA(np.array(volatility),14)

        stop_long = (half_bars[-1].x,half_bars[-1].yl+volatility[-1][1]*2)
        stop_short = (half_bars[-1].x,half_bars[-1].yh-volatility[-1][1]*2)

        take_long = (half_bars[-1].x,half_bars[-1].yh-volatility[-1][1]*4)
        take_short = (half_bars[-1].x,half_bars[-1].yl+volatility[-1][1]*4)

        
        if not self.trader.free_stop_l:
            stop_long = stop_long if stop_long[1] < self.trader.stop_long else (half_bars[-1].x,self.trader.stop_long)
            take_long = (half_bars[-1].x,self.trader.take_long)
        if not self.trader.free_stop_s:
            stop_short = stop_short if stop_short[1] > self.trader.stop_short else (half_bars[-1].x,self.trader.stop_short)
            take_short = (half_bars[-1].x,self.trader.take_short)

        if self.trader.mode in (2,0):
            cv2.circle(chart,stop_long,1,(0,255,255),1)
            cv2.circle(chart,take_long,1,(0,255,255),2)
            cv2.circle(chart,stop_short,1,(255,0,255),1)
            cv2.circle(chart,take_short,1,(255,0,255),2)
            # cv2.polylines(chart,[ups],False,(255,0,200),2)
            # cv2.polylines(chart,[downs],False,(55,200,250),2)
            # cv2.polylines(chart,[middle],False,(155,100,250),2)
            # cv2.polylines(chart,[siu],False,(255,0,200),2)
            # cv2.polylines(chart,[sid],False,(55,200,250),2)

        return KeysW(
            cur_price=cur_price[1],
            long_pattern=long_pattern,
            short_pattern=short_pattern,
            stop_long=stop_long[1],
            stop_short=stop_short[1],
            take_long=take_long[1],
            take_short=take_short[1]

        )

    def get_action(self, keys:KeysW):
        if keys.short_pattern:
            return 'short'
        if keys.long_pattern:
            return 'long'
        if self.trader.have_pos_l:
            if keys.cur_price < keys.take_long or keys.cur_price > keys.stop_long:
                return 'close_long'
        if self.trader.have_pos_s:
            if keys.cur_price > keys.take_short or keys.cur_price < keys.stop_short:
                return 'close_short'

