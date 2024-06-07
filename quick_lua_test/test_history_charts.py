
# import required packages
import mplfinance as mpf
import pandas as pd

def prepare_data(path_file:str):
    df = pd.read_csv(path_file,sep='\t')
    df = df.iloc[-30:]
    df.rename(columns={'datetime':'Date'},inplace=True)
    columns = list(df.columns)
    columns = list(map(str.capitalize,columns))
    df.columns = columns
    df.index = pd.DatetimeIndex(df['Date'])
    return df 

def prepare_ticker(ticker:str):
    return f'./DATA/TQBR.{ticker}_D1.txt'

tickers_name = ['VTBR','SBER','GAZP']

tickers = list(map(prepare_ticker,tickers_name))
tickers = list(map(prepare_data,tickers))
# i = 0
# mpf.plot(tickers[i],title='\n'+tickers_name[i])
tickers[0].info()
fig = mpf.figure(figsize=(12,9))

ax1 = fig.add_subplot(2,3,1)
ax2 = fig.add_subplot(2,3,2)
ax3 = fig.add_subplot(2,3,3)

av1 = fig.add_subplot(3,3,7,sharex=ax1)
av2 = fig.add_subplot(3,3,8,sharex=ax1)
av3 = fig.add_subplot(3,3,9,sharex=ax3)

i = 0
while i < len(tickers_name):
    mpf.plot(tickers[i],ax=eval(f'ax{i+1}'),volume=eval(f'av{i+1}'),axtitle=tickers_name[i])
    i +=1

mpf.show()
