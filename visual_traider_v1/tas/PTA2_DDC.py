'''
Трейдер на основе отбоя канала Дончана с закрытие при выходе за серднюю линию
'''

import cv2
from tas.BaseTA import BaseTA,Keys
from utils.chart_utils.indicators import get_donchan_channel,get_van_gerchick_p,get_donchan_channel_lite
from dataclasses import dataclass

@dataclass
class KeysW(Keys):
    ups_fast:int
    downs_fast:int
    middle_fast:int
    h_last_hb:int
    l_last_hb:int

@dataclass
class KeysW2(Keys):
    ups_fast:int
    downs_fast:int
    middle_up:int
    middle_down:int
    h_last_hb:int
    l_last_hb:int


class PTA2_DDC(BaseTA):
    def __init__(self, trader,period=60,*args):
        super().__init__(trader,*args)
        self.period = period
    def get_keys(self, img)-> KeysW:
        region = self.trader.chart_region
        chart = self.trader._get_chart(img,region)
        candle_mask = self.trader._get_candle_mask(chart)
        volume_mask = self.trader._get_volume_mask(chart)
        candle_cords = self.trader._get_cords_on_mask(candle_mask)
        volume_cords = self.trader._get_cords_on_mask(volume_mask)
        half_bars = self.trader._get_half_bars(candle_mask,candle_cords,volume_cords)
        cur_price = self.trader._get_current_price(chart)
        ups,downs,middle = get_donchan_channel(half_bars,self.period)
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

class PTA2a_DDC(PTA2_DDC):
    def get_action(self, keys:KeysW):
        if keys.h_last_hb == keys.ups_fast:
            return 'short'
        if keys.l_last_hb == keys.downs_fast:
            return 'long'
        if keys.h_last_hb < keys.middle_fast:
            return 'close_long'
        if keys.l_last_hb > keys.middle_fast:
            return 'close_short'

class PTA2_DDC2(BaseTA):
    def __init__(self, trader,period=60,*args):
        super().__init__(trader,*args)
        self.period = period
    def get_keys(self, img)-> KeysW2:
        region = self.trader.chart_region
        chart = self.trader._get_chart(img,region)
        candle_mask = self.trader._get_candle_mask(chart)
        volume_mask = self.trader._get_volume_mask(chart)
        candle_cords = self.trader._get_cords_on_mask(candle_mask)
        volume_cords = self.trader._get_cords_on_mask(volume_mask)
        half_bars = self.trader._get_half_bars(candle_mask,candle_cords,volume_cords)
        cur_price = self.trader._get_current_price(chart)
        max_hb,min_hb,middle_hb = get_donchan_channel_lite(half_bars,self.period)
        up,down,mup,mdown = get_van_gerchick_p(max_hb,min_hb,middle_hb)
        last_hb = half_bars[-1]
        if self.trader.mode in (2,3):
            cv2.circle(chart,(half_bars[-1].x,up),1,(255,255,255))
            cv2.circle(chart,(half_bars[-1].x,down),1,(255,255,255))
            cv2.circle(chart,(half_bars[-1].x,mup),1,(255,255,255))
            cv2.circle(chart,(half_bars[-1].x,mdown),1,(255,255,255))
            cv2.circle(chart,(half_bars[-1].x,max_hb),1,(255,255,255))
            cv2.circle(chart,(half_bars[-1].x,min_hb),1,(255,255,255))
            cv2.circle(chart,(half_bars[-1].x,middle_hb),1,(255,255,255))

        return KeysW2(
            cur_price=cur_price[1],
            ups_fast=up,
            downs_fast=down,
            middle_up=mup,
            middle_down=mdown,
            h_last_hb=last_hb.yh,
            l_last_hb=last_hb.yl,
        )
    def get_action(self, keys:KeysW2):
        if keys.h_last_hb <= keys.ups_fast:
            return 'short'
        if keys.l_last_hb >= keys.downs_fast:
            return 'long'
        if keys.cur_price <= keys.middle_down:
            return 'close_long'
        if keys.cur_price >= keys.middle_up:
            return 'close_short'
        
class PTA2a_DDC2(PTA2_DDC2):
    def get_action(self, keys:KeysW2):
        if keys.h_last_hb <= keys.ups_fast:
            return 'short'
        if keys.l_last_hb >= keys.downs_fast:
            return 'long'
        if keys.h_last_hb <= keys.middle_down:
            return 'close_long'
        if keys.l_last_hb >= keys.middle_up:
            return 'close_short'