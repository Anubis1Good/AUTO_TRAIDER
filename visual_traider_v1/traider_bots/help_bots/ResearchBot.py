import os
from time import time
import cv2
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.general_v2 import get_candle_mask, get_volume_mask, get_statistic_volume, get_cords_on_mask, get_corners, get_divide_chart, get_xy
from utils.test_utils.test_draws_funcs import draw_trendlines_v2
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
        candle_mask = get_candle_mask(chart)
        volume_mask = get_volume_mask(chart)
        volume_cords = get_cords_on_mask(volume_mask)
        mean_volume,max_volume = get_statistic_volume(volume_cords)
        # print(mean_volume,max_volume)
        mean_volume = change_cords(mean_volume)
        max_volume = change_cords(max_volume)
        cv2.circle(img,mean_volume,1,(250,0,0),3)
        cv2.circle(img,max_volume,1,(200,100,0),3)
        candle_corners = get_corners(candle_mask)
        
        for i in range(candle_corners.shape[0]):
            candle_corners[i] = change_cords(candle_corners[i])
        divide_regions = get_divide_chart(candle_corners)
        for dr in divide_regions:
            cv2.rectangle(img,(dr[0],dr[1]),(dr[2],dr[3]),(200,200,100),2)
        # candle_corners = self._change_coords(candle_corners,region)
        x,y = get_xy(candle_corners)
        draw_trendlines_v2(x,y,img)
        
    def _test(self, img):
        name = f'{self.save_dir_raw}{self.name}_{int(time())}.png'
        cv2.imwrite(name,img)
        # self.draw_all(img,self.day_chart_region)
        # self.draw_all(img,self.hour_chart_region)
        # self.draw_all(img,self.minute_chart_region)
        # name = f'{self.save_dir}{self.name}_{int(time())}.png'
        # cv2.imwrite(name,img)
