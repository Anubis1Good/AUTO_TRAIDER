import os
import sys
import cv2
from tqdm import tqdm
from stock_groups import stock_groups
# from traider_bots.Collector1 import Collector1 as Trader
from traider_bots.archive.PT2ov1 import PT2 as Trader
# from traider_bots.ST14 import ST14 as Trader
# from traider_bots.ST8 import ST8 as Trader4
# from traider_bots.PST1 import PST1a as Trader5
# from traider_bots.PST1 import PST1 as Trader6
from traider_bots.help_bots.ResearchBot import ResearchBot
from settings import configuration_traiders_v2, reset_test_json,clear_test_images,clear_logs


param_bots = configuration_traiders_v2('config_files\config.txt')
if len(sys.argv) < 2:
    date_stock = '30.07.24d'
else:
    date_stock = sys.argv[1]

img_path = './test_data/'

full_path = img_path + date_stock + '/'

imgs = os.listdir(full_path)
clear_test_images()
clear_logs()
reset_test_json()
# stock_groups = ['MTLR','SBER','AFKS','SOFL','SELG']
# stock_groups = ['MXI','SBER']
# stock_groups = ['CNY']
for ticker in tqdm(stock_groups):
    traider = Trader(*param_bots,name=ticker)
    # traider2 = Trader2(*param_bots,name=ticker)
    # traider3 = Trader3(*param_bots,name=ticker)
    # traider4 = Trader4(*param_bots,name=ticker)
    # traider5 = Trader5(*param_bots,name=ticker)
    # traider6 = Trader6(*param_bots,name=ticker)
    # traider7 = Trader7(*param_bots,name=ticker)
    # test_traider = ResearchBot(*param_bots,name=ticker)
    # print(ticker)
    for img in imgs:
        if ticker in img:
            # print(img)
            full_path_img = full_path + img
            image = cv2.imread(full_path_img)
            price = float(img.split('_')[-1][:-4])
            
            traider.run(image,price)
            # traider2.run(image)
            # traider3.run(image)
            # traider3.draw_research(image)
            # traider4.run(image)
            # traider5.run(image)
            # traider6.run(image)
            # traider7.run(image)
            # traider.draw_research(image)
            # test_traider.run(image)
print('done')