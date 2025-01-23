'''
workBot
'''
import pandas as pd
import numpy as np
import cv2
from tas.BaseTA import BaseTA,Keys
from utils.chart_utils.indicators import *
from utils.chart_utils.VSA import VSA
from utils.df_utils.indicators import *
from utils.df_utils.draw_df import *
from utils.df_utils.strategy_df import *
from utils.df_utils.dtype_help import DataTest
from utils.test_utils.test_draws_funcs import draw_bollinger
from utils.ML_utils.cls_utils import most_similar_point_cs,most_similar_point_cs_mult,most_similar_relative_point_cs,most_similar_relative_point_cs_mult
from dataclasses import dataclass



class WorkTA(BaseTA):
    def __init__(self, trader,period=10,*args):
        super().__init__(trader,*args)
        self.period = period
    def get_keys(self, img)-> Keys:
        region = self.trader.chart_region
        chart = self.trader._get_chart(img,region)
        # candle_mask = self.trader._get_candle_mask(chart)
        # volume_mask = self.trader._get_volume_mask(chart)
        # candle_cords = self.trader._get_cords_on_mask(candle_mask)
        # volume_cords = self.trader._get_cords_on_mask(volume_mask)
        df = self.trader. _get_df(chart)
        print(df.head())
        df.info()
        df = get_df_donchan_channel(df,20)
        df.info()
        print(df.tail())
        df.apply(lambda row: draw_df_dc(row,chart),axis=1)
        df_res = pd.DataFrame(columns=['name_strategy','equity','count'])
        strategies = ['DDC','EDDC','LDDC','SDDC','LEDDC','SEDDC']
        for strategy in strategies:
            data = eval(f"{strategy}(df)")
            df_res.loc[len(df_res)] = [strategy,data.equity,data.count]
        # print('DDC:')
        # data = DDC(df)
        # df_res.loc[len(df_res)] = ['DDC',data.equity,data.count]
        # data = EDDC(df)
        # df_res.loc[len(df_res)] = ['EDDC',data.equity,data.count]
        # data = LDDC(df)
        # df_res.loc[len(df_res)] = ['LDDC',data.equity,data.count]
        # data = SDDC(df)
        # df_res.loc[len(df_res)] = ['SDDC',data.equity,data.count]
        # data = LEDDC(df)
        # df_res.loc[len(df_res)] = ['LEDDC',data.equity,data.count]
        # data = SEDDC(df)
        # df_res.loc[len(df_res)] = ['SEDDC',data.equity,data.count]
        df_res['average_eq'] = df_res['equity'] / df_res['count']
        # print(df_res.head(10))
        df_res =df_res.sort_values('equity',axis=0,ascending=False)
        print(df_res.head(10))
        print(df_res.iloc[0]['name_strategy'])
        data_test = DataTest(0,0,0,0)
        print(eval(f"help_{df_res.iloc[0]['name_strategy']}(df.iloc[-1],data_test)"))

        

        # half_bars = self.trader._get_half_bars(candle_mask,candle_cords,volume_cords)
        # dhbs = self.trader._get_dir_half_bars(chart,volume_cords)
        # for i,dhb in enumerate(dhbs):
        #     # if i % 10 == 0:
        #     #     cv2.putText(chart,str(i),(dhb.x,100),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255))
        #     # print(dhb.x,dhb.direction)
        #     color = (0,255,0) if dhb.direction == 1 else (100,100,255)
        #     cv2.polylines(chart,[dhb.draw_line],False,color,1)
        cur_price = self.trader._get_current_price(chart)
        # distance_per_hb = half_bars[1].x - half_bars[0].x
        # print(distance_per_hb)
        # hpts = np.array(list(map(lambda x: x.hpt,half_bars)))
        # lpts = np.array(list(map(lambda x: x.lpt,half_bars)))
        # yms = np.array(list(map(lambda x: x.ym,half_bars)))
        # ups,downs,middle = get_donchan_channel(half_bars,self.period)
        # delta_up = get_mean_delta(ups,half_bars,self.period,1)
        # ups_delta = np.array(list(map(lambda p: (p[0],p[1]-delta_up),ups)))
        # delta_down = get_mean_delta(downs,half_bars,self.period,-1)
        # downs_delta = np.array(list(map(lambda p: (p[0],p[1]-delta_down),downs)))

        # up_rotate = []
        # for i,up in enumerate(ups):
        #     if i == 0:
        #         continue
        #     if i == len(ups)-1:
        #         continue
        #     if ups[i-1][1] > up[1] == ups[i+1][1]:
        #         up_rotate.append(up)
        # for up in up_rotate:
        #     cv2.circle(chart,up,1,(0,200,100),2)
        # down_rotate = []
        # for i,down in enumerate(downs):
        #     if i == 0:
        #         continue
        #     if i == len(downs)-1:
        #         continue
        #     if downs[i-1][1] < down[1] == downs[i+1][1]:
        #         down_rotate.append(down)
        # for down in down_rotate:
        #     cv2.circle(chart,down,1,(200,200,100),2)
        # ms_i = most_similar_relative_point_cs(yms)
        # # ms_i2 = most_similar_point_cs(yms)
        # ms_i2 = most_similar_relative_point_cs_mult(half_bars)
        # h_out,l_out = get_projection(half_bars[ms_i+11:ms_i+21],half_bars[ms_i+10],half_bars[-1])
        # ms_i = most_similar_point_cs(yms)
        # maxs,mins =  get_williams_fractals(hpts,lpts,is_qual=True,n=6)
        # maxs = clear_fractals(maxs)
        # mins = clear_fractals(mins,False)
        # mean_maxs = maxs[:,0].mean()
        # mean_mins = mins[:,0].mean()
        # print(mean_maxs,mean_maxs//distance_per_hb)
        # print(mean_mins,mean_mins//distance_per_hb)
        # mean_all = int(mean_maxs//distance_per_hb + mean_mins//distance_per_hb)//2
        # print(mean_all)
        # print(check_michael_harris_pattern(half_bars))
        # print(check_michael_harris_pattern(half_bars,False))
        # vsa = VSA(half_bars)
        # vsa.draw_all(chart)
        # # volatility = np.array(list(map(lambda x: x.spred,half_bars)))
        # mpts = np.array(list(map(lambda x: x.mpt,half_bars)))
        # # volatility = np.mean(volatility)
        # # bullish_FGV,bearish_FGV = get_FVG(half_bars,volatility,2)
        # max_hb,min_hb,middle_hb = get_donchan_channel_lite(half_bars[ms_i+10:ms_i+20],10)
        # max_hb,min_hb,middle_hb = get_donchan_channel_lite(half_bars,60)
        # up,down,mup,mdown = get_van_gerchick_p(max_hb,min_hb,middle_hb)
        # # bbm,bbu,bbd = get_bollinger_bands(mpts)
        # rsi = get_rsi(half_bars)
        # # siu,sid = get_strong_index(half_bars)
        # ri,mi = get_rocket_meteor_index(half_bars,14)
        # # sma = get_SMA(np.array(list(map(lambda x: x.mpt,half_bars))))
        # print(rsi)
        # print(ri[-1][1])
        # print(mi[-1][1])
        # if ri[-1][1] > 60:
        #     print('long')
        # elif mi[-1][1] > 60:
        #     print('short')
        # else:
        #     print('range')
        if self.trader.mode in (2,0):
            1
            # cv2.polylines(chart,[half_bars[ms_i].draw_line],False,(55,155,255),2)
            # cv2.polylines(chart,[half_bars[ms_i+10].draw_line],False,(55,155,255),2)
            # cv2.polylines(chart,[half_bars[ms_i2].draw_line],False,(255,55,55),2)
            # cv2.polylines(chart,[half_bars[ms_i2+10].draw_line],False,(255,55,55),2)
            # cv2.polylines(chart,[half_bars[-1].draw_line],False,(0,255,0),2)
            # cv2.polylines(chart,[half_bars[-11].draw_line],False,(0,255,0),2)

            # cv2.circle(chart,(half_bars[-1].x,h_out),1,(100,255,0),2)
            # cv2.circle(chart,(half_bars[-1].x,l_out),1,(255,50,0),2)
            # cv2.circle(chart,(half_bars[-1].x,up),1,(0,255,0))
            # cv2.circle(chart,(half_bars[-1].x,down),1,(255,0,0))
            # cv2.circle(chart,(half_bars[-1].x,mup),1,(0,255,255))
            # cv2.circle(chart,(half_bars[-1].x,mdown),1,(255,0,255))
            # cv2.circle(chart,(half_bars[-1].x,max_hb),1,(255,255,255),2)
            # cv2.circle(chart,(half_bars[-1].x,min_hb),1,(255,255,255),2)
            # cv2.circle(chart,(half_bars[-1].x,middle_hb),1,(255,255,255),2)
            # # vsa.draw_all(chart)
            # cv2.polylines(chart,[ups_delta],False,(205,50,100),1)
            # cv2.polylines(chart,[downs_delta],False,(40,150,200),1)
            # cv2.polylines(chart,[ups],False,(255,0,200),1)
            # cv2.polylines(chart,[downs],False,(55,200,250),1)
            # cv2.polylines(chart,[middle],False,(155,100,250),1)
            # for p in maxs:
            #     cv2.circle(chart,p,1,(0,200,100),2)
            # for p in mins:
            #     cv2.circle(chart,p,1,(255,100,150),2)
            # cv2.polylines(chart,[maxs],False,(0,200,100),2)
            # cv2.polylines(chart,[mins],False,(255,100,150),2)
            # draw_bollinger(chart,bbm,bbu,bbd,thickness=2)
            # for pl in [ups,downs,middle]:
            #     cv2.polylines(chart,[pl],False,(0,200,0))
            # cv2.polylines(chart,[middle],False,(155,100,250),2)
            # cv2.polylines(chart,[sma],False,(255,100,0),1)
            # for zone in bullish_FGV:
            #     cv2.rectangle(chart,zone[0],zone[1],(0,255,0),1)
            #     cv2.line(chart,zone[0],(zone[0][0]+200,zone[0][1]),(0,255,0))
            # for zone in bearish_FGV:
            #     cv2.rectangle(chart,zone[0],zone[1],(0,100,255),1)
            #     cv2.line(chart,zone[0],(zone[0][0]+200,zone[0][1]),(0,100,255))
            1

        return Keys(
            cur_price=cur_price[1],

        )

    def get_action(self, keys:Keys):
        pass
