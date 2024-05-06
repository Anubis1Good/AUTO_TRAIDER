import pyautogui as pag
import cv2
import keyboard
import sys
from time import sleep
from VisualTraider import VisualTraider

traiders = [
    VisualTraider(58,50,318,1055),
    VisualTraider(378,50,639,1055),
    VisualTraider(698,50,958,1055),
    VisualTraider(1018,50,1278,1055),
    VisualTraider(1338,50,1598,1055),
    VisualTraider(1658,50,1917,1055),
]
sleep(2)
while True:
    for i in range(20):
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