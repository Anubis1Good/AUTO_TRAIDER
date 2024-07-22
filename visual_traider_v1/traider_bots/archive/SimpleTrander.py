import cv2
from traider_bots.archive.VisualTraider import VisualTraider
from utils.conditions import check_pos, check_req, get_current_level
from utils.traid_utils import click_bl,click_bs,idle
from utils.chart_utils.archive.general import get_formation, get_main_points, get_mean_y
class SimpleTraider(VisualTraider):
    def __init__(self, glass_region: tuple, chart_region: tuple) -> None:
        super().__init__(glass_region, chart_region)
        self.Send_req = click_bl
        self.Has_req = idle
        self.Has_close = idle
        self.Need_close = click_bs
        self.buff = (self.region_chart[3]-self.region_chart[1])//12
        self.chart_width = chart_region[2] - chart_region[0]
    
    def run(self, img):
        pos = check_pos(img,self.region_pos)
        x,y = check_req(img,self.region_glass)
        # TODO
        y = get_current_level(img,self.region_chart)
        chart = img[self.region_chart[1]:self.region_chart[3],self.region_chart[0]:int((self.chart_width)*0.9)+self.region_chart[0]]
        try:
            main_points = get_main_points(chart)
            cur_formation = get_formation(main_points)
            new_main_points = []
            for i in main_points:
                i[0] += self.region_chart[0]
                i[1] += self.region_chart[1]
                new_main_points.append(i)
            main_points = tuple(new_main_points)
            top_mean = get_mean_y(main_points[0],main_points[1])
            bottom_mean = get_mean_y(main_points[2],main_points[3])
            # cv2.line(img,main_points[0],main_points[1],(255,0,0),5)
            # cv2.line(img,main_points[2],main_points[3],(255,0,0),5)
            # cv2.line(img,(0,y),(200,y),(0,255,0),5)
            # cv2.line(img,(100,top_mean),(100,bottom_mean),(0,0,255),5)
            # cv2.line(img,
            #          (self.region_chart[0],self.region_chart[1]),
            #          (int((self.chart_width)*0.9)+self.region_chart[0],self.region_chart[3]),
            #          (150,150,140),
            #          5)
            # cv2.line(img,
            #          (main_points[0][0],main_points[0][1]+self.buff),
            #          (main_points[1][0],main_points[1][1]+self.buff),
            #          (200,0,70),5)
            # cv2.line(img,
            #          (main_points[2][0],main_points[2][1]-self.buff),
            #          (main_points[3][0],main_points[3][1]-self.buff),
            #          (200,0,70),5)
            # cv2.imwrite('test.png',img)
            # print(y,top_mean)
            # print(y,main_points[1][1])
            # print(y,bottom_mean)
            # print(cur_formation)
            if pos:
                if x > 0:
                    self.current_state = self.Has_close
                else:
                    if cur_formation == 'range':
                        if y < top_mean+self.buff:
                            self.current_state = self.Need_close
                        else:
                            self.current_state = self.Not_idea
                    else:
                        if y < main_points[1][1]+self.buff:
                            self.current_state = self.Need_close
                        else:
                            self.current_state = self.Not_idea
            else:
                if x > 0:
                    self.current_state = self.Has_req
                else:
                    if y > bottom_mean-self.buff and cur_formation != 'short':
                        self.current_state = self.Send_req
                    else:
                        self.current_state = self.Not_idea
        except:
            self.current_state = self.Not_idea

        # print(self,self.current_state, cur_formation)
  
        self.current_state(img,self.region_glass)