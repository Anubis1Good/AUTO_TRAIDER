import cv2
import numpy as np
import numpy.typing as npt
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.indicators import get_bollinger_bands, get_dynamics, check_zona
from utils.chart_utils.ProSveT import ProSveT


class PT2(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'PT2'
        self.bbu_attached = False
        self.bbd_attached = False
        self.close_long = False
        self.close_short = False

    def _get_keys(self, img, region) -> dict:
        chart = self._get_chart(img,region)
        candle_mask = self._get_candle_mask(chart)
        volume_mask = self._get_volume_mask(chart)
        candle_cords = self._get_cords_on_mask(candle_mask)
        volume_cords = self._get_cords_on_mask(volume_mask)
        half_bars = self._get_half_bars(candle_mask,candle_cords,volume_cords)
        cur_price = self._get_current_price(chart)
        pst = ProSveT(half_bars)
        sma_sm,bbu_sm,bbd_sm = get_bollinger_bands(np.array(pst.mpts))
        sma_lr,bbu_lr,bbd_lr = get_bollinger_bands(np.array(pst.mpts),k=1,step=40)
        dynamics_sm = round(get_dynamics(sma_sm)/10,2)
        dynamics_lr = round(get_dynamics(sma_lr,20)/20,2)
        dynamics_lr_50 = round(get_dynamics(sma_lr,len(sma_lr)//2)/(len(sma_lr)//2),2)
        bbu_attached = half_bars[-2].y_in_bar(bbu_sm[-1][1]) or half_bars[-1].y_in_bar(bbu_sm[-1][1])
        bbd_attached = half_bars[-2].y_in_bar(bbd_sm[-1][1]) or half_bars[-1].y_in_bar(bbd_sm[-1][1]) 
        is_big_vsai = half_bars[-1].vsai < pst.vs_bbu[-1][1]
        over_bbu = half_bars[-1].yl < bbu_sm[-1][1]
        over_bbd = half_bars[-1].yh > bbd_sm[-1][1]
        sell_zona = check_zona(pst.sell_zona,half_bars)
        buy_zona = check_zona(pst.buy_zona,half_bars)
        # TODO 
        # 1. Расстояние между зонами, между bb
        class Keys: 
            def __init__(self):             
                self.cur_price = cur_price[1]
                self.sma_lr = sma_lr[-1][1]
                self.bbd_lr = bbd_lr[-1][1]
                self.bbu_lr = bbu_lr[-1][1]
                self.bbd_sm = bbd_sm[-1][1]
                self.bbu_sm = bbu_sm[-1][1]
                self.bbu_attached = bbu_attached
                self.bbd_attached = bbd_attached
                self.dynamics_sm = dynamics_sm
                self.dynamics_lr = dynamics_lr
                self.dynamics_lr_50 = dynamics_lr_50
                self.is_big_vsai = is_big_vsai
                self.over_bbd = over_bbd
                self.over_bbu = over_bbu
                self.sell_zona = sell_zona
                self.buy_zona = buy_zona

            
        if self.mode != 1:
            cv2.polylines(chart,[sma_sm],False,(200,0,0),1)
            cv2.polylines(chart,[bbu_sm],False,(200,200,0),1)
            cv2.polylines(chart,[bbd_sm],False,(200,0,200),1)
            cv2.polylines(chart,[sma_lr],False,(100,0,0),2)
            cv2.polylines(chart,[bbu_lr],False,(100,200,0),2)
            cv2.polylines(chart,[bbd_lr],False,(100,0,200),2)
            cv2.polylines(chart,[pst.vsaipts],False,(242,78,168),1)
            cv2.polylines(chart,[pst.vs_sma20],False,(217,142,127),1)
            cv2.polylines(chart,[pst.vs_bbu],False,(177,217,141),1)
            # cv2.polylines(chart,[pst.raw_creeks],False,(0,0,200),1)
            # cv2.polylines(chart,[pst.raw_ices],False,(0,200,0),1)
            for zona in pst.sell_zona:
                cv2.rectangle(chart,zona[0],(pst.half_bars[-1].x,zona[1][1]),(139,71,219),1)
            for zona in  pst.buy_zona:
                cv2.rectangle(chart,zona[0],(pst.half_bars[-1].x,zona[1][1]),(71,219,195),1)
            # cv2.polylines(chart,[v_sma],False,(230,100,100),1)
            # cv2.putText(chart,'Lock: '+str(lock),(0,20),cv2.FONT_HERSHEY_SIMPLEX,0.8,(20,255,255),3)
            cv2.putText(chart,"DSM: " +str(dynamics_sm),(0,50),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
            cv2.putText(chart,"DLR: "+str(dynamics_lr),(0,70),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
            cv2.putText(chart,"DLRa: "+str(dynamics_lr_50),(0,90),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,205,155),2)
            cv2.putText(chart,"bbuAt: "+str(bbu_attached),(0,110),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,205,155),2)
            cv2.putText(chart,"bbdAt: "+str(bbd_attached),(0,130),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,205,155),2)
            cv2.putText(chart,"VSAI: "+str(is_big_vsai),(0,150),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,205,155),2)
            # cv2.putText(chart,"Wave: "+str(wave),(0,110),cv2.FONT_HERSHEY_SIMPLEX,0.8,(155,205,155),2)
        return Keys()

    
    def _get_action(self,keys):
        # short_context
        if keys.dynamics_lr_50 > 0.3:
            if keys.dynamics_sm < -2 and keys.cur_price > keys.bbu_lr and keys.dynamics_lr < -0.3:
                return 'close_short'
            if keys.bbd_attached and keys.is_big_vsai:
                return 'close_short'
            if not keys.bbd_attached and self.bbd_attached:
                return 'close_short'
            if keys.over_bbd:
                return 'close_short'
            if keys.dynamics_sm > 1:
                if keys.dynamics_lr > 0.5 or keys.dynamics_sm > 2:
                    if keys.cur_price < keys.bbd_lr:
                        return 'short'
            if keys.sell_zona and keys.cur_price < keys.sma_lr and keys.dynamics_lr > 0.5:
                return 'short'
        # long_context
        elif keys.dynamics_lr_50 < -0.3:
            if keys.dynamics_sm > 2 and keys.cur_price < keys.bbd_lr and keys.dynamics_lr > 0.3:
                return 'close_long'
            if keys.bbu_attached and keys.is_big_vsai:
                return 'close_long'
            if not keys.bbu_attached and self.bbu_attached:
                return 'close_long'
            if keys.over_bbu:
                return 'close_long'
            if keys.dynamics_sm < -1:
                if keys.dynamics_lr < -0.5 or keys.dynamics_sm < -2:
                    if keys.cur_price > keys.bbu_lr:
                        return 'long'
            if keys.buy_zona and keys.cur_price > keys.sma_lr and keys.dynamics_lr < -0.5:
                return 'long'
        # range_context
        else:
            if keys.cur_price > keys.sma_lr:
                return 'close_short'
            if keys.cur_price < keys.sma_lr:
                return 'close_long'
            if keys.over_bbu:
                return 'short'
            if keys.over_bbd:
                return 'long'
            if keys.sell_zona and keys.cur_price < keys.bbu_lr:
                return 'short'
            if keys.buy_zona and keys.cur_price > keys.bbd_lr:
                return 'long'
    
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
        self.bbd_attached = m_keys.bbd_attached
        self.bbu_attached = m_keys.bbu_attached
    
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

    