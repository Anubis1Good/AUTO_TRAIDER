import pyautogui as pag
import cv2
import keyboard
import sys
from time import sleep
from VisualTraider import VisualTraider

traiders = [
    VisualTraider(58,52,270,740),
    VisualTraider(331,52,543,740),
    VisualTraider(603,52,816,740),
    VisualTraider(877,52,1090,740),
    VisualTraider(1151,52,1363,740),


]   
sleep(3)
while True:
    for i in range(50):
        sleep(1)
        pag.press('shift')
        pag.screenshot('Screen.png')
        img = cv2.imread('Screen.png')
        for traider in traiders:
            traider.run(img)
            if keyboard.is_pressed('Esc'):
                print("\nyou pressed Esc, so exiting...")
                sys.exit(0)
        pag.moveTo(traiders[0].region_glass[0]+10,traiders[0].region_glass[1]+10)
        pag.press('tab') 
    pag.press('space')