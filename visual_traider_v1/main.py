import pyautogui as pag
import cv2
import keyboard
import sys
from time import sleep
from settings import configurtion_traiders
from stock_groups import stock_groups
traiders = configurtion_traiders()

sleep(1)
while True:
    for stock in stock_groups:
        sleep(1)
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
        # pag.moveTo(traiders[0].region_glass[0]+10,traiders[0].region_glass[1]+10)
        # keyboard.send('tab') 
    # pag.press('space')