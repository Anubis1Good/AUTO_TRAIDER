import pyautogui as pag
import cv2
import keyboard
import sys
from time import sleep
from settings import configurtion_traiders
from stock_groups import stock_groups
from traider_bots.LRTraider import LRTraider
from utils.test_utils.windows import draw_borders
LR_traiders = configurtion_traiders(LRTraider,'config.txt')

sleep(3)
# pag.screenshot('Screen.png')
# img = cv2.imread('Screen.png')
# draw_borders(img,LR_traiders)
while True:
    for stock in stock_groups:
        sleep(2)
        keyboard.send('shift')
        pag.screenshot('Screen.png')
        img = cv2.imread('Screen.png')
        for i in range(len(LR_traiders)):
            LR_traiders[i].name = stock[i]
            LR_traiders[i].run(img)
            # LR_traiders[i].test(img)
            if keyboard.is_pressed('Esc'):
                print("\nyou pressed Esc, so exiting...")
                sys.exit(0)
        # sys.exit(0)
        pag.moveTo(LR_traiders[0].region_glass[0]+10,LR_traiders[0].region_glass[1]+10)
        sleep(2)
        keyboard.send('tab') 
    # pag.press('space')