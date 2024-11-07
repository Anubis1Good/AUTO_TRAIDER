import cv2
import numpy as np
from dataclasses import dataclass
from tas.BaseTA import BaseTA,Keys
from utils.chart_utils.indicators import get_bollinger_bands, get_SMA

@dataclass
class KeysWork(Keys):
    sma_sm:int
    bbd_sm:int
    bbu_sm:int
    bbu_attached:bool
    bbd_attached:bool
    over_bbd:bool
    over_bbu:bool
    stop_long:int
    stop_short:int
    direction:int
    take_long:int
    take_short:int

class STA1(BaseTA):
    def get_keys(self,img) -> KeysWork:
        region = self.trader.chart_region
        chart = self.trader._get_chart(img,region)
        candle_mask = self.trader._get_candle_mask(chart)
        volume_mask = self.trader._get_volume_mask(chart)
        candle_cords = self.trader._get_cords_on_mask(candle_mask)
        volume_cords = self.trader._get_cords_on_mask(volume_mask)
        half_bars = self.trader._get_half_bars(candle_mask,candle_cords,volume_cords)
        cur_price = self.trader._get_current_price(chart)
        mpts = np.array(list(map(lambda x: x.mpt,half_bars)))
        sma_sm,bbu_sm,bbd_sm = get_bollinger_bands(np.array(mpts))

        sma_low = get_SMA(mpts,50)
        sma_fast = get_SMA(mpts,10)

        direction = 1 if sma_low[-1][1] > sma_fast[-1][1] else -1
        bbu_attached = half_bars[-2].y_in_bar(bbu_sm[-1][1]) or half_bars[-1].y_in_bar(bbu_sm[-1][1])
        bbd_attached = half_bars[-2].y_in_bar(bbd_sm[-1][1]) or half_bars[-1].y_in_bar(bbd_sm[-1][1]) 
        over_bbu = half_bars[-1].yl < bbu_sm[-1][1]
        over_bbd = half_bars[-1].yh > bbd_sm[-1][1]


        volatility = list(map(lambda x: x.spred_pt,half_bars))
        volatility = get_SMA(np.array(volatility),14)

        stop_long = (half_bars[-1].x,half_bars[-1].yl+volatility[-1][1]*2)
        stop_short = (half_bars[-1].x,half_bars[-1].yh-volatility[-1][1]*2)

        take_long = (half_bars[-1].x,half_bars[-1].yh-volatility[-1][1]*3)
        take_short = (half_bars[-1].x,half_bars[-1].yl+volatility[-1][1]*3)

        if not self.trader.free_stop_l:
            stop_long = stop_long if stop_long[1] < self.trader.stop_long else (half_bars[-1].x,self.trader.stop_long)
            take_long = (half_bars[-1].x,self.trader.take_long)
        if not self.trader.free_stop_s:
            stop_short = stop_short if stop_short[1] > self.trader.stop_short else (half_bars[-1].x,self.trader.stop_short)
            take_short = (half_bars[-1].x,self.trader.take_short)
      
        keys = KeysWork(
            cur_price[1],
            sma_sm[-1][1],
            bbd_sm[-1][1],
            bbu_sm[-1][1],
            bbu_attached,
            bbd_attached,
            over_bbd,
            over_bbu,
            stop_long[1],
            stop_short[1],
            direction,
            take_long[1],
            take_short[1]
            )
            
        if self.trader.mode != 1:
            cv2.circle(chart,stop_long,1,(0,200,0),2)
            cv2.circle(chart,stop_short,1,(200,200,0),2)
            cv2.circle(chart,take_long,1,(0,250,100),1)
            cv2.circle(chart,take_short,1,(250,100,0),1)
            cv2.polylines(chart,[volatility],False,(200,200,0),1)
            cv2.polylines(chart,[sma_sm],False,(200,0,0),1)
            cv2.polylines(chart,[bbu_sm],False,(200,200,0),1)
            cv2.polylines(chart,[bbd_sm],False,(200,0,200),1)
            cv2.polylines(chart,[sma_low],False,(100,0,0),2)
            cv2.polylines(chart,[sma_fast],False,(160,217,100),2)

            cv2.putText(chart,"bbuAt: "+str(bbu_attached),(0,110),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,205,155),2)
            cv2.putText(chart,"bbdAt: "+str(bbd_attached),(0,130),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,205,155),2)
            cv2.putText(chart,"SUA: "+str(self.trader.bbu_attached),(0,165),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,205,155),2)
            cv2.putText(chart,"SDA: "+str(self.trader.bbd_attached),(0,180),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,205,155),2)

            # cv2.putText(chart,"Wave: "+str(wave),(0,110),cv2.FONT_HERSHEY_SIMPLEX,0.8,(155,205,155),2)
        return keys
    def get_action(self,keys:KeysWork):
        self.trader.stop_long = keys.stop_long
        self.trader.stop_short = keys.stop_short
        self.trader.take_long = keys.take_long
        self.trader.take_short = keys.take_short
        if keys.direction == -1:
            if keys.cur_price < keys.stop_short:
                return 'close_short'
            if keys.cur_price > keys.take_short and not keys.bbd_attached:
                return 'close_short'
            if not keys.bbd_attached and self.trader.bbd_attached:
                return 'close_short'
            if keys.over_bbd:
                return 'close_short'
            if keys.cur_price < keys.bbu_sm:
                self.free_stop = False
                return 'short'
            if keys.cur_price > keys.stop_long:
                return 'close_long'
        # long_context
        if keys.direction == 1:
            if keys.cur_price > keys.stop_long:
                return 'close_long'
            if keys.cur_price < keys.take_long and not keys.bbu_attached:
                return 'close_long'
            if not keys.bbu_attached and self.trader.bbu_attached:
                return 'close_long'
            if keys.over_bbu:
                return 'close_long'
            if keys.cur_price > keys.bbd_sm:
                self.free_stop = False
                return 'long'
            if keys.cur_price < keys.stop_short:
                return 'close_short'