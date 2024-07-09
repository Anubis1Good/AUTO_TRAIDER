import pyautogui as pag
import cv2
import keyboard
import sys
from time import sleep
from settings import configurtion_traiders
from stock_groups import stock_groups
from traider_bots.help_bots.PrepareBot import PrepareBot
from utils.test_utils.windows import draw_borders
main_bots = configurtion_traiders(PrepareBot,'config.txt')



sleep(3)
# pag.screenshot('Screen.png')
# img = cv2.imread('Screen.png')
# draw_borders(img,LR_tranders)
while True:
    for stock in stock_groups:
        sleep(5)
        keyboard.send('shift')
        sleep(1)
        pag.screenshot('Screen.png')
        img = cv2.imread('Screen.png')
        for i in range(len(main_bots)):
            main_bots[i].name = stock[i]
            # LR_tranders[i].run(img)
            main_bots[i].test(img)
            if keyboard.is_pressed('Esc'):
                print("\nyou pressed Esc, so exiting...")
                sys.exit(0)
        # sys.exit(0)
        pag.moveTo(main_bots[0].region_glass[0]+10,main_bots[0].region_glass[1]+10)
        sleep(4)
        keyboard.send('tab') 
    # pag.press('space')