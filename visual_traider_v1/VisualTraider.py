import sys
import cv2
import keyboard
import pyautogui as pag
from traid_utils import click_lr, reset_lr, click_sr, reset_sr, idle, click_bl,click_bs, not_idea
from conditions import check_pos, check_req, check_graphic_level
from time import sleep
class VisualTraider():
    def __init__(self,left,top,right,bottom,high_graphic) -> None:
        self.region_glass = (left,top,right,high_graphic-25)
        self.region_pos = (left,high_graphic-25,right,high_graphic)
        self.region_graphic = (left, high_graphic,right,bottom)
        # self.Send_req = click_lr
        # self.Has_req = reset_lr
        # self.Has_close = reset_sr
        # self.Need_close = click_sr
        self.Send_req = click_bl
        self.Has_req = idle
        self.Has_close = idle
        self.Need_close = click_bs
        self.Not_idea = not_idea
        self.current_state = self.Not_idea
    
    def __repr__(self):
        return f'VT - {self.region_glass}'

    def run(self,img):      
        pos = check_pos(img,self.region_pos)
        x,y = check_req(img,self.region_glass)
        graphic_level = check_graphic_level(img,self.region_graphic)
        print(self,x,y)
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
        # pag.PAUSE
        print(self, self.current_state)
     
# test1 = VisualTraider(1240,49,1918,1057)
# sleep(2)
# while True:
#     for i in range(30): 
#         pag.screenshot('Screen.png')
#         img = cv2.imread('Screen.png')
#         test1.run(img)
#         if keyboard.is_pressed('Esc'):
#             print("\nyou pressed Esc, so exiting...")
#             sys.exit(0)

#     pag.press('space')


 