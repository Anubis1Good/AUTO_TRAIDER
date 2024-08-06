import numpy as np
import cv2
from utils.chart_utils.dtype import HalfBar
from utils.chart_utils.indicators import get_bollinger_bands,get_context
class ProSveT:
    def __init__(self,half_bars: list[HalfBar],smoth_coef:int=30,stop_clear=5) -> None:
        self.half_bars = half_bars
        self.smoth_coef = smoth_coef
        self.stop_clear = stop_clear
        self.mpts = []
        self.vpts = []
        self.vsaipts = []
        self.spreds = []
        for i in range(len(half_bars)):
            mpt = half_bars[i].mpt
            vpt = half_bars[i].vpt
            vsaipt = half_bars[i].vsaipt
            spred = half_bars[i].spred
            self.mpts.append(mpt)
            self.vpts.append(vpt)
            self.spreds.append(spred)
            self.vsaipts.append(vsaipt)
        self.vpts = np.array(self.vpts)
        self.vsaipts = np.array(self.vsaipts)
        self.mpts = np.array(self.mpts)
        self.spreds = np.array(self.spreds)
        self.mean_spred = np.mean(self.spreds)
        self.vs_sma20,self.vs_bbu,_ = get_bollinger_bands(self.vsaipts,1)
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
        creeks = self.clear_exline(creeks,'top')
        ices = self.clear_exline(ices,'bottom')
        creeks = self.filter_exline(creeks,'top',self.mean_spred)
        ices = self.filter_exline(ices,'top',self.mean_spred)
        for creek in creeks:
            point = self.half_bars[creek].mpt if self.half_bars[creek].yl - self.half_bars[creek].ym < self.mean_spred else self.half_bars[creek].pred_hp
            self.sell_zona.append((self.half_bars[creek].hpt,point))
        for ice in ices:
            point = self.half_bars[ice].mpt if self.half_bars[ice].yl - self.half_bars[ice].ym < self.mean_spred else self.half_bars[ice].pred_lp
            self.buy_zona.append((point,self.half_bars[ice].lpt))
        try:
            self.sell_zona.pop()
        except:
            pass
        try:
            self.buy_zona.pop()
        except:
            pass
        self.creeks = np.array(list(creeks.values()))
        self.ices = np.array(list(ices.values()))

            
    def draw_all(self,img):
        cv2.polylines(img,[self.vsaipts],False,(242,78,168),1)
        cv2.polylines(img,[self.vs_sma20],False,(217,142,127),1)
        cv2.polylines(img,[self.vs_bbu],False,(177,217,141),1)
        cv2.polylines(img,[self.raw_creeks],False,(0,0,200),1)
        cv2.polylines(img,[self.raw_ices],False,(0,200,0),1)
        cv2.polylines(img,[self.creeks],False,(0,0,200),2)
        cv2.polylines(img,[self.ices],False,(0,200,0),2)
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
                if keys[i] < len(self.half_bars) - self.stop_clear:
                    for j in range(i,len(keys)):
                        if points[keys[i]][1] > points[keys[j]][1]:
                            break
                    else:
                        new_points[keys[i]] = points[keys[i]]
                else:
                    new_points[keys[i]] = points[keys[i]]
        elif type_clear == 'bottom':
            for i in range(len(keys)):
                if keys[i] < len(self.half_bars) - self.stop_clear:
                    for j in range(i,len(keys)):
                        if points[keys[i]][1] < points[keys[j]][1]:
                            break
                    else:
                        new_points[keys[i]] = points[keys[i]]
                else:
                    new_points[keys[i]] = points[keys[i]]
        return new_points

    def filter_exline(self,points:dict,type_clear:str,spred:int=10):
        keys = list(points.keys())
        new_points = {}
        new_points[keys[0]] = points[keys[0]]
        if type_clear == 'top':
            for i in range(1,len(keys)):
                if abs(points[keys[i]][1] - points[keys[i-1]][1]) > spred:
                    new_points[keys[i]] = points[keys[i]]
        elif type_clear == 'bottom':
            for i in range(1,len(keys)):
                if abs(points[keys[i-1]][1] - points[keys[i]][1]) > spred:
                    new_points[keys[i-1]] = points[keys[i-1]]
        new_points[keys[-1]] = points[keys[-1]]
        return new_points

    