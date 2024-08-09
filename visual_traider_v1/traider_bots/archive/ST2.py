import cv2
import os
import numpy as np
import numpy.typing as npt
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.indicators import get_bollinger_bands,  get_dynamics,check_zona
from utils.chart_utils.ProSveT import ProSveT
class ST2(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'ST2'
        self.i = 0
        self.close_long = False
        self.close_short = False

    def _get_keys(self, img, region) -> dict:
        chart = self._get_chart(img,region)
        candle_mask = self._get_candle_mask(chart)
        volume_mask = self._get_volume_mask(chart)
        candle_cords = self._get_cords_on_mask(candle_mask)
        volume_cords = self._get_cords_on_mask(volume_mask)
        half_bars = self._get_half_bars(candle_mask,candle_cords,volume_cords)
        pst = ProSveT(half_bars)
        pst.draw_all(chart)
        cur_price = self._get_current_price(chart)

        sma20,bbu,bbd = get_bollinger_bands(pst.mpts)
        dynamics = get_dynamics(sma20)
        sell_zona = check_zona(pst.sell_zona,half_bars)
        buy_zona = check_zona(pst.buy_zona,half_bars)
        keys = {
            'cur_price':cur_price,
            'sell_zona':sell_zona,
            'buy_zona':buy_zona,
            'sma20':sma20,
            'bbu':bbu,
            'bbd':bbd,
            'dynamics':dynamics,
            'last_hb':half_bars[-2]    
        }
        if self.mode != 1:
            cv2.polylines(chart,[sma20],False,(200,100,100),1)
            cv2.polylines(chart,[bbu],False,(200,200,100),1)
            cv2.polylines(chart,[bbd],False,(200,100,200),1)
            cv2.putText(chart,str(keys['dynamics']),(0,100),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
        return keys
    
    def _get_wave(self,keys):
        lock = self._check_lock(keys)
        if keys['buy_zona']:
            if keys['dynamics'] < -10:
                if keys['cur_price'][1] > keys['sma20'][-1][1]:
                    return 'long'
            if lock == 1:
                return 'close_long'

        if keys['sell_zona']:
            if keys['dynamics'] > 10:
                if keys['cur_price'][1] < keys['sma20'][-1][1]:
                    return 'short'
            if lock == -1:
                return 'close_short'

    def _check_lock(self,keys):
        if keys['cur_price'][1] > keys['bbd'][-1][1] < keys['last_hb'].yl:
            return -1
        if keys['cur_price'][1] < keys['bbu'][-1][1] > keys['last_hb'].yh:
            return 1
        return 0 
        

    def _test(self, img):
        h_keys = self._get_keys(img,self.hour_chart_region)
        m_keys = self._get_keys(img,self.minute_chart_region)
        wave = self._get_wave(m_keys)
        # self.i+=1
        # cv2.imwrite('./test_images/'+self.name+str(self.i)+'.png',img)
        if wave == 'long':
            self._test_send_close(img,'short')
            self._test_send_open(img,'long') 
        if wave == 'close_long':
            self._test_send_close(img,'long')
        if wave == 'short':
            self._test_send_close(img,'long')
            self._test_send_open(img,'short')
        if wave == 'close_short':
            self._test_send_close(img,'short')

    def _traide(self, img):
        pos = self._check_position(img)
        m_keys = self._get_keys(img,self.minute_chart_region)
        wave = self._get_wave(m_keys)
        if wave:
            if wave == 'long':
                if pos == -1:
                    self.close_short = True
                    self._reverse_pos(img,'long')
                if pos == 0:
                    self._send_open('long')
            if wave == 'close_long':
                self.close_long = True
                self._send_close(img,'long')
            if wave == 'short':
                if pos == 1:
                    self.close_long = True
                    self._reverse_pos(img,'short')
                if pos == 0:
                    self._send_open('short')
            if wave == 'close_short':
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

