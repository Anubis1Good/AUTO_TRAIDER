import pyautogui as pag
import cv2
import keyboard
import sys
import traceback
from time import sleep
from settings import configuration_traiders_v2
from sgs.sg_laptop import stock_groups
from utils.test_utils.windows import draw_borders_online
from traider_bots.help_bots.ResearchBot import ResearchBot
from traider_bots.VisualTraider_v3 import VisualTraider_v3 
from tas.SleepTA import SleepTA
from tas.PTA2_DDC import PTA2_DDC
from init_trader import init_trader

param_bots = configuration_traiders_v2('config_files\config.txt')
test_traiders = []
work_traiders = []
for i in range(len(stock_groups)):
    traider = ResearchBot(*param_bots,name=stock_groups[i])
    test_traiders.append(traider)
    traider = init_trader(stock_groups,i,param_bots)
    # if isinstance(traider,VisualTraider_v3):
    #     if isinstance(traider.TA,SleepTA):
    #         print(stock_groups[i])
    #         traider.TA = PTA2_DDC(traider,60)
    work_traiders.append(traider)

# draw_borders_online([work_traiders[0]])

sleep(3)
i = 0
while True:
    for i in range(len(test_traiders)):
        sleep(2)
        keyboard.send('shift')
        pag.screenshot('screens\Screen.png')
        img = cv2.imread('screens\Screen.png')
        work_traiders[i].run(img)
        test_traiders[i].run(img)
        if keyboard.is_pressed('Esc'):
            print("\nyou pressed Esc, so exiting...")
            sys.exit(0)
        try:
            pag.moveTo(work_traiders[i].glass_region[0]+10,work_traiders[i].glass_region[1]+10)
        except Exception as err:
            traceback.print_exc()
        keyboard.send('tab') 
