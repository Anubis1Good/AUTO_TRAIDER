import pyautogui as pag
import cv2
import keyboard
import sys
from time import sleep
from settings import configurtion_traiders
from stock_groups import stock_groups
from traider_bots.LRConter import LRConter
from traider_bots.LRDeport import LRDeport
from utils.test_utils.windows import draw_borders
LR_conter = configurtion_traiders(LRConter,'config.txt')
LR_deport = configurtion_traiders(LRDeport, 'config.txt')


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
        for i in range(len(LR_conter)):
            LR_deport[i].name = stock[i]
            LR_conter[i].name = stock[i]
            # LR_tranders[i].run(img)
            LR_deport[i].test(img)
            LR_conter[i].test(img)
            if keyboard.is_pressed('Esc'):
                print("\nyou pressed Esc, so exiting...")
                sys.exit(0)
        # sys.exit(0)
        pag.moveTo(LR_conter[0].region_glass[0]+10,LR_conter[0].region_glass[1]+10)
        sleep(2)
        keyboard.send('tab') 
    # pag.press('space')