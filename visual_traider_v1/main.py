import pyautogui as pag
import cv2
import keyboard
import sys
import traceback
from time import sleep
from settings import configuration_traiders_v2
from stock_groups import stock_groups
from utils.test_utils.windows import draw_borders,draw_borders_online
from traider_bots.help_bots.ResearchBot import ResearchBot
from traider_bots.Collector1 import Collector1 as Traider1
from wrappers.GroupBotWrapper import GroupBotWrapper


param_bots = configuration_traiders_v2('config_files\config.txt')
test_traiders = []
work_traiders = []
for i in range(len(stock_groups)):
    traider = ResearchBot(*param_bots,name=stock_groups[i])
    test_traiders.append(traider)
    gbw = GroupBotWrapper(
    Traider1,
    ['Stock1','Stock2','Stock3','Stock4'],
    51,
    1364,
    529,
    222,
    474,
    499,
    701,
    60,
    1)
    # if i %2 == 0:
    # traider = Traider1(*param_bots,name=stock_groups[i])
    # else:
    #     traider = Traider2(*param_bots,name=stock_groups[i])
    # gbw.mode = 1
    work_traiders.append(gbw)


# print(traider)
# pag.screenshot('screens\Screen.png')
# img = cv2.imread('Screen.png')
draw_borders_online(gbw.traders)
# gbw.draw_borders(img)

# sleep(3)
# i = 0
# while True:
#     for i in range(len(test_traiders)):
#         # print(i)
#         sleep(2)
#         keyboard.send('shift')
#         pag.screenshot('screens\Screen.png')
#         img = cv2.imread('screens\Screen.png')

#         work_traiders[i].run(img)
#         test_traiders[i].run(img)
#         if keyboard.is_pressed('Esc'):
#             print("\nyou pressed Esc, so exiting...")
#             sys.exit(0)
#         # sys.exit(0)
#         try:
#             pag.moveTo(traider.glass_region[0]+10,traider.glass_region[1]+10)
#         except Exception as err:
#             traceback.print_exc()
#         # sleep(1)
#         # i += 1
#         keyboard.send('tab') 
#     # pag.press('space')