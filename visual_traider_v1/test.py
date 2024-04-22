import pyautogui as pag 
from time import sleep
from config import ImagesBtns
# button_start_loc = pag.locateOnScreen('./buttons/Header.png')
# pag.moveTo(button_start_loc)

# while True:
#     print(pag.position())
#     sleep(2)
# sleep(1)
pag.moveTo(pag.locateOnScreen(ImagesBtns.plate,grayscale=False,limit=10))