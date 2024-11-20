'''
Трейдер на основе отбоя адптивного канала Дончана с закрытие при выходе за среднюю линию
'''

import cv2
from tas.BaseTA import BaseTA,Keys
from utils.chart_utils.VSA import VSA
from utils.chart_utils.dtype import FullBar
from dataclasses import dataclass

@dataclass
class KeysW(Keys):
    last_fb:FullBar



class OGTA1_Rails(BaseTA):
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
        vsa = VSA(half_bars)
        last_fb = vsa.full_bars[-1]
        if self.trader.mode in (2,3):
            pass

        return KeysW(
            cur_price=cur_price[1],
            last_fb=last_fb

        )

    def get_action(self, keys:KeysW):
        if keys.last_fb.over_vsai:
            if keys.cur_price > keys.last_fb.yl:
                return 'short'
            if keys.cur_price < keys.last_fb.yh:
                return 'long'
        # if keys.cur_price < keys.top_close:
        #     return 'close_long'
        # if keys.cur_price > keys.top_close:
        #     return 'close_short'


