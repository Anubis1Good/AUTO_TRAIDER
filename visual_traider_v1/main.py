import pyautogui as pag
import cv2
import keyboard
import sys
from time import sleep
from settings import configurtion_traiders

traiders = configurtion_traiders()
sleep(3)
while True:
    for i in range(50):
        sleep(1)
        keyboard.send('shift')
        pag.screenshot('Screen.png')
        img = cv2.imread('Screen.png')
        for traider in traiders:
            traider.run(img)
            if keyboard.is_pressed('Esc'):
                print("\nyou pressed Esc, so exiting...")
                sys.exit(0)
        pag.moveTo(traiders[0].region_glass[0]+10,traiders[0].region_glass[1]+10)
        # keyboard.send('tab') 
    # pag.press('space')