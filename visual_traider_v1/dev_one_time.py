import pyautogui as pag
import cv2
from settings import configuration_traiders_v2
from traider_bots.help_bots.WorkBot import WorkBot
param_bots = configuration_traiders_v2('config.txt')
traider = WorkBot(*param_bots,name='MLTR')
online = False
if online:
    param_bots = configuration_traiders_v2('config_dev.txt')
    traider = WorkBot(*param_bots,name='MLTR')
    pag.screenshot('Screen.png')
    img = cv2.imread('Screen.png')
else:
    param_bots = configuration_traiders_v2('config.txt')
    traider = WorkBot(*param_bots,name='MLTR')
    img = cv2.imread('./test_data/24.07.24/images/SBER_1721808621.png')
    
traider.run(img)
cv2.imshow('work',img)
cv2.moveWindow('work',-20,-20)
cv2.waitKey(0)
cv2.imwrite('test.png',img)
print('done')