import cv2
import os
import numpy as np
import numpy.typing as npt
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.indicators import get_bollinger_bands, get_zona, get_SMA, get_dynamics
class ST1(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'ST1'
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
        mpts = []
        vpts = []
        for i in range(len(half_bars)):
            mpt = half_bars[i].mpt
            vpt = half_bars[i].vpt
            mpts.append(mpt)
            vpts.append(vpt)
        vpts = np.array(vpts)
        v_sma = get_SMA(vpts,20)
        cur_price = self._get_current_price(chart)
        zona,m_pt_zona = get_zona(half_bars,cur_price,vpts,v_sma)
        sma20,bbu,bbd = get_bollinger_bands(np.array(mpts))
        dynamics = get_dynamics(sma20)
        keys = {
            'cur_price':cur_price,
            'zona':zona,
            'm_pt_zona':m_pt_zona,
            'sma20':sma20,
            'bbu':bbu,
            'bbd':bbd,
            'dynamics':dynamics,
            'last_hb':half_bars[-2]    
        }
        return keys
    
    def _draw(self,img,keys:dict,region):
        keys_copy = keys.copy()
        colors = (
            (255,255,255),
            (145,145,245),
            (235,135,135),
            (230,100,0),
            (230,200,50),
            (230,100,200),
            (130,100,0),
            (130,200,50),
            (130,100,200),
            (30,200,10),
            (230,10,200),
        )
        i = 0
        for key in keys_copy:
            if 'numpy.ndarray' in str(type(keys_copy[key])):
                keys_copy[key] = np.array(list(map(lambda x:self._change_coords(x,region), keys_copy[key])))
                cv2.polylines(img,[keys_copy[key]],False,colors[i],2)
                i += 1

        cv2.putText(img,str(keys['dynamics']),(region[0],region[1]+100),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
        return img

    def _all_draw(self,img,m_keys,h_keys):
        img = self._draw(img,m_keys,self.minute_chart_region)
        img = self._draw(img,h_keys,self.hour_chart_region)
        return img
    
 

    
    def _get_wave(self,keys):
        lock = self._check_lock(keys)
        if keys['zona']:
            if keys['dynamics'] < -10:
                if keys['cur_price'][1] > keys['sma20'][-1][1]:
                    return 'long'
                if lock == 1:
                    return 'close_long'
            if keys['dynamics'] > 10:
                if keys['cur_price'][1] < keys['sma20'][-1][1]:
                    return 'short'
                if lock == -1:
                    return 'close_short'
            if lock == 1:
                return 'close_long'
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
        draw_func = lambda img:self._all_draw(img,m_keys,h_keys)
        wave = self._get_wave(m_keys)
        if wave == 'long':
            self._test_send_close(img,'short',draw_func)
            self._test_send_open(img,'long',draw_func) 
        if wave == 'close_long':
            self._test_send_close(img,'long',draw_func)
        if wave == 'short':
            self._test_send_close(img,'long',draw_func)
            self._test_send_open(img,'short',draw_func)
        if wave == 'close_short':
            self._test_send_close(img,'short',draw_func)

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


class ST1a(ST1):
    def _get_wave(self,keys):
        lock = self._check_lock(keys)
        if keys['zona']:
            if keys['dynamics'] < -10:
                if keys['cur_price'][1] > keys['sma20'][-1][1]:
                    return 'long'
                if lock == 1:
                    return 'close_long'
            if keys['dynamics'] > 10:
                if keys['cur_price'][1] < keys['sma20'][-1][1]:
                    return 'short'
                if lock == -1:
                    return 'close_short'
        if keys['cur_price'][1] > keys['sma20'][-1][1] and keys['dynamics'] < -5:
            return 'close_short'
        if keys['cur_price'][1] < keys['sma20'][-1][1] and keys['dynamics'] > 5:
            return 'close_long'
