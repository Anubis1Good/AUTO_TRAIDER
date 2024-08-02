import cv2
import os
import numpy as np
import numpy.typing as npt
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.indicators import get_bollinger_bands, get_context, get_zona, get_SMA, get_last_pick, get_dynamics
class ST1(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'ST1'
        self.i = 0


    def _get_keys(self, img, region) -> dict:
        chart = self._get_chart(img,region)
        candle_mask = self._get_candle_mask(chart)
        volume_mask = self._get_volume_mask(chart)
        candle_cords = self._get_cords_on_mask(candle_mask)
        volume_cords = self._get_cords_on_mask(volume_mask)
        half_bars = self._get_half_bars(candle_mask,candle_cords,volume_cords)
        mpts = []
        vpts = []
        for i in range(len(half_bars)):
            mpt = half_bars[i].mpt
            vpt = half_bars[i].vpt
            mpts.append(mpt)
            vpts.append(vpt)
        vpts = np.array(vpts)
        v_sma = get_SMA(vpts,20)

        max_hb,min_hb,local_hb,direction,max_hb_i,min_hb_i = get_context(half_bars)

        points = self._get_points(half_bars)
        x,y = self._get_xy(points)
        trend,top_trend,bottom_trend,slope = self._get_trend_lines(x,y)
        cur_price = self._get_current_price(chart)
        zona,m_pt_zona = get_zona(half_bars,cur_price,vpts,v_sma)
        sma20,bbu,bbd = get_bollinger_bands(np.array(mpts))
        dynamics = get_dynamics(sma20)
        context_polyline = []   
        delta_global = min_hb.yl - max_hb.yh
        if direction == 'long':
            delta_local = local_hb.yl - max_hb.yh
            delta_cur_price = cur_price[1] - max_hb.yh
            slice_global = half_bars[min_hb_i:]
            context_polyline.append(min_hb.lpt)
            context_polyline.append(max_hb.hpt)
            context_polyline.append(local_hb.lpt)
        else:
            delta_local = min_hb.yl - local_hb.yh
            delta_cur_price = min_hb.yl - cur_price[1]
            slice_global = half_bars[max_hb_i:]
            context_polyline.append(max_hb.hpt)
            context_polyline.append(min_hb.lpt)
            context_polyline.append(local_hb.hpt)
        context_polyline = np.array(context_polyline)

        relation_lg = delta_local/delta_global
        relation_cl = delta_cur_price/delta_local
        points = self._get_points(slice_global)
        x,y = self._get_xy(points)
        trend_sg,top_trend_sg,bottom_trend_sg,slope_sg = self._get_trend_lines(x,y)
        last_pick = get_last_pick(half_bars,top_trend_sg,bottom_trend_sg)
        # buffer = (trend_sg[-1][1] - top_trend_sg[-1][1] )//2
        buffer = (sma20[-1][1] - bbu[-1][1] )//2
        keys = {
            'cur_price':cur_price,
            # 'trend':trend,
            # 'top_trend':top_trend,
            # 'bottom_trend':bottom_trend,
            'trend_sg':trend_sg,
            'top_trend_sg':top_trend_sg,
            'bottom_trend_sg':bottom_trend_sg,
            'vpts':vpts,
            'v_sma':v_sma,
            'slope':slope,
            'zona':zona,
            'relation_lg':round(relation_lg,2),
            'relation_cl':round(relation_cl,2),
            'direction':direction,
            'm_pt_zona':m_pt_zona,
            'last_pick':last_pick,
            # 'top_quarter': top_trend_sg[-1][1] + buffer,
            # 'bottom_quarter': bottom_trend_sg[-1][1] - buffer,
            'top_quarter': bbu[-1][1] + buffer,
            'bottom_quarter': bbd[-1][1] - buffer,
            'context_polyline': context_polyline,
            'sma20':sma20,
            'bbu':bbu,
            'bbd':bbd,
            'dynamics':dynamics,
            'last_hb':half_bars[-2]
            # 'trend_sl':trend_sl,
            # 'top_trend_sl':top_trend_sl,
            # 'bottom_trend_sl':bottom_trend_sl,            

        }
        return keys
    
    def _draw(self,img,keys:dict,region):
        keys_copy = keys.copy()
        colors = (
            (255,255,255),
            (145,145,245),
            (235,135,135),
            (230,100,0),
            (230,200,50),
            (230,100,200),
            (130,100,0),
            (130,200,50),
            (130,100,200),
            (30,200,10),
            (230,10,200),
        )
        i = 0
        for key in keys_copy:
            if 'numpy.ndarray' in str(type(keys_copy[key])):
                keys_copy[key] = np.array(list(map(lambda x:self._change_coords(x,region), keys_copy[key])))
                cv2.polylines(img,[keys_copy[key]],False,colors[i],2)
                i += 1

        cv2.circle(img,(keys['trend_sg'][-1][0]+region[0],keys['top_quarter']+region[1]),1,(255,100,100),3)
        cv2.circle(img,(keys['trend_sg'][-1][0]+region[0],keys['bottom_quarter']+region[1]),1,(255,100,100),3)
        cv2.putText(img,str(keys['relation_lg']),(region[0],region[1]+20),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
        cv2.putText(img,str(keys['relation_cl']),(region[0],region[1]+40),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
        cv2.putText(img,str(keys['direction']),(region[0],region[1]+60),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
        cv2.putText(img,str(keys['last_pick']),(region[0],region[1]+80),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
        cv2.putText(img,str(keys['dynamics']),(region[0],region[1]+100),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
        return img

    def _all_draw(self,img,m_keys,h_keys):
        img = self._draw(img,m_keys,self.minute_chart_region)
        img = self._draw(img,h_keys,self.hour_chart_region)
        return img
    
    def _check_over_limit(self,keys):
        if keys['bbd'][-1][1] < keys['cur_price'][1] > keys['bottom_trend'][-1][1]:
            return 1
        if keys['bbu'][-1][1] > keys['cur_price'][1] < keys['top_trend'][-1][1]:
            return -1
        return 0
    
    def _check_price_in_trend(self,keys):
        return keys['top_trend'][-1][1] < keys['cur_price'][1] < keys['bottom_trend'][-1][1]
    
    def _check_volume_over(self,keys):
        return keys['vpts'][-1][1] < keys['v_sma'][-1][1]
    
    def _get_direction(self,keys):
        if keys['relation_lg'] > 0.7 and keys['relation_cl'] > 0.7:
            if keys['zona'] :
                if keys['cur_price'][1] > keys['m_pt_zona']:
                    if keys['direction'] == 'long':
                        return 'long'
                else:
                    if keys['direction'] == 'short':
                        return 'short'                  
        if keys['relation_cl'] < 0.3:
            if keys['zona']:
                if keys['cur_price'][1] > keys['m_pt_zona']:
                    if keys['direction'] == 'short':
                        return 'close_short'
                    
                else:
                    if keys['direction'] == 'long':
                        return 'close_long'
                    
        return 'wait'

    def _get_tendency(self,keys):
        if keys['last_pick'] == 1:
            if keys['zona']:
                if keys['cur_price'][1] > keys['top_quarter']:
                    if keys['cur_price'][1] > keys['m_pt_zona'] or self._check_volume_over(keys):
                        return 'long'
                if keys['cur_price'][1] < keys['top_trend_sg'][-1][1]:
                    if keys['cur_price'][1] < keys['m_pt_zona'] or self._check_volume_over(keys):
                        return 'close_long'
        if keys['last_pick'] == -1:
            if keys['zona']:
                if keys['cur_price'][1] < keys['bottom_quarter']:
                    if keys['cur_price'][1] < keys['m_pt_zona'] or self._check_volume_over(keys):
                        return 'short'
                if keys['cur_price'][1] > keys['bottom_trend_sg'][-1][1]:
                    if keys['cur_price'][1] > keys['m_pt_zona'] or self._check_volume_over(keys):
                        return 'close_short'
        return 'wait'
    
    def _get_wave(self,keys):
        lock = self._check_lock(keys)
        if keys['zona']:
            if keys['dynamics'] < -10:
                if keys['cur_price'][1] > keys['sma20'][-1][1]:
                    return 'long'
                if lock == 1:
                    return 'close_long'
            if keys['dynamics'] > 10:
                if keys['cur_price'][1] < keys['sma20'][-1][1]:
                    return 'short'
                if lock == -1:
                    return 'close_short'
            if lock == 1:
                return 'close_long'
            if lock == -1:
                return 'close_short'

    def _check_lock(self,keys):
        if keys['cur_price'][1] > keys['bbd'][-1][1] < keys['last_hb'].yl:
            return -1
        if keys['cur_price'][1] < keys['bbu'][-1][1] > keys['last_hb'].yh:
            return 1
        return 0 
        

    def _test(self, img):
        h_keys = self._get_keys(img,self.hour_chart_region)
        m_keys = self._get_keys(img,self.minute_chart_region)
        draw_func = lambda img:self._all_draw(img,m_keys,h_keys)
        # open
        # price in range_channel
        # price in long_channel
        # price in short_channel
        h_direction = self._get_direction(h_keys)
        m_direction = self._get_direction(m_keys)
        image = img.copy()
        image = draw_func(image)
        save_dir= './test_images/'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        self.i += 1
        img_name = save_dir + self.name + str(self.i) +'.png'
        # cv2.imwrite(img_name,image)
        wave = self._get_wave(m_keys)
        # m_tendency = self._get_tendency(m_keys)
        if wave == 'long':
            self._test_send_close(img,'short',draw_func)
            self._test_send_open(img,'long',draw_func) 
        if wave == 'close_long':
            self._test_send_close(img,'long',draw_func)
        if wave == 'short':
            self._test_send_close(img,'long',draw_func)
            self._test_send_open(img,'short',draw_func)
        if wave == 'close_short':
            self._test_send_close(img,'short',draw_func)
        # if h_direction == 'long' or h_direction == 'try_long':
        #     if m_direction == 'long' or m_direction == 'try_long':
        #         self._test_send_close(img,'short',draw_func)
        #         self._test_send_open(img,'long',draw_func)
        # elif h_direction == 'short' or h_direction == 'try_short':
        #     if m_direction == 'short' or m_direction == 'try_short':
        #         self._test_send_close(img,'long',draw_func)
        #         self._test_send_open(img,'short',draw_func)
        # else:
        # if m_direction == 'long':
        #     self._test_send_close(img,'short',draw_func)
        #     self._test_send_open(img,'long',draw_func)
        # if m_direction == 'short':
        #     self._test_send_close(img,'long',draw_func)
        #     self._test_send_open(img,'short',draw_func)
        # if m_direction == 'close_long':
        #     self._test_send_close(img,'long',draw_func)
        # if m_direction == 'close_short':
        #     self._test_send_close(img,'short',draw_func)

        # if self._check_vsai_over(m_keys):
        #     if self._check_price_in_trend(h_keys) and h_keys['slope'] < -0.1:
        #         if self._check_over_limit(m_keys) == 1:
        #             self._test_send_open(img,'long',draw_func)

        #     if self._check_price_in_trend(h_keys) and h_keys['slope'] > 0.1:
        #         if self._check_over_limit(m_keys) == -1:
        #             self._test_send_open(img,'short',draw_func)

        
        # vsai 

        # if m_keys['cur_price'][1] > m_keys['m_sma'][-1][1]:
        #     self._test_send_close(img,'short',draw_func)
        # if m_keys['cur_price'][1] < m_keys['m_sma'][-1][1]:
        #     self._test_send_close(img,'long',draw_func)
        # price in overlimit
        # if m_keys['last_hpt'][1] <= m_keys['bbu'][-1][1] and self._check_over_limit(m_keys) == -1 and m_keys['slope'] > -0.1:
        #         self._test_send_open(img,'long',draw_func)
        # if m_keys['last_lpt'][1] >= m_keys['bbd'][-1][1] and self._check_over_limit(m_keys) == 1 and m_keys['slope'] < 0.1:
        #         self._test_send_open(img,'short',draw_func)

        # # close
        # if m_keys['last_hpt'][1] > m_keys['s_bbu'][-1][1] < m_keys['cur_price'][1]:
        #     self._test_send_close(img,'long',draw_func)
        # if m_keys['last_lpt'][1] < m_keys['s_bbd'][-1][1] > m_keys['cur_price'][1]:
        #     self._test_send_close(img,'short',draw_func)