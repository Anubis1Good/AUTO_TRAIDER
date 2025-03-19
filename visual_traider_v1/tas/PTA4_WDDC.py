'''
Трейдер на основе отбоя адптивного канала Дончана с закрытие при выходе за среднюю линию
'''

import cv2
import pandas as pd
from tas.BaseTA import BaseTA,Keys
from utils.chart_utils.indicators import get_donchan_channel,get_strong_index, get_rocket_meteor_index,get_bull_power_index, get_donchan_channel_lite
from utils.test_utils.test_draws_funcs import draw_dhbs,draw_bollinger,draw_rsi
from dataclasses import dataclass

from utils.df_utils.indicators import add_donchan_channel,add_rsi,add_slice_df,add_vodka_channel
from utils.df_utils.draw_df import draw_df_chart,draw_df_DC_polyline,draw_df_VC_polyline,draw_rsi

@dataclass
class KeysW(Keys):
    ups_fast:int
    downs_fast:int
    middle_fast:int
    h_last_hb:int
    l_last_hb:int
    siu:int
    sid:int

@dataclass
class KeysW3(Keys):
    ups_fast:int
    downs_fast:int
    middle_fast:int
    h_last_hb:int
    l_last_hb:int
    bpi:int



class PTA4_WDDC(BaseTA):
    def __init__(self, trader,period_dc=15,period_si=14,threshold=20,*args):
        super().__init__(trader,*args)
        self.period_dc = period_dc
        self.period_si = period_si
        self.threshold = threshold
    def get_keys(self, img)-> KeysW:
        region = self.trader.chart_region
        chart = self.trader._get_chart(img,region)
        candle_mask = self.trader._get_candle_mask(chart)
        volume_mask = self.trader._get_volume_mask(chart)
        candle_cords = self.trader._get_cords_on_mask(candle_mask)
        volume_cords = self.trader._get_cords_on_mask(volume_mask)
        half_bars = self.trader._get_half_bars(candle_mask,candle_cords,volume_cords)
        cur_price = self.trader._get_current_price(chart)
        ups,downs,middle = get_donchan_channel(half_bars,self.period_dc)
        siu,sid = get_strong_index(half_bars,self.period_si)
        last_hb = half_bars[-1]
        if self.trader.mode in (2,3):
            cv2.polylines(chart,[ups],False,(255,0,200),2)
            cv2.polylines(chart,[downs],False,(55,200,250),2)
            cv2.polylines(chart,[middle],False,(155,100,250),2)
            cv2.polylines(chart,[siu],False,(255,0,200),2)
            cv2.polylines(chart,[sid],False,(55,200,250),2)

        return KeysW(
            cur_price=cur_price[1],
            ups_fast=ups[-1][1],
            downs_fast=downs[-1][1],
            middle_fast=middle[-1][1],
            h_last_hb=last_hb.yh,
            l_last_hb=last_hb.yl,
            siu=siu[-1][1],
            sid=sid[-1][1]
        )

    def get_action(self, keys:KeysW):
        delta = abs(keys.siu-keys.sid)
        if delta > self.threshold:
            if keys.h_last_hb == keys.ups_fast:
                return 'short'
            if keys.l_last_hb == keys.downs_fast:
                return 'long'
        if keys.cur_price < keys.middle_fast:
            return 'close_long'
        if keys.cur_price > keys.middle_fast:
            return 'close_short'

