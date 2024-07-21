# import cv2
from traider_bots.archive.VisualTraider import VisualTraider
from utils.conditions import check_pos, check_req, get_current_level
from utils.traid_utils import click_bl,click_bs,idle
from utils.chart_utils.general import get_last_points_trend
from utils.test_utils.test_traide import test_close,test_open
from utils.utils import change_coords
class Begginer3(VisualTraider):
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
        # self.buff = (self.region_chart[3]-self.region_chart[1])//12
        self.chart_width = chart_region[2] - chart_region[0]
        self.chart_height = chart_region[3] - chart_region[1]
        self.sell_border = chart_region[1] + self.chart_height//6
        self.buy_border = chart_region[3] - self.chart_height//6
        self.traider_name = 'Begginer3'
    
    def get_chart(self,img):
            chart = img[
            self.region_chart[1]:self.region_chart[3],
            self.region_chart[0]:int((self.chart_width)*0.99)+self.region_chart[0]]
            return chart
    
    def get_keys(self,chart):
        slope,_,_ = get_last_points_trend(chart)
        return slope
    
    def run(self, img):
        pass


    def test(self,img):
        y_cur_price = get_current_level(img,self.region_chart)
        chart = self.get_chart(img)
        try:
            slope= self.get_keys(chart)
            success = 0
            if y_cur_price > self.buy_border and slope < 0.05:
                self.current_state = lambda image,name: self.Test_send_req(image,name,'long',self.traider_name)
                success = self.current_state(chart,self.name)
                if success == 1:
                    return None
            if y_cur_price < self.sell_border or slope > 0.20:
                self.current_state = lambda image,name: self.Test_need_close(image,name,'long',self.traider_name)
                success = self.current_state(chart,self.name)
                if success == 1:
                    return None
            if self.sell_border > y_cur_price and slope > 0.10:
                self.current_state = lambda image,name: self.Test_send_req(image,name,'short',self.traider_name)
                success = self.current_state(chart,self.name)
                if success == 1:
                    return None
            if y_cur_price > self.buy_border or slope < -0.10:
                self.current_state = lambda image,name: self.Test_need_close(image,name,'short',self.traider_name)
                success = self.current_state(chart,self.name)
                if success == 1:
                    return None
            self.current_state = self.Test_sleep


        except Exception as err:
            self.current_state = self.Test_sleep
            print(err)   

        self.current_state(chart,self.name)
