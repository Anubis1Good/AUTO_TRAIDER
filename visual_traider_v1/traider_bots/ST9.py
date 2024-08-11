import os
import cv2
import numpy as np
import numpy.typing as npt
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.indicators import get_bollinger_bands, get_dynamics, check_zona,get_bb_points,get_SMA,get_fractals
from utils.chart_utils.ProSveT import ProSveT
from utils.chart_utils.dtype import HalfBar
from dataclasses import dataclass
from time import time 

@dataclass
class Keys:       
    cur_price:int
    stop_long:int
    stop_short:int
    volatility:int
    take:int
    direction_long:bool
    direction_short:bool
    go:bool

class ST9(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'ST9'
        self.close_long = False
        self.close_short = False
        self.free_stop_l = True
        self.free_stop_s = True
        self.i = 0
        self.have_pos_l = False
        self.have_pos_s = False

    def _get_keys(self, img, region) -> dict:
        chart = self._get_chart(img,region)
        candle_mask = self._get_candle_mask(chart)
        volume_mask = self._get_volume_mask(chart)
        candle_cords = self._get_cords_on_mask(candle_mask)
        volume_cords = self._get_cords_on_mask(volume_mask)
        half_bars = self._get_half_bars(candle_mask,candle_cords,volume_cords)
        cur_price = self._get_current_price(chart)

        volatility = list(map(lambda x: x.spred_pt,half_bars))
        volatility = get_SMA(np.array(volatility),14)
        stop_long = (half_bars[-1].x,half_bars[-1].yl+volatility[-1][1])
        stop_short = (half_bars[-1].x,half_bars[-1].yh-volatility[-1][1])
        take = (half_bars[-1].x,half_bars[-2].ym)
        direction_long = half_bars[-1].yh > half_bars[-2].yh
        direction_short = half_bars[-1].yl < half_bars[-2].yl
        go = abs(cur_price[1] - half_bars[-2].ym) > volatility[-1][1]*1.6

        if not self.free_stop_l:
            stop_long = stop_long if stop_long[1] < self.stop_long else (half_bars[-1].x,self.stop_long)
        if not self.free_stop_s:
            stop_short = stop_short if stop_short[1] > self.stop_short else (half_bars[-1].x,self.stop_short)
      
        keys = Keys(
            cur_price[1],
            stop_long[1],
            stop_short[1],
            volatility[-1][1],
            take[1],
            direction_long,
            direction_short,
            go
            )
            
        if self.mode != 1:
            cv2.circle(chart,stop_long,1,(0,200,0),2)
            cv2.circle(chart,stop_short,1,(200,200,0),2)
            cv2.circle(chart,take,1,(250,200,200),2)
            cv2.polylines(chart,[volatility],False,(200,200,0),1)
            cv2.putText(chart,"FSL: " +str(self.free_stop_l),(0,25),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
            cv2.putText(chart,"FSS: " +str(self.free_stop_s),(0,50),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)

        return keys

    
    def _get_action(self,keys:Keys):
        self.stop_long = keys.stop_long
        self.stop_short = keys.stop_short
        if self.have_pos_l:
            if keys.cur_price < keys.take or keys.cur_price > keys.stop_long:
                return 'close_long'
        if self.have_pos_s:
            if keys.cur_price > keys.take or keys.cur_price < keys.stop_short:
                return 'close_short'
        if keys.go:
            if keys.direction_long:
                return 'long'
            if keys.direction_short:
                return 'short'


    
    def _test(self, img):
        m_keys = self._get_keys(img,self.minute_chart_region)
        # h_keys = self._get_keys(img,self.hour_chart_region)
        action = self._get_action(m_keys)
        res1_l,res2_l = 0,0
        res1_s,res2_s = 0,0
        if action == 'long':
            res1_s = self._test_send_close(img,'short')
            res2_l = self._test_send_open(img,'long') 
        if action == 'close_long':
            res1_l = self._test_send_close(img,'long')
        if action == 'short':
            res1_l = self._test_send_close(img,'long')
            res2_s = self._test_send_open(img,'short')
        if action == 'close_short':
            res1_s = self._test_send_close(img,'short')
        if res1_s == 1 and res2_l == 0:
            self.have_pos_s = False
            self.free_stop_s = True
        if res1_l == 1 and res2_s == 0:
            self.have_pos_l = False
            self.free_stop_l = True
        if res2_l == 1:
            self.have_pos_l = True
            self.have_pos_s = False
            self.free_stop_l = False
            self.free_stop_s = True
        if res2_s == 1:
            self.have_pos_s = True
            self.have_pos_l = False
            self.free_stop_s = False
            self.free_stop_l = True
        self.write_logs(m_keys,action)

    def _traide(self, img):
        # TODO free_stop
        pos = self._check_position(img)
        if pos == 0:
            self.have_pos_l = False
            self.have_pos_s = False
            self.free_stop_l = True
            self.free_stop_s = True
        if pos == 1:
            self.have_pos_l = True
            self.have_pos_s = False
            self.free_stop_l = False
            self.free_stop_s = True
        if pos == -1:
            self.have_pos_l = False
            self.have_pos_s = True
            self.free_stop_l = True
            self.free_stop_s = False
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
        log = f'{self.name} - {time()} - action: {action}- pos_s:{self.have_pos_s}- pos_s:{self.have_pos_l}- fsl: {self.free_stop_l}- fss: {self.free_stop_s}- state: {vars(keys)}\n'
        if not os.path.exists(file_name):
            with open(file_name, 'w') as f:
                f.write(log)
        else:
            with open(file_name, 'a') as f:
                f.write(log)
