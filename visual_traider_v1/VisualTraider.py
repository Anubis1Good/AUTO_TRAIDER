import sys
import cv2
import keyboard
import pyautogui as pag
from traid_utils import click_lr,reset_lr,click_sr,reset_sr
from conditions import check_pos, check_req
from time import sleep
class VisualTraider():
    def __init__(self,left,top,right,bottom) -> None:
        self.region_glass = (left,top,right,bottom-25)
        self.region_pos = (left,bottom-25,right,bottom)
        self.Send_req = click_lr
        self.Has_req = reset_lr
        self.Has_close = reset_sr
        self.Need_close = click_sr
        self.current_state = self.Send_req

    def run(self,img):
        
        
        pos = check_pos(img,self.region_pos)
        x,y = check_req(img,self.region_glass)

        if pos:
            if x > 0:
                self.current_state = self.Has_close
            else: 
                self.current_state = self.Need_close
        else:
            if x > 0:
                self.current_state = self.Has_req
            else:
                self.current_state = self.Send_req    
  
  
        self.current_state(img,self.region_glass)
        # pag.PAUSE
        # print(self.current_state)
     
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


 