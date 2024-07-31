import cv2
import numpy as np
import numpy.typing as npt
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.indicators import get_bollinger_bands

class ST1(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'ST1'

    def _get_keys(self, img, region) -> dict:
        chart = self._get_chart(img,region)
        candle_mask = self._get_candle_mask(chart)
        volume_mask = self._get_volume_mask(chart)
        candle_cords = self._get_cords_on_mask(candle_mask)
        volume_cords = self._get_cords_on_mask(volume_mask)
        half_bars = self._get_half_bars(candle_mask,candle_cords,volume_cords)
        mpts = []
        vsaipts = []
        for i in range(len(half_bars)):
            mpt = half_bars[i].mpt
            vsaipt = half_bars[i].vsaipt
            mpts.append(mpt)
            vsaipts.append(vsaipt)
        vsaipts = np.array(vsaipts)
        vsai_sma,vsai_bbu,vsai_bbd = get_bollinger_bands(vsaipts,1)
        m_sma,bbu,bbd = get_bollinger_bands(np.array(mpts))
        s_m_sma,s_bbu,s_bbd = get_bollinger_bands(np.array(mpts),1)
        points = self._get_points(half_bars)
        x,y = self._get_xy(points)
        trend,top_trend,bottom_trend,slope = self._get_trend_lines(x,y)
        cur_price = self._get_current_price(chart)
        keys = {
            'cur_price':cur_price,
            'trend':trend,
            'top_trend':top_trend,
            'bottom_trend':bottom_trend,
            'm_sma':m_sma,
            'bbu':bbu,
            'bbd':bbd,
            's_m_sma':s_m_sma,
            's_bbu':s_bbu,
            's_bbd':s_bbd,
            'vsaipts':vsaipts,
            'vsai_bbd':vsai_bbd,
            'slope':slope,
            'stop':(trend[-1][1]-top_trend[-1][1])//2,
            'last_hpt':half_bars[-2].hpt,
            'last_lpt':half_bars[-2].lpt
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
    
    def _check_vsai_over(self,keys):
        return keys['vsaipts'][-1][1] > keys['vsai_bbd'][-1][1]
    
    def _test(self, img):
        h_keys = self._get_keys(img,self.hour_chart_region)
        m_keys = self._get_keys(img,self.minute_chart_region)
        draw_func = lambda img:self._all_draw(img,m_keys,h_keys)
        # open
        # price in range_channel
        # price in long_channel
        # price in short_channel

        if self._check_vsai_over(m_keys):
            if self._check_price_in_trend(h_keys) and h_keys['slope'] < -0.1:
                if self._check_over_limit(m_keys) == 1:
                    self._test_send_open(img,'long',draw_func)

            if self._check_price_in_trend(h_keys) and h_keys['slope'] > 0.1:
                if self._check_over_limit(m_keys) == -1:
                    self._test_send_open(img,'short',draw_func)

        
        # vsai 

        if m_keys['cur_price'][1] > m_keys['m_sma'][-1][1]:
            self._test_send_close(img,'short',draw_func)
        if m_keys['cur_price'][1] < m_keys['m_sma'][-1][1]:
            self._test_send_close(img,'long',draw_func)
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