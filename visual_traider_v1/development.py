import pyautogui as pag
import cv2
import keyboard
import sys
from time import sleep
from settings import configurtion_traiders
from sg_dev import stock_groups
from utils.test_utils.windows import draw_borders
from traider_bots.TestTraider import TestTraider
from traider_bots.FourPointsLR import FourPointsLR


# traiders = configurtion_traiders(TestTraider,'config_dev.txt')
traiders = configurtion_traiders(FourPointsLR,'config_dev.txt')
# pag.screenshot('Screen.png')
# img = cv2.imread('Screen.png')
# draw_borders(img,traiders)

# sleep(3)
while True:
    for stock in stock_groups:
        sleep(2)
        keyboard.send('shift')
        pag.screenshot('Screen.png')
        img = cv2.imread('Screen.png')
        for i in range(len(traiders)):
            traiders[i].name = stock[i]
            # traiders[i].run(img)
            traiders[i].test(img)
            if keyboard.is_pressed('Esc'):
                print("\nyou pressed Esc, so exiting...")
                sys.exit(0)
        # sys.exit(0)
        pag.moveTo(traiders[0].region_glass[0]+10,traiders[0].region_glass[1]+10)
        sleep(2)
        # keyboard.send('tab') 
    # pag.press('space')