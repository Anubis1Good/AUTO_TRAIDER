import pyautogui as pag
import cv2
from settings import configuration_traiders_v2
from traider_bots.help_bots.WorkBot import WorkBot
param_bots = configuration_traiders_v2('config_dev.txt')
traider = WorkBot(*param_bots,name='MLTR')
pag.screenshot('Screen.png')
img = cv2.imread('Screen.png')
traider.run(img)
cv2.imshow('work',img)
cv2.moveWindow('work',-20,-20)
cv2.waitKey(0)
print('done')