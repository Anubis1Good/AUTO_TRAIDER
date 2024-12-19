'''
Трейдер на основе поиска схожего паттерна на истории
'''

import cv2
from tas.BaseTA import BaseTA,Keys
from utils.chart_utils.indicators import get_projection
from utils.ML_utils.cls_utils import most_similar_relative_point_cs_mult
from utils.middlewares.reverse import simple_reverse
from dataclasses import dataclass

@dataclass
class KeysW(Keys):
    h_pred:int
    l_pred:int
    allowance:bool

class STA2_PPP(BaseTA):
    def __init__(self, trader,size_cluster=10,size_projection=10,divider=10,use_volume=False,*args):
        super().__init__(trader,*args)
        self.divider = divider
        self.size_cluster = size_cluster
        self.size_projection = size_projection
        self.use_volume = use_volume
    def get_keys(self, img)-> KeysW:
        region = self.trader.chart_region
        chart = self.trader._get_chart(img,region)
        candle_cords,volume_cords,candle_mask=self.trader._get_candle_volume_cords(chart)
        half_bars = self.trader._get_half_bars(candle_mask,candle_cords,volume_cords)
        cur_price = self.trader._get_current_price(chart)
        ms_i = most_similar_relative_point_cs_mult(half_bars,size_cluster=self.size_cluster,use_volume=self.use_volume)
        start = ms_i + 1 + self.size_cluster
        end = start + self.size_projection
        h_out,l_out = get_projection(half_bars[start:end],half_bars[ms_i+self.size_cluster],half_bars[-1])
        dist_lh = abs(l_out - h_out)
        buff = (dist_lh)//10
        heigth = region[3]-region[1]
        allowance = dist_lh > (heigth // self.divider)
        if self.trader.mode in (2,0):
            cv2.polylines(chart,[half_bars[ms_i].draw_line],False,(255,55,55),2)
            cv2.polylines(chart,[half_bars[ms_i+self.size_cluster].draw_line],False,(255,55,55),2)
            cv2.polylines(chart,[half_bars[-1].draw_line],False,(0,255,0),2)
            cv2.polylines(chart,[half_bars[-1-self.size_cluster].draw_line],False,(0,255,0),2)
            cv2.circle(chart,(half_bars[-1].x,h_out),1,(100,255,0),5)
            cv2.circle(chart,(half_bars[-1].x,l_out),1,(255,50,0),5)
            cv2.putText(chart,str(allowance),(30,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255))

        return KeysW(
            cur_price=cur_price[1],
            h_pred=h_out+buff,
            l_pred=l_out-buff,
            allowance=allowance
        )

    def get_action(self, keys:KeysW):
        if keys.allowance:
            if keys.cur_price < keys.h_pred:
                return 'short'
            if keys.cur_price > keys.l_pred:
                return 'long'

class STA2_R_PPP(STA2_PPP):
    def get_action(self, keys):
        return simple_reverse(super().get_action(keys))