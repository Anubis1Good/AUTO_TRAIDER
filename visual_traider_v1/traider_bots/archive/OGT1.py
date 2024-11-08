from time import time
import cv2
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.VSA import VSA
from utils.chart_utils.dtype import HalfBar
class Keys:
    def __init__(self,cur_price:tuple,vsa:VSA,formation:str,short_bar1:int,long_bar1:int,short_bar1y:int,long_bar1y:int,last_hb:HalfBar,short_bar_cp:int,long_bar_cp:int) -> None:
        self.cur_price = cur_price
        self.vsa = vsa
        self.formation = formation
        self.short_bar1 = short_bar1
        self.long_bar1 = long_bar1
        self.short_bar1y = short_bar1y
        self.long_bar1y = long_bar1y
        self.last_hb = last_hb
        self.short_bar_cp = short_bar_cp
        self.long_bar_cp = long_bar_cp

class OGT1(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'OGT1'
        self.close_long = False
        self.close_short = False
        self.check_bar_long = False
        self.check_bar_short = False
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
        vsa = VSA(half_bars)
        formation = vsa.formation
        short_bar1,short_bar2,long_bar1,long_bar2,rotate_short,rotate_long = vsa.get_important_bars()
        # short_bar1 = short_bar2
        # long_bar1 = long_bar2
        short_bar1y = vsa.get_important_bars_y(vsa.full_bars[-1].yc)[1]
        long_bar1y = vsa.get_important_bars_y(vsa.full_bars[-1].yc)[3]
        short_bar_cp = vsa.get_important_bars_y(cur_price[1])[1]
        long_bar_cp = vsa.get_important_bars_y(cur_price[1])[3]
        keys = Keys(cur_price,vsa,formation,short_bar1,long_bar1,short_bar1y,long_bar1y,half_bars[-1],short_bar_cp,long_bar_cp)
        # print(short_bar1y,long_bar1y)
        if self.mode != 1:
            vsa.draw_context(chart)
            cv2.putText(chart,"Formation: " +str(formation),(0,20),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
            cv2.putText(chart,"check_long: " +str(self.check_bar_long),(0,35),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
            cv2.putText(chart,"check_short: " +str(self.check_bar_short),(0,50),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
            if short_bar1:
                cv2.line(chart,vsa.full_bars[short_bar1].hpt,vsa.full_bars[short_bar1].lpt,(255,130,165),1)
            if long_bar1:
                cv2.polylines(chart,[vsa.full_bars[long_bar1].draw_line],False,(45,166,69),1)
            if short_bar1y:
                cv2.line(chart,vsa.full_bars[short_bar1y].hpt,vsa.full_bars[short_bar1y].lpt,(255,0,72),1)
            if long_bar1y:
                cv2.polylines(chart,[vsa.full_bars[long_bar1y].draw_line],False,(0,255,51),1)
            if short_bar_cp:
                cv2.polylines(chart,[vsa.full_bars[short_bar_cp].draw_line],False,(148,0,250),2)
                # cv2.line(chart,vsa.full_bars[short_bar_cp].mpt,(vsa.full_bars[-1].x,vsa.full_bars[short_bar_cp].ym),(0,0,255),2)
            if long_bar_cp:
                cv2.polylines(chart,[vsa.full_bars[long_bar_cp].draw_line],False,(0,250,241),2)
                # cv2.line(chart,vsa.full_bars[long_bar_cp].mpt,(vsa.full_bars[-1].x,vsa.full_bars[long_bar_cp].ym),(0,0,255),2)
            # cv2.polylines(chart,[vsa.full_bars[-1].draw_line],False,(255,229,250),2)
            
        return keys
    
    def _get_action(self,keys:Keys):
        formation = keys.formation
        context = keys.vsa.context
        full_context = keys.vsa.full_context
        delta = keys.vsa.delta
        cur_price = keys.cur_price[1]
        # cur_bar,_ = keys.vsa.get_context_y(cur_price)
        short_bar1c = keys.short_bar1
        long_bar1c = keys.long_bar1
        short_bar1y = keys.short_bar1y
        long_bar1y = keys.long_bar1y
        if keys.vsa.full_bars[long_bar1c].yl > cur_price:
            self.check_bar_long = True 
        if keys.vsa.full_bars[short_bar1c].yh < cur_price:
            self.check_bar_short = True 
        if self.check_bar_short:
            short_bar1 = short_bar1c
        else:
            short_bar1 = short_bar1y
        if self.check_bar_long:
            long_bar1 = long_bar1c
        else:
            long_bar1 = long_bar1y
        short_bar_cp = keys.short_bar_cp
        long_bar_cp = keys.long_bar_cp
        zone = self._check_zona(keys,short_bar1y,long_bar1y)
        save_zone = self._check_zona(keys,short_bar_cp,long_bar_cp)
        if keys.vsa.context == 1 and keys.vsa.formation != 'strong_long':
            delta_a = (full_context[0][1] - full_context[1][1])//2
            delta_b = (full_context[2][1] - full_context[1][1])//2
        if keys.vsa.context == -1 and keys.vsa.formation != 'strong_short':
            delta_a = (full_context[1][1] - full_context[0][1])//2
            delta_b = (full_context[1][1] - full_context[2][1])//2
        if formation == 'long':
            if cur_price > full_context[0][1] - delta_a:
                if zone == 'long_zone':
                    return 'long'

            if self.is_close_long(long_bar1,cur_price,keys,save_zone,delta_b):
                return 'close_long'
        if formation == 'strong_long':
            if cur_price > full_context[1][1] + delta:
                if zone == 'long_zone':
                    return 'long'
            if self.is_close_long(long_bar1,cur_price,keys,save_zone,0):
                return 'close_long'
        if formation == 'short':
            if cur_price < full_context[0][1] + delta_a:
                if zone == 'short_zone':
                    return 'short'

            if self.is_close_short(short_bar1,cur_price,keys,save_zone,delta_b):  
                return 'close_short'
        if formation == 'strong_short':
            if cur_price < full_context[1][1] - delta:
                if zone == 'short_zone':
                    return 'short'
            if self.is_close_short(short_bar1,cur_price,keys,save_zone,0):  
                return 'close_short'
        if formation == 'range':
            if context == 1:
                if cur_price > full_context[2][1] - delta:
                    if zone == 'long_zone':
                        return 'long'
                if cur_price < full_context[3][1] + delta:
                    if zone == 'short_zone':
                        return 'short'
            if context == -1:
                if cur_price > full_context[3][1] - delta:
                    if zone == 'long_zone':
                        return 'long'
                if cur_price < full_context[2][1] + delta:
                    if zone == 'short_zone':
                        return 'short'
            if self.is_close_long(long_bar1,cur_price,keys,save_zone,delta_b):
                return 'close_long'
            if self.is_close_short(short_bar1,cur_price,keys,save_zone,delta_b):  
                return 'close_short'
                    
        if formation == 'long_flag':
            if cur_price > full_context[2][1] - keys.vsa.help_delta:
                if zone == 'long_zone':
                    return 'long'
            if self.is_close_long(long_bar1,cur_price,keys,save_zone,delta_b):
                return 'close_long'
        if formation == 'short_flag':
            if cur_price < full_context[2][1] + keys.vsa.help_delta:
                if zone == 'short_zone':
                    return 'short'
            if self.is_close_short(short_bar1,cur_price,keys,save_zone,delta_b):  
                return 'close_short'
        if formation == 'base_triangle':
            if context == 1:
                if cur_price > full_context[2][1] - delta:
                    if zone == 'long_zone':
                        return 'long'
                if self.is_close_long(long_bar1,cur_price,keys,save_zone,delta_b):
                    return 'close_long'
            if context == -1:
                if cur_price < full_context[2][1] + delta:
                    if zone == 'short_zone':
                        return 'short'
                if self.is_close_short(short_bar1,cur_price,keys,save_zone,delta_b):  
                    return 'close_short'
        if formation == 'preload_triangle':
            if context == 1:
                if cur_price > full_context[3][1] - delta:
                    if zone == 'long_zone':
                        return 'long'
                if self.is_close_long(long_bar1,cur_price,keys,save_zone,delta_b):
                    return 'close_long'
            if context == -1:
                if cur_price < full_context[3][1] + delta:
                    if zone == 'short_zone':
                        return 'short'
                if self.is_close_short(short_bar1,cur_price,keys,save_zone,delta_b):  
                    return 'close_short'
        if formation == 'local_range':
            if context == 1:
                if cur_price > full_context[2][1] - keys.vsa.help_delta:
                    if zone == 'long_zone':
                        return 'long'
                if cur_price < full_context[3][1] + keys.vsa.help_delta:
                    if zone == 'short_zone':
                        return 'short'
            if context == -1:
                if cur_price > full_context[3][1] - keys.vsa.help_delta:
                    if zone == 'long_zone':
                        return 'long'
                if cur_price < full_context[2][1] + keys.vsa.help_delta:
                    if zone == 'short_zone':
                        return 'short'
            if self.is_close_long(long_bar1,cur_price,keys,save_zone,delta_b):
                return 'close_long'
            if self.is_close_short(short_bar1,cur_price,keys,save_zone,delta_b):  
                return 'close_short'

    def is_close_long(self,long_bar1,cur_price,keys:Keys,save_zone,delta_b):
        if long_bar1 and save_zone != 'long_zone':
            if keys.last_hb.yh > keys.vsa.full_bars[long_bar1].yl:
                return True
        if save_zone == 'short_zone' and cur_price < keys.vsa.full_context[0][1] + delta_b:
            return True
        if keys.vsa.max_vsai / keys.last_hb.vsai > 0.9:
            return True
        return False

    def is_close_short(self,short_bar1,cur_price,keys:Keys,save_zone,delta_b):
        if short_bar1 and save_zone != 'short_zone':
            if keys.last_hb.yl < keys.vsa.full_bars[short_bar1].yh:
                return True
        if save_zone == 'long_zone' and  cur_price > keys.vsa.full_context[0][1] - delta_b:
            return True
        if keys.vsa.max_vsai / keys.last_hb.vsai > 0.9:
            return True
        return False


    
    def _test(self, img,price):
        m_keys = self._get_keys(img,self.minute_chart_region)
        action = self._get_action(m_keys)
        res,res2 = 0,0
        
        if self.save_all_img:
            self.i+=1
            cv2.imwrite('./test_images/'+self.name+str(self.i)+'.png',img)
        if action == 'long':
            res = self._test_send_close(img,'short',price=price)
            res2 = self._test_send_open(img,'long',price=price) 
        if action == 'close_long':
            res = self._test_send_close(img,'long',price=price)
        if action == 'short':
            res = self._test_send_close(img,'long',price=price)
            res2 = self._test_send_open(img,'short',price=price)
        if action == 'close_short':
            res = self._test_send_close(img,'short',price=price)
        if res == 1 or res2 == 1:
            self._reset_check()

    
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
    

    def _check_zona(self,keys:Keys,short_bar1,long_bar1):
        cur_price = keys.cur_price[1]
        if short_bar1:
            if keys.vsa.check_overlap(short_bar1,'top')[0]:
                if keys.vsa.full_bars[short_bar1].spred / keys.vsa.max_spred  > 0.5:
                    end_point = keys.vsa.full_bars[short_bar1].pred_yl
                else:
                    end_point = keys.vsa.full_bars[short_bar1].ym
                if keys.vsa.full_bars[short_bar1].yl > cur_price > end_point:
                    return 'long_zone'
            else:
                if keys.vsa.full_bars[short_bar1].spred / keys.vsa.max_spred  > 0.5:
                    end_point = keys.vsa.full_bars[short_bar1].pred_yh
                else:
                    end_point = keys.vsa.full_bars[short_bar1].ym
                if keys.vsa.full_bars[short_bar1].yh < cur_price < end_point:
                    return 'short_zone'
        if long_bar1:
            if keys.vsa.check_overlap(long_bar1,'bottom')[0]:
                if keys.vsa.full_bars[long_bar1].spred / keys.vsa.max_spred  > 0.5:
                    end_point = keys.vsa.full_bars[long_bar1].pred_yh
                else:
                    end_point = keys.vsa.full_bars[long_bar1].ym
                if keys.vsa.full_bars[long_bar1].yh < cur_price < end_point:
                    return 'short_zone'
            else:
                if keys.vsa.full_bars[long_bar1].spred / keys.vsa.max_spred  > 0.5:
                    end_point = keys.vsa.full_bars[long_bar1].pred_yl
                else:
                    end_point = keys.vsa.full_bars[long_bar1].ym
                if keys.vsa.full_bars[long_bar1].yl > cur_price > keys.vsa.full_bars[long_bar1].ym:
                    return 'long_zone'
            
    def _reset_check(self):
        self.check_bar_long = False
        self.check_bar_short = False
        
            