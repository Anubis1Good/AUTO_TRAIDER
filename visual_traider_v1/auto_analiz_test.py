import os
import sys
import pandas as pd

file_name = 'test.json'
trader_name = 'PTA2_DDC_20'
if len(sys.argv) < 2:
    date = '01.08.24'
else:
    date = sys.argv[1]


df = pd.read_json(file_name)
# print(df.head())
def get_quity(row):
    # print(row)
    if row.pos == 'long':
        quity = row.close_price - row.open_price
    else:
        quity = row.open_price- row.close_price
    return quity
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