import pyautogui as pag
import cv2
import keyboard
import sys
import traceback
from time import sleep
from settings import configuration_traiders_v2
from sgs.sg_laptop import stock_groups
from utils.test_utils.windows import draw_borders,draw_borders_online
from traider_bots.help_bots.ResearchBot import ResearchBot
from traider_bots.PST1 import PST1 as Traider1
from traider_bots.VisualTraider_v3 import VisualTraider_v3 as Trader
from tas.PTA1_BDDC import PTA1_R_BDDC as TA



param_bots = configuration_traiders_v2('config_files\config.txt')
test_traiders = []
work_traiders = []
for i in range(len(stock_groups)):
    traider = ResearchBot(*param_bots,name=stock_groups[i])
    test_traiders.append(traider)
    if stock_groups[i] == 'MXI':
        traider = Trader(*param_bots,name=stock_groups[i],mode=1,fast_close=True)
        traider.TA = TA(traider)
    else:
        traider = Traider1(*param_bots,name=stock_groups[i],mode=1)
    work_traiders.append(traider)


# print(traider)
# pag.screenshot('screens\Screen.png')
# img = cv2.imread('Screen.png')
# draw_borders_online([work_traiders[0]])
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