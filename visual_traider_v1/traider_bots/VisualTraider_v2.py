from utils.utils import color_search
from utils.config import ColorsBtnBGR
class VisualTraider_v2():
    def __init__(
            self,
            cluster:tuple,
            dealfeed:tuple,
            glass:tuple,
            day:tuple,
            hour:tuple,
            minute:tuple,
            position:tuple,
            name:str,
            mode:int = 0) -> None:
        self.cluster_region = cluster
        self.dealfeed_region = dealfeed
        self.glass_region = glass
        self.day_chart_region = day
        self.hour_chart_region = hour
        self.minute_chart_region = minute
        self.position_region = position
        self.name = name 
        self.traider_name = 'VisualTraider_v2'
        self.mode = mode

    def __repr__(self) -> str:
        return f'{self.traider_name} - {self.name}'
    
    def _test(self,img):
        print(self,'the _test method is not implemented')

    def _traide(self,img):
        print(self,'the _traide method is not implemented')
    
    def run(self,img):
        if self.mode == 0:
            self._test(img)
        elif self.mode == 1:
            self._traide(img)
        elif self.mode == 2:
            self._traide(img)
            self._test(img)

    def _get_chart(self,img,region):
        chart = img[
        region[1]:region[3],
        region[0]:region[2]]
        return chart
    
    def _get_current_price(self,chart):
        x,y = color_search(chart,ColorsBtnBGR.cur_price_1,reverse=True)
        if y > 0:
            x,y2 = color_search(chart,ColorsBtnBGR.cur_price_1,reverse=False)
            return (x,(y+y2)//2)
        x,y = color_search(chart,ColorsBtnBGR.cur_price_2,reverse=True)
        if y > 0:
            x,y2 = color_search(chart,ColorsBtnBGR.cur_price_2,reverse=False)
            return (x,(y+y2)//2)
        return None,None
    
    def _check_position(self,img) -> int:
        x,y = color_search(img,ColorsBtnBGR.best_bid,self.position_region)
        if x >= 0:
            return 1
        x,y = color_search(img,ColorsBtnBGR.best_ask,self.position_region)
        if x >= 0:
            return -1
        return 0
    
    def _check_req(self,img) ->tuple | bool:
        x,y = color_search(img,ColorsBtnBGR.color_x_shadow,self.glass_region)
        if x>0:
            return x,y
        else:
            x,y = color_search(img,ColorsBtnBGR.color_x,self.glass_region)
            if x > 0:
                return x,y
            else:
                x,y = color_search(img,ColorsBtnBGR.color_x_bb,self.glass_region)
                return x,y
    
    def _change_coords(self,point,region:tuple) -> tuple:
        point = list(point)
        point[0] += region[0]
        point[1] += region[1]
        return tuple(point)

