import cv2

import numpy as np
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.indicators import get_SMA, get_bollinger_bands,get_fractals, get_context,get_rsi,get_spred_channel,get_bb_points
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
        mpts = list(map(lambda x: x.mpt,half_bars))
        spcl = SpredChannel(half_bars)
        # spcl.draw_all(chart)
        # print(spcl.dynamics10)
        # print(spcl.dynamics_all)
        ma,ups,downs = get_bollinger_bands(np.array(mpts),1)
        draw_bollinger(chart,ma,ups,downs,thickness=2)
        # ups_p,downs_p = get_bb_points(ups,downs,3)
        # cv2.polylines(chart,[ups_p],False,(200,200,0),2)
        # cv2.polylines(chart,[downs_p],False,(200,200,200),2)
        pst = ProSveT(half_bars)
        # pst.draw_all(chart)
        # try:
        #     zona = pst.sell_zona[-1]
        #     cv2.rectangle(chart,zona[0],(pst.half_bars[-1].x,zona[1][1]),(139,11,259),3)
        #     zona = pst.buy_zona[-1]
        #     cv2.rectangle(chart,zona[0],(pst.half_bars[-1].x,zona[1][1]),(71,259,225),3)
        # except:
        #     pass
        # self.get_trends(chart,half_bars,(100,100,255))
        # self.get_trends(chart,half_bars[len(half_bars) - len(half_bars)//4:],(0,200,0))



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

    def _test(self, img):
        # self._get_dealfeed(img)

        # self.draw_all(img,self.day_chart_region)
        # self.draw_all(img,self.hour_chart_region)
        self.draw_all(img,self.minute_chart_region)

        # cv2.imwrite('test.png',img)

