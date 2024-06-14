import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
def prepare_data(path_file:str):
    df = pd.read_csv(path_file,sep='\t')
    # df = df.iloc[-100:]
    df.rename(columns={'datetime':'Date'},inplace=True)
    columns = list(df.columns)
    columns = list(map(str.capitalize,columns))
    df.columns = columns
    # df.index = pd.DatetimeIndex(df['Date'])
    return df 

def prepare_ticker(ticker:str):
    return f'./DATA/TQBR.{ticker}_D1.txt'

tickers_name = ['VTBR','SBER','GAZP','ROSN']
ticker_on_folder = os.listdir('Data')

index = 0
tickers = list(map(prepare_ticker,tickers_name))
ticker = prepare_data(f'./DATA/{ticker_on_folder[index]}')
x=ticker.index
y=ticker.Close

plt.figure(figsize=(11,6))
slope, intercept, r, p, std_err = stats.linregress(x, y)

def myfunc(x,offset):
  return slope * x + intercept+offset

print(slope)

mymodel = list(map(lambda x:myfunc(x,0), x))
top_border = list(map(lambda x:myfunc(x,y.std()), x))
bottom_border = list(map(lambda x:myfunc(x,-y.std()), x))


plt.plot(x,y)
plt.plot(x, mymodel,color='r')
plt.plot(x, top_border,color='g')
plt.plot(x, bottom_border,color='g')
plt.title(ticker_on_folder[index])
plt.show()