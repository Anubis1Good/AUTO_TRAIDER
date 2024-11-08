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
    cur_price:tuple
    spcl:SpredChannel
    last_hb:HalfBar
    stop_long:int
    stop_short:int

class ST5(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'ST5'
        self.close_long = False
        self.close_short = False
        self.stop_long = 1000
        self.stop_short = -1
        self.free_stop = True   

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

        volatility = list(map(lambda x: x.spred_pt,half_bars))
        volatility = get_SMA(np.array(volatility),14)
        if self.traider_name == 'ST5':
            stop_long = (half_bars[-2].x,half_bars[-2].ym+volatility[-1][1])
            stop_short = (half_bars[-2].x,half_bars[-2].ym-volatility[-1][1])
        if self.traider_name == 'ST5a':
            stop_long = (half_bars[-1].x,half_bars[-1].yl+volatility[-1][1])
            stop_short = (half_bars[-1].x,half_bars[-1].yh-volatility[-1][1])

        if not self.free_stop:
            stop_long = stop_long if stop_long[1] < self.stop_long else (half_bars[-1].x,self.stop_long)
            stop_short = stop_short if stop_short[1] > self.stop_short else (half_bars[-1].x,self.stop_short)
        self.stop_long = stop_long[1]
        self.stop_short = stop_short[1]

        keys = Keys(cur_price,spcl,last_hb,stop_long[1],stop_short[1])
        if self.mode != 1:
            spcl.draw_all(chart)
            cv2.circle(chart,stop_long,1,(0,200,0),2)
            cv2.circle(chart,stop_short,1,(200,200,0),2)
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
        downs3 = keys.spcl.downs3[-1][1]
        ups3 = keys.spcl.ups3[-1][1]
        # if cur_price > downs2:
        #     return 'long'
        # if cur_price < ups2:
        #     return 'short'
        # if cur_price < downs1:
        #     return 'close_long'
        # if cur_price > ups1:
        #     return 'close_short'
        if dynamics10 > 20:
            if cur_price < keys.stop_short:
                return 'close_short'
            if cur_price < downs2:
                return 'short'
            if cur_price > downs3:
                return 'close_short'
            # return 'close_long'
        elif dynamics10 >= 10:
            if cur_price < keys.stop_short:
                return 'close_short'
            if cur_price < ma:
                return 'short'
            if cur_price > downs1:
                return 'close_short'
            # return 'close_long'
        elif 10 > dynamics10 > -10:
            if cur_price < keys.stop_short:
                return 'close_short'
            if cur_price > keys.stop_long:
                return 'close_long'
            if cur_price > downs3:
                return 'long'
            if cur_price < ups3:
                return 'short'
        elif dynamics10 < -20:
            if cur_price > keys.stop_long:
                return 'close_long'
            if cur_price > ups2:
                return 'long'
            if cur_price < ups3:
                return 'close_long'
        else:
            if cur_price > keys.stop_long:
                return 'close_long'
            if cur_price > ma:
                return 'long'
            if cur_price < ups1:
                return 'close_long'
    
    def _test(self, img,price):
        m_keys = self._get_keys(img,self.minute_chart_region)
        action = self._get_action(m_keys)
        res1,res2 = 0,0
        if action == 'long':
            res1 = self._test_send_close(img,'short',price=price)
            res2 = self._test_send_open(img,'long',price=price) 
        if action == 'close_long':
            res1 = self._test_send_close(img,'long',price=price)
        if action == 'short':
            res1 = self._test_send_close(img,'long',price=price)
            res2 = self._test_send_open(img,'short',price=price)
        if action == 'close_short':
            res1 = self._test_send_close(img,'short',price=price)


    
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


class ST5a(ST5):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'ST5a'

    def _test(self, img,price):
        m_keys = self._get_keys(img,self.minute_chart_region)
        action = self._get_action(m_keys)
        res1,res2 = 0,0
        if action == 'long':
            res1 = self._test_send_close(img,'short',price=price)
            res2 = self._test_send_open(img,'long',price=price) 
        if action == 'close_long':
            res1 = self._test_send_close(img,'long',price=price)
        if action == 'short':
            res1 = self._test_send_close(img,'long',price=price)
            res2 = self._test_send_open(img,'short',price=price)
        if action == 'close_short':
            res1 = self._test_send_close(img,'short',price=price)
        if res1 == 1 and res2 == 0:
            self.free_stop = True
        if res2 == 1:
            self.free_stop = False

    def _traide(self, img):
        pos = self._check_position(img)
        m_keys = self._get_keys(img,self.minute_chart_region)
        action = self._get_action(m_keys)
        if pos == 0:
            self.free_stop = True
        else:
            self.free_stop = False
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