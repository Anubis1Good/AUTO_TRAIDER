import cv2
import numpy as np
import numpy.typing as npt
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.Indicators.SpredChannel import SpredChannel
from utils.chart_utils.indicators import get_SMA,get_bollinger_bands
from utils.test_utils.test_draws_funcs import draw_bollinger
from utils.chart_utils.dtype import HalfBar
from dataclasses import dataclass

@dataclass
class Keys:
    cur_price:int
    stop_long:int
    stop_short:int
    bbu:int
    bbd:int
    last_hb:HalfBar

class ST7(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'ST7'
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
        stop_long = (half_bars[-1].x,half_bars[-2].ym+volatility[-1][1])
        stop_short = (half_bars[-1].x,half_bars[-2].ym-volatility[-1][1])
        sma_sm,bbu_sm,bbd_sm = get_bollinger_bands(np.array(list(map(lambda x: x.mpt,half_bars))))
        last_hb = half_bars[-1]

        keys = Keys(cur_price[1],stop_long[1],stop_short[1],bbu_sm[-1][1],bbd_sm[-1][1],last_hb)
        if self.mode != 1:
            cv2.circle(chart,stop_long,1,(0,200,0),2)
            cv2.circle(chart,stop_short,1,(200,200,0),2)
            draw_bollinger(chart,sma_sm,bbu_sm,bbd_sm)
        return keys

    def _get_action(self,keys:Keys):
        cur_price = keys.cur_price
        stop_long = keys.stop_long
        stop_short = keys.stop_short
        if cur_price > stop_long:
            return 'close_all'
        if cur_price < stop_short:
            return 'close_all'
        if keys.last_hb.yh < keys.bbu:
            return 'long'
        if keys.last_hb.yl > keys.bbd:
            return 'short'

    
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
