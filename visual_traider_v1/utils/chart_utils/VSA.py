import numpy as np
import cv2
from utils.chart_utils.dtype import HalfBar,FullBar


class VSA:
    def __init__(self,half_bars: list[HalfBar]) -> None:
        pass
        self.full_bars:list[FullBar] = []
        volumes = []
        for i in range(1,len(half_bars)-1):
            prev_hb = half_bars[i-1]
            next_hb = half_bars[i+1]
            cur_hb = half_bars[i]
            yo,direction = self._get_open(prev_hb,cur_hb)
            yc,next_direction = self._get_open(cur_hb,next_hb)
            yc = cur_hb.yl if yc > cur_hb.yl and next_direction == -1 else yc
            yc = cur_hb.yh if yc < cur_hb.yh and next_direction == 1 else yc
            direction = 1 if yo > yc else -1
            bar = FullBar(cur_hb.x,cur_hb.yh,cur_hb.yl,cur_hb.yv,yo,yc,direction)
            self.full_bars.append(bar)
            volumes.append(half_bars[i].yv)
        self.max_volume = np.min(np.array(volumes))
    
    def draw_all(self,img):
        for fb in self.full_bars:
            color = (0,200,0) if fb.direction == 1 else (0,0,200)
            cv2.line(img,fb.hpt,fb.lpt,color,1)
            cv2.circle(img,(fb.x-1,fb.yo),1,color,1)
            cv2.circle(img,(fb.x+1,fb.yc),1,color,1)
            cv2.circle(img,fb.vsaipt,1,(200,0,0),1)
            # print(fb.vsai)
    
    def _get_direction_bar(self,prev_hb,next_hb):
        if prev_hb.yh > next_hb.yh and prev_hb.yl >= next_hb.yl:
            direction = 1
        elif prev_hb.yh <= next_hb.yh and prev_hb.yl < next_hb.yl:
            direction = -1
        else:
            if abs(prev_hb.yh - next_hb.yh) < abs(prev_hb.yl - next_hb.yl):
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
