import os
import cv2
import numpy as np
import numpy.typing as npt
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.indicators import get_linear_reg_clear
from dataclasses import dataclass
from time import time 

@dataclass
class Keys:       
    cur_price:int
    h_pred:int
    l_pred:int
    h_pred_f:int
    l_pred_f:int



class ST12(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'ST12'
        self.close_long = False
        self.close_short = False
        self.i = 0


    def _get_keys(self, img, region) -> dict:
        chart = self._get_chart(img,region)
        candle_mask = self._get_candle_mask(chart)
        volume_mask = self._get_volume_mask(chart)
        candle_cords = self._get_cords_on_mask(candle_mask)
        volume_cords = self._get_cords_on_mask(volume_mask)
        half_bars = self._get_half_bars(candle_mask,candle_cords,volume_cords)
        cur_price = self._get_current_price(chart)
        hpts = np.array(list(map(lambda x: x.hpt,half_bars)))
        lpts = np.array(list(map(lambda x: x.lpt,half_bars)))
        x,y = self._get_xy(hpts[-14:])
        h_pred = get_linear_reg_clear(x,y)
        x,y = self._get_xy(lpts[-14:])
        l_pred = get_linear_reg_clear(x,y)
        x,y = self._get_xy(hpts)
        h_pred_f = get_linear_reg_clear(x,y)
        x,y = self._get_xy(lpts)
        l_pred_f = get_linear_reg_clear(x,y)
      
        keys = Keys(
            cur_price[1],
            h_pred[1],
            l_pred[1],
            h_pred_f[1],
            l_pred_f[1]
            )
            
        if self.mode != 1:
            cv2.circle(chart,h_pred,1,(200,200,200),2)
            cv2.circle(chart,l_pred,1,(100,250,200),2)
            cv2.circle(chart,h_pred_f,1,(200,200,200),1)
            cv2.circle(chart,l_pred_f,1,(100,250,200),1)

        return keys

    
    def _get_action(self,keys:Keys):
        if keys.cur_price < keys.h_pred_f:
            if keys.cur_price > keys.l_pred:
                return 'close_long'
            if keys.cur_price < keys.h_pred:
                return 'long'
        if keys.cur_price > keys.l_pred_f:
            if keys.cur_price > keys.l_pred:
                return 'short'
            if keys.cur_price < keys.h_pred:
                return 'close_short'

    
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
