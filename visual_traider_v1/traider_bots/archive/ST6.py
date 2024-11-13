import cv2
import numpy as np
import numpy.typing as npt
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.Indicators.SpredChannel import SpredChannel
from utils.chart_utils.indicators import get_SMA, get_fractals
from utils.chart_utils.dtype import HalfBar
from dataclasses import dataclass

@dataclass
class Keys:
    cur_price:int
    stop_long:int
    stop_short:int
    enter_long:int
    enter_short:int
    mean_spred:float
    volatility:int
    last_hb:HalfBar

class ST6(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'ST6'
        self.close_long = False
        self.close_short = False

    def _get_keys(self, img, region) -> Keys:
        chart = self._get_chart(img,region)
        candle_mask = self._get_candle_mask(chart)
        volume_mask = self._get_volume_mask(chart)
        candle_cords = self._get_cords_on_mask(candle_mask)
        volume_cords = self._get_cords_on_mask(volume_mask)
        half_bars = self._get_half_bars(candle_mask,candle_cords,volume_cords)
        cur_price = self._get_current_price(chart)
        volatility = list(map(lambda x: x.spred_pt,half_bars))
        volatility = get_SMA(np.array(volatility),14)
        hpts = np.array(list(map(lambda x: x.hpt,half_bars)))
        lpts = np.array(list(map(lambda x: x.lpt,half_bars)))
        max_hb,min_hb = get_fractals(hpts,lpts)
        enter_short = (half_bars[-1].x,max_hb[-1][1]-volatility[-1][1]*2)
        enter_long = (half_bars[-1].x,min_hb[-1][1]+volatility[-1][1]*2)
        stop_long = (half_bars[-1].x,min_hb[-1][1]+volatility[-1][1])
        stop_short = (half_bars[-1].x,max_hb[-1][1]-volatility[-1][1])
        spreds = np.array(list(map(lambda x: x.spred,half_bars)))
        mean_spred = np.average(spreds)
        last_hb = half_bars[-2]
        keys = Keys(cur_price[1],stop_long[1],stop_short[1],enter_long[1],enter_short[1],mean_spred,volatility[-1][1],last_hb)
        # if self.mode != 1:
        #     cv2.circle(chart,stop_long,1,(0,200,0),2)
        #     cv2.circle(chart,stop_short,1,(200,200,0),2)
        #     cv2.circle(chart,enter_short,1,(200,0,200),2)
        #     cv2.circle(chart,enter_long,1,(0,100,100),2)
        #     cv2.polylines(chart,[max_hb],False,(200,200,0))
        #     cv2.polylines(chart,[min_hb],False,(200,200,200))
        #     cv2.putText(chart,"CP: " +str(cur_price[1]),(0,20),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
        #     cv2.putText(chart,"ES: " +str(enter_short[1]),(0,40),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
        #     cv2.putText(chart,"EL: " +str(enter_long[1]),(0,60),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
        return keys

    def _get_action(self,keys:Keys):
        cur_price = keys.cur_price
        stop_long = keys.stop_long
        stop_short = keys.stop_short
        # if keys.volatility > keys.mean_spred:
        if cur_price > keys.enter_long:
            # print(cur_price,keys.enter_long)
            return 'long'
        if cur_price < keys.enter_short:
            return 'short'
        # if cur_price < stop_long:
        #     return 'close_long'
        # if cur_price > stop_short:
        #     return 'close_short'
        if cur_price < keys.last_hb.ym:
            return 'close_long'
        if cur_price > keys.last_hb.ym:
            return 'close_short'


    def _test(self, img,price):
        m_keys = self._get_keys(img,self.minute_chart_region)
        action = self._get_action(m_keys)
        if action == 'long':
            self._test_send_close(img,'short',price=price)
            self._test_send_open(img,'long',price=price) 
        if action == 'close_long':
            self._test_send_close(img,'long',price=price)
        if action == 'short':
            self._test_send_close(img,'long',price=price)
            self._test_send_open(img,'short',price=price)
        if action == 'close_short':
            self._test_send_close(img,'short',price=price)
        if action == 'close_all':
            self._test_send_close(img,'short',price=price)
            self._test_send_close(img,'long',price=price)

    
    def _traide(self, img):
        pos = self._check_position(img)
        m_keys = self._get_keys(img,self.minute_chart_region)
        action = self._get_action(m_keys)
        if action:
            if action == 'long':
                if pos == -1:
                    self.close_short = True
                    self._reverse_pos(img,'long')
                if pos == 0:
                    self._send_open('long')
            if action == 'close_long':
                if pos == 1:
                    self.close_long = True
                    self._send_close(img,'long')
            if action == 'short':
                if pos == 1:
                    self.close_long = True
                    self._reverse_pos(img,'short')
                if pos == 0:
                    self._send_open('short')
            if action == 'close_short':
                if pos == -1:
                    self.close_short = True
                    self._send_close(img,'short')
            if action == 'close_all':
                if pos == 1:
                    self.close_long = True
                    self._send_close(img,'long')
                if pos == -1:
                    self.close_short = True
                    self._send_close(img,'short')
        elif self.close_long:
            if pos == 1:
                self._send_close(img,'long')
            else:
                self.close_long = False
        elif self.close_short:
            if pos == -1:
                self._send_close(img,'short')
            else:
                self.close_long = False
        else:
            self._reset_req()
