import pyautogui as pag
import cv2
import keyboard
import sys
from time import sleep
from settings import configuration_traiders_v2
from sg_dev import stock_groups
from utils.test_utils.windows import draw_borders
from traider_bots.help_bots.ResearchBot import ResearchBot



# traiders = configurtion_traiders(TestTraider,'config_dev.txt')
param_bots = configuration_traiders_v2('config_files\config.txt')
traider = ResearchBot(*param_bots,name=stock_groups[0])
# print(traider)
# pag.screenshot('Screen.png')
# img = cv2.imread('Screen.png')
# draw_borders(img,traider)

# sleep(3)
i = 0
while True:
    for stock in stock_groups:
        print(i)
        sleep(2)
        keyboard.send('shift')
        pag.screenshot('screens\Screen.png')
        img = cv2.imread('screens\Screen.png')
        
        traider.name = stock
            # traiders[i].run(img)
        traider.run(img)
        if keyboard.is_pressed('Esc'):
            print("\nyou pressed Esc, so exiting...")
            sys.exit(0)
        # sys.exit(0)
        pag.moveTo(traider.glass_region[0]+10,traider.glass_region[1]+10)
        sleep(2)
        i += 1
        # keyboard.send('tab') 
    # pag.press('space')