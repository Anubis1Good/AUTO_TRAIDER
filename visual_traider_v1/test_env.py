import os
import sys
import cv2
from tqdm import tqdm
from stock_groups import stock_groups
# from traider_bots.Collector1 import Collector1 as Trader
from traider_bots.archive.OGT2 import OGT2 as Trader
# from traider_bots.VisualTraider_v3 import VisualTraider_v3 as Trader
# from tas.PTA1_BDDC import PTA1_R_BDDC as TA
from traider_bots.help_bots.ResearchBot import ResearchBot
from settings import configuration_traiders_v2, reset_test_json,clear_test_images,clear_logs


param_bots = configuration_traiders_v2('config_files\config.txt')
if len(sys.argv) < 2:
    date_stock = '01.08.24'
else:
    date_stock = sys.argv[1]

img_path = 'test_data'
data_variant = 'old_data'
# data_variant = 'new_data1'
# data_variant = 'new_data2'
full_path = os.path.join(img_path,data_variant,date_stock) + '/'
# full_path = img_path + date_stock + '/'

imgs = os.listdir(full_path)
clear_test_images()
clear_logs()
reset_test_json()
# stock_groups = ['MTLR','SBER','AFKS','SOFL','SELG']
# stock_groups = ['MXI','SBER']
# stock_groups = ['CNY']
for ticker in tqdm(stock_groups):
    # traider = Trader(*param_bots,name=ticker)
    traider = Trader(*param_bots,ticker)
    # traider.TA = TA(traider)
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
            # test_traider.run(image)
print('done')