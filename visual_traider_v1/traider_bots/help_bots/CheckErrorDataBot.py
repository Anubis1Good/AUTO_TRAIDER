import os
import cv2
import numpy as np
import numpy.typing as npt
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.ProSveT import ProSveT
from dataclasses import dataclass
from time import time 





class CED(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'CED'
        self.close_long = False
        self.close_short = False
        self.i = 0
        self.pred_coef = 14


    def _get_keys(self, img, region) -> dict:
        chart = self._get_chart(img,region)
        try:
            candle_mask = self._get_candle_mask(chart)
            volume_mask = self._get_volume_mask(chart)
            candle_cords = self._get_cords_on_mask(candle_mask)
            volume_cords = self._get_cords_on_mask(volume_mask)
            half_bars = self._get_half_bars(candle_mask,candle_cords,volume_cords)
            cur_price = self._get_current_price(chart)
            pst = ProSveT(half_bars)
            return 1
        except:
            return 0


        
    def _test(self, img,price):
        keys = self._get_keys(img,self.minute_chart_region)
        return keys
    
    def run(self, img, price=0):
        return self._test(img,price)


    
