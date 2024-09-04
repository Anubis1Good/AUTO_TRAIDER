import os
import cv2
import numpy as np
import numpy.typing as npt
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.indicators import get_bollinger_bands, get_SMA
from utils.chart_utils.dtype import HalfBar
from dataclasses import dataclass
from time import time 

@dataclass
class Keys:       
    cur_price:int
    sma_sm:int
    bbd_sm:int
    bbu_sm:int
    bbu_attached:bool
    bbd_attached:bool
    over_bbd:bool
    over_bbu:bool
    stop_long:int
    stop_short:int
    direction:int
    take_long:int
    take_short:int

class PT4(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'PT4'
        self.bbu_attached = False
        self.bbd_attached = False
        self.close_long = False
        self.close_short = False
        self.stop_long = 1000
        self.stop_short = -1
        self.take_short = 1000
        self.take_long = -1
        self.free_stop = True
        self.i = 0

    def _get_keys(self, img, region) -> Keys:
        chart = self._get_chart(img,region)
        candle_mask = self._get_candle_mask(chart)
        volume_mask = self._get_volume_mask(chart)
        candle_cords = self._get_cords_on_mask(candle_mask)
        volume_cords = self._get_cords_on_mask(volume_mask)
        half_bars = self._get_half_bars(candle_mask,candle_cords,volume_cords)
        cur_price = self._get_current_price(chart)
        mpts = np.array(list(map(lambda x: x.mpt,half_bars)))
        sma_sm,bbu_sm,bbd_sm = get_bollinger_bands(np.array(mpts))

        sma_low = get_SMA(mpts,50)
        sma_fast = get_SMA(mpts,30)

        direction = 1 if sma_low[-1][1] > sma_fast[-1][1] else -1
        bbu_attached = half_bars[-2].y_in_bar(bbu_sm[-1][1]) or half_bars[-1].y_in_bar(bbu_sm[-1][1])
        bbd_attached = half_bars[-2].y_in_bar(bbd_sm[-1][1]) or half_bars[-1].y_in_bar(bbd_sm[-1][1]) 
        over_bbu = half_bars[-1].yl < bbu_sm[-1][1]
        over_bbd = half_bars[-1].yh > bbd_sm[-1][1]


        volatility = list(map(lambda x: x.spred_pt,half_bars))
        volatility = get_SMA(np.array(volatility),14)

        stop_long = (half_bars[-1].x,half_bars[-1].yl+volatility[-1][1]*2)
        stop_short = (half_bars[-1].x,half_bars[-1].yh-volatility[-1][1]*2)

        take_long = (half_bars[-1].x,half_bars[-1].yh-volatility[-1][1]*3)
        take_short = (half_bars[-1].x,half_bars[-1].yl+volatility[-1][1]*3)

        if not self.free_stop:
            stop_long = stop_long if stop_long[1] < self.stop_long else (half_bars[-1].x,self.stop_long)
            stop_short = stop_short if stop_short[1] > self.stop_short else (half_bars[-1].x,self.stop_short)
            take_long = (half_bars[-1].x,self.take_long)
            take_short = (half_bars[-1].x,self.take_short)
      
        keys = Keys(
            cur_price[1],
            sma_sm[-1][1],
            bbd_sm[-1][1],
            bbu_sm[-1][1],
            bbu_attached,
            bbd_attached,
            over_bbd,
            over_bbu,
            stop_long[1],
            stop_short[1],
            direction,
            take_long[1],
            take_short[1]
            )
            
        if self.mode != 1:
            cv2.circle(chart,stop_long,1,(0,200,0),2)
            cv2.circle(chart,stop_short,1,(200,200,0),2)
            cv2.circle(chart,take_long,1,(0,250,100),1)
            cv2.circle(chart,take_short,1,(250,100,0),1)
            cv2.polylines(chart,[volatility],False,(200,200,0),1)
            cv2.polylines(chart,[sma_sm],False,(200,0,0),1)
            cv2.polylines(chart,[bbu_sm],False,(200,200,0),1)
            cv2.polylines(chart,[bbd_sm],False,(200,0,200),1)
            cv2.polylines(chart,[sma_low],False,(100,0,0),2)
            cv2.polylines(chart,[sma_fast],False,(160,217,100),2)

            cv2.putText(chart,"bbuAt: "+str(bbu_attached),(0,110),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,205,155),2)
            cv2.putText(chart,"bbdAt: "+str(bbd_attached),(0,130),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,205,155),2)
            cv2.putText(chart,"SUA: "+str(self.bbu_attached),(0,165),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,205,155),2)
            cv2.putText(chart,"SDA: "+str(self.bbd_attached),(0,180),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,205,155),2)

            # cv2.putText(chart,"Wave: "+str(wave),(0,110),cv2.FONT_HERSHEY_SIMPLEX,0.8,(155,205,155),2)
        return keys

    
    def _get_action(self,keys:Keys):
        self.stop_long = keys.stop_long
        self.stop_short = keys.stop_short
        self.take_long = keys.take_long
        self.take_short = keys.take_short
        if keys.direction == -1:
            if keys.cur_price < keys.stop_short:
                return 'close_short'
            if keys.cur_price > keys.take_short and not keys.bbd_attached:
                return 'close_short'
            if not keys.bbd_attached and self.bbd_attached:
                return 'close_short'
            if keys.over_bbd:
                return 'close_short'
            if keys.cur_price < keys.bbu_sm:
                self.free_stop = False
                return 'short'
            if keys.cur_price > keys.stop_long:
                return 'close_long'
        # long_context
        if keys.direction == 1:
            if keys.cur_price > keys.stop_long:
                return 'close_long'
            if keys.cur_price < keys.take_long and not keys.bbu_attached:
                return 'close_long'
            if not keys.bbu_attached and self.bbu_attached:
                return 'close_long'
            if keys.over_bbu:
                return 'close_long'
            if keys.cur_price > keys.bbd_sm:
                self.free_stop = False
                return 'long'
            if keys.cur_price < keys.stop_short:
                return 'close_short'

    
    def _test(self, img):
        m_keys = self._get_keys(img,self.minute_chart_region)
        # h_keys = self._get_keys(img,self.hour_chart_region)
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
            self.free_stop = True
        self.bbd_attached = m_keys.bbd_attached
        self.bbu_attached = m_keys.bbu_attached
        self.write_logs(m_keys,action)

    def _traide(self, img):
        # TODO free_stop
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
        self.bbd_attached = m_keys.bbd_attached
        self.bbu_attached = m_keys.bbu_attached

    
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
        log = f'{self.name} - {time()} - {action}: state: {vars(keys)}\n'
        if not os.path.exists(file_name):
            with open(file_name, 'w') as f:
                f.write(log)
        else:
            with open(file_name, 'a') as f:
                f.write(log)
