import pyautogui as pag
import cv2
import keyboard
import sys
import traceback
from time import sleep
from datetime import datetime
from settings import configuration_traiders_v2
from sgs.sg_laptop import stock_groups
from utils.test_utils.windows import draw_borders_online
from traider_bots.help_bots.ResearchBot import ResearchBot
from traider_bots.VisualTraider_v3 import VisualTraider_v3 
from tas.SleepTA import SleepTA
from tas.CloserTA import CloserTA
from tas.LTA1_C import LTA1_C
from init_trader import init_trader

now = datetime.now()
hour = now.hour
minute = now.minute

param_bots = configuration_traiders_v2('config_files\config.txt')
test_traiders = []
work_traiders = []
for i in range(len(stock_groups)):
    traider = ResearchBot(*param_bots,name=stock_groups[i])
    test_traiders.append(traider)
    traider = init_trader(stock_groups[i],param_bots)
    if 23 > hour > 18:
        if isinstance(traider,VisualTraider_v3):
            if isinstance(traider.TA,SleepTA):
                traider.TA = LTA1_C(traider)
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

        # if hour == 18 and minute > 25:
        #     work_traiders[i].TA = CloserTA(work_traiders[i])
        # if hour == 23 and minute > 25:
        #     work_traiders[i].TA = CloserTA(work_traiders[i])

        work_traiders[i].run(img)
        test_traiders[i].run(img)
        if keyboard.is_pressed('Esc'):
            print("\nyou pressed Esc, so exiting...")
            sys.exit(0)
        try:
            pag.moveTo(work_traiders[i].glass_region[0]+10,work_traiders[i].glass_region[1]+10)
        except Exception as err:
            traceback.print_exc()

        now = datetime.now()
        hour = now.hour
        minute = now.minute

        keyboard.send('tab') 
