import pandas as pd 



df = pd.read_csv('./Data/TQBR.ABIO_T1.txt',sep='\t')
# print(df.head())
df.drop(['datetime','open','close'],axis=1,inplace=True)


def xy_generator(df):
    for step in range(df.shape[0]-10):
        X = df.iloc[step:step+10]
        Y = df.iloc[step+10]
        yield X,Y
    return
gen = xy_generator(df)
print(next(gen))
print(next(gen))
print(next(gen))

