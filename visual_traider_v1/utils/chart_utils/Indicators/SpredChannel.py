import numpy as np
import cv2
from utils.chart_utils.dtype import HalfBar
from utils.chart_utils.indicators import get_dynamics
class SpredChannel:
    def __init__(self,half_bars:list[HalfBar],period=14):
        ma = []
        ups1,downs1 = [],[]
        ups2,downs2 = [],[]
        ups3,downs3 = [],[]
        i = period 
        while i <= len(half_bars):
            slice = half_bars[i-period:i]
            slice_ym = []
            slice_spreds = []
            for hb in slice:
                slice_ym.append(hb.ym)
                slice_spreds.append(hb.spred)
            cum_sumy_ma = np.sum(np.array(slice_ym))
            cum_sumy_spred = np.sum(np.array(slice_spreds))
            xs = half_bars[i-1].x
            ma_y = cum_sumy_ma // period
            spreds = cum_sumy_spred // period
            ma.append([xs,ma_y])
            ups1.append([xs,ma_y - spreds])
            downs1.append([xs,ma_y + spreds])
            ups2.append([xs,ma_y - spreds*2])
            downs2.append([xs,ma_y + spreds*2])
            ups3.append([xs,ma_y - spreds*3])
            downs3.append([xs,ma_y + spreds*3])
            i += 1
        
        self.ma = np.array(ma)
        self.ups1 = np.array(ups1)
        self.downs1 = np.array(downs1)
        self.ups2 = np.array(ups2)
        self.downs2 = np.array(downs2)
        self.ups3 = np.array(ups3)
        self.downs3 = np.array(downs3)
        self.dynamics10 = get_dynamics(self.ma)
        self.dynamics50 = get_dynamics(self.ma,50)
        self.dynamics_all = get_dynamics(self.ma,len(self.ma)-1)

    def draw_all(self,chart,color_up=(20,200,10),color_ma=(200,200,0),color_down=(200,0,200),thickness=1):
        cv2.polylines(chart,[self.ma],False,color_ma,thickness)
        cv2.polylines(chart,[self.ups1],False,color_up,thickness)
        cv2.polylines(chart,[self.downs1],False,color_down,thickness)
        cv2.polylines(chart,[self.ups2],False,color_up,thickness)
        cv2.polylines(chart,[self.downs2],False,color_down,thickness)
        cv2.polylines(chart,[self.ups3],False,color_up,thickness)
        cv2.polylines(chart,[self.downs3],False,color_down,thickness)
        cv2.putText(chart,"D10: " +str(self.dynamics10),(0,30),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
        cv2.putText(chart,"D_ALL: " +str(self.dynamics_all),(0,45),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
        cv2.putText(chart,"D50: " +str(self.dynamics50),(0,60),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)