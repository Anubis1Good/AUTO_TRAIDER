'''
Трейдер на основе отбоя адптивного канала Дончана с закрытие при выходе за среднюю линию
'''

import cv2
from tas.BaseTA import BaseTA,Keys
from utils.chart_utils.indicators import get_adaptive_DC
from dataclasses import dataclass

@dataclass
class KeysW(Keys):
    ups_fast:int
    downs_fast:int
    middle_fast:int
    h_last_hb:int
    l_last_hb:int


class PTA3_ADDC(BaseTA):
    def __init__(self, trader,period=15,multer=1.5,*args):
        super().__init__(trader,*args)
        self.period = period
        self.multer = multer
    def get_keys(self, img)-> KeysW:
        region = self.trader.chart_region
        chart = self.trader._get_chart(img,region)
        candle_mask = self.trader._get_candle_mask(chart)
        volume_mask = self.trader._get_volume_mask(chart)
        candle_cords = self.trader._get_cords_on_mask(candle_mask)
        volume_cords = self.trader._get_cords_on_mask(volume_mask)
        half_bars = self.trader._get_half_bars(candle_mask,candle_cords,volume_cords)
        cur_price = self.trader._get_current_price(chart)
        ups,downs,middle = get_adaptive_DC(half_bars,self.period,multer=self.multer)
        last_hb = half_bars[-1]
        if self.trader.mode != 1:
            cv2.polylines(chart,[ups],False,(255,0,200),2)
            cv2.polylines(chart,[downs],False,(55,200,250),2)
            cv2.polylines(chart,[middle],False,(155,100,250),2)

        return KeysW(
            cur_price=cur_price[1],
            ups_fast=ups[-1][1],
            downs_fast=downs[-1][1],
            middle_fast=middle[-1][1],
            h_last_hb=last_hb.yh,
            l_last_hb=last_hb.yl,
        )

    def get_action(self, keys:KeysW):
        if keys.h_last_hb == keys.ups_fast:
            return 'short'
        if keys.l_last_hb == keys.downs_fast:
            return 'long'
        if keys.cur_price < keys.middle_fast:
            return 'close_long'
        if keys.cur_price > keys.middle_fast:
            return 'close_short'

class PTA3a_ADDC(PTA3_ADDC):
    def get_action(self, keys:KeysW):
        if keys.h_last_hb == keys.ups_fast:
            return 'short'
        if keys.l_last_hb == keys.downs_fast:
            return 'long'
        if keys.h_last_hb < keys.middle_fast:
            return 'close_long'
        if keys.l_last_hb > keys.middle_fast:
            return 'close_short'