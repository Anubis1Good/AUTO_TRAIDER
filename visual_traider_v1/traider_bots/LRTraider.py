# import cv2
from traider_bots.VisualTraider import VisualTraider
from utils.conditions import check_pos, check_req, get_current_level
from utils.traid_utils import click_bl,click_bs,idle
from utils.chart_utils.general import get_last_points_trend
from utils.test_utils.test_traide import test_close,test_open
from utils.utils import change_coords
class LRTraider(VisualTraider):
    def __init__(self, glass_region: tuple, chart_region: tuple) -> None:
        super().__init__(glass_region, chart_region)
        self.Test_send_req = test_open
        self.Test_need_close = test_close
        self.Test_sleep = idle
        self.Send_req = idle
        # self.Send_req = click_bl
        self.Has_req = idle
        self.Has_close = idle
        # self.Need_close = click_bs
        self.Need_close = idle
        self.buff = (self.region_chart[3]-self.region_chart[1])//12
        self.chart_width = chart_region[2] - chart_region[0]
    
    def get_chart(self,img):
            chart = img[
            self.region_chart[1]:self.region_chart[3],
            self.region_chart[0]:int((self.chart_width)*0.99)+self.region_chart[0]]
            return chart
    
    def get_keys(self,chart):
        slope,top_trend,bottom_trend = get_last_points_trend(chart)
        top_trend = change_coords(top_trend,self.region_chart)
        bottom_trend = change_coords(bottom_trend,self.region_chart)
        self.offset = (bottom_trend[1]-top_trend[1])//10
        top_offset  = top_trend[1]+self.offset
        top_stop = top_trend[1]-self.offset*5
        bottom_offset = bottom_trend[1]-self.offset
        bottom_stop = bottom_trend[1]+self.offset*5
        return slope,top_offset,bottom_offset,top_stop,bottom_stop
    
    def run(self, img):
        pos = check_pos(img,self.region_pos)
        req_x, req_y = check_req(img,self.region_glass)
        y_cur_price = get_current_level(img,self.region_chart)
        chart = self.get_chart(img)
        try:
            slope,top_offset,bottom_offset,top_stop,bottom_stop = self.get_keys(chart)
            if pos:
                if req_x > 0:
                    if y_cur_price < top_offset:
                        self.current_state = self.Has_close
                    else:
                        self.current_state = self.Not_idea
                else:
                    if y_cur_price < top_offset:
                        self.current_state = self.Need_close
                    else:
                        self.current_state = self.Not_idea
            else:
                if req_x > 0:
                    if y_cur_price > bottom_offset:
                        self.current_state = self.Has_req
                    else:
                        self.current_state = self.Not_idea
                else:
                    if y_cur_price > bottom_offset and slope < 0.1:
                        self.current_state = self.Send_req
                    else:
                        self.current_state = self.Not_idea

        except Exception as err:
            self.current_state = self.Not_idea
            # print(err)   

        self.current_state(img,self.region_glass)


    def test(self,img):
        y_cur_price = get_current_level(img,self.region_chart)
        chart = self.get_chart(img)
        try:
            slope,top_offset,bottom_offset,top_stop,bottom_stop = self.get_keys(chart)
            success = 0
            if bottom_offset+self.offset*2 > y_cur_price > bottom_offset and slope < 0.05:
                self.current_state = lambda image,name: self.Test_send_req(image,name,'long')
                success = self.current_state(chart,self.name)
                if success == 1:
                    return None
            if y_cur_price < top_offset or y_cur_price > bottom_stop or slope > 0.20:
                self.current_state = lambda image,name: self.Test_need_close(image,name,'long')
                success = self.current_state(chart,self.name)
                if success == 1:
                    return None
            if top_offset-self.offset*2 < y_cur_price < top_offset and slope > 0.10:
                self.current_state = lambda image,name: self.Test_send_req(image,name,'short')
                success = self.current_state(chart,self.name)
                if success == 1:
                    return None
            if y_cur_price > bottom_offset or y_cur_price < top_stop or slope < -0.10:
                self.current_state = lambda image,name: self.Test_need_close(image,name,'short')
                success = self.current_state(chart,self.name)
                if success == 1:
                    return None
            self.current_state = self.Test_sleep


        except Exception as err:
            self.current_state = self.Test_sleep
            print(err)   

        self.current_state(chart,self.name)
