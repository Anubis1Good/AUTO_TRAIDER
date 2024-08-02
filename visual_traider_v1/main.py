import pyautogui as pag
import cv2
import keyboard
import sys
from time import sleep
from settings import configuration_traiders_v2
from stock_groups import stock_groups
from utils.test_utils.windows import draw_borders
from traider_bots.help_bots.ResearchBot import ResearchBot
from traider_bots.PT1 import PT1



param_bots = configuration_traiders_v2('config.txt')
test_traiders = []
work_traiders = []
for stock in stock_groups:
    traider = ResearchBot(*param_bots,name=stock)
    test_traiders.append(traider)
    traider = PT1(*param_bots,name=stock)
    traider.mode = 1
    work_traiders.append(traider)


# print(traider)
# pag.screenshot('Screen.png')
# img = cv2.imread('Screen.png')
# draw_borders(img,traider)

# sleep(3)
i = 0
while True:
    for i in range(len(test_traiders)):
        # print(i)
        sleep(2)
        keyboard.send('shift')
        pag.screenshot('Screen.png')
        img = cv2.imread('Screen.png')

        work_traiders[i].run(img)
        test_traiders[i].run(img)
        if keyboard.is_pressed('Esc'):
            print("\nyou pressed Esc, so exiting...")
            sys.exit(0)
        # sys.exit(0)
        try:
            pag.moveTo(traider.glass_region[0]+10,traider.glass_region[1]+10)
        except Exception as err:
            print(err)
        # sleep(1)
        # i += 1
        keyboard.send('tab') 
    # pag.press('space')