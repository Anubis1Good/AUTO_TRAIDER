import os
import sys
import json
import pandas as pd

fast_test_env = True

if fast_test_env:
    file_name = 'test_files/fast_test.json'
else:
    file_name = 'test.json'

if len(sys.argv) < 2:
    date = '31.07.24'
else:
    date = sys.argv[1]
if len(sys.argv) < 3:
    trader_name = 'ST2'
else:
    trader_name = sys.argv[2]

with open('test_files\last_price.json') as f:
    last_prices = json.load(f)


df = pd.read_json(file_name)

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
    lp = last_prices[date]
    df.close_price = df.apply(lambda row:change_cp(row,lp),axis=1)
    df['quity'] = df.apply(get_quity,axis=1)
    df['percent'] = round(df['quity'] / df['open_price'],4)*100
    res = df.groupby('name')['quity'].agg(['sum','count'])
    res = res.sort_values(by='count',axis=0,ascending=False)
    res['part'] = res['sum'] / res['count']
    res['total_percent'] = df.groupby('name')['percent'].agg(['sum'])['sum']
    res['average_percent'] = round(res['total_percent']/ res['count'],2)
    path_output = os.path.join('test_results',trader_name + '_' + date + "_output.xlsx")
    with pd.ExcelWriter(path_output) as writer:  
        df.to_excel(writer,sheet_name='total') 
        res.to_excel(writer,sheet_name='sum_count') 
except:
    print('not data')