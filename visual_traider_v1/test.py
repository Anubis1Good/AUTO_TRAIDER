import pyautogui as pag
import pydirectinput as pdi 
from time import sleep,time
import numpy as np
from utils.config import ColorsBtnBGR
from utils.utils import color_search
from datetime import datetime
import cv2
import sys
import keyboard
from wrappers.GroupBotWrapper import GroupBotWrapper
from traider_bots.VisualTraider_v2 import VisualTraider_v2
import threading
from multiprocessing import Pool

# def if_prime(x):
#     if x <= 1:
#         return 0
#     elif x <= 3:
#         return x
#     elif x % 2 == 0 or x % 3 == 0:
#         return 0
#     i = 5
#     while i**2 <= x:
#         if x % i == 0 or x % (i + 2) == 0:
#             return 0
#         i += 6
#     return x

# a = time()
# answer = 0

# if __name__ == '__main__':
#     with Pool(6) as p:
#         answer = sum(p.map(if_prime, list(range(1000000))))
# print(time() - a)

a = [1,2,3]
b = ['a','b','c']
c = [10]*len(a)
print(list(zip(a,b,c)))

# now = datetime.now()
# hour = now.hour
# minute = now.minute
# print(hour)
# print(minute)
# print('_'.split('_'))
# sleep(5)
# print(sys.argv)
# pag.screenshot('screens\Screen.png')
# gbw = GroupBotWrapper(
#     VisualTraider_v2,
#     ['SBER','GAZP','VTBR','LKOH'],
#     51,
#     1918,
#     766,
#     151,
#     709,
#     737,
#     1035,
#     143,
#     0)
# img = cv2.imread('screens\Screen.png')
# gbw.draw_borders(img)
# img = cv2.imread('screens\Screenshot_7.png')
# gbw = GroupBotWrapper(
#     VisualTraider_v2,
#     ['Stock1','Stock2','Stock3','Stock4'],
#     51,
#     1364,
#     529,
#     222,
#     474,
#     499,
#     701,
#     60,
#     0)
# gbw.draw_borders(img)
# print(10+int(None))
# a = np.array([[1,2],[3,4]])
# b = a[:,1:]
# b += 10
# b = np.hstack([a[:,:1],b])
# print(b)
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
#     pag.screenshot('screens\Screen.png')

#     img = cv2.imread('screens\Screen.png')

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

