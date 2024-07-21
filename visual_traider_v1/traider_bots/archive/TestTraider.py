import cv2
import numpy as np
from traider_bots.archive.VisualTraider import VisualTraider
from utils.chart_utils.general import get_chart_point, get_trend_lines


class TestTraider(VisualTraider):
    def __init__(self, glass_region: tuple, chart_region: tuple, name: str = 'none') -> None:
        super().__init__(glass_region, chart_region, name)

    def run(self,img):         
        self.current_state(img,self.region_glass)

    def test(self,img):
        chart = self.get_chart(img)
        tops,bottoms = get_chart_point(chart)
        slope,top_trend,bottom_trend = get_trend_lines(chart)
        point = (np.average(tops[:,0],axis=0).astype(np.int32),np.average(tops[:,1],axis=0).astype(np.int32))
        point_m = (np.quantile(tops[:,0],0.2,axis=0).astype(np.int32),np.quantile(tops[:,1],0.2,axis=0).astype(np.int32))
        cv2.polylines(chart,[tops],False,(255,0,0),2)
        cv2.polylines(chart,[bottoms],False,(255,255,0),2)
        cv2.polylines(chart,[top_trend],False,(255,0,255),2)
        cv2.polylines(chart,[bottom_trend],False,(255,0,255),2)
        cv2.circle(chart,point,1,(0,0,255),3)
        cv2.circle(chart,point_m,1,(200,10,200),3)
        point = (np.average(bottoms[:,0],axis=0).astype(np.int32),np.average(bottoms[:,1],axis=0).astype(np.int32))
        point_m = (np.quantile(bottoms[:,0],0.8,axis=0).astype(np.int32),np.quantile(bottoms[:,1],0.8,axis=0).astype(np.int32))
        cv2.circle(chart,point,1,(0,255,255),3)
        cv2.circle(chart,point_m,1,(50,200,200),3)
        cv2.imwrite(f'test{self.name}.png',chart)
        print(self.name)
    
    def get_chart(self,img):
        chart = img[
        self.region_chart[1]:self.region_chart[3],
        self.region_chart[0]:self.region_chart[2]]
        return chart
