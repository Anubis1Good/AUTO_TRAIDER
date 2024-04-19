import pyautogui as pag
from VisualTraider import VisualTraider
test1 = VisualTraider(324,49,960,1055)
test2 = VisualTraider(1280,48,1916,1058)
while True:
    for i in range(30):
        test1.run()
        test2.run()
    pag.press('space')
    print('space')