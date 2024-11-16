'''
workBot
'''
import numpy as np
import cv2
from tas.BaseTA import BaseTA,Keys
from utils.chart_utils.indicators import get_donchan_channel,get_SMA,get_FVG,get_adaptive_DC,get_borders
from dataclasses import dataclass

@dataclass
class KeysW(Keys):
    ups_fast:int
    downs_fast:int
    middle_fast:int
    h_last_hb:int
    l_last_hb:int


class WorkTA(BaseTA):
    def __init__(self, trader,period=20,*args):
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
        # volatility = np.array(list(map(lambda x: x.spred,half_bars)))
        # volatility = np.mean(volatility)
        # bullish_FGV,bearish_FGV = get_FVG(half_bars,volatility,2)
        ups,downs,middle = get_adaptive_DC(half_bars,self.period,multer=1.5)
        # sma = get_SMA(np.array(list(map(lambda x: x.mpt,half_bars))))
        top_line,bottom_line = get_borders(self.trader.chart_region,5)
        top_line2,bottom_line2 = get_borders(self.trader.chart_region,2)
        last_hb = half_bars[-1]
        if self.trader.mode != 1:
            cv2.line(chart,top_line[0],top_line[1],(200,33,150),2)
            cv2.line(chart,bottom_line[0],bottom_line[1],(100,233,250),2)
            cv2.line(chart,top_line2[0],top_line2[1],(200,233,50),2)
            # cv2.line(chart,bottom_line2[0],bottom_line2[1],(200,33,150),2)
            # cv2.polylines(chart,[ups],False,(255,0,200),2)
            # cv2.polylines(chart,[downs],False,(55,200,250),2)
            # cv2.polylines(chart,[middle],False,(155,100,250),2)
            # cv2.polylines(chart,[sma],False,(255,100,0),1)
            # for zone in bullish_FGV:
            #     cv2.rectangle(chart,zone[0],zone[1],(0,255,0),1)
            #     cv2.line(chart,zone[0],(zone[0][0]+200,zone[0][1]),(0,255,0))
            # for zone in bearish_FGV:
            #     cv2.rectangle(chart,zone[0],zone[1],(0,100,255),1)
            #     cv2.line(chart,zone[0],(zone[0][0]+200,zone[0][1]),(0,100,255))

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
