import traceback
import os
from time import time
import cv2
import numpy as np
import numpy.typing as npt
import pyautogui as pag
import pydirectinput as pdi
from scipy import stats
from utils.config import ColorsBtnBGR
from utils.chart_utils.dtype import HalfBar
from utils.config import TemplateCandle
from utils.test_utils.test_traide import test_open,test_close
from tas.BaseTA import BaseTA

class VisualTraider_v3():
    def __init__(
            self,
            cluster:tuple,
            dealfeed:tuple,
            glass:tuple,
            chart1:tuple,
            chart2:tuple,
            chart3:tuple,
            position:tuple,
            name:str,
            mode:int = 0,
            fast_close:bool = False) -> None:
        self.cluster_region = cluster
        self.dealfeed_region = dealfeed
        self.glass_region = glass
        self.chart_region = chart3
        self.chart_region1 = chart1
        self.chart_region2 = chart2
        self.position_region = position
        self.name = name 
        self.traider_name = 'VisualTraider_v3'
        self.mode = mode
        self.TA = BaseTA(self)
        self.fast_close = fast_close
        self.have_pos_l = None
        self.have_pos_s = None
        self.free_stop_l = None
        self.free_stop_s = None
        self.stop_long = 10000
        self.stop_short = -1
        self.take_short = 10000
        self.take_long = -1
        self.bbu_attached = False
        self.bbd_attached = False

    def __repr__(self) -> str:
        return f'{self.traider_name} - {self.name}'
    
    # work function
    def _test(self, img,price):
        action,keys = self.TA(img)
        res1_l,res2_l = 0,0
        res1_s,res2_s = 0,0
        if action == 'long':
            res1_s = self._test_send_close(img,'short',price=price)
            res2_l = self._test_send_open(img,'long',price=price) 
        if action == 'close_long':
            res1_l = self._test_send_close(img,'long',price=price)
        if action == 'short':
            res1_l = self._test_send_close(img,'long',price=price)
            res2_s = self._test_send_open(img,'short',price=price)
        if action == 'close_short':
            res1_s = self._test_send_close(img,'short',price=price)
        if res1_s == 1 and res2_l == 0:
            self.have_pos_s = False
            self.free_stop_s = True
        if res1_l == 1 and res2_s == 0:
            self.have_pos_l = False
            self.free_stop_l = True
        if res2_l == 1:
            self.have_pos_l = True
            self.have_pos_s = False
            self.free_stop_l = False
            self.free_stop_s = True
        if res2_s == 1:
            self.have_pos_s = True
            self.have_pos_l = False
            self.free_stop_s = False
            self.free_stop_l = True
        self.write_logs(keys,action)

    def _traide(self, img):
        pos = self._check_position(img)
        if pos == 0:
            self.have_pos_l = False
            self.have_pos_s = False
            self.free_stop_l = True
            self.free_stop_s = True
        if pos == 1:
            self.have_pos_l = True
            self.have_pos_s = False
            self.free_stop_l = False
            self.free_stop_s = True
        if pos == -1:
            self.have_pos_l = False
            self.have_pos_s = True
            self.free_stop_l = True
            self.free_stop_s = False
        action,keys = self.ТА(self,img)
        if action:
            if action == 'long':
                if pos == -1:
                    self.close_short = True
                    self._reverse_pos(img,'long')
                if pos == 0:
                    self._send_open('long')
            if action == 'close_long':
                if pos == 1:
                    self.close_long = True
                    self._send_close(img,'long')
            if action == 'short':
                if pos == 1:
                    self.close_long = True
                    self._reverse_pos(img,'short')
                if pos == 0:
                    self._send_open('short')
            if action == 'close_short':
                if pos == -1:
                    self.close_short = True
                    self._send_close(img,'short')
        elif self.close_long:
            if pos == 1:
                self._send_close(img,'long')
            else:
                self.close_long = False
        elif self.close_short:
            if pos == -1:
                self._send_close(img,'short')
            else:
                self.close_long = False
        else:
            self._reset_req()

    
    def run(self,img,price=0.0):
        copy_img = img.copy()
        try:
            if self.mode == 0:
                self._test(copy_img,price)
            elif self.mode == 1:
                self._traide(copy_img)
            elif self.mode == 2:
                self._traide(copy_img)
                self._test(copy_img,price)
        except Exception as err:
            traceback.print_exc()
        return copy_img

    # terminal_function
    def _check_position(self,img) -> int:
        x,y = self._color_search(img,ColorsBtnBGR.best_bid,self.position_region)
        if x >= 0:
            return 1
        x,y = self._color_search(img,ColorsBtnBGR.best_ask,self.position_region)
        if x >= 0:
            return -1
        return 0
    
    def _check_req(self,img) ->tuple | bool:
        x,y = self._color_search(img,ColorsBtnBGR.color_x_shadow,self.glass_region)
        if x>0:
            return x,y
        else:
            x,y = self._color_search(img,ColorsBtnBGR.color_x,self.glass_region)
            if x > 0:
                return x,y
            else:
                x,y = self._color_search(img,ColorsBtnBGR.color_x_bb,self.glass_region)
                return x,y
            
    
    # trade_function
    def _send_open(self,direction):
        pag.moveTo(self.glass_region[0]+11,self.glass_region[1]+11)
        pdi.press('f')
        if direction == 'long':
            button = 'a'
        elif direction == 'short':
            button = 's'
        else:
            button = 'f'
        pdi.press(button)

    def _send_close(self,img,direction):
        if self.fast_close:
            rev_direction = 'long' if direction == 'short' else 'short'
            self._send_open(rev_direction)
        else:
            if direction == 'long':
                x,y = self._color_search(img, ColorsBtnBGR.best_ask,self.glass_region,reverse=True)
                if x < 0:
                    x,y = self._color_search(img, ColorsBtnBGR.ask,self.glass_region,reverse=True)
                x -= 50
                y -= 5
                button = 'right'
            elif direction == 'short':
                x,y = self._color_search(img, ColorsBtnBGR.best_bid,self.glass_region,reverse=False)
                if x < 0:
                    x,y = self._color_search(img, ColorsBtnBGR.bid,self.glass_region,reverse=False)
                x += 10
                y += 5
                button = 'left'
            else:
                return None
            pag.moveTo(x,y)
            pdi.press('f')
            pdi.keyDown('altleft')
            pag.click(x, y,button=button)
            pdi.keyUp('altleft')
    
    def _reverse_pos(self,img,direction):
        if direction == 'long':
            button = 'a'
            x,y = self._color_search(img, ColorsBtnBGR.best_bid,self.glass_region,reverse=False)
            if x < 0:
                x,y = self._color_search(img, ColorsBtnBGR.bid,self.glass_region,reverse=False)
            x += 10
            y += 5
            button_m = 'left'
        elif direction == 'short':
            button = 's'
            x,y = self._color_search(img, ColorsBtnBGR.best_ask,self.glass_region,reverse=True)
            if x < 0:
                x,y = self._color_search(img, ColorsBtnBGR.ask,self.glass_region,reverse=True)
            x -= 50
            y -= 5
            button_m = 'right'
        else:
            button = 'f'
            return None
        pag.moveTo(x,y)
        pdi.press('f')
        pdi.press(button)
        pdi.keyDown('altleft')
        pag.click(x, y,button=button_m)
        pdi.keyUp('altleft')

    def _reset_req(self):
        pag.moveTo(self.glass_region[0]+11,self.glass_region[1]+11)
        pdi.press('f')
    # test trade_function

    def _test_send_open(self,img,direction,draw=lambda img:img,price=0.0):
        return test_open(img,self.name,direction,self.traider_name,draw,price)

    def _test_send_close(self,img,direction,draw=lambda img:img,price=0.0):
        return test_close(img,self.name,direction,self.traider_name,draw,price)

    def _draw(self,img,keys,region):
        pass

    # chart_function
    def _get_chart(self,img,region):
        chart = img[
        region[1]:region[3],
        region[0]:region[2]]
        return chart
    
    def _get_current_price(self,chart):
        x,y = self._color_search(chart,ColorsBtnBGR.cur_price_1,reverse=True)
        if y > 0:
            x,y2 = self._color_search(chart,ColorsBtnBGR.cur_price_1,reverse=False)
            return (x,(y+y2)//2)
        x,y = self._color_search(chart,ColorsBtnBGR.cur_price_2,reverse=True)
        if y > 0:
            x,y2 = self._color_search(chart,ColorsBtnBGR.cur_price_2,reverse=False)
            return (x,(y+y2)//2)
        return None,None    
    
    def _get_mask(self,chart:npt.ArrayLike,color) -> npt.ArrayLike:
        mask = cv2.inRange(chart,color,color)
        return mask
    
    def _get_candle_mask(self,chart:npt.ArrayLike) -> npt.ArrayLike:
        mask1 = self._get_mask(chart,ColorsBtnBGR.candle_color_1)
        mask2 = self._get_mask(chart,ColorsBtnBGR.candle_color_2)
        mask = cv2.add(mask1,mask2)
        kernel = np.ones((2, 1), np.uint8) 
        mask = cv2.erode(mask,kernel)
        return mask

    def _get_volume_mask(self,chart:npt.ArrayLike) -> npt.ArrayLike:
        mask1 = self._get_mask(chart,ColorsBtnBGR.volume_color_1)
        mask2 = self._get_mask(chart,ColorsBtnBGR.volume_color_2)
        mask = cv2.add(mask1,mask2)
        return mask
    
    def _get_cords_on_mask(self,mask:npt.ArrayLike) -> npt.NDArray:
        cords = np.argwhere(mask == 255)
        return cords
    
    def _get_half_bars(
            self,
            candle_mask: npt.ArrayLike,
            candle_cords: npt.NDArray, 
            volume_cords: npt.NDArray
            ) -> list[HalfBar]: 
        res_top = cv2.matchTemplate(candle_mask,TemplateCandle.candle_top,cv2.TM_CCOEFF_NORMED)
        res_top = np.argwhere(res_top >= 0.9)
        res_top = res_top[res_top[:, 1].argsort()]
        half_bars:list[HalfBar] = []
        for i in range(res_top.shape[0]):
            res_top[i] = (res_top[i][0],res_top[i][1]+1)
            point_b = candle_cords[np.where(candle_cords[:,1] == res_top[i][1])]
            point_v = volume_cords[np.where(volume_cords[:,1] == res_top[i][1])]
            y_b = point_b[:,0].max()
            y_v = point_v[:,0].min()
            half_bars.append(HalfBar(res_top[i][1],res_top[i][0],y_b,y_v))
        return np.array(half_bars)
    
    def _get_mean(self,cords:npt.NDArray):
        mean_val = (10,int(np.mean(cords,axis=0)[0]))
        return mean_val
    
    def _get_limit(self,cords:npt.NDArray):
        max_val = (10,np.min(cords[:,:1]))
        min_val = (10,np.max(cords[:,:1]))
        return max_val,min_val
    
    def _get_xy(self,points:npt.NDArray) -> npt.NDArray:
        x = points[:,0]
        y = points[:,1]
        return x,y
    
    def _get_points(self,half_bars:list[HalfBar]) -> npt.NDArray:
        points = []
        for hb in half_bars:
            points.append(hb.hpt)
            points.append(hb.lpt)
        return np.array(points)

    def _get_trend_lines(self,x,y):
        std_y = np.std(y)
        slope,intercept = self._get_linear_regress(x,y)
        middle_line = list(map(lambda x:self._get_points_linear_reg(x,slope,intercept,0), x))
        top_line = list(map(lambda x:self._get_points_linear_reg(x,slope,intercept,-std_y), x))
        bottom_line = list(map(lambda x:self._get_points_linear_reg(x,slope,intercept,std_y), x))
        trend = np.column_stack([x, middle_line])
        top_trend = np.column_stack([x, top_line])
        bottom_trend = np.column_stack([x, bottom_line])
        return trend,top_trend,bottom_trend,slope
    
        # help function
    def _change_coords(self,point,region:tuple) -> tuple:
        point = list(point)
        point[0] += region[0]
        point[1] += region[1]
        return tuple(point)
    
    def _color_search(self,img:npt.ArrayLike,color:tuple[int],region:tuple[int]=(None,None,None,None),reverse:bool=False):
        try:
            result = np.argwhere(
                (img[region[1]:region[3],region[0]:region[2],0] == color[0])& 
                (img[region[1]:region[3],region[0]:region[2],1] == color[1])& 
                (img[region[1]:region[3],region[0]:region[2],2] == color[2])
            )
            y = -1 if reverse else 0
            if region[0]:
                return result[y,1]+region[0], result[y,0]+region[1]
            return result[y,1],result[y,0]

        except Exception:
            # traceback.print_exc()
            return -1,-1
    
    # ml function
    def _get_linear_regress(self,x,y):
        slope, intercept, r, p, std_err = stats.linregress(x, y)
        return round(slope,4),intercept

    def _get_points_linear_reg(self,x,slope,intercept,offset=0):
        return int(slope * x + intercept+offset)


    # debug function
    def write_logs(self,keys,action):
        file_name = f'./logs/{self.traider_name}{self.name}.txt'
        log = f'{self.name} - {time()} - {action}: state: {vars(keys)}\n'
        if not os.path.exists(file_name):
            with open(file_name, 'w') as f:
                f.write(log)
        else:
            with open(file_name, 'a') as f:
                f.write(log)