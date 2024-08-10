import cv2
import numpy as np
import numpy.typing as npt
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.Indicators.SpredChannel import SpredChannel
from utils.chart_utils.dtype import HalfBar
from dataclasses import dataclass

@dataclass
class Keys:
    cur_price:tuple
    spcl:SpredChannel
    last_hb:HalfBar

class ST5(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'ST2'
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
        last_hb = half_bars[-1]
        spcl = SpredChannel(half_bars)

        keys = Keys(cur_price,spcl,last_hb)

        if self.mode != 1:
            spcl.draw_all(chart)

        return keys

    def _get_action(self,keys:Keys):
        cur_price = keys.cur_price[1]
        dynamics10 = keys.spcl.dynamics10
        dynamics50 = keys.spcl.dynamics50
        ma = keys.spcl.ma[-1][1]
        downs1 = keys.spcl.downs1[-1][1]
        ups1 = keys.spcl.ups1[-1][1]
        downs2 = keys.spcl.downs2[-1][1]
        ups2 = keys.spcl.ups2[-1][1]
        # if cur_price > downs2:
        #     return 'long'
        # if cur_price < ups2:
        #     return 'short'
        # if cur_price < downs1:
        #     return 'close_long'
        # if cur_price > ups1:
        #     return 'close_short'
        if dynamics10 > 0 and dynamics50 > 5:
            if cur_price < downs1:
                return 'short'
            if cur_price > downs2:
                return 'close_all'
            return 'close_long'
        elif dynamics10 < 0 and dynamics50 < -5:
            if cur_price > ups1:
                return 'long'
            if cur_price < ups2:
                return 'close_all'
            return 'close_short'
        else:
            if cur_price > downs1:
                return 'long'
            if cur_price < ups1:
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
