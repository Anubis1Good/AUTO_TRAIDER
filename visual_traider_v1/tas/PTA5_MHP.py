'''
Майкл Харрис паттерн
'''

import cv2
from tas.BaseTA import BaseTA,Keys
from utils.chart_utils.indicators import check_michael_harris_pattern
from dataclasses import dataclass

@dataclass
class KeysW(Keys):
    long_pattern:bool
    short_pattern:bool



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


        if self.trader.mode in (2,0):
            1
            # cv2.polylines(chart,[ups],False,(255,0,200),2)
            # cv2.polylines(chart,[downs],False,(55,200,250),2)
            # cv2.polylines(chart,[middle],False,(155,100,250),2)
            # cv2.polylines(chart,[siu],False,(255,0,200),2)
            # cv2.polylines(chart,[sid],False,(55,200,250),2)

        return KeysW(
            cur_price=cur_price[1],
            long_pattern=long_pattern,
            short_pattern=short_pattern

        )

    def get_action(self, keys:KeysW):
        if keys.short_pattern:
            return 'short'
        if keys.long_pattern:
            return 'long'
        # if keys.cur_price < keys.middle_fast:
        #     return 'close_long'
        # if keys.cur_price > keys.middle_fast:
        #     return 'close_short'

