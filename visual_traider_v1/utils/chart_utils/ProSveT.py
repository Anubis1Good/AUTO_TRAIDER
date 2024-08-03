import numpy as np
import cv2
from utils.chart_utils.dtype import HalfBar
from utils.chart_utils.indicators import get_bollinger_bands,get_context
class ProSveT:
    def __init__(self,half_bars: list[HalfBar],smoth_coef:int=20) -> None:
        self.half_bars = half_bars
        self.mpts = []
        self.vpts = []
        self.spreds = []
        for i in range(len(half_bars)):
            mpt = half_bars[i].mpt
            vpt = half_bars[i].vpt
            spred = half_bars[i].spred
            self.mpts.append(mpt)
            self.vpts.append(vpt)
            self.spreds.append(spred)
        self.vpts = np.array(self.vpts)
        self.mpts = np.array(self.mpts)
        self.spreds = np.array(self.spreds)
        self.mean_spred = np.mean(self.spreds)
        self.v_sma20,self.v_bbu,_ = get_bollinger_bands(self.vpts,1)
        max_hb,min_hb,local_hb,direction,max_hb_i,min_hb_i = get_context(self.half_bars)
        self.zona1,self.zona2 = [],[]
        self.dynamics = []
        start = min(max_hb_i,min_hb_i)
        last_rotate = 0
        creeks = []
        ices = []
        for i in range(start,len(half_bars)-1):
            if i < 20:
                if half_bars[i].yv < self.v_sma20[0][1]:
                    self.zona1.append((half_bars[i].hpt,half_bars[i].lpt,i))
                if half_bars[i].yv < self.v_bbu[0][1]:
                    self.zona2.append((half_bars[i].hpt,half_bars[i].lpt,i))
            else:
                if half_bars[i].yv < self.v_sma20[i-20][1]:
                    self.zona1.append((half_bars[i].hpt,half_bars[i].lpt,i))
                if half_bars[i].yv < self.v_bbu[i-20][1]:
                    self.zona2.append((half_bars[i].hpt,half_bars[i].lpt,i))
            if last_rotate ==  1:
                if half_bars[i-1].yh >= half_bars[i].yh <= half_bars[i+1].yh:
                    self.dynamics.append(half_bars[i].hpt)
                    last_rotate = -1
            elif last_rotate == -1:
                if half_bars[i-1].yl <= half_bars[i].yl >= half_bars[i+1].yl:
                    self.dynamics.append(half_bars[i].lpt)
                    last_rotate = 1
            else:
                if half_bars[i-1].yh >= half_bars[i].yh <= half_bars[i+1].yh:
                    self.dynamics.append(half_bars[i].hpt)
                    last_rotate = -1
                if half_bars[i-1].yl <= half_bars[i].yl >= half_bars[i+1].yl:
                    self.dynamics.append(half_bars[i].lpt)
                    last_rotate = 1
            if half_bars[i-1].yh >= half_bars[i].yh <= half_bars[i+1].yh:
                creeks.append(half_bars[i].hpt)
            if half_bars[i-1].yl <= half_bars[i].yl >= half_bars[i+1].yl:
                ices.append(half_bars[i].lpt)
        self.dynamics = np.array(self.dynamics)
        while len(creeks) > smoth_coef:
            creeks = self.smooth_exline(creeks,'top')
        while len(ices) > smoth_coef:
            ices = self.smooth_exline(ices,'bottom')
        self.creeks = np.array(creeks)
        self.ices = np.array(ices)

            
    def draw_all(self,img):
        cv2.polylines(img,[self.vpts],False,(242,78,168),1)
        cv2.polylines(img,[self.v_sma20],False,(217,142,127),1)
        cv2.polylines(img,[self.v_bbu],False,(177,217,141),1)
        cv2.polylines(img,[self.creeks],False,(0,0,200),1)
        cv2.polylines(img,[self.ices],False,(0,200,0),1)
        # cv2.polylines(img,[self.dynamics],False,(100,200,100),2)
        for zona in self.zona1:
            cv2.line(img,zona[0],zona[1],(139,71,219),2)
        for zona in  self.zona2:
            cv2.line(img,zona[0],zona[1],(71,219,195),2)
        # for hb in self.half_bars:
        #     if hb.spred > self.mean_spred:
        #         cv2.circle(img,hb.hpt,1,(200,200,0),2)
        #         cv2.circle(img,hb.lpt,1,(200,200,0),2)

    def smooth_exline(self,points,type_smooth):
        new_points = [points[0]]
        if type_smooth == 'top':
            for i in range(1,len(points)-1):
                if points[i-1][1] >= points[i][1] <= points[i+1][1]:
                    new_points.append(points[i])
        elif type_smooth == 'bottom':
            for i in range(1,len(points)-1):
                if points[i-1][1] <= points[i][1] >= points[i+1][1]:
                    new_points.append(points[i])
        new_points.append(points[-1])
        return new_points
