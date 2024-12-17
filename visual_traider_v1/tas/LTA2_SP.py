'''
Трейдер на основе статистических точек
'''

import cv2
import numpy as np
import numpy.typing as npt
from tas.BaseTA import BaseTA,Keys
from dataclasses import dataclass

@dataclass
class KeysW(Keys):
    top:int
    bottom:int
    median:int




class LTA2_SP(BaseTA):
    def __init__(self, trader,quantile=0.25,*args):
        super().__init__(trader,*args)
        self.quantile = quantile
    def get_keys(self, img)-> KeysW:
        region = self.trader.chart_region
        chart = self.trader._get_chart(img,region)
        candle_mask = self.trader._get_candle_mask(chart)
        candle_cords = self.trader._get_cords_on_mask(candle_mask)
        ys:npt.NDArray = candle_cords[:,0]
        median = int(np.median(ys))
        top = int(np.quantile(ys,0+self.quantile))
        bottom = int(np.quantile(ys,1-self.quantile))
        cur_price = self.trader._get_current_price(chart)

        if self.trader.mode in (2,0):
            cv2.circle(chart,(candle_cords[-1][0],top),1,(100,255,0),2)
            cv2.circle(chart,(candle_cords[-1][0],bottom),1,(100,55,250),2)
            cv2.circle(chart,(candle_cords[-1][0],median),1,(200,155,100),2)
            0

        return KeysW(
            cur_price=cur_price[1],
            top=top,
            bottom=bottom,
            median=median
        )

    def get_action(self, keys:KeysW):
        if keys.cur_price < keys.top:
            return 'short'
        if keys.cur_price > keys.bottom:
            return 'long'
        if keys.cur_price < keys.median:
            return 'close_long'
        if keys.cur_price > keys.median:
            return 'close_short'


