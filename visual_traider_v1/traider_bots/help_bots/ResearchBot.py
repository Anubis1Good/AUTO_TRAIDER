import os
from time import time
import cv2
import numpy as np
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.indicators import get_SMA, get_bollinger_bands
class ResearchBot(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'ResearchBot'
        self.save_dir = './learn_data/draw/'
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        self.save_dir_raw = './learn_data/images/'
        if not os.path.exists(self.save_dir_raw):
            os.makedirs(self.save_dir_raw)
    
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
        for i in range(len(half_bars)):
            hpt,lpt,vpt = half_bars[i].to_img_cords(change_cords)
            mpt = change_cords(half_bars[i].mpt)
            mpts.append(mpt)
            vpts.append(vpt)
            if half_bars[i].is_big_volume(mean_volume[1]): 
                cv2.circle(img,vpt,1,(0,200,0))
                cv2.line(img,hpt,lpt,colors[1],1)
        period = 27
        V_sma = get_SMA(np.array(vpts),period)
        m_sma,bbu,bbd = get_bollinger_bands(np.array(mpts))
        cv2.polylines(img,[V_sma],False,(176,80,10),2)
        cv2.polylines(img,[m_sma],False,(176,180,10),1)
        cv2.polylines(img,[bbu],False,(176,80,90),2)
        cv2.polylines(img,[bbd],False,(176,80,90),2)
        mean_volume = change_cords(mean_volume)
        cv2.circle(img,mean_volume,1,(150,200,70),3)
        points = self._get_points(half_bars)
        for i in range(points.shape[0]):
            points[i] = change_cords(points[i])
        x,y = self._get_xy(points)
        trend,top_trend,bottom_trend,slope = self._get_trend_lines(x,y)
        cv2.polylines(img,[trend],False,(255,255,255),2)
        cv2.polylines(img,[top_trend],False,(255,255,255),2)
        cv2.polylines(img,[bottom_trend],False,(255,255,255),2)
        
    def _test(self, img,price):
        name = f'{self.save_dir_raw}{self.name}_{int(time())}.png'
        cv2.imwrite(name,img)
        # self.draw_all(img,self.day_chart_region)
        # self.draw_all(img,self.hour_chart_region)
        # self.draw_all(img,self.minute_chart_region)
        # name = f'{self.save_dir}{self.name}_{int(time())}.png'
        # cv2.imwrite(name,img)
