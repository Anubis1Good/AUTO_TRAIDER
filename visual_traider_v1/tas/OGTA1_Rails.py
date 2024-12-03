'''
Трейдер на основе отбоя адптивного канала Дончана с закрытие при выходе за среднюю линию
'''

import cv2
from tas.BaseTA import BaseTA,Keys
from utils.chart_utils.VSA import VSA
from utils.chart_utils.dtype import FullBar,HalfBar
from dataclasses import dataclass
from utils.middlewares.reverse import simple_reverse

@dataclass
class KeysW(Keys):
    last_hb:HalfBar



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
        last_hb = half_bars[-2]
        # vsa = VSA(half_bars)
        # last_fb = vsa.full_bars[-1]
        if self.trader.mode in (2,3):
            pass

        return KeysW(
            cur_price=cur_price[1],
            last_hb=last_hb

        )
    def classic_get_action(self, keys:KeysW):
        if keys.cur_price > keys.last_hb.yl:
            return 'short'
        if keys.cur_price < keys.last_hb.yh:
            return 'long'
        
    def get_action(self, keys:KeysW):
        return simple_reverse(self.classic_get_action(keys))
        # if keys.cur_price < keys.top_close:
        #     return 'close_long'
        # if keys.cur_price > keys.top_close:
        #     return 'close_short'


