'''
Пересечение скальзяшек
'''

import cv2
import numpy as np
from tas.BaseTA import BaseTA,Keys
from utils.chart_utils.indicators import get_bollinger_bands,get_donchan_channel,get_bull_power_index, get_SMA, get_williams_fractals,get_extreme_walker
from utils.test_utils.test_draws_funcs import draw_dhbs,draw_bollinger,draw_rsi, draw_points
from dataclasses import dataclass

@dataclass
class KeysW(Keys):
    sma_f:int
    sma_s:int
    sma_h:int
    sma_l:int



class PTA6_COMA(BaseTA):
    def __init__(self, trader,fast_period:int=30,slow_period:int=60,*args):
        super().__init__(trader,*args)
        self.fast_period = fast_period
        self.slow_period = slow_period
    def get_keys(self, img)-> KeysW:
        region = self.trader.chart_region
        chart = self.trader._get_chart(img,region)
        dhbs = self.trader._get_dir_half_bars(chart)
        cur_price = self.trader._get_current_price(chart)
        # bpi = get_bull_power_index(dhbs,15)
        mpts = np.array(list(map(lambda x: x.mpt,dhbs)))
        hpts = np.array(list(map(lambda x: x.hpt,dhbs)))
        lpts = np.array(list(map(lambda x: x.lpt,dhbs)))
        sma_f = get_SMA(mpts,self.fast_period)
        sma_s = get_SMA(mpts,self.slow_period)
        sma_h = get_SMA(hpts,3)
        sma_l = get_SMA(lpts,3)
        # epts = get_extreme_walker(sma_m)
        # maxs,mins = get_williams_fractals(sma_m,sma_m)
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
            cv2.polylines(chart,[sma_h],False,(55,200,100),1)
            cv2.polylines(chart,[sma_l],False,(155,100,100),1)
            # draw_points(chart,epts,(100,200,100),two_classes=True)
            # draw_points(chart,mins,(200,100,200))
            # draw_points(chart,maxs,(50,200,100))
            # cv2.polylines(chart,[downs],False,(55,200,250),2)
            # cv2.polylines(chart,[middle],False,(155,100,250),2)
            # cv2.polylines(chart,[siu],False,(255,0,200),2)
            # cv2.polylines(chart,[sid],False,(55,200,250),2)

        return KeysW(
            cur_price=cur_price[1],
            sma_f=sma_f[-1][1],
            sma_s=sma_s[-1][1],
            sma_h= sma_h[-1][1],
            sma_l= sma_l[-1][1]
        )

    def get_action(self, keys:KeysW):
        if keys.sma_s > keys.sma_f:
            if keys.sma_l > keys.sma_f:
                return 'long'
        if keys.sma_s < keys.sma_f:
            if keys.sma_h < keys.sma_f:
                return 'short'
        # if self.trader.have_pos_l:
        #     if keys.cur_price < keys.take_long or keys.cur_price > keys.stop_long:
        #         return 'close_long'
        # if self.trader.have_pos_s:
        #     if keys.cur_price > keys.take_short or keys.cur_price < keys.stop_short:
        #         return 'close_short'

