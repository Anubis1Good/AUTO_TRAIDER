import os
import cv2
import numpy as np
import numpy.typing as npt
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.indicators import get_borders
from dataclasses import dataclass
from time import time 

@dataclass
class Keys:       
    cur_price:int
    top:int
    bottom:int



class Collector1(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'Collector1'
        self.close_long = False
        self.close_short = False
        self.i = 0
        self.take_short = False


    def _get_keys(self, img, region) -> Keys:
        chart = self._get_chart(img,region)
        cur_price = self._get_current_price(chart)
        top_line,bottom_line = get_borders(region,5)
      
        keys = Keys(
            cur_price[1],
            top_line[-1][1],
            bottom_line[-1][1]
            )
            
        if self.mode != 1:
            cv2.polylines(chart,[top_line],False,(255,0,200),2)
            cv2.polylines(chart,[bottom_line],False,(55,200,250),2)

        return keys

    
    def _get_action(self,keys:Keys):
        if keys.cur_price > keys.bottom:
            return 'long'
        if keys.cur_price < keys.top:
            if self.take_short:
                return 'short'
            return 'close_long'

    
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
