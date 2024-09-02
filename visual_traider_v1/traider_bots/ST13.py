import os
import cv2
import numpy as np
import numpy.typing as npt
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.indicators import get_linear_reg_clear,get_williams_fractals, get_SMA
from dataclasses import dataclass
from time import time 

@dataclass
class Keys:       
    cur_price:int
    h_pred:int
    l_pred:int
    slope:float
    creek:int
    ice:int




class ST13(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'ST13'
        self.close_long = False
        self.close_short = False
        self.i = 0
        self.pred_coef = 14


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
        mpts = np.array(list(map(lambda x: x.mpt,half_bars)))
        x,y = self._get_xy(hpts[-self.pred_coef:])
        h_pred = get_linear_reg_clear(x,y)
        x,y = self._get_xy(lpts[-self.pred_coef:])
        l_pred = get_linear_reg_clear(x,y)
        len_mpts = len(mpts)
        x,y = self._get_xy(mpts[len_mpts - len_mpts//4:])
        slope,intercept = self._get_linear_regress(x,y)

        volatility = list(map(lambda x: x.spred_pt,half_bars))
        volatility = get_SMA(np.array(volatility),14)

        ups,downs = get_williams_fractals(hpts,lpts,8,True)
        creek = 0
        ice = chart.shape[0]
        if len(ups) > 1:
            for i in range(len(ups)-1,0,-1):
                if ups[i][1] < cur_price[1]:
                    creek = ups[i][1]
                    break
        if len(downs) > 1:
            for i in range(len(downs)-1,0,-1):
                if downs[i][1] > cur_price[1]:
                    ice = downs[i][1]
                    break
        
        creek += volatility[-1][1]
        ice -= volatility[-1][1]

        keys = Keys(
            cur_price[1],
            h_pred[1],
            l_pred[1],
            slope,
            creek,
            ice
            )
            
        if self.mode != 1:
            cv2.circle(chart,h_pred,1,(200,200,200),2)
            cv2.circle(chart,l_pred,1,(100,250,200),2)
            cv2.polylines(chart,[ups],False,(255,0,200),2)
            cv2.polylines(chart,[downs],False,(55,200,250),2)

            cv2.putText(chart,"Slope: " +str(slope),(0,25),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)

        return keys

    
    def _get_action(self,keys:Keys):
        # long
        if keys.slope < -0.1:
            if keys.cur_price > keys.l_pred:
                return 'close_long'
            if keys.cur_price > keys.ice:
                return 'long'
            if keys.cur_price < keys.h_pred:
                return 'close_short'
        # short
        elif keys.slope > 0.1:
            if keys.cur_price < keys.h_pred:
                return 'close_short'
            if keys.cur_price < keys.creek:
                return 'short'
            if keys.cur_price > keys.l_pred:
                return 'close_long'
        # range
        else:
            if keys.cur_price > keys.ice:
                return 'long'
            if keys.cur_price < keys.creek:
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
