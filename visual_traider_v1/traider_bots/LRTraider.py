import cv2
from traider_bots.VisualTraider import VisualTraider
from utils.conditions import check_pos, check_req, get_current_level
from utils.traid_utils import click_bl,click_bs,idle
from utils.chart_utils.general import get_last_points_trend
from utils.test_utils.test_traide import test_close,test_open
class LRTraider(VisualTraider):
    def __init__(self, glass_region: tuple, chart_region: tuple) -> None:
        super().__init__(glass_region, chart_region)
        # self.Send_req = idle
        self.Send_req = test_open
        # self.Send_req = click_bl
        self.Has_req = idle
        self.Has_close = idle
        # self.Need_close = click_bs
        self.Need_close = test_close
        self.buff = (self.region_chart[3]-self.region_chart[1])//12
        self.chart_width = chart_region[2] - chart_region[0]
    
    def run(self, img):
        pos = check_pos(img,self.region_pos)
        req_x, req_y = check_req(img,self.region_glass)
        y_cur_price = get_current_level(img,self.region_chart)
        chart = img[
            self.region_chart[1]:self.region_chart[3],
            self.region_chart[0]:int((self.chart_width)*0.98)+self.region_chart[0]]
        try:
            slope,top_trend,bottom_trend = get_last_points_trend(chart)
            # if pos:
            #     if req_x > 0:
            #         if y_cur_price < top_trend+self.buff:
            #             self.current_state = self.Has_close
            #         else:
            #             self.current_state = self.Not_idea
            #     else:
            #         if y_cur_price < top_trend+self.buff:
            #             self.current_state = self.Need_close
            #         else:
            #             self.current_state = self.Not_idea
            # else:
            #     if req_x > 0:
            #         if y_cur_price > bottom_trend-self.buff:
            #             self.current_state = self.Has_req
            #         else:
            #             self.current_state = self.Not_idea
            #     else:
            #         if y_cur_price > bottom_trend-self.buff and slope < 0.1:
            #             self.current_state = self.Send_req
            #         else:
            #             self.current_state = self.Not_idea
            # test
            if y_cur_price > bottom_trend-self.buff and slope < 0.1:
                self.current_state = self.Send_req
            elif y_cur_price < top_trend+self.buff:
                self.current_state = self.Need_close
            else:
                self.current_state = self.Has_close
        except:
            # self.current_state = self.Not_idea
            # test
            self.current_state = self.Has_close

        # self.current_state(img,self.region_glass)
        # test
        self.current_state(img,self.name)

        # cv2.imwrite('test.png',chart)
            # cv2.circle(chart, trend,2, (255,0,0),-1)
            # cv2.circle(chart, top_trend,2, (255,0,0),-1)
            # cv2.circle(chart, bottom_trend,2, (255,0,0),-1)
            # cv2.polylines(chart,[trend],False,(255,255,255),2)
            # cv2.polylines(chart,[top_trend],False,(255,255,255),2)
            # cv2.polylines(chart,[bottom_trend],False,(255,255,255),2)