import pandas as pd
def _help_donchan_channel(row,period,df,point):
    if point == 1:
        if row.name < period:
            return -1
        return int(df.iloc[row.name-period:row.name+1]['yh'].min())
    if point == -1:
        if row.name < period:
            return -1
        return int(df.iloc[row.name-period:row.name+1]['yl'].max())
    

def get_df_donchan_channel(df:pd.DataFrame,period:int=20):
    df['up_dc'] = df.apply(lambda row: _help_donchan_channel(row,period,df,1),axis=1)
    df['down_dc'] = df.apply(lambda row: _help_donchan_channel(row,period,df,-1),axis=1)
    # df.info()
    df['middle_dc'] = df.apply(lambda row: (row['up_dc']+row['down_dc'])//2,axis=1)
    return df