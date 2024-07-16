import os
import re
from datetime import datetime
import pandas as pd
import cv2
import numpy as np
from sec_codes import sec_codes

test_re1, test_re2 = None,None
df_bars = None
df_data = None
delta_std = None
path_images = None



def get_time(filename:str):
    moment_time = re.sub(test_re1,"",filename)
    moment_time = re.sub(test_re2,"",moment_time)
    moment_time = re.sub('[P]?',"",moment_time)
    try:
        moment_time = float(moment_time)//60
    except:
        print(test_re1,test_re2,filename,moment_time)
        raise ValueError('Недопустимое значение')
    return moment_time

def get_price(row):
    row_bars = df_bars[df_bars['datetime'] == row['time']]
    open = row_bars['open'].values
    close = row_bars['close'].values
    if len(open) != 0 and len(close) != 0:
        price = (open[0] + close[0])/2
    else:
        price = None
    row['price'] = price
    return row

def change_date(date):
    return datetime.strptime(date,'%d.%m.%Y %H:%M').timestamp()//60

def add_delta(row):
    index = row.name
    delta = 0
    try:
        delta = round((df_data.iloc[index+5]['price'] - df_data.iloc[index]['price']),2)
    except:
        pass
    return delta

def add_direction(row):
    if row['delta'] > delta_std/2:
        return 1
    if row['delta'] < -delta_std/2:
        return -1
    return 0

def change_img(img:str):
    image = cv2.imread(f'{path_images}{img}')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = np.array(cv2.resize(image,(300,200)))
    image = image.flatten()
    image = image/255
    return image.tolist()

def create_df(ticker,path_images,date):
    global test_re1, test_re2, df_bars, df_data, delta_std
    path_bars = f'./Data/TQBR.{ticker}_T1.txt'
    df_bars = pd.read_csv(path_bars,sep='\t')
    df_bars['datetime'] = df_bars['datetime'].apply(change_date)
    df_bars = df_bars.drop_duplicates()
    files = os.listdir(path_images)
    filter_files = list(filter(lambda x: x.find(ticker) != -1, files))
    test_re1 = f'[{ticker}]'
    test_re2 = '.png'
    df_data = pd.DataFrame(columns=['img','time','price'])
    df_data['img'] = filter_files
    df_data['time'] = df_data['img'].apply(get_time)
    df_data = df_data.apply(get_price,axis=1)
    df_data.dropna(inplace=True)
    df_data.reset_index(inplace=True)
    df_data.drop('index',axis=1,inplace=True)
    df_data['delta'] = df_data.apply(add_delta,axis=1)
    delta_std = df_data['delta'].std()
    df_data['direction'] = df_data.apply(add_direction,axis=1)
    df_data = df_data.iloc[:-5]
    folder_path = f'./DataFrames/{date}'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    df_data.to_csv(f'{folder_path}/{ticker}.csv', index=False) 

if __name__ == '__main__':
    path_images = './DataForLearning/10.07.24/images/'
    for ticker in sec_codes:
        create_df(ticker,path_images,'10.07.24')













# df_data.to_json(f'./DataFrames/{ticker}.json', index=False) 
# df_data['img'] = df_data['img'].apply(change_img)

# check_work
# sample = df_data.sample()
# img = sample['img'].to_numpy()[0]
# print(img.shape)
# print(sample)

# # img = np.array(img,np.uint8)
# cv2.imshow('some_name',img) 
# cv2.waitKey(0)
# df_data.info()