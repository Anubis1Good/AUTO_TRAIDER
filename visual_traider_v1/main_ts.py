import pyautogui as pag
import cv2
import keyboard
import sys
import traceback
from time import sleep
from settings import configuration_traiders_v2
from sgs.sg_laptop import stock_groups
from sgs.sg_on_bot import *
from utils.test_utils.windows import draw_borders,draw_borders_online
from traider_bots.help_bots.ResearchBot import ResearchBot
from traider_bots.PT2ov1 import PT2 
from traider_bots.PST1 import PST1 
from traider_bots.VisualTraider_v3 import VisualTraider_v3 
from tas.PTA2_DDC import PTA2_DDC
from tas.BaseTA import BaseTA



param_bots = configuration_traiders_v2('config_files\config_ts.txt')
test_traiders = []
work_traiders = []
for i in range(len(stock_groups)):
    traider = ResearchBot(*param_bots,name=stock_groups[i])
    test_traiders.append(traider)
    if stock_groups[i] in PTA_R_group:
        traider = VisualTraider_v3(*param_bots,name=stock_groups[i],mode=1)
        traider.TA = PTA2_DDC(traider,20)
    elif stock_groups[i] in PTA_R5_group:
        traider = VisualTraider_v3(*param_bots,name=stock_groups[i],mode=1)
        traider.TA = PTA2_DDC(traider,30)
    elif stock_groups[i] in PTA_R6_group:
        traider = VisualTraider_v3(*param_bots,name=stock_groups[i],mode=1)
        traider.TA = PTA2_DDC(traider,60)
    elif stock_groups[i] in PST1_group:
        traider = PST1(*param_bots,name=stock_groups[i],mode=1)
    elif stock_groups[i] in PT2ov_group:
        traider = PT2(*param_bots,name=stock_groups[i],mode=1)
    else:
        traider = VisualTraider_v3(*param_bots,name=stock_groups[i],mode=1)
        traider.TA = BaseTA(traider)
    work_traiders.append(traider)


# print(traider)
# pag.screenshot('screens\Screen.png')
# img = cv2.imread('Screen.png')
draw_borders_online([work_traiders[0]])
# gbw.draw_borders(img)

sleep(3)
i = 0
while True:
    for i in range(len(test_traiders)):
        # print(i)
        sleep(2)
        keyboard.send('shift')
        pag.screenshot('screens\Screen.png')
        img = cv2.imread('screens\Screen.png')

        work_traiders[i].run(img)
        test_traiders[i].run(img)
        if keyboard.is_pressed('Esc'):
            print("\nyou pressed Esc, so exiting...")
            sys.exit(0)
        # sys.exit(0)
        try:
            pag.moveTo(work_traiders[i].glass_region[0]+10,work_traiders[i].glass_region[1]+10)
        except Exception as err:
            traceback.print_exc()
        # sleep(1)
        # i += 1
        keyboard.send('tab') 
#     # pag.press('space')