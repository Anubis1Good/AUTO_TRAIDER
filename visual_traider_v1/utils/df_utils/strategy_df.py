import pandas as pd
from utils.df_utils.dtype_help import DataTest
def help_DDC(row,data:DataTest):
    if row['yh'] == row['up_dc']:
        if data.pos == 0:
            data.pos = -1
            data.price = row['yh']
        elif data.pos == 1:
            data.pos = -1
            data.equity += data.price - row['yh']  
            data.price = row['yh']
            data.count += 1
        return 'short'
    elif row['yl'] == row['down_dc']:
        if data.pos == 0:
            data.pos = 1
            data.price = row['yl']
        elif data.pos == -1:
            data.pos = 1
            data.equity += row['yl'] - data.price 
            data.price = row['yl']
            data.count += 1
        return 'long'
    else:
        if row['yl'] >= row['middle_dc']:
            if data.pos == -1:
                data.pos = 0
                data.equity += row['yl'] - data.price
                data.count += 1
            return 'close_short'
        if row['yh'] <= row['middle_dc']:
            if data.pos == 1:
                data.pos = 0
                data.equity += data.price - row['yh']  
                data.count += 1
            return 'close_long'



def DDC(df:pd.DataFrame):
    data = DataTest(0,0,0,0)
    df.apply(lambda row: help_DDC(row,data),axis=1)
    return data

def help_EDDC(row,data:DataTest):
    if row['yh'] == row['up_dc']:
        if data.pos == 0:
            data.pos = -1
            data.price = row['yh']
        elif data.pos == 1:
            data.pos = -1
            data.equity += data.price - row['yh']  
            data.price = row['yh']
            data.count += 1
        return 'short'
    elif row['yl'] == row['down_dc']:
        if data.pos == 0:
            data.pos = 1
            data.price = row['yl']
        elif data.pos == -1:
            data.pos = 1
            data.equity += row['yl'] - data.price 
            data.price = row['yl']
            data.count += 1
        return 'long'

def EDDC(df:pd.DataFrame):
    data = DataTest(0,0,0,0)
    df.apply(lambda row: help_EDDC(row,data),axis=1)
    return data

def help_LDDC(row,data:DataTest):
    if row['yl'] == row['down_dc']:
        if data.pos == 0:
            data.pos = 1
            data.price = row['yl']
        elif data.pos == -1:
            data.pos = 1
            data.equity += row['yl'] - data.price 
            data.price = row['yl']
            data.count += 1
        return 'long'
    else:
        if row['yl'] >= row['middle_dc']:
            if data.pos == -1:
                data.pos = 0
                data.equity += row['yl'] - data.price
                data.count += 1
            return 'close_short'
        if row['yh'] <= row['middle_dc']:
            if data.pos == 1:
                data.pos = 0
                data.equity += data.price - row['yh']  
                data.count += 1
            return 'close_long'



def LDDC(df:pd.DataFrame):
    data = DataTest(0,0,0,0)
    df.apply(lambda row: help_LDDC(row,data),axis=1)
    return data

def help_SDDC(row,data:DataTest):
    if row['yh'] == row['up_dc']:
        if data.pos == 0:
            data.pos = -1
            data.price = row['yh']
        elif data.pos == 1:
            data.pos = -1
            data.equity += data.price - row['yh']  
            data.price = row['yh']
            data.count += 1
        return 'short'
    else:
        if row['yl'] >= row['middle_dc']:
            if data.pos == -1:
                data.pos = 0
                data.equity += row['yl'] - data.price
                data.count += 1
            return 'close_short'
        if row['yh'] <= row['middle_dc']:
            if data.pos == 1:
                data.pos = 0
                data.equity += data.price - row['yh']  
                data.count += 1
            return 'close_long'



def SDDC(df:pd.DataFrame):
    data = DataTest(0,0,0,0)
    df.apply(lambda row: help_SDDC(row,data),axis=1)
    return data

def help_LEDDC(row,data:DataTest):
    if row['yh'] == row['up_dc']:
        if data.pos == 1:
            data.pos = 0
            data.equity += data.price - row['yh']  
            data.count += 1
        return 'close_long'
    elif row['yl'] == row['down_dc']:
        if data.pos == 0:
            data.pos = 1
            data.price = row['yl']
        elif data.pos == -1:
            data.pos = 1
            data.equity += row['yl'] - data.price 
            data.price = row['yl']
            data.count += 1
        return 'long'

def LEDDC(df:pd.DataFrame):
    data = DataTest(0,0,0,0)
    df.apply(lambda row: help_LEDDC(row,data),axis=1)
    return data

def help_SEDDC(row,data:DataTest):
    if row['yh'] == row['up_dc']:
        if data.pos == 0:
            data.pos = -1
            data.price = row['yh']
        elif data.pos == 1:
            data.pos = -1
            data.equity += data.price - row['yh']  
            data.price = row['yh']
            data.count += 1
        return 'short'
    elif row['yl'] == row['down_dc']:
        if data.pos == -1:
            data.pos = 0
            data.equity += row['yl'] - data.price 
            data.count += 1
        return 'close_short'

def SEDDC(df:pd.DataFrame):
    data = DataTest(0,0,0,0)
    df.apply(lambda row: help_SEDDC(row,data),axis=1)
    return data