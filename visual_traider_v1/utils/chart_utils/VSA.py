import numpy as np
import cv2
from utils.chart_utils.dtype import HalfBar,FullBar
from utils.chart_utils.indicators import get_bollinger_bands


class VSA:
    def __init__(self,half_bars: list[HalfBar],step_bb_vsai:int=20) -> None:
        self.full_bars:list[FullBar] = []
        volumes = []
        self.vsaipts = []
        self.min_bar = 1
        self.max_bar = 1
        spreds = []
        for i in range(1,len(half_bars)-1):
            prev_hb = half_bars[i-1]
            next_hb = half_bars[i+1]
            cur_hb = half_bars[i]
            if half_bars[self.max_bar].yh >= cur_hb.yh:
                self.max_bar = i
            if half_bars[self.min_bar].yl <= cur_hb.yl:
                self.min_bar = i
            yo,direction = self._get_open(prev_hb,cur_hb)
            yc,next_direction = self._get_open(cur_hb,next_hb)
            yc = cur_hb.yl if yc > cur_hb.yl and next_direction == -1 else yc
            yc = cur_hb.yh if yc < cur_hb.yh and next_direction == 1 else yc
            direction = 1 if yo > yc else -1
            top_rotate,bottom_rotate = self._check_rotate_point(prev_hb,cur_hb,next_hb)
            bar = FullBar(cur_hb.x,cur_hb.yh,cur_hb.yl,cur_hb.yv,yo,yc,direction,top_rotate,bottom_rotate)
            self.full_bars.append(bar)
            volumes.append(half_bars[i].yv)
            spreds.append(half_bars[i].spred)
            self.vsaipts.append(half_bars[i].vsaipt)
        self.vsaipts = np.array(self.vsaipts)
        spreds = np.array(spreds)
        self.max_vsai = np.min(self.vsaipts[:,1])
        # print(self.max_vsai)
        self.max_spred = np.max(spreds)
        self.mean_spred = np.mean(spreds)
        self.max_volume = np.min(np.array(volumes))
        self.min_volume = np.max(np.array(volumes))
        self.vs_sma20,self.vs_bbu,_ = get_bollinger_bands(self.vsaipts,1,step_bb_vsai)
        for i in range(20,len(self.full_bars)):
            self.full_bars[i].over_v_sma = self.full_bars[i].vsaipt[1] < self.vs_sma20[i-20][1]
            self.full_bars[i].over_vsai = self.full_bars[i].vsaipt[1] < self.vs_bbu[i-20][1]
        self.max_bar -= 1
        self.min_bar -= 1
        self.context = 1 if self.max_bar > self.min_bar else -1
        start = self.max_bar if self.context == 1 else self.min_bar
        self.local_point1 = self._get_local_extremum(self.context,start)
        self.local_point2 = self._get_local_extremum(-self.context,self.local_point1)
        self.local_point3 = self._get_local_extremum(self.context,self.local_point2)
        self.local_point4 = self._get_local_extremum(-self.context,self.local_point3)
        self.full_context = self._get_full_context()
        self.delta = abs(self.full_context[0][1] - self.full_context[1][1])//10
        # self.real_context = self._get_real_context()
        self.formation = self._get_formation()

    def draw_all(self,img):
        for fb in self.full_bars:
            color = (0,250,0) if fb.direction == 1 else (0,0,250)
            color = (250,100,0) if fb.top_rotate else color
            color = (100,100,250) if fb.bottom_rotate else color
            color = (200,200,200) if fb.bottom_rotate and fb.top_rotate else color

            cv2.line(img,fb.hpt,fb.lpt,color,1)
            cv2.circle(img,(fb.x-1,fb.yo),1,color,1)
            cv2.circle(img,(fb.x+1,fb.yc),1,color,1)
            cv2.circle(img,fb.vsaipt,1,(200,100,0),1)
            if fb.over_v_sma:
                cv2.line(img,fb.vsaipt,(fb.x,self.min_volume),(0,200,0),1)
            if fb.over_vsai:
                cv2.line(img,fb.vsaipt,(fb.x,self.min_volume),(140,70,160),1)
            # print(fb.vsai)
        # self.draw_context(img)
        cv2.putText(img,"Formation: " +str(self.formation),(0,20),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
    
    def _get_direction_bar(self,prev_hb,next_hb):
        if prev_hb.yh > next_hb.yh and prev_hb.yl >= next_hb.yl:
            direction = 1
        elif prev_hb.yh <= next_hb.yh and prev_hb.yl < next_hb.yl:
            direction = -1
        else:
            if abs(prev_hb.yh - next_hb.yh) > abs(prev_hb.yl - next_hb.yl):
                direction = 1
            else: 
                direction = -1

        return direction
    
    def _get_open(self,prev_hb,cur_hb):
        direction = self._get_direction_bar(prev_hb,cur_hb)
        if direction == 1:
            yo = prev_hb.yh
            if yo > cur_hb.yl:
                yo = cur_hb.yl
            elif yo < cur_hb.yh:
                yo = cur_hb.yh
        else:
            yo = prev_hb.yl
            if yo < cur_hb.yh:
                yo = cur_hb.yh
            elif yo > cur_hb.yl:
                yo = cur_hb.yl
        return yo,direction
    
    def _check_rotate_point(self,prev_hb:HalfBar,cur_hb:HalfBar,next_hb:HalfBar):
        top_rotate = False
        bottom_rotate = False
        if prev_hb.yh > cur_hb.yh <= next_hb.yh:
            top_rotate = True
        if prev_hb.yl < cur_hb.yl >= next_hb.yl:
            bottom_rotate = True
        return top_rotate,bottom_rotate

    def get_important_bars(self):
        short_bar1,short_bar2,long_bar1,long_bar2,rotate_short,rotate_long = None,None,None,None,None,None
        done = 0
        for i in range(len(self.full_bars)-1,0,-1):
            fb = self.full_bars[i]
            if not short_bar1:
                if fb.over_v_sma and fb.direction == -1:
                    short_bar1 = i
                    done += 1
            if not short_bar2:
                if fb.over_vsai and fb.direction == -1:
                    short_bar2 = i
                    done += 1
            if not long_bar1:
                if fb.over_v_sma and fb.direction == 1:
                    long_bar1 = i
                    done += 1
            if not long_bar2:
                if fb.over_vsai and fb.direction == 1:
                    long_bar2 = i   
                    done += 1            
            if not rotate_long:
                if fb.bottom_rotate:
                    rotate_long = i
                    done += 1
            if not rotate_short:
                if fb.top_rotate:
                    rotate_short = i
                    done += 1
            if done == 6:
                break
        return short_bar1,short_bar2,long_bar1,long_bar2,rotate_short,rotate_long
    
    def get_context_y(self,y):
        for i in range(len(self.full_bars)-1,0,-1):
            fb = self.full_bars[i]
            if fb.y_in_bar(y):
                return fb,i
        return None,None
    
    def check_overlap(self,i,direction):
        overlap = False
        j = 0
        if type(i) == int:
            fb_check = self.full_bars[i]
            for j in range(i+1,len(self.full_bars)):
                fb_cur = self.full_bars[j]
                if direction == 'top':
                    if fb_cur.yl < fb_check.yh > fb_cur.yh:
                        overlap = True
                        break
                if direction == 'bottom':
                    if fb_cur.yl > fb_check.yl < fb_cur.yh:
                        overlap = True
                        break
        else:
            j = -1
        return overlap,j
    
    def check_retest(self,i,direction,i_overlap):
        retest = False
        j = 0
        if type(i) == int:
            fb_check = self.full_bars[i]
            if type(i_overlap) == int:
                for j in range(j+1,len(self.full_bars)):
                    fb_cur = self.full_bars[j]
                    if direction == 'top':
                        if fb_check.ym > fb_cur.yh:
                            retest = True
                            break
                    if direction == 'bottom':
                        if fb_cur.yl > fb_check.ym:
                            retest = True
                            break
        else:
            j = -1
        return retest,j
    
    def get_important_bars_y(self,y):
        short_bar1,short_bar2,long_bar1,long_bar2,rotate_short,rotate_long = None,None,None,None,None,None
        done = 0
        for i in range(len(self.full_bars)-1,0,-1):
            fb = self.full_bars[i]
            # top_overlap,j = self.check_overlap(i,'top')
            # bottom_overlap,j = self.check_overlap(i,'bottom')
            # if not top_overlap:
            if not short_bar1:
                if fb.over_v_sma and fb.direction == -1 and fb.yh < y:
                    short_bar1 = i
                    done += 1
            if not short_bar2:
                if fb.over_vsai and fb.direction == -1 and fb.yh < y:
                    short_bar2 = i
                    done += 1
            # if not bottom_overlap:
            if not long_bar1:
                if fb.over_v_sma and fb.direction == 1 and fb.yl > y:
                    long_bar1 = i
                    done += 1
            if not long_bar2:
                if fb.over_vsai and fb.direction == 1 and fb.yl > y:
                    long_bar2 = i   
                    done += 1            
            if not rotate_long:
                if fb.bottom_rotate and fb.yl > y and i != len(self.full_bars)-1:
                    rotate_long = i
                    done += 1
            if not rotate_short:
                if fb.top_rotate and fb.yh < y and i < len(self.full_bars)-2:
                    rotate_short = i
                    done += 1
            if done == 6:
                break
        return short_bar1,short_bar2,long_bar1,long_bar2,rotate_short,rotate_long
    

    
    def _get_local_extremum(self,direction,start):
        local_point = None
        if start:
            if start < len(self.full_bars)-2:
                local_point = start + 1
                for i in range(local_point,len(self.full_bars)):
                    cur_hb = self.full_bars[i]
                    if direction == 1:
                        if self.full_bars[local_point].yl <= cur_hb.yl:
                            local_point = i
                    if direction == -1:
                        if self.full_bars[local_point].yh >= cur_hb.yh:
                            local_point = i
        return local_point
    
    def _get_full_context(self):
        points = []
        if self.context == 1:
            points.append(self.full_bars[self.min_bar].lpt)
            points.append(self.full_bars[self.max_bar].hpt)
            if self.local_point1:
                points.append(self.full_bars[self.local_point1].lpt)
                if self.local_point2:
                    points.append(self.full_bars[self.local_point2].hpt)
                    if self.local_point3:
                        points.append(self.full_bars[self.local_point3].lpt)
                    if self.local_point4:
                        points.append(self.full_bars[self.local_point4].hpt)
        if self.context == -1:
            points.append(self.full_bars[self.max_bar].hpt)
            points.append(self.full_bars[self.min_bar].lpt)
            if self.local_point1:
                points.append(self.full_bars[self.local_point1].hpt)
                if self.local_point2:
                    points.append(self.full_bars[self.local_point2].lpt)
                    if self.local_point3:
                        points.append(self.full_bars[self.local_point3].hpt)
                    if self.local_point4:
                        points.append(self.full_bars[self.local_point4].lpt)
        return np.array(points)
    
    def _get_real_context(self):
        real_context = self.context
        if len(self.full_context) > 3:

            if abs(self.full_context[0][1] - self.full_context[2][1] ) < self.delta:
                if self.context == 1:
                    real_context -= 0.5
                else:
                    real_context += 0.5
            if abs(self.full_context[1][1] - self.full_context[3][1] ) < self.delta:
                if self.context == 1:
                    real_context -= 0.5
                else:
                    real_context += 0.5
        return real_context
    
    def _get_formation(self):
        
        if len(self.full_context) > 4:
            self.help_delta = abs(self.full_context[1][1] - self.full_context[2][1])//8
            if self.context == 1:
                if   abs(self.full_context[0][1] - self.full_context[2][1] ) <self.delta:
                    return 'range'
                if abs(self.full_context[1][1] - self.full_context[3][1] ) <self.delta:
                    if abs(self.full_context[4][1] - self.full_context[2][1] ) < self.help_delta:
                        return 'long_flag'
            if self.context == -1:
                if abs(self.full_context[0][1] - self.full_context[2][1] ) <self.delta:
                    return 'range'
                if abs(self.full_context[1][1] - self.full_context[3][1] ) <self.delta:
                    if abs(self.full_context[4][1] - self.full_context[2][1] ) < self.help_delta:
                        return 'short_flag'
            if abs(self.full_context[0][1] - self.full_context[1][1] ) <self.delta:
                if abs(self.full_context[0][1] - self.full_context[4][1] ) <self.delta: return 'base_triangle'
            if len(self.full_context) > 5:
                if abs(self.full_context[1][1] - self.full_context[3][1] ) <self.delta:
                    if abs(self.full_context[1][1] - self.full_context[5][1] ) < self.help_delta: 
                        return 'preload_triangle'
                local_delta = abs(self.full_context[2][1] - self.full_context[3][1])//7
                if abs(self.full_context[2][1] - self.full_context[4][1] ) < local_delta:
                    if abs(self.full_context[3][1] - self.full_context[5][1] ) < local_delta:
                        return 'local_range'
        if self.context == 1:
            if len(self.full_context) >= 3:
                if abs(self.full_context[1][1] - self.full_context[2][1] ) <self.delta*2:
                    return 'strong_long'
            if len(self.full_context) == 2:
                return 'strong_long'
            return 'long'
        if self.context == -1:
            if len(self.full_context) >= 3:
                if abs(self.full_context[1][1] - self.full_context[2][1] ) <self.delta*2:
                    return 'strong_short'
            if len(self.full_context) == 2:
                return 'strong_short'
            return 'short'
                
    def draw_context(self,img):
        cv2.polylines(img,[self.full_context],False,(90,210,90),2)

                

