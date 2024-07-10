import os
import re
import pandas as pd
from datetime import datetime,timedelta

path_bars = './Data/TQBR.ABIO_T1.txt'

df_bars = pd.read_csv(path_bars,sep='\t')
# df.info()

ticker = 'ABIO'
files = os.listdir('./images/')

filter_files = list(filter(lambda x: x.find(ticker) != -1, files))
# print(filter_files)
test_re1 = f'[{ticker}]'
test_re2 = '.png'
def get_time(filename:str):
    moment_time = re.sub(test_re1,"",filename)
    moment_time = re.sub(test_re2,"",moment_time)
    return float(moment_time)

print(get_time(filter_files[0]))

df_data = pd.DataFrame(columns=['img','time','price'])
df_data['img'] = filter_files
print(datetime.strptime(df_bars.iloc[0]['datetime'],'%d.%m.%Y %H:%M').timestamp())