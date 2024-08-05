import os
import cv2
from stock_groups import stock_groups
from traider_bots.ST3 import ST3a as Trader
from traider_bots.help_bots.ResearchBot import ResearchBot
from settings import configuration_traiders_v2, reset_test_json


param_bots = configuration_traiders_v2('config.txt')
date_stock = '01.08.24'
img_path = './test_data/'

full_path = img_path + date_stock + '/'

imgs = os.listdir(full_path)
reset_test_json()

for ticker in stock_groups:
    traider = Trader(*param_bots,name=ticker)
    test_traider = ResearchBot(*param_bots,name=ticker)
    for img in imgs:
        if ticker in img:
            print(img)
            image = cv2.imread(full_path + img)
            traider.run(image)
            test_traider.run(image)
print('done')