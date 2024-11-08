from time import time
import cv2
import os
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.VSA import VSA
from utils.chart_utils.dtype import FullBar
class Keys:
    def __init__(self,cur_price:int,long_bar:int,short_bar:int,vsa:VSA) -> None:
        self.cur_price = cur_price
        self.long_bar = long_bar
        self.short_bar = short_bar
        self.vsa = vsa


class OGT2(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'OGT2'
        self.close_long = False
        self.close_short = False
        self.stop_long = 1000
        self.stop_short = -1
        self.pos = 0
        self.i = 0
        self.save_all_img = False

    def _get_keys(self, img, region) -> dict:
        chart = self._get_chart(img,region)
        candle_mask = self._get_candle_mask(chart)
        volume_mask = self._get_volume_mask(chart)
        candle_cords = self._get_cords_on_mask(candle_mask)
        volume_cords = self._get_cords_on_mask(volume_mask)
        half_bars = self._get_half_bars(candle_mask,candle_cords,volume_cords)
        cur_price = self._get_current_price(chart)
        vsa = VSA(half_bars,step_bb_vsai=20)
        short_bar1,short_bar2,long_bar1,long_bar2,rotate_short,rotate_long = vsa.get_important_bars_y(cur_price[1])

        keys = Keys(cur_price[1],long_bar2,short_bar2,vsa)
        if self.mode != 1:
            if rotate_long:
                cv2.polylines(chart,[vsa.full_bars[rotate_long].draw_line],False,(0,255,250),2)
            if rotate_short:
                cv2.polylines(chart,[vsa.full_bars[rotate_short].draw_line],False,(250,255,0),2)
            
        return keys
    
    def _get_action(self,keys:Keys):
        price = keys.cur_price
        long_bar = keys.long_bar
        short_bar = keys.short_bar
        vsa = keys.vsa
        
        if self.pos:
            if price > self.stop_long or price < self.stop_short:
                if self.pos == 1:
                    return 'close_long'
                else:
                    return 'close_short'
        if long_bar:
            if vsa.full_bars[long_bar].yh < price < vsa.full_bars[long_bar].ym:
                overlap,j = vsa.check_overlap(long_bar,'bottom')
                # retest,_ = vsa.check_retest(long_bar,'top',j)
                if overlap:
                    self.stop_long = vsa.full_bars[long_bar].yl
                    self.stop_short = vsa.full_bars[long_bar].yh
                    return 'short'
        if short_bar:
            if vsa.full_bars[short_bar].yl > price > vsa.full_bars[short_bar].ym:
                overlap,j = vsa.check_overlap(short_bar,'top')
                # retest,_ = vsa.check_retest(short_bar,'bottom',j)
                if overlap:
                    self.stop_long = vsa.full_bars[long_bar].yl
                    self.stop_short = vsa.full_bars[long_bar].yh
                    return 'long'
            
            
            
    def _reset_stop(self):
        self.stop_long = 1000
        self.stop_short = -1




    
    def _test(self, img,price):
        m_keys = self._get_keys(img,self.minute_chart_region)
        action = self._get_action(m_keys)
        res_l,res2_l = 0,0
        res_s,res2_s = 0,0
        if self.save_all_img:
            self.i+=1
            cv2.imwrite('./test_images/'+self.name+str(self.i)+'.png',img)
        if action == 'long':
            res_s = self._test_send_close(img,'short',price=price)
            res2_l = self._test_send_open(img,'long',price=price) 
        if action == 'close_long':
            res_l = self._test_send_close(img,'long',price=price)
        if action == 'short':
            res_l = self._test_send_close(img,'long',price=price)
            res2_s = self._test_send_open(img,'short',price=price)
        if action == 'close_short':
            res_s = self._test_send_close(img,'short',price=price)
        if action == 'close_all':
            res_s = self._test_send_close(img,'short',price=price)
            res_l = self._test_send_close(img,'long',price=price)
        if res_s == 1 and res2_l == 0:
            self._reset_stop()
        if res_l == 1 and res2_s == 0:
            self._reset_stop()
        if res2_s:
            self.pos = -1
        if res2_l:
            self.pos = 1 

    
    def _traide(self, img):
        pos = self._check_position(img)
        m_keys = self._get_keys(img,self.minute_chart_region)
        action = self._get_action(m_keys)
        if pos == 0:
            self._reset_check()
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
        m_keys = self._get_keys(img,self.minute_chart_region)
        save_dir= './test_images/'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        self.i += 1
        img_name = save_dir + self.name + str(self.i) +'.png'
        cv2.imwrite(img_name,img)

        
            