'''

'''

import cv2
from tas.BaseTA import BaseTA,Keys
from utils.chart_utils.indicators import get_borders
from dataclasses import dataclass

@dataclass
class KeysW(Keys):
    top:int
    bottom:int
    top_close:int
    bottom_close:int



class LTA1_C(BaseTA):
    def __init__(self, trader,divider=4,*args):
        super().__init__(trader,*args)
        self.divider = divider
    def get_keys(self, img)-> KeysW:
        region = self.trader.chart_region
        chart = self.trader._get_chart(img,region)
        top_line,bottom_line = get_borders(self.trader.chart_region,divider=self.divider)
        center_line,_ = get_borders(self.trader.chart_region,2)
        cur_price = self.trader._get_current_price(chart)

        if self.trader.mode != 1:
            cv2.line(chart,top_line[0],top_line[1],(200,33,150),2)
            cv2.line(chart,bottom_line[0],bottom_line[1],(100,233,250),2)
            cv2.line(chart,center_line[0],center_line[1],(200,233,50),2)

        return KeysW(
            cur_price=cur_price[1],
            top=top_line[0][1],
            bottom=bottom_line[0][1],
            top_close=center_line[0][1]
        )

    def get_action(self, keys:KeysW):
        if keys.cur_price < keys.top:
            return 'short'
        if keys.cur_price > keys.bottom:
            return 'long'
        if keys.cur_price < keys.top_close:
            return 'close_long'
        if keys.cur_price > keys.top_close:
            return 'close_short'


class LTA1_C2(BaseTA):
    def __init__(self, trader,divider1=5,divider2=2.5,*args):
        super().__init__(trader,*args)
        self.divider1 = divider1
        self.divider2 = divider2
    def get_keys(self, img)-> KeysW:
        region = self.trader.chart_region
        chart = self.trader._get_chart(img,region)
        top_line,bottom_line = get_borders(self.trader.chart_region,self.divider1)
        top_line2,bottom_line2 = get_borders(self.trader.chart_region,self.divider2)
        cur_price = self.trader._get_current_price(chart)

        if self.trader.mode != 1:
            cv2.line(chart,top_line[0],top_line[1],(200,33,150),2)
            cv2.line(chart,bottom_line[0],bottom_line[1],(100,233,250),2)
            cv2.line(chart,top_line2[0],top_line2[1],(200,233,50),2)
            cv2.line(chart,bottom_line2[0],bottom_line2[1],(200,33,150),2)

        return KeysW(
            cur_price=cur_price[1],
            top=top_line[0][1],
            bottom=bottom_line[0][1],
            top_close=top_line2[0][1],
            bottom_close=bottom_line2[0][1]
        )

    def get_action(self, keys:KeysW):
        if keys.cur_price < keys.top:
            return 'short'
        if keys.cur_price > keys.bottom:
            return 'long'
        if keys.cur_price < keys.top_close:
            return 'close_long'
        if keys.cur_price > keys.bottom_close:
            return 'close_short'