class PTA4_WDDC2(BaseTA):
    def __init__(self, trader,period_dc=15,period_si=14,threshold=20,*args):
        super().__init__(trader,*args)
        self.period_dc = period_dc
        self.period_si = period_si
        self.threshold = threshold
    def get_keys(self, img)-> KeysW:
        region = self.trader.chart_region
        chart = self.trader._get_chart(img,region)
        candle_mask = self.trader._get_candle_mask(chart)
        volume_mask = self.trader._get_volume_mask(chart)
        candle_cords = self.trader._get_cords_on_mask(candle_mask)
        volume_cords = self.trader._get_cords_on_mask(volume_mask)
        half_bars = self.trader._get_half_bars(candle_mask,candle_cords,volume_cords)
        cur_price = self.trader._get_current_price(chart)
        ups,downs,middle = get_donchan_channel(half_bars,self.period_dc)
        ri,mi = get_rocket_meteor_index(half_bars,self.period_si)
        last_hb = half_bars[-1]
        if self.trader.mode in (2,3):
            cv2.polylines(chart,[ups],False,(255,0,200),2)
            cv2.polylines(chart,[downs],False,(55,200,250),2)
            cv2.polylines(chart,[middle],False,(155,100,250),2)
            cv2.polylines(chart,[ri],False,(255,0,200),2)
            cv2.polylines(chart,[mi],False,(55,200,250),2)

        return KeysW(
            cur_price=cur_price[1],
            ups_fast=ups[-1][1],
            downs_fast=downs[-1][1],
            middle_fast=middle[-1][1],
            h_last_hb=last_hb.yh,
            l_last_hb=last_hb.yl,
            siu=ri[-1][1],
            sid=mi[-1][1]
        )

    def get_action(self, keys:KeysW):
        delta = abs(keys.siu-keys.sid)
        if delta > self.threshold:
            if keys.h_last_hb == keys.ups_fast:
                return 'short'
            if keys.l_last_hb == keys.downs_fast:
                return 'long'
        if keys.cur_price < keys.middle_fast:
            return 'close_long'
        if keys.cur_price > keys.middle_fast:
            return 'close_short'


class PTA4_WDDC3(BaseTA):
    def __init__(self, trader,period_dc=15,period_bpi=15,limits=30,*args):
        super().__init__(trader,*args)
        self.period_dc = period_dc
        self.period_bpi = period_bpi
        self.limits = limits
    def get_keys(self, img)-> KeysW:
        region = self.trader.chart_region
        chart = self.trader._get_chart(img,region)
        dhbs = self.trader._get_dir_half_bars(chart)
        cur_price = self.trader._get_current_price(chart)
        bpi = get_bull_power_index(dhbs,self.period_bpi)
        max_hb,min_hb,middle_hb = get_donchan_channel_lite(dhbs,self.period_dc)
        last_hb = dhbs[-1]
        if self.trader.mode in (2,0):
            draw_dhbs(chart,dhbs)
            draw_rsi(chart,bpi,dhbs,30)
            cv2.circle(chart,(dhbs[-1].x,max_hb),1,(255,255,255))
            cv2.circle(chart,(dhbs[-1].x,min_hb),1,(255,255,255))
            cv2.circle(chart,(dhbs[-1].x,middle_hb),1,(255,255,255))

        return KeysW3(
            cur_price=cur_price[1],
            ups_fast=max_hb,
            downs_fast=min_hb,
            middle_fast=middle_hb,
            h_last_hb=last_hb.yh,
            l_last_hb=last_hb.yl,
            bpi=bpi[-1][1]
        )

    def get_action(self, keys:KeysW3):
        if keys.h_last_hb == keys.ups_fast and keys.bpi > 100-self.limits:
            return 'short'
        if keys.l_last_hb == keys.downs_fast and keys.bpi < self.limits:
            return 'long'
        if keys.cur_price < keys.middle_fast:
            return 'close_long'
        if keys.cur_price > keys.middle_fast:
            return 'close_short'
        
class PTA4_WDDC3b(PTA4_WDDC3):
    def get_action(self, keys:KeysW3):
        if keys.h_last_hb == keys.ups_fast and keys.bpi > 100-self.limits:
            return 'short'
        if keys.l_last_hb == keys.downs_fast and keys.bpi < self.limits:
            return 'long'
        if keys.h_last_hb == keys.ups_fast:
            return 'close_long'
        if keys.l_last_hb == keys.downs_fast:
            return 'close_short'

@dataclass
class KeysWRL1(Keys):
    row:pd.Series  
