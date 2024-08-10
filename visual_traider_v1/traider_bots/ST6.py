import cv2
import numpy as np
import numpy.typing as npt
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.Indicators.SpredChannel import SpredChannel
from utils.chart_utils.indicators import get_SMA
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
        enter_short = (half_bars[-2].x,half_bars[-2].ym+volatility[-1][1])
        enter_long = (half_bars[-2].x,half_bars[-2].ym-volatility[-1][1])
        stop_long = (half_bars[-2].x,half_bars[-2].ym+volatility[-1][1]*2)
        stop_short = (half_bars[-2].x,half_bars[-2].ym-volatility[-1][1]*2)
        spreds = np.array(list(map(lambda x: x.spred,half_bars)))
        mean_spred = np.average(spreds)
        keys = Keys(cur_price[1],stop_long[1],stop_short[1],enter_short[1],enter_long[1],mean_spred,volatility[-1][1])
        if self.mode != 1:
            cv2.circle(chart,stop_long,1,(0,200,0),2)
            cv2.circle(chart,stop_short,1,(200,200,0),2)
            cv2.circle(chart,enter_short,1,(200,0,200),1)
            cv2.circle(chart,enter_long,1,(0,100,100),1)
        return keys

    def _get_action(self,keys:Keys):
        cur_price = keys.cur_price
        stop_long = keys.stop_long
        stop_short = keys.stop_short
        # if keys.volatility > keys.mean_spred:
        if cur_price > stop_long:
            return 'close_long'
        if cur_price < stop_short:
            return 'close_short'
        if cur_price > keys.enter_long:
            return 'long'
        if cur_price < keys.enter_short:
            return 'short'
    
    def _test(self, img):
        m_keys = self._get_keys(img,self.minute_chart_region)
        action = self._get_action(m_keys)
        if action == 'long':
            self._test_send_close(img,'short')
            self._test_send_open(img,'long') 
        if action == 'close_long':
            self._test_send_close(img,'long')
        if action == 'short':
            self._test_send_close(img,'long')
            self._test_send_open(img,'short')
        if action == 'close_short':
            self._test_send_close(img,'short')
        if action == 'close_all':
            self._test_send_close(img,'short')
            self._test_send_close(img,'long')

    
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
