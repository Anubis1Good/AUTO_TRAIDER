'''
Мультристратеговый бот на основе канала Дончана
'''
import cv2
import numpy as np
from tas.BaseTA import BaseTA,Keys
from utils.df_utils.indicators import get_df_donchan_channel
from utils.df_utils.draw_df import draw_df_dc
from utils.df_utils.strategy_df import *
from utils.df_utils.dtype_help import DataTest
from dataclasses import dataclass

@dataclass
class Keys:
    df:pd.DataFrame
    strategy: str

class PTA7_MS1(BaseTA):
    def __init__(self, trader,period:int=30,*args):
        super().__init__(trader,*args)
        self.period = period

    def get_keys(self, img)-> Keys:
        region = self.trader.chart_region
        chart = self.trader._get_chart(img,region)
        df = self.trader. _get_df(chart)
        df = get_df_donchan_channel(df,20)
        df_res = pd.DataFrame(columns=['name_strategy','equity','count'])
        strategies = ['DDC','EDDC','LDDC','SDDC','LEDDC','SEDDC']
        for strategy in strategies:
            data = eval(f"{strategy}(df)")
            df_res.loc[len(df_res)] = [strategy,data.equity,data.count]
        df_res['average_eq'] = df_res['equity'] / df_res['count']
        df_res =df_res.sort_values('equity',axis=0,ascending=False)

        if self.trader.mode in (2,0):
            df.apply(lambda row: draw_df_dc(row,chart),axis=1)
        
        return Keys(
            df,
            df_res.iloc[0]['name_strategy'])
    
    def get_action(self, keys:Keys):
        data_test = DataTest(0,0,0,0)
        return eval(f"help_{keys.strategy}(keys.df.iloc[-1],data_test)")