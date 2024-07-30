import pyautogui as pag
import cv2
from settings import configuration_traiders_v2
from traider_bots.help_bots.ResearchBot import ResearchBot
param_bots = configuration_traiders_v2('config.txt')
traider = ResearchBot(*param_bots,name='MLTR')
online = False
if online:
    pag.screenshot('Screen.png')
    img = cv2.imread('Screen.png')
else:
    img = cv2.imread('./learn_data/images/SOFL_1722342707.png')
traider.run(img)
cv2.imshow('work',img)
cv2.moveWindow('work',-20,-20)
cv2.waitKey(0)
cv2.imwrite('test.png',img)
print('done')