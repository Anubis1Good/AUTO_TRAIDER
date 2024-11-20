'''
workBot
'''
import numpy as np
import cv2
from tas.BaseTA import BaseTA,Keys
from utils.chart_utils.indicators import *
from utils.chart_utils.VSA import VSA
from utils.test_utils.test_draws_funcs import draw_bollinger
from dataclasses import dataclass




class WorkTA(BaseTA):
    def __init__(self, trader,period=20,*args):
        super().__init__(trader,*args)
        self.period = period
    def get_keys(self, img)-> Keys:
        region = self.trader.chart_region
        chart = self.trader._get_chart(img,region)
        candle_mask = self.trader._get_candle_mask(chart)
        volume_mask = self.trader._get_volume_mask(chart)
        candle_cords = self.trader._get_cords_on_mask(candle_mask)
        volume_cords = self.trader._get_cords_on_mask(volume_mask)
        half_bars = self.trader._get_half_bars(candle_mask,candle_cords,volume_cords)
        cur_price = self.trader._get_current_price(chart)
        vsa = VSA(half_bars)
        # volatility = np.array(list(map(lambda x: x.spred,half_bars)))
        mpts = np.array(list(map(lambda x: x.mpt,half_bars)))
        # volatility = np.mean(volatility)
        # bullish_FGV,bearish_FGV = get_FVG(half_bars,volatility,2)
        ups,downs,middle = get_donchan_channel(half_bars,60)
        bbm,bbu,bbd = get_bollinger_bands(mpts)
        rsi = get_rsi(half_bars)
        # siu,sid = get_strong_index(half_bars)
        ri,mi = get_rocket_meteor_index(half_bars,14)
        # sma = get_SMA(np.array(list(map(lambda x: x.mpt,half_bars))))
        print(rsi)
        print(ri[-1][1])
        print(mi[-1][1])
        if ri[-1][1] > 60:
            print('long')
        elif mi[-1][1] > 60:
            print('short')
        else:
            print('range')
        if self.trader.mode != 1:
            vsa.draw_all(chart)
            # cv2.polylines(chart,[ri],False,(0,200,100),2)
            # cv2.polylines(chart,[mi],False,(255,100,150),2)
            # draw_bollinger(chart,bbm,bbu,bbd,thickness=2)
            # for pl in [ups,downs,middle]:
            #     cv2.polylines(chart,[pl],False,(0,200,0))
            # cv2.polylines(chart,[middle],False,(155,100,250),2)
            # cv2.polylines(chart,[sma],False,(255,100,0),1)
            # for zone in bullish_FGV:
            #     cv2.rectangle(chart,zone[0],zone[1],(0,255,0),1)
            #     cv2.line(chart,zone[0],(zone[0][0]+200,zone[0][1]),(0,255,0))
            # for zone in bearish_FGV:
            #     cv2.rectangle(chart,zone[0],zone[1],(0,100,255),1)
            #     cv2.line(chart,zone[0],(zone[0][0]+200,zone[0][1]),(0,100,255))

        return Keys(
            cur_price=cur_price[1],

        )

    def get_action(self, keys:Keys):
        pass
