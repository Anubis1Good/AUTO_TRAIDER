import os
import numpy as np
import cv2
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.ProSveT import ProSveT
from utils.chart_utils.indicators import check_zona,get_SMA,get_bollinger_bands
from dataclasses import dataclass
from time import time 

@dataclass
class Keys:       
    cur_price:int
    bbd_sm:int
    bbu_sm:int
    bbu_attached:bool
    bbd_attached:bool
    is_big_vsai:bool
    over_bbd:bool
    over_bbu:bool
    sell_zona:bool
    buy_zona:bool
    # creek:int
    # ice:int
    stop_long:int
    stop_short:int
    slope:int
    slope_sm:int

class PST1(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0,**kw) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode,**kw)
        self.traider_name = 'PST1'
        self.bbu_attached = False
        self.bbd_attached = False
        self.close_long = False
        self.close_short = False
        self.stop_long = 1000
        self.stop_short = -1
        self.free_stop = True
        self.i = 0
    
    def _get_keys(self, img, region) -> Keys:
        chart = self._get_chart(img,region)
        candle_mask = self._get_candle_mask(chart)
        volume_mask = self._get_volume_mask(chart)
        candle_cords = self._get_cords_on_mask(candle_mask)
        volume_cords = self._get_cords_on_mask(volume_mask)
        half_bars = self._get_half_bars(candle_mask,candle_cords,volume_cords)
        pst = ProSveT(half_bars)
        cur_price = self._get_current_price(chart)
        sell_zona = check_zona(pst.sell_zona,half_bars,cur_price[1],'short')
        buy_zona = check_zona(pst.buy_zona,half_bars,cur_price[1],'long')
        points = self._get_points(half_bars)
        x,y = self._get_xy(points)
        trend,top_trend,bottom_trend,slope = self._get_trend_lines(x,y)
        points = self._get_points(half_bars[-len(half_bars)//4:])
        x,y = self._get_xy(points)
        trend_sm,top_trend_sm,bottom_trend_sm,slope_sm = self._get_trend_lines(x,y)
        sma_sm,bbu_sm,bbd_sm = get_bollinger_bands(np.array(pst.mpts))
        volatility = list(map(lambda x: x.spred_pt,pst.half_bars))
        volatility = get_SMA(np.array(volatility),14)
        bbu_attached = half_bars[-2].y_in_bar(bbu_sm[-1][1]) or half_bars[-1].y_in_bar(bbu_sm[-1][1])
        bbd_attached = half_bars[-2].y_in_bar(bbd_sm[-1][1]) or half_bars[-1].y_in_bar(bbd_sm[-1][1]) 
        is_big_vsai = half_bars[-1].vsai < pst.vs_bbu[-1][1]
        over_bbu = half_bars[-1].yl < bbu_sm[-1][1]
        over_bbd = half_bars[-1].yh > bbd_sm[-1][1]
        if len(pst.buy_zona) > 1:
            stop_long = (half_bars[-1].x,pst.buy_zona[-2][1][1]+volatility[-1][1])
        else:
            stop_long = (half_bars[-1].x,pst.raw_ices[-1][1]+volatility[-1][1])
        if len(pst.sell_zona) > 1:
            stop_short = (half_bars[-1].x,pst.sell_zona[-2][0][1]-volatility[-1][1])
        else:
            stop_short = (half_bars[-1].x,pst.raw_creeks[-1][1]-volatility[-1][1])

        if not self.free_stop:
            stop_long = stop_long if stop_long[1] < self.stop_long else (half_bars[-1].x,self.stop_long)
            stop_short = stop_short if stop_short[1] > self.stop_short else (half_bars[-1].x,self.stop_short)
        self.stop_long = stop_long[1]
        self.stop_short = stop_short[1]
        keys = Keys(
            cur_price[1],
            bbd_sm[-1][1],
            bbu_sm[-1][1],
            bbu_attached,
            bbd_attached,
            is_big_vsai,
            over_bbd,
            over_bbu,
            sell_zona,
            buy_zona,
            stop_long[1],
            stop_short[1],
            slope,
            slope_sm
            ) 
        if self.mode != 1:
            cv2.circle(chart,stop_long,1,(0,200,0),2)
            cv2.circle(chart,stop_short,1,(200,200,0),2)
            cv2.polylines(chart,[volatility],False,(200,200,0),1)
            cv2.polylines(chart,[sma_sm],False,(200,0,0),1)
            cv2.polylines(chart,[bbu_sm],False,(200,200,0),1)
            cv2.polylines(chart,[bbd_sm],False,(200,0,200),1)
            cv2.polylines(chart,[top_trend_sm],False,(100,0,0),2)
            cv2.polylines(chart,[bottom_trend_sm],False,(100,200,0),2)
            # cv2.polylines(chart,[pst.vsaipts],False,(242,78,168),1)
            # cv2.polylines(chart,[pst.vs_sma20],False,(217,142,127),1)
            # cv2.polylines(chart,[pst.vs_bbu],False,(177,217,141),1)
            cv2.polylines(chart,[top_trend],False,(160,217,100),2)
            cv2.polylines(chart,[bottom_trend],False,(160,217,100),2)
            cv2.polylines(chart,[pst.raw_creeks],False,(0,0,200),1)
            cv2.polylines(chart,[pst.raw_ices],False,(0,200,0),1)
            for zona in pst.sell_zona:
                cv2.rectangle(chart,zona[0],(pst.half_bars[-1].x,zona[1][1]),(139,71,219),1)
            for zona in  pst.buy_zona:
                cv2.rectangle(chart,zona[0],(pst.half_bars[-1].x,zona[1][1]),(71,219,195),1)
            # cv2.polylines(chart,[v_sma],False,(230,100,100),1)
            # cv2.putText(chart,'Lock: '+str(lock),(0,20),cv2.FONT_HERSHEY_SIMPLEX,0.8,(20,255,255),3)
            cv2.putText(chart,"Slope: " +str(slope),(0,25),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
            cv2.putText(chart,"Slope_sm: " +str(slope_sm),(0,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
            cv2.putText(chart,"FS: " +str(self.free_stop),(0,70),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
            # cv2.putText(chart,"DLR: "+str(dynamics_lr),(0,70),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
            # cv2.putText(chart,"DLRa: "+str(dynamics_lr_50),(0,90),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,205,155),2)
            cv2.putText(chart,"bbuAt: "+str(bbu_attached),(0,110),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,205,155),2)
            cv2.putText(chart,"bbdAt: "+str(bbd_attached),(0,130),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,205,155),2)
            cv2.putText(chart,"VSAI: "+str(is_big_vsai),(0,150),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,205,155),2)
            cv2.putText(chart,"SUA: "+str(self.bbu_attached),(0,165),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,205,155),2)
            cv2.putText(chart,"SDA: "+str(self.bbd_attached),(0,180),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,205,155),2)
            cv2.putText(chart,"SZ: "+str(sell_zona),(0,195),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,205,155),2)
            cv2.putText(chart,"BZ: "+str(buy_zona),(0,210),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,205,155),2)
        return keys
    def _get_action(self,keys:Keys):
        if keys.slope < -0.1:
            if keys.cur_price > keys.stop_long:
                return 'close_long'
            if keys.bbu_attached and keys.is_big_vsai:
                return 'close_long'
            if not keys.bbu_attached and self.bbu_attached:
                return 'close_long'
            if keys.over_bbu:
                return 'close_long'
            if keys.slope_sm < 0.1:
                if keys.buy_zona:
                    return 'long'
            else:
                if keys.sell_zona:
                    return 'close_long'
        elif keys.slope > 0.1:
            if keys.cur_price < keys.stop_short:
                return 'close_short'
            if keys.bbd_attached and keys.is_big_vsai:
                return 'close_short'
            if not keys.bbd_attached and self.bbd_attached:
                return 'close_short'
            if keys.over_bbd:
                return 'close_short'
            if keys.slope_sm > -0.1:
                if keys.sell_zona:
                    return 'short'
            else:
                if keys.buy_zona:
                    return 'close_short'
        else:
            if keys.slope_sm > 0.1:
                if keys.buy_zona:
                    return 'long'
            if keys.slope_sm < -0.1:
                if keys.sell_zona:
                    return 'short'
                
    def _test(self, img,price):
        m_keys = self._get_keys(img,self.minute_chart_region)
        # h_keys = self._get_keys(img,self.hour_chart_region)
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
        self.bbd_attached = m_keys.bbd_attached
        self.bbu_attached = m_keys.bbu_attached
        self.write_logs(m_keys,action)
        
        
    
    def _traide(self, img):
        pos = self._check_position(img)
        m_keys = self._get_keys(img,self.minute_chart_region)
        action = self._get_action(m_keys)
        if pos == 0:
            self.free_stop = True
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
        m_keys = self._get_keys(img,self.minute_chart_region)
        save_dir= './test_images/'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        self.i += 1
        img_name = save_dir + self.name + str(self.i) +'.png'
        cv2.imwrite(img_name,img)

    def write_logs(self,keys,action):
        file_name = f'./logs/{self.traider_name}{self.name}.txt'
        log = f'{self.name} - {time()} - {action}: state: {vars(keys)}\n'
        if not os.path.exists(file_name):
            with open(file_name, 'w') as f:
                f.write(log)
        else:
            with open(file_name, 'a') as f:
                f.write(log)

class PST1a(PST1):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'PST1a'
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
        if res2 == 1:
            self.free_stop = False
        self.bbd_attached = m_keys.bbd_attached
        self.bbu_attached = m_keys.bbu_attached
        self.write_logs(m_keys,action)