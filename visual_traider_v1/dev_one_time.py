import os
from random import choice
import pyautogui as pag
import cv2
from settings import configuration_traiders_v2
# from traider_bots.VisualTraider_v3 import VisualTraider_v3 as Trader
from tas.PSTA1 import PSTA1 as TA
from traider_bots.help_bots.WorkBot import WorkBot as Trader

param_bots = configuration_traiders_v2('config_files\config.txt')
traider = Trader(*param_bots,name='MXI')
online = False
if online:
    param_bots = configuration_traiders_v2('config_files\config.txt')
    traider = Trader(*param_bots,name='MXI')
    pag.screenshot('screens\Screen.png')
    img = cv2.imread('screens\Screen.png')
else:
    param_bots = configuration_traiders_v2('config_files\config.txt')
    traider = Trader(*param_bots,name='MXI')
    traider.TA = TA(traider)
    list_folder = os.listdir('./test_data/')
    folder = choice(list_folder)
    list_imgs = os.listdir('./test_data/'+ folder + '/')
    rand_img = choice(list_imgs)
    print('./test_data/'+ folder + '/' + rand_img)
    img = cv2.imread('./test_data/'+ folder + '/' + rand_img)
    
img = traider.run(img)
cv2.imshow('work',img)
cv2.moveWindow('work',-10,-10)
cv2.waitKey(0)
cv2.imwrite('test.png',img)
print('done')