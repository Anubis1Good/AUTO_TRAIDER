import os
import sys
import cv2
from tqdm import tqdm
from stock_groups import stock_groups
from init_trader import init_test
from settings import configuration_traiders_v2, reset_test_json,clear_test_images,clear_logs


param_bots = configuration_traiders_v2('config_files\config.txt')
if len(sys.argv) < 2:
    date_stock = '13.11.2024'
else:
    date_stock = sys.argv[1]

img_path = 'test_data'
if len(sys.argv) < 3:
    data_variant = 'new_data2'
else:
    data_variant = sys.argv[2]
if len(sys.argv) < 4:
    bot_name = 'ST1'
else:
    bot_name = sys.argv[3]
if len(sys.argv) > 4:
    temp = sys.argv[4].split('_')
    if all(temp):
        stock_groups = temp




full_path = os.path.join(img_path,data_variant,date_stock) + '/'


imgs = os.listdir(full_path)
clear_test_images()
clear_logs()
reset_test_json()
# stock_groups = ['MTLR','SBER','AFKS','SOFL','SELG']
# stock_groups = ['MXI','SBER']
# stock_groups = ['CNY']
for ticker in tqdm(stock_groups):
    
    trader = init_test(bot_name,param_bots,ticker)

    for img in imgs:
        if ticker in img:
            # print(img)
            full_path_img = full_path + img
            image = cv2.imread(full_path_img)
            price = float(img.split('_')[-1][:-4])
            
            trader.run(image,price)

print('done')