import pyautogui as pag
import pydirectinput as pdi 
from time import sleep
import numpy as np
from utils.config import ColorsBtnBGR
from utils.utils import color_search
from time import time
import cv2
import sys
import keyboard
# sleep(5)
# pag.screenshot('Screen.png')
# print(10+int(None))
a = np.array([[1,2],[3,4]])
b = a[:,1:]
b += 10
b = np.hstack([a[:,:1],b])
print(b)
# img = cv2.imread('./mask.png')
# img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# print(img.tolist())
# template = np.array([
#     [[0,0,0],[0,0,0],[0,0,0]],
#     [[0,0,0],[255,255,255],[0,0,0]],
#     [[0,0,0],[255,255,255],[0,0,0]]],dtype=np.uint8)
# print(template)
# cv2.imshow('template',template)
# cv2.waitKey(0)
# pdi.press("f")
# keyboard.send('f')

# while True:
#     if keyboard.is_pressed('Esc'):
#         print("\nyou pressed Esc, so exiting...")
#         sys.exit(0) 
#     pag.screenshot('Screen.png')

#     img = cv2.imread('Screen.png')

#     # x,y = color_search(img,ColorsBtnBGR.best_bid,(1600,49,1918,1050))
#     region = (1600,49,1918,1050)
#     xbb,ybb = color_search(img,ColorsBtnBGR.best_bid,region)
#     if xbb > 0:
#         new_region = (xbb,ybb,region[2],region[3])
#         x,y = color_search(img,ColorsBtnBGR.large_value_2,new_region)
#         pag.moveTo(x,y)

    # if x>0:
    # else:
    #     x,y = color_search(img,ColorsBtnBGR.color_x,(1380,49,1918,1050),reverse=True)
    #     if x>0:
    #         pag.moveTo(x,y)
    #     else:
    #         print('Not Found!')

# print(type(img))
# img[400:600,400:600] = [0,0,255]
# ===============
# x = np.argwhere((img[123:983,1323:1780,0] == ColorsBtnBGR.large_value_1[0])& (img[123:983,1323:1780,1] == ColorsBtnBGR.large_value_1[1])& (img[123:983,1323:1780,2] == ColorsBtnBGR.large_value_1[2]))

# pag.moveTo(x[-1,1]+1323,x[-1,0]+123)
# pag.moveTo(x[0,1],x[0,0])
# ===============
# img[x[0]] = [0,0,255]
# cv2.imshow('test',img)

# cv2.waitKey(0)