class PTA4_WDDCrRL(BaseTA):
    def __init__(self, trader,period_dc=11,period_si=11,threshold=30,*args):
        super().__init__(trader,*args)
        self.period_dc = period_dc
        self.period_si = period_si
        self.threshold = threshold
    def get_keys(self, img)-> KeysWRL1:
        region = self.trader.chart_region
        chart = self.trader._get_chart(img,region)
        df = self.trader._get_df(chart)
        df = add_donchan_channel(df,self.period_dc)
        df = add_rsi(df,self.period_si)
        max_period = max(self.period_dc,self.period_si)
        df = add_slice_df(df,max_period)
        cur_price = self.trader._get_current_price(chart)

        if self.trader.mode in (2,3):
            draw_df_DC_polyline(df,chart)
            draw_rsi(df,chart)

        return KeysWRL1(
            cur_price=cur_price[1],
            row=df.iloc[-1]
        )

    def get_action(self, keys:KeysWRL1):
        row = keys.row
        nearest_long = keys.cur_price - row['high'] > row['low']  -  keys.cur_price
        if row['low'] == row['min_hb']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long'
        if row['high'] == row['max_hb']:
            if row['rsi'] > 100-self.threshold:
                return 'short'
            
class PTA4_WWEDDCrRL(BaseTA):
    def __init__(self, trader,period_dc=11,period_si=11,threshold=20,threshold_c=35,*args):
        super().__init__(trader,*args)
        self.period_dc = period_dc
        self.period_si = period_si
        self.threshold = threshold
        self.threshold_c = threshold_c
    def get_keys(self, img)-> KeysWRL1:
        region = self.trader.chart_region
        chart = self.trader._get_chart(img,region)
        df = self.trader._get_df(chart)
        df = add_donchan_channel(df,self.period_dc)
        df = add_rsi(df,self.period_si)
        max_period = max(self.period_dc,self.period_si)
        df = add_slice_df(df,max_period)
        cur_price = self.trader._get_current_price(chart)

        if self.trader.mode in (2,3):
            draw_df_DC_polyline(df,chart)
            draw_rsi(df,chart)

        return KeysWRL1(
            cur_price=cur_price[1],
            row=df.iloc[-1]
        )

    def get_action(self, keys:KeysWRL1):
        row = keys.row
        nearest_long = keys.cur_price - row['high'] > row['low']  -  keys.cur_price
        if row['low'] == row['min_hb']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long'
        if row['high'] == row['max_hb']:
            if row['rsi'] > 100-self.threshold:
                return 'short'
        if row['rsi'] < self.threshold_c:
            return 'close_short'
        if row['rsi'] > 100-self.threshold_c:
            return 'close_long'
        
            
class PTA4_WDVCrRL(BaseTA):
    def __init__(self, trader,period_vc=11,period_si=11,threshold=30,*args):
        super().__init__(trader,*args)
        self.period_vc = period_vc
        self.period_si = period_si
        self.threshold = threshold
    def get_keys(self, img)-> KeysWRL1:
        region = self.trader.chart_region
        chart = self.trader._get_chart(img,region)
        df = self.trader._get_df(chart)
        df = add_vodka_channel(df,self.period_vc)
        df = add_rsi(df,self.period_si)
        max_period = max(self.period_vc,self.period_si)
        df = add_slice_df(df,max_period)
        cur_price = self.trader._get_current_price(chart)

        if self.trader.mode in (2,3):
            draw_df_VC_polyline(df,chart)
            draw_rsi(df,chart)

        return KeysWRL1(
            cur_price=cur_price[1],
            row=df.iloc[-1]
        )

    def get_action(self, keys:KeysWRL1):
        row = keys.row
        nearest_long = keys.cur_price - row['high'] > row['low']  -  keys.cur_price
        if row['low'] > row['bottom_mean']:
            if nearest_long:
                if row['rsi'] < self.threshold:
                    return 'long'
        if row['high'] < row['top_mean']:
            if row['rsi'] > 100-self.threshold:
                return 'short'
