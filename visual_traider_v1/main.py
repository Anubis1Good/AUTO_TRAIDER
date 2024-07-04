import pyautogui as pag
import cv2
import keyboard
import sys
from time import sleep
from settings import configurtion_traiders
from stock_groups import stock_groups
from traider_bots.LRTrander import LRTrander
from traider_bots.LRConter import LRConter
from traider_bots.AntiLR import AntiLR
from traider_bots.FourPointsLR import FourPointsLR
from utils.test_utils.windows import draw_borders
LR_tranders = configurtion_traiders(LRTrander,'config.txt')
LR_conter = configurtion_traiders(LRConter,'config.txt')
LR_anti = configurtion_traiders(AntiLR,'config.txt')
Four_points = configurtion_traiders(FourPointsLR,'config.txt')

sleep(3)
# pag.screenshot('Screen.png')
# img = cv2.imread('Screen.png')
# draw_borders(img,LR_tranders)
while True:
    for stock in stock_groups:
        sleep(1)
        keyboard.send('shift')
        sleep(1)
        pag.screenshot('Screen.png')
        img = cv2.imread('Screen.png')
        for i in range(len(LR_tranders)):
            LR_tranders[i].name = stock[i]
            LR_conter[i].name = stock[i]
            LR_anti[i].name = stock[i]
            Four_points[i].name = stock[i]
            # LR_tranders[i].run(img)
            LR_tranders[i].test(img)
            LR_conter[i].test(img)
            LR_anti[i].test(img)
            Four_points[i].test(img)
            if keyboard.is_pressed('Esc'):
                print("\nyou pressed Esc, so exiting...")
                sys.exit(0)
        # sys.exit(0)
        pag.moveTo(LR_tranders[0].region_glass[0]+10,LR_tranders[0].region_glass[1]+10)
        sleep(2)
        keyboard.send('tab') 
    # pag.press('space')