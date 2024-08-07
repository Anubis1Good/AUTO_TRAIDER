import cv2
import numpy as np
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.indicators import get_SMA, get_bollinger_bands,get_fractals, get_context
from utils.config import ColorsBtnBGR
from  utils.chart_utils.ProSveT import ProSveT
from  utils.chart_utils.VSA import VSA
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
        pst = ProSveT(half_bars)
        # pst.draw_all(chart)
        vsa = VSA(half_bars)
        # vsa.draw_all(chart)
        short_bar1,short_bar2,long_bar1,long_bar2,rotate_short,rotate_long = vsa.get_important_bars_y(cur_price[1])
        cur_bar,_ = vsa.get_context_y(cur_price[1])
        sma20,bbu,bbd = get_bollinger_bands(np.array(pst.mpts))
        sma40,bbu_b,bbd_b = get_bollinger_bands(np.array(pst.mpts),k=1.8,step=120)
        print(vsa.context)
        print(vsa.formation)
        if short_bar1:
            cv2.line(chart,vsa.full_bars[short_bar1].hpt,vsa.full_bars[short_bar1].lpt,(200,0,250))
        if short_bar2:
            cv2.polylines(chart,[vsa.full_bars[short_bar2].draw_line],False,(200,0,250),2)
        if long_bar1:
            cv2.polylines(chart,[vsa.full_bars[long_bar1].draw_line],False,(50,250,150))
        if long_bar2:
            cv2.polylines(chart,[vsa.full_bars[long_bar2].draw_line],False,(50,250,150),2)
        if cur_bar:
            cv2.polylines(chart,[cur_bar.draw_line],False,(10,250,250),2)
        if rotate_long:
            cv2.circle(chart,vsa.full_bars[rotate_long].lpt,1,(0,200,0))
        if rotate_short:
            cv2.circle(chart,vsa.full_bars[rotate_short].hpt,1,(200,100,200))
        cv2.line(chart,vsa.full_bars[vsa.max_bar].hpt, (vsa.full_bars[-1].x,vsa.full_bars[vsa.max_bar].yh),(30,119,93))
        cv2.line(chart,vsa.full_bars[vsa.min_bar].lpt, (vsa.full_bars[-1].x,vsa.full_bars[vsa.min_bar].yl),(130,19,193))
        vsa.draw_context(chart)
        # cv2.polylines(chart,[sma20],False,(200,0,0),1)
        # cv2.polylines(chart,[bbu],False,(200,200,0),1)
        # cv2.polylines(chart,[bbd],False,(200,0,200),1)
        # cv2.polylines(chart,[sma40],False,(100,0,0),2)
        # cv2.polylines(chart,[bbu_b],False,(100,200,0),2)
        # cv2.polylines(chart,[bbd_b],False,(100,0,200),2)
        buffer = chart.shape[0]//4
        end = chart.shape[1]-10
        top_line = 0 + buffer
        bottom_line = chart.shape[0] - buffer
        # cv2.line(chart,(0,top_line),(end,top_line),(100,50,200),2)
        # cv2.line(chart,(0,bottom_line),(end,bottom_line),(100,250,20),2)
        # print(chart.shape)
        # img[region[1]:region[3],region[0]:region[1],:] = chart


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

