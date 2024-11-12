'''
Трейдер на основе пробоя канала Дончана со стопом за среднюю линию при тренде
'''

import numpy as np
import cv2
from tas.BaseTA import BaseTA,Keys
from utils.chart_utils.indicators import get_donchan_channel,get_dynamics
from dataclasses import dataclass

@dataclass
class KeysW(Keys):
    ups_fast:int
    downs_fast:int
    middle_fast:int
    h_last_hb:int
    l_last_hb:int
    ups_slow:int
    downs_slow:int
    middle_slow:int
    stop_up:int
    stop_down:int

class PTA1_BDDC(BaseTA):
    def get_keys(self, img)-> KeysW:
        region = self.trader.chart_region
        chart = self.trader._get_chart(img,region)
        candle_mask = self.trader._get_candle_mask(chart)
        volume_mask = self.trader._get_volume_mask(chart)
        candle_cords = self.trader._get_cords_on_mask(candle_mask)
        volume_cords = self.trader._get_cords_on_mask(volume_mask)
        half_bars = self.trader._get_half_bars(candle_mask,candle_cords,volume_cords)
        cur_price = self.trader._get_current_price(chart)
        ups,downs,middle = get_donchan_channel(half_bars)
        ups1,downs1,middle1 = get_donchan_channel(half_bars,40)
        last_hb = half_bars[-1]
        if self.trader.mode != 1:
            cv2.polylines(chart,[ups],False,(255,0,200),2)
            cv2.polylines(chart,[downs],False,(55,200,250),2)
            cv2.polylines(chart,[middle],False,(155,100,250),2)
            cv2.polylines(chart,[ups1],False,(255,0,200),1)
            cv2.polylines(chart,[downs1],False,(55,200,250),1)
            cv2.polylines(chart,[middle1],False,(155,100,250),1)


        return KeysW(
            cur_price=cur_price[1],
            ups_fast=ups[-1][1],
            downs_fast=downs[-1][1],
            middle_fast=middle[-1][1],
            h_last_hb=last_hb.yh,
            l_last_hb=last_hb.yl,
            ups_slow=ups1[-1][1],
            downs_slow=downs1[-1][1],
            middle_slow=middle1[-1][1],
            stop_up=ups1[-10][1],
            stop_down=downs1[-10][1]
        )

    def get_action(self, keys:KeysW):
        if keys.h_last_hb == keys.ups_fast:
            return 'long'
        if keys.l_last_hb == keys.downs_fast:
            return 'short'
        if keys.cur_price < keys.middle_fast:
            return 'close_short'
        if keys.cur_price > keys.middle_fast:
            return 'close_long'

class PTA1_R_BDDC(PTA1_BDDC):
    def get_action(self, keys):
        if keys.h_last_hb == keys.ups_fast:
            return 'short'
        if keys.l_last_hb == keys.downs_fast:
            return 'long'
        if keys.cur_price < keys.middle_fast:
            return 'close_long'
        if keys.cur_price > keys.middle_fast:
            return 'close_short'
        
class PTA1_R2_BDDC(PTA1_BDDC):
    def get_action(self, keys):
        if keys.ups_fast != keys.ups_slow:
            if keys.h_last_hb == keys.ups_fast:
                return 'short'
        if keys.downs_fast != keys.downs_slow:
            if keys.l_last_hb == keys.downs_fast:
                return 'long'
        if keys.cur_price < keys.middle_fast:
            return 'close_long'
        if keys.cur_price > keys.middle_fast:
            return 'close_short'
        
class PTA1_R3_BDDC(PTA1_BDDC):
    def get_action(self, keys):
        if keys.cur_price > keys.stop_down:
            return 'close_long'
        if keys.cur_price < keys.stop_up:
            return 'close_short'
        if keys.ups_fast != keys.ups_slow:
            if keys.h_last_hb == keys.ups_fast:
                return 'short'
        if keys.downs_fast != keys.downs_slow:
            if keys.l_last_hb == keys.downs_fast:
                return 'long'
        if keys.cur_price < keys.middle_fast:
            return 'close_long'
        if keys.cur_price > keys.middle_fast:
            return 'close_short'
        
class PTA1_R4_BDDC(PTA1_BDDC):
    def get_action(self, keys):
        width_fast = keys.downs_fast - keys.ups_fast
        width_slow = keys.downs_slow - keys.ups_slow
        range_target = width_slow/2 > width_fast
        if keys.cur_price > keys.stop_down:
            return 'close_long'
        if keys.cur_price < keys.stop_up:
            return 'close_short'
        if keys.ups_fast != keys.ups_slow:
            if keys.h_last_hb == keys.ups_fast:
                return 'short'
        if keys.downs_fast != keys.downs_slow:
            if keys.l_last_hb == keys.downs_fast:
                return 'long'
        if range_target:
            if keys.cur_price == keys.ups_fast:
                return 'close_long'
            if keys.cur_price == keys.downs_fast:
                return 'close_short'
        else:
            if keys.cur_price < keys.middle_fast:
                return 'close_long'
            if keys.cur_price > keys.middle_fast:
                return 'close_short'
            
class PTA1_R5_BDDC(PTA1_BDDC):
    def get_action(self, keys):
        if keys.h_last_hb == keys.ups_slow:
            return 'short'
        if keys.l_last_hb == keys.downs_slow:
            return 'long'
        if keys.cur_price < keys.middle_slow:
            return 'close_long'
        if keys.cur_price > keys.middle_slow:
            return 'close_short'