import os
import sys
import cv2
import json
import pandas as pd
from tqdm import tqdm
from stock_groups import stock_groups
from init_trader import init_smart_test
from settings import configuration_traiders_v2

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
    bot_name = 'PTA2_DDC_60'
else:
    bot_name = sys.argv[3]
if len(sys.argv) > 4:
    temp = sys.argv[4].split('_')
    if all(temp):
        stock_groups = temp




full_path = os.path.join(img_path,data_variant,date_stock) + '/'

imgs = os.listdir(full_path)

store,close_store = [],[]

bots = {}
# stock_groups = ['AFKS']
for ticker in stock_groups:
    trader = init_smart_test(bot_name,param_bots,ticker)
    bots[ticker] = trader
        
for img in tqdm(imgs):
    img_split = img.split('_')
    ticker = img_split[0]
    if ticker in stock_groups:
        full_path_img = full_path + img
        image = cv2.imread(full_path_img)
        price = float(img_split[-1][:-4])
        bots[ticker].run(image,price,store,close_store)


# smart_tests_path = 'test_files\smart_tests'
# if not os.path.exists(smart_tests_path):
#     os.mkdir(smart_tests_path)

# file_path = os.path.join(smart_tests_path,date_stock + '.json')
# print(store)
# print(close_store)
# with open(file_path,'w') as f:
#     json.dump(close_store,f)

close_store += store

df = pd.DataFrame(close_store)

with open('test_files\last_price.json') as f:
    last_prices = json.load(f)

def change_cp(row,lp):
    if row['close'] == "":
        if row['name'] in lp:
            cp = float(lp[row['name']])
            return cp
    return row.close_price

def get_quity(row):
    if row.pos == 'long':
        quity = row.close_price - row.open_price
    else:
        quity = row.open_price- row.close_price
    return quity
try:
    lp = last_prices[date_stock]
    df.close_price = df.apply(lambda row:change_cp(row,lp),axis=1)
    df['quity'] = df.apply(get_quity,axis=1)
    df['percent'] = round(df['quity'] / df['open_price'],4)*100
    res = df.groupby('name')['quity'].agg(['sum','count'])
    res = res.sort_values(by='count',axis=0,ascending=False)
    res['part'] = res['sum'] / res['count']
    res['total_percent'] = df.groupby('name')['percent'].agg(['sum'])['sum']
    res['average_percent'] = round(res['total_percent']/ res['count'],2)
    path_output = os.path.join('test_results',bot_name + '_' + date_stock + "_output.xlsx")
    with pd.ExcelWriter(path_output) as writer:  
        df.to_excel(writer,sheet_name='total') 
        res.to_excel(writer,sheet_name='sum_count') 
except:
    print('not data')

print('done')