from traider_bots.archive.VisualTraider import VisualTraider
from utils.traid_utils import click_bl, idle, click_bs
from utils.conditions import check_pos, check_req, check_graphic_level

class Begginer2(VisualTraider):
    def __init__(self, glass_region: tuple, chart_region: tuple) -> None:
        super().__init__(glass_region, chart_region)
        self.Send_req = click_bl
        self.Has_req = idle
        self.Has_close = idle
        self.Need_close = click_bs
    
    def run(self,img):
        pos = check_pos(img,self.region_pos)
        x,y = check_req(img,self.region_glass)
        graphic_level = check_graphic_level(img,self.region_chart)
        if pos:
            if graphic_level == 'sell':
                if x > 0:
                    self.current_state = self.Has_close
                else: 
                    self.current_state = self.Need_close
            else:
                self.current_state = self.Not_idea
        else:
            if graphic_level == 'buy':
                if x > 0:
                    self.current_state = self.Has_req
                else:
                    self.current_state = self.Send_req
            else:
                self.current_state = self.Not_idea   
  
        self.current_state(img,self.region_glass)
