import cv2

import numpy as np
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.indicators import get_SMA, get_bollinger_bands,get_fractals, get_context,get_rsi,get_spred_channel,get_bb_points,get_borders,get_williams_fractals,get_linear_reg_clear,get_donchan_channel,get_level_DC
from utils.chart_utils.general_v2 import get_divide_chart
from utils.config import ColorsBtnBGR
from  utils.chart_utils.ProSveT import ProSveT
from  utils.chart_utils.VSA import VSA
from utils.test_utils.test_draws_funcs import draw_bollinger
from utils.chart_utils.Indicators.SpredChannel import SpredChannel
class WorkBot(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'WorkBot'

    
    def draw_all(self,img,region):
        change_cords = lambda p: self._change_coords(p,region)
        chart = self._get_chart(img,region)
        candle_mask = self._get_candle_mask(chart)
        volume_mask = self._get_volume_mask(chart)
        candle_cords = self._get_cords_on_mask(candle_mask)
        volume_cords = self._get_cords_on_mask(volume_mask)
        half_bars = self._get_half_bars(candle_mask,candle_cords,volume_cords)
        cur_price = self._get_current_price(chart)
        hpts = np.array(list(map(lambda x: x.hpt,half_bars)))
        lpts = np.array(list(map(lambda x: x.lpt,half_bars)))

        vpts = np.array(list(map(lambda x: x.vpt,half_bars)))
        ups,downs,avarage = get_donchan_channel(half_bars)
        sells,byes = get_level_DC(ups,downs,10)
        # ups,downs = get_williams_fractals(hpts,lpts,8,True)
        cv2.polylines(chart,[ups],False,(255,0,200),2)
        cv2.polylines(chart,[downs],False,(55,200,250),2)
        cv2.polylines(chart,[avarage],False,(155,100,250),2)
        for sell in sells:
            cv2.rectangle(chart,sell[0],sell[1],(0,0,255),-1)
        for bye in byes:
            cv2.rectangle(chart,bye[0],bye[1],(0,255,255),-1)


        # print(chart.shape)



    def get_trends(self,chart,half_bars,color=(200,0,0)):
        points = self._get_points(half_bars)
        x,y = self._get_xy(points)
        trend,top_trend,bottom_trend,slope = self._get_trend_lines(x,y)
        cv2.polylines(chart,[trend],False,color)
        cv2.polylines(chart,[top_trend],False,color)
        cv2.polylines(chart,[bottom_trend],False,color)

        # vsa = VSA(half_bars)

        # vsa.draw_all(chart)



    def _get_dealfeed(self,img):
        dealfeed = self._get_chart(img,self.dealfeed_region)
        bid_mask = self._get_mask(dealfeed,ColorsBtnBGR.best_bid)
        ask_mask = self._get_mask(dealfeed,ColorsBtnBGR.best_ask)
        contours, hierarchy = cv2.findContours(bid_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE,offset=(self.dealfeed_region[0],self.dealfeed_region[1])) 
        cv2.drawContours(img, contours,-1,(0,255,0),3) 
        contours, hierarchy = cv2.findContours(ask_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE,offset=(self.dealfeed_region[0],self.dealfeed_region[1])) 
        cv2.drawContours(img, contours,-1,(120,155,200),3) 

    def _test(self, img,price):
        # self._get_dealfeed(img)

        # self.draw_all(img,self.day_chart_region)
        # self.draw_all(img,self.hour_chart_region)
        self.draw_all(img,self.minute_chart_region)

        # cv2.imwrite('test.png',img)

