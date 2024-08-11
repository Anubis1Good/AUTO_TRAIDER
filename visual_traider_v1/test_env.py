import os
import cv2
from stock_groups import stock_groups
from traider_bots.ST9 import ST9 as Trader
from traider_bots.archive.OGT1 import OGT1 as Trader2
from traider_bots.archive.PT2ov1 import PT2 as Trader3
from traider_bots.archive.PT3 import PT3 as Trader4
from traider_bots.ST8 import ST8 as Trader5
from traider_bots.ST9 import ST9 as Trader6
from traider_bots.PST1 import PST1 as Trader7
from traider_bots.help_bots.ResearchBot import ResearchBot
from settings import configuration_traiders_v2, reset_test_json,clear_test_images,clear_logs


param_bots = configuration_traiders_v2('config.txt')
date_stock = '08.08.24'
img_path = './test_data/'

full_path = img_path + date_stock + '/'

imgs = os.listdir(full_path)
clear_test_images()
clear_logs()
reset_test_json()
# stock_groups = ['MXI','CNY','LKOH','SBER','AFKS','SOFL','SELG']
for ticker in stock_groups:
    traider = Trader(*param_bots,name=ticker)
    # traider2 = Trader2(*param_bots,name=ticker)
    # traider3 = Trader3(*param_bots,name=ticker)
    # traider4 = Trader4(*param_bots,name=ticker)
    # traider5 = Trader5(*param_bots,name=ticker)
    # traider6 = Trader6(*param_bots,name=ticker)
    # traider7 = Trader7(*param_bots,name=ticker)
    # test_traider = ResearchBot(*param_bots,name=ticker)
    for img in imgs:
        if ticker in img:
            print(img)
            image = cv2.imread(full_path + img)
            traider.run(image)
            # traider2.run(image)
            # traider3.run(image)
            # traider4.run(image)
            # traider5.run(image)
            # traider6.run(image)
            # traider7.run(image)
            # traider.draw_research(image)
            # test_traider.run(image)
print('done')