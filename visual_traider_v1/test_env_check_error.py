import os
import sys
import cv2
from tqdm import tqdm
from stock_groups import stock_groups
from traider_bots.help_bots.CheckErrorDataBot import CED
from settings import configuration_traiders_v2, reset_test_json,clear_test_images,clear_logs


param_bots = configuration_traiders_v2('config_files\config.txt')
img_path = 'test_data'
error_path = 'errors_data'
data_variant = 'old_data'
# data_variant = 'new_data1'
# data_variant = 'new_data2'

if len(sys.argv) < 2:
    days = os.listdir(os.path.join(img_path,data_variant))
    date_stock = days[0]
    print(date_stock)
else:
    date_stock = sys.argv[1]

full_path = os.path.join(img_path,data_variant,date_stock) + '/'
# full_path = img_path + date_stock + '/'

imgs = os.listdir(full_path)
clear_test_images()
clear_logs()
reset_test_json()
for ticker in tqdm(stock_groups):
    traider = CED(*param_bots,ticker)
    for img in imgs:
        if ticker in img:
            # print(img)
            full_path_img = full_path + img
            image = cv2.imread(full_path_img)
            price = float(img.split('_')[-1][:-4])
            
            res = traider.run(image,price)
            if res != 1:
                new_path = os.path.join(error_path,img)    
                os.replace(full_path_img,new_path)
print('done')