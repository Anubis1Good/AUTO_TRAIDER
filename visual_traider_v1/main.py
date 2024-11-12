import pyautogui as pag
import cv2
import keyboard
import sys
import traceback
from time import sleep
from settings import configuration_traiders_v2
from stock_groups import stock_groups
from sgs.sg_on_bot import *
from utils.test_utils.windows import draw_borders,draw_borders_online
from traider_bots.help_bots.ResearchBot import ResearchBot
from traider_bots.Collector1 import Collector1
from traider_bots.PT2ov1 import PT2 
from traider_bots.PST1 import PST1 
from traider_bots.archive.PT1 import PT1 
from traider_bots.VisualTraider_v3 import VisualTraider_v3 
from tas.PTA1_BDDC import PTA1_R_BDDC 
from tas.PTA1_BDDC import PTA1_R5_BDDC 
from tas.BaseTA import BaseTA
from wrappers.GroupBotWrapper import GroupBotWrapper


param_bots = configuration_traiders_v2('config_files\config.txt')
test_traiders = []
work_traiders = []
for i in range(len(stock_groups)):
    traider = ResearchBot(*param_bots,name=stock_groups[i])
    test_traiders.append(traider)
    ta = lambda: None
    if stock_groups[i] in PTA_R_group:
        traider = VisualTraider_v3
        ta = PTA1_R_BDDC
    # elif stock_groups[i] in PTA_R5_group:
    #     traider = VisualTraider_v3
    #     ta = PTA1_R5_BDDC
    # elif stock_groups[i] in PT1_group:
    #     traider = PT1
    # elif stock_groups[i] in PST1_group:
    #     traider = PST1
    elif stock_groups[i] in PT2ov_group:
        traider = PT2
    else:
        traider = VisualTraider_v3
        ta = PTA1_R5_BDDC
        # traider = VisualTraider_v3
        # ta = BaseTA
    gbw = GroupBotWrapper(
    traider,
    ['Stock1','Stock2','Stock3','Stock4'],
    51,
    1277,
    653,
    105,
    599,
    624,
    877,
    108,
    1,
    ta,
    True)
    # if i %2 == 0:
    # traider = Traider1(*param_bots,name=stock_groups[i])
    # else:
    #     traider = Traider2(*param_bots,name=stock_groups[i])
    # gbw.mode = 1
    work_traiders.append(gbw)


# print(traider)
# pag.screenshot('screens\Screen.png')
# img = cv2.imread('Screen.png')
# draw_borders_online(gbw.traders)
# gbw.draw_borders(img)

sleep(5)
i = 0
while True:
    for i in range(len(test_traiders)):
        # print(i)
        sleep(2)
        keyboard.send('shift')
        pag.screenshot('screens\Screen.png')
        img = cv2.imread('screens\Screen.png')

        work_traiders[i].run(img)
        # test_traiders[i].run(img)
        if keyboard.is_pressed('Esc'):
            print("\nyou pressed Esc, so exiting...")
            sys.exit(0)
        # sys.exit(0)
        try:
            pag.moveTo(traider.glass_region[0]+10,traider.glass_region[1]+10)
        except Exception as err:
            traceback.print_exc()
        # sleep(1)
        # i += 1
        keyboard.send('tab') 
#     # pag.press('space')