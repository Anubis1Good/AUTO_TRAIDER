import pyautogui as pag
from time import sleep
from random import randint
for i in range(30):
    sleep(2)
    pag.move(randint(1,10), randint(1,10))

