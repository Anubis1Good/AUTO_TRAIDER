import cv2
import numpy as np
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.indicators import get_SMA, get_bollinger_bands,get_fractals
from utils.config import ColorsBtnBGR
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
        colors = (
            (100,200,0),
            (0,200,100),
            (200,0,100)
        )
        mean_volume = self._get_mean(volume_cords)
        vpts = []
        mpts = []
        hpts = []
        lpts = []
        vsaipts = []
        for i in range(len(half_bars)):
            hpt,lpt,vpt = half_bars[i].to_img_cords(change_cords)
            mpt = change_cords(half_bars[i].mpt)
            vsaipt = change_cords(half_bars[i].vsaipt)
            mpts.append(mpt)
            vpts.append(vpt)
            hpts.append(hpt)
            lpts.append(lpt)
            vsaipts.append(vsaipt)

        vsaipts = np.array(vsaipts)
        vsai_sma,vsai_bbu,vsai_bbd = get_bollinger_bands(vsaipts,1)
        cv2.polylines(img,[vsaipts],False,(0,240,20),1)
        cv2.polylines(img,[vsai_sma],False,(200,40,20),1)
        cv2.polylines(img,[vsai_bbd],False,(00,40,200),1)
        cv2.polylines(img,[vsai_bbu],False,(200,40,20),1)
        cv2.line(img,hpts[-2],lpts[-2],(0,250,0),2)
        #     if half_bars[i].is_big_volume(mean_volume[1]): 
        #         cv2.circle(img,vpt,1,(0,200,0))
        #         cv2.line(img,hpt,lpt,colors[1],1)
        # period = 27
        # V_sma = get_SMA(np.array(vpts),period)
        m_sma,bbu,bbd = get_bollinger_bands(np.array(mpts))
        # _,bbu1,bbd1 = get_bollinger_bands(np.array(mpts),1)
        # cv2.polylines(img,[V_sma],False,(176,80,10),2)
        cv2.polylines(img,[m_sma],False,(176,180,10),1)
        cv2.polylines(img,[bbu],False,(176,80,90),2)
        cv2.polylines(img,[bbd],False,(176,80,90),2)
        # cv2.polylines(img,[bbu1],False,(176,180,90),2)
        # cv2.polylines(img,[bbd1],False,(176,180,90),2)
        # mean_volume = change_cords(mean_volume)
        # cv2.circle(img,mean_volume,1,(150,200,70),3)
        # points = self._get_points(half_bars)
        # for i in range(points.shape[0]):
        #     points[i] = change_cords(points[i])
        # x,y = self._get_xy(points)
        # trend,top_trend,bottom_trend,slope = self._get_trend_lines(x,y)
        # cv2.polylines(img,[trend],False,(255,255,255),2)
        # cv2.polylines(img,[top_trend],False,(255,255,255),2)
        # cv2.polylines(img,[bottom_trend],False,(255,255,255),2)

        # maxs,mins = get_fractals(hpts,lpts)

        # cv2.polylines(img,[maxs],False,(55,155,255),2)
        # cv2.polylines(img,[mins],False,(55,55,255),2)

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

        self.draw_all(img,self.day_chart_region)
        self.draw_all(img,self.hour_chart_region)
        self.draw_all(img,self.minute_chart_region)

        # cv2.imwrite('test.png',img)

