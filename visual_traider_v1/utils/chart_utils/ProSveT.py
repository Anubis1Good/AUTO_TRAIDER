import numpy as np
import cv2
from utils.chart_utils.dtype import HalfBar
from utils.chart_utils.indicators import get_bollinger_bands,get_context
class ProSveT:
    def __init__(self,half_bars: list[HalfBar],smoth_coef:int=30) -> None:
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
        self.sell_zona,self.buy_zona = [],[]
        self.dynamics = []
        creeks = {}
        ices = {}
        for i in range(1,len(half_bars)-1):
            if half_bars[i-1].yh > half_bars[i].yh <= half_bars[i+1].yh:
                creeks[i] = half_bars[i].hpt
            if half_bars[i-1].yl < half_bars[i].yl >= half_bars[i+1].yl:
                ices[i] = half_bars[i].lpt
        self.dynamics = np.array(self.dynamics)
        self.raw_creeks = np.array(list(creeks.values()))
        self.raw_ices = np.array(list(ices.values()))
        while len(creeks) > smoth_coef:
            creeks = self.smooth_exline(creeks,'top')
        while len(ices) > smoth_coef:
            ices = self.smooth_exline(ices,'bottom')
        creeks = self.clear_exline(creeks,'top')
        ices = self.clear_exline(ices,'bottom')
        for creek in creeks:
            point = self.half_bars[creek].lpt if self.half_bars[creek].yl - self.half_bars[creek].ym < self.mean_spred else self.half_bars[creek].pred_hp
            self.sell_zona.append((self.half_bars[creek].hpt,point))
        for ice in ices:
            point = self.half_bars[ice].hpt if self.half_bars[ice].yl - self.half_bars[ice].ym < self.mean_spred else self.half_bars[ice].pred_lp
            self.buy_zona.append((point,self.half_bars[ice].lpt))
        self.sell_zona.pop()
        self.buy_zona.pop()
        self.creeks = np.array(list(creeks.values()))
        self.ices = np.array(list(ices.values()))

            
    def draw_all(self,img):
        cv2.polylines(img,[self.vpts],False,(242,78,168),1)
        cv2.polylines(img,[self.v_sma20],False,(217,142,127),1)
        cv2.polylines(img,[self.v_bbu],False,(177,217,141),1)
        cv2.polylines(img,[self.raw_creeks],False,(0,0,200),1)
        cv2.polylines(img,[self.raw_ices],False,(0,200,0),1)
        for zona in self.sell_zona:
            cv2.rectangle(img,zona[0],(self.half_bars[-1].x,zona[1][1]),(139,71,219),2)
        for zona in  self.buy_zona:
            cv2.rectangle(img,zona[0],(self.half_bars[-1].x,zona[1][1]),(71,219,195),2)


    def smooth_exline(self,points:dict,type_smooth):
        keys = list(points.keys())
        new_points ={keys[0]:points[keys[0]]}
        if type_smooth == 'top':
            for i in range(1,len(points)-1):
                if points[keys[i-1]][1] >= points[keys[i]][1] <= points[keys[i+1]][1]:
                    new_points[keys[i]] = points[keys[i]]
        elif type_smooth == 'bottom':
            for i in range(1,len(points)-1):
                if points[keys[i-1]][1] <= points[keys[i]][1] >= points[keys[i+1]][1]:
                    new_points[keys[i]] = points[keys[i]]
        new_points[keys[-1]] = points[keys[-1]]
        return new_points
    
    def clear_exline(self,points:dict,type_clear):
        keys = list(points.keys())
        new_points = {}
        if type_clear == 'top':
            for i in range(len(keys)):
                for j in range(i,len(keys)):
                    if points[keys[i]][1] > points[keys[j]][1]:
                        break
                else:
                    new_points[keys[i]] = points[keys[i]]
        elif type_clear == 'bottom':
            for i in range(len(keys)):
                for j in range(i,len(keys)):
                    if points[keys[i]][1] < points[keys[j]][1]:
                        break
                else:
                    new_points[keys[i]] = points[keys[i]]
        return new_points
