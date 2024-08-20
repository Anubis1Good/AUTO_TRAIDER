import os
import cv2
import numpy as np
import numpy.typing as npt
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.indicators import get_bollinger_bands, get_dynamics,get_SMA
from utils.test_utils.test_draws_funcs import draw_bollinger
from dataclasses import dataclass
from time import time 

@dataclass
class Keys:       
    cur_price:int
    ma:int
    bbu:int
    bbd:int
    dynamics:float
    stop_long:int
    stop_short:int


class ST10(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'ST10'
        self.close_long = False
        self.close_short = False
        self.i = 0
        self.stop_long = 1000
        self.stop_short = -1
        self.free_stop_l = True
        self.free_stop_s = True
        self.have_pos = False

    def _get_keys(self, img, region) -> dict:
        chart = self._get_chart(img,region)
        candle_mask = self._get_candle_mask(chart)
        volume_mask = self._get_volume_mask(chart)
        candle_cords = self._get_cords_on_mask(candle_mask)
        volume_cords = self._get_cords_on_mask(volume_mask)
        half_bars = self._get_half_bars(candle_mask,candle_cords,volume_cords)
        cur_price = self._get_current_price(chart)
        mpts = np.array(list(map(lambda x: x.mpt,half_bars)))
        ma,ups,downs=get_bollinger_bands(mpts,2,5)
        dynamics_sm = round(get_dynamics(ma,5)/5,2)

        
        volatility = list(map(lambda x: x.spred_pt,half_bars))
        volatility = get_SMA(np.array(volatility),14)
        stop_long = (half_bars[-1].x,half_bars[-2].yl+volatility[-1][1])
        stop_short = (half_bars[-1].x,half_bars[-2].yh-volatility[-1][1])


        if not self.free_stop_l:
            stop_long = stop_long if stop_long[1] < self.stop_long else (half_bars[-1].x,self.stop_long)
        if not self.free_stop_s:
            stop_short = stop_short if stop_short[1] > self.stop_short else (half_bars[-1].x,self.stop_short)

      
        keys = Keys(
            cur_price[1],
            ma[-1][1],
            ups[-1][1],
            downs[-1][1],
            dynamics_sm,
            stop_long[1],
            stop_short[1],
            )
            
        if self.mode != 1:
            cv2.circle(chart,stop_long,1,(0,200,0),2)
            cv2.circle(chart,stop_short,1,(200,200,0),2)
            draw_bollinger(chart,ma,ups,downs,(255,155,155))
            cv2.putText(chart,"DSM: " +str(dynamics_sm),(0,75),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
            cv2.putText(chart,"FSL: " +str(self.free_stop_l),(0,25),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
            cv2.putText(chart,"FSS: " +str(self.free_stop_s),(0,50),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)

        return keys

    
    def _get_action(self,keys:Keys):
        self.stop_long = keys.stop_long
        self.stop_short = keys.stop_short
        if keys.dynamics < -0.7:
            if self.have_pos:
                self.free_stop_l = False
            if keys.cur_price > keys.stop_long:
                return 'close_long'
            if keys.cur_price > keys.ma:
                return 'long'
            if keys.cur_price < keys.stop_short:
                return 'close_short'
            if keys.cur_price < keys.bbu:
                return 'close_long'
        elif keys.dynamics > 0.7:
            if self.have_pos:
                self.free_stop_s = False
            if keys.cur_price < keys.stop_short:
                return 'close_short'
            if keys.cur_price < keys.ma:
                return 'short'
            if keys.cur_price > keys.stop_long:
                return 'close_long'
            if keys.cur_price > keys.bbd:
                return 'close_short'
        else:
            if self.have_pos:
                self.free_stop_s = False
                self.free_stop_l = False
            if keys.cur_price > keys.bbd:
                return 'long'
            if keys.cur_price < keys.bbu:
                return 'short'

    
    def _test(self, img):
        m_keys = self._get_keys(img,self.minute_chart_region)
        action = self._get_action(m_keys)
        res1,res2 = 0,0
        if action == 'long':
            res1 = self._test_send_close(img,'short')
            res2 = self._test_send_open(img,'long') 
        if action == 'close_long':
            res1 = self._test_send_close(img,'long')
        if action == 'short':
            res1 = self._test_send_close(img,'long')
            res2 = self._test_send_open(img,'short')
        if action == 'close_short':
            res1 = self._test_send_close(img,'short')
        if res1 == 1 and res2 == 0:
            self.have_pos = False
            self.free_stop_s = True
            self.free_stop_l = True
        if res2 == 1:
            self.have_pos = True
        self.write_logs(m_keys,action)

    def _traide(self, img):
        # TODO free_stop
        pos = self._check_position(img)
        if pos != 0:
            self.have_pos = True
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


    
    def draw_research(self,img):
        try:
            m_keys = self._get_keys(img,self.minute_chart_region)
            save_dir= './test_images/'
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            self.i += 1
            img_name = save_dir + self.name + str(self.i) +'.png'
            cv2.imwrite(img_name,img)
        except:
            pass

    def write_logs(self,keys,action):
        file_name = f'./logs/{self.traider_name}{self.name}.txt'
        log = f'{self.name} - {time()} - action: {action} state: {vars(keys)}\n'
        if not os.path.exists(file_name):
            with open(file_name, 'w') as f:
                f.write(log)
        else:
            with open(file_name, 'a') as f:
                f.write(log)
