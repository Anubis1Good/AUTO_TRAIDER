import os
import cv2
from stock_groups import stock_groups
from traider_bots.PT1 import PT1
from settings import configuration_traiders_v2

param_bots = configuration_traiders_v2('config.txt')
date_stock = '24.07.24'
img_path = './test_data/'

full_path = img_path + date_stock + '/images/'

imgs = os.listdir(full_path)

# ticker = 'LKOH'
for ticker in stock_groups:
    traider = PT1(*param_bots,name=ticker)
    for img in imgs:
        if ticker in img:
            print(img)
            image = cv2.imread(full_path + img)
            traider.run(image)
print('